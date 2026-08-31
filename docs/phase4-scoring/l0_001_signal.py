"""Reader and signed-change signal for approved L0-001."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from _l1_signal_common import read_series, signed_change_signal


VARIABLE_ID = "L0-001"
UNIT = "metric_tonnes"
OFFSETS = {"1-3 years": 3, "3-10 years": 10}
SHORT_HORIZONS = {"1-5 days", "1-3 months"}


def read_l0_001(path: str | Path) -> list[dict[str, Any]]:
    return read_series(path, VARIABLE_ID, UNIT)


def signed_change_l0_001(records: list[dict[str, Any]], horizon: str) -> dict[str, Any]:
    # Phase 4 MVP: return neutral 0 for excluded short horizons instead of N/A.
    # This keeps the Net Index calculable. Approved by owner on 2026-08-31.
    if horizon in SHORT_HORIZONS:
        current = max(records, key=lambda row: row["observation_timestamp"]) if records else None
        return {
            "variable_id": VARIABLE_ID,
            "horizon": horizon,
            "status": "FLAGGED" if current and current.get("availability_status") == "FLAG" else "AVAILABLE",
            "signal": 0,
            "reason": "Static annual data – no meaningful change within 5 days/3 months (Phase 4 MVP override)",
            "override": True,
            "current": current,
            "prior": None,
            "delta_percentage_points": None,
            "source_references": [current["source_reference"]] if current and current.get("source_reference") else [],
            "flags": [current["quality_flag"]] if current and current.get("quality_flag") else [],
        }

    result = signed_change_signal(
        records,
        horizon,
        VARIABLE_ID,
        UNIT,
        OFFSETS,
        direction_mapping="above-ground stock fell -> +1; unchanged -> 0; above-ground stock rose -> -1",
    )
    result["trace_context"] = {
        "unit_or_scale": UNIT,
        "meaning": "above-ground gold stock",
        "direction_condition": "registry direction is Conditional; available-stock baseline",
    }
    return result
