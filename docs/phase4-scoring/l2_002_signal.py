"""Reader and signed-change signal for approved L2-002."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _l1_signal_common import read_series, signed_change_signal


VARIABLE_ID = "L2-002"
UNIT = "index_jan_2006_100_not_seasonally_adjusted"
OFFSETS = {"1-5 days": 5, "1-3 months": 63, "1-3 years": 252, "3-10 years": 756}


def read_l2_002(path: str | Path) -> list[dict[str, Any]]:
    return read_series(path, VARIABLE_ID, UNIT)


def signed_change_l2_002(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    result = signed_change_signal(
        records, horizon, VARIABLE_ID, UNIT, OFFSETS,
        direction_mapping="index fell -> +1; unchanged -> 0; index rose -> -1",
    )
    result["trace_context"] = {
        "unit_or_scale": UNIT,
        "index_name": "Broad Trade-Weighted Nominal US Dollar Index",
        "index_base": "January 2006 = 100; not seasonally adjusted",
    }
    return result
