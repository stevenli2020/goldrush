import csv
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
from parser import carry_forward, parse_observations

class L2002ParserTests(unittest.TestCase):

    def write_raw(self, directory, payload, *, series_id=None):
        if series_id is not None:
            payload = {**payload, 'series_id': series_id}
        path = Path(directory) / 'raw.json'
        path.write_text(json.dumps(payload), encoding='utf-8')
        return path

    def write_manifest(self, directory, raw_path, series_id='DTWEXBGS'):
        metadata = None
        path = Path(directory) / 'manifest.json'
        path.write_text(json.dumps({'series_id': series_id, 'retrieved_at': '2026-08-23T00:00:00+00:00'}), encoding='utf-8')
        return path

    def test_valid_missing_and_ordering(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = self.write_raw(directory, {'observations': [{'date': '2026-01-03', 'value': '119.2'}, {'date': '2026-01-02', 'value': '.'}, {'date': '2026-01-01', 'value': '118.9'}]})
            rows = parse_observations(raw, stale_after_days=1000)
            self.assertEqual([r['observation_date'] for r in rows], ['2026-01-01', '2026-01-03'])
            self.assertEqual(rows[0]['source_series_id'], 'DTWEXBGS')
            self.assertEqual(rows[0]['availability_status'], 'AVAILABLE')

    def test_conflicting_duplicate_and_wrong_series_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = self.write_raw(directory, {'observations': [{'date': '2026-01-01', 'value': '119'}, {'date': '2026-01-01', 'value': '120'}]})
            with self.assertRaises(ValueError):
                parse_observations(raw)
            wrong = self.write_raw(directory, {'observations': [{'date': '2026-01-01', 'value': '119'}]}, series_id='DFII10')
            with self.assertRaises(ValueError):
                parse_observations(wrong)

    def test_manifest_provenance_and_freshness(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = self.write_raw(directory, {'observations': [{'date': '2026-01-01', 'value': '119'}]})
            manifest = self.write_manifest(directory, raw)
            rows = parse_observations(raw, manifest_path=manifest, stale_after_days=1)
            self.assertEqual(rows[0]['retrieved_at'], '2026-08-23T00:00:00+00:00')
            self.assertEqual(rows[0]['availability_status'], 'STALE')

    def test_fallback_with_and_without_prior(self):
        with tempfile.TemporaryDirectory() as directory:
            prior = Path(directory) / 'prior.csv'
            fields = ['variable_id', 'observation_date', 'index_value', 'validation_status', 'availability_status']
            with prior.open('w', newline='', encoding='utf-8') as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerow({'variable_id': 'L2-002', 'observation_date': '2026-01-01', 'index_value': '119', 'validation_status': 'PASS', 'availability_status': 'AVAILABLE'})
            rows = carry_forward(prior, retrieved_at='2026-08-23T00:00:00+00:00')
            self.assertEqual(rows[0]['availability_status'], 'STALE')
            with self.assertRaises(FileNotFoundError):
                carry_forward(Path(directory) / 'missing.csv')

    def test_out_of_range_is_flagged(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = self.write_raw(directory, {'observations': [{'date': '2026-01-01', 'value': '250'}]})
            self.assertEqual(parse_observations(raw)[0]['validation_status'], 'FLAG')

    def test_cli_writes_blocked_status_without_prior(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = self.write_raw(directory, {'observations': [{'date': 'bad', 'value': '119'}]})
            output = root / 'processed' / 'L2_002_observations.csv'
            result = subprocess.run([sys.executable, str(Path(__file__).parents[1] / 'parser.py'), '--raw', str(raw), '--output', str(output)], capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0)
            status_path = output.with_suffix('.status.json')
            status = json.loads(status_path.read_text(encoding='utf-8'))
            self.assertEqual(status['status'], 'BLOCKED')
            self.assertEqual(status['availability_status'], 'BLOCKED')
            valid_raw = self.write_raw(directory, {'observations': [{'date': '2026-08-14', 'value': '118.9028'}]})
            recovered = subprocess.run([sys.executable, str(Path(__file__).parents[1] / 'parser.py'), '--raw', str(valid_raw), '--output', str(output)], capture_output=True, text=True, check=False)
            self.assertEqual(recovered.returncode, 0)
            self.assertTrue(output.exists())
            self.assertFalse(status_path.exists())
if __name__ == '__main__':
    unittest.main()
