"""Reader and signed-change signal for the approved L1-001 pilot."""
from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


OFFSETS: dict[str, int] = {
    "1-5 days": 5,
    "1-3 months": 63,
    "1-3 years": 252,
    "3-10 years": 756,
}
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


def _timestamp(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError("invalid observation_timestamp") from exc


def _validate_record(record: dict[str, Any]) -> None:
    missing = REQUIRED_FIELDS - record.keys()
    if missing:
        raise ValueError(f"missing canonical fields: {sorted(missing)}")
    if record["variable_id"] != "L1-001":
        raise ValueError("input contains a non-L1-001 record")
    if record["unit_or_scale"] != "percent":
        raise ValueError("L1-001 unit_or_scale must be percent")
    if record["availability_status"] not in ALLOWED_STATUSES:
        raise ValueError("invalid availability_status")
    _timestamp(record["observation_timestamp"])
    try:
        value = float(record["value"])
    except (TypeError, ValueError) as exc:
        raise ValueError("L1-001 value must be numeric") from exc
    if not math.isfinite(value):
        raise ValueError("L1-001 value must be finite")
    if not str(record["source_reference"]).strip():
        raise ValueError("source_reference is required")


def read_l1_001(path: str | Path) -> list[dict[str, Any]]:
    """Read and validate one JSON array of canonical L1-001 records."""
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("L1-001 handoff is not readable JSON") from exc
    if not isinstance(payload, list) or not payload:
        raise ValueError("L1-001 handoff must be a non-empty JSON array")
    records: list[dict[str, Any]] = []
    for record in payload:
        if not isinstance(record, dict):
            raise ValueError("each L1-001 record must be an object")
        _validate_record(record)
        records.append(dict(record))
    records.sort(key=lambda row: _timestamp(row["observation_timestamp"]))
    timestamps = [row["observation_timestamp"] for row in records]
    if len(set(timestamps)) != len(timestamps):
        raise ValueError("duplicate L1-001 observation_timestamp")
    return records


def _incomplete(horizon: str, current: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "variable_id": "L1-001",
        "horizon": horizon,
        "status": "INCOMPLETE",
        "signal": None,
        "reason": reason,
        "current": current,
        "prior": None,
        "delta_percentage_points": None,
        "source_references": [current["source_reference"]],
        "flags": [current["quality_flag"]] if current["quality_flag"] else [],
    }


def signed_change_signal(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    """Return the approved -1/0/+1 gold-direction signal for one horizon."""
    if horizon not in OFFSETS:
        raise ValueError(f"unknown L1-001 horizon: {horizon}")
    if not records:
        raise ValueError("records must be non-empty")
    validated = [dict(record) for record in records]
    for record in validated:
        _validate_record(record)
    ordered = sorted(validated, key=lambda row: _timestamp(row["observation_timestamp"]))
    current = ordered[-1]
    if current["availability_status"] in {"STALE", "BLOCKED"}:
        return _incomplete(horizon, current, "current record is not eligible")
    offset = OFFSETS[horizon]
    if len(ordered) <= offset:
        return _incomplete(horizon, current, "insufficient permitted history")
    prior = ordered[-1 - offset]
    if prior["availability_status"] == "BLOCKED":
        return _incomplete(horizon, current, "prior record is BLOCKED")
    if prior["availability_status"] == "STALE":
        return _incomplete(horizon, current, "prior record is STALE")
    delta = float(current["value"]) - float(prior["value"])
    signal = 1 if delta < 0 else -1 if delta > 0 else 0
    flags = [record["quality_flag"] for record in (current, prior) if record["quality_flag"]]
    return {
        "variable_id": "L1-001",
        "horizon": horizon,
        "status": "FLAGGED" if current["availability_status"] == "FLAG" else "AVAILABLE",
        "signal": signal,
        "direction_mapping": "yield fell -> +1; unchanged -> 0; yield rose -> -1",
        "current": {
            "timestamp": current["observation_timestamp"],
            "value": float(current["value"]),
            "source_reference": current["source_reference"],
        },
        "prior": {
            "offset_positions": offset,
            "timestamp": prior["observation_timestamp"],
            "value": float(prior["value"]),
            "source_reference": prior["source_reference"],
        },
        "delta_percentage_points": delta,
        "source_references": [current["source_reference"], prior["source_reference"]],
        "flags": flags,
    }
