import csv
import importlib.util
import json
import sys
from pathlib import Path
import jsonschema
import pytest
ROOT = Path(__file__).resolve().parents[1]

def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
collector = load('l7_003_collector', 'collector.py')
parser = load('l7_003_parser', 'parser.py')
HEADER = ['STRUCTURE_ID', 'FREQ', 'BORROWERS_CTY', 'TC_BORROWERS', 'TC_LENDERS', 'VALUATION', 'UNIT_TYPE', 'UNIT_MULT', 'TC_ADJUST', 'TIME_PERIOD', 'OBS_VALUE']

def package(tmp_path, rows, *, dataset=parser.DATASET_ID, key=parser.SERIES_KEY, good_metadata=True):
    tmp_path.mkdir(parents=True, exist_ok=True)
    raw = tmp_path / 'raw.csv'
    with raw.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(rows)
    metadata = None
    manifest = tmp_path / 'manifest.json'
    manifest.write_text(json.dumps({'dataset_id': dataset, 'series_key': key, 'source_url': collector.SOURCE_URL, 'retrieved_at': '2026-08-24T00:00:00+00:00', 'raw_path': str(raw), 'size_bytes': raw.stat().st_size, 'http_status': 200, 'collector_version': collector.COLLECTOR_VERSION}), encoding='utf-8')
    return (raw, manifest)

def row(period, value, **overrides):
    result = {'STRUCTURE_ID': 'BIS:WS_TC(2.0)', 'FREQ': 'Q', 'BORROWERS_CTY': '5A', 'TC_BORROWERS': 'P', 'TC_LENDERS': 'A', 'VALUATION': 'M', 'UNIT_TYPE': 'USD', 'UNIT_MULT': '9', 'TC_ADJUST': 'A', 'TIME_PERIOD': period, 'OBS_VALUE': value}
    result.update(overrides)
    return result

def validate(record):
    schema = json.loads((ROOT / 'schema.json').read_text(encoding='utf-8'))
    jsonschema.validate(record, schema, format_checker=jsonschema.FormatChecker())

def test_valid_parse_missing_growth_order_provenance_and_schema(tmp_path):
    raw, manifest = package(tmp_path, [row('2026-Q1', '110'), row('2025-Q1', '100'), row('2025-Q2', '.')])
    records = parser.parse(raw, manifest, as_of='2026-08-24')
    assert [item['observation_date'] for item in records] == ['2025-03-31', '2026-03-31']
    assert records[0]['credit_growth_yoy_pct'] is None
    assert records[1]['credit_growth_yoy_pct'] == pytest.approx(10)
    validate(records[0])
    validate(records[1])

@pytest.mark.parametrize('bad', [row('2026-13', '100'), row('2026-Q1', 'bad'), row('2026-Q1', '0'), row('2026-Q1', '100', UNIT_TYPE='EUR')])
def test_malformed_nonpositive_and_incompatible_series_rejected(tmp_path, bad):
    raw, manifest = package(tmp_path, [bad])
    with pytest.raises(ValueError):
        parser.parse(raw, manifest)

def test_flag_current_and_stale(tmp_path):
    raw, manifest = package(tmp_path, [row('2025-Q1', '100'), row('2026-Q1', '140')])
    current = parser.parse(raw, manifest, as_of='2026-08-24')
    assert current[-1]['validation_status'] == 'FLAG'
    assert current[-1]['availability_status'] == 'AVAILABLE'
    assert parser.parse(raw, manifest, as_of='2027-02-01')[-1]['availability_status'] == 'STALE'

def test_collector_preserves_bytes_and_manifest(tmp_path):
    data = (','.join(HEADER) + '\n').encode()

    class Response:
        status_code = 200
        content = data

    class Session:

        def get(self, *args, **kwargs):
            return Response()
    result = collector.collect(tmp_path / 'raw', tmp_path / 'manifests', session=Session())
    assert Path(result['raw_path']).read_bytes() == data
    assert result['size_bytes'] == len(data)

@pytest.mark.parametrize('retrieved', [None, 'not-a-timestamp', '2026-08-24T00:00:00'])
def test_manifest_retrieved_at_is_required_and_controlled(tmp_path, retrieved):
    raw, manifest = package(tmp_path, [row('2026-Q1', '100')])
    metadata = json.loads(manifest.read_text())
    if retrieved is None:
        metadata.pop('retrieved_at')
    else:
        metadata['retrieved_at'] = retrieved
    manifest.write_text(json.dumps(metadata))
    with pytest.raises(ValueError, match='retrieved_at'):
        parser.parse(raw, manifest)

def test_unit_multiplier_nine_is_required(tmp_path):
    raw, manifest = package(tmp_path, [row('2026-Q1', '100', UNIT_MULT='6')])
    with pytest.raises(ValueError, match='no BIS'):
        parser.parse(raw, manifest)

def test_malformed_manifest_falls_back_and_prior_identity_is_checked(tmp_path, monkeypatch):
    raw, manifest = package(tmp_path, [row('2025-Q1', '100'), row('2026-Q1', '110')])
    prior = tmp_path / 'prior.csv'
    parser.write_csv(parser.parse(raw, manifest, as_of='2026-08-24'), prior)
    metadata = json.loads(manifest.read_text())
    metadata['retrieved_at'] = 'bad'
    manifest.write_text(json.dumps(metadata))
    output = tmp_path / 'fallback.csv'
    monkeypatch.setattr(sys, 'argv', ['parser.py', '--raw', str(raw), '--manifest', str(manifest), '--prior', str(prior), '--output', str(output)])
    assert parser.main() == 0
    with output.open(newline='', encoding='utf-8') as handle:
        assert next(csv.DictReader(handle))['availability_status'] == 'STALE'
    rows = list(csv.DictReader(prior.open(newline='', encoding='utf-8')))
    rows[0]['source_series_key'] = 'WRONG'
    with prior.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=parser.FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError, match='identity'):
        parser.carry_forward(prior)

def test_cli_fallback_blocked_and_recovery(tmp_path, monkeypatch):
    raw, manifest = package(tmp_path, [row('2025-Q1', '100'), row('2026-Q1', '110')])
    prior = tmp_path / 'prior.csv'
    parser.write_csv(parser.parse(raw, manifest, as_of='2026-08-24'), prior)
    output = tmp_path / 'out.csv'
    monkeypatch.setattr(sys, 'argv', ['parser.py', '--raw', 'missing', '--manifest', 'missing', '--prior', str(prior), '--output', str(output)])
    assert parser.main() == 0
    with output.open(newline='', encoding='utf-8') as handle:
        fallback = next(csv.DictReader(handle))
    assert fallback['availability_status'] == 'STALE'
    validate({**fallback, 'private_nonfinancial_credit_usd_billions': float(fallback['private_nonfinancial_credit_usd_billions']), 'credit_growth_yoy_pct': float(fallback['credit_growth_yoy_pct'])})
    output.unlink()
    monkeypatch.setattr(sys, 'argv', ['parser.py', '--raw', 'missing', '--manifest', 'missing', '--output', str(output)])
    assert parser.main() == 0 and output.with_suffix('.status.json').exists()
    assert json.loads(output.with_suffix('.status.json').read_text())['status'] == 'BLOCKED'
    monkeypatch.setattr(sys, 'argv', ['parser.py', '--raw', str(raw), '--manifest', str(manifest), '--as-of', '2026-08-24', '--output', str(output)])
    assert parser.main() == 0 and output.exists() and (not output.with_suffix('.status.json').exists())
