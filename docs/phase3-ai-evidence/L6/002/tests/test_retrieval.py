import importlib.util
import json
from pathlib import Path


spec = importlib.util.spec_from_file_location('l6_002_retrieval', Path(__file__).parents[1] / 'retrieval.py')
retrieval = importlib.util.module_from_spec(spec)
spec.loader.exec_module(retrieval)


class Response:
    def __init__(self, url, status_code=200, text='', content_type='text/html'):
        self.url = url
        self.status_code = status_code
        self.text = text
        self.content = text.encode()
        self.headers = {'content-type': content_type}

    def json(self):
        return {'results': [{'html_url': 'https://www.federalregister.gov/documents/2026/example'}]}


class Session:
    def __init__(self, responses):
        self.responses = responses

    def get(self, url, **kwargs):
        if url.endswith('/robots.txt'):
            return Response(url, text='User-agent: *\nAllow: /')
        return self.responses.pop(0)


def event():
    return {'ofac_entity_id': '1', 'publication_date': '2026-08-20', 'target_name': 'Central Bank of Example', 'official_names': json.dumps([{'value': 'Central Bank of Example'}, {'value': 'Example Reserve Bank'}]), 'legal_authorities_raw': 'Executive Order 14024'}


def test_recent_action_link_matches_entity_name():
    html = '<article><a href="/recent-actions/example">Central Bank of Example action</a></article>'
    assert retrieval.recent_action_links(html, ['Central Bank of Example'], '2026-08-20') == ['https://ofac.treasury.gov/recent-actions/example']


def test_legal_authority_query_uses_executive_order_number_when_present():
    assert retrieval.legal_authority_query('Executive Order 14024 (Russia)') == 'E.O. 14024'


def test_primary_document_must_identify_an_official_name_and_not_be_an_access_page():
    names = ['Central Bank of Example', 'Example Reserve Bank']
    assert retrieval.matching_official_name('Official notice for Example Reserve Bank', names) == 'Example Reserve Bank'
    assert retrieval.matching_official_name('Federal Register :: Request Access Central Bank of Example', names) is None
    assert retrieval.matching_official_name('Official notice for a different entity', names) is None


def test_recent_action_links_prioritise_dates_without_excluding_undated_matches():
    html = '<li>08/19/2026 <a href="/recent-actions/old">Central Bank of Example</a></li><li>08/20/2026 <a href="/recent-actions/same">Central Bank of Example</a></li>'
    assert retrieval.recent_action_links(html, ['Central Bank of Example'], '2026-08-20') == ['https://ofac.treasury.gov/recent-actions/same', 'https://ofac.treasury.gov/recent-actions/old']


def test_dated_recent_action_url_uses_publication_date():
    assert retrieval.dated_recent_action_url('2026-08-20') == 'https://ofac.treasury.gov/recent-actions/20260820'


def test_retrieve_uses_dated_ofac_document_and_records_attempts():
    session = Session([
        Response(retrieval.dated_recent_action_url('2026-08-20'), text='<h1>Official notice</h1><p>Central Bank of Example</p>'),
    ])
    record = retrieval.retrieve_event(event(), session)
    assert record['retrieval_status'] == 'FOUND'
    assert record['primary_document_url'].endswith('/20260820')
    assert 'Official notice' in record['primary_document_text']
    assert len(record['retrieval_attempts']) == 1


def test_retrieve_records_not_found_after_federal_register_fallback():
    session = Session([
        Response(retrieval.dated_recent_action_url('2026-08-20'), status_code=404),
        Response(retrieval.RECENT_ACTIONS_URL, text='<article>no matching action</article>'),
        Response(retrieval.FEDERAL_REGISTER_API, content_type='application/json'),
        Response('https://www.federalregister.gov/documents/2026/example', status_code=404),
    ])
    record = retrieval.retrieve_event(event(), session)
    assert record['retrieval_status'] == 'NOT_FOUND'
    assert record['primary_document_text'] is None
    assert record['retrieval_attempts'][-1]['status'] == 404
