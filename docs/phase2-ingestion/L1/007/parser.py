"""Build the L1-007 5Y5Y real-forward proxy from DFII5 and DFII10."""
from __future__ import annotations
import argparse, csv, hashlib, json, math
from datetime import datetime, timezone
from pathlib import Path

VARIABLE_ID = "L1-007"
SERIES_5Y = "DFII5"
SERIES_10Y = "DFII10"
FORMULA_VERSION = "5y5y-real-forward-compound-v1"
PARSER_VERSION = "0.1.0"
FIELDS = [
    "variable_id", "observation_date", "value", "unit", "source_name",
    "input_5y_series_id", "input_10y_series_id", "input_5y_raw_path",
    "input_10y_raw_path", "input_5y_raw_sha256", "input_10y_raw_sha256",
    "input_5y_retrieved_at", "input_10y_retrieved_at", "formula_version",
    "parser_version", "validation_status", "availability_status",
]


def load_series(path: Path) -> tuple[dict[str, float], str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    items = payload.get("observations") if isinstance(payload, dict) else None
    if not isinstance(items, list):
        raise ValueError(f"{path} does not contain an observations list")
    values = {}
    for item in items:
        raw_value = item.get("value")
        if raw_value in (None, "", "."):
            continue
        try:
            datetime.strptime(str(item["date"]), "%Y-%m-%d")
            values[str(item["date"])] = float(raw_value)
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"invalid FRED observation in {path}: {item}") from exc
    if not values:
        raise ValueError(f"{path} contains no usable observations")
    return values, hashlib.sha256(path.read_bytes()).hexdigest()


def calculate_forward(real_5y: float, real_10y: float) -> float:
    base_5y, base_10y = 1 + real_5y / 100, 1 + real_10y / 100
    if base_5y <= 0 or base_10y <= 0:
        raise ValueError("real yield is at or below -100%, cannot compound")
    return 100 * ((base_10y**10 / base_5y**5) ** (1 / 5) - 1)


def parse_observations(
    dfii5_path: Path,
    dfii10_path: Path,
    *,
    dfii5_retrieved_at: str,
    dfii10_retrieved_at: str,
    stale_after_days: int = 7,
) -> list[dict[str, object]]:
    five_year, hash_5y = load_series(dfii5_path)
    ten_year, hash_10y = load_series(dfii10_path)
    now = datetime.now(timezone.utc)
    rows = []
    for date_text in sorted(set(five_year) & set(ten_year)):
        date = datetime.strptime(date_text, "%Y-%m-%d").date()
        value = calculate_forward(five_year[date_text], ten_year[date_text])
        rows.append({
            "variable_id": VARIABLE_ID,
            "observation_date": date_text,
            "value": value,
            "unit": "percent",
            "source_name": "FRED-derived",
            "input_5y_series_id": SERIES_5Y,
            "input_10y_series_id": SERIES_10Y,
            "input_5y_raw_path": str(dfii5_path),
            "input_10y_raw_path": str(dfii10_path),
            "input_5y_raw_sha256": hash_5y,
            "input_10y_raw_sha256": hash_10y,
            "input_5y_retrieved_at": dfii5_retrieved_at,
            "input_10y_retrieved_at": dfii10_retrieved_at,
            "formula_version": FORMULA_VERSION,
            "parser_version": PARSER_VERSION,
            "validation_status": "PASS" if -10 <= value <= 20 else "FLAG",
            "availability_status": "STALE" if (now.date() - date).days > stale_after_days else "AVAILABLE",
        })
    if not rows:
        raise ValueError("DFII5 and DFII10 have no overlapping usable dates")
    return rows


def write_csv(rows: list[dict[str, object]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Parse the L1-007 5Y5Y real-forward proxy")
    ap.add_argument("--dfii5", type=Path, required=True)
    ap.add_argument("--dfii10", type=Path, required=True)
    ap.add_argument("--dfii5-retrieved-at", required=True)
    ap.add_argument("--dfii10-retrieved-at", required=True)
    ap.add_argument("--output", type=Path, default=Path("data/processed/L1_007_observations.csv"))
    args = ap.parse_args(argv)
    rows = parse_observations(args.dfii5, args.dfii10, dfii5_retrieved_at=args.dfii5_retrieved_at, dfii10_retrieved_at=args.dfii10_retrieved_at)
    write_csv(rows, args.output)
    print(f"Wrote {len(rows)} observations to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
