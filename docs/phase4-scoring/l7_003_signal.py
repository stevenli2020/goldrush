"""Reader and signed-change signal for approved L7-003."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _l1_signal_common import read_series, signed_change_signal


VARIABLE_ID = "L7-003"
UNIT = "percent_yoy"
OFFSETS = {"1-3 years": 12, "3-10 years": 40}


def read_l7_003(path: str | Path) -> list[dict[str, Any]]:
    return read_series(path, VARIABLE_ID, UNIT)


def signed_change_l7_003(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    result = signed_change_signal(
        records,
        horizon,
        VARIABLE_ID,
        UNIT,
        OFFSETS,
        falling_signal=1,
        rising_signal=-1,
        direction_mapping="YoY credit growth fell -> +1; unchanged -> 0; YoY credit growth rose -> -1",
    )
    result["trace_context"] = {
        "unit_or_scale": UNIT,
        "meaning": "already-derived quarterly year-over-year private non-financial credit growth",
        "observed_cadence": "quarterly",
        "pre_derived_measure": "YoY; no recomputation",
        "direction_condition": "registry direction is Conditional",
    }
    return result
