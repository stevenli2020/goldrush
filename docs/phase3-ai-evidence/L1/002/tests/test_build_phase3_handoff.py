import importlib.util
from pathlib import Path
import pytest

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_phase3_handoff.py"
spec = importlib.util.spec_from_file_location("l1_002_handoff", MODULE_PATH)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

def test_builds_five_year_tips_handoff():
    row = {"variable_id": "L1-002", "observation_date": "2026-08-27", "value": "2.04", "unit": "percent", "validation_status": "PASS", "availability_status": "AVAILABLE"}
    result = module.build_handoff([row], "fred.json")
    assert result[0]["value"] == 2.04 and result[0]["unit_or_scale"] == "percent"

def test_rejects_blocked_input(tmp_path):
    path = tmp_path / "input.csv"
    path.write_text("variable_id,observation_date,value,unit,validation_status,availability_status\nL1-002,2026-08-27,2.04,percent,PASS,BLOCKED\n", encoding="utf-8")
    with pytest.raises(ValueError): module.load_rows(path)
