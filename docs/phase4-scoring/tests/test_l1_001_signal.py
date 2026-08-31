import importlib.util
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[3]
MODULE_PATH = ROOT / "docs/phase4-scoring/l1_001_signal.py"
spec = importlib.util.spec_from_file_location("l1_001_signal", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


def record(index: int, value: float, status: str = "AVAILABLE", quality: str = "OK"):
    timestamp = datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(days=index - 1)
    return {
        "variable_id": "L1-001",
        "observation_timestamp": timestamp.isoformat().replace("+00:00", "Z"),
        "value": value,
        "unit_or_scale": "percent",
        "availability_status": status,
        "source_reference": "fixture:DFII10",
        "quality_flag": quality,
    }


def test_reader_sorts_and_rejects_invalid_contract(tmp_path):
    path = tmp_path / "handoff.json"
    path.write_text(json.dumps([record(2, 2.0), record(1, 2.1)]), encoding="utf-8")
    assert [row["observation_timestamp"] for row in module.read_l1_001(path)] == [
        "2026-01-01T00:00:00Z",
        "2026-01-02T00:00:00Z",
    ]
    invalid_rows = [
        ({**record(1, 2.0), "unit_or_scale": "basis_points"}, "unit_or_scale"),
        ({**record(1, 2.0), "variable_id": "L1-002"}, "non-L1-001"),
        ({**record(1, 2.0), "observation_timestamp": "not-a-date"}, "timestamp"),
        ({**record(1, 2.0), "value": "NaN"}, "finite"),
    ]
    for row, message in invalid_rows:
        path.write_text(json.dumps([row]), encoding="utf-8")
        with pytest.raises(ValueError, match=message):
            module.read_l1_001(path)

    path.write_text(json.dumps([record(1, 2.0), record(1, 2.1)]), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate"):
        module.read_l1_001(path)


@pytest.mark.parametrize("horizon,offset", module.OFFSETS.items())
def test_signal_uses_configured_position_offset(horizon, offset):
    rows = [record(i + 1, 3.0) for i in range(offset + 1)]
    rows[0]["value"] = 3.1
    rows[-1]["value"] = 2.9
    result = module.signed_change_signal(rows, horizon)
    assert result["status"] == "AVAILABLE"
    assert result["signal"] == 1
    assert result["prior"]["offset_positions"] == offset
    assert result["delta_percentage_points"] == pytest.approx(-0.2)


def test_signal_returns_all_three_directions():
    rows = [record(i + 1, 3.0) for i in range(6)]
    rows[-1]["value"] = 3.0
    assert module.signed_change_signal(rows, "1-5 days")["signal"] == 0
    rows[-1]["value"] = 3.2
    assert module.signed_change_signal(rows, "1-5 days")["signal"] == -1
    rows[-1]["value"] = 2.8
    assert module.signed_change_signal(rows, "1-5 days")["signal"] == 1


def test_flagged_current_record_remains_visibly_flagged():
    rows = [record(i + 1, 3.0) for i in range(6)]
    rows[0]["value"] = 3.1
    rows[-1] = record(6, 2.9, status="FLAG", quality="LOW_COVERAGE")
    result = module.signed_change_signal(rows, "1-5 days")
    assert result["status"] == "FLAGGED"
    assert result["signal"] == 1
    assert "LOW_COVERAGE" in result["flags"]


def test_missing_or_insufficient_history_is_incomplete():
    result = module.signed_change_signal([record(1, 2.0)], "1-5 days")
    assert result["status"] == "INCOMPLETE"
    assert result["signal"] is None
    rows = [record(i + 1, 3.0) for i in range(6)]
    rows[-1]["availability_status"] = "STALE"
    assert module.signed_change_signal(rows, "1-5 days")["status"] == "INCOMPLETE"


def test_stale_prior_record_is_incomplete():
    rows = [record(i + 1, 3.0) for i in range(6)]
    rows[0]["availability_status"] = "STALE"
    result = module.signed_change_signal(rows, "1-5 days")
    assert result["status"] == "INCOMPLETE"
    assert result["reason"] == "prior record is STALE"
    assert result["signal"] is None


def test_reader_accepts_preserved_l1_001_handoff():
    path = ROOT / "docs/phase3-ai-evidence/L1/001/data/l1_001_phase3_handoff.json"
    rows = module.read_l1_001(path)
    assert len(rows) == 5918
    assert rows[-1]["availability_status"] == "AVAILABLE"
