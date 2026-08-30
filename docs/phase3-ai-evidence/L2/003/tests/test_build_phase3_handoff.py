import importlib.util
from pathlib import Path
import pytest

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_phase3_handoff.py"
spec = importlib.util.spec_from_file_location("l2_003_handoff", MODULE_PATH)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

def test_builds_usd_cny_handoff():
    row = {"variable_id": "L2-003", "observation_date": "2026-08-21", "usd_cny": "6.721", "unit": "cny_per_usd", "validation_status": "PASS", "availability_status": "AVAILABLE"}
    result = module.build_handoff([row], "fred.json")
    assert result[0]["value"] == 6.721 and result[0]["unit_or_scale"] == "cny_per_usd"

def test_rejects_wrong_unit(tmp_path):
    path = tmp_path / "input.csv"
    path.write_text("variable_id,observation_date,usd_cny,unit,validation_status,availability_status\nL2-003,2026-08-21,6.721,index,PASS,AVAILABLE\n", encoding="utf-8")
    with pytest.raises(ValueError): module.load_rows(path)
