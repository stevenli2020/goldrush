"""Build the canonical Phase 3 handoff for L2-002."""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle); rows = list(reader)
    required = {"variable_id", "observation_date", "index_value", "unit", "validation_status", "availability_status"}
    if not reader.fieldnames or not required.issubset(reader.fieldnames) or not rows:
        raise ValueError("L2-002 processed input is invalid or empty")
    if any(r["variable_id"] != "L2-002" or r["unit"] != "index" for r in rows):
        raise ValueError("L2-002 input contains an invalid index record")
    return rows

def build_handoff(rows: list[dict[str, str]], source_reference: str) -> list[dict[str, object]]:
    return [{"variable_id": "L2-002", "observation_timestamp": f"{r['observation_date']}T00:00:00Z",
             "value": float(r["index_value"]), "unit_or_scale": "index_jan_2006_100_not_seasonally_adjusted",
             "availability_status": r["availability_status"], "source_reference": source_reference,
             "quality_flag": r["validation_status"]} for r in rows]

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--input", type=Path, required=True); parser.add_argument("--source-reference", required=True); parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(); output = build_handoff(load_rows(args.input), args.source_reference)
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(output), "output": str(args.output)})); return 0

if __name__ == "__main__": raise SystemExit(main())
