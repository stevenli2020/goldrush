import csv
import importlib.util
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_phase4_handoff.py"
spec = importlib.util.spec_from_file_location("l3_004_handoff", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def write_input(path: Path, rows: list[dict[str, str]]) -> None:
    fields = list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def rows() -> list[dict[str, str]]:
    common = {
        "variable_id": "L3-004",
        "observation_date": "2026-08-27",
        "current_target_lower_pct": "3.5",
        "source_manifest_path": "manifest.json",
        "validation_status": "PASS",
        "availability_status": "AVAILABLE",
    }
    return [
        {**common, "meeting_date": "2026-09-16", "target_rate_lower_pct": "3.25", "probability": "0.2"},
        {**common, "meeting_date": "2026-09-16", "target_rate_lower_pct": "3.5", "probability": "0.5"},
        {**common, "meeting_date": "2026-09-16", "target_rate_lower_pct": "3.75", "probability": "0.3"},
    ]


def test_handoff_preserves_probability_categories_and_expected_change(tmp_path):
    path = tmp_path / "input.csv"
    write_input(path, rows())
    result = module.handoff_rows(module.load_latest_distribution(path))
    values = {row["unit_or_scale"]: row["value"] for row in result}
    assert values == pytest.approx({
        "probability_easing_0_to_1": 0.2,
        "probability_hold_0_to_1": 0.5,
        "probability_tightening_0_to_1": 0.3,
        "expected_target_change_bps": 2.5,
    })
    assert {row["meeting_date"] for row in result} == {"2026-09-16"}
    assert {row["quality_flag"] for row in result} == {"PASS"}


def test_handoff_rejects_distribution_that_does_not_sum_to_one(tmp_path):
    path = tmp_path / "input.csv"
    invalid = rows()
    invalid[0]["probability"] = "0.3"
    write_input(path, invalid)
    with pytest.raises(ValueError, match="sum to one"):
        module.handoff_rows(module.load_latest_distribution(path))
