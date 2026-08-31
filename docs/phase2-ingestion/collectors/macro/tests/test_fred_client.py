import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0, str(Path(__file__).parents[1]))
from fred_client import fetch_series, read_api_key_file, validate_payload

class FakeSession:

    def __init__(self, payload, status_code=200):
        self.content = json.dumps(payload).encode('utf-8')
        self.payload = payload
        self.status_code = status_code

    def get(self, url, **kwargs):
        return SimpleNamespace(status_code=self.status_code, content=self.content, json=lambda: self.payload)

class FredClientTests(unittest.TestCase):

    def test_reads_local_key_file_and_rejects_empty_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'fred_api_key'
            path.write_text(' local-key \n', encoding='utf-8')
            self.assertEqual(read_api_key_file(path), 'local-key')
            path.write_text('\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                read_api_key_file(path)

    def test_preserves_raw_and_skips_unchanged_response(self):
        payload = {'observations': [{'date': '2026-01-01', 'value': '2.1'}]}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            session = FakeSession(payload)
            first = fetch_series('DFII10', 'test-key', root / 'raw', root / 'manifests', session=session)
            second = fetch_series('DFII10', 'test-key', root / 'raw', root / 'manifests', session=session)
            self.assertTrue(first['changed'])
            self.assertFalse(second['changed'])
            self.assertTrue(Path(first['raw_path']).exists())

    def test_http_and_auth_failures(self):
        payload = {'observations': []}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                fetch_series('DFII10', '', root / 'raw', root / 'manifests')
            with self.assertRaises(RuntimeError):
                fetch_series('DFII10', 'test-key', root / 'raw', root / 'manifests', session=FakeSession(payload, 500))
if __name__ == '__main__':
    unittest.main()
