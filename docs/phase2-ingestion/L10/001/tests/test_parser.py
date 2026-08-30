import csv
import importlib.util
from pathlib import Path
MODULE = Path(__file__).parents[1] / 'parser.py'
spec = importlib.util.spec_from_file_location('l10_001_parser', MODULE)
parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)

def source_file(tmp_path, report_date='2026-08-18', long='154595', short='12947'):
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / 'source.csv'
    fields = {'report_date': report_date, 'market_name': 'GOLD - COMMODITY EXCHANGE INC.', 'cftc_contract_market_code': '088691', 'open_interest': '406260', 'managed_money_long': long, 'managed_money_short': short, 'managed_money_spreading': '15591', 'contract_units': 'CONTRACTS OF 100 TROY OUNCES', 'fut_only_or_combined': 'FutOnly', 'raw_path': 'raw.txt', 'retrieved_at': '2026-08-21T00:00:00+00:00'}
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields))
        writer.writeheader()
        writer.writerow(fields)
    return path

def test_net_calculation_and_available_status(tmp_path):
    row = parser.parse(source_file(tmp_path), as_of='2026-08-20')[0]
    assert row['value'] == 141648
    assert row['validation_status'] == 'PASS'
    assert row['availability_status'] == 'AVAILABLE'

def test_stale_uses_report_date_not_retrieval_time(tmp_path):
    row = parser.parse(source_file(tmp_path, report_date='2026-08-01'), as_of='2026-08-22')[0]
    assert row['availability_status'] == 'STALE'

def test_revision_is_recorded(tmp_path):
    source = source_file(tmp_path)
    prior = source_file(tmp_path / 'prior')
    with prior.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    rows[0]['managed_money_long'] = '154000'
    with prior.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    assert parser.parse(source, as_of='2026-08-20', prior=prior)[0]['is_revision'] is True

def test_unchanged_processed_prior_is_not_revision(tmp_path):
    source = source_file(tmp_path)
    prior = tmp_path / 'prior.csv'
    current = parser.parse(source, as_of='2026-08-20')
    with prior.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(current[0]))
        writer.writeheader()
        writer.writerows(current)
    assert parser.parse(source, as_of='2026-08-20', prior=prior)[0]['is_revision'] is False
