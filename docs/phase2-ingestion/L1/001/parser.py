"""Parse preserved FRED DFII10 observations for L1-001."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PARSER_VERSION = "0.1.0"
VARIABLE_ID = "L1-001"
SERIES_ID = "DFII10"
OUTPUT_FIELDS = [
    "variable_id", "observation_date", "value", "unit", "source_name",
    "source_series_id", "raw_file_path", "raw_sha256", "retrieved_at",
    "validation_status", "availability_status", "parser_version",
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_observations(raw_path: Path) -> list[dict[str, Any]]:
    payload = json.loads(raw_path.read_text(encoding="utf-8"))
    observations = payload.get("observations") if isinstance(payload, dict) else None
    if not isinstance(observations, list):
        raise ValueError("raw FRED file does not contain an observations list")
    return observations


def parse_observations(raw_path: Path, *, retrieved_at: str | None = None,
                       stale_after_days: int = 7) -> list[dict[str, Any]]:
    observations = load_observations(raw_path)
    raw_hash = sha256_file(raw_path)
    now = datetime.now(timezone.utc)
    retrieved = retrieved_at or now.isoformat()
    rows = []
    for item in observations:
        date_text = str(item.get("date", ""))
        value_text = item.get("value")
        if value_text in (None, "", "."):
            continue
        if not date_text:
            raise ValueError(f"invalid FRED observation: {item}")
        try:
            observation_date = datetime.strptime(date_text, "%Y-%m-%d").date()
            value = float(value_text)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"invalid FRED observation: {item}") from exc
        if not -10 <= value <= 20:
            validation = "FLAG"
        else:
            validation = "PASS"
        age_days = (now.date() - observation_date).days
        availability = "STALE" if age_days > stale_after_days else "AVAILABLE"
        rows.append({
            "variable_id": VARIABLE_ID,
            "observation_date": observation_date.isoformat(),
            "value": value,
            "unit": "percent",
            "source_name": "FRED",
            "source_series_id": SERIES_ID,
            "raw_file_path": str(raw_path),
            "raw_sha256": raw_hash,
            "retrieved_at": retrieved,
            "validation_status": validation,
            "availability_status": availability,
            "parser_version": PARSER_VERSION,
        })
    if not rows:
        raise ValueError("raw FRED file contains no observations")
    return rows


def write_csv(rows: list[dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Parse FRED DFII10 observations for L1-001")
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("data/processed/L1_001_observations.csv"))
    parser.add_argument("--retrieved-at")
    parser.add_argument("--stale-after-days", type=int, default=7)
    args = parser.parse_args(argv)
    rows = parse_observations(args.raw, retrieved_at=args.retrieved_at,
                              stale_after_days=args.stale_after_days)
    write_csv(rows, args.output)
    print(f"Wrote {len(rows)} observations to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
