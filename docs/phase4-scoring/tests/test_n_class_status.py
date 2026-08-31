import importlib.util
import json
import sys
from datetime import datetime, timezone
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


CASES = [
    ("l0_009_status", "L0-009", "percent_per_annum", 1.1349607944426228),
    ("l3_001_status", "L3-001", "percent_per_annum", 3.8954166666666663),
    ("l3_003_status", "L3-003", "percent_per_annum", 4.23),
    ("l10_001_status", "L10-001", "contracts", 144747),
    ("l10_002_status", "L10-002", "contracts", 423793.0),
]
HORIZONS = ("1-5 days", "1-3 months", "1-3 years", "3-10 years")


def record(variable_id, unit, value, status="AVAILABLE", quality="OK"):
    return {
        "variable_id": variable_id,
        "observation_timestamp": "2026-08-31T00:00:00Z",
        "value": value,
        "unit_or_scale": unit,
        "availability_status": status,
        "source_reference": f"fixture:{variable_id}",
        "quality_flag": quality,
    }


@pytest.mark.parametrize("module_name,variable_id,unit,value", CASES)
def test_reader_accepts_exactly_one_scalar_and_rejects_zero_multiple_or_malformed(module_name, variable_id, unit, value, tmp_path):
    module = load(module_name)
    reader = getattr(module, f"read_{variable_id.lower().replace('-', '_')}")
    valid = record(variable_id, unit, value)
    path = tmp_path / "handoff.json"
    path.write_text(json.dumps([valid]), encoding="utf-8")
    assert reader(path) == valid
    for payload in ([], [valid, valid], "bad"):
        path.write_text(json.dumps(payload), encoding="utf-8")
        with pytest.raises(ValueError):
            reader(path)
    path.write_text("{malformed", encoding="utf-8")
    with pytest.raises(ValueError, match="readable JSON"):
        reader(path)


@pytest.mark.parametrize("module_name,variable_id,unit,value", CASES)
def test_available_returns_not_applicable_all_horizons_with_complete_trace(module_name, variable_id, unit, value):
    module = load(module_name)
    method = getattr(module, f"status_only_{variable_id.lower().replace('-', '_')}")
    row = record(variable_id, unit, value)
    for horizon in HORIZONS:
        result = method(row, horizon)
        assert result["status"] == "NOT_APPLICABLE"
        assert result["method_state"] == "NOT_APPLICABLE"
        assert result["signal"] is None
        assert result["variable"] == variable_id
        assert result["current"]["value"] == value
        assert result["current"]["source_reference"] == row["source_reference"]
        assert result["source_references"] == [row["source_reference"]]
        assert result["trace_context"]["history_class"] == "N"
        assert result["trace_context"]["history_used"] is False
        assert "offset" not in result["trace_context"]


@pytest.mark.parametrize("module_name,variable_id,unit,value", CASES)
def test_flag_is_visible_but_still_not_applicable(module_name, variable_id, unit, value):
    module = load(module_name)
    method = getattr(module, f"status_only_{variable_id.lower().replace('-', '_')}")
    result = method(record(variable_id, unit, value, "FLAG", "REVIEW_REQUIRED"), "1-3 months")
    assert result["status"] == "NOT_APPLICABLE"
    assert result["flags"] == ["REVIEW_REQUIRED"]
    assert result["current"]["availability_status"] == "FLAG"


@pytest.mark.parametrize("module_name,variable_id,unit,value", CASES)
@pytest.mark.parametrize("bad_status", ["STALE", "BLOCKED"])
def test_stale_and_blocked_are_incomplete(module_name, variable_id, unit, value, bad_status):
    module = load(module_name)
    method = getattr(module, f"status_only_{variable_id.lower().replace('-', '_')}")
    result = method(record(variable_id, unit, value, bad_status), "1-5 days")
    assert result["status"] == "INCOMPLETE"
    assert result["reason"] == f"current record is {bad_status}"


@pytest.mark.parametrize("module_name,variable_id,unit,value", CASES)
def test_invalid_current_record_is_incomplete_without_fallback(module_name, variable_id, unit, value):
    module = load(module_name)
    method = getattr(module, f"status_only_{variable_id.lower().replace('-', '_')}")
    valid = record(variable_id, unit, value)
    for bad in (
        {**valid, "unit_or_scale": "wrong"},
        {**valid, "observation_timestamp": "bad"},
        {**valid, "value": "NaN"},
        {**valid, "availability_status": "UNKNOWN"},
        {key: val for key, val in valid.items() if key != "source_reference"},
        [valid],
    ):
        result = method(bad, "1-3 years")
        assert result["status"] == "INCOMPLETE"
        assert result["signal"] is None
        assert result["trace_context"]["history_used"] is False


def test_readers_match_preserved_canonical_scalar_values():
    canonical = {
        row["variable_id"]: row
        for row in (json.loads(line) for line in (ROOT / "docs/phase3-ai-evidence/closure/canonical_dataset.jsonl").read_text(encoding="utf-8").splitlines())
    }
    for module_name, variable_id, unit, value in CASES:
        module = load(module_name)
        reader = getattr(module, f"read_{variable_id.lower().replace('-', '_')}")
        row = canonical[variable_id]
        path = ROOT / "docs/phase4-scoring/tests" / f"_{variable_id.replace('-', '_')}.json"
        path.write_text(json.dumps([row]), encoding="utf-8")
        try:
            loaded = reader(path)
        finally:
            path.unlink()
        assert loaded["variable_id"] == variable_id
        assert loaded["unit_or_scale"] == unit
        assert float(loaded["value"]) == pytest.approx(value)
