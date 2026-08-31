"""Reader and signed-change signal for approved L9-001."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _l1_signal_common import read_series, signed_change_signal


VARIABLE_ID = "L9-001"
UNIT = "usd_per_troy_ounce"
OFFSETS = {"1-5 days": 5, "1-3 months": 63, "1-3 years": 252}


def read_l9_001(path: str | Path) -> list[dict[str, Any]]:
    return read_series(path, VARIABLE_ID, UNIT)


def signed_change_l9_001(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    result = signed_change_signal(
        records,
        horizon,
        VARIABLE_ID,
        UNIT,
        OFFSETS,
        falling_signal=-1,
        rising_signal=1,
        direction_mapping="SGE premium/discount fell -> -1; unchanged -> 0; SGE premium/discount rose -> +1",
    )
    result["trace_context"] = {
        "unit_or_scale": UNIT,
        "meaning": "daily Shanghai Gold Exchange premium/discount",
        "observed_cadence": "daily",
        "direction_condition": "registry direction is Conditional; rising-premium physical-tightness baseline",
        "registry_definition": "premium/discount, not spot price",
    }
    return result
