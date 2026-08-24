import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import requests

sys.path.insert(0, str(Path(__file__).parents[1]))
from treasury_api_client import fetch_dataset


class FakeSession:
    def __init__(self, pages=None, status=200, content_type="application/json"):
        self.pages = pages or []
        self.status = status
        self.content_type = content_type
        self.calls = []

    def get(self, url, **kwargs):
        self.calls.append(kwargs)
        page = kwargs["params"]["page[number]"]
        payload = self.pages[page - 1] if self.pages else {"data": [], "meta": {"total-pages": 1}}
        content = json.dumps(payload).encode()
        return SimpleNamespace(status_code=self.status, content=content,
                               headers={"content-type": self.content_type}, json=lambda: payload)


class TreasuryClientTests(unittest.TestCase):
    def test_preserves_response_and_manifest(self):
        pages = [{"data": [{"record_date": "2025-09-30"}], "meta": {"total-pages": 1}}]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = fetch_dataset("https://example.test/table", {"filter": "x:y"},
                                   root / "raw", root / "manifests", session=FakeSession(pages))
            self.assertEqual(result["record_count"], 1)
            self.assertEqual(len(result["source_sha256"]), 64)
            self.assertTrue(Path(result["raw_paths"][0]).exists())
            self.assertTrue(Path(result["manifest_path"]).exists())

    def test_paginates(self):
        pages = [
            {"data": [{"id": 1}], "meta": {"total-pages": 2}},
            {"data": [{"id": 2}], "meta": {"total-pages": 2}},
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            session = FakeSession(pages)
            result = fetch_dataset("https://example.test/table", {}, root / "raw",
                                   root / "manifests", session=session)
            self.assertEqual(result["page_count"], 2)
            self.assertEqual(result["record_count"], 2)
            self.assertEqual(len(session.calls), 2)

    def test_fields_query_is_preserved(self):
        pages = [{"data": [{"record_date": "2025-09-30"}], "meta": {"total-pages": 1}}]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            session = FakeSession(pages)
            fields = "record_date,maturity_date,outstanding_amt"
            result = fetch_dataset("https://example.test/table", {"fields": fields},
                                   root / "raw", root / "manifests", session=session)
            self.assertEqual(session.calls[0]["params"]["fields"], fields)
            self.assertEqual(result["query"]["fields"], fields)

    def test_rejects_http_and_content_failures(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(RuntimeError):
                fetch_dataset("https://example.test/table", {}, root / "raw", root / "m",
                              session=FakeSession(status=404), max_retries=0)
            with self.assertRaises(ValueError):
                fetch_dataset("https://example.test/table", {}, root / "raw", root / "m",
                              session=FakeSession(content_type="text/html"), max_retries=0)
            with self.assertRaises(ValueError):
                fetch_dataset("https://example.test/table", {}, root / "raw", root / "m",
                              session=FakeSession(pages=[{"unexpected": []}]), max_retries=0)

    def test_retries_timeout_and_connection_failures(self):
        payload = {"data": [{"id": 1}], "meta": {"total-pages": 1}}

        class FlakySession:
            def __init__(self):
                self.calls = 0

            def get(self, url, **kwargs):
                self.calls += 1
                if self.calls == 1:
                    raise requests.Timeout("timed out")
                if self.calls == 2:
                    raise requests.ConnectionError("connection failed")
                content = json.dumps(payload).encode()
                return SimpleNamespace(status_code=200, content=content,
                                       headers={"content-type": "application/json"},
                                       json=lambda: payload)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            session = FlakySession()
            result = fetch_dataset("https://example.test/table", {}, root / "raw",
                                   root / "manifests", session=session, max_retries=2)
            self.assertEqual(session.calls, 3)
            self.assertEqual(result["record_count"], 1)


if __name__ == "__main__":
    unittest.main()
