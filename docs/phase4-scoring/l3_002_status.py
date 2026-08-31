"""Reader and status-only method for approved L3-002 MVP treatment."""
from pathlib import Path
from typing import Any

from _ep_signal_common import HORIZONS, read_structure, status_only_method as _status_only

VARIABLE_ID = "L3-002"
UNIT = "percent_per_annum"
CONTEXT_KEY = "curve_context"


def read_l3_002(path: str | Path) -> list[dict[str, Any]]:
    return read_structure(path, VARIABLE_ID, {UNIT}, {"contract"})


def status_only_l3_002(record: Any, horizon: str, context: Any = None) -> dict[str, Any]:
    return _status_only(record, horizon, VARIABLE_ID, UNIT, context, CONTEXT_KEY, "E")


status_only_method = status_only_l3_002
