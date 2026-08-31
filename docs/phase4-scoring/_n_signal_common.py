"""Shared reader and status-only method for approved N-class scalars."""
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


def _validate_timestamp(value: Any) -> None:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError("invalid observation_timestamp") from exc


def validate_record(record: Any, variable_id: str, unit: str) -> None:
    if not isinstance(record, dict):
        raise ValueError("input must be one canonical scalar object")
    missing = REQUIRED_FIELDS - record.keys()
    if missing:
        raise ValueError(f"missing canonical fields: {sorted(missing)}")
    if record["variable_id"] != variable_id:
        raise ValueError(f"input variable_id must be {variable_id}")
    if record["unit_or_scale"] != unit:
        raise ValueError(f"{variable_id} unit_or_scale must be {unit}")
    if record["availability_status"] not in ALLOWED_STATUSES:
        raise ValueError("invalid availability_status")
    _validate_timestamp(record["observation_timestamp"])
    try:
        value = float(record["value"])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{variable_id} value must be numeric") from exc
    if not math.isfinite(value):
        raise ValueError(f"{variable_id} value must be finite")
    if not str(record["source_reference"]).strip():
        raise ValueError("source_reference is required")


def read_scalar(path: str | Path, variable_id: str, unit: str) -> dict[str, Any]:
    """Read exactly one canonical scalar from a JSON object or one-item array."""
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{variable_id} handoff is not readable JSON") from exc
    if isinstance(payload, list):
        if len(payload) != 1:
            raise ValueError(f"{variable_id} handoff must contain exactly one record")
        record = payload[0]
    elif isinstance(payload, dict):
        record = payload
    else:
        raise ValueError(f"{variable_id} handoff must be one object or a one-item array")
    validate_record(record, variable_id, unit)
    return dict(record)


def _trace(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        return {}
    return {key: record[key] for key in REQUIRED_FIELDS if key in record}


def _flags(record: Any) -> list[Any]:
    if not isinstance(record, dict):
        return []
    quality = record.get("quality_flag")
    return [] if quality in (None, "", "OK", "PASS") else [quality]


def status_only_method(record: Any, horizon: str, variable_id: str, unit: str) -> dict[str, Any]:
    """Return explicit NOT_APPLICABLE or INCOMPLETE status for one horizon."""
    if horizon not in HORIZONS:
        raise ValueError(f"unknown {variable_id} horizon: {horizon}")
    try:
        validate_record(record, variable_id, unit)
        error = None
    except ValueError as exc:
        error = str(exc)

    refs = [record["source_reference"]] if isinstance(record, dict) and record.get("source_reference") else []
    flags = _flags(record)
    base = {
        "variable": variable_id,
        "variable_id": variable_id,
        "horizon": horizon,
        "signal": None,
        "current": _trace(record),
        "prior": None,
        "source_references": refs,
        "flags": flags,
        "trace_context": {
            "unit_or_scale": unit,
            "history_class": "N",
            "method": "status-only",
            "history_used": False,
        },
    }
    if error:
        return {
            **base,
            "status": "INCOMPLETE",
            "method_state": "INCOMPLETE",
            "reason": error,
        }
    if record["availability_status"] in {"STALE", "BLOCKED"}:
        return {
            **base,
            "status": "INCOMPLETE",
            "method_state": "INCOMPLETE",
            "reason": f"current record is {record['availability_status']}",
        }
    return {
        **base,
        "status": "NOT_APPLICABLE",
        "method_state": "NOT_APPLICABLE",
        "reason": f"no approved {variable_id} history or neutral level anchor",
    }
