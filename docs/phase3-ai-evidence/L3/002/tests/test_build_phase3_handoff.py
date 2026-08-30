import importlib.util
from pathlib import Path
import pytest

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_phase3_handoff.py"
spec = importlib.util.spec_from_file_location("l3_002_handoff", MODULE_PATH)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

def test_builds_curve_contract_rows():
    row = {"variable_id": "L3-002", "observation_date": "2026-08-29", "contract": "ZQQ26", "implied_policy_rate_pct": "3.63", "unit": "percent_per_annum", "validation_status": "PASS", "availability_status": "AVAILABLE"}
    result = module.build_handoff([row], "section10.json")
    assert result[0]["value"] == 3.63 and result[0]["contract"] == "ZQQ26"

def test_rejects_wrong_unit(tmp_path):
    path = tmp_path / "input.csv"
    path.write_text("variable_id,observation_date,contract,implied_policy_rate_pct,unit,validation_status,availability_status\nL3-002,2026-08-29,ZQQ26,3.63,percent,PASS,AVAILABLE\n", encoding="utf-8")
    with pytest.raises(ValueError): module.load_rows(path)
