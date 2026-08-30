import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0, str(Path(__file__).parents[1]))
from fomc_download import CALENDAR_URL, classify_url, collect, discover_documents, download_document, preserve_manual
CALENDAR = b"""<html><body><p>Meeting calendars</p>
<div class='panel panel-default'>
  <div class='panel-heading'><h4>2026 FOMC Meetings</h4></div>
  <div class='row fomc-meeting'>
    <div class='fomc-meeting__month'>July</div>
    <div class='fomc-meeting__date'>28-29</div>
    <div><strong>Statement:</strong><br>
      <a href='/monetarypolicy/files/renamed-statement.pdf'>PDF</a> |
      <a href='/newsevents/pressreleases/renamed-statement.html'>HTML</a><br>
      <a href='/newsevents/pressreleases/monetary20260729a1.htm'>Implementation Note</a>
    </div>
  </div>
  <div class='row fomc-meeting'>
    <div class='fomc-meeting__month'>June</div>
    <div class='fomc-meeting__date'>16-17*</div>
    <div><strong>Projection Materials</strong><br>
      <a href='/monetarypolicy/files/renamed-sep.pdf'>PDF</a> |
      <a href='/monetarypolicy/renamed-sep.html'>HTML</a>
    </div>
  </div>
</div>
<a href='https://example.com/bad.htm'>external</a></body></html>"""
STATEMENT = b'<html><body>Federal Open Market Committee approved the following statement target range</body></html>'
SEP = b'<html><body>Summary of Economic Projections Midpoint of target range</body></html>'
PDF = b'%PDF-1.4 test document'

class FakeSession:

    def __init__(self, responses):
        self.responses = responses

    def get(self, url, **kwargs):
        status, content_type, content = self.responses[url]
        return SimpleNamespace(status_code=status, content=content, headers={'content-type': content_type})

class FomcDownloadTests(unittest.TestCase):

    def test_discovery_and_classification(self):
        docs = discover_documents(CALENDAR, date(2026, 6, 1), date(2026, 7, 31))
        self.assertEqual({d['document_type'] for d in docs}, {'statement_html', 'statement_pdf', 'sep_html', 'sep_pdf'})
        self.assertEqual(classify_url('https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260617.htm'), ('sep_html', '2026-06-17'))
        self.assertEqual(classify_url('https://www.federalreserve.gov/newsevents/press/monetary/20080130a.htm'), ('statement_html', '2008-01-30'))

    def test_layout_discovery_is_independent_of_filename(self):
        docs = discover_documents(CALENDAR, date(2026, 7, 1), date(2026, 7, 31))
        urls = {d['source_url'] for d in docs}
        self.assertEqual(urls, {
            'https://www.federalreserve.gov/monetarypolicy/files/renamed-statement.pdf',
            'https://www.federalreserve.gov/newsevents/pressreleases/renamed-statement.html',
        })

    def test_bounded_collection(self):
        urls = {CALENDAR_URL: (200, 'text/html', CALENDAR), 'https://www.federalreserve.gov/newsevents/pressreleases/renamed-statement.html': (200, 'text/html', STATEMENT), 'https://www.federalreserve.gov/monetarypolicy/files/renamed-statement.pdf': (200, 'application/pdf', PDF)}
        with tempfile.TemporaryDirectory() as directory:
            records = collect(date(2026, 7, 1), date(2026, 7, 31), session=FakeSession(urls), raw_dir=Path(directory) / 'raw', manifest_dir=Path(directory) / 'manifests')
            self.assertEqual([r['document_type'] for r in records], ['calendar_html', 'statement_html', 'statement_pdf'])

    def test_invalid_domain_and_http_failure(self):
        with self.assertRaises(ValueError):
            classify_url('https://example.com/monetary20260729a.htm')
        doc = {'document_type': 'statement_html', 'release_date': '2026-07-29', 'meeting_date': '2026-07-29', 'source_url': 'https://www.federalreserve.gov/newsevents/pressreleases/monetary20260729a.htm'}
        with self.assertRaises(RuntimeError):
            download_document(doc, session=FakeSession({doc['source_url']: (500, 'text/html', b'bad')}))

    def test_wrong_content_type_and_malformed_content(self):
        doc = {'document_type': 'statement_html', 'release_date': '2026-07-29', 'meeting_date': '2026-07-29', 'source_url': 'https://www.federalreserve.gov/newsevents/pressreleases/monetary20260729a.htm'}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                download_document(doc, session=FakeSession({doc['source_url']: (200, 'application/pdf', PDF)}), raw_dir=root / 'raw', manifest_dir=root / 'm')
            with self.assertRaises(ValueError):
                download_document(doc, session=FakeSession({doc['source_url']: (200, 'text/html', b'<html>wrong</html>')}), raw_dir=root / 'raw', manifest_dir=root / 'm')

    def test_manual_file_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manual = root / 'statement.html'
            manual.write_bytes(STATEMENT)
            record = preserve_manual(manual, source_url='https://www.federalreserve.gov/newsevents/pressreleases/monetary20260729a.htm', document_type='statement_html', release_date='2026-07-29', raw_dir=root / 'raw', manifest_dir=root / 'manifests')
            self.assertTrue(Path(record['raw_path']).exists())
            self.assertTrue(Path(record['manifest_path']).exists())
if __name__ == '__main__':
    unittest.main()
