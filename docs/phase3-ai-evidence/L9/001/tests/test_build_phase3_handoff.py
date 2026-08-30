import csv, importlib.util
from pathlib import Path
ROOT=Path(__file__).parents[5]
spec=importlib.util.spec_from_file_location('handoff',ROOT/'docs/phase3-ai-evidence/L9/001/scripts/build_phase3_handoff.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def test_builds_handoff(tmp_path):
 p=tmp_path/'x.csv'; f=sorted(m.REQUIRED)
 with p.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=f); w.writeheader(); w.writerow({'variable_id':'L9-001','observation_date':'2026-08-20','premium_discount_usd_per_oz':'12.5','unit':'usd_per_troy_ounce','value_definition':'WGC theoretical difference','smoothing_method':'5-day moving average as published by WGC','source_workbook':'gold-premiums.xlsx','manifest_path':'m','validation_status':'PASS','availability_status':'AVAILABLE'})
 assert m.build(p,'WGC premiums')[0]['value']==12.5
def test_rejects_flag(tmp_path):
 p=tmp_path/'x.csv'; p.write_text('variable_id,observation_date,premium_discount_usd_per_oz,unit,value_definition,smoothing_method,source_workbook,manifest_path,validation_status,availability_status\nL9-001,2026-08-20,12,usd_per_troy_ounce,x,x,w,m,FLAG,AVAILABLE\n')
 try: m.build(p,'source')
 except ValueError: pass
 else: raise AssertionError('expected rejection')
