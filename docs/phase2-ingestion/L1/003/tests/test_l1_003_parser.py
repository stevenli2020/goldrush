import importlib.util
import csv
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("l1_003_parser", Path(__file__).parents[1] / "parser.py")
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
calculate_components, parse_source = module.calculate_components, module.parse_source


class L1003ParserTests(unittest.TestCase):
    def test_component_formulas(self):
        values = {"TIPSY02": 2, "TIPSY03": 3, "TIPSY05": 5, "TIPSY07": 7, "TIPSY10": 10, "TIPSY20": 20}
        result = calculate_components(values)
        self.assertEqual(result["forward_2y1y"], 5)
        self.assertEqual(result["forward_3y2y"], 8)
        self.assertEqual(result["forward_5y2y"], 12)
        self.assertEqual(result["forward_7y3y"], 17)
        self.assertEqual(result["forward_10y10y"], 30)

    def test_complete_case_provenance_and_stale(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory) / "source.csv"
            raw.write_text("Note\nDate,TIPSY02,TIPSY03,TIPSY05,TIPSY07,TIPSY10,TIPSY20\n2020-01-02,2,3,5,7,10,20\n", encoding="utf-8")
            rows = parse_source(raw, source_retrieved_at="2026-08-21T00:00:00+00:00")
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["availability_status"], "STALE")
            self.assertEqual(rows[0]["source_name"], "Federal Reserve GS&W")
            self.assertEqual(len(rows[0]["raw_sha256"]), 64)
            self.assertEqual(rows[0]["formula_version"], "gsw-forward-summary-v1")

    def test_missing_input_is_not_interpolated(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory) / "source.csv"
            raw.write_text("Date,TIPSY02,TIPSY03,TIPSY05,TIPSY07,TIPSY10,TIPSY20\n2026-08-20,2,3,5,7,10,.\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                parse_source(raw, source_retrieved_at="2026-08-21T00:00:00+00:00")

    def test_malformed_source_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory) / "bad.csv"
            raw.write_text("Date,TIPSY02\n2026-08-20,2\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                parse_source(raw, source_retrieved_at="2026-08-21T00:00:00+00:00")


if __name__ == "__main__":
    unittest.main()
