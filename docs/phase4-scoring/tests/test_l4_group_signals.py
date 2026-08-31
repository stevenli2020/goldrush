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


CASES = [
    ("l4_001_signal", "L4-001", "index", "1-3 months", 1, "1-5 days"),
    ("l4_002_signal", "L4-002", "index", "1-3 years", 12, "3-10 years"),
    ("l4_003_signal", "L4-003", "percent", "1-3 months", 63, "1-5 days"),
    ("l4_004_signal", "L4-004", "percent", "3-10 years", 756, "1-3 months"),
    ("l4_006_signal", "L4-006", "percent_of_gdp", "1-3 years", 3, "1-5 days"),
    ("l4_007_signal", "L4-007", "percent_of_gdp", "3-10 years", 40, "1-3 months"),
    ("l4_008_signal", "L4-008", "percent_of_federal_receipts", "3-10 years", 10, "1-5 days"),
    ("l4_009_signal", "L4-009", "percent_of_marketable_treasury_debt", "1-3 years", 12, "1-5 days"),
]
MODULES = [(load(name), variable_id, unit, horizon, offset, not_applicable) for name, variable_id, unit, horizon, offset, not_applicable in CASES]


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
        "source_reference": "fixture:layer4",
        "quality_flag": quality,
    }


def handoff_path(variable_id: str) -> Path:
    return ROOT / f"docs/phase3-ai-evidence/L4/{variable_id[-3:]}/data/{variable_id.lower().replace('-', '_')}_phase3_handoff.json"


@pytest.mark.parametrize("module,variable_id,unit,horizon,offset,not_applicable", MODULES)
def test_readers_load_preserved_series_and_sort(module, variable_id, unit, horizon, offset, not_applicable):
    rows = reader_for(module, variable_id)(handoff_path(variable_id))
    assert rows == sorted(rows, key=lambda row: row["observation_timestamp"])
    assert len(rows) > offset if variable_id != "L4-009" else len(rows) == 24
    assert all(row["variable_id"] == variable_id and row["unit_or_scale"] == unit for row in rows)


