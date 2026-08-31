"""Reader and status-only method for approved L3-004 MVP treatment."""
from pathlib import Path
from typing import Any

from _ep_signal_common import HORIZONS, read_structure, status_only_method as _status_only

VARIABLE_ID = "L3-004"
UNIT = "expected_target_change_bps"
CONTEXT_KEY = "event_distribution_context"
INCOMPLETE_HORIZONS = {"1-5 days", "1-3 months"}


def read_l3_004(path: str | Path) -> list[dict[str, Any]]:
    return read_structure(
        path,
        VARIABLE_ID,
        {"probability_easing_0_to_1", "probability_hold_0_to_1", "probability_tightening_0_to_1", UNIT},
        {"meeting_date"},
    )


def status_only_l3_004(record: Any, horizon: str, context: Any = None) -> dict[str, Any]:
    return _status_only(
        record,
        horizon,
        VARIABLE_ID,
        UNIT,
        context,
        CONTEXT_KEY,
        "E",
        INCOMPLETE_HORIZONS,
        "missing meeting/component selection metadata",
    )


status_only_method = status_only_l3_004
