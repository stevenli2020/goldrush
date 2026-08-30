import importlib.util
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_phase3_handoff.py"
spec = importlib.util.spec_from_file_location("l0_001_handoff", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def rows():
    return [
        {
            "observation_year": "2025",
            "observation_date": "2025-12-31",
            "total_above_ground_tonnes": "216000",
            "validation_status": "PASS",
            "availability_status": "AVAILABLE",
        }
    ]


def test_builds_canonical_total_stock_row():
    result = module.build_handoff(rows(), "manifest.json")
    assert result == [
        {
            "variable_id": "L0-001",
            "observation_timestamp": "2025-12-31T00:00:00Z",
            "value": 216000.0,
            "unit_or_scale": "metric_tonnes",
            "availability_status": "AVAILABLE",
            "source_reference": "manifest.json",
            "quality_flag": "PASS",
        }
    ]


@pytest.mark.parametrize(
    "status",
    [("FLAG", "AVAILABLE"), ("PASS", "STALE"), ("PASS", "BLOCKED")],
)
def test_rejects_noncanonical_status(status, tmp_path):
    data = rows()
    data[0]["validation_status"], data[0]["availability_status"] = status
    path = tmp_path / "test-input.csv"
    path.write_text(",".join(data[0]) + "\n" + ",".join(data[0].values()) + "\n", encoding="utf-8")
    with pytest.raises(ValueError):
        module.load_rows(path)
