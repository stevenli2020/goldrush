import csv
import importlib.util
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[3]
MODULE_DIR = ROOT / "docs/phase4-scoring"
sys.path.insert(0, str(MODULE_DIR))
HORIZONS = ("1-5 days", "1-3 months", "1-3 years", "3-10 years")


def load(name):
    spec = importlib.util.spec_from_file_location(name, MODULE_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


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


@pytest.mark.parametrize(
    "module_name,variable_id,unit,value,context_key",
    [
        ("l0_002_status", "L0-002", "metric_tonnes", 8133.461672731797, "panel_context"),
        ("l9_004_status", "L9-004", "metric_tonnes", 50.25048632, "component_panel_context"),
        ("l6_002_status", "L6-002", "sovereign_asset_freeze_score_0_to_100", 0.0, "event_context"),
    ],
)
def test_status_only_final_methods_are_not_numeric(module_name, variable_id, unit, value, context_key):
    module = load(module_name)
    method = getattr(module, f"status_only_{variable_id.lower().replace('-', '_')}")
    context = {"scoring_status": "REVERSED", "action_state": "REVERSED"} if variable_id == "L6-002" else []
    for horizon in HORIZONS:
        result = method(record(variable_id, unit, value), horizon, context)
        assert result["status"] == "NOT_APPLICABLE"
        assert result["signal"] is None
        assert result["trace_context"]["history_used"] is False
    if variable_id == "L6-002":
        assert result[context_key] == [context]


@pytest.mark.parametrize(
    "module_name,variable_id,unit,value",
    [
        ("l0_002_status", "L0-002", "metric_tonnes", 1.0),
        ("l9_004_status", "L9-004", "metric_tonnes", 1.0),
        ("l6_002_status", "L6-002", "sovereign_asset_freeze_score_0_to_100", 0.0),
    ],
)
@pytest.mark.parametrize("status", ["STALE", "BLOCKED"])
def test_final_status_only_methods_reject_ineligible_current_records(module_name, variable_id, unit, value, status):
    method = getattr(load(module_name), f"status_only_{variable_id.lower().replace('-', '_')}")
    result = method(record(variable_id, unit, value, status=status), "1-3 months")
    assert result["status"] == "INCOMPLETE"
    assert result["reason"] == f"current record is {status}"


@pytest.mark.parametrize("module_name,variable_id,unit,value", [
    ("l0_002_status", "L0-002", "metric_tonnes", 1.0),
    ("l9_004_status", "L9-004", "metric_tonnes", 1.0),
    ("l6_002_status", "L6-002", "sovereign_asset_freeze_score_0_to_100", 0.0),
])
def test_final_status_only_methods_reject_invalid_records(module_name, variable_id, unit, value):
    method = getattr(load(module_name), f"status_only_{variable_id.lower().replace('-', '_')}")
    result = method({**record(variable_id, unit, value), "unit_or_scale": "wrong"}, "1-3 years")
    assert result["status"] == "INCOMPLETE"
    assert result["signal"] is None


def test_l0_002_reader_preserves_country_panel_without_aggregation(tmp_path):
    path = tmp_path / "panel.csv"
    fields = ["variable_id", "country", "holdings_tonnes", "unit", "source_publication_date", "source_file", "availability_status"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([
            {"variable_id": "L0-002", "country": "A", "holdings_tonnes": "1", "unit": "metric_tonnes", "source_publication_date": "2026-08-20", "source_file": "source.xlsx", "availability_status": "AVAILABLE"},
            {"variable_id": "L0-002", "country": "B", "holdings_tonnes": "2", "unit": "metric_tonnes", "source_publication_date": "2026-08-20", "source_file": "source.xlsx", "availability_status": "AVAILABLE"},
        ])
    rows = load("l0_002_status").read_l0_002(path)
    assert [row["country"] for row in rows] == ["A", "B"]
    result = load("l0_002_status").status_only_l0_002(
        record("L0-002", "metric_tonnes", 1.0), "1-3 years", rows
    )
    assert result["panel_context"] == rows
    assert "aggregate" not in result["trace_context"]


def test_l9_004_reader_keeps_same_date_components_separate(tmp_path):
    path = tmp_path / "panel.json"
    rows = [record("L9-004", "metric_tonnes", 1.0), record("L9-004", "metric_tonnes", 2.0)]
    path.write_text(json.dumps(rows), encoding="utf-8")
    assert [row["value"] for row in load("l9_004_status").read_l9_004(path)] == [1.0, 2.0]


@pytest.mark.parametrize("score,expected", [(49.9, 1), (50.0, 0), (50.1, -1)])
def test_l3_006_midpoint_mapping_and_flag_retention(score, expected):
    module = load("l3_006_signal")
    result = module.signal_l3_006(record("L3-006", "hawkishness_score_0_to_100", score), "1-5 days")
    assert result["signal"] == expected
    assert result["status"] == "AVAILABLE"
    flagged = module.signal_l3_006(record("L3-006", "hawkishness_score_0_to_100", 63.4, "FLAG", "LOW_COVERAGE"), "1-3 months")
    assert flagged["status"] == "FLAGGED"
    assert flagged["flags"] == ["LOW_COVERAGE", "FLAG"]
    assert flagged["reason"] == "LOW_COVERAGE"


def test_l3_006_invalid_and_long_horizons_are_explicit():
    module = load("l3_006_signal")
    assert module.signal_l3_006(record("L3-006", "hawkishness_score_0_to_100", 101), "1-5 days")["status"] == "INCOMPLETE"
    for horizon in ("1-3 years", "3-10 years"):
        assert module.signal_l3_006(record("L3-006", "hawkishness_score_0_to_100", 50), horizon)["status"] == "NOT_APPLICABLE"


@pytest.mark.parametrize("score,expected", [(0.2, 1), (0.0, 0), (-0.2, -1)])
def test_l6_001_sign_mapping_without_scorer_recalculation(score, expected):
    module = load("l6_001_signal")
    result = module.signal_l6_001(record("L6-001", "standard_deviation_units_clamped_-1_to_1", score), "1-5 days")
    assert result["signal"] == expected
    assert result["trace_context"]["source_score"] == score
    assert result["trace_context"]["history_used"] is False


def test_l6_001_long_horizons_and_stale_current_are_explicit():
    module = load("l6_001_signal")
    current = record("L6-001", "standard_deviation_units_clamped_-1_to_1", -0.2)
    for horizon in ("1-3 years", "3-10 years"):
        assert module.signal_l6_001(current, horizon)["status"] == "NOT_APPLICABLE"
    stale = module.signal_l6_001({**current, "availability_status": "STALE"}, "1-3 months")
    assert stale["status"] == "INCOMPLETE"
    assert stale["reason"] == "current record is STALE"


def test_real_preserved_panels_and_canonical_adapters_are_usable_without_scorer_changes():
    canonical = {
        row["variable_id"]: row
        for row in (
            json.loads(line)
            for line in (ROOT / "docs/phase3-ai-evidence/closure/canonical_dataset.jsonl").read_text(encoding="utf-8").splitlines()
        )
    }
    l0_context = load("l0_002_status").read_l0_002(
        ROOT / "docs/phase2-ingestion/L0/002/processed/L0_002_observations.csv"
    )
    assert len(l0_context) == 52
    assert l0_context[0]["country"] == "United States"
    l9_context = load("l9_004_status").read_l9_004(
        ROOT / "docs/phase3-ai-evidence/L9/004/data/l9_004_phase3_handoff.json"
    )
    assert len(l9_context) == 308
    assert load("l0_002_status").status_only_l0_002(canonical["L0-002"], "1-3 years", l0_context)["status"] == "NOT_APPLICABLE"
    assert load("l9_004_status").status_only_l9_004(canonical["L9-004"], "1-3 months", l9_context)["status"] == "NOT_APPLICABLE"
    assert load("l3_006_signal").signal_l3_006(canonical["L3-006"], "1-5 days")["status"] == "FLAGGED"
    assert load("l6_001_signal").signal_l6_001(canonical["L6-001"], "1-3 months")["signal"] == -1
    assert load("l6_002_status").status_only_l6_002(canonical["L6-002"], "1-3 years")["status"] == "NOT_APPLICABLE"
