import csv, importlib.util
from pathlib import Path
ROOT=Path(__file__).parents[5]
spec=importlib.util.spec_from_file_location('handoff',ROOT/'docs/phase3-ai-evidence/L7/003/scripts/build_phase3_handoff.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def test_builds_handoff(tmp_path):
 p=tmp_path/'x.csv'; f=sorted(m.REQUIRED)
 with p.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=f); w.writeheader(); w.writerow({'variable_id':'L7-003','observation_date':'2026-06-30','private_nonfinancial_credit_usd_billions':'1000','credit_growth_yoy_pct':'4.5','unit':'USD_billions','aggregate_id':'5A_ALL_REPORTING_COUNTRIES','source_dataset_id':'BIS:WS_TC(2.0)','source_series_key':'Q.5A.P.A.M.USD.A','manifest_path':'m','validation_status':'PASS','availability_status':'AVAILABLE'})
 assert m.build(p,'BIS WS_TC')[0]['value']==4.5
def test_rejects_flag(tmp_path):
 p=tmp_path/'x.csv'; p.write_text('variable_id,observation_date,private_nonfinancial_credit_usd_billions,credit_growth_yoy_pct,unit,aggregate_id,source_dataset_id,source_series_key,manifest_path,validation_status,availability_status\nL7-003,2026-06-30,1000,40,USD_billions,5A_ALL_REPORTING_COUNTRIES,BIS:WS_TC(2.0),Q.5A.P.A.M.USD.A,m,FLAG,AVAILABLE\n')
 try: m.build(p,'source')
 except ValueError: pass
 else: raise AssertionError('expected rejection')
