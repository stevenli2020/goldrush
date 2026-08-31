"""Reader and provisional signed-change signal for L1-005."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _l1_signal_common import read_series, signed_change_signal


VARIABLE_ID = "L1-005"
UNIT = "percent"
OFFSETS = {"1-3 months": 63, "1-3 years": 252}
DIRECTION_STATUS = "provisional_conditional_opportunity_cost_proxy"


def read_l1_005(path: str | Path) -> list[dict[str, Any]]:
    """Read and validate only the preserved L1-005 term-premium series."""
    return read_series(path, VARIABLE_ID, UNIT)


def signed_change_l1_005(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    """Return the provisional conditional opportunity-cost signed-change signal."""
    result = signed_change_signal(records, horizon, VARIABLE_ID, UNIT, OFFSETS)
    result["direction_status"] = DIRECTION_STATUS
    return result
