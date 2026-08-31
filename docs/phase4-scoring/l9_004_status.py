"""Reader and status-only method for approved L9-004 component-panel treatment."""
from pathlib import Path
from typing import Any

from _ep_signal_common import read_structure, status_only_method as _status_only


VARIABLE_ID = "L9-004"
UNIT = "metric_tonnes"
CONTEXT_KEY = "component_panel_context"


def read_l9_004(path: str | Path) -> list[dict[str, Any]]:
    """Read the preserved panel without selecting or combining components."""
    return read_structure(path, VARIABLE_ID, {UNIT}, set())


def status_only_l9_004(record: Any, horizon: str, context: Any = None) -> dict[str, Any]:
    return _status_only(record, horizon, VARIABLE_ID, UNIT, context, CONTEXT_KEY, "P")


status_only_method = status_only_l9_004
