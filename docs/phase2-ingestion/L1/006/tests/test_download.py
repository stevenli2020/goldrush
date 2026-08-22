import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
import download

class Response:
    status = 200
    headers = {"Content-Type": "text/html"}
    def getcode(self): return self.status
    def read(self): return b"<html>blocked</html>"
    def __enter__(self): return self
    def __exit__(self, *args): pass

def test_downloader_rejects_html(monkeypatch, tmp_path):
    monkeypatch.setattr(download.urllib.request, "urlopen", lambda *args, **kwargs: Response())
    try: download.download(tmp_path, "https://example.invalid")
    except ValueError as e: assert "not a PDF" in str(e)
    else: raise AssertionError("HTML response was saved")
