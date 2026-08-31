"""Reader and signed-change signal for approved L0-001."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _l1_signal_common import read_series, signed_change_signal


VARIABLE_ID = "L0-001"
UNIT = "metric_tonnes"
OFFSETS = {"1-3 years": 3, "3-10 years": 10}


def read_l0_001(path: str | Path) -> list[dict[str, Any]]:
    return read_series(path, VARIABLE_ID, UNIT)


def signed_change_l0_001(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    result = signed_change_signal(
        records,
        horizon,
        VARIABLE_ID,
        UNIT,
        OFFSETS,
        direction_mapping="above-ground stock fell -> +1; unchanged -> 0; above-ground stock rose -> -1",
    )
    result["trace_context"] = {
        "unit_or_scale": UNIT,
        "meaning": "above-ground gold stock",
        "direction_condition": "registry direction is Conditional; available-stock baseline",
    }
    return result
