import importlib.util
from pathlib import Path
import pytest

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_phase3_handoff.py"
spec = importlib.util.spec_from_file_location("l0_009_handoff", MODULE_PATH)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

def test_builds_forward_minus_sofr_handoff():
    row = {"variable_id": "L0-009", "observation_date": "2026-08-28", "value": "-0.85", "unit": "percent_per_annum", "validation_status": "PASS", "availability_status": "AVAILABLE"}
    result = module.build_handoff([row], "cme.json;sofr.json")
    assert result[0]["value"] == -0.85 and result[0]["unit_or_scale"] == "percent_per_annum"

def test_rejects_unavailable_input(tmp_path):
    path = tmp_path / "input.csv"
    path.write_text("variable_id,observation_date,value,unit,validation_status,availability_status\nL0-009,2026-08-28,-0.85,percent_per_annum,PASS,STALE\n", encoding="utf-8")
    with pytest.raises(ValueError): module.load_rows(path)
