import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("l1_007_parser", Path(__file__).parents[1] / "parser.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
calculate_forward = module.calculate_forward
parse_observations = module.parse_observations


class L1007ParserTests(unittest.TestCase):
    def test_formula(self):
        expected = 100 * (((1 + 2.41 / 100) ** 10 / (1 + 2.12 / 100) ** 5) ** (1 / 5) - 1)
        self.assertAlmostEqual(calculate_forward(2.12, 2.41), expected, places=12)

    def test_inner_join_and_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            five = root / "DFII5.json"; ten = root / "DFII10.json"
            five.write_text(json.dumps({"observations": [{"date": "2026-08-20", "value": "2.12"}, {"date": "2026-08-19", "value": "."}]}), encoding="utf-8")
            ten.write_text(json.dumps({"observations": [{"date": "2026-08-20", "value": "2.41"}, {"date": "2026-08-18", "value": "2.38"}]}), encoding="utf-8")
            rows = parse_observations(five, ten, dfii5_retrieved_at="2026-08-21T00:00:00+00:00", dfii10_retrieved_at="2026-08-21T00:00:00+00:00")
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["input_5y_series_id"], "DFII5")
            self.assertEqual(rows[0]["input_10y_series_id"], "DFII10")
            self.assertEqual(rows[0]["formula_version"], "5y5y-real-forward-compound-v1")
            self.assertEqual(len(rows[0]["input_5y_raw_sha256"]), 64)

    def test_no_overlap_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); five = root / "five.json"; ten = root / "ten.json"
            five.write_text(json.dumps({"observations": [{"date": "2026-08-20", "value": "2"}]}), encoding="utf-8")
            ten.write_text(json.dumps({"observations": [{"date": "2026-08-19", "value": "2"}]}), encoding="utf-8")
            with self.assertRaises(ValueError):
                parse_observations(five, ten, dfii5_retrieved_at="2026-08-21T00:00:00+00:00", dfii10_retrieved_at="2026-08-21T00:00:00+00:00")


if __name__ == "__main__":
    unittest.main()
