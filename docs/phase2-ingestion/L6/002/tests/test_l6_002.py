import json, sys, importlib.util
from pathlib import Path
import pytest
spec = importlib.util.spec_from_file_location('l6_002_parser', Path(__file__).parents[1] / 'parser.py')
parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)
spec2 = importlib.util.spec_from_file_location('l6_002_collector', Path(__file__).parents[1] / 'collector.py')
collector = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(collector)
XML = '<?xml version="1.0"?><sanctionsData xmlns="https://www.treasury.gov/ofac/DeltaFile/1.0"><publicationInfo><datePublished>2026-08-20T00:00:00-04:00</datePublished></publicationInfo><entities><entity id="1" action="add"><generalInfo><entityType>Organization</entityType></generalInfo><names><name><isPrimary>true</isPrimary><translations><translation><formattedFullName>Central Bank of Example</formattedFullName></translation></translations></name><name><isPrimary>false</isPrimary><aliasType>A.K.A.</aliasType><translations><translation><formattedFullName>Example Reserve Bank</formattedFullName></translation></translations></name></names><sanctionsTypes><sanctionsType>Block</sanctionsType></sanctionsTypes><legalAuthorities><legalAuthority>Executive Order 14024</legalAuthority></legalAuthorities></entity><entity id="2"><sanctionsPrograms><sanctionsProgram action="add">IRAN</sanctionsProgram></sanctionsPrograms></entity><entity id="3" action="remove"><generalInfo><entityType>Individual</entityType></generalInfo></entity></entities></sanctionsData>'

def fixture(tmp_path):
    raw = tmp_path / 'delta.xml'
    raw.write_text(XML)
    mp = tmp_path / 'm.json'
    m = {'source_url': 'https://example/delta.xml', 'retrieved_at': '2026-08-24T00:00:00+00:00', 'publication_date': '2026-08-20', 'raw_path': str(raw), 'size_bytes': raw.stat().st_size, 'http_status': 200}
    mp.write_text(json.dumps(m))
    return (raw, mp)

def test_namespaced_actions_dates_and_missing_name(tmp_path):
    raw, mp = fixture(tmp_path)
    rows = parser.parse(raw, mp)
    assert [r['action_type'] for r in rows] == ['ADD', 'UPDATE', 'REMOVE']
    assert rows[0]['event_date'] == '2026-08-20'
    assert rows[1]['target_name'] is None
    assert rows[1]['program_tags'] == 'IRAN'

def test_duplicate_and_malformed_xml(tmp_path):
    raw, mp = fixture(tmp_path)
    raw.write_text('<bad>')
    m = json.loads(mp.read_text())
    m['size_bytes'] = raw.stat().st_size
    mp.write_text(json.dumps(m))
    with pytest.raises(ValueError):
        parser.parse(raw, mp)

def test_latest_uses_publish_display_date():
    entries = [{'fileName': 'old_delta.xml', 'downloadLink': 'x', 'publishDisplayDate': '2026-08-01T00:00:00'}, {'fileName': 'new_delta.xml', 'downloadLink': 'y', 'publishDisplayDate': '2026-08-20T00:00:00'}]
    assert collector.select_latest(entries)['fileName'] == 'new_delta.xml'

def test_latest_same_date_uses_numbered_sequence():
    entries = [{'fileName': '2026-05-28_delta.xml', 'downloadLink': 'x', 'publishDisplayDate': '2026-05-28T00:00:00'}, {'fileName': '2026-05-28_delta_2.xml', 'downloadLink': 'y', 'publishDisplayDate': '2026-05-28T00:00:00'}]
    assert collector.select_latest(entries)['fileName'].endswith('_delta_2.xml')

def test_select_entry_uses_exact_archive_filename():
    entries = [{'fileName': '2026-07-14_delta.xml', 'downloadLink': 'x', 'publishDisplayDate': '2026-07-14T00:00:00'}]
    assert collector.select_entry(entries, '2026-07-14_delta.xml')['downloadLink'] == 'x'
    with pytest.raises(ValueError):
        collector.select_entry(entries, 'missing.xml')

def test_api_url_and_namespace_fixture(tmp_path):
    raw, mp = fixture(tmp_path)
    assert 'publication_date' in json.loads(mp.read_text())
    row = parser.parse_xml(raw, '2026-08-20')[0]
    assert row['target_name'] == 'Central Bank of Example'
    assert row['ofac_entity_id'] == '1'
    assert row['sanctions_type'] == 'Block'
    assert row['legal_authorities_raw'] == 'Executive Order 14024'
    assert json.loads(row['official_names']) == [{'value': 'Central Bank of Example', 'is_primary': True, 'alias_type': None}, {'value': 'Example Reserve Bank', 'is_primary': False, 'alias_type': 'A.K.A.'}]
    assert row['is_candidate'] is True
    assert row['matched_term'] == 'Central Bank'

def test_candidate_exclusions_are_metadata_only():
    assert parser.candidate_metadata('Central Bank of Example') == (True, 'Central Bank')
    assert parser.candidate_metadata('Central Bank Commercial PLC') == (False, None)
    assert parser.candidate_metadata(None) == (False, None)
    assert parser.candidate_metadata(['Unrelated name', 'Banco Central de Example']) == (True, 'Banco Central')

def test_archive_sequence():
    assert collector.archive_sequence('2026-05-28_delta.xml') == 1
    assert collector.archive_sequence('2026-05-28_delta_2.xml') == 2

def test_collect_uses_publication_date_and_archive_sequence(tmp_path):
    class Response:
        status_code = 200
        headers = {'content-type': 'application/xml'}
        content = XML.encode()
        def json(self):
            return [{'fileName': '2026-08-20_delta_2.xml', 'downloadLink': 'archive/2026-08-20_delta_2.xml', 'publishDisplayDate': '2026-08-20T00:00:00'}]
    class Session:
        def post(self, *args, **kwargs): return Response()
        def get(self, *args, **kwargs): return Response()
    manifest = collector.collect(tmp_path / 'raw', tmp_path / 'manifests', year=2026, session=Session())
    assert Path(manifest['raw_path']).name == 'L6-002_2026-08-20_2.xml'
    assert manifest['publication_date'] == '2026-08-20'
    assert manifest['archive_sequence'] == 2

def test_no_new_delta_is_empty(tmp_path):
    raw = tmp_path / 'empty.xml'
    raw.write_text('<sanctionsData xmlns="https://www.treasury.gov/ofac/DeltaFile/1.0"><publicationInfo><datePublished>2026-08-20T00:00:00-04:00</datePublished></publicationInfo><entities/></sanctionsData>')
    assert parser.parse_xml(raw, '2026-08-20') == []
