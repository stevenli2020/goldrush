import importlib.util
from pathlib import Path
import pytest

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_phase3_handoff.py"
spec = importlib.util.spec_from_file_location("l3_005_handoff", MODULE_PATH)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

def test_builds_dot_distribution_handoff():
    row = {"variable_id": "L3-005", "sep_release_date": "2026-06-17", "projection_horizon": "2027", "rate_bin_midpoint": "3.875", "participant_count": "3", "median_projected_rate": "3.8", "unit": "percent", "validation_status": "PASS", "availability_status": "AVAILABLE"}
    result = module.build_handoff([row], "sep.json")
    assert result[0]["value"] == 3.875 and result[0]["participant_count"] == 3

def test_rejects_wrong_unit(tmp_path):
    path = tmp_path / "input.csv"
    path.write_text("variable_id,sep_release_date,projection_horizon,rate_bin_midpoint,participant_count,median_projected_rate,unit,validation_status,availability_status\nL3-005,2026-06-17,2027,3.875,3,3.8,index,PASS,AVAILABLE\n", encoding="utf-8")
    with pytest.raises(ValueError): module.load_rows(path)
