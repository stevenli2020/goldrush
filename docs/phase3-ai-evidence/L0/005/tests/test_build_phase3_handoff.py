import importlib.util
from pathlib import Path
import pytest

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_phase3_handoff.py"
spec = importlib.util.spec_from_file_location("l0_005_handoff", MODULE_PATH)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

def row(period="Q2'26", status="PASS"):
    return {"observation_period": period, "observation_period_type": "quarterly", "observation_year": "2026", "observation_quarter": "2", "total_bar_and_coin_tonnes": "307.08", "unit": "metric_tonnes", "validation_status": status, "availability_status": "AVAILABLE"}

def test_builds_period_preserving_handoff():
    result = module.build_handoff([row()], "manifest.json")
    assert result[0]["observation_period"] == "Q2'26" and result[0]["value"] == 307.08

def test_rejects_duplicate_periods(tmp_path):
    path = tmp_path / "input.csv"; fields = list(row()); path.write_text(",".join(fields) + "\n" + ",".join(row().values()) + "\n" + ",".join(row().values()) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate"):
        module.load_rows(path)
