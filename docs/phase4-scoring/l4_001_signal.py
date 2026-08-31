"""Reader and signed-change signal for approved L4-001."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _l1_signal_common import read_series, signed_change_signal


VARIABLE_ID = "L4-001"
UNIT = "index"
OFFSETS = {"1-3 months": 1, "1-3 years": 12}


def read_l4_001(path: str | Path) -> list[dict[str, Any]]:
    return read_series(path, VARIABLE_ID, UNIT)


def signed_change_l4_001(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    result = signed_change_signal(
        records, horizon, VARIABLE_ID, UNIT, OFFSETS,
        falling_signal=-1,
        rising_signal=1,
        direction_mapping="CPI index fell -> -1; unchanged -> 0; CPI index rose -> +1",
    )
    result["trace_context"] = {
        "unit_or_scale": UNIT,
        "meaning": "CPI index; realized purchasing-power pressure proxy",
        "direction_condition": "registry direction is Conditional",
    }
    return result
