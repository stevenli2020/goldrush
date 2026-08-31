"""Collect and validate IMF monthly gold-holdings history for L0-002.

The current WGC workbook remains the approved snapshot route.  This collector
adds a separately auditable IMF/OpenBB history for Phase 4 research and keeps
the raw provider response beside the processed observations.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
from openbb import obb


LOGGER = logging.getLogger("l0_002_historical")
VARIABLE_ID = "L0-002"
SYMBOL = "IL::RGV_REVS"
FREQUENCY = "month"
START_DATE = "2000-01-01"
OUNCE_TO_TONNES = 31.1034768 / 1_000_000
PARSER_VERSION = "1.0.0"
MAX_ALL_COUNTRY_ROWS = 100_000

ROOT = Path(__file__).resolve().parents[4]
SNAPSHOT_PATH = ROOT / "docs/phase2-ingestion/L0/002/processed/L0_002_observations.csv"
RAW_DIR = ROOT / "docs/phase2-ingestion/data/imf/raw"
OUTPUT_PATH = ROOT / "docs/phase2-ingestion/L0/002/processed/L0_002_historical_observations.csv"

OUTPUT_COLUMNS = [
    "variable_id",
    "country",
    "holdings_tonnes",
    "unit",
    "source_file",
    "source_publication_date",
    "download_date",
    "ingested_at",
    "validation_status",
    "availability_status",
    "parser_version",
]

# IMF ISO3 identifiers for the snapshot panel and its aggregate rows.  The
# all-country request normally avoids this path; it is retained for a bounded
# retry if the wildcard response is unavailable or too large.
FALLBACK_CODES = {
    "United States": "USA",
    "Germany": "DEU",
    "IMF": "IMF",
    "Italy": "ITA",
    "France": "FRA",
    "China, P.R.: Mainland": "CHN",
    "Russian Federation": "RUS",
    "Switzerland": "CHE",
    "India": "IND",
    "Japan": "JPN",
    "Poland, Rep. of": "POL",
    "Netherlands, The": "NLD",
    "Turkey5)": "TUR",
    "ECB": "EZB",
    "Uzbekistan, Rep. of": "UZB",
    "Taiwan Province of China": "TWN",
    "Portugal": "PRT",
    "Kazakhstan, Rep. of": "KAZ",
    "Saudi Arabia": "SAU",
    "United Kingdom": "GBR",
    "Lebanon": "LBN",
    "Spain": "ESP",
    "Austria": "AUT",
    "Thailand": "THA",
    "Belgium": "BEL",
    "Singapore": "SGP",
    "Azerbaijan, Rep. of8)": "AZE",
    "Iraq": "IRQ",
    "Algeria": "DZA",
    "Brazil": "BRA",
    "Venezuela, Republica Bolivariana de": "VEN",
    "Libya": "LBY",
    "Philippines": "PHL",
    "Egypt, Arab Rep. of": "EGY",
    "Sweden": "SWE",
    "South Africa": "ZAF",
    "Mexico": "MEX",
    "Qatar": "QAT",
    "Greece": "GRC",
    "Hungary": "HUN",
    "Korea, Rep. of": "KOR",
    "Romania": "ROU",
    "BIS2)": "BIS",
    "Indonesia": "IDN",
    "Czech Rep.": "CZE",
    "Australia": "AUS",
    "Kuwait": "KWT",
    "Jordan": "JOR",
    "United Arab Emirates": "ARE",
    "Denmark": "DNK",
    "World6)": "W00",
    "Euro Area (incl. ECB)": "EZB",
}

IMF_COUNTRY_ALIASES = {
    "Azerbaijan, Republic of": "Azerbaijan, Rep. of8)",
    "Bank for International Settlements (BIS)": "BIS2)",
    "China, People's Republic of": "China, P.R.: Mainland",
    "Czech Republic": "Czech Rep.",
    "Egypt, Arab Republic of": "Egypt, Arab Rep. of",
    "European Central Bank (ECB)": "ECB",
    "Euro Area (EA)": "Euro Area (incl. ECB)",
    "International Monetary Fund (IMF)": "IMF",
    "Kazakhstan, Republic of": "Kazakhstan, Rep. of",
    "Korea, Republic of": "Korea, Rep. of",
    "Poland, Republic of": "Poland, Rep. of",
    "Türkiye, Republic of": "Turkey5)",
    "Uzbekistan, Republic of": "Uzbekistan, Rep. of",
    "Venezuela, República Bolivariana de": "Venezuela, Republica Bolivariana de",
    "World": "World6)",
}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _json_value(value: Any) -> Any:
    if isinstance(value, (datetime, pd.Timestamp)):
        return value.isoformat()
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if pd.isna(value):
        return None
    return value.item() if hasattr(value, "item") else value


def _response_frame(response: Any) -> pd.DataFrame:
    frame = response.to_dataframe()
    if not isinstance(frame, pd.DataFrame) or frame.empty:
        raise ValueError("OpenBB returned no data")
    frame = frame.reset_index()
    required = {"date", "country", "value"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"OpenBB response is missing columns: {sorted(missing)}")
    return frame


def _fetch(country: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    response = obb.economy.indicators(
        symbol=SYMBOL,
        country=country,
        provider="imf",
        frequency=FREQUENCY,
        start_date=START_DATE,
    )
    frame = _response_frame(response)
    extra = getattr(response, "extra", {}) or {}
    metadata = {
        "provider": "imf",
        "symbol": SYMBOL,
        "frequency": FREQUENCY,
        "start_date": START_DATE,
        "country_request": country,
        "response_metadata": {
            "results_metadata": _json_value(extra.get("results_metadata", {})),
            "arguments": _json_value(extra.get("arguments", {})),
        },
    }
    return frame, metadata


def _snapshot_countries(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [row["country"] for row in csv.DictReader(handle) if row.get("country")]


def _fetch_history(snapshot_countries: list[str]) -> tuple[pd.DataFrame, dict[str, Any]]:
    try:
        frame, metadata = _fetch("*")
        if len(frame) > MAX_ALL_COUNTRY_ROWS:
            raise ValueError(
                f"wildcard response has {len(frame)} rows; limit is {MAX_ALL_COUNTRY_ROWS}"
            )
        metadata["fetch_mode"] = "all_countries"
        return frame, metadata
    except Exception as exc:  # noqa: BLE001 - bounded provider fallback
        LOGGER.warning("Wildcard IMF request failed; using country fallback: %s", exc)
        frames: list[pd.DataFrame] = []
        failures: dict[str, str] = {}
        for name in snapshot_countries:
            code = FALLBACK_CODES.get(name)
            if not code:
                failures[name] = "no IMF ISO3 mapping"
                continue
            try:
                frame, _ = _fetch(code)
                frames.append(frame)
            except Exception as country_exc:  # noqa: BLE001 - retain per-country evidence
                failures[name] = str(country_exc)
        if not frames:
            raise RuntimeError(f"all IMF fallback requests failed: {failures}") from exc
        return pd.concat(frames, ignore_index=True), {
            "provider": "imf",
            "symbol": SYMBOL,
            "frequency": FREQUENCY,
            "start_date": START_DATE,
            "country_request": "fallback",
            "fetch_mode": "snapshot_countries",
            "fallback_failures": failures,
        }


def _normalise_date(value: Any) -> str:
    return pd.Timestamp(value).date().isoformat()


def _validate(rows: list[dict[str, Any]], expected_countries: set[str]) -> dict[str, Any]:
    by_key: dict[tuple[str, str], int] = {}
    by_country: dict[str, set[pd.Timestamp]] = {}
    reasons: list[str] = []
    for row in rows:
        key = (row["country"], row["source_publication_date"])
        by_key[key] = by_key.get(key, 0) + 1
        by_country.setdefault(row["country"], set()).add(
            pd.Timestamp(row["source_publication_date"])
        )
        value = float(row["holdings_tonnes"])
        if not math.isfinite(value):
            reasons.append(f"non-finite value for {row['country']} {key[1]}")
        elif value < 0:
            reasons.append(f"negative value for {row['country']} {key[1]}")

    duplicate_keys = [key for key, count in by_key.items() if count > 1]
    if duplicate_keys:
        reasons.append(f"duplicate rows: {len(duplicate_keys)} country/date keys")

    observed_countries = set(by_country)
    missing_countries = sorted(expected_countries - observed_countries)
    if missing_countries:
        reasons.append("missing countries: " + ", ".join(missing_countries))

    continuity_gaps: dict[str, int] = {}
    for country, dates in by_country.items():
        if len(dates) < 2:
            continue
        expected = pd.date_range(min(dates), max(dates), freq="ME")
        gaps = len(set(expected) - dates)
        if gaps:
            continuity_gaps[country] = gaps
    if continuity_gaps:
        reasons.append(
            "internal monthly gaps: "
            + ", ".join(f"{country} ({count})" for country, count in sorted(continuity_gaps.items()))
        )

    return {
        "reasons": reasons,
        "missing_countries": missing_countries,
        "duplicate_keys": duplicate_keys,
        "continuity_gaps": continuity_gaps,
        "observed_country_count": len(observed_countries),
        "expected_country_count": len(expected_countries),
    }


def collect(snapshot_path: Path = SNAPSHOT_PATH, output_path: Path = OUTPUT_PATH) -> dict[str, Any]:
    snapshot_countries = _snapshot_countries(snapshot_path)
    expected_countries = set(snapshot_countries)
    frame, fetch_metadata = _fetch_history(snapshot_countries)
    raw_frame = frame.copy()
    # Keep the same 52-country panel as the canonical snapshot.  Country names
    # are the IMF display identifiers, retained in the processed country field.
    frame["country"] = frame["country"].replace(IMF_COUNTRY_ALIASES)
    frame = frame[frame["country"].isin(expected_countries)].copy()
    if frame.empty:
        raise ValueError("IMF response contained no snapshot-panel countries")

    ingested_at = _utc_now()
    download_date = ingested_at.date().isoformat()
    raw_name = f"l0_002_imf_{ingested_at.strftime('%Y%m%dT%H%M%SZ')}.json"
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    raw_payload = {
        **fetch_metadata,
        "retrieved_at": ingested_at.isoformat(),
        "conversion": {
            "from": "fine_troy_ounces",
            "to": "metric_tonnes",
            "factor": OUNCE_TO_TONNES,
            "provider_unit_label": "Volume in millions of fine troy ounces",
        },
        "records": [
            {str(key): _json_value(value) for key, value in row.items()}
            for row in raw_frame.to_dict(orient="records")
        ],
    }
    (RAW_DIR / raw_name).write_text(
        json.dumps(raw_payload, ensure_ascii=False, indent=2, default=_json_value),
        encoding="utf-8",
    )

    rows: list[dict[str, Any]] = []
    for record in frame.to_dict(orient="records"):
        raw_value = float(record["value"])
        rows.append(
            {
                "variable_id": VARIABLE_ID,
                "country": str(record["country"]),
                "holdings_tonnes": raw_value * OUNCE_TO_TONNES,
                "unit": "metric_tonnes",
                "source_file": raw_name,
                "source_publication_date": _normalise_date(record["date"]),
                "download_date": download_date,
                "ingested_at": ingested_at.isoformat(),
                "validation_status": "PENDING",
                "availability_status": "AVAILABLE",
                "parser_version": PARSER_VERSION,
            }
        )

    validation = _validate(rows, expected_countries)
    validation_status = "PASS" if not validation["reasons"] else "FAIL: " + "; ".join(validation["reasons"])
    for row in rows:
        row["validation_status"] = validation_status
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    return {
        "raw_path": str(RAW_DIR / raw_name),
        "output_path": str(output_path),
        "row_count": len(rows),
        "validation": validation,
        "validation_status": validation_status,
        "fetch_metadata": fetch_metadata,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, default=SNAPSHOT_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level.upper()), format="%(levelname)s %(message)s")
    result = collect(args.snapshot, args.output)
    print(json.dumps(result, indent=2, default=_json_value))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
