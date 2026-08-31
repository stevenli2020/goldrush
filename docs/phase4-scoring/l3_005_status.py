"""Reader and status-only method for approved L3-005 MVP treatment."""
from pathlib import Path
from typing import Any

from _ep_signal_common import HORIZONS, read_structure, status_only_method as _status_only

VARIABLE_ID = "L3-005"
UNIT = "percent"
CONTEXT_KEY = "dot_plot_context"
INCOMPLETE_HORIZONS = {"1-3 months", "1-3 years"}


def read_l3_005(path: str | Path) -> list[dict[str, Any]]:
    return read_structure(path, VARIABLE_ID, {UNIT}, {"projection_horizon", "participant_count", "median_projected_rate"})


def status_only_l3_005(record: Any, horizon: str, context: Any = None) -> dict[str, Any]:
    return _status_only(
        record,
        horizon,
        VARIABLE_ID,
        UNIT,
        context,
        CONTEXT_KEY,
        "E",
        INCOMPLETE_HORIZONS,
        "missing projection-horizon/statistic selection metadata",
    )


status_only_method = status_only_l3_005
