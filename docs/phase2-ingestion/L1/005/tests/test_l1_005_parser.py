import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
spec = importlib.util.spec_from_file_location('l1_005_parser', Path(__file__).parents[1] / 'parser.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
parse_observations, write_csv = (module.parse_observations, module.write_csv)

class L1005ParserTests(unittest.TestCase):

    def test_valid_and_stale_observations(self):
        payload = {'observations': [{'date': '2026-08-20', 'value': '0.42'}, {'date': '2020-01-02', 'value': '0.10'}]}
        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory) / 'THREEFYTP10.json'
            raw.write_text(json.dumps(payload), encoding='utf-8')
            rows = parse_observations(raw, retrieved_at='2026-08-21T00:00:00+00:00')
            self.assertEqual(rows[0]['variable_id'], 'L1-005')
            self.assertEqual(rows[0]['source_series_id'], 'THREEFYTP10')
            self.assertEqual(rows[0]['validation_status'], 'PASS')
            self.assertEqual(rows[1]['availability_status'], 'STALE')

    def test_outlier_and_missing_marker(self):
        payload = {'observations': [{'date': '2026-08-20', 'value': '12'}, {'date': '2026-08-19', 'value': '.'}]}
        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory) / 'raw.json'
            raw.write_text(json.dumps(payload), encoding='utf-8')
            rows = parse_observations(raw)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['validation_status'], 'FLAG')

    def test_malformed_payload_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory) / 'bad.json'
            raw.write_text(json.dumps({'observations': [{'date': 'bad', 'value': 'x'}]}), encoding='utf-8')
            with self.assertRaises(ValueError):
                parse_observations(raw)
if __name__ == '__main__':
    unittest.main()
