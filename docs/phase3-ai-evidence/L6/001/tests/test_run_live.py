import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "run_live.py"
spec = importlib.util.spec_from_file_location("l6_001_live", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def row(day: int, value: float, availability: str = "AVAILABLE") -> dict[str, str]:
    return {
        "observation_date": f"2026-08-{day:02d}",
        "gpr_act_index": str(value),
        "availability_status": availability,
        "manifest_path": "source.manifest.json",
        "validation_status": "PASS",
    }


def test_builds_available_phase4_handoff():
    rows = [row(day, 1.0) for day in range(1, 61)]
    handoff, state = module.build_handoff(rows, {"prev_score": None, "missing_days": 0}, "now")
    assert handoff["variable_id"] == "L6-001"
    assert handoff["value"] == 0.0
    assert handoff["availability_status"] == "AVAILABLE"
    assert state["prev_score"] == 0.0 and state["missing_days"] == 0


def test_stale_handoff_decays_persisted_score():
    rows = [row(day, 1.0) for day in range(1, 60)] + [row(60, 1.0, "STALE")]
    handoff, state = module.build_handoff(rows, {"prev_score": 0.8, "missing_days": 0}, "now")
    assert handoff["value"] == 0.76
    assert handoff["availability_status"] == "STALE"
    assert handoff["quality_flag"] == "MISSING_DECAY"
    assert state["missing_days"] == 1


def test_same_source_rows_and_state_replay_identically():
    rows = [row(day, 1.0) for day in range(1, 61)]
    state = {"prev_score": None, "missing_days": 0}
    first = module.build_handoff(rows, state, "now")
    second = module.build_handoff(rows, state, "now")
    assert first == second
