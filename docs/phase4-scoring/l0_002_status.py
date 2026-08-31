"""Aggregate monthly central-bank gold holdings into an L0-002 signal."""
from __future__ import annotations

import csv
import math
from calendar import monthrange
from datetime import date
from pathlib import Path
from typing import Any


VARIABLE_ID = "L0-002"
UNIT = "metric_tonnes"
HORIZONS = ("1-5 days", "1-3 months", "1-3 years", "3-10 years")
LOOKBACK_MONTHS = {"1-3 years": 36, "3-10 years": 120}
ALLOWED_STATUSES = {"AVAILABLE", "FLAG", "STALE", "BLOCKED"}
DEFAULT_HISTORY_PATH = (
    Path(__file__).resolve().parents[1]
    / "phase2-ingestion/L0/002/processed/L0_002_historical_observations.csv"
)


def _month_key(value: str) -> tuple[int, int]:
    parsed = date.fromisoformat(value)
    return parsed.year, parsed.month


def _month_index(key: tuple[int, int]) -> int:
    return key[0] * 12 + key[1]


def _month_timestamp(key: tuple[int, int]) -> str:
    year, month = key
    day = monthrange(year, month)[1]
    return f"{year:04d}-{month:02d}-{day:02d}T00:00:00Z"


def read_l0_002(path: str | Path = DEFAULT_HISTORY_PATH) -> list[dict[str, Any]]:
    """Read the monthly country panel used by the aggregate scorer."""
    try:
        with Path(path).open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except OSError as exc:
        raise ValueError("L0-002 historical holdings is not readable CSV") from exc
    if not rows:
        raise ValueError("L0-002 historical holdings must contain records")

    seen: set[tuple[str, tuple[int, int]]] = set()
    validated: list[dict[str, Any]] = []
    for row in rows:
        if row.get("variable_id") != VARIABLE_ID:
            raise ValueError("L0-002 historical record variable_id must be L0-002")
        country = str(row.get("country", "")).strip()
        if not country:
            raise ValueError("L0-002 historical country is required")
        if row.get("unit") != UNIT:
            raise ValueError("L0-002 historical unit must be metric_tonnes")
        if row.get("availability_status") not in ALLOWED_STATUSES:
            raise ValueError("invalid L0-002 availability_status")
        try:
            value = float(row.get("holdings_tonnes"))
        except (TypeError, ValueError) as exc:
            raise ValueError("L0-002 holdings_tonnes must be numeric") from exc
        if not math.isfinite(value) or value < 0:
            raise ValueError("L0-002 holdings_tonnes must be finite and non-negative")
        try:
            key = _month_key(str(row.get("source_publication_date")))
        except (TypeError, ValueError) as exc:
            raise ValueError("invalid L0-002 source_publication_date") from exc
        identity = (country, key)
        if identity in seen:
            raise ValueError("duplicate L0-002 country/month observation")
        seen.add(identity)
        validated.append({**row, "country": country, "holdings_tonnes": value, "month_key": key})
    return sorted(validated, key=lambda row: (row["month_key"], row["country"]))


def _aggregate(records: list[dict[str, Any]]) -> dict[tuple[int, int], dict[str, Any]]:
    totals: dict[tuple[int, int], dict[str, Any]] = {}
    for row in records:
        key = row["month_key"]
        bucket = totals.setdefault(key, {"value": 0.0, "rows": [], "countries": set()})
        bucket["value"] += float(row["holdings_tonnes"])
        bucket["rows"].append(row)
        bucket["countries"].add(row["country"])
    return totals


def _result(
    horizon: str,
    current_key: tuple[int, int],
    current: dict[str, Any],
    signal: int,
    reason: str,
    prior_key: tuple[int, int] | None = None,
    prior: dict[str, Any] | None = None,
    change_percentage: float | None = None,
) -> dict[str, Any]:
    flags = sorted({
        str(row.get("validation_status"))
        for row in current["rows"]
        if row.get("validation_status") not in {None, "", "PASS"}
    })
    if any(row.get("availability_status") == "FLAG" for row in current["rows"]):
        flags.append("FLAG")
    status = "FLAGGED" if "FLAG" in flags else "AVAILABLE"
    current_refs = list(dict.fromkeys(
        str(row.get("source_file"))
        for row in current["rows"]
        if row.get("source_file")
    ))
    current_trace = {
        "timestamp": _month_timestamp(current_key),
        "value": current["value"],
        "country_count": len(current["countries"]),
        "source_references": current_refs,
    }
    prior_trace = None
    if prior is not None and prior_key is not None:
        prior_refs = list(dict.fromkeys(
            str(row.get("source_file"))
            for row in prior["rows"]
            if row.get("source_file")
        ))
        prior_trace = {
            "timestamp": _month_timestamp(prior_key),
            "value": prior["value"],
            "country_count": len(prior["countries"]),
            "lookback_months": _month_index(current_key) - _month_index(prior_key),
            "source_references": prior_refs,
        }
    prior_refs = prior_trace["source_references"] if prior_trace else []
    return {
        "variable_id": VARIABLE_ID,
        "horizon": horizon,
        "status": status,
        "signal": signal,
        "reason": reason,
        "current": current_trace,
        "prior": prior_trace,
        "change_percentage": change_percentage,
        "source_references": list(dict.fromkeys(current_refs + prior_refs)),
        "flags": flags,
        "trace_context": {
            "method": "aggregate monthly holdings change",
            "unit_or_scale": UNIT,
            "meaning": "aggregate official central-bank gold holdings",
            "country_count": len(current["countries"]),
            "monthly_granularity": True,
        },
    }


