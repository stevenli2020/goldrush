"""Reader and signed-change signal for approved L1-003."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _l1_signal_common import read_series, signed_change_signal


VARIABLE_ID = "L1-003"
UNIT = "percent"
OFFSETS = {"1-3 months": 63, "1-3 years": 252, "3-10 years": 756}


def read_l1_003(path: str | Path) -> list[dict[str, Any]]:
    return read_series(path, VARIABLE_ID, UNIT)


def signed_change_l1_003(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    return signed_change_signal(records, horizon, VARIABLE_ID, UNIT, OFFSETS)
