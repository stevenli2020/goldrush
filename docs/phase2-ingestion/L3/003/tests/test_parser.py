import csv
import importlib.util
import subprocess
import sys
from pathlib import Path
MODULE_PATH = Path(__file__).parents[1] / 'parser.py'
spec = importlib.util.spec_from_file_location('l3_003_parser', MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
def curve(tmp_path, rates):
    path = tmp_path / 'curve.csv'
    fields = ['variable_id', 'observation_date', 'contract', 'implied_policy_rate_pct', 'expiry_date', 'curve_position', 'source_url', 'source_pdf_path', 'source_manifest_path', 'retrieved_at', 'validation_status', 'availability_status']
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for position, rate in enumerate(rates, 1):
            writer.writerow({'variable_id': 'L3-002', 'observation_date': '2026-08-20', 'contract': f'ZQF{position:02d}', 'implied_policy_rate_pct': rate, 'expiry_date': f'2027-{min(position, 12):02d}-28', 'curve_position': position, 'source_url': 'url', 'source_pdf_path': 'pdf', 'source_manifest_path': 'manifest', 'retrieved_at': '2026-08-21T00:00:00+00:00', 'validation_status': 'PASS', 'availability_status': 'AVAILABLE'})
    return path

def test_upward_selects_maximum_first_twelve(tmp_path):
    row = module.parse_terminal(curve(tmp_path, [3.0 + i / 10 for i in range(13)]))[0]
    assert row['curve_direction'] == 'upward' and row['expected_terminal_policy_rate_pct'] == 4.1
    assert row['contracts_examined'] == 12 and row['selected_contract'] == 'ZQF12'

def test_downward_selects_minimum(tmp_path):
    row = module.parse_terminal(curve(tmp_path, [4.0, 3.8, 3.9, 3.5]))[0]
    assert row['curve_direction'] == 'downward' and row['expected_terminal_policy_rate_pct'] == 3.5

def test_flat_selects_farthest(tmp_path):
    row = module.parse_terminal(curve(tmp_path, [3.5, 3.4, 3.5]))[0]
    assert row['curve_direction'] == 'flat' and row['selected_contract'] == 'ZQF03'

def test_rejects_mixed_provenance_and_too_short(tmp_path):
    path = curve(tmp_path, [3.5])
    try:
        module.parse_terminal(path)
    except ValueError:
        pass
    else:
        raise AssertionError('single point accepted')
    path = curve(tmp_path, [3.5, 3.6])
    rows = list(csv.DictReader(path.open()))
    rows[1]['source_manifest_path'] = 'different-manifest'
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)
    try:
        module.parse_terminal(path)
    except ValueError as exc:
        assert 'provenance' in str(exc)
    else:
        raise AssertionError('mixed provenance accepted')

def test_revision_is_value_based(tmp_path):
    first = module.parse_terminal(curve(tmp_path, [3.5, 3.6]))
    prior = tmp_path / 'prior.csv'
    module.write_csv(first, prior)
    assert not module.parse_terminal(curve(tmp_path, [3.5, 3.6]), prior)[0]['is_revised']
    changed = module.parse_terminal(curve(tmp_path, [3.5, 3.7]), prior)[0]
    assert changed['is_revised'] and changed['prior_terminal_rate_pct'] == 3.6

def test_blocked_recovery_and_stale_fallback(tmp_path):
    output = tmp_path / 'out.csv'
    missing = tmp_path / 'missing.csv'
    bad = subprocess.run([sys.executable, str(MODULE_PATH), '--curve', str(missing), '--output', str(output)], capture_output=True, text=True)
    assert bad.returncode == 0 and output.with_suffix('.status.json').exists()
    valid = curve(tmp_path, [3.5, 3.6])
    good = subprocess.run([sys.executable, str(MODULE_PATH), '--curve', str(valid), '--output', str(output)], capture_output=True, text=True)
    assert good.returncode == 0 and output.exists() and (not output.with_suffix('.status.json').exists())
    assert module.carry_forward(output)[0]['availability_status'] == 'STALE'
