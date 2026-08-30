import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from jsonschema import validate
ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))
from parser import ENDPOINT, carry_forward, parse_manifest, write_csv
SCHEMA = json.loads((ROOT / 'schema.json').read_text(encoding='utf-8'))

def row(date, year, code, amount, description=None):
    descriptions = {'130': 'Total Receipts', '360': 'Interest on Treasury Debt Securities (Gross)'}
    return {'record_date': date, 'record_fiscal_year': str(year), 'line_code_nbr': code, 'classification_desc': description or descriptions[code], 'current_fytd_rcpt_outly_amt': str(amount)}

class L4008ParserTests(unittest.TestCase):

    def fixture(self, directory, rows, **manifest_changes):
        root = Path(directory)
        raw = root / 'raw.json'
        raw.write_text(json.dumps({'data': rows, 'meta': {'total-pages': 1}}), encoding='utf-8')
        metadata = None
        manifest = {'endpoint': ENDPOINT, 'query': {'filter': 'line_code_nbr:in:(130,360)', 'page[size]': 1000}, 'retrieved_at': '2026-08-24T00:00:00+00:00', 'raw_paths': [str(raw)]}
        manifest.update(manifest_changes)
        path = root / 'manifest.json'
        path.write_text(json.dumps(manifest), encoding='utf-8')
        return path

    def valid_rows(self):
        return [row('2024-08-31', 2024, '130', 300), row('2024-08-31', 2024, '360', 60), row('2024-09-30', 2024, '130', 500), row('2024-09-30', 2024, '360', 100), row('2025-09-30', 2025, '130', 600), row('2025-09-30', 2025, '360', 150)]

    def test_calculation_september_selection_and_schema(self):
        with tempfile.TemporaryDirectory() as directory:
            rows = parse_manifest(self.fixture(directory, self.valid_rows()), stale_after_days=10000)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]['interest_expense_to_revenue_pct'], 20.0)
            self.assertEqual(rows[1]['interest_expense_to_revenue_pct'], 25.0)
            self.assertTrue(all((r['observation_date'][5:7] == '09' for r in rows)))
            for item in rows:
                validate(item, SCHEMA)

    def test_wrong_description_and_missing_pair_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            bad = [row('2025-09-30', 2025, '130', 600, 'Wrong'), row('2025-09-30', 2025, '360', 150)]
            with self.assertRaises(ValueError):
                parse_manifest(self.fixture(directory, bad))
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                parse_manifest(self.fixture(directory, [row('2025-09-30', 2025, '130', 600)]))
        with tempfile.TemporaryDirectory() as directory:
            unexpected = row('2025-09-30', 2025, '130', 600)
            unexpected['line_code_nbr'] = '999'
            with self.assertRaises(ValueError):
                parse_manifest(self.fixture(directory, [unexpected]))

    def test_conflicting_duplicate_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            rows = self.valid_rows() + [row('2025-09-30', 2025, '130', 601)]
            with self.assertRaises(ValueError):
                parse_manifest(self.fixture(directory, rows))

    def test_pass_flag_available_and_stale(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = self.fixture(directory, [row('2025-09-30', 2025, '130', 100), row('2025-09-30', 2025, '360', 60)])
            flagged = parse_manifest(manifest, stale_after_days=10000)[0]
            self.assertEqual(flagged['validation_status'], 'FLAG')
            self.assertEqual(flagged['availability_status'], 'AVAILABLE')
            self.assertEqual(parse_manifest(manifest, stale_after_days=1)[0]['availability_status'], 'STALE')

    def test_fallback_output_is_one_schema_valid_stale_row(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            rows = parse_manifest(self.fixture(directory, self.valid_rows()), stale_after_days=10000)
            prior = root / 'prior.csv'
            write_csv(rows, prior)
            fallback = carry_forward(prior, retrieved_at='2026-08-24T01:00:00+00:00')
            self.assertEqual(len(fallback), 1)
            self.assertEqual(fallback[0]['availability_status'], 'STALE')
            typed = dict(fallback[0])
            for field in ('fiscal_year',):
                typed[field] = int(typed[field])
            for field in ('gross_interest_expense_usd', 'total_receipts_usd', 'interest_expense_to_revenue_pct'):
                typed[field] = float(typed[field])
            validate(typed, SCHEMA)

    def test_cli_blocked_fallback_and_recovery(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / 'out.csv'
            missing = root / 'missing.json'
            command = [sys.executable, str(ROOT / 'parser.py'), '--manifest', str(missing), '--output', str(output)]
            blocked = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(blocked.returncode, 0)
            status = output.with_suffix('.status.json')
            self.assertEqual(json.loads(status.read_text())['status'], 'BLOCKED')
            manifest = self.fixture(directory, self.valid_rows())
            recovered = subprocess.run([sys.executable, str(ROOT / 'parser.py'), '--manifest', str(manifest), '--output', str(output)], capture_output=True, text=True, check=False)
            self.assertEqual(recovered.returncode, 0)
            self.assertTrue(output.exists())
            self.assertFalse(status.exists())
            stale = root / 'stale.csv'
            fallback = subprocess.run([sys.executable, str(ROOT / 'parser.py'), '--manifest', str(missing), '--prior', str(output), '--output', str(stale)], capture_output=True, text=True, check=False)
            self.assertEqual(fallback.returncode, 0)
            with stale.open(newline='', encoding='utf-8') as handle:
                result = list(csv.DictReader(handle))
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['availability_status'], 'STALE')

    def test_unchanged_replay_is_identical(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = self.fixture(directory, self.valid_rows())
            self.assertEqual(parse_manifest(manifest), parse_manifest(manifest))
if __name__ == '__main__':
    unittest.main()
