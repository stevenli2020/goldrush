"""Reader and signed-change signal for approved L0-003."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _l1_signal_common import read_series, signed_change_signal


VARIABLE_ID = "L0-003"
UNIT = "metric_tonnes"
OFFSETS = {"1-3 months": 1, "1-3 years": 12}


def read_l0_003(path: str | Path) -> list[dict[str, Any]]:
    return read_series(path, VARIABLE_ID, UNIT)


def signed_change_l0_003(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    result = signed_change_signal(
        records,
        horizon,
        VARIABLE_ID,
        UNIT,
        OFFSETS,
        falling_signal=-1,
        rising_signal=1,
        direction_mapping="ETF holdings fell -> -1; unchanged -> 0; ETF holdings rose -> +1",
    )
    result["trace_context"] = {
        "unit_or_scale": UNIT,
        "meaning": "global gold ETF holdings stock",
        "observed_cadence": "monthly",
        "registry_cadence_note": "registry release frequency is daily; preserved handoff is monthly",
        "direction_condition": "registry direction is Conditional",
    }
    return result
