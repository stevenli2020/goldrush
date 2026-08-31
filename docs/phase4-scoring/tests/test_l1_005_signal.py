import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[3]
MODULE_DIR = ROOT / "docs/phase4-scoring"
sys.path.insert(0, str(MODULE_DIR))

from l1_005_signal import (  # noqa: E402
    OFFSETS,
    DIRECTION_STATUS,
    read_l1_005,
    signed_change_l1_005,
)


def record(index: int, value: float, status: str = "AVAILABLE", quality: str = "OK"):
    timestamp = datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(days=index - 1)
    return {
        "variable_id": "L1-005",
        "observation_timestamp": timestamp.isoformat().replace("+00:00", "Z"),
        "value": value,
        "unit_or_scale": "percent",
        "availability_status": status,
        "source_reference": "fixture:l1-005",
        "quality_flag": quality,
    }


def test_reader_loads_preserved_series_and_sorts():
    path = ROOT / "docs/phase3-ai-evidence/L1/005/data/l1_005_phase3_handoff.json"
    rows = read_l1_005(path)
    assert len(rows) == 9146
    assert rows == sorted(rows, key=lambda row: row["observation_timestamp"])
    assert all(row["variable_id"] == "L1-005" and row["unit_or_scale"] == "percent" for row in rows)


def test_reader_rejects_invalid_contract(tmp_path):
    path = tmp_path / "rows.json"
    row = record(1, 2.0)
    for invalid, message in [
        ({**row, "variable_id": "OTHER"}, "non-"),
        ({**row, "unit_or_scale": "basis_points"}, "unit_or_scale"),
        ({**row, "observation_timestamp": "bad"}, "timestamp"),
        ({**row, "value": "NaN"}, "finite"),
        ({**row, "availability_status": "UNKNOWN"}, "availability_status"),
        ({**row, "source_reference": ""}, "source_reference"),
    ]:
        path.write_text(json.dumps([invalid]), encoding="utf-8")
        with pytest.raises(ValueError, match=message):
            read_l1_005(path)
    path.write_text(json.dumps([row, row]), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate"):
        read_l1_005(path)


def test_signal_uses_exact_offsets_and_trace_fields():
    offset = OFFSETS["1-3 months"]
    rows = [record(i + 1, 3.0) for i in range(offset + 1)]
    rows[0]["value"] = 3.1
    rows[-1]["value"] = 2.9
    result = signed_change_l1_005(rows, "1-3 months")
    assert result["status"] == "AVAILABLE"
    assert result["signal"] == 1
    assert result["prior"]["offset_positions"] == offset
    assert result["delta_percentage_points"] == pytest.approx(-0.2)
    assert result["direction_status"] == DIRECTION_STATUS
    assert {"variable_id", "horizon", "current", "prior", "delta_percentage_points", "direction_mapping", "source_references", "flags", "direction_status"} <= result.keys()


@pytest.mark.parametrize("current, expected", [(3.0, 0), (3.2, -1), (2.8, 1)])
def test_signal_maps_falling_unchanged_and_rising(current, expected):
    rows = [record(i + 1, 3.0) for i in range(OFFSETS["1-3 years"] + 1)]
    rows[-1]["value"] = current
    assert signed_change_l1_005(rows, "1-3 years")["signal"] == expected


def test_flag_stale_blocked_and_prior_statuses_are_explicit():
    rows = [record(i + 1, 3.0) for i in range(OFFSETS["1-3 months"] + 1)]
    rows[0]["value"] = 3.1
    rows[-1] = record(OFFSETS["1-3 months"] + 1, 2.9, status="FLAG", quality="LOW_COVERAGE")
    flagged = signed_change_l1_005(rows, "1-3 months")
    assert flagged["status"] == "FLAGGED" and flagged["signal"] == 1
    assert "LOW_COVERAGE" in flagged["flags"]
    rows[-1]["availability_status"] = "STALE"
    assert signed_change_l1_005(rows, "1-3 months")["status"] == "INCOMPLETE"
    rows[-1]["availability_status"] = "BLOCKED"
    assert signed_change_l1_005(rows, "1-3 months")["status"] == "INCOMPLETE"
    rows[-1] = record(OFFSETS["1-3 months"] + 1, 2.9)
    rows[0]["availability_status"] = "STALE"
    prior_stale = signed_change_l1_005(rows, "1-3 months")
    assert prior_stale["status"] == "INCOMPLETE"
    assert prior_stale["reason"] == "prior record is STALE"
    rows[0]["availability_status"] = "BLOCKED"
    prior_blocked = signed_change_l1_005(rows, "1-3 months")
    assert prior_blocked["status"] == "INCOMPLETE"
    assert prior_blocked["reason"] == "prior record is BLOCKED"


def test_missing_malformed_insufficient_and_not_applicable_are_explicit():
    assert signed_change_l1_005([], "1-3 months")["status"] == "INCOMPLETE"
    rows = [record(i + 1, 3.0) for i in range(OFFSETS["1-3 months"])]
    assert signed_change_l1_005(rows, "1-3 months")["status"] == "INCOMPLETE"
    malformed = [record(i + 1, 3.0) for i in range(OFFSETS["1-3 months"] + 1)]
    del malformed[-1]["source_reference"]
    assert signed_change_l1_005(malformed, "1-3 months")["status"] == "INCOMPLETE"
    for horizon in ("1-5 days", "3-10 years"):
        result = signed_change_l1_005([], horizon)
        assert result["status"] == "NOT_APPLICABLE"
        assert result["direction_status"] == DIRECTION_STATUS


def test_real_preserved_handoff_remains_incomplete_under_stale_status_rule():
    path = ROOT / "docs/phase3-ai-evidence/L1/005/data/l1_005_phase3_handoff.json"
    rows = read_l1_005(path)
    result = signed_change_l1_005(rows, "1-3 months")
    assert result["status"] == "INCOMPLETE"
    assert result["reason"] == "current record is not eligible"
    assert result["direction_status"] == DIRECTION_STATUS
