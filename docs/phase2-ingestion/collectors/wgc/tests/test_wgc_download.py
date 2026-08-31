import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from wgc_download import download_target, find_download_url, validate_xlsx

class FakeSession:

    def __init__(self, page, workbook):
        self.page = page
        self.workbook = workbook

    def get(self, url, **kwargs):
        if url.endswith('page'):
            return SimpleNamespace(status_code=200, text=self.page, headers={}, content=b'page')
        return SimpleNamespace(status_code=200, text='', headers={'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'Content-Disposition': 'attachment; filename="sample.xlsx"'}, content=self.workbook)

class DownloaderTests(unittest.TestCase):

    def test_url_and_manifest_unchanged_detection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            roots = {'raw': root / 'raw', 'manifests': root / 'manifests', 'logs': root / 'logs'}
            target = {'page_url': 'https://example.test/page', 'directory': 'gdt', 'link_pattern': 'href=["\\\'](.*?xlsx)["\\\']'}
            session = FakeSession('<a href="/file.xlsx">x</a>', b'PK\x03\x04data')
            first = download_target(session, 'gdt', target, roots)
            second = download_target(session, 'gdt', target, roots)
            self.assertTrue(first['changed'])
            self.assertFalse(second['changed'])
            self.assertTrue((root / 'raw/gdt/sample.xlsx').exists())
            self.assertEqual(first['target'], 'gdt')
            manifest = json.loads(Path(first['manifest_path']).read_text(encoding='utf-8'))
            self.assertEqual(manifest['manifest_path'], first['manifest_path'])
            self.assertEqual(find_download_url('<a href="/file.xlsx">', target['link_pattern'], target['page_url']), 'https://example.test/file.xlsx')

    def test_gold_premiums_link_pattern(self):
        import yaml
        config = yaml.safe_load((Path(__file__).parents[1] / 'config.yaml').read_text())
        target = config['targets']['gold_premiums']
        html = '<a href="/download/file/11657/gold-premiums.xlsx">download</a>'
        self.assertEqual(find_download_url(html, target['link_pattern'], target['page_url']), 'https://www.gold.org/download/file/11657/gold-premiums.xlsx')
if __name__ == '__main__':
    unittest.main()
