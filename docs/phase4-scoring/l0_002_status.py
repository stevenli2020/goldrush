"""Cached IMF World aggregate holdings and moving-average L0-002 signals."""
from __future__ import annotations

import csv
import math
from calendar import monthrange
from datetime import date
from pathlib import Path
from typing import Any


VARIABLE_ID = "L0-002"
UNIT = "metric_tonnes"
HORIZONS = ("1-5 days", "1-3 months", "1-3 years", "3-10 years")
DEFAULT_CACHE_PATH = (
    Path(__file__).resolve().parents[1]
    / "phase2-ingestion/L0/002/processed/L0_002_aggregate_holdings.csv"
)
OUNCE_TO_TONNES = 31.1034768 / 1_000_000
REQUIRED_COLUMNS = ("date", "total_holdings_tonnes")


def _month_key(value: str) -> tuple[int, int]:
    parsed = date.fromisoformat(value)
    return parsed.year, parsed.month


def _month_index(key: tuple[int, int]) -> int:
    return key[0] * 12 + key[1]


def _month_timestamp(key: tuple[int, int]) -> str:
    year, month = key
    return f"{year:04d}-{month:02d}-{monthrange(year, month)[1]:02d}T00:00:00Z"


def read_aggregate_cache(path: str | Path = DEFAULT_CACHE_PATH) -> list[dict[str, Any]]:
    """Read and validate the cached monthly World aggregate series."""
    try:
        with Path(path).open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if tuple(reader.fieldnames or ()) != REQUIRED_COLUMNS:
                raise ValueError(f"aggregate cache columns must be {list(REQUIRED_COLUMNS)}")
            rows = list(reader)
    except OSError as exc:
        raise ValueError("L0-002 aggregate cache is not readable CSV") from exc
    if not rows:
        raise ValueError("L0-002 aggregate cache must contain records")
    parsed: list[dict[str, Any]] = []
    seen: set[tuple[int, int]] = set()
    for row in rows:
        try:
            key = _month_key(str(row["date"]))
            value = float(row["total_holdings_tonnes"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("invalid L0-002 aggregate cache row") from exc
        if not math.isfinite(value) or value < 0 or key in seen:
            raise ValueError("invalid or duplicate L0-002 aggregate cache row")
        seen.add(key)
        parsed.append({"date": f"{key[0]:04d}-{key[1]:02d}-{monthrange(*key)[1]:02d}", "total_holdings_tonnes": value, "month_key": key})
    return sorted(parsed, key=lambda row: row["month_key"])


def update_aggregate_cache(
    path: str | Path = DEFAULT_CACHE_PATH,
    end_date: str | None = None,
) -> list[dict[str, Any]]:
    """Fetch the World aggregate history, refreshing only the cached tail."""
    cache_path = Path(path)
    existing: dict[tuple[int, int], float] = {}
    if cache_path.exists():
        existing = {
            row["month_key"]: row["total_holdings_tonnes"]
            for row in read_aggregate_cache(cache_path)
        }
    start_date = "2000-01-01"
    if existing:
        latest = max(existing)
        start_date = f"{latest[0]:04d}-{latest[1]:02d}-01"
    requested_end = end_date or date.today().isoformat()

    # OpenBB is imported only when refreshing the cache; scoring remains a
    # deterministic local read of the saved aggregate series.
    from openbb import obb

    response = obb.economy.indicators(
        symbol="IL::RGV_REVS",
        country="G001",
        provider="imf",
        frequency="month",
        start_date=start_date,
        end_date=requested_end,
        use_cache=False,
    )
    frame = response.to_dataframe().reset_index()
    required = {"date", "value", "country_code"}
    if not required.issubset(frame.columns):
        raise ValueError(f"IMF World response missing columns: {sorted(required - set(frame.columns))}")
    frame = frame[frame["country_code"] == "G001"]
    for row in frame.to_dict(orient="records"):
        key = _month_key(str(row["date"]))
        raw_value = float(row["value"])
        if not math.isfinite(raw_value) or raw_value < 0:
            raise ValueError(f"invalid IMF aggregate value for {key}")
        existing[key] = raw_value * OUNCE_TO_TONNES

    if not existing:
        raise ValueError("IMF returned no aggregate World observations")
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "date": f"{key[0]:04d}-{key[1]:02d}-{monthrange(*key)[1]:02d}",
            "total_holdings_tonnes": existing[key],
        }
        for key in sorted(existing)
    ]
    with cache_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    return read_aggregate_cache(cache_path)


