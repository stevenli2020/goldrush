import json
import tempfile
import unittest
import importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location('l1_002_parser', Path(__file__).parents[1] / 'parser.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
parse_observations, write_csv = (module.parse_observations, module.write_csv)

class L1002ParserTests(unittest.TestCase):

    def test_parse_valid_observations_and_stale_status(self):
        payload = {'observations': [{'date': '2026-08-20', 'value': '1.42'}, {'date': '2020-01-02', 'value': '0.10'}]}
        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory) / 'DFII5.json'
            raw.write_text(json.dumps(payload), encoding='utf-8')
            rows = parse_observations(raw, retrieved_at='2026-08-21T00:00:00+00:00')
            self.assertEqual(rows[0]['variable_id'], 'L1-002')
            self.assertEqual(rows[0]['source_series_id'], 'DFII5')
            self.assertEqual(rows[0]['validation_status'], 'PASS')
            self.assertEqual(rows[1]['availability_status'], 'STALE')

    def test_outlier_is_flagged_and_output_is_written(self):
        payload = {'observations': [{'date': '2026-08-20', 'value': '25'}]}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = root / 'raw.json'
            raw.write_text(json.dumps(payload), encoding='utf-8')
            rows = parse_observations(raw)
            self.assertEqual(rows[0]['validation_status'], 'FLAG')
            output = root / 'processed.csv'
            write_csv(rows, output)
            self.assertTrue(output.exists())

    def test_fred_missing_value_is_skipped(self):
        payload = {'observations': [{'date': '2026-08-19', 'value': '.'}, {'date': '2026-08-20', 'value': '1.42'}]}
        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory) / 'DFII5.json'
            raw.write_text(json.dumps(payload), encoding='utf-8')
            rows = parse_observations(raw)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['observation_date'], '2026-08-20')

    def test_malformed_payload_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory) / 'bad.json'
            raw.write_text(json.dumps({'observations': [{'date': 'bad', 'value': '.'}]}), encoding='utf-8')
            with self.assertRaises(ValueError):
                parse_observations(raw)
if __name__ == '__main__':
    unittest.main()
