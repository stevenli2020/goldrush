import csv, importlib.util
from pathlib import Path
ROOT=Path(__file__).parents[5]
spec=importlib.util.spec_from_file_location('handoff',ROOT/'docs/phase3-ai-evidence/L10/001/scripts/build_phase3_handoff.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def test_builds_handoff(tmp_path):
 p=tmp_path/'x.csv'; f=sorted(m.REQUIRED)
 with p.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=f); w.writeheader(); w.writerow({'variable_id':'L10-001','observation_date':'2026-08-25','value':'100','managed_money_net_contracts':'100','managed_money_long_contracts':'500','managed_money_short_contracts':'400','open_interest_contracts':'10000','unit':'contracts','source_name':'CFTC','source_series_id':'CFTC_088691_FutOnly','raw_path':'raw','retrieved_at':'now','validation_status':'PASS','availability_status':'AVAILABLE'})
 assert m.build(p,'CFTC manifest')[0]['value']==100
def test_rejects_flag(tmp_path):
 p=tmp_path/'x.csv'; p.write_text('variable_id,observation_date,value,managed_money_net_contracts,managed_money_long_contracts,managed_money_short_contracts,open_interest_contracts,unit,source_name,source_series_id,raw_path,retrieved_at,validation_status,availability_status\nL10-001,2026-08-25,100,100,500,400,10000,contracts,CFTC,CFTC_088691_FutOnly,r,now,FLAG,AVAILABLE\n')
 try: m.build(p,'source')
 except ValueError: pass
 else: raise AssertionError('expected rejection')
