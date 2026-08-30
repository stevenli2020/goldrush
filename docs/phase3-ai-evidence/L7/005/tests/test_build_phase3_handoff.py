import csv, importlib.util
from pathlib import Path
ROOT=Path(__file__).parents[5]
spec=importlib.util.spec_from_file_location('handoff',ROOT/'docs/phase3-ai-evidence/L7/005/scripts/build_phase3_handoff.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def test_builds_handoff(tmp_path):
 p=tmp_path/'x.csv'; f=sorted(m.REQUIRED)
 with p.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=f); w.writeheader(); w.writerow({'variable_id':'L7-005','observation_date':'2026-08-28','sofr_percent':'4.3','effr_percent':'4.32','repo_funding_stress_bps':'-2','unit':'basis_points','observation_definition':'SOFR-EFFR','source_attribution':'NY Fed via FRED','sofr_manifest_file_path':'s','effr_manifest_file_path':'e','validation_status':'PASS','availability_status':'AVAILABLE'})
 assert m.build(p,'FRED SOFR/EFFR')[0]['value']==-2.0
def test_rejects_flag(tmp_path):
 p=tmp_path/'x.csv'; p.write_text('variable_id,observation_date,sofr_percent,effr_percent,repo_funding_stress_bps,unit,observation_definition,source_attribution,sofr_manifest_file_path,effr_manifest_file_path,validation_status,availability_status\nL7-005,2026-08-28,4,4,0,basis_points,x,x,s,e,FLAG,AVAILABLE\n')
 try: m.build(p,'source')
 except ValueError: pass
 else: raise AssertionError('expected rejection')
