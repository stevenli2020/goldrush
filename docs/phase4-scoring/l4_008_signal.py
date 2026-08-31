"""Reader and signed-change signal for approved L4-008."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _l1_signal_common import read_series, signed_change_signal


VARIABLE_ID = "L4-008"
UNIT = "percent_of_federal_receipts"
OFFSETS = {"1-3 years": 3, "3-10 years": 10}


def read_l4_008(path: str | Path) -> list[dict[str, Any]]:
    return read_series(path, VARIABLE_ID, UNIT)


def signed_change_l4_008(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    result = signed_change_signal(
        records, horizon, VARIABLE_ID, UNIT, OFFSETS,
        falling_signal=-1,
        rising_signal=1,
        direction_mapping="interest expense/revenue fell -> -1; unchanged -> 0; rose -> +1",
    )
    result["trace_context"] = {
        "unit_or_scale": UNIT,
        "meaning": "gross interest expense as percent of federal receipts",
        "direction_condition": "registry direction is Conditional",
        "history_note": "11 annual rows; offset 10 is minimally sufficient",
    }
    return result
