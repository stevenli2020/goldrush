import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from jsonschema import Draft7Validator, FormatChecker
sys.path.insert(0, str(Path(__file__).parents[1]))
from parser import carry_forward, parse_raw

class L2001Tests(unittest.TestCase):

    def raw(self, root, text):
        path = Path(root) / 'raw.csv'
        path.write_text(text, encoding='utf-8')
        return path

    def manifest(self, root, raw):
        path = Path(root) / 'manifest.json'
        path.write_text(json.dumps({'symbol': 'DX-Y.NYB', 'retrieved_at': '2026-08-24T00:00:00+00:00'}), encoding='utf-8')
        return path

    def test_normalization_missing_order_and_schema(self):
        with tempfile.TemporaryDirectory() as root:
            raw = self.raw(root, 'date,open,high,low,close,volume\n2026-08-14,100,101,99,100.5,0\n2026-08-13,99,100,98,99.5,0\n')
            rows = parse_raw(raw, manifest_path=self.manifest(root, raw), stale_after_days=1000)
            self.assertEqual(rows[0]['observation_date'], '2026-08-13')
            schema = json.loads((Path(__file__).parents[1] / 'schema.json').read_text())
            self.assertEqual(list(Draft7Validator(schema, format_checker=FormatChecker()).iter_errors(rows[0])), [])

    def test_invalid_date_numbers_and_missing_close_fail(self):
        with tempfile.TemporaryDirectory() as root:
            for text in ['date,close\nbad,100\n', 'date,close\n2026-08-14,bad\n', 'date,open\n2026-08-14,100\n']:
                with self.assertRaises(ValueError):
                    parse_raw(self.raw(root, text))

    def test_freshness_prior_and_revision(self):
        with tempfile.TemporaryDirectory() as root:
            raw = self.raw(root, 'date,open,high,low,close,volume\n2026-01-01,100,101,99,100,0\n')
            rows = parse_raw(raw, stale_after_days=1)
            self.assertEqual(rows[0]['availability_status'], 'STALE')
            prior = Path(root) / 'prior.csv'
            with prior.open('w', newline='') as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerow(rows[0])
            self.assertEqual(carry_forward(prior)[0]['availability_status'], 'STALE')
            same_raw = Path(root) / 'same.csv'
            same_raw.write_text(raw.read_text(encoding='utf-8'), encoding='utf-8')
            revised = self.raw(root, 'date,open,high,low,close,volume\n2026-01-01,100,101,99,101,0\n')
            changed = parse_raw(revised, prior_path=prior)
            self.assertTrue(changed[0]['is_revised'])
            same_snapshot = parse_raw(same_raw, prior_path=prior)
            self.assertFalse(same_snapshot[0]['is_revised'])

    def test_cli_blocked_recovery_and_prior(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            script = Path(__file__).parents[1] / 'parser.py'
            output = root / 'out.csv'
            bad = self.raw(root, 'date,close\nbad,100\n')
            result = subprocess.run([sys.executable, str(script), '--raw', str(bad), '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            status = output.with_suffix('.status.json')
            self.assertTrue(status.exists())
            good = self.raw(root, 'date,close\n2026-08-14,100\n')
            subprocess.run([sys.executable, str(script), '--raw', str(good), '--output', str(output)], check=True)
            self.assertTrue(output.exists())
            self.assertFalse(status.exists())
            prior = root / 'prior.csv'
            prior_rows = parse_raw(good)
            with prior.open('w', newline='') as handle:
                writer = csv.DictWriter(handle, fieldnames=list(prior_rows[0]))
                writer.writeheader()
                writer.writerows(prior_rows)
            result = subprocess.run([sys.executable, str(script), '--raw', str(bad), '--prior', str(prior), '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertFalse(status.exists())
            with output.open(newline='') as handle:
                carried = next(csv.DictReader(handle))
                self.assertEqual(carried['availability_status'], 'STALE')
            schema = json.loads((Path(__file__).parents[1] / 'schema.json').read_text())
            typed = dict(carried)
            for key in ('dxy_open', 'dxy_high', 'dxy_low', 'dxy_close', 'volume', 'prior_dxy_close'):
                typed[key] = None if typed[key] == '' else float(typed[key])
            typed['is_revised'] = typed['is_revised'].lower() == 'true'
            self.assertEqual(list(Draft7Validator(schema, format_checker=FormatChecker()).iter_errors(typed)), [])

    def test_nonfinite_and_incomplete_current_day(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(ValueError):
                parse_raw(self.raw(root, 'date,close\n2026-08-14,inf\n'))
            today = __import__('datetime').datetime.now(__import__('datetime').timezone.utc).date().isoformat()
            raw = self.raw(root, f'date,open,high,low,close,volume\n2026-08-21,100,101,99,100,0\n{today},100,101,99,100,0\n')
            rows = parse_raw(raw, stale_after_days=1000)
            self.assertEqual([row['observation_date'] for row in rows], ['2026-08-21'])

    def test_incomplete_historical_bar_is_skipped_and_latest_complete_bar_kept(self):
        with tempfile.TemporaryDirectory() as root:
            raw = self.raw(root, 'date,open,high,low,close,volume\n'
                                '2026-08-26,98.92,99.23,98.90,99.17,0\n'
                                '2026-08-27,99.12,99.26,99.07,99.16,0\n'
                                '2026-08-28,99.11,99.72,99.09,,0\n')
            rows = parse_raw(raw, stale_after_days=1000)
            self.assertEqual([row['observation_date'] for row in rows], ['2026-08-26', '2026-08-27'])
            self.assertEqual(rows[-1]['dxy_close'], 99.16)
if __name__ == '__main__':
    unittest.main()
