"""Reader and status-only method for approved L0-002 panel treatment."""
from __future__ import annotations

import csv
import math
from datetime import date
from pathlib import Path
from typing import Any

from _ep_signal_common import ALLOWED_STATUSES, status_only_method as _status_only


VARIABLE_ID = "L0-002"
UNIT = "metric_tonnes"
CONTEXT_KEY = "panel_context"


def read_l0_002(path: str | Path) -> list[dict[str, Any]]:
    """Read the preserved country panel without selecting or aggregating it."""
    try:
        with Path(path).open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except OSError as exc:
        raise ValueError("L0-002 preserved panel is not readable CSV") from exc
    if not rows:
        raise ValueError("L0-002 preserved panel must contain records")

    seen_countries: set[str] = set()
    for row in rows:
        if row.get("variable_id") != VARIABLE_ID:
            raise ValueError("preserved record variable_id must be L0-002")
        country = str(row.get("country", "")).strip()
        if not country:
            raise ValueError("L0-002 preserved panel country is required")
        if country in seen_countries:
            raise ValueError("duplicate L0-002 preserved panel country")
        seen_countries.add(country)
        if row.get("unit") != UNIT:
            raise ValueError("L0-002 preserved panel unit must be metric_tonnes")
        if row.get("availability_status") not in ALLOWED_STATUSES:
            raise ValueError("invalid availability_status")
        try:
            value = float(row.get("holdings_tonnes"))
        except (TypeError, ValueError) as exc:
            raise ValueError("L0-002 holdings_tonnes must be numeric") from exc
        if not math.isfinite(value):
            raise ValueError("L0-002 holdings_tonnes must be finite")
        try:
            date.fromisoformat(str(row.get("source_publication_date")))
        except ValueError as exc:
            raise ValueError("invalid source_publication_date") from exc
        if not str(row.get("source_file", "")).strip():
            raise ValueError("L0-002 source_file is required")
    return [dict(row) for row in rows]


def status_only_l0_002(record: Any, horizon: str, context: Any = None) -> dict[str, Any]:
    return _status_only(record, horizon, VARIABLE_ID, UNIT, context, CONTEXT_KEY, "P")


status_only_method = status_only_l0_002
