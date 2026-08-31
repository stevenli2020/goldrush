import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
from parser import parse

def test_forward_minus_sofr(tmp_path):
    cme = tmp_path / 'cme.csv'
    cme.write_text('observation_date,near_settlement,far_settlement,days\n2026-08-20,4500,4545,90\n', encoding='utf-8')
    sofr = tmp_path / 'sofr.csv'
    sofr.write_text('observation_date,sofr3m_percent\n2026-08-20,4.2\n', encoding='utf-8')
    row = parse(cme, sofr)[0]
    assert row['variable_id'] == 'L0-009'
    assert row['validation_status'] == 'PASS'

def test_missing_overlap_fails(tmp_path):
    cme = tmp_path / 'cme.csv'
    cme.write_text('observation_date,near_settlement,far_settlement,days\n2026-08-20,4500,4545,90\n', encoding='utf-8')
    sofr = tmp_path / 'sofr.csv'
    sofr.write_text('observation_date,sofr3m_percent\n2026-08-19,4.2\n', encoding='utf-8')
    try:
        parse(cme, sofr)
    except ValueError as exc:
        assert 'overlapping' in str(exc)
    else:
        raise AssertionError('missing overlap was accepted')
