import csv, importlib.util
from pathlib import Path
ROOT=Path(__file__).parents[5]
spec=importlib.util.spec_from_file_location('handoff',ROOT/'docs/phase3-ai-evidence/L4/004/scripts/build_phase3_handoff.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def test_builds_handoff(tmp_path):
 p=tmp_path/'x.csv'; f=sorted(m.REQUIRED)
 with p.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=f); w.writeheader(); w.writerow({'variable_id':'L4-004','observation_date':'2026-08-20','value':'2.28','unit':'percent','raw_file_path':'raw','retrieved_at':'now','validation_status':'PASS','availability_status':'AVAILABLE'})
 assert m.build(p,'FRED T10YIE')[0]['value']==2.28
def test_rejects_flag(tmp_path):
 p=tmp_path/'x.csv'; p.write_text('variable_id,observation_date,value,unit,raw_file_path,retrieved_at,validation_status,availability_status\nL4-004,2026-08-20,25,percent,raw,now,FLAG,AVAILABLE\n')
 try: m.build(p,'source')
 except ValueError: pass
 else: raise AssertionError('expected rejection')
