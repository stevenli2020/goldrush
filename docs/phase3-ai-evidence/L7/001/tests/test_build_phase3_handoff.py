import csv, importlib.util
from pathlib import Path
ROOT=Path(__file__).parents[5]
spec=importlib.util.spec_from_file_location('handoff',ROOT/'docs/phase3-ai-evidence/L7/001/scripts/build_phase3_handoff.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def test_builds_handoff(tmp_path):
 p=tmp_path/'x.csv'; f=sorted(m.REQUIRED)
 with p.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=f); w.writeheader(); w.writerow({'variable_id':'L7-001','observation_date':'2026-08-19','fed_total_assets_millions_usd':'6745699','unit':'millions_usd','observation_definition':'Fed total assets','manifest_file_path':'m','validation_status':'PASS','availability_status':'AVAILABLE'})
 assert m.build(p,'FRED WALCL')[0]['value']==6745699.0
def test_rejects_flag(tmp_path):
 p=tmp_path/'x.csv'; p.write_text('variable_id,observation_date,fed_total_assets_millions_usd,unit,observation_definition,manifest_file_path,validation_status,availability_status\nL7-001,2026-08-19,1,millions_usd,x,m,FLAG,AVAILABLE\n')
 try: m.build(p,'source')
 except ValueError: pass
 else: raise AssertionError('expected rejection')
