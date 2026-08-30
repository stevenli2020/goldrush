import csv, importlib.util
from pathlib import Path
ROOT=Path(__file__).parents[5]
spec=importlib.util.spec_from_file_location('handoff',ROOT/'docs/phase3-ai-evidence/L4/006/scripts/build_phase3_handoff.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def test_builds_handoff(tmp_path):
 p=tmp_path/'x.csv'; f=sorted(m.REQUIRED)
 with p.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=f); w.writeheader(); w.writerow({'variable_id':'L4-006','observation_date':'2025-09-30','fiscal_balance_pct_gdp':'-5.7','unit':'percent_of_gdp','sign_convention':'negative=deficit; positive=surplus','period_definition':'annual','manifest_path':'manifest','validation_status':'PASS','availability_status':'AVAILABLE'})
 assert m.build(p,'FRED FYFSGDA188S')[0]['value']==-5.7
def test_rejects_flag(tmp_path):
 p=tmp_path/'x.csv'; p.write_text('variable_id,observation_date,fiscal_balance_pct_gdp,unit,sign_convention,period_definition,manifest_path,validation_status,availability_status\nL4-006,2025-09-30,-40,percent_of_gdp,s,annual,m,FLAG,AVAILABLE\n')
 try: m.build(p,'source')
 except ValueError: pass
 else: raise AssertionError('expected rejection')
