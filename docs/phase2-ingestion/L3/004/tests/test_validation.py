import importlib.util
from datetime import date
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).parents[1] / "validate_alternative1.py"
spec = importlib.util.spec_from_file_location("l3_004_validation", MODULE_PATH)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)


def test_filename_and_basis_point_range_parsing():
    assert module.meeting_date_from_filename(Path("FedMeeting_20260916_downloaded_2026-08-24.csv")) == date(2026, 9, 16)
    assert module.official_bucket("(350-375)") == (3.5, 3.75)
    with pytest.raises(ValueError): module.meeting_date_from_filename(Path("meeting.csv"))
    with pytest.raises(ValueError): module.official_bucket("(375-350)")


def test_official_header_blank_and_numerical_zero(tmp_path):
    path = tmp_path / "FedMeeting_20260916_downloaded_2026-08-24.csv"
    path.write_text("Date,(325-350),(350-375),(375-400)\n8/21/2026,,0.000000,1.000000\n", encoding="utf-8")
    distribution = module.load_official(path, date(2026, 8, 21))
    assert "(325-350)" not in distribution and distribution["(350-375)"] == 0.0
    assert distribution["(375-400)"] == 1.0


def test_official_csv_rejects_bad_header(tmp_path):
    path = tmp_path / "FedMeeting_20260916_downloaded_2026-08-24.csv"
    path.write_text("Wrong,(350-375)\n8/21/2026,1.0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Date header"): module.load_official(path, date(2026, 8, 21))


def test_comparison_thresholds_and_missing_bucket():
    passing = module.compare_distributions({"(350-375)": 0.60, "(375-400)": 0.40},
        {"(350-375)": 0.50, "(375-400)": 0.50})
    assert passing["maximum_absolute_bucket_error"] == pytest.approx(0.10)
    assert passing["total_variation_distance"] == pytest.approx(0.10) and passing["pass"]
    failing = module.compare_distributions({"(350-375)": 0.60, "(375-400)": 0.40},
        {"(375-400)": 0.20, "(400-425)": 0.80})
    assert failing["missing_material_official_buckets"] == ["(350-375)"] and not failing["pass"]


def test_material_bucket_threshold_is_inclusive():
    result = module.compare_distributions({"(350-375)": 0.999, "(375-400)": 0.001}, {"(350-375)": 1.0})
    assert result["missing_material_official_buckets"] == ["(375-400)"]
