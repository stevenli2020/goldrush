"""Build the canonical Phase 3 handoff for L0-003."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REQUIRED = {"observation_date", "region", "holdings_tonnes", "unit", "validation_status", "availability_status"}


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            raise ValueError("L0-003 processed input is missing required columns")
        rows = list(reader)
    if not rows or any(row["region"] != "GLOBAL" for row in rows):
        raise ValueError("L0-003 input must contain global observations")
    if any(row["availability_status"] != "AVAILABLE" for row in rows):
        raise ValueError("L0-003 input contains unavailable observations")
    return rows


def build_handoff(rows: list[dict[str, str]], source_reference: str) -> list[dict[str, object]]:
    result = []
    for row in rows:
        value = float(row["holdings_tonnes"])
        if value < 0 or row["unit"] != "metric_tonnes":
            raise ValueError("L0-003 holdings must be non-negative metric tonnes")
        result.append({
            "variable_id": "L0-003",
            "observation_timestamp": f"{row['observation_date']}T00:00:00Z",
            "value": value,
            "unit_or_scale": "metric_tonnes",
            "availability_status": row["availability_status"],
            "source_reference": source_reference,
            "quality_flag": row["validation_status"],
        })
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.source_manifest.exists():
        raise FileNotFoundError(args.source_manifest)
    output = build_handoff(load_rows(args.input), args.source_manifest.as_posix())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(output), "output": str(args.output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
