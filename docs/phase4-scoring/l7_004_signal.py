"""Reader and signed-change signal for approved L7-004."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _l1_signal_common import read_series, signed_change_signal


VARIABLE_ID = "L7-004"
UNIT = "percentage_points"
OFFSETS = {"1-5 days": 5, "1-3 months": 63, "1-3 years": 252}


def read_l7_004(path: str | Path) -> list[dict[str, Any]]:
    return read_series(path, VARIABLE_ID, UNIT)


def signed_change_l7_004(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    result = signed_change_signal(
        records,
        horizon,
        VARIABLE_ID,
        UNIT,
        OFFSETS,
        falling_signal=-1,
        rising_signal=1,
        direction_mapping="credit spread narrowed -> -1; unchanged -> 0; credit spread widened -> +1",
    )
    result["trace_context"] = {
        "unit_or_scale": UNIT,
        "meaning": "daily credit-spread financial stress",
        "observed_cadence": "daily",
        "direction_condition": "registry direction is Conditional; widening-stress baseline",
    }
    return result
