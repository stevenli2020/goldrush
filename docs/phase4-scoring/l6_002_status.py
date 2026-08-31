"""Reader and status-only method for approved L6-002 event treatment."""
from pathlib import Path
from typing import Any

from _ep_signal_common import status_only_method as _status_only
from _n_signal_common import read_scalar


VARIABLE_ID = "L6-002"
UNIT = "sovereign_asset_freeze_score_0_to_100"
CONTEXT_KEY = "event_context"


def read_l6_002(path: str | Path) -> dict[str, Any]:
    """Read the canonical event score; scorer internals remain upstream."""
    return read_scalar(path, VARIABLE_ID, UNIT)


def status_only_l6_002(record: Any, horizon: str, context: Any = None) -> dict[str, Any]:
    context_rows = [context] if isinstance(context, dict) else context
    return _status_only(record, horizon, VARIABLE_ID, UNIT, context_rows, CONTEXT_KEY, "Q")


status_only_method = status_only_l6_002
