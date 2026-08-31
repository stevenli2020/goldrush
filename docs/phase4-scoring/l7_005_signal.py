"""Reader and signed-change signal for approved L7-005."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _l1_signal_common import read_series, signed_change_signal


VARIABLE_ID = "L7-005"
UNIT = "basis_points"
OFFSETS = {"1-5 days": 5, "1-3 months": 63, "1-3 years": 252}


def read_l7_005(path: str | Path) -> list[dict[str, Any]]:
    return read_series(path, VARIABLE_ID, UNIT)


def signed_change_l7_005(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    result = signed_change_signal(
        records,
        horizon,
        VARIABLE_ID,
        UNIT,
        OFFSETS,
        falling_signal=-1,
        rising_signal=1,
        direction_mapping="Treasury repo spread narrowed -> -1; unchanged -> 0; Treasury repo spread widened -> +1",
    )
    result["trace_context"] = {
        "unit_or_scale": UNIT,
        "meaning": "daily SOFR-minus-EFFR secured-funding spread",
        "observed_cadence": "daily",
        "stress_measure": "change in the already-derived spread; no absolute-level threshold",
        "direction_condition": "registry direction is Conditional; widening-stress baseline",
    }
    return result
