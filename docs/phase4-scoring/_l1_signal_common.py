"""Shared validation and signed-change logic for approved Layer 1 pilots."""
from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


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


def validate_record(record: dict[str, Any], variable_id: str, unit: str) -> None:
    missing = REQUIRED_FIELDS - record.keys()
    if missing:
        raise ValueError(f"missing canonical fields: {sorted(missing)}")
    if record["variable_id"] != variable_id:
        raise ValueError(f"input contains a non-{variable_id} record")
    if record["unit_or_scale"] != unit:
        raise ValueError(f"{variable_id} unit_or_scale must be {unit}")
    if record["availability_status"] not in ALLOWED_STATUSES:
        raise ValueError("invalid availability_status")
    _timestamp(record["observation_timestamp"])
    try:
        value = float(record["value"])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{variable_id} value must be numeric") from exc
    if not math.isfinite(value):
        raise ValueError(f"{variable_id} value must be finite")
    if not str(record["source_reference"]).strip():
        raise ValueError("source_reference is required")


def read_series(path: str | Path, variable_id: str, unit: str) -> list[dict[str, Any]]:
    """Read and validate one canonical JSON array for a configured variable."""
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{variable_id} handoff is not readable JSON") from exc
    if not isinstance(payload, list) or not payload:
        raise ValueError(f"{variable_id} handoff must be a non-empty JSON array")
    records: list[dict[str, Any]] = []
    for record in payload:
        if not isinstance(record, dict):
            raise ValueError(f"each {variable_id} record must be an object")
        validate_record(record, variable_id, unit)
        records.append(dict(record))
    records.sort(key=lambda row: _timestamp(row["observation_timestamp"]))
    timestamps = [row["observation_timestamp"] for row in records]
    if len(set(timestamps)) != len(timestamps):
        raise ValueError(f"duplicate {variable_id} observation_timestamp")
    return records


def _incomplete(
    variable_id: str,
    horizon: str,
    current: dict[str, Any] | None,
    reason: str,
    prior: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "variable_id": variable_id,
        "horizon": horizon,
        "status": "INCOMPLETE",
        "signal": None,
        "reason": reason,
        "current": current,
        "prior": {
            "timestamp": prior["observation_timestamp"],
            "value": float(prior["value"]),
            "source_reference": prior["source_reference"],
        } if prior else None,
        "delta_percentage_points": None,
        "source_references": [
            reference
            for reference in (
                current.get("source_reference") if current else None,
                prior.get("source_reference") if prior else None,
            )
            if reference
        ],
        "flags": [current["quality_flag"]] if current and current.get("quality_flag") else [],
    }


def not_applicable(variable_id: str, horizon: str) -> dict[str, Any]:
    return {
        "variable_id": variable_id,
        "horizon": horizon,
        "status": "NOT_APPLICABLE",
        "signal": None,
        "reason": "horizon is not approved for this variable",
        "current": None,
        "prior": None,
        "delta_percentage_points": None,
        "source_references": [],
        "flags": [],
    }


def signed_change_signal(
    records: list[dict[str, Any]],
    horizon: str,
    variable_id: str,
    unit: str,
    offsets: dict[str, int],
    falling_signal: int = 1,
    rising_signal: int = -1,
    direction_mapping: str = "value fell -> +1; unchanged -> 0; value rose -> -1",
) -> dict[str, Any]:
    """Return the configured -1/0/+1 gold-direction signal for one horizon."""
    if horizon not in offsets:
        return not_applicable(variable_id, horizon)
    if not records:
        return _incomplete(variable_id, horizon, None, "missing input records")
    validated = [dict(record) for record in records]
    try:
        for record in validated:
            validate_record(record, variable_id, unit)
    except ValueError as exc:
        return _incomplete(variable_id, horizon, validated[-1] if validated else None, str(exc))
    ordered = sorted(validated, key=lambda row: _timestamp(row["observation_timestamp"]))
    if len({row["observation_timestamp"] for row in ordered}) != len(ordered):
        return _incomplete(variable_id, horizon, ordered[-1], "duplicate observation_timestamp")
    current = ordered[-1]
    if current["availability_status"] in {"STALE", "BLOCKED"}:
        return _incomplete(variable_id, horizon, current, "current record is not eligible")
    offset = offsets[horizon]
    if len(ordered) <= offset:
        return _incomplete(variable_id, horizon, current, "insufficient permitted history")
    prior = ordered[-1 - offset]
    if prior["availability_status"] == "STALE":
        return _incomplete(variable_id, horizon, current, "prior record is STALE", prior)
    if prior["availability_status"] == "BLOCKED":
        return _incomplete(variable_id, horizon, current, "prior record is BLOCKED", prior)
    delta = float(current["value"]) - float(prior["value"])
    signal = falling_signal if delta < 0 else rising_signal if delta > 0 else 0
    flags = [record["quality_flag"] for record in (current, prior) if record.get("quality_flag")]
    return {
        "variable_id": variable_id,
        "horizon": horizon,
        "status": "FLAGGED" if current["availability_status"] == "FLAG" else "AVAILABLE",
        "signal": signal,
        "direction_mapping": direction_mapping,
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
