import importlib.util
from pathlib import Path
import pytest

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_phase3_handoff.py"
spec = importlib.util.spec_from_file_location("l2_001_handoff", MODULE_PATH)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

def test_builds_dxy_close_handoff():
    row = {"variable_id": "L2-001", "observation_date": "2026-08-21", "dxy_close": "98.8", "canonical_field": "dxy_close", "unit": "index", "validation_status": "PASS", "availability_status": "STALE"}
    result = module.build_handoff([row], "dxy.json")
    assert result[0]["value"] == 98.8 and result[0]["availability_status"] == "STALE"

def test_rejects_invalid_canonical_field(tmp_path):
    path = tmp_path / "input.csv"
    path.write_text("variable_id,observation_date,dxy_close,canonical_field,unit,validation_status,availability_status\nL2-001,2026-08-21,98.8,dxy_open,index,PASS,AVAILABLE\n", encoding="utf-8")
    with pytest.raises(ValueError): module.load_rows(path)
