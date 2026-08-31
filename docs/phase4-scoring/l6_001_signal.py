"""Approved Phase 4 adapter for the existing L6-001 continuous scorer."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _n_signal_common import HORIZONS, REQUIRED_FIELDS, read_scalar, validate_record


VARIABLE_ID = "L6-001"
UNIT = "standard_deviation_units_clamped_-1_to_1"
NUMERIC_HORIZONS = {"1-5 days", "1-3 months"}
MAPPING = "score > 0 -> +1; score = 0 -> 0; score < 0 -> -1"


def read_l6_001(path: str | Path) -> dict[str, Any]:
    return read_scalar(path, VARIABLE_ID, UNIT)


def _trace(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        return {}
    return {key: record[key] for key in REQUIRED_FIELDS if key in record}


def _flags(record: Any) -> list[Any]:
    if not isinstance(record, dict):
        return []
    quality = record.get("quality_flag")
    return [] if quality in (None, "", "OK", "PASS") else [quality]


def _base(record: Any, horizon: str) -> dict[str, Any]:
    return {
        "variable": VARIABLE_ID,
        "variable_id": VARIABLE_ID,
        "horizon": horizon,
        "signal": None,
        "current": _trace(record),
        "prior": None,
        "source_references": [record["source_reference"]] if isinstance(record, dict) and record.get("source_reference") else [],
        "flags": _flags(record),
        "trace_context": {
            "history_class": "H",
            "method": "existing-scorer-adapter",
            "history_used": False,
            "source_score": record.get("value") if isinstance(record, dict) else None,
            "mapping_direction": MAPPING,
        },
    }


def signal_l6_001(record: Any, horizon: str) -> dict[str, Any]:
    if horizon not in HORIZONS:
        raise ValueError(f"unknown {VARIABLE_ID} horizon: {horizon}")
    base = _base(record, horizon)
    try:
        validate_record(record, VARIABLE_ID, UNIT)
        score = float(record["value"])
        if not -1.0 <= score <= 1.0:
            raise ValueError("L6-001 value must be between -1 and 1")
    except ValueError as exc:
        return {**base, "status": "INCOMPLETE", "method_state": "INCOMPLETE", "reason": str(exc)}
    if record["availability_status"] in {"STALE", "BLOCKED"}:
        return {
            **base,
            "status": "INCOMPLETE",
            "method_state": "INCOMPLETE",
            "reason": f"current record is {record['availability_status']}",
        }
    if horizon not in NUMERIC_HORIZONS:
        return {
            **base,
            "status": "NOT_APPLICABLE",
            "method_state": "NOT_APPLICABLE",
            "reason": "horizon is not approved for this variable",
        }
    signal = 1 if score > 0.0 else 0 if score == 0.0 else -1
    return {
        **base,
        "status": "FLAGGED" if record["availability_status"] == "FLAG" else "AVAILABLE",
        "method_state": "NUMERIC",
        "signal": signal,
        "reason": record["quality_flag"] if record["availability_status"] == "FLAG" else None,
    }


signal_method = signal_l6_001
