import importlib.util
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[3]
MODULE_DIR = ROOT / "docs/phase4-scoring"
sys.path.insert(0, str(MODULE_DIR))


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, MODULE_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


MODULES = [
    (load("l1_002_signal"), "L1-002", "l1_002_phase3_handoff.json", "1-5 days", 5, "3-10 years"),
    (load("l1_003_signal"), "L1-003", "l1_003_phase3_handoff.json", "1-3 months", 63, "1-5 days"),
    (load("l1_007_signal"), "L1-007", "l1_007_phase3_handoff.json", "1-3 years", 252, "1-5 days"),
]


def reader_for(module, variable_id):
    return getattr(module, f"read_{variable_id.lower().replace('-', '_')}")


def signal_for(module, variable_id):
    return getattr(module, f"signed_change_{variable_id.lower().replace('-', '_')}")


def record(variable_id: str, index: int, value: float, status: str = "AVAILABLE", quality: str = "OK"):
    timestamp = datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(days=index - 1)
    return {
        "variable_id": variable_id,
        "observation_timestamp": timestamp.isoformat().replace("+00:00", "Z"),
        "value": value,
        "unit_or_scale": "percent",
        "availability_status": status,
        "source_reference": "fixture:layer1",
        "quality_flag": quality,
    }


@pytest.mark.parametrize("module,variable_id,filename,horizon,offset,not_applicable", MODULES)
def test_reader_loads_preserved_series_and_sorts(module, variable_id, filename, horizon, offset, not_applicable):
    rows = reader_for(module, variable_id)(ROOT / f"docs/phase3-ai-evidence/L1/{variable_id[-3:]}/data/{filename}")
    assert len(rows) > offset
    assert rows == sorted(rows, key=lambda row: row["observation_timestamp"])
    assert all(row["variable_id"] == variable_id and row["unit_or_scale"] == "percent" for row in rows)


@pytest.mark.parametrize("module,variable_id,filename,horizon,offset,not_applicable", MODULES)
def test_reader_rejects_invalid_contract_for_each_variable(module, variable_id, filename, horizon, offset, not_applicable, tmp_path):
    path = tmp_path / "rows.json"
    row = record(variable_id, 1, 2.0)
    for invalid, message in [
        ({**row, "variable_id": "OTHER"}, "non-"),
        ({**row, "unit_or_scale": "basis_points"}, "unit_or_scale"),
        ({**row, "observation_timestamp": "bad"}, "timestamp"),
        ({**row, "value": "NaN"}, "finite"),
    ]:
        path.write_text(json.dumps([invalid]), encoding="utf-8")
        with pytest.raises(ValueError, match=message):
            reader_for(module, variable_id)(path)
    path.write_text(json.dumps([row, row]), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate"):
        reader_for(module, variable_id)(path)


@pytest.mark.parametrize("module,variable_id,filename,horizon,offset,not_applicable", MODULES)
def test_signal_uses_exact_offset_and_emits_trace(module, variable_id, filename, horizon, offset, not_applicable):
    rows = [record(variable_id, i + 1, 3.0) for i in range(offset + 1)]
    rows[0]["value"] = 3.1
    rows[-1]["value"] = 2.9
    result = signal_for(module, variable_id)(rows, horizon)
    assert result["status"] == "AVAILABLE"
    assert result["signal"] == 1
    assert result["prior"]["offset_positions"] == offset
    assert result["delta_percentage_points"] == pytest.approx(-0.2)
    assert {"variable_id", "horizon", "current", "prior", "delta_percentage_points", "direction_mapping", "source_references", "flags"} <= result.keys()
    assert result["current"]["timestamp"] and result["prior"]["timestamp"]


@pytest.mark.parametrize("module,variable_id,filename,horizon,offset,not_applicable", MODULES)
def test_signal_maps_all_three_directions(module, variable_id, filename, horizon, offset, not_applicable):
    rows = [record(variable_id, i + 1, 3.0) for i in range(offset + 1)]
    assert signal_for(module, variable_id)(rows, horizon)["signal"] == 0
    rows[-1]["value"] = 3.2
    assert signal_for(module, variable_id)(rows, horizon)["signal"] == -1
    rows[-1]["value"] = 2.8
    assert signal_for(module, variable_id)(rows, horizon)["signal"] == 1


@pytest.mark.parametrize("module,variable_id,filename,horizon,offset,not_applicable", MODULES)
def test_flag_and_unavailable_statuses_are_explicit(module, variable_id, filename, horizon, offset, not_applicable):
    rows = [record(variable_id, i + 1, 3.0) for i in range(offset + 1)]
    rows[0]["value"] = 3.1
    rows[-1] = record(variable_id, offset + 1, 2.9, status="FLAG", quality="LOW_COVERAGE")
    flagged = signal_for(module, variable_id)(rows, horizon)
    assert flagged["status"] == "FLAGGED" and flagged["signal"] == 1
    assert "LOW_COVERAGE" in flagged["flags"]
    rows[-1]["availability_status"] = "STALE"
    assert signal_for(module, variable_id)(rows, horizon)["status"] == "INCOMPLETE"
    rows[-1]["availability_status"] = "BLOCKED"
    assert signal_for(module, variable_id)(rows, horizon)["status"] == "INCOMPLETE"
    rows[0]["availability_status"] = "BLOCKED"
    rows[-1]["availability_status"] = "AVAILABLE"
    blocked_prior = signal_for(module, variable_id)(rows, horizon)
    assert blocked_prior["reason"] == "prior record is BLOCKED"
    assert blocked_prior["prior"]["timestamp"] == rows[0]["observation_timestamp"]
    rows[0]["availability_status"] = "STALE"
    stale_prior = signal_for(module, variable_id)(rows, horizon)
    assert stale_prior["reason"] == "prior record is STALE"
    assert stale_prior["prior"]["timestamp"] == rows[0]["observation_timestamp"]


@pytest.mark.parametrize("module,variable_id,filename,horizon,offset,not_applicable", MODULES)
def test_missing_insufficient_and_non_applicable_inputs(module, variable_id, filename, horizon, offset, not_applicable):
    assert signal_for(module, variable_id)([], horizon)["status"] == "INCOMPLETE"
    rows = [record(variable_id, i + 1, 3.0) for i in range(offset)]
    assert signal_for(module, variable_id)(rows, horizon)["status"] == "INCOMPLETE"
    malformed = [record(variable_id, i + 1, 3.0) for i in range(offset + 1)]
    del malformed[-1]["source_reference"]
    assert signal_for(module, variable_id)(malformed, horizon)["status"] == "INCOMPLETE"
    assert signal_for(module, variable_id)([], not_applicable)["status"] == "NOT_APPLICABLE"
