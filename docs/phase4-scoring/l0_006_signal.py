"""Reader and signed-change signal for corrected L0-006 source path."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from _l1_signal_common import signed_change_signal, validate_record


VARIABLE_ID = "L0-006"
UNIT = "metric_tonnes"
OFFSETS = {"1-3 years": 12}


def _timestamp(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError("invalid observation_timestamp") from exc


def read_l0_006(path: str | Path) -> list[dict[str, Any]]:
    path = Path(path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("L0-006 source is not readable JSON") from exc
    observations = payload.get("observations") if isinstance(payload, dict) else None
    if not isinstance(observations, list) or not observations:
        raise ValueError("L0-006 source must contain non-empty observations")
    if payload.get("variable_id") != VARIABLE_ID:
        raise ValueError("input contains a non-L0-006 record")
    status = payload.get("availability_status")
    if status not in {"AVAILABLE", "FLAG", "STALE", "BLOCKED"}:
        raise ValueError("invalid availability_status")
    source_reference = path.as_posix()
    records: list[dict[str, Any]] = []
    for observation in observations:
        if not isinstance(observation, dict):
            raise ValueError("each L0-006 observation must be an object")
        if observation.get("frequency") != "quarterly" or observation.get("unit") != "tonnes":
            raise ValueError("L0-006 observations must be quarterly tonnes")
        date = observation.get("observation_date")
        timestamp = f"{date}T00:00:00Z"
        record = {
            "variable_id": VARIABLE_ID,
            "observation_timestamp": timestamp,
            "value": observation.get("value"),
            "unit_or_scale": UNIT,
            "availability_status": status,
            "source_reference": source_reference,
            "quality_flag": "PASS",
        }
        validate_record(record, VARIABLE_ID, UNIT)
        records.append(record)
    records.sort(key=lambda row: _timestamp(row["observation_timestamp"]))
    if len({row["observation_timestamp"] for row in records}) != len(records):
        raise ValueError("duplicate L0-006 observation_timestamp")
    return records


def signed_change_l0_006(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    result = signed_change_signal(
        records,
        horizon,
        VARIABLE_ID,
        UNIT,
        OFFSETS,
        falling_signal=1,
        rising_signal=-1,
        direction_mapping="gold recycling flow fell -> +1; unchanged -> 0; gold recycling flow rose -> -1",
    )
    result["trace_context"] = {
        "unit_or_scale": UNIT,
        "meaning": "gold recycling flow into market supply",
        "source_path": "docs/phase2-ingestion/L0/006/processed/l0_006_gold_recycling_flow.json",
        "direction_condition": "registry direction is Negative",
    }
    return result
