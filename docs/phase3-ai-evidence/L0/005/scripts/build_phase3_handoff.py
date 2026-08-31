"""Build the canonical Phase 3 handoff for L0-005."""
from __future__ import annotations
import argparse, calendar, csv, json
from pathlib import Path

REQUIRED = {"observation_period", "observation_period_type", "total_bar_and_coin_tonnes", "unit", "validation_status", "availability_status"}

def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            raise ValueError("L0-005 processed input is missing required columns")
        rows = list(reader)
    keys = [(r["observation_period"], r["observation_period_type"]) for r in rows]
    if not rows or len(keys) != len(set(keys)):
        raise ValueError("L0-005 processed input contains duplicate periods")
    if any(r["availability_status"] != "AVAILABLE" or r["validation_status"] == "FAIL" for r in rows):
        raise ValueError("L0-005 input contains unavailable or failed observations")
    return rows

def build_handoff(rows: list[dict[str, str]], source_reference: str) -> list[dict[str, object]]:
    result = []
    for row in rows:
        value = float(row["total_bar_and_coin_tonnes"])
        if value < 0 or row["unit"] != "metric_tonnes":
            raise ValueError("L0-005 demand must be non-negative metric tonnes")
        if row["observation_period_type"] == "annual":
            observation_date = f"{row['observation_year']}-12-31"
        else:
            year, quarter = int(row["observation_year"]), int(row["observation_quarter"])
            month = quarter * 3
            observation_date = f"{year}-{month:02d}-{calendar.monthrange(year, month)[1]:02d}"
        result.append({"variable_id": "L0-005", "observation_timestamp": f"{observation_date}T00:00:00Z",
                       "observation_period": row["observation_period"], "observation_period_type": row["observation_period_type"],
                       "value": value, "unit_or_scale": "metric_tonnes", "availability_status": row["availability_status"],
                       "source_reference": source_reference, "quality_flag": row["validation_status"]})
    return result

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True); parser.add_argument("--source-manifest", type=Path, required=True); parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.source_manifest.exists(): raise FileNotFoundError(args.source_manifest)
    output = build_handoff(load_rows(args.input), args.source_manifest.as_posix())
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(output), "output": str(args.output)})); return 0

if __name__ == "__main__": raise SystemExit(main())
