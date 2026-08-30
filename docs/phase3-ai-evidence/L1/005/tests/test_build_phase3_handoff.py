import importlib.util
from pathlib import Path
import pytest

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_phase3_handoff.py"
spec = importlib.util.spec_from_file_location("l1_005_handoff", MODULE_PATH)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

def test_builds_term_premium_handoff():
    row = {"variable_id": "L1-005", "observation_date": "2026-08-21", "value": "0.8682", "unit": "percent", "validation_status": "PASS", "availability_status": "STALE"}
    result = module.build_handoff([row], "fred.json")
    assert result[0]["value"] == 0.8682 and result[0]["availability_status"] == "STALE"

def test_rejects_blocked_input(tmp_path):
    path = tmp_path / "input.csv"
    path.write_text("variable_id,observation_date,value,unit,validation_status,availability_status\nL1-005,2026-08-21,0.8682,percent,PASS,BLOCKED\n", encoding="utf-8")
    with pytest.raises(ValueError): module.load_rows(path)
