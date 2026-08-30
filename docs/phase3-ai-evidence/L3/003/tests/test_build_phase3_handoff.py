import importlib.util
from pathlib import Path
import pytest

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_phase3_handoff.py"
spec = importlib.util.spec_from_file_location("l3_003_handoff", MODULE_PATH)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

def test_builds_terminal_rate_handoff():
    row = {"variable_id": "L3-003", "observation_date": "2026-08-29", "expected_terminal_policy_rate_pct": "4.08", "selected_contract": "ZQN27", "unit": "percent_per_annum", "validation_status": "PASS", "availability_status": "AVAILABLE"}
    result = module.build_handoff([row], "section10.json")
    assert result[0]["value"] == 4.08 and result[0]["selected_contract"] == "ZQN27"

def test_rejects_wrong_unit(tmp_path):
    path = tmp_path / "input.csv"
    path.write_text("variable_id,observation_date,expected_terminal_policy_rate_pct,selected_contract,unit,validation_status,availability_status\nL3-003,2026-08-29,4.08,ZQN27,percent,PASS,AVAILABLE\n", encoding="utf-8")
    with pytest.raises(ValueError): module.load_rows(path)
