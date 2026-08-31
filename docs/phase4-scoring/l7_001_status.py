"""Reader and status-only method for approved L7-001 MVP treatment."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _l1_signal_common import REQUIRED_FIELDS, read_series, validate_record


VARIABLE_ID = "L7-001"
UNIT = "millions_usd"
HORIZONS = ("1-5 days", "1-3 months", "1-3 years", "3-10 years")


def read_l7_001(path: str | Path) -> list[dict[str, Any]]:
    return read_series(path, VARIABLE_ID, UNIT)


def _trace(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        return {}
    return {key: record[key] for key in REQUIRED_FIELDS if key in record}


def status_only_l7_001(record: Any, horizon: str) -> dict[str, Any]:
    if horizon not in HORIZONS:
        raise ValueError(f"unknown L7-001 horizon: {horizon}")
    if not isinstance(record, dict):
        reason = "input must be one canonical scalar object"
    else:
        try:
            validate_record(record, VARIABLE_ID, UNIT)
            reason = None
        except ValueError as exc:
            reason = str(exc)
    refs = [record["source_reference"]] if isinstance(record, dict) and record.get("source_reference") else []
    flags = [record["quality_flag"]] if isinstance(record, dict) and record.get("quality_flag") else []
    if reason:
        return {
            "variable_id": VARIABLE_ID,
            "horizon": horizon,
            "status": "INCOMPLETE",
            "method_state": "INCOMPLETE",
            "signal": None,
            "reason": reason,
            "current": _trace(record),
            "prior": None,
            "source_references": refs,
            "flags": flags,
            "trace_context": {"unit_or_scale": UNIT, "observed_cadence": "weekly", "method": "status-only"},
        }
    if record["availability_status"] in {"STALE", "BLOCKED"}:
        return {
            "variable_id": VARIABLE_ID,
            "horizon": horizon,
            "status": "INCOMPLETE",
            "method_state": "INCOMPLETE",
            "signal": None,
            "reason": f"current record is {record['availability_status']}",
            "current": _trace(record),
            "prior": None,
            "source_references": refs,
            "flags": flags,
            "trace_context": {"unit_or_scale": UNIT, "observed_cadence": "weekly", "method": "status-only"},
        }
    return {
        "variable_id": VARIABLE_ID,
        "horizon": horizon,
        "status": "NOT_APPLICABLE",
        "method_state": "NOT_APPLICABLE",
        "signal": None,
        "reason": "no approved weekly offset rule; L7-001 is status-only",
        "current": _trace(record),
        "prior": None,
        "source_references": refs,
        "flags": flags,
        "trace_context": {"unit_or_scale": UNIT, "observed_cadence": "weekly", "method": "status-only"},
    }


status_only_method = status_only_l7_001
