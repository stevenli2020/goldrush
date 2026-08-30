"""Build the canonical Phase 3 handoff for L3-005."""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle); rows = list(reader)
    required = {"variable_id", "sep_release_date", "projection_horizon", "rate_bin_midpoint", "participant_count", "median_projected_rate", "unit", "validation_status", "availability_status"}
    if not reader.fieldnames or not required.issubset(reader.fieldnames) or not rows:
        raise ValueError("L3-005 processed input is invalid or empty")
    if any(r["variable_id"] != "L3-005" or r["unit"] != "percent" for r in rows):
        raise ValueError("L3-005 input contains an invalid SEP record")
    return rows

def build_handoff(rows: list[dict[str, str]], source_reference: str) -> list[dict[str, object]]:
    return [{"variable_id": "L3-005", "observation_timestamp": f"{r['sep_release_date']}T00:00:00Z",
             "value": float(r["rate_bin_midpoint"]), "unit_or_scale": "percent",
             "projection_horizon": r["projection_horizon"], "participant_count": int(r["participant_count"]),
             "median_projected_rate": float(r["median_projected_rate"]), "availability_status": r["availability_status"],
             "source_reference": source_reference, "quality_flag": r["validation_status"]} for r in rows]

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--input", type=Path, required=True); parser.add_argument("--source-reference", required=True); parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(); output = build_handoff(load_rows(args.input), args.source_reference)
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(output), "output": str(args.output)})); return 0

if __name__ == "__main__": raise SystemExit(main())
