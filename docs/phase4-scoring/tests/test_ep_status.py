import importlib.util
import json
import sys
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
    ("l3_002_status", "L3-002", "percent_per_annum", "curve_context"),
    ("l3_004_status", "L3-004", "expected_target_change_bps", "event_distribution_context"),
    ("l3_005_status", "L3-005", "percent", "dot_plot_context"),
    ("l5_002_status", "L5-002", "fraction", "panel_context"),
    ("l5_006_status", "L5-006", "metric_tonnes", "panel_context"),
]
HORIZONS = ("1-5 days", "1-3 months", "1-3 years", "3-10 years")


def record(variable_id, unit, value=1.0, status="AVAILABLE", quality="OK"):
    return {
        "variable_id": variable_id,
        "observation_timestamp": "2026-08-31T00:00:00Z",
        "value": value,
        "unit_or_scale": unit,
        "availability_status": status,
        "source_reference": f"fixture:{variable_id}",
        "quality_flag": quality,
    }


def context_row(variable_id, unit, value=1.0, **extra):
    return {**record(variable_id, unit, value), **extra}


@pytest.mark.parametrize("module_name,variable_id,unit,context_key", CASES)
def test_reader_validates_each_preserved_structure(module_name, variable_id, unit, context_key, tmp_path):
    module = load(module_name)
    reader = getattr(module, f"read_{variable_id.lower().replace('-', '_')}")
    extra = {
        "L3-002": {"contract": "ZQQ26"},
        "L3-004": {"meeting_date": "2026-09-16"},
        "L3-005": {"projection_horizon": "2026", "participant_count": 1, "median_projected_rate": 3.8},
        "L5-002": {},
        "L5-006": {},
    }[variable_id]
    valid = context_row(variable_id, unit, **extra)
    path = tmp_path / "handoff.json"
    path.write_text(json.dumps([valid]), encoding="utf-8")
    assert reader(path)[0]["variable_id"] == variable_id
    duplicate_payloads = () if variable_id in {"L5-002", "L5-006"} else ([valid, valid],)
    for payload in ([], *duplicate_payloads, "bad"):
        path.write_text(json.dumps(payload), encoding="utf-8")
        with pytest.raises(ValueError):
            reader(path)
    path.write_text("{malformed", encoding="utf-8")
    with pytest.raises(ValueError, match="readable JSON"):
        reader(path)
    path.write_text(json.dumps([{**valid, "unit_or_scale": "wrong"}]), encoding="utf-8")
    with pytest.raises(ValueError, match="unit"):
        reader(path)


@pytest.mark.parametrize("module_name,variable_id,unit,context_key", CASES)
def test_available_trace_and_status(module_name, variable_id, unit, context_key):
    module = load(module_name)
    method = getattr(module, f"status_only_{variable_id.lower().replace('-', '_')}")
    current = record(variable_id, unit, 2.0)
    context = [context_row(variable_id, unit, 2.0)]
    for horizon in HORIZONS:
        result = method(current, horizon, context)
        assert result["signal"] is None
        assert result["current"]["value"] == 2.0
        assert result[context_key] == context
        assert result["source_references"] == [f"fixture:{variable_id}"]
        assert result["trace_context"]["history_used"] is False
        assert result["variable"] == variable_id


def test_status_matrix_for_each_variable():
    expectations = {
        "L3-002": {h: "NOT_APPLICABLE" for h in HORIZONS},
        "L3-004": {"1-5 days": "INCOMPLETE", "1-3 months": "INCOMPLETE", "1-3 years": "NOT_APPLICABLE", "3-10 years": "NOT_APPLICABLE"},
        "L3-005": {"1-5 days": "NOT_APPLICABLE", "1-3 months": "INCOMPLETE", "1-3 years": "INCOMPLETE", "3-10 years": "NOT_APPLICABLE"},
        "L5-002": {h: "NOT_APPLICABLE" for h in HORIZONS},
        "L5-006": {h: "NOT_APPLICABLE" for h in HORIZONS},
    }
    for module_name, variable_id, unit, _ in CASES:
        method = getattr(load(module_name), f"status_only_{variable_id.lower().replace('-', '_')}")
        current = record(variable_id, unit)
        for horizon, expected in expectations[variable_id].items():
            result = method(current, horizon, [context_row(variable_id, unit)])
            assert result["status"] == expected
            if expected == "INCOMPLETE":
                assert result["reason"] in {
                    "missing meeting/component selection metadata",
                    "missing projection-horizon/statistic selection metadata",
                }


@pytest.mark.parametrize("module_name,variable_id,unit,context_key", CASES)
def test_flag_visible_and_current_stale_blocked_incomplete(module_name, variable_id, unit, context_key):
    module = load(module_name)
    method = getattr(module, f"status_only_{variable_id.lower().replace('-', '_')}")
    flagged = method(record(variable_id, unit, status="FLAG", quality="REVIEW"), "1-3 months", [])
    assert flagged["flags"] == ["REVIEW", "FLAG"]
    for status in ("STALE", "BLOCKED"):
        result = method(record(variable_id, unit, status=status), "1-3 months", [])
        assert result["status"] == "INCOMPLETE"
        assert result["reason"] == f"current record is {status}"


@pytest.mark.parametrize("module_name,variable_id,unit,context_key", CASES)
def test_invalid_current_inputs_are_incomplete(module_name, variable_id, unit, context_key):
    module = load(module_name)
    method = getattr(module, f"status_only_{variable_id.lower().replace('-', '_')}")
    valid = record(variable_id, unit)
    for bad in (
        {**valid, "unit_or_scale": "wrong"},
        {**valid, "observation_timestamp": "bad"},
        {**valid, "value": "NaN"},
        {**valid, "availability_status": "UNKNOWN"},
        {key: value for key, value in valid.items() if key != "source_reference"},
        [valid],
    ):
        result = method(bad, "1-3 years", [])
        assert result["status"] == "INCOMPLETE"
        assert result["signal"] is None


def test_real_preserved_e_structures_load_and_p_structures_expose_legacy_timestamp_issue():
    for module_name, variable_id, expected_count in [
        ("l3_002_status", "L3-002", 19),
        ("l3_004_status", "L3-004", 8),
        ("l3_005_status", "L3-005", 26),
    ]:
        module = load(module_name)
        path = ROOT / f"docs/phase3-ai-evidence/{variable_id[:2]}/{variable_id[-3:]}/data/{variable_id.lower().replace('-', '_')}_phase3_handoff.json"
        if variable_id == "L3-004":
            path = ROOT / "docs/phase3-ai-evidence/L3/004/data/l3_004_phase4_handoff.json"
        rows = getattr(module, f"read_{variable_id.lower().replace('-', '_')}")(path)
        assert len(rows) == expected_count
    module = load("l5_002_status")
    path = ROOT / "docs/phase3-ai-evidence/L5/002/data/l5_002_phase3_handoff.json"
    with pytest.raises(ValueError, match="timestamp"):
        module.read_l5_002(path)
    module = load("l5_006_status")
    path = ROOT / "docs/phase3-ai-evidence/L5/006/data/l5_006_phase3_handoff.json"
    rows = module.read_l5_006(path)
    assert len(rows) == 2724
    assert sum(row["availability_status"] == "STALE" for row in rows) == 2719
