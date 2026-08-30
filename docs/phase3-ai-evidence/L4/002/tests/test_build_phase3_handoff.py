import csv, importlib.util
from pathlib import Path
ROOT = Path(__file__).parents[5]
spec = importlib.util.spec_from_file_location('handoff', ROOT/'docs/phase3-ai-evidence/L4/002/scripts/build_phase3_handoff.py'); module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

def test_builds_handoff(tmp_path):
    p=tmp_path/'rows.csv'; fields=sorted(module.REQUIRED)
    with p.open('w', newline='') as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerow({'variable_id':'L4-002','observation_date':'2026-06-01','value':'130.266','unit':'index','raw_file_path':'raw.json','retrieved_at':'now','validation_status':'PASS','availability_status':'AVAILABLE'})
    row=module.build(p,'FRED PCEPILFE manifest')[0]; assert row['value']==130.266; assert row['unit_or_scale']=='index'

def test_rejects_invalid_row(tmp_path):
    p=tmp_path/'rows.csv'; p.write_text('variable_id,observation_date,value,unit,raw_file_path,retrieved_at,validation_status,availability_status\nL4-002,2026-06-01,130.266,index,raw,now,FLAG,AVAILABLE\n')
    try: module.build(p,'source')
    except ValueError: pass
    else: raise AssertionError('expected invalid row rejection')
