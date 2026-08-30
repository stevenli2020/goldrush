"""Convert L3-004 probability buckets into compact Phase 4 handoff rows."""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path


VARIABLE_ID = "L3-004"
REQUIRED_COLUMNS = {
    "variable_id",
    "observation_date",
    "meeting_date",
    "target_rate_lower_pct",
    "probability",
    "current_target_lower_pct",
    "source_manifest_path",
    "validation_status",
    "availability_status",
}


def load_latest_distribution(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not REQUIRED_COLUMNS.issubset(reader.fieldnames):
            raise ValueError("L3-004 input is missing required columns")
        rows = [row for row in reader if row["variable_id"] == VARIABLE_ID]
    if not rows:
        raise ValueError("L3-004 input has no rows")
    latest_date = max(row["observation_date"] for row in rows)
    rows = [row for row in rows if row["observation_date"] == latest_date]
    statuses = {row["validation_status"] for row in rows}
    availability = {row["availability_status"] for row in rows}
    if not statuses.issubset({"PASS", "FLAG"}) or len(availability) != 1:
        raise ValueError("latest L3-004 distribution is not usable")
    return rows


def handoff_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    observation_dates = {row["observation_date"] for row in rows}
    manifests = {row["source_manifest_path"] for row in rows}
    target_lowers = {float(row["current_target_lower_pct"]) for row in rows}
    if len(observation_dates) != 1 or len(manifests) != 1 or len(target_lowers) != 1:
        raise ValueError("L3-004 distribution has inconsistent shared metadata")

    observation_date = observation_dates.pop()
    manifest = manifests.pop()
    current_lower = target_lowers.pop()
    availability = rows[0]["availability_status"]
    quality_flag = "FLAG" if any(row["validation_status"] == "FLAG" for row in rows) else "PASS"
    by_meeting: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_meeting[row["meeting_date"]].append(row)

    result = []
    for meeting_date, buckets in sorted(by_meeting.items()):
        total = sum(float(row["probability"]) for row in buckets)
        if not math.isclose(total, 1.0, abs_tol=0.001):
            raise ValueError(f"probabilities do not sum to one for {meeting_date}")
        easing = sum(float(row["probability"]) for row in buckets if float(row["target_rate_lower_pct"]) < current_lower)
        hold = sum(float(row["probability"]) for row in buckets if math.isclose(float(row["target_rate_lower_pct"]), current_lower, abs_tol=1e-9))
        tightening = sum(float(row["probability"]) for row in buckets if float(row["target_rate_lower_pct"]) > current_lower)
        expected_change_bps = sum(
            float(row["probability"]) * (float(row["target_rate_lower_pct"]) - current_lower) * 100
            for row in buckets
        )
        measures = {
            "probability_easing_0_to_1": easing,
            "probability_hold_0_to_1": hold,
            "probability_tightening_0_to_1": tightening,
            "expected_target_change_bps": expected_change_bps,
        }
        for unit_or_scale, value in measures.items():
            result.append({
                "variable_id": VARIABLE_ID,
                "observation_timestamp": f"{observation_date}T00:00:00Z",
                "meeting_date": meeting_date,
                "value": value,
                "unit_or_scale": unit_or_scale,
                "availability_status": availability,
                "source_reference": manifest,
                "quality_flag": quality_flag,
            })
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the Phase 4 L3-004 handoff")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    output = handoff_rows(load_latest_distribution(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(output), "output": str(args.output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
