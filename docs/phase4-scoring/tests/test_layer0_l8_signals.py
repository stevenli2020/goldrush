import calendar
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
    (load("l0_001_signal"), "L0-001", "metric_tonnes", "1-3 years", 3),
    (load("l0_003_signal"), "L0-003", "metric_tonnes", "1-3 months", 1),
    (load("l0_005_signal"), "L0-005", "metric_tonnes", "1-3 years", 12),
    (load("l0_006_signal"), "L0-006", "metric_tonnes", "1-3 years", 12),
    (load("l8_001_signal"), "L8-001", "metric_tonnes", "1-3 months", 1),
]


def record(variable_id, unit, index, value, status="AVAILABLE", quality="OK", period_type=None):
    row = {
        "variable_id": variable_id,
        "observation_timestamp": (datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(days=index - 1)).isoformat().replace("+00:00", "Z"),
        "value": value,
        "unit_or_scale": unit,
        "availability_status": status,
        "source_reference": "fixture:layer0",
        "quality_flag": quality,
    }
    if period_type:
        row["observation_period_type"] = period_type
    return row


def reader_for(module, variable_id):
    return getattr(module, f"read_{variable_id.lower().replace('-', '_')}")


def signal_for(module, variable_id):
    return getattr(module, f"signed_change_{variable_id.lower().replace('-', '_')}")


def handoff_path(variable_id):
    return ROOT / f"docs/phase3-ai-evidence/{variable_id[0:2]}/{variable_id[-3:]}/data/{variable_id.lower().replace('-', '_')}_phase3_handoff.json"


@pytest.mark.parametrize("module,variable_id,unit,horizon,offset", MODULES)
def test_preserved_readers_load_expected_histories(module, variable_id, unit, horizon, offset):
    rows = reader_for(module, variable_id)(handoff_path(variable_id)) if variable_id != "L0-006" else reader_for(module, variable_id)(ROOT / "docs/phase2-ingestion/L0/006/processed/l0_006_gold_recycling_flow.json")
    expected_counts = {"L0-001": 16, "L0-003": 281, "L0-005": 82, "L0-006": 66, "L8-001": 281}
    assert len(rows) == expected_counts[variable_id]
    assert rows == sorted(rows, key=lambda row: row["observation_timestamp"])
    assert all(row["variable_id"] == variable_id and row["unit_or_scale"] == unit for row in rows)


def test_corrections_are_preserved_and_resolved():
    corrected = json.loads((ROOT / "docs/phase3-ai-evidence/L0/005/data/l0_005_phase3_handoff.json").read_text())
    superseded = json.loads((ROOT / "docs/phase3-ai-evidence/L0/005/data/l0_005_phase3_handoff.superseded-20260831.json").read_text())
    assert len(corrected) == len(superseded) == 82
    changes = []
    for old, new in zip(superseded, corrected):
        old_copy, new_copy = dict(old), dict(new)
        old_ts, new_ts = old_copy.pop("observation_timestamp"), new_copy.pop("observation_timestamp")
        assert old_copy == new_copy
        if old_ts != new_ts:
            changes.append((old_ts, new_ts))
    assert len(changes) == 16
    for row in corrected:
        year, month, day = map(int, row["observation_timestamp"][:10].split("-"))
        assert day <= calendar.monthrange(year, month)[1]

    source = ROOT / "docs/phase2-ingestion/L0/006/processed/l0_006_gold_recycling_flow.json"
    assert source.exists()
    register = json.loads((ROOT / "docs/phase3-ai-evidence/closure/variable_register.json").read_text())
    entry = next(row for row in register if row["variable_id"] == "L0-006")
    relative_source = "docs/phase2-ingestion/L0/006/processed/l0_006_gold_recycling_flow.json"
    assert entry["transformation_output"] == relative_source
    canonical = next(row for row in (ROOT / "docs/phase3-ai-evidence/closure/canonical_dataset.jsonl").read_text().splitlines() if '"variable_id":"L0-006"' in row)
    assert relative_source in canonical


