"""Reader and period-matched signed-change signal for approved L0-005."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _l1_signal_common import (
    _incomplete,
    _timestamp,
    not_applicable,
    read_series,
    signed_change_signal,
    validate_record,
)


VARIABLE_ID = "L0-005"
UNIT = "metric_tonnes"
OFFSETS = {
    "1-3 years": {"quarterly": 12, "annual": 3},
    "3-10 years": {"quarterly": 40, "annual": 10},
}


def read_l0_005(path: str | Path) -> list[dict[str, Any]]:
    rows = read_series(path, VARIABLE_ID, UNIT)
    for row in rows:
        if row.get("observation_period_type") not in {"annual", "quarterly"}:
            raise ValueError("L0-005 observation_period_type must be annual or quarterly")
    return rows


def signed_change_l0_005(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    if horizon not in OFFSETS:
        return not_applicable(VARIABLE_ID, horizon)
    if not records:
        return _incomplete(VARIABLE_ID, horizon, None, "missing input records")
    validated = [dict(record) for record in records]
    try:
        for record in validated:
            validate_record(record, VARIABLE_ID, UNIT)
            if record.get("observation_period_type") not in {"annual", "quarterly"}:
                raise ValueError("L0-005 observation_period_type must be annual or quarterly")
    except ValueError as exc:
        return _incomplete(VARIABLE_ID, horizon, validated[-1], str(exc))
    ordered = sorted(validated, key=lambda row: _timestamp(row["observation_timestamp"]))
    period_type = ordered[-1]["observation_period_type"]
    same_period = [row for row in ordered if row["observation_period_type"] == period_type]
    result = signed_change_signal(
        same_period,
        horizon,
        VARIABLE_ID,
        UNIT,
        {horizon: OFFSETS[horizon][period_type]},
        falling_signal=-1,
        rising_signal=1,
        direction_mapping="bar-and-coin demand fell -> -1; unchanged -> 0; bar-and-coin demand rose -> +1",
    )
    result["trace_context"] = {
        "unit_or_scale": UNIT,
        "meaning": "bar-and-coin physical investment demand",
        "period_type": period_type,
        "period_type_matching": "current and prior use the same annual or quarterly series",
        "direction_condition": "registry direction is Positive",
    }
    return result
