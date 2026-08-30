import importlib.util
from pathlib import Path
import pytest
MODULE = Path(__file__).parents[1] / 'collector.py'
spec = importlib.util.spec_from_file_location('l10_001_collector', MODULE)
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)

def make_row(code='088691', market='GOLD - COMMODITY EXCHANGE INC.', fut='FutOnly', missing=False):
    fields = ['0'] * 191
    fields[0] = market
    fields[2] = '2026-08-18'
    fields[3] = code
    fields[7] = '406260'
    fields[13] = '154595' if not missing else '.'
    fields[14] = '12947'
    fields[15] = '15591'
    fields[185] = 'CONTRACTS OF 100 TROY OUNCES'
    fields[190] = fut
    return fields

def test_extracts_locked_gold_contract():
    rows = collector.extract_gold_rows(','.join(make_row()), raw_metadata='a' * 64, raw_path='raw.txt', retrieved_at='2026-08-21T00:00:00+00:00')
    assert rows[0]['managed_money_long'] == 154595
    assert rows[0]['managed_money_short'] == 12947

def test_ignores_other_contracts():
    text = ','.join(make_row(code='000001')) + '\n' + ','.join(make_row())
    assert len(collector.extract_gold_rows(text, raw_metadata='a' * 64, raw_path='raw.txt', retrieved_at='2026-08-21T00:00:00+00:00')) == 1

def test_rejects_wrong_layout():
    with pytest.raises(ValueError, match='191 fields'):
        collector.extract_gold_rows(','.join(['x'] * 190), raw_metadata='a' * 64, raw_path='raw.txt', retrieved_at='2026-08-21T00:00:00+00:00')

def test_rejects_missing_required_gold_field():
    with pytest.raises(ValueError, match='missing required'):
        collector.extract_gold_rows(','.join(make_row(missing=True)), raw_metadata='a' * 64, raw_path='raw.txt', retrieved_at='2026-08-21T00:00:00+00:00')

def test_rejects_conflicting_duplicate_report_date():
    first = make_row()
    second = make_row()
    second[13] = '154000'
    with pytest.raises(ValueError, match='conflicting duplicate'):
        collector.extract_gold_rows(','.join(first) + '\n' + ','.join(second), raw_metadata='a' * 64, raw_path='raw.txt', retrieved_at='2026-08-21T00:00:00+00:00')
