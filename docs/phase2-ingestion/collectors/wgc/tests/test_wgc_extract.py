import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from wgc_extract import latest_manifests, run_parser

class ExtractTests(unittest.TestCase):

    def test_latest_manifest_selects_newest_per_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for stamp, sha in (('20260820T000000Z', 'old'), ('20260821T000000Z', 'new')):
                (root / f'gdt-{stamp}.json').write_text(json.dumps({'target': 'gdt', 'raw_path': f'{sha}.xlsx', 'downloaded_at': stamp}))
            manifests = latest_manifests(root)
            self.assertEqual(len(manifests), 1)
            self.assertEqual(manifests[0]['raw_path'], 'new.xlsx')

    @patch('wgc_extract.subprocess.run')
    def test_parser_command_replaces_input(self, run):
        run.return_value.returncode = 0
        run.return_value.stdout = 'ok'
        run.return_value.stderr = ''
        result = run_parser({'script': 'parser.py', 'args': ['--input', '{input}', '--manifest', '{manifest}']}, Path('sample.xlsx'), Path('/project'), {'downloaded_at': '2026-08-21T00:00:00+00:00', 'manifest_path': 'manifest.json'})
        self.assertEqual(result['returncode'], 0)
        self.assertEqual(run.call_args.args[0][3], 'sample.xlsx')
        self.assertEqual(run.call_args.args[0][5], 'manifest.json')

    def test_l9_shared_dispatch_failure_uses_prior_stale(self):
        project_root = Path(__file__).resolve().parents[5]
        prior = project_root / 'docs/phase2-ingestion/L9/001/data/processed/L9_001_observations.csv'
        self.assertTrue(prior.exists())
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bad = root / 'missing.xlsx'
            output = root / 'out.csv'
            mapping = {'script': 'docs/phase2-ingestion/L9/001/parser.py', 'args': ['--workbook', '{input}', '--manifest', '{manifest}', '--prior', str(prior), '--output', str(output)]}
            result = run_parser(mapping, bad, project_root, {'manifest_path': str(root / 'missing.json'), 'downloaded_at': '2026-08-24T00:00:00+00:00'})
            self.assertEqual(result['returncode'], 0)
            import csv
            with output.open(newline='') as handle:
                self.assertEqual(next(csv.DictReader(handle))['availability_status'], 'STALE')
if __name__ == '__main__':
    unittest.main()
