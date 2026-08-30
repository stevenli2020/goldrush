import importlib.util
from pathlib import Path
import pytest

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_phase3_handoff.py"
spec = importlib.util.spec_from_file_location("l2_002_handoff", MODULE_PATH)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

def test_builds_broad_dollar_index_handoff():
    row = {"variable_id": "L2-002", "observation_date": "2026-08-21", "index_value": "118.0628", "unit": "index", "validation_status": "PASS", "availability_status": "AVAILABLE"}
    result = module.build_handoff([row], "fred.json")
    assert result[0]["value"] == 118.0628 and result[0]["availability_status"] == "AVAILABLE"

def test_rejects_wrong_unit(tmp_path):
    path = tmp_path / "input.csv"
    path.write_text("variable_id,observation_date,index_value,unit,validation_status,availability_status\nL2-002,2026-08-21,118.06,percent,PASS,AVAILABLE\n", encoding="utf-8")
    with pytest.raises(ValueError): module.load_rows(path)
