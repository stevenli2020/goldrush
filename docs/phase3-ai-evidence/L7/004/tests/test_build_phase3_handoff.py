import csv, importlib.util
from pathlib import Path
ROOT=Path(__file__).parents[5]
spec=importlib.util.spec_from_file_location('handoff',ROOT/'docs/phase3-ai-evidence/L7/004/scripts/build_phase3_handoff.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def test_builds_handoff(tmp_path):
 p=tmp_path/'x.csv'; f=sorted(m.REQUIRED)
 with p.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=f); w.writeheader(); w.writerow({'variable_id':'L7-004','observation_date':'2026-08-28','high_yield_oas_pct':'3.1','unit':'percentage_points','observation_definition':'daily close','source_attribution':'ICE via FRED','manifest_file_path':'m','validation_status':'PASS','availability_status':'AVAILABLE'})
 assert m.build(p,'FRED BAMLH0A0HYM2')[0]['value']==3.1
def test_rejects_flag(tmp_path):
 p=tmp_path/'x.csv'; p.write_text('variable_id,observation_date,high_yield_oas_pct,unit,observation_definition,source_attribution,manifest_file_path,validation_status,availability_status\nL7-004,2026-08-28,40,percentage_points,daily,ICE,m,FLAG,AVAILABLE\n')
 try: m.build(p,'source')
 except ValueError: pass
 else: raise AssertionError('expected rejection')
