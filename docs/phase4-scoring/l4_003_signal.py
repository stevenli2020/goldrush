"""Reader and signed-change signal for approved L4-003."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _l1_signal_common import read_series, signed_change_signal


VARIABLE_ID = "L4-003"
UNIT = "percent"
OFFSETS = {"1-3 months": 63, "1-3 years": 252}


def read_l4_003(path: str | Path) -> list[dict[str, Any]]:
    return read_series(path, VARIABLE_ID, UNIT)


def signed_change_l4_003(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    result = signed_change_signal(
        records, horizon, VARIABLE_ID, UNIT, OFFSETS,
        falling_signal=-1,
        rising_signal=1,
        direction_mapping="5Y breakeven percentage fell -> -1; unchanged -> 0; rose -> +1",
    )
    result["trace_context"] = {
        "unit_or_scale": UNIT,
        "meaning": "5Y market-implied inflation expectation",
        "direction_condition": "registry direction is Conditional",
        "registry_horizons": ["1-3 months", "1-3 years"],
    }
    return result
