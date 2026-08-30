import importlib.util
from pathlib import Path
import pytest

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_phase3_handoff.py"
spec = importlib.util.spec_from_file_location("l3_001_handoff", MODULE_PATH)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

def test_builds_fed_funds_path_handoff():
    row = {"variable_id": "L3-001", "observation_date": "2026-08-29", "path_average_percent": "3.8954", "unit": "percent_per_annum", "validation_status": "PASS", "availability_status": "AVAILABLE"}
    result = module.build_handoff([row], "section10.json")
    assert result[0]["value"] == 3.8954 and result[0]["unit_or_scale"] == "percent_per_annum"

def test_rejects_wrong_unit(tmp_path):
    path = tmp_path / "input.csv"
    path.write_text("variable_id,observation_date,path_average_percent,unit,validation_status,availability_status\nL3-001,2026-08-29,3.8954,percent,PASS,AVAILABLE\n", encoding="utf-8")
    with pytest.raises(ValueError): module.load_rows(path)
