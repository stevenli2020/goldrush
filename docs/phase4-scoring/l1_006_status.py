"""Reader and status-only method for the approved L1-006 MVP treatment."""
from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


HORIZONS = ("1-5 days", "1-3 months", "1-3 years", "3-10 years")
REQUIRED_FIELDS = {
    "variable_id",
    "observation_timestamp",
    "value",
    "unit_or_scale",
    "availability_status",
    "source_reference",
    "quality_flag",
}
ALLOWED_STATUSES = {"AVAILABLE", "FLAG", "STALE", "BLOCKED"}


def _timestamp(value: Any) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError("invalid observation_timestamp") from exc


def _validation_error(record: Any) -> str | None:
    if not isinstance(record, dict):
        return "input must be one canonical scalar object"
    missing = REQUIRED_FIELDS - record.keys()
    if missing:
        return f"missing canonical fields: {sorted(missing)}"
    if record["variable_id"] != "L1-006":
        return "input variable_id must be L1-006"
    if record["unit_or_scale"] != "percent_per_annum":
        return "L1-006 unit_or_scale must be percent_per_annum"
    if record["availability_status"] not in ALLOWED_STATUSES:
        return "invalid availability_status"
    try:
        _timestamp(record["observation_timestamp"])
    except ValueError as exc:
        return str(exc)
    try:
        value = float(record["value"])
    except (TypeError, ValueError):
        return "L1-006 value must be numeric"
    if not math.isfinite(value):
        return "L1-006 value must be finite"
    if not str(record["source_reference"]).strip():
        return "source_reference is required"
    return None


def read_l1_006(path: str | Path) -> dict[str, Any]:
    """Read exactly one canonical L1-006 scalar from JSON."""
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("L1-006 handoff is not readable JSON") from exc
    if isinstance(payload, list):
        if len(payload) != 1:
            raise ValueError("L1-006 handoff must contain exactly one record")
        record = payload[0]
    elif isinstance(payload, dict):
        record = payload
    else:
        raise ValueError("L1-006 handoff must be one object or a one-item array")
    error = _validation_error(record)
    if error:
        raise ValueError(error)
    return dict(record)


def _flags(record: Any) -> list[Any]:
    if isinstance(record, dict) and record.get("quality_flag") not in (None, "", "OK"):
        return [record["quality_flag"]]
    return []


def _trace_context(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        return {}
    return {
        key: record[key]
        for key in (
            "observation_timestamp",
            "value",
            "unit_or_scale",
            "source_reference",
            "availability_status",
        )
        if key in record
    }


def status_only_method(record: Any, horizon: str) -> dict[str, Any]:
    """Return explicit NOT_APPLICABLE or INCOMPLETE status for one horizon."""
    if horizon not in HORIZONS:
        raise ValueError(f"unknown L1-006 horizon: {horizon}")
    error = _validation_error(record)
    if error:
        return {
            "variable_id": record.get("variable_id", "L1-006") if isinstance(record, dict) else "L1-006",
            "horizon": horizon,
            "status": "INCOMPLETE",
            "method_state": "INCOMPLETE",
            "signal": None,
            "reason": error,
            "current": _trace_context(record),
            "source_references": [record["source_reference"]] if isinstance(record, dict) and record.get("source_reference") else [],
            "flags": _flags(record),
        }
    availability = record["availability_status"]
    if availability in {"STALE", "BLOCKED"}:
        return {
            "variable_id": "L1-006",
            "horizon": horizon,
            "status": "INCOMPLETE",
            "method_state": "INCOMPLETE",
            "signal": None,
            "reason": f"current record is {availability}",
            "current": _trace_context(record),
            "source_references": [record["source_reference"]],
            "flags": _flags(record),
        }
    return {
        "variable_id": "L1-006",
        "horizon": horizon,
        "status": "NOT_APPLICABLE",
        "method_state": "NOT_APPLICABLE",
        "signal": None,
        "reason": "no approved L1-006 history or neutral level anchor",
        "current": _trace_context(record),
        "source_references": [record["source_reference"]],
        "flags": _flags(record),
    }
