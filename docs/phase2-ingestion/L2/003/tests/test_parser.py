import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from jsonschema import Draft7Validator, FormatChecker
sys.path.insert(0, str(Path(__file__).parents[1]))
from parser import carry_forward, parse_observations

class L2003ParserTests(unittest.TestCase):

    def write_raw(self, directory, payload, *, series_id=None):
        if series_id is not None:
            payload = {**payload, 'series_id': series_id}
        path = Path(directory) / 'raw.json'
        path.write_text(json.dumps(payload), encoding='utf-8')
        return path

    def write_manifest(self, directory, raw_path, series_id='DEXCHUS'):
        path = Path(directory) / 'manifest.json'
        path.write_text(json.dumps({'series_id': series_id, 'retrieved_at': '2026-08-23T00:00:00+00:00'}), encoding='utf-8')
        return path

    def test_quote_direction_missing_and_ordering(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = self.write_raw(directory, {'observations': [{'date': '2026-01-03', 'value': '6.8'}, {'date': '2026-01-02', 'value': '.'}, {'date': '2026-01-01', 'value': '6.9'}]})
            rows = parse_observations(raw, stale_after_days=1000)
            self.assertEqual([r['observation_date'] for r in rows], ['2026-01-01', '2026-01-03'])
            self.assertEqual(rows[0]['usd_cny'], 6.9)
            self.assertEqual(rows[0]['unit'], 'cny_per_usd')
            self.assertEqual(rows[0]['source_series_id'], 'DEXCHUS')

    def test_invalid_duplicate_series_and_numeric_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            duplicate = self.write_raw(directory, {'observations': [{'date': '2026-01-01', 'value': '6.9'}, {'date': '2026-01-01', 'value': '7.0'}]})
            with self.assertRaises(ValueError):
                parse_observations(duplicate)
            wrong = self.write_raw(directory, {'observations': [{'date': '2026-01-01', 'value': '6.9'}]}, series_id='DTWEXBGS')
            with self.assertRaises(ValueError):
                parse_observations(wrong)
            malformed = self.write_raw(directory, {'observations': [{'date': '2026-01-01', 'value': 'bad'}]})
            with self.assertRaises(ValueError):
                parse_observations(malformed)

    def test_rows_validate_against_schema(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = self.write_raw(directory, {'observations': [{'date': '2026-08-14', 'value': '6.7412'}]})
            rows = parse_observations(raw, stale_after_days=1000)
            schema = json.loads((Path(__file__).parents[1] / 'schema.json').read_text(encoding='utf-8'))
            instance = {**rows[0], 'usd_cny': float(rows[0]['usd_cny'])}
            self.assertEqual(list(Draft7Validator(schema, format_checker=FormatChecker()).iter_errors(instance)), [])

    def test_prior_stale_and_cli_blocked_recovery(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prior = root / 'prior.csv'
            with prior.open('w', newline='', encoding='utf-8') as handle:
                writer = csv.DictWriter(handle, fieldnames=['variable_id', 'observation_date', 'usd_cny', 'validation_status', 'availability_status'])
                writer.writeheader()
                writer.writerow({'variable_id': 'L2-003', 'observation_date': '2026-01-01', 'usd_cny': '6.9', 'validation_status': 'PASS', 'availability_status': 'AVAILABLE'})
            self.assertEqual(carry_forward(prior, retrieved_at='2026-08-23T00:00:00+00:00')[0]['availability_status'], 'STALE')
            output = root / 'processed' / 'L2_003_observations.csv'
            bad = self.write_raw(directory, {'observations': [{'date': 'bad', 'value': '6.9'}]})
            script = str(Path(__file__).parents[1] / 'parser.py')
            blocked = subprocess.run([sys.executable, script, '--raw', str(bad), '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(blocked.returncode, 0)
            status_path = output.with_suffix('.status.json')
            self.assertEqual(json.loads(status_path.read_text(encoding='utf-8'))['status'], 'BLOCKED')
            good = self.write_raw(directory, {'observations': [{'date': '2026-08-14', 'value': '6.7412'}]})
            recovered = subprocess.run([sys.executable, script, '--raw', str(good), '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(recovered.returncode, 0)
            self.assertTrue(output.exists())
            self.assertFalse(status_path.exists())

    def test_cli_prior_fallback_writes_schema_valid_stale_row(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prior = root / 'canonical_prior.csv'
            raw_metadata = 'a' * 64
            fields = ['variable_id', 'observation_date', 'usd_cny', 'unit', 'source_name', 'source_series_id', 'source_release', 'raw_file_path', 'manifest_path', 'retrieved_at', 'validation_status', 'availability_status', 'parser_version']
            row = {'variable_id': 'L2-003', 'observation_date': '2026-08-14', 'usd_cny': '6.7412', 'unit': 'cny_per_usd', 'source_name': 'FRED / Federal Reserve Board', 'source_series_id': 'DEXCHUS', 'source_release': 'H.10 Foreign Exchange Rates', 'raw_file_path': 'raw.json', 'manifest_path': 'manifest.json', 'retrieved_at': '2026-08-23T00:00:00+00:00', 'validation_status': 'PASS', 'availability_status': 'AVAILABLE', 'parser_version': '0.1.0'}
            with prior.open('w', newline='', encoding='utf-8') as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerow(row)
            output = root / 'processed' / 'L2_003_observations.csv'
            script = str(Path(__file__).parents[1] / 'parser.py')
            result = subprocess.run([sys.executable, script, '--raw', str(root / 'missing.json'), '--prior', str(prior), '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            fallback_rows = list(csv.DictReader(output.open(newline='', encoding='utf-8')))
            self.assertEqual(len(fallback_rows), 1)
            self.assertEqual(fallback_rows[0]['availability_status'], 'STALE')
            schema = json.loads((Path(__file__).parents[1] / 'schema.json').read_text(encoding='utf-8'))
            instance = {**fallback_rows[0], 'usd_cny': float(fallback_rows[0]['usd_cny'])}
            self.assertEqual(list(Draft7Validator(schema, format_checker=FormatChecker()).iter_errors(instance)), [])
if __name__ == '__main__':
    unittest.main()
