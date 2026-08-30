import csv
import importlib.util
from pathlib import Path

ROOT = Path(__file__).parents[5]
SCRIPT = ROOT / 'docs/phase3-ai-evidence/L4/001/scripts/build_phase3_handoff.py'
spec = importlib.util.spec_from_file_location('handoff', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_builds_index_handoff(tmp_path):
    source = tmp_path / 'input.csv'
    with source.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=sorted(module.REQUIRED))
        writer.writeheader()
        writer.writerow({'variable_id': 'L4-001', 'observation_date': '2026-07-01', 'value': '332.813', 'unit': 'index', 'raw_file_path': 'raw.json', 'retrieved_at': '2026-08-29T00:00:00Z', 'validation_status': 'PASS', 'availability_status': 'AVAILABLE'})
    result = module.build(source, 'FRED CPIAUCSL manifest')
    assert result[0]['value'] == 332.813
    assert result[0]['observation_timestamp'] == '2026-07-01T00:00:00Z'


def test_rejects_non_pass(tmp_path):
    source = tmp_path / 'input.csv'
    source.write_text('variable_id,observation_date,value,unit,raw_file_path,retrieved_at,validation_status,availability_status\nL4-001,2026-07-01,332.813,index,raw.json,now,FLAG,AVAILABLE\n')
    try:
        module.build(source, 'source')
    except ValueError as exc:
        assert 'validation failure' in str(exc)
    else:
        raise AssertionError('expected validation failure')
