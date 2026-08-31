"""Reader and status-only method for approved L0-009 MVP treatment."""
from pathlib import Path
from typing import Any

from _n_signal_common import HORIZONS, read_scalar, status_only_method as _status_only

VARIABLE_ID = "L0-009"
UNIT = "percent_per_annum"


def read_l0_009(path: str | Path) -> dict[str, Any]:
    return read_scalar(path, VARIABLE_ID, UNIT)


def status_only_l0_009(record: Any, horizon: str) -> dict[str, Any]:
    return _status_only(record, horizon, VARIABLE_ID, UNIT)


status_only_method_l0_009 = status_only_l0_009
status_only_method = status_only_l0_009
