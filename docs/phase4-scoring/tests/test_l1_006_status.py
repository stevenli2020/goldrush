import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[3]
MODULE_PATH = ROOT / "docs/phase4-scoring/l1_006_status.py"
spec = importlib.util.spec_from_file_location("l1_006_status", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


def record(status="AVAILABLE", value=3.63, quality="OK"):
    return {
        "variable_id": "L1-006",
        "observation_timestamp": "2026-08-30T00:00:00Z",
        "value": value,
        "unit_or_scale": "percent_per_annum",
        "availability_status": status,
        "source_reference": "fixture:CME-Section10",
        "quality_flag": quality,
    }


def test_reader_accepts_exactly_one_scalar_and_rejects_wrong_shapes_and_fields(tmp_path):
    path = tmp_path / "l1_006.json"
    path.write_text(json.dumps([record()]), encoding="utf-8")
    assert module.read_l1_006(path)["value"] == 3.63
    path.write_text(json.dumps(record()), encoding="utf-8")
    assert module.read_l1_006(path)["variable_id"] == "L1-006"
    for payload, message in (
        ([record(), record()], "exactly one"),
        ({**record(), "unit_or_scale": "percent"}, "unit_or_scale"),
        ({**record(), "variable_id": "L1-001"}, "variable_id"),
        ({key: value for key, value in record().items() if key != "source_reference"}, "source_reference"),
    ):
        path.write_text(json.dumps(payload), encoding="utf-8")
        with pytest.raises(ValueError, match=message):
            module.read_l1_006(path)


@pytest.mark.parametrize("horizon", module.HORIZONS)
def test_available_scalar_is_not_applicable_with_raw_context(horizon):
    result = module.status_only_method(record(), horizon)
    assert result["status"] == "NOT_APPLICABLE"
    assert result["method_state"] == "NOT_APPLICABLE"
    assert result["signal"] is None
    assert result["current"] == {
        "observation_timestamp": "2026-08-30T00:00:00Z",
        "value": 3.63,
        "unit_or_scale": "percent_per_annum",
        "source_reference": "fixture:CME-Section10",
        "availability_status": "AVAILABLE",
    }


def test_flagged_scalar_is_not_applicable_and_retains_flag():
    result = module.status_only_method(record("FLAG", quality="REVIEW_REQUIRED"), "1-3 months")
    assert result["status"] == "NOT_APPLICABLE"
    assert result["signal"] is None
    assert result["flags"] == ["REVIEW_REQUIRED"]


@pytest.mark.parametrize("status", ["STALE", "BLOCKED"])
def test_stale_and_blocked_are_incomplete(status):
    result = module.status_only_method(record(status), "1-3 years")
    assert result["status"] == "INCOMPLETE"
    assert result["signal"] is None
    assert status in result["reason"]


@pytest.mark.parametrize(
    "bad_record,reason",
    [
        ({}, "missing canonical fields"),
        ({**record(), "observation_timestamp": "not-a-date"}, "invalid observation_timestamp"),
        ({**record(), "value": float("nan")}, "finite"),
        ({**record(), "unit_or_scale": "percent"}, "unit_or_scale"),
        ({**record(), "value": "not-a-number"}, "numeric"),
    ],
)
def test_malformed_nonfinite_and_wrong_unit_inputs_are_incomplete(bad_record, reason):
    result = module.status_only_method(bad_record, "3-10 years")
    assert result["status"] == "INCOMPLETE"
    assert result["signal"] is None
    assert reason in result["reason"]


def test_trace_contains_required_fields_and_no_numeric_method_state():
    result = module.status_only_method(record("FLAG", quality="LOW_COVERAGE"), "1-5 days")
    assert set(result) >= {
        "horizon",
        "current",
        "source_references",
        "status",
        "method_state",
        "flags",
    }
    assert result["current"]["observation_timestamp"]
    assert result["current"]["value"] == 3.63
    assert result["current"]["unit_or_scale"] == "percent_per_annum"
    assert result["current"]["source_reference"] == "fixture:CME-Section10"
    assert result["current"]["availability_status"] == "FLAG"
    assert result["flags"] == ["LOW_COVERAGE"]
    assert result["signal"] is None


def test_preserved_canonical_record_is_readable():
    path = ROOT / "docs/phase3-ai-evidence/closure/canonical_dataset.jsonl"
    line = next(line for line in path.read_text(encoding="utf-8").splitlines() if '"variable_id":"L1-006"' in line)
    row = json.loads(line)
    assert module.status_only_method(row, "1-3 months")["status"] == "NOT_APPLICABLE"
