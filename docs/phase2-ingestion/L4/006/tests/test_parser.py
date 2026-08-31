import csv
import importlib.util
import json
import subprocess
import sys
from datetime import date
from pathlib import Path
import pytest
from jsonschema import FormatChecker, validate
PACKAGE = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location('l4_006_parser', PACKAGE / 'parser.py')
parser = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(parser)
SCHEMA = json.loads((PACKAGE / 'schema.json').read_text(encoding='utf-8'))

def write_inputs(tmp_path, observations, *, series_id='FYFSGDA188S', bad_metadata=False):
    raw = tmp_path / 'raw.json'
    raw.write_text(json.dumps({'observations': observations}), encoding='utf-8')
    metadata = None
    manifest = tmp_path / 'manifest.json'
    manifest.write_text(json.dumps({'series_id': series_id, 'retrieved_at': '2026-08-24T00:00:00+00:00'}), encoding='utf-8')
    return (raw, manifest)

def test_correct_series_unit_and_sign_convention(tmp_path):
    raw, manifest = write_inputs(tmp_path, [{'date': '2024-01-01', 'value': '-6.2'}, {'date': '2025-01-01', 'value': '1.5'}])
    rows = parser.parse_observations(raw, manifest, today=date(2026, 8, 24))
    assert rows[0]['source_series_id'] == 'FYFSGDA188S'
    assert rows[0]['unit'] == 'percent_of_gdp'
    assert rows[0]['fiscal_balance_pct_gdp'] == -6.2
    assert rows[1]['fiscal_balance_pct_gdp'] == 1.5
    assert rows[0]['sign_convention'] == 'negative=deficit; positive=surplus'

def test_missing_marker_and_chronological_order(tmp_path):
    raw, manifest = write_inputs(tmp_path, [{'date': '2025-01-01', 'value': '-5'}, {'date': '2023-01-01', 'value': '.'}, {'date': '2024-01-01', 'value': '-6'}])
    rows = parser.parse_observations(raw, manifest)
    assert [row['observation_year'] for row in rows] == [2024, 2025]

@pytest.mark.parametrize('value', ['bad', 'nan', 'inf'])
def test_invalid_numeric_value(tmp_path, value):
    raw, manifest = write_inputs(tmp_path, [{'date': '2025-01-01', 'value': value}])
    with pytest.raises(ValueError, match='invalid FRED observation'):
        parser.parse_observations(raw, manifest)

def test_conflicting_duplicate_year(tmp_path):
    raw, manifest = write_inputs(tmp_path, [{'date': '2025-01-01', 'value': '-5'}, {'date': '2025-12-31', 'value': '-6'}])
    with pytest.raises(ValueError, match='conflicting duplicate observation year'):
        parser.parse_observations(raw, manifest)

def test_validation_bounds_and_freshness(tmp_path):
    raw, manifest = write_inputs(tmp_path, [{'date': '2024-01-01', 'value': '-31'}, {'date': '2025-01-01', 'value': '11'}])
    rows = parser.parse_observations(raw, manifest, today=date(2026, 8, 24))
    assert {row['validation_status'] for row in rows} == {'FLAG'}
    assert {row['availability_status'] for row in rows} == {'AVAILABLE'}
    stale = parser.parse_observations(raw, manifest, today=date(2027, 5, 1))
    assert {row['availability_status'] for row in stale} == {'STALE'}

def test_canonical_prior_fallback_is_one_schema_valid_stale_row(tmp_path):
    raw, manifest = write_inputs(tmp_path, [{'date': '2024-01-01', 'value': '-6.2'}, {'date': '2025-01-01', 'value': '-5.7'}])
    prior = tmp_path / 'prior.csv'
    parser.write_csv(parser.parse_observations(raw, manifest), prior)
    rows = parser.carry_forward(prior, retrieved_at='2026-08-24T01:00:00+00:00')
    assert len(rows) == 1
    assert rows[0]['observation_year'] == 2025
    assert rows[0]['availability_status'] == 'STALE'
    validate(rows[0], SCHEMA, format_checker=FormatChecker())

def test_blocked_then_successful_recovery(tmp_path):
    output = tmp_path / 'processed' / 'L4_006_observations.csv'
    bad_raw, bad_manifest = write_inputs(tmp_path, [{'date': 'bad', 'value': '-5'}])
    command = [sys.executable, str(PACKAGE / 'parser.py'), '--raw', str(bad_raw), '--manifest', str(bad_manifest), '--output', str(output)]
    blocked = subprocess.run(command, capture_output=True, text=True, check=False)
    status_path = output.with_suffix('.status.json')
    assert blocked.returncode == 0
    assert json.loads(status_path.read_text())['availability_status'] == 'BLOCKED'
    good_raw, good_manifest = write_inputs(tmp_path, [{'date': '2025-01-01', 'value': '-5.7'}])
    recovered = subprocess.run([sys.executable, str(PACKAGE / 'parser.py'), '--raw', str(good_raw), '--manifest', str(good_manifest), '--output', str(output)], capture_output=True, text=True, check=False)
    assert recovered.returncode == 0
    assert output.exists()
    assert not status_path.exists()

def test_cli_failure_with_prior_writes_one_stale_row(tmp_path):
    good_raw, good_manifest = write_inputs(tmp_path, [{'date': '2024-01-01', 'value': '-6.2'}, {'date': '2025-01-01', 'value': '-5.7'}])
    prior = tmp_path / 'prior.csv'
    parser.write_csv(parser.parse_observations(good_raw, good_manifest), prior)
    bad_raw, bad_manifest = write_inputs(tmp_path, [{'date': 'bad', 'value': '-5.7'}])
    output = tmp_path / 'fallback.csv'
    result = subprocess.run([sys.executable, str(PACKAGE / 'parser.py'), '--raw', str(bad_raw), '--manifest', str(bad_manifest), '--prior', str(prior), '--output', str(output)], capture_output=True, text=True, check=False)
    assert result.returncode == 0
    with output.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 1
    assert rows[0]['observation_year'] == '2025'
    assert rows[0]['availability_status'] == 'STALE'
    assert not output.with_suffix('.status.json').exists()

def test_all_parsed_rows_validate_against_schema(tmp_path):
    raw, manifest = write_inputs(tmp_path, [{'date': '2024-01-01', 'value': '-6.2'}, {'date': '2025-01-01', 'value': '-5.7'}])
    for row in parser.parse_observations(raw, manifest):
        validate(row, SCHEMA, format_checker=FormatChecker())
