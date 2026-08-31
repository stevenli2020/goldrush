import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
from parser import parse

def test_formula_provenance_and_freshness(tmp_path):
    p = tmp_path / 'x.csv'
    p.write_text('observation_date,contract,settlement_price,expiry_date\n2026-08-20,ZQU26,96.3675,2026-08-21\n', encoding='utf-8')
    row = parse(p, '2026-08-21T00:00:00+00:00', 'abc')[0]
    assert round(row['value'], 4) == 3.6325
    assert row['availability_status'] == 'AVAILABLE'

def test_stale_and_flag(tmp_path):
    p = tmp_path / 'x.csv'
    p.write_text('observation_date,contract,settlement_price,expiry_date\n2026-08-10,ZQU26,70,2026-08-21\n', encoding='utf-8')
    row = parse(p, '2026-08-21T00:00:00+00:00')[0]
    assert row['availability_status'] == 'STALE' and row['validation_status'] == 'FLAG'

def test_malformed_source_rejected(tmp_path):
    p = tmp_path / 'x.csv'
    p.write_text('date,value\n2026-08-20,3\n', encoding='utf-8')
    try:
        parse(p, '2026-08-21T00:00:00+00:00')
    except ValueError as e:
        assert 'missing required columns' in str(e)
    else:
        raise AssertionError('malformed source was accepted')

def test_ineligible_contract_is_not_selected(tmp_path):
    p = tmp_path / 'x.csv'
    p.write_text('observation_date,contract,settlement_price,expiry_date\n2026-08-20,SOFRU26,96,2026-08-21\n', encoding='utf-8')
    try:
        parse(p, '2026-08-21T00:00:00+00:00')
    except ValueError as e:
        assert 'no eligible' in str(e)
    else:
        raise AssertionError('ineligible contract was accepted')

def test_no_eligible_contract_is_clear_failure(tmp_path):
    p = tmp_path / 'x.csv'
    p.write_text('observation_date,contract,settlement_price,expiry_date\n2026-08-20,ZQU26,96,2026-08-19\n', encoding='utf-8')
    try:
        parse(p, '2026-08-21T00:00:00+00:00')
    except ValueError as e:
        assert 'no eligible' in str(e)
    else:
        raise AssertionError('expired contract was accepted')

def test_duplicate_observation_contract_is_rejected(tmp_path):
    p = tmp_path / 'x.csv'
    p.write_text('observation_date,contract,settlement_price,expiry_date\n2026-08-20,ZQU26,96,2026-08-21\n2026-08-20,ZQU26,96,2026-08-21\n', encoding='utf-8')
    try:
        parse(p, '2026-08-21T00:00:00+00:00')
    except ValueError as e:
        assert 'duplicate' in str(e)
    else:
        raise AssertionError('duplicate row was accepted')
