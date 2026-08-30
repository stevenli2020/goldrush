import importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location('l3_001_parser', Path(__file__).parents[1] / 'parser.py')
parser_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser_module)
parse = parser_module.parse

def test_builds_multi_contract_path(tmp_path):
    source = tmp_path / 'x.csv'
    source.write_text('observation_date,contract,implied_rate_percent,months_ahead,,source_manifest\n2026-08-20,ZQQ26,3.63,1,' + 'a' * 64 + ',manifest.json\n2026-08-20,ZQU26,3.55,3,' + 'a' * 64 + ',manifest.json\n', encoding='utf-8')
    row = parse(source)[0]
    assert row['contracts_used'] == 2
    assert round(row['path_average_percent'], 3) == 3.59

def test_single_contract_does_not_become_l3_path(tmp_path):
    source = tmp_path / 'x.csv'
    source.write_text('observation_date,contract,implied_rate_percent,months_ahead,,source_manifest\n2026-08-20,ZQQ26,3.63,1,' + 'a' * 64 + ',manifest.json\n', encoding='utf-8')
    try:
        parse(source)
    except ValueError as exc:
        assert 'at least two' in str(exc)
    else:
        raise AssertionError('single contract was accepted as a path')
