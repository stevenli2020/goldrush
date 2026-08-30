import importlib.util
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_phase3_handoff.py"
spec = importlib.util.spec_from_file_location("l0_003_handoff", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_builds_global_holdings_row():
    result = module.build_handoff([{
        "observation_date": "2026-07-31", "region": "GLOBAL", "holdings_tonnes": "4067.97",
        "unit": "metric_tonnes", "validation_status": "PASS", "availability_status": "AVAILABLE",
    }], "manifest.json")
    assert result[0]["value"] == 4067.97
    assert result[0]["quality_flag"] == "PASS"


def test_preserves_parser_flag_as_quality_flag():
    row = {"observation_date": "2020-01-31", "region": "GLOBAL", "holdings_tonnes": "3000",
           "unit": "metric_tonnes", "validation_status": "FLAG", "availability_status": "AVAILABLE"}
    assert module.build_handoff([row], "manifest.json")[0]["quality_flag"] == "FLAG"


def test_rejects_unavailable_input(tmp_path):
    path = tmp_path / "input.csv"
    path.write_text("observation_date,region,holdings_tonnes,unit,validation_status,availability_status\n2026-01-31,GLOBAL,1,metric_tonnes,PASS,STALE\n", encoding="utf-8")
    with pytest.raises(ValueError):
        module.load_rows(path)