def _signal_result(
    horizon: str,
    rows: list[dict[str, Any]],
    signal: int,
    reason: str,
    moving_averages: dict[str, float] | None = None,
) -> dict[str, Any]:
    latest = rows[-1]
    return {
        "variable_id": VARIABLE_ID,
        "horizon": horizon,
        "status": "AVAILABLE",
        "signal": signal,
        "reason": reason,
        "current": {
            "timestamp": _month_timestamp(latest["month_key"]),
            "value": latest["total_holdings_tonnes"],
        },
        "moving_averages": moving_averages or {},
        "source_references": ["docs/phase2-ingestion/L0/002/processed/L0_002_aggregate_holdings.csv"],
        "flags": [],
        "trace_context": {
            "method": "moving-average crossover on IMF World aggregate",
            "unit_or_scale": UNIT,
            "meaning": "aggregate official central-bank gold holdings",
            "monthly_granularity": True,
        },
    }


def _window(values: list[float], requested: int) -> tuple[float | None, int]:
    if len(values) >= requested:
        size = requested
    elif len(values) >= 12:
        size = len(values)
    else:
        return None, 0
    return sum(values[-size:]) / size, size


def signed_change_l0_002(
    records: list[dict[str, Any]] | str | Path,
    horizon: str,
) -> dict[str, Any]:
    """Return the L0-002 moving-average signal for one horizon."""
    if horizon not in HORIZONS:
        raise ValueError(f"unknown {VARIABLE_ID} horizon: {horizon}")
    rows = read_aggregate_cache(records) if isinstance(records, (str, Path)) else records
    if not rows:
        return {"variable_id": VARIABLE_ID, "horizon": horizon, "status": "INCOMPLETE", "signal": None, "reason": "missing aggregate cache"}
    rows = sorted(rows, key=lambda row: row["month_key"])
    values = [float(row["total_holdings_tonnes"]) for row in rows]
    if horizon == "1-5 days":
        return _signal_result(horizon, rows, 0, "monthly data has no daily resolution")
    if horizon == "1-3 months":
        latest_ma = sum(values[-3:]) / 3 if len(values) >= 3 else _window(values, 3)[0]
        if latest_ma is None:
            return _signal_result(horizon, rows, 0, "insufficient history for a 12-month minimum moving average")
        signal = 1 if values[-1] > latest_ma else -1 if values[-1] < latest_ma else 0
        return _signal_result(horizon, rows, signal, "latest total versus 3-month moving average", {"latest": values[-1], "ma_3": latest_ma})

    short_requested, long_requested = (3, 36) if horizon == "1-3 years" else (12, 120)
    short_ma, short_size = _window(values, short_requested)
    long_ma, long_size = _window(values, long_requested)
    if short_ma is None or long_ma is None:
        return _signal_result(horizon, rows, 0, "insufficient history for a 12-month minimum moving average")
    signal = 1 if short_ma > long_ma else -1 if short_ma < long_ma else 0
    return _signal_result(
        horizon,
        rows,
        signal,
        f"{short_size}-month moving average versus {long_size}-month moving average",
        {"short_ma": short_ma, "long_ma": long_ma},
    )


def signal_l0_002(source: str | Path = DEFAULT_CACHE_PATH, horizon: str = "1-3 years") -> dict[str, Any]:
    return signed_change_l0_002(source, horizon)


status_only_l0_002 = signed_change_l0_002
status_only_method = signed_change_l0_002

