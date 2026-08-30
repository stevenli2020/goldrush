import csv
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
import pytest
from jsonschema import Draft7Validator, FormatChecker
MODULE_PATH = Path(__file__).parents[1] / 'parser.py'
SCHEMA_PATH = Path(__file__).parents[1] / 'schema.json'
spec = importlib.util.spec_from_file_location('l3_004_parser', MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def metadata(path):
    return None

def fixture(tmp_path, state='ok', retrieved_at='2026-08-24T02:00:00+00:00'):
    tmp_path.mkdir(parents=True, exist_ok=True)
    cme = tmp_path / 'cme.json'
    cme.write_text(json.dumps({'tradeDate': '08/21/2026', 'settlements': [{'month': 'SEP 26', 'settle': '96.3250'}, {'month': 'OCT 26', 'settle': '96.2650'}, {'month': 'NOV 26', 'settle': '96.2150'}, {'month': 'DEC 26', 'settle': '96.1400'}]}), encoding='utf-8')
    fred = {}
    for series, value, obs in [('EFFR', '3.63', '2026-08-20'), ('DFEDTARL', '3.50', '2026-08-21'), ('DFEDTARU', '3.75', '2026-08-21')]:
        path = tmp_path / f'{series}.json'
        path.write_text(json.dumps({'observations': [{'date': obs, 'value': value}]}), encoding='utf-8')
        fred[series] = {'series_id': series, 'raw_path': str(path)}
    schedule = tmp_path / 'schedule.json'
    schedule.write_text(json.dumps({'schedule_status': {'state': state}, 'meetings': ['2026-09-16', '2026-10-28', '2026-12-09']}), encoding='utf-8')
    manifest = tmp_path / 'manifest.json'
    manifest.write_text(json.dumps({'variable_id': 'L3-004', 'observation_date': '2026-08-21', 'retrieved_at': retrieved_at, 'cme': {'raw_path': str(cme), 'trade_date': '2026-08-21'}, 'fred': fred, 'schedule': {'raw_path': str(schedule)}, 'package_version': '0.1.3'}), encoding='utf-8')
    return (manifest, cme, schedule)

def test_cumulative_tree_matches_expected_and_schema(tmp_path):
    manifest, _, _ = fixture(tmp_path)
    rows = module.parse_manifest(manifest)
    assert len(rows) == 5 and {row['meeting_date'] for row in rows} == {'2026-09-16', '2026-10-28'}
    for meeting in {'2026-09-16', '2026-10-28'}:
        assert sum((row['probability'] for row in rows if row['meeting_date'] == meeting)) == pytest.approx(1.0)
    assert all((row['observation_date'] == '2026-08-21' and row['effr_observation_date'] == '2026-08-20' for row in rows))
    schema = json.loads(SCHEMA_PATH.read_text())
    validator = Draft7Validator(schema, format_checker=FormatChecker())
    assert not [error for row in rows for error in validator.iter_errors(row)]

def test_convolution_and_adjacent_transition():
    assert module.convolve(module.adjacent_transition(0.4), module.adjacent_transition(0.2)) == pytest.approx({0: 0.48, 1: 0.44, 2: 0.08})

@pytest.mark.parametrize('state,expected', [('ok', 'PASS'), ('expiring', 'FLAG')])
def test_schedule_ok_and_expiring(tmp_path, state, expected):
    manifest, _, _ = fixture(tmp_path, state=state)
    assert {row['validation_status'] for row in module.parse_manifest(manifest)} == {expected}

def test_expired_schedule_blocks_even_with_prior(tmp_path):
    good, _, _ = fixture(tmp_path / 'good')
    prior = tmp_path / 'prior.csv'
    module.write_csv(module.parse_manifest(good), prior)
    expired, _, _ = fixture(tmp_path / 'expired', state='expired')
    output = tmp_path / 'out.csv'
    result = subprocess.run([sys.executable, str(MODULE_PATH), '--manifest', str(expired), '--prior', str(prior), '--output', str(output)], capture_output=True, text=True)
    assert result.returncode == 0 and json.loads(output.with_suffix('.status.json').read_text())['status'] == 'BLOCKED'

def test_unchanged_replay_and_value_revision(tmp_path):
    manifest, cme, _ = fixture(tmp_path)
    first = module.parse_manifest(manifest)
    prior = tmp_path / 'prior.csv'
    module.write_csv(first, prior)
    assert not any((row['is_revision'] for row in module.parse_manifest(manifest, prior)))
    payload = json.loads(cme.read_text())
    payload['settlements'][0]['settle'] = '96.3200'
    cme.write_text(json.dumps(payload))
    record = json.loads(manifest.read_text())
    manifest.write_text(json.dumps(record))
    assert any((row['is_revision'] for row in module.parse_manifest(manifest, prior)))

def test_stale_fallback_blocked_and_recovery(tmp_path):
    manifest, _, _ = fixture(tmp_path)
    output = tmp_path / 'out.csv'
    blocked = subprocess.run([sys.executable, str(MODULE_PATH), '--manifest', str(tmp_path / 'missing.json'), '--output', str(output)], capture_output=True, text=True)
    assert blocked.returncode == 0 and output.with_suffix('.status.json').exists()
    recovered = subprocess.run([sys.executable, str(MODULE_PATH), '--manifest', str(manifest), '--output', str(output)], capture_output=True, text=True)
    assert recovered.returncode == 0 and output.exists() and (not output.with_suffix('.status.json').exists())
    stale = subprocess.run([sys.executable, str(MODULE_PATH), '--manifest', str(tmp_path / 'missing.json'), '--prior', str(output), '--output', str(output)], capture_output=True, text=True)
    assert stale.returncode == 0
    with output.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    assert rows and {row['availability_status'] for row in rows} == {'STALE'}
