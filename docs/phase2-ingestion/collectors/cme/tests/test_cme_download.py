import importlib.util
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).parents[1] / 'cme_download.py'
SPEC = importlib.util.spec_from_file_location('cme_download', MODULE_PATH)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class Response:
    def __init__(self, *, status=200, content=b'', text='', content_type='application/pdf'):
        self.status_code = status
        self.content = content
        self.text = text
        self.headers = {'Content-Type': content_type}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f'HTTP {self.status_code}')


class Session:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = 0

    def get(self, *_args, **_kwargs):
        self.calls += 1
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def test_retry_recovers_from_transport_error(monkeypatch):
    monkeypatch.setattr(module.time, 'sleep', lambda _seconds: None)
    session = Session([RuntimeError('reset'), Response()])
    assert module.get_with_retries(session, 'https://www.cmegroup.com/test').status_code == 200
    assert session.calls == 2


def test_discovery_rejects_non_cme_host():
    html = '<a href="https://example.com/Section10_Interest_Rate_Futures_Continued.pdf">x</a>'
    with pytest.raises(ValueError, match='unexpected CME URL'):
        module.discover(Session([Response(text=html, content_type='text/html')]))


def test_identical_pdf_reuses_prior_file_without_hash(tmp_path, monkeypatch):
    raw = tmp_path / 'prior.pdf'
    raw.write_bytes(b'%PDF same')
    manifests = tmp_path / 'manifests'
    manifests.mkdir()
    (manifests / 'section10-20260101T000000Z.json').write_text(
        json_manifest(raw), encoding='utf-8'
    )
    monkeypatch.setattr(module, 'MANIFESTS', manifests)
    monkeypatch.setattr(module, 'RAW_DIRS', {key: tmp_path / 'raw' for key in module.TARGETS})
    response = Response(content=b'%PDF same')
    record = module.download_one(
        Session([response]), 'section10', 'https://www.cmegroup.com/test.pdf', False, False
    )
    assert record['changed'] is False
    assert Path(record['raw_path']) == raw
    assert 'sha256' not in record


def test_metals_sections_have_a_separate_raw_directory():
    assert module.RAW_DIRS['section09'].name == 'interest-rates'
    assert module.RAW_DIRS['section10'].name == 'interest-rates'
    assert module.RAW_DIRS['section62'].name == 'metals'
    assert module.RAW_DIRS['section02b'].name == 'metals'


def test_new_section02b_pdf_is_saved_under_metals(tmp_path, monkeypatch):
    monkeypatch.setattr(module, 'MANIFESTS', tmp_path / 'manifests')
    monkeypatch.setattr(module, 'RAW_DIRS', {
        'section09': tmp_path / 'interest-rates',
        'section10': tmp_path / 'interest-rates',
        'section62': tmp_path / 'metals',
        'section02b': tmp_path / 'metals',
    })
    record = module.download_one(
        Session([Response(content=b'%PDF new')]),
        'section02b',
        'https://www.cmegroup.com/section02b.pdf',
        True,
        False,
    )
    assert record['changed'] is True
    assert Path(record['raw_path']).parent == tmp_path / 'metals'
    assert Path(record['raw_path']).read_bytes() == b'%PDF new'


def json_manifest(raw):
    return '{"target":"section10","raw_path":"' + raw.as_posix() + '"}'
