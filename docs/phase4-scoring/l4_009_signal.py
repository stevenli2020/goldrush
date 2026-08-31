"""Reader and signed-change signal for approved L4-009."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _l1_signal_common import read_series, signed_change_signal


VARIABLE_ID = "L4-009"
UNIT = "percent_of_marketable_treasury_debt"
OFFSETS = {"1-3 months": 1, "1-3 years": 12, "3-10 years": 120}


def read_l4_009(path: str | Path) -> list[dict[str, Any]]:
    return read_series(path, VARIABLE_ID, UNIT)


def signed_change_l4_009(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    result = signed_change_signal(
        records, horizon, VARIABLE_ID, UNIT, OFFSETS,
        falling_signal=-1,
        rising_signal=1,
        direction_mapping="maturing-within-one-year share fell -> -1; unchanged -> 0; rose -> +1",
    )
    result["trace_context"] = {
        "unit_or_scale": UNIT,
        "meaning": "marketable Treasury debt maturing within one calendar year",
        "direction_condition": "registry direction is Conditional",
        "history_note": "24 monthly rows; offset 120 is insufficient in the preserved snapshot",
    }
    return result
