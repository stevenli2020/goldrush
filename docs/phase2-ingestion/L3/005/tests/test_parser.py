import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from jsonschema import validate
PARSER_PATH = Path(__file__).parents[1] / 'parser.py'
SPEC = importlib.util.spec_from_file_location('l3_005_parser', PARSER_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
parse_sep, write_csv = (MODULE.parse_sep, MODULE.write_csv)
HTML = '<html><body>\n<p>For release at 2:00 p.m., EDT, June 17, 2026</p>\n<h1>Summary of Economic Projections</h1>\n<table><tr><th>Variable</th><th>2026</th><th>2027</th></tr>\n<tr><th>Federal funds rate</th><td>4.0</td><td>3.5</td></tr>\n<tr><th>March projection</th><td>9.9</td><td>9.9</td></tr></table>\n<table><tr><th>Midpoint of target range or target level (Percent)</th><th>2026</th><th>2027</th></tr>\n<tr><th>3.500</th><td>1</td><td>2</td></tr>\n<tr><th>4.000</th><td>2</td><td>1</td></tr>\n<tr><th>4.500</th><td>1</td><td></td></tr></table>\n</body></html>'

class SepParserTests(unittest.TestCase):

    def materials(self, directory, html=HTML, release='2026-06-17'):
        root = Path(directory)
        html_path = root / 'sep.html'
        html_path.write_text(html, encoding='utf-8')
        pdf_path = root / 'sep.pdf'
        pdf_path.write_bytes(b'%PDF-1.4 test')
        manifests = []
        for document_type, raw, url in [('sep_html', html_path, 'https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260617.htm'), ('sep_pdf', pdf_path, 'https://www.federalreserve.gov/monetarypolicy/files/fomcprojtabl20260617.pdf')]:
            manifest = root / f'{document_type}.json'
            manifest.write_text(json.dumps({'document_type': document_type, 'release_date': release, 'meeting_date': release, 'retrieved_at': '2026-08-24T00:00:00+00:00', 'source_url': url, 'raw_path': str(raw)}), encoding='utf-8')
            manifests.append(manifest)
        return manifests

    def test_valid_current_distribution_excludes_prior_projection(self):
        with tempfile.TemporaryDirectory() as directory:
            rows = parse_sep(*self.materials(directory))
            self.assertEqual(len(rows), 5)
            self.assertEqual({r['projection_horizon'] for r in rows}, {'2026', '2027'})
            self.assertNotIn(9.9, {r['median_projected_rate'] for r in rows})
            self.assertEqual({r['validation_status'] for r in rows}, {'PASS'})

    def test_participant_reconciliation_and_median(self):
        with tempfile.TemporaryDirectory() as directory:
            rows = parse_sep(*self.materials(directory))
            totals = {h: sum((r['participant_count'] for r in rows if r['projection_horizon'] == h)) for h in {r['projection_horizon'] for r in rows}}
            self.assertEqual(totals, {'2026': 4, '2027': 3})

    def test_schema_and_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            rows = parse_sep(*self.materials(directory))
            schema = json.loads((Path(__file__).parents[1] / 'schema.json').read_text())
            for row in rows:
                validate(row, schema)

    def test_duplicate_rate_bin_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            bad = HTML.replace('<tr><th>4.500</th>', '<tr><th>4.000</th>')
            with self.assertRaises(ValueError):
                parse_sep(*self.materials(directory, bad))

    def test_invalid_count_and_malformed_table_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                parse_sep(*self.materials(directory, HTML.replace('<td>2</td><td>1</td>', '<td>x</td><td>1</td>')))
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                parse_sep(*self.materials(directory, HTML.replace('<td>1</td><td>2</td>', '<td>1</td>')))

    def test_stale_behavior(self):
        with tempfile.TemporaryDirectory() as directory:
            rows = parse_sep(*self.materials(directory, release='2020-06-17'), stale_after_days=120)
            self.assertEqual({r['availability_status'] for r in rows}, {'STALE'})

    def test_cli_blocked_and_prior_stale(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / 'out.csv'
            script = Path(__file__).parents[1] / 'parser.py'
            result = subprocess.run([sys.executable, str(script), '--output', str(output)], check=False)
            self.assertEqual(result.returncode, 0)
            self.assertTrue(output.with_suffix('.status.json').exists())
            rows = parse_sep(*self.materials(directory))
            write_csv(rows, output)
            self.assertFalse(output.with_suffix('.status.json').exists())
            bad = root / 'bad.json'
            bad.write_text('{}', encoding='utf-8')
            result = subprocess.run([sys.executable, str(script), '--html-manifest', str(bad), '--pdf-manifest', str(bad), '--prior', str(output), '--output', str(output)], check=False)
            self.assertEqual(result.returncode, 0)
            with output.open(newline='', encoding='utf-8') as handle:
                self.assertEqual({r['availability_status'] for r in csv.DictReader(handle)}, {'STALE'})
if __name__ == '__main__':
    unittest.main()
