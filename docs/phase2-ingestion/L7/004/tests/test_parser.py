import csv
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from jsonschema import FormatChecker, validate
sys.path.insert(0, str(Path(__file__).parents[1]))
from parser import carry_forward, parse_observations, write_csv
SCHEMA = json.loads((Path(__file__).parents[1] / 'schema.json').read_text(encoding='utf-8'))

class L7004ParserTests(unittest.TestCase):

    def write_raw(self, root, observations):
        path = Path(root) / 'raw.json'
        path.write_text(json.dumps({'observations': observations}), encoding='utf-8')
        return path

    def write_manifest(self, root, raw, *, series_id='BAMLH0A0HYM2', metadata=None):
        path = Path(root) / 'manifest.json'
        path.write_text(json.dumps({'series_id': series_id, 'retrieved_at': '2026-08-23T20:30:00+00:00'}), encoding='utf-8')
        return path

    def test_valid_parse_missing_marker_order_units_weekend_and_schema(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = self.write_raw(directory, [{'date': '2026-08-21', 'value': '3.06'}, {'date': '2026-08-19', 'value': '3.12'}, {'date': '2026-08-20', 'value': '.'}])
            manifest = self.write_manifest(directory, raw)
            rows = parse_observations(raw, manifest, today=date(2026, 8, 23))
            self.assertEqual([row['observation_date'] for row in rows], ['2026-08-19', '2026-08-21'])
            self.assertEqual(rows[-1]['high_yield_oas_pct'], 3.06)
            self.assertEqual(rows[-1]['unit'], 'percentage_points')
            self.assertEqual(rows[-1]['availability_status'], 'AVAILABLE')
            validate(rows[-1], SCHEMA, format_checker=FormatChecker())

    def test_bad_date_nonfinite_rejected_and_finite_outlier_flagged(self):
        with tempfile.TemporaryDirectory() as directory:
            for observation in ({'date': 'bad', 'value': '3.1'}, {'date': '2026-08-21', 'value': 'nan'}):
                raw = self.write_raw(directory, [observation])
                manifest = self.write_manifest(directory, raw)
                with self.assertRaises(ValueError):
                    parse_observations(raw, manifest)
            raw = self.write_raw(directory, [{'date': '2026-08-21', 'value': '35'}])
            manifest = self.write_manifest(directory, raw)
            self.assertEqual(parse_observations(raw, manifest)[0]['validation_status'], 'FLAG')

    def test_duplicate_dates_dedupe_or_reject_conflicts(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = self.write_raw(directory, [{'date': '2026-08-21', 'value': '3.06'}, {'date': '2026-08-21', 'value': '3.06'}])
            self.assertEqual(len(parse_observations(raw, self.write_manifest(directory, raw))), 1)
            raw = self.write_raw(directory, [{'date': '2026-08-21', 'value': '3.06'}, {'date': '2026-08-21', 'value': '3.07'}])
            with self.assertRaises(ValueError):
                parse_observations(raw, self.write_manifest(directory, raw))

    def test_prior_fallback_is_one_stale_schema_valid_row(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = self.write_raw(directory, [{'date': '2026-08-21', 'value': '3.06'}])
            prior = root / 'prior.csv'
            write_csv(parse_observations(raw, self.write_manifest(directory, raw)), prior)
            rows = carry_forward(prior, retrieved_at='2026-08-24T00:00:00+00:00')
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['availability_status'], 'STALE')
            validate(rows[0], SCHEMA, format_checker=FormatChecker())

    def test_cli_failure_uses_valid_prior(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = self.write_raw(directory, [{'date': '2026-08-21', 'value': '3.06'}])
            prior = root / 'prior.csv'
            write_csv(parse_observations(raw, self.write_manifest(directory, raw)), prior)
            bad_raw = self.write_raw(directory, [{'date': 'bad', 'value': '3.1'}])
            bad_manifest = self.write_manifest(directory, bad_raw)
            output = root / 'fallback.csv'
            result = subprocess.run([sys.executable, str(Path(__file__).parents[1] / 'parser.py'), '--raw', str(bad_raw), '--manifest', str(bad_manifest), '--prior', str(prior), '--output', str(output)], capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0)
            rows = list(csv.DictReader(output.open(encoding='utf-8')))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['availability_status'], 'STALE')

    def test_cli_blocked_then_recovery_clears_status(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bad_raw = self.write_raw(directory, [{'date': 'bad', 'value': '3.1'}])
            bad_manifest = self.write_manifest(directory, bad_raw)
            output = root / 'processed' / 'L7_004_observations.csv'
            command = [sys.executable, str(Path(__file__).parents[1] / 'parser.py')]
            blocked = subprocess.run(command + ['--raw', str(bad_raw), '--manifest', str(bad_manifest), '--output', str(output)], capture_output=True, text=True, check=False)
            status_path = output.with_suffix('.status.json')
            self.assertEqual(blocked.returncode, 0)
            self.assertEqual(json.loads(status_path.read_text())['availability_status'], 'BLOCKED')
            good_raw = self.write_raw(directory, [{'date': '2026-08-21', 'value': '3.06'}])
            good_manifest = self.write_manifest(directory, good_raw)
            recovered = subprocess.run(command + ['--raw', str(good_raw), '--manifest', str(good_manifest), '--output', str(output)], capture_output=True, text=True, check=False)
            self.assertEqual(recovered.returncode, 0)
            self.assertTrue(output.exists())
            self.assertFalse(status_path.exists())
if __name__ == '__main__':
    unittest.main()
