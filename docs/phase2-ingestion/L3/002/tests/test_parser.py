import csv
import importlib.util
import json
import pytest
import subprocess
import sys
from pathlib import Path
MODULE_PATH = Path(__file__).parents[1] / 'parser.py'
spec = importlib.util.spec_from_file_location('l3_002_parser', MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def fixture(tmp_path, rows=None, target='section10'):
    pdf = tmp_path / 'section10.pdf'
    pdf.write_bytes(b'%PDF fixture')
    metadata = None
    manifest = tmp_path / 'manifest.json'
    manifest.write_text(json.dumps({'target': target, 'source_url': f'https://example.test/{target}.pdf', 'raw_path': str(pdf), 'retrieved_at': '2026-08-21T00:00:00+00:00', 'observation_date': '2026-08-20'}), encoding='utf-8')
    source = tmp_path / 'settlements.csv'
    rows = rows or [['2026-08-20', 'ZQQ26', '96.3700', '2026-08-31'], ['2026-08-20', 'ZQU26', '96.3300', '2026-09-30']]
    with source.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['observation_date', 'contract', 'settlement_price', 'expiry_date'])
        writer.writerows(rows)
    return (source, manifest, pdf)

@pytest.mark.parametrize('target', ['section09', 'section10'])
def test_supported_manifest_targets_are_accepted(tmp_path, target):
    source, manifest, pdf = fixture(tmp_path, target=target)
    assert len(module.parse_curve(source, manifest, pdf)) == 2

def test_unrelated_manifest_target_is_rejected(tmp_path):
    source, manifest, pdf = fixture(tmp_path, target='section62')
    with pytest.raises(ValueError, match='section09 or section10'):
        module.parse_curve(source, manifest, pdf)

def test_full_curve_formula_and_provenance(tmp_path):
    source, manifest, pdf = fixture(tmp_path)
    rows = module.parse_curve(source, manifest, pdf)
    assert len(rows) == 2 and rows[0]['implied_policy_rate_pct'] == 3.63

def test_malformed_contract_conflict_and_empty_fail(tmp_path):
    for rows in ([['2026-08-20', 'BAD', '96.3', '2026-08-31']], [['2026-08-20', 'ZQQ26', '96.3', '2026-08-31'], ['2026-08-20', 'ZQQ26', '96.4', '2026-08-31']], [['2026-08-20', 'ZQQ26', '96.3', '2026-07-31']]):
        source, manifest, pdf = fixture(tmp_path, rows)
        try:
            module.parse_curve(source, manifest, pdf)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid curve was accepted')

def test_fallback_blocked_and_recovery_cli(tmp_path):
    source, manifest, pdf = fixture(tmp_path)
    output = tmp_path / 'out.csv'
    bad = subprocess.run([sys.executable, str(MODULE_PATH), '--input', str(source), '--manifest', str(manifest), '--source-pdf', str(tmp_path / 'missing.pdf'), '--output', str(output)], capture_output=True, text=True)
    assert bad.returncode == 0 and output.with_suffix('.status.json').exists()
    good = subprocess.run([sys.executable, str(MODULE_PATH), '--input', str(source), '--manifest', str(manifest), '--source-pdf', str(pdf), '--output', str(output)], capture_output=True, text=True)
    assert good.returncode == 0 and output.exists() and (not output.with_suffix('.status.json').exists())
    stale = module.carry_forward(output)
    assert all((row['availability_status'] == 'STALE' for row in stale))

def test_no_prior_carry_forward_fails(tmp_path):
    try:
        module.carry_forward(tmp_path / 'missing.csv')
    except FileNotFoundError:
        pass
    else:
        raise AssertionError('missing prior output accepted')