def _validate_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Validate already-loaded rows using the same rules as the CSV reader."""
    validated: list[dict[str, Any]] = []
    seen: set[tuple[str, tuple[int, int]]] = set()
    for row in records:
        if not isinstance(row, dict):
            raise ValueError("L0-002 historical record must be an object")
        country = str(row.get("country", "")).strip()
        if row.get("variable_id") != VARIABLE_ID or not country:
            raise ValueError("invalid L0-002 historical record")
        if row.get("unit") != UNIT or row.get("availability_status") not in ALLOWED_STATUSES:
            raise ValueError("invalid L0-002 historical record metadata")
        try:
            value = float(row.get("holdings_tonnes"))
            key = row.get("month_key") or _month_key(str(row.get("source_publication_date")))
        except (TypeError, ValueError) as exc:
            raise ValueError("invalid L0-002 historical value or date") from exc
        if not math.isfinite(value) or value < 0:
            raise ValueError("L0-002 holdings_tonnes must be finite and non-negative")
        if (country, key) in seen:
            raise ValueError("duplicate L0-002 country/month observation")
        seen.add((country, key))
        validated.append({**row, "country": country, "holdings_tonnes": value, "month_key": key})
    return validated


def signed_change_l0_002(
    records: list[dict[str, Any]] | str | Path,
    horizon: str,
) -> dict[str, Any]:
    """Return the aggregate holdings change signal for one approved horizon."""
    if horizon not in HORIZONS:
        raise ValueError(f"unknown {VARIABLE_ID} horizon: {horizon}")
    if isinstance(records, (str, Path)):
        records = read_l0_002(records)
    if not records:
        return {
            "variable_id": VARIABLE_ID,
            "horizon": horizon,
            "status": "INCOMPLETE",
            "signal": None,
            "reason": "missing L0-002 historical holdings",
        }
    validated = _validate_records(records)
    totals = _aggregate(validated)
    current_key = max(totals)
    current = totals[current_key]
    if any(row.get("availability_status") == "BLOCKED" for row in current["rows"]):
        result = _result(horizon, current_key, current, 0, "latest aggregate includes BLOCKED input")
        result["status"] = "INCOMPLETE"
        result["signal"] = None
        return result

    if horizon in {"1-5 days", "1-3 months"}:
        return _result(horizon, current_key, current, 0, "monthly data has no meaningful daily or intra-month change")

    requested = LOOKBACK_MONTHS[horizon]
    target_index = _month_index(current_key) - requested
    prior_key = next((key for key in totals if _month_index(key) == target_index), None)
    if prior_key is None:
        eligible = [
            key for key in totals
            if _month_index(current_key) - _month_index(key) >= 12
        ]
        prior_key = min(eligible, key=_month_index) if eligible else None
    if prior_key is None:
        return _result(horizon, current_key, current, 0, "insufficient history for a 12-month minimum lookback")
    prior = totals[prior_key]
    if any(row.get("availability_status") == "BLOCKED" for row in prior["rows"]):
        result = _result(horizon, current_key, current, 0, "prior aggregate includes BLOCKED input", prior_key, prior)
        result["status"] = "INCOMPLETE"
        result["signal"] = None
        return result
    if prior["value"] == 0:
        return _result(horizon, current_key, current, 0, "prior aggregate is zero; percentage change is undefined", prior_key, prior)
    change = (current["value"] - prior["value"]) / prior["value"] * 100.0
    signal = 1 if change > 0 else -1 if change < 0 else 0
    actual = _month_index(current_key) - _month_index(prior_key)
    reason = f"aggregate holdings change over {actual} months"
    if actual != requested:
        reason += f" (fallback from requested {requested}-month lookback)"
    return _result(horizon, current_key, current, signal, reason, prior_key, prior, change)


def signal_l0_002(
    source: str | Path = DEFAULT_HISTORY_PATH,
    horizon: str = "1-3 years",
) -> dict[str, Any]:
    return signed_change_l0_002(read_l0_002(source), horizon)


status_only_l0_002 = signed_change_l0_002
status_only_method = signed_change_l0_002