@pytest.mark.parametrize("module,variable_id,unit,horizon,offset", MODULES)
def test_signals_use_exact_offsets_and_direction(module, variable_id, unit, horizon, offset):
    period_type = "quarterly" if variable_id in {"L0-005", "L0-006"} else None
    rows = [record(variable_id, unit, i + 1, 3.0, period_type=period_type) for i in range(offset + 1)]
    rows[0]["value"], rows[-1]["value"] = 3.1, 2.9
    result = signal_for(module, variable_id)(rows, horizon)
    expected = 1 if variable_id in {"L0-001", "L0-006"} else -1
    assert result["status"] == "AVAILABLE"
    assert result["signal"] == expected
    assert result["prior"]["offset_positions"] == offset
    assert result["delta_percentage_points"] == pytest.approx(-0.2)
    assert {"variable_id", "horizon", "current", "prior", "direction_mapping", "source_references", "trace_context"} <= result.keys()


@pytest.mark.parametrize("module,variable_id,unit,horizon,offset", MODULES)
def test_all_three_directions_and_status_rules(module, variable_id, unit, horizon, offset):
    period_type = "quarterly" if variable_id in {"L0-005", "L0-006"} else None
    rows = [record(variable_id, unit, i + 1, 3.0, period_type=period_type) for i in range(offset + 1)]
    signal = signal_for(module, variable_id)
    assert signal(rows, horizon)["signal"] == 0
    rows[-1]["value"] = 3.2
    assert signal(rows, horizon)["signal"] == (1 if variable_id not in {"L0-001", "L0-006"} else -1)
    rows[-1]["value"] = 2.8
    assert signal(rows, horizon)["signal"] == (1 if variable_id in {"L0-001", "L0-006"} else -1)
    rows[-1]["value"] = 2.9
    rows[-1]["availability_status"], rows[-1]["quality_flag"] = "FLAG", "CHECK"
    flagged = signal(rows, horizon)
    assert flagged["status"] == "FLAGGED" and "CHECK" in flagged["flags"]
    rows[-1]["availability_status"] = "STALE"
    assert signal(rows, horizon)["status"] == "INCOMPLETE"
    rows[-1]["availability_status"] = "AVAILABLE"
    rows[0]["availability_status"] = "STALE"
    assert signal(rows, horizon)["reason"] == "prior record is STALE"
    rows[0]["availability_status"] = "BLOCKED"
    assert signal(rows, horizon)["reason"] == "prior record is BLOCKED"


@pytest.mark.parametrize("module,variable_id,unit,horizon,offset", MODULES)
def test_missing_insufficient_and_not_applicable_are_explicit(module, variable_id, unit, horizon, offset):
    signal = signal_for(module, variable_id)
    assert signal([], horizon)["status"] == "INCOMPLETE"
    period_type = "quarterly" if variable_id in {"L0-005", "L0-006"} else None
    rows = [record(variable_id, unit, i + 1, 3.0, period_type=period_type) for i in range(offset)]
    assert signal(rows, horizon)["status"] == "INCOMPLETE"
    invalid = record(variable_id, "wrong", 1, 3.0, period_type=period_type)
    path = ROOT / "docs/phase4-scoring/tests/.tmp_layer0_invalid.json"
    try:
        path.write_text(json.dumps([invalid]), encoding="utf-8")
        with pytest.raises(ValueError):
            reader_for(module, variable_id)(path)
    finally:
        path.unlink(missing_ok=True)
    assert signal([], "1-5 days")["status"] == "NOT_APPLICABLE" if variable_id != "L0-003" else signal([], "3-10 years")["status"] == "NOT_APPLICABLE"


def test_l0_005_matches_period_type_and_uses_annual_offset():
    module = load("l0_005_signal")
    rows = [record("L0-005", "metric_tonnes", i + 1, 10.0, period_type="annual") for i in range(4)]
    rows[-1]["value"] = 12.0
    result = module.signed_change_l0_005(rows, "1-3 years")
    assert result["signal"] == 1 and result["prior"]["offset_positions"] == 3
    quarterly = [record("L0-005", "metric_tonnes", i + 1, 10.0, period_type="quarterly") for i in range(13)]
    quarterly[-1]["value"] = 12.0
    result = module.signed_change_l0_005(quarterly, "1-3 years")
    assert result["signal"] == 1 and result["prior"]["offset_positions"] == 12


def test_l8_corrected_value_and_source():
    module = load("l8_001_signal")
    rows = module.read_l8_001(handoff_path("L8-001"))
    assert rows[-1]["value"] == pytest.approx(23.46395211)
    assert "Demand by month" in rows[-1]["source_reference"]
