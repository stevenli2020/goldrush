import importlib.util
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[3]
MODULE_DIR = ROOT / "docs/phase4-scoring"
sys.path.insert(0, str(MODULE_DIR))


def load(name):
    spec = importlib.util.spec_from_file_location(name, MODULE_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


SIGNALS = [
    (load("l5_001_signal"), "L5-001", "metric_tonnes", "1-3 months", 1),
    (load("l5_003_signal"), "L5-003", "percentage_points_qoq", "1-3 years", 12),
    (load("l7_003_signal"), "L7-003", "percent_yoy", "1-3 years", 12),
    (load("l7_004_signal"), "L7-004", "percentage_points", "1-5 days", 5),
    (load("l7_005_signal"), "L7-005", "basis_points", "1-5 days", 5),
    (load("l9_001_signal"), "L9-001", "usd_per_troy_ounce", "1-5 days", 5),
]


def record(variable_id, unit, index, value, status="AVAILABLE", quality="OK"):
    return {
        "variable_id": variable_id,
        "observation_timestamp": (datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(days=index - 1)).isoformat().replace("+00:00", "Z"),
        "value": value,
        "unit_or_scale": unit,
        "availability_status": status,
        "source_reference": "fixture:phase4-l579",
        "quality_flag": quality,
    }


def reader_for(module, variable_id):
    return getattr(module, f"read_{variable_id.lower().replace('-', '_')}")


def signal_for(module, variable_id):
    return getattr(module, f"signed_change_{variable_id.lower().replace('-', '_')}")


def handoff_path(variable_id):
    return ROOT / f"docs/phase3-ai-evidence/{variable_id[:2]}/{variable_id[-3:]}/data/{variable_id.lower().replace('-', '_')}_phase3_handoff.json"


@pytest.mark.parametrize("module,variable_id,unit,horizon,offset", SIGNALS)
def test_reader_contract_and_preserved_counts(module, variable_id, unit, horizon, offset):
    path = handoff_path(variable_id)
    if variable_id in {"L5-003", "L7-003"}:
        with pytest.raises(ValueError):
            reader_for(module, variable_id)(path)
        return
    rows = reader_for(module, variable_id)(path)
    expected = {"L5-001": 294, "L7-004": 787, "L7-005": 2099, "L9-001": 6088}[variable_id]
    assert len(rows) == expected
    assert rows == sorted(rows, key=lambda row: row["observation_timestamp"])
    assert all(row["unit_or_scale"] == unit for row in rows)


@pytest.mark.parametrize("module,variable_id,unit,horizon,offset", SIGNALS)
def test_signed_change_offsets_direction_and_trace(module, variable_id, unit, horizon, offset):
    rows = [record(variable_id, unit, i + 1, 3.0) for i in range(offset + 1)]
    rows[0]["value"], rows[-1]["value"] = 3.1, 2.9
    result = signal_for(module, variable_id)(rows, horizon)
    assert result["status"] == "AVAILABLE"
    expected = {"L5-001": -1, "L5-003": 1, "L7-003": 1, "L7-004": -1, "L7-005": -1, "L9-001": -1}
    assert result["signal"] == expected[variable_id]
    assert result["prior"]["offset_positions"] == offset
    assert result["delta_percentage_points"] == pytest.approx(-0.2)
    assert {"variable_id", "horizon", "current", "prior", "direction_mapping", "source_references", "flags", "trace_context"} <= result.keys()


@pytest.mark.parametrize("module,variable_id,unit,horizon,offset", SIGNALS)
def test_status_propagation_and_not_applicable(module, variable_id, unit, horizon, offset):
    rows = [record(variable_id, unit, i + 1, 3.0) for i in range(offset + 1)]
    rows[-1]["availability_status"], rows[-1]["quality_flag"] = "FLAG", "CHECK"
    assert signal_for(module, variable_id)(rows, horizon)["status"] == "FLAGGED"
    rows[-1]["availability_status"] = "STALE"
    assert signal_for(module, variable_id)(rows, horizon)["status"] == "INCOMPLETE"
    rows[-1]["availability_status"] = "AVAILABLE"
    rows[0]["availability_status"] = "STALE"
    assert signal_for(module, variable_id)(rows, horizon)["reason"] == "prior record is STALE"
    rows[0]["availability_status"] = "BLOCKED"
    assert signal_for(module, variable_id)(rows, horizon)["reason"] == "prior record is BLOCKED"
    assert signal_for(module, variable_id)([], "1-5 days")["status"] == "NOT_APPLICABLE" if horizon != "1-5 days" else signal_for(module, variable_id)([], "3-10 years")["status"] == "NOT_APPLICABLE"


@pytest.mark.parametrize("module,variable_id,unit,horizon,offset", SIGNALS)
def test_reader_rejects_wrong_unit_malformed_nonfinite_and_duplicate(module, variable_id, unit, horizon, offset, tmp_path):
    valid = record(variable_id, unit, 1, 2.0)
    path = tmp_path / "rows.json"
    for row, message in [
        ({**valid, "unit_or_scale": "wrong"}, "unit_or_scale"),
        ({**valid, "observation_timestamp": "bad"}, "timestamp"),
        ({**valid, "value": "NaN"}, "finite"),
    ]:
        path.write_text(json.dumps([row]), encoding="utf-8")
        with pytest.raises(ValueError, match=message):
            reader_for(module, variable_id)(path)
    path.write_text(json.dumps([valid, valid]), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate"):
        reader_for(module, variable_id)(path)


def test_l7_001_status_only_all_horizons_and_raw_trace():
    module = load("l7_001_status")
    row = record("L7-001", "millions_usd", 1, 100.0)
    for horizon in module.HORIZONS:
        result = module.status_only_l7_001(row, horizon)
        assert result["status"] == "NOT_APPLICABLE"
        assert result["method_state"] == "NOT_APPLICABLE"
        assert result["signal"] is None
        assert result["current"]["value"] == 100.0
        assert result["trace_context"]["method"] == "status-only"
    row["availability_status"] = "STALE"
    assert module.status_only_l7_001(row, "1-3 years")["status"] == "INCOMPLETE"
    row["availability_status"] = "FLAG"
    assert module.status_only_method(row, "1-3 years")["status"] == "NOT_APPLICABLE"


def test_prederived_measures_and_premium_direction():
    for name, variable_id, unit, horizon, offset in [
        ("l5_003_signal", "L5-003", "percentage_points_qoq", "1-3 years", 12),
        ("l7_003_signal", "L7-003", "percent_yoy", "1-3 years", 12),
    ]:
        module = load(name)
        rows = [record(variable_id, unit, i + 1, 1.0) for i in range(offset + 1)]
        rows[-1]["value"] = 0.5
        assert signal_for(module, variable_id)(rows, horizon)["signal"] == 1
        assert signal_for(module, variable_id)(rows, horizon)["trace_context"]["pre_derived_measure"] in {"QoQ; no recomputation", "YoY; no recomputation"}
    module = load("l9_001_signal")
    rows = [record("L9-001", "usd_per_troy_ounce", i + 1, 1.0) for i in range(6)]
    rows[-1]["value"] = 2.0
    assert module.signed_change_l9_001(rows, "1-5 days")["signal"] == 1
    rows[0]["availability_status"] = "STALE"
    assert module.signed_change_l9_001(rows, "1-5 days")["status"] == "INCOMPLETE"


def test_l7_001_reader_loads_preserved_history():
    module = load("l7_001_status")
    rows = module.read_l7_001(handoff_path("L7-001"))
    assert len(rows) == 1237
    assert rows[-1]["availability_status"] == "AVAILABLE"
