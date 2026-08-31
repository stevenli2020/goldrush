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
SPEC = importlib.util.spec_from_file_location('l3_006_parser', PARSER_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
extract_statement, parse_statement = (MODULE.extract_statement, MODULE.parse_statement)
write_csv, = (MODULE.write_csv,)
HTML = "<html><body><div id='article'>\n<p class='releaseTime'>For release at 2:00 p.m. EDT</p>\n<p>The Federal Open Market Committee approved the following statement for release:</p>\n<p>The Committee decided to maintain the target range for the federal funds rate at 3-1/2 to 3-3/4 percent.</p>\n<p>Inflation remains elevated relative to the Committee's 2 percent goal.</p>\n<p>For media inquiries, please email test@example.com.</p>\n</div></body></html>"

class StatementParserTests(unittest.TestCase):

    def materials(self, directory, html=HTML, release='2026-07-29'):
        root = Path(directory)
        html_path = root / 'statement.html'
        html_path.write_text(html, encoding='utf-8')
        pdf_path = root / 'statement.pdf'
        pdf_path.write_bytes(b'%PDF-1.4 test')
        manifests = []
        for kind, raw, url in [('statement_html', html_path, 'https://www.federalreserve.gov/newsevents/pressreleases/monetary20260729a.htm'), ('statement_pdf', pdf_path, 'https://www.federalreserve.gov/monetarypolicy/files/monetary20260729a1.pdf')]:
            path = root / f'{kind}.json'
            path.write_text(json.dumps({'document_type': kind, 'release_date': release, 'meeting_date': release, 'retrieved_at': '2026-08-24T00:00:00+00:00', 'source_url': url, 'raw_path': str(raw)}), encoding='utf-8')
            manifests.append(path)
        return (manifests, html_path)

    def test_statement_text_target_range_is_unclassified(self):
        with tempfile.TemporaryDirectory() as directory:
            manifests, _ = self.materials(directory)
            row = parse_statement(*manifests)[0]
            self.assertEqual((row['target_range_lower_percent'], row['target_range_upper_percent']), (3.5, 3.75))
            self.assertEqual(row['guidance_signal'], 'UNCLASSIFIED')
            self.assertNotIn('media inquiries', row['statement_text'].lower())

    def test_missing_annotation_is_unclassified_without_forcing_signal(self):
        with tempfile.TemporaryDirectory() as directory:
            manifests, _ = self.materials(directory)
            self.assertEqual(parse_statement(*manifests)[0]['guidance_signal'], 'UNCLASSIFIED')

    def test_different_html_wrapper_preserves_statement_extraction(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = root / 'original'
            wrapped = root / 'wrapped'
            original.mkdir()
            wrapped.mkdir()
            self.materials(original)
            changed_wrapper = HTML.replace('<body>', '<body><script>volatile-token-2</script>')
            manifests, _ = self.materials(wrapped, changed_wrapper)
            row = parse_statement(*manifests)[0]
            self.assertEqual(row['guidance_signal'], 'UNCLASSIFIED')

    def test_changed_statement_text_remains_unclassified(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = root / 'original'
            changed = root / 'changed'
            original.mkdir()
            changed.mkdir()
            self.materials(original)
            changed_html = HTML.replace('Inflation remains elevated', 'Inflation has moderated')
            manifests, _ = self.materials(changed, changed_html)
            row = parse_statement(*manifests)[0]
            self.assertEqual(row['guidance_signal'], 'UNCLASSIFIED')
            self.assertIn('Inflation has moderated', row['statement_text'])

    def test_schema_and_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            manifests, _ = self.materials(directory)
            row = parse_statement(*manifests)[0]
            schema = json.loads((Path(__file__).parents[1] / 'schema.json').read_text())
            validate(row, schema)

    def test_duplicate_release_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            manifests, _ = self.materials(directory)
            row = parse_statement(*manifests)[0]
            with self.assertRaises(ValueError):
                write_csv([row, row], Path(directory) / 'out.csv')

    def test_malformed_document_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            manifests, _ = self.materials(directory, '<html><body>wrong</body></html>')
            with self.assertRaises(ValueError):
                parse_statement(*manifests)

    def test_stale_behavior(self):
        with tempfile.TemporaryDirectory() as directory:
            manifests, _ = self.materials(directory, release='2020-07-29')
            self.assertEqual(parse_statement(*manifests)[0]['availability_status'], 'STALE')

    def test_cli_blocked_recovery_and_prior_stale(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / 'out.csv'
            script = Path(__file__).parents[1] / 'parser.py'
            result = subprocess.run([sys.executable, str(script), '--output', str(output)], check=False)
            self.assertEqual(result.returncode, 0)
            self.assertTrue(output.with_suffix('.status.json').exists())
            status = json.loads(output.with_suffix('.status.json').read_text(encoding='utf-8'))
            self.assertIn('both statement manifests are required', status['reason'])
            self.assertIn('no prior valid statement exists', status['fallback_reason'])
            manifests, _ = self.materials(directory)
            rows = parse_statement(*manifests)
            write_csv(rows, output)
            self.assertFalse(output.with_suffix('.status.json').exists())
            bad = root / 'bad.json'
            bad.write_text('{}', encoding='utf-8')
            result = subprocess.run([sys.executable, str(script), '--html-manifest', str(bad), '--pdf-manifest', str(bad), '--prior', str(output), '--output', str(output)], check=False)
            self.assertEqual(result.returncode, 0)
            with output.open(newline='', encoding='utf-8') as handle:
                self.assertEqual(next(csv.DictReader(handle))['availability_status'], 'STALE')
if __name__ == '__main__':
    unittest.main()
