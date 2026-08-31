"""Reader and signed-change signal for approved L2-003."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _l1_signal_common import read_series, signed_change_signal


VARIABLE_ID = "L2-003"
UNIT = "cny_per_usd"
OFFSETS = {"1-5 days": 5, "1-3 months": 63, "1-3 years": 252}


def read_l2_003(path: str | Path) -> list[dict[str, Any]]:
    return read_series(path, VARIABLE_ID, UNIT)


def signed_change_l2_003(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    result = signed_change_signal(
        records, horizon, VARIABLE_ID, UNIT, OFFSETS,
        falling_signal=-1,
        rising_signal=1,
        direction_mapping="CNY per USD fell -> -1; unchanged -> 0; CNY per USD rose -> +1",
    )
    result["trace_context"] = {
        "unit_or_scale": UNIT,
        "quotation": "CNY per USD",
        "direction_convention": "rising USD/CNY -> +1",
    }
    return result
