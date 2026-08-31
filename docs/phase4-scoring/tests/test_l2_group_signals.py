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
    (load("l2_001_signal"), "L2-001", "index", "1-5 days", 5, "3-10 years", "DXY"),
    (load("l2_002_signal"), "L2-002", "index_jan_2006_100_not_seasonally_adjusted", "3-10 years", 756, "none", "broad"),
    (load("l2_003_signal"), "L2-003", "cny_per_usd", "1-3 months", 63, "3-10 years", "CNY/USD"),
]


def reader_for(module, variable_id):
    return getattr(module, f"read_{variable_id.lower().replace('-', '_')}")


def signal_for(module, variable_id):
    return getattr(module, f"signed_change_{variable_id.lower().replace('-', '_')}")


def record(variable_id: str, unit: str, index: int, value: float, status: str = "AVAILABLE", quality: str = "OK"):
    timestamp = datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(days=index - 1)
    return {
        "variable_id": variable_id,
        "observation_timestamp": timestamp.isoformat().replace("+00:00", "Z"),
        "value": value,
        "unit_or_scale": unit,
        "availability_status": status,
        "source_reference": "fixture:layer2",
        "quality_flag": quality,
    }


@pytest.mark.parametrize("module,variable_id,unit,horizon,offset,not_applicable,label", MODULES)
def test_readers_load_preserved_series_and_sort(module, variable_id, unit, horizon, offset, not_applicable, label):
    path = ROOT / f"docs/phase3-ai-evidence/{variable_id[0:2]}/{variable_id[-3:]}/data/{variable_id.lower().replace('-', '_')}_phase3_handoff.json"
    rows = reader_for(module, variable_id)(path)
    assert rows == sorted(rows, key=lambda row: row["observation_timestamp"])
    assert len(rows) > offset
    assert all(row["variable_id"] == variable_id and row["unit_or_scale"] == unit for row in rows)


@pytest.mark.parametrize("module,variable_id,unit,horizon,offset,not_applicable,label", MODULES)
def test_readers_reject_invalid_contract(module, variable_id, unit, horizon, offset, not_applicable, label, tmp_path):
    path = tmp_path / "rows.json"
    row = record(variable_id, unit, 1, 2.0)
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


@pytest.mark.parametrize("module,variable_id,unit,horizon,offset,not_applicable,label", MODULES)
def test_signals_use_exact_offsets_and_emit_trace(module, variable_id, unit, horizon, offset, not_applicable, label):
    rows = [record(variable_id, unit, i + 1, 3.0) for i in range(offset + 1)]
    rows[0]["value"] = 3.1
    rows[-1]["value"] = 2.9
    result = signal_for(module, variable_id)(rows, horizon)
    expected = 1 if variable_id != "L2-003" else -1
    assert result["status"] == "AVAILABLE"
    assert result["signal"] == expected
    assert result["prior"]["offset_positions"] == offset
    assert result["delta_percentage_points"] == pytest.approx(-0.2)
    assert {"variable_id", "horizon", "current", "prior", "delta_percentage_points", "direction_mapping", "source_references", "flags", "trace_context"} <= result.keys()
    assert result["current"]["timestamp"] and result["prior"]["timestamp"]


@pytest.mark.parametrize("module,variable_id,unit,horizon,offset,not_applicable,label", MODULES)
def test_signals_map_all_three_directions(module, variable_id, unit, horizon, offset, not_applicable, label):
    rows = [record(variable_id, unit, i + 1, 3.0) for i in range(offset + 1)]
    assert signal_for(module, variable_id)(rows, horizon)["signal"] == 0
    rows[-1]["value"] = 3.2
    assert signal_for(module, variable_id)(rows, horizon)["signal"] == (-1 if variable_id != "L2-003" else 1)
    rows[-1]["value"] = 2.8
    assert signal_for(module, variable_id)(rows, horizon)["signal"] == (1 if variable_id != "L2-003" else -1)


@pytest.mark.parametrize("module,variable_id,unit,horizon,offset,not_applicable,label", MODULES)
def test_statuses_and_flag_propagate(module, variable_id, unit, horizon, offset, not_applicable, label):
    rows = [record(variable_id, unit, i + 1, 3.0) for i in range(offset + 1)]
    rows[0]["value"] = 3.1
    rows[-1] = record(variable_id, unit, offset + 1, 2.9, status="FLAG", quality="CHECK")
    flagged = signal_for(module, variable_id)(rows, horizon)
    assert flagged["status"] == "FLAGGED" and "CHECK" in flagged["flags"]
    rows[-1]["availability_status"] = "STALE"
    assert signal_for(module, variable_id)(rows, horizon)["status"] == "INCOMPLETE"
    rows[-1]["availability_status"] = "BLOCKED"
    assert signal_for(module, variable_id)(rows, horizon)["status"] == "INCOMPLETE"
    rows[-1]["availability_status"] = "AVAILABLE"
    rows[0]["availability_status"] = "STALE"
    assert signal_for(module, variable_id)(rows, horizon)["reason"] == "prior record is STALE"
    rows[0]["availability_status"] = "BLOCKED"
    assert signal_for(module, variable_id)(rows, horizon)["reason"] == "prior record is BLOCKED"


@pytest.mark.parametrize("module,variable_id,unit,horizon,offset,not_applicable,label", MODULES)
def test_missing_insufficient_and_non_applicable_are_explicit(module, variable_id, unit, horizon, offset, not_applicable, label):
    assert signal_for(module, variable_id)([], horizon)["status"] == "INCOMPLETE"
    rows = [record(variable_id, unit, i + 1, 3.0) for i in range(offset)]
    assert signal_for(module, variable_id)(rows, horizon)["status"] == "INCOMPLETE"
    malformed = [record(variable_id, unit, i + 1, 3.0) for i in range(offset + 1)]
    del malformed[-1]["source_reference"]
    assert signal_for(module, variable_id)(malformed, horizon)["status"] == "INCOMPLETE"
    assert signal_for(module, variable_id)([], not_applicable)["status"] == "NOT_APPLICABLE"


def test_l2_001_long_offsets_are_insufficient_history():
    module = MODULES[0][0]
    rows = [record("L2-001", "index", i + 1, 3.0) for i in range(19)]
    assert module.signed_change_l2_001(rows, "1-3 months")["status"] == "INCOMPLETE"
    assert module.signed_change_l2_001(rows, "1-3 years")["status"] == "INCOMPLETE"
    assert module.signed_change_l2_001(rows, "3-10 years")["status"] == "NOT_APPLICABLE"
