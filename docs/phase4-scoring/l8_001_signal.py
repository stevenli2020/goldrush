"""Reader and signed-change signal for corrected L8-001."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _l1_signal_common import read_series, signed_change_signal


VARIABLE_ID = "L8-001"
UNIT = "metric_tonnes"
OFFSETS = {"1-3 months": 1, "1-3 years": 12}


def read_l8_001(path: str | Path) -> list[dict[str, Any]]:
    return read_series(path, VARIABLE_ID, UNIT)


def signed_change_l8_001(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    result = signed_change_signal(
        records,
        horizon,
        VARIABLE_ID,
        UNIT,
        OFFSETS,
        falling_signal=-1,
        rising_signal=1,
        direction_mapping="ETF net flow fell -> -1; unchanged -> 0; ETF net flow rose -> +1",
    )
    result["trace_context"] = {
        "unit_or_scale": UNIT,
        "meaning": "monthly ETF net flow from per-fund Demand (tonnes)",
        "source_measure": "Demand by month / Demand (tonnes)",
        "direction_condition": "registry direction is Positive for net inflows",
    }
    return result
