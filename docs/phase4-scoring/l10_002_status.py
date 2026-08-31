"""Reader and status-only method for approved L10-002 MVP treatment."""
from pathlib import Path
from typing import Any

from _n_signal_common import HORIZONS, read_scalar, status_only_method as _status_only

VARIABLE_ID = "L10-002"
UNIT = "contracts"


def read_l10_002(path: str | Path) -> dict[str, Any]:
    return read_scalar(path, VARIABLE_ID, UNIT)


def status_only_l10_002(record: Any, horizon: str) -> dict[str, Any]:
    return _status_only(record, horizon, VARIABLE_ID, UNIT)


status_only_method_l10_002 = status_only_l10_002
status_only_method = status_only_l10_002
