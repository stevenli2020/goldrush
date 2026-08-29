import importlib.util
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
    return {'ofac_entity_id': '1', 'publication_date': '2026-08-20', 'target_name': 'Central Bank of Example', 'legal_authorities_raw': 'Executive Order 14024'}


def test_recent_action_link_matches_entity_name():
    html = '<article><a href="/recent-actions/example">Central Bank of Example action</a></article>'
    assert retrieval.recent_action_links(html, 'Central Bank of Example') == ['https://ofac.treasury.gov/recent-actions/example']


def test_legal_authority_query_uses_executive_order_number_when_present():
    assert retrieval.legal_authority_query('Executive Order 14024 (Russia)') == 'E.O. 14024'


def test_primary_document_must_identify_the_entity_and_not_be_an_access_page():
    assert retrieval.is_matching_primary_document('Official notice for Central Bank of Example', 'Central Bank of Example')
    assert not retrieval.is_matching_primary_document('Federal Register :: Request Access Central Bank of Example', 'Central Bank of Example')
    assert not retrieval.is_matching_primary_document('Official notice for a different entity', 'Central Bank of Example')


def test_retrieve_uses_ofac_document_and_records_attempts():
    session = Session([
        Response(retrieval.RECENT_ACTIONS_URL, text='<article><a href="/recent-actions/example">Central Bank of Example action</a></article>'),
        Response('https://ofac.treasury.gov/recent-actions/example', text='<h1>Official notice</h1><p>Central Bank of Example</p>'),
    ])
    record = retrieval.retrieve_event(event(), session)
    assert record['retrieval_status'] == 'FOUND'
    assert record['primary_document_url'].endswith('/recent-actions/example')
    assert 'Official notice' in record['primary_document_text']
    assert len(record['retrieval_attempts']) == 2


def test_retrieve_records_not_found_after_federal_register_fallback():
    session = Session([
        Response(retrieval.RECENT_ACTIONS_URL, text='<article>no matching action</article>'),
        Response(retrieval.FEDERAL_REGISTER_API, content_type='application/json'),
        Response('https://www.federalregister.gov/documents/2026/example', status_code=404),
    ])
    record = retrieval.retrieve_event(event(), session)
    assert record['retrieval_status'] == 'NOT_FOUND'
    assert record['primary_document_text'] is None
    assert record['retrieval_attempts'][-1]['status'] == 404
