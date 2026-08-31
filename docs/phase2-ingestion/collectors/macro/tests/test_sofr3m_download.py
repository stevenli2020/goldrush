import importlib.util
import json
from pathlib import Path
import pytest
MODULE_PATH = Path(__file__).parents[1] / 'sofr3m_download.py'
spec = importlib.util.spec_from_file_location('sofr3m_download', MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class Response:
    status = 200
    stdout = b'observation_date,SOFR90DAYAVG\n2026-08-20,3.70\n'

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return b'observation_date,SOFR90DAYAVG\n2026-08-20,3.70\n'

def test_download_normalizes_and_writes_manifest(tmp_path, monkeypatch):
    monkeypatch.setattr(module.subprocess, 'run', lambda *args, **kwargs: Response())
    output = tmp_path / 'sofr3m.csv'
    manifest = tmp_path / 'manifest.json'
    record = module.download(output, manifest)
    assert output.read_text() == 'observation_date,sofr3m_percent\n2026-08-20,3.70\n'
    assert record['source_series'] == 'SOFR90DAYAVG'
    assert json.loads(manifest.read_text())['rows'] == 1

def test_download_rejects_http_error(tmp_path, monkeypatch):

    class BadResponse(Response):
        status = 503
    monkeypatch.setattr(module.subprocess, 'run', lambda *args, **kwargs: (_ for _ in ()).throw(module.subprocess.CalledProcessError(22, 'curl')))
    with pytest.raises(RuntimeError, match='curl'):
        module.download(tmp_path / 'out.csv', tmp_path / 'manifest.json')

def test_download_uses_curl_after_timeout(tmp_path, monkeypatch):

    class CurlResult:
        stdout = b'observation_date,SOFR90DAYAVG\n2026-08-20,3.70\n'
    monkeypatch.setattr(module.subprocess, 'run', lambda *args, **kwargs: CurlResult())
    record = module.download(tmp_path / 'out.csv', tmp_path / 'manifest.json')
    assert record['rows'] == 1
