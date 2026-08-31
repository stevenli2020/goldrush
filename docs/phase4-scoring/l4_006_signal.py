"""Reader and signed-change signal for approved L4-006."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _l1_signal_common import read_series, signed_change_signal


VARIABLE_ID = "L4-006"
UNIT = "percent_of_gdp"
OFFSETS = {"1-3 years": 3, "3-10 years": 10}


def read_l4_006(path: str | Path) -> list[dict[str, Any]]:
    return read_series(path, VARIABLE_ID, UNIT)


def signed_change_l4_006(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    result = signed_change_signal(
        records, horizon, VARIABLE_ID, UNIT, OFFSETS,
        falling_signal=1,
        rising_signal=-1,
        direction_mapping="fiscal balance/GDP fell (more negative deficit) -> +1; unchanged -> 0; rose -> -1",
    )
    result["trace_context"] = {
        "unit_or_scale": UNIT,
        "meaning": "fiscal balance as percent of GDP",
        "source_sign_convention": "negative = deficit; positive = surplus",
        "direction_condition": "registry direction is Conditional",
    }
    return result