@pytest.mark.parametrize("module,variable_id,unit,horizon,offset,not_applicable", MODULES)
def test_readers_reject_invalid_contract(module, variable_id, unit, horizon, offset, not_applicable, tmp_path):
    path = tmp_path / "rows.json"
    row = record(variable_id, unit, 1, 2.0)
    for invalid, message in [
        ({**row, "variable_id": "OTHER"}, "non-"),
        ({**row, "unit_or_scale": "basis_points"}, "unit_or_scale"),
        ({**row, "observation_timestamp": "bad"}, "timestamp"),
        ({**row, "value": "NaN"}, "finite"),
        ({**row, "source_reference": ""}, "source_reference"),
        ({**row, "availability_status": "UNKNOWN"}, "availability_status"),
    ]:
        path.write_text(json.dumps([invalid]), encoding="utf-8")
        with pytest.raises(ValueError, match=message):
            reader_for(module, variable_id)(path)
    path.write_text(json.dumps([row, row]), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate"):
        reader_for(module, variable_id)(path)


@pytest.mark.parametrize("module,variable_id,unit,horizon,offset,not_applicable", MODULES)
def test_signals_use_exact_offsets_and_trace(module, variable_id, unit, horizon, offset, not_applicable):
    rows = [record(variable_id, unit, i + 1, 3.0) for i in range(offset + 1)]
    rows[0]["value"] = 3.1
    rows[-1]["value"] = 2.9
    result = signal_for(module, variable_id)(rows, horizon)
    expected = 1 if variable_id == "L4-006" else -1
    assert result["status"] == "AVAILABLE"
    assert result["signal"] == expected
    assert result["prior"]["offset_positions"] == offset
    assert result["delta_percentage_points"] == pytest.approx(-0.2)
    assert {"variable_id", "horizon", "current", "prior", "delta_percentage_points", "direction_mapping", "source_references", "flags", "trace_context"} <= result.keys()
    assert result["current"]["timestamp"] and result["prior"]["timestamp"]
    assert result["trace_context"]["direction_condition"] == "registry direction is Conditional"


@pytest.mark.parametrize("module,variable_id,unit,horizon,offset,not_applicable", MODULES)
def test_signals_map_rising_falling_and_unchanged(module, variable_id, unit, horizon, offset, not_applicable):
    rows = [record(variable_id, unit, i + 1, 3.0) for i in range(offset + 1)]
    signal = signal_for(module, variable_id)
    assert signal(rows, horizon)["signal"] == 0
    rows[-1]["value"] = 3.2
    assert signal(rows, horizon)["signal"] == (1 if variable_id != "L4-006" else -1)
    rows[-1]["value"] = 2.8
    assert signal(rows, horizon)["signal"] == (-1 if variable_id != "L4-006" else 1)


def test_l4_006_deficit_inversion_is_explicit():
    module = load("l4_006_signal")
    rows = [record("L4-006", "percent_of_gdp", i + 1, -3.0) for i in range(4)]
    rows[-1]["value"] = -5.0
    result = module.signed_change_l4_006(rows, "1-3 years")
    assert result["signal"] == 1
    assert "more negative deficit" in result["direction_mapping"]


@pytest.mark.parametrize("module,variable_id,unit,horizon,offset,not_applicable", MODULES)
def test_statuses_and_flag_propagate(module, variable_id, unit, horizon, offset, not_applicable):
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


@pytest.mark.parametrize("module,variable_id,unit,horizon,offset,not_applicable", MODULES)
def test_missing_insufficient_and_not_applicable_are_explicit(module, variable_id, unit, horizon, offset, not_applicable):
    signal = signal_for(module, variable_id)
    assert signal([], horizon)["status"] == "INCOMPLETE"
    rows = [record(variable_id, unit, i + 1, 3.0) for i in range(offset)]
    assert signal(rows, horizon)["status"] == "INCOMPLETE"
    malformed = [record(variable_id, unit, i + 1, 3.0) for i in range(offset + 1)]
    del malformed[-1]["source_reference"]
    assert signal(malformed, horizon)["status"] == "INCOMPLETE"
    assert signal([], not_applicable)["status"] == "NOT_APPLICABLE"


def test_l4_008_offset_10_is_count_sufficient_and_fragile():
    module = load("l4_008_signal")
    rows = [record("L4-008", "percent_of_federal_receipts", i + 1, 10.0) for i in range(11)]
    rows[-1]["value"] = 12.0
    assert module.signed_change_l4_008(rows, "3-10 years")["signal"] == 1
    rows.pop(0)
    assert module.signed_change_l4_008(rows, "3-10 years")["status"] == "INCOMPLETE"


def test_l4_009_long_horizon_is_incomplete_with_24_rows():
    module = load("l4_009_signal")
    rows = [record("L4-009", "percent_of_marketable_treasury_debt", i + 1, 10.0) for i in range(24)]
    result = module.signed_change_l4_009(rows, "3-10 years")
    assert result["status"] == "INCOMPLETE"
    assert result["reason"] == "insufficient permitted history"


def test_registry_applicability_for_daily_l4_variables_is_reflected():
    assert load("l4_003_signal").OFFSETS == {"1-3 months": 63, "1-3 years": 252}
    assert load("l4_004_signal").OFFSETS == {"1-3 years": 252, "3-10 years": 756}


@pytest.mark.parametrize(
    "module_name,expected_not_applicable",
    [
        ("l4_001_signal", {"1-5 days", "3-10 years"}),
        ("l4_002_signal", {"1-5 days", "3-10 years"}),
        ("l4_003_signal", {"1-5 days", "3-10 years"}),
        ("l4_004_signal", {"1-5 days", "1-3 months"}),
        ("l4_006_signal", {"1-5 days", "1-3 months"}),
        ("l4_007_signal", {"1-5 days", "1-3 months"}),
        ("l4_008_signal", {"1-5 days", "1-3 months"}),
        ("l4_009_signal", {"1-5 days"}),
    ],
)
def test_all_non_applicable_horizons_are_explicit(module_name, expected_not_applicable):
    module = load(module_name)
    variable_id = module.VARIABLE_ID
    unit = module.UNIT
    for horizon in expected_not_applicable:
        result = getattr(module, f"signed_change_{variable_id.lower().replace('-', '_')}")([], horizon)
        assert result["status"] == "NOT_APPLICABLE"
