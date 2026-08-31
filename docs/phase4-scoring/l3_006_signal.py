"""Approved Phase 4 adapter for the existing L3-006 hawkishness scorer."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _n_signal_common import HORIZONS, REQUIRED_FIELDS, read_scalar, validate_record


VARIABLE_ID = "L3-006"
UNIT = "hawkishness_score_0_to_100"
NUMERIC_HORIZONS = {"1-5 days", "1-3 months"}
MAPPING = "score < 50 -> +1; score = 50 -> 0; score > 50 -> -1"


def read_l3_006(path: str | Path) -> dict[str, Any]:
    return read_scalar(path, VARIABLE_ID, UNIT)


def _trace(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        return {}
    return {key: record[key] for key in REQUIRED_FIELDS if key in record}


def _flags(record: Any) -> list[Any]:
    if not isinstance(record, dict):
        return []
    flags: list[Any] = []
    quality = record.get("quality_flag")
    if quality not in (None, "", "OK", "PASS"):
        flags.append(quality)
    if record.get("availability_status") == "FLAG":
        flags.append("FLAG")
    return flags


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
            "history_class": "Q",
            "method": "existing-scorer-adapter",
            "history_used": False,
            "source_score": record.get("value") if isinstance(record, dict) else None,
            "mapping_direction": MAPPING,
        },
    }


def signal_l3_006(record: Any, horizon: str) -> dict[str, Any]:
    if horizon not in HORIZONS:
        raise ValueError(f"unknown {VARIABLE_ID} horizon: {horizon}")
    base = _base(record, horizon)
    try:
        validate_record(record, VARIABLE_ID, UNIT)
        score = float(record["value"])
        if not 0.0 <= score <= 100.0:
            raise ValueError("L3-006 value must be between 0 and 100")
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
    signal = 1 if score < 50.0 else 0 if score == 50.0 else -1
    return {
        **base,
        "status": "FLAGGED" if record["availability_status"] == "FLAG" else "AVAILABLE",
        "method_state": "NUMERIC",
        "signal": signal,
        "reason": record["quality_flag"] if record["availability_status"] == "FLAG" else None,
    }


signal_method = signal_l3_006
