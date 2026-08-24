import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).parents[1]))
from fomc_download import (
    CALENDAR_URL, classify_url, collect, discover_documents, download_document,
    preserve_manual,
)

CALENDAR = b"""<html><body><h2>2026 FOMC Meetings</h2><p>Meeting calendars</p>
<a href='/newsevents/pressreleases/monetary20260729a.htm'>HTML</a>
<a href='/monetarypolicy/files/monetary20260729a1.pdf'>PDF</a>
<a href='/monetarypolicy/fomcprojtabl20260617.htm'>HTML</a>
<a href='/monetarypolicy/files/fomcprojtabl20260617.pdf'>PDF</a>
<a href='https://example.com/bad.htm'>external</a></body></html>"""
STATEMENT = b"<html><body>Federal Open Market Committee approved the following statement target range</body></html>"
SEP = b"<html><body>Summary of Economic Projections Midpoint of target range</body></html>"
PDF = b"%PDF-1.4 test document"


class FakeSession:
    def __init__(self, responses):
        self.responses = responses

    def get(self, url, **kwargs):
        status, content_type, content = self.responses[url]
        return SimpleNamespace(status_code=status, content=content,
                               headers={"content-type": content_type})


class FomcDownloadTests(unittest.TestCase):
    def test_discovery_and_classification(self):
        docs = discover_documents(CALENDAR, date(2026, 6, 1), date(2026, 7, 31))
        self.assertEqual({d["document_type"] for d in docs},
                         {"statement_html", "statement_pdf", "sep_html", "sep_pdf"})
        self.assertEqual(classify_url("https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260617.htm"),
                         ("sep_html", "2026-06-17"))

    def test_preservation_manifest_hash_and_unchanged_skip(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            doc = {"document_type": "statement_html", "release_date": "2026-07-29",
                   "meeting_date": "2026-07-29", "source_url": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20260729a.htm"}
            session = FakeSession({doc["source_url"]: (200, "text/html", STATEMENT)})
            first = download_document(doc, session=session, raw_dir=root / "raw", manifest_dir=root / "manifests")
            second = download_document(doc, session=session, raw_dir=root / "raw", manifest_dir=root / "manifests")
            self.assertTrue(first["changed"])
            self.assertFalse(second["changed"])
            self.assertEqual(len(first["sha256"]), 64)
            self.assertTrue(Path(first["raw_path"]).exists())
            self.assertEqual(json.loads(Path(first["manifest_path"]).read_text())["sha256"], first["sha256"])

    def test_bounded_collection(self):
        urls = {
            CALENDAR_URL: (200, "text/html", CALENDAR),
            "https://www.federalreserve.gov/newsevents/pressreleases/monetary20260729a.htm": (200, "text/html", STATEMENT),
            "https://www.federalreserve.gov/monetarypolicy/files/monetary20260729a1.pdf": (200, "application/pdf", PDF),
        }
        with tempfile.TemporaryDirectory() as directory:
            records = collect(date(2026, 7, 1), date(2026, 7, 31), session=FakeSession(urls),
                              raw_dir=Path(directory) / "raw", manifest_dir=Path(directory) / "manifests")
            self.assertEqual([r["document_type"] for r in records],
                             ["calendar_html", "statement_html", "statement_pdf"])

    def test_invalid_domain_and_http_failure(self):
        with self.assertRaises(ValueError):
            classify_url("https://example.com/monetary20260729a.htm")
        doc = {"document_type": "statement_html", "release_date": "2026-07-29",
               "meeting_date": "2026-07-29", "source_url": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20260729a.htm"}
        with self.assertRaises(RuntimeError):
            download_document(doc, session=FakeSession({doc["source_url"]: (500, "text/html", b"bad")}))

    def test_wrong_content_type_and_malformed_content(self):
        doc = {"document_type": "statement_html", "release_date": "2026-07-29",
               "meeting_date": "2026-07-29", "source_url": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20260729a.htm"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                download_document(doc, session=FakeSession({doc["source_url"]: (200, "application/pdf", PDF)}), raw_dir=root / "raw", manifest_dir=root / "m")
            with self.assertRaises(ValueError):
                download_document(doc, session=FakeSession({doc["source_url"]: (200, "text/html", b"<html>wrong</html>")}), raw_dir=root / "raw", manifest_dir=root / "m")

    def test_manual_file_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manual = root / "statement.html"
            manual.write_bytes(STATEMENT)
            record = preserve_manual(manual, source_url="https://www.federalreserve.gov/newsevents/pressreleases/monetary20260729a.htm",
                                     document_type="statement_html", release_date="2026-07-29",
                                     raw_dir=root / "raw", manifest_dir=root / "manifests")
            self.assertTrue(Path(record["raw_path"]).exists())
            self.assertTrue(Path(record["manifest_path"]).exists())


if __name__ == "__main__":
    unittest.main()
