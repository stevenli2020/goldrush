"""Reader and status-only method for approved L5-002 MVP treatment."""
from pathlib import Path
from typing import Any

from _ep_signal_common import HORIZONS, read_structure, status_only_method as _status_only

VARIABLE_ID = "L5-002"
UNIT = "fraction"
CONTEXT_KEY = "panel_context"


def read_l5_002(path: str | Path) -> list[dict[str, Any]]:
    return read_structure(path, VARIABLE_ID, {UNIT}, set(), reject_duplicate_rows=False)


def status_only_l5_002(record: Any, horizon: str, context: Any = None) -> dict[str, Any]:
    return _status_only(record, horizon, VARIABLE_ID, UNIT, context, CONTEXT_KEY, "P")


status_only_method = status_only_l5_002
