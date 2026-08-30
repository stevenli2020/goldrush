import csv, importlib.util
from pathlib import Path
ROOT=Path(__file__).parents[5]
spec=importlib.util.spec_from_file_location('handoff',ROOT/'docs/phase3-ai-evidence/L5/006/scripts/build_phase3_handoff.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def test_builds_handoff(tmp_path):
 p=tmp_path/'x.csv'; f=sorted(m.REQUIRED)
 with p.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=f); w.writeheader(); w.writerow({'variable_id':'L5-006','country_entity':'A','observation_date':'2026-06-01','signed_change_tonnes':'-2','official_sector_net_reduction_tonnes':'2','unit':'metric_tonnes','value_definition':'net reduction proxy','source_workbook':'wgc.xlsx','publication_date':'2026-08-20','download_date':'2026-08-21','validation_status':'PASS','availability_status':'AVAILABLE'})
 assert m.build(p,'WGC workbook')[0]['value']==2.0
def test_rejects_flag(tmp_path):
 p=tmp_path/'x.csv'; p.write_text('variable_id,country_entity,observation_date,signed_change_tonnes,official_sector_net_reduction_tonnes,unit,value_definition,source_workbook,publication_date,download_date,validation_status,availability_status\nL5-006,A,2026-06-01,-2,2,metric_tonnes,x,w,p,d,FLAG,AVAILABLE\n')
 try: m.build(p,'source')
 except ValueError: pass
 else: raise AssertionError('expected rejection')
