"""Shared validation and status-only responses for E/P-class inputs."""
from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


HORIZONS = ("1-5 days", "1-3 months", "1-3 years", "3-10 years")
REQUIRED_FIELDS = {
    "variable_id",
    "observation_timestamp",
    "value",
    "unit_or_scale",
    "availability_status",
    "source_reference",
    "quality_flag",
}
ALLOWED_STATUSES = {"AVAILABLE", "FLAG", "STALE", "BLOCKED"}


def validate_record(record: Any, variable_id: str, unit: str) -> None:
    if not isinstance(record, dict):
        raise ValueError("input must be one canonical record object")
    missing = REQUIRED_FIELDS - record.keys()
    if missing:
        raise ValueError(f"missing canonical fields: {sorted(missing)}")
    if record["variable_id"] != variable_id:
        raise ValueError(f"input variable_id must be {variable_id}")
    if record["unit_or_scale"] != unit:
        raise ValueError(f"{variable_id} unit_or_scale must be {unit}")
    if record["availability_status"] not in ALLOWED_STATUSES:
        raise ValueError("invalid availability_status")
    try:
        datetime.fromisoformat(record["observation_timestamp"].replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError("invalid observation_timestamp") from exc
    try:
        value = float(record["value"])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{variable_id} value must be numeric") from exc
    if not math.isfinite(value):
        raise ValueError(f"{variable_id} value must be finite")
    if not str(record["source_reference"]).strip():
        raise ValueError("source_reference is required")


def read_structure(
    path: str | Path,
    variable_id: str,
    units: set[str],
    required_context_fields: set[str],
    reject_duplicate_rows: bool = True,
) -> list[dict[str, Any]]:
    """Read and validate a non-empty preserved component/panel JSON structure."""
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{variable_id} preserved output is not readable JSON") from exc
    if not isinstance(payload, list) or not payload:
        raise ValueError(f"{variable_id} preserved output must be a non-empty record array")
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in payload:
        if not isinstance(row, dict):
            raise ValueError(f"{variable_id} preserved output contains a malformed record")
        missing = (REQUIRED_FIELDS | required_context_fields) - row.keys()
        if missing:
            raise ValueError(f"missing preserved fields: {sorted(missing)}")
        if row["variable_id"] != variable_id:
            raise ValueError(f"preserved record variable_id must be {variable_id}")
        if row["unit_or_scale"] not in units:
            raise ValueError(f"{variable_id} preserved unit_or_scale is invalid")
        validate_record({**row, "unit_or_scale": row["unit_or_scale"]}, variable_id, row["unit_or_scale"])
        identity = json.dumps(row, sort_keys=True, separators=(",", ":"))
        if reject_duplicate_rows and identity in seen:
            raise ValueError(f"duplicate preserved record for {variable_id}")
        seen.add(identity)
        rows.append(dict(row))
    return rows


def _trace(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        return {}
    return {key: record[key] for key in record if key in REQUIRED_FIELDS or key not in {"value"}}


def _flags(records: list[dict[str, Any]]) -> list[Any]:
    result: list[Any] = []
    for record in records:
        quality = record.get("quality_flag")
        if quality not in (None, "", "OK", "PASS") and quality not in result:
            result.append(quality)
        if record.get("availability_status") == "FLAG" and "FLAG" not in result:
            result.append("FLAG")
    return result


def status_only_method(
    record: Any,
    horizon: str,
    variable_id: str,
    unit: str,
    context: Any = None,
    context_key: str = "context",
    history_class: str = "E/P",
    incomplete_horizons: set[str] | None = None,
    incomplete_reason: str | None = None,
) -> dict[str, Any]:
    if horizon not in HORIZONS:
        raise ValueError(f"unknown {variable_id} horizon: {horizon}")
    try:
        validate_record(record, variable_id, unit)
        error = None
    except ValueError as exc:
        error = str(exc)

    context_rows = context if isinstance(context, list) else []
    base = {
        "variable": variable_id,
        "variable_id": variable_id,
        "horizon": horizon,
        "signal": None,
        "current": _trace(record),
        context_key: context_rows,
        "source_references": list(dict.fromkeys(
            ([record["source_reference"]] if isinstance(record, dict) and record.get("source_reference") else [])
            + [row["source_reference"] for row in context_rows if isinstance(row, dict) and row.get("source_reference")]
        )),
        "flags": _flags(([record] if isinstance(record, dict) else []) + [row for row in context_rows if isinstance(row, dict)]),
        "trace_context": {
            "method": "status-only",
            "history_class": history_class,
            "history_used": False,
            "context_row_count": len(context_rows),
        },
    }
    if error:
        return {**base, "status": "INCOMPLETE", "method_state": "INCOMPLETE", "reason": error}
    if record["availability_status"] in {"STALE", "BLOCKED"}:
        return {
            **base,
            "status": "INCOMPLETE",
            "method_state": "INCOMPLETE",
            "reason": f"current record is {record['availability_status']}",
        }
    if incomplete_horizons and horizon in incomplete_horizons:
        return {
            **base,
            "status": "INCOMPLETE",
            "method_state": "INCOMPLETE",
            "reason": incomplete_reason or "required selection metadata is missing",
        }
    return {
        **base,
        "status": "NOT_APPLICABLE",
        "method_state": "NOT_APPLICABLE",
        "reason": f"no approved numeric {variable_id} method for this MVP horizon",
    }
