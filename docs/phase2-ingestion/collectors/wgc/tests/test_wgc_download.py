import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from wgc_download import download_target, find_download_url, sha256_bytes, validate_xlsx


class FakeSession:
    def __init__(self, page, workbook):
        self.page = page
        self.workbook = workbook

    def get(self, url, **kwargs):
        if url.endswith("page"):
            return SimpleNamespace(status_code=200, text=self.page, headers={}, content=b"page")
        return SimpleNamespace(status_code=200, text="", headers={"Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "Content-Disposition": 'attachment; filename="sample.xlsx"'}, content=self.workbook)


class DownloaderTests(unittest.TestCase):
    def test_hash_and_xlsx_validation(self):
        response = SimpleNamespace(status_code=200, headers={"Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}, content=b"PK\x03\x04data")
        validate_xlsx(response)
        self.assertEqual(len(sha256_bytes(response.content)), 64)

    def test_url_and_manifest_unchanged_detection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            roots = {"raw": root / "raw", "manifests": root / "manifests", "logs": root / "logs"}
            target = {"page_url": "https://example.test/page", "directory": "gdt", "link_pattern": r'href=["\'](.*?xlsx)["\']'}
            session = FakeSession('<a href="/file.xlsx">x</a>', b"PK\x03\x04data")
            first = download_target(session, "gdt", target, roots)
            second = download_target(session, "gdt", target, roots)
            self.assertTrue(first["changed"])
            self.assertFalse(second["changed"])
            self.assertTrue((root / "raw/gdt/sample.xlsx").exists())
            self.assertEqual(find_download_url('<a href="/file.xlsx">', target["link_pattern"], target["page_url"]), "https://example.test/file.xlsx")


if __name__ == "__main__":
    unittest.main()
