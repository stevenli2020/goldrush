import csv, importlib.util
from pathlib import Path
ROOT=Path(__file__).parents[5]
spec=importlib.util.spec_from_file_location('handoff',ROOT/'docs/phase3-ai-evidence/L5/001/scripts/build_phase3_handoff.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def test_builds_handoff(tmp_path):
 p=tmp_path/'x.csv'; f=sorted(m.REQUIRED)
 with p.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=f); w.writeheader(); w.writerow({'variable_id':'L5-001','observation_date':'2026-07-01','official_purchase_change_tonnes':'12.5','unit':'metric_tonnes','source_file':'wgc.xlsx','source_publication_date':'2026-08-20','download_date':'2026-08-21','validation_status':'PASS','availability_status':'AVAILABLE'})
 assert m.build(p,'WGC workbook')[0]['value']==12.5
def test_rejects_invalid(tmp_path):
 p=tmp_path/'x.csv'; p.write_text('variable_id,observation_date,official_purchase_change_tonnes,unit,source_file,source_publication_date,download_date,validation_status,availability_status\nL5-001,2026-07-01,12,metric_tonnes,w,p,d,FLAG,AVAILABLE\n')
 try: m.build(p,'source')
 except ValueError: pass
 else: raise AssertionError('expected rejection')
