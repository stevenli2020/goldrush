"""Reader and signed-change signal for approved L5-003."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _l1_signal_common import read_series, signed_change_signal


VARIABLE_ID = "L5-003"
UNIT = "percentage_points_qoq"
OFFSETS = {"1-3 years": 12, "3-10 years": 40}


def read_l5_003(path: str | Path) -> list[dict[str, Any]]:
    return read_series(path, VARIABLE_ID, UNIT)


def signed_change_l5_003(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    result = signed_change_signal(
        records,
        horizon,
        VARIABLE_ID,
        UNIT,
        OFFSETS,
        falling_signal=1,
        rising_signal=-1,
        direction_mapping="QoQ USD-share change fell -> +1; unchanged -> 0; QoQ USD-share change rose -> -1",
    )
    result["trace_context"] = {
        "unit_or_scale": UNIT,
        "meaning": "already-derived quarterly change in USD reserve share",
        "observed_cadence": "quarterly",
        "pre_derived_measure": "QoQ; no recomputation",
        "direction_condition": "registry direction is Conditional",
    }
    return result
