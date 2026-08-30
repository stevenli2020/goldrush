import csv, importlib.util
from pathlib import Path
ROOT=Path(__file__).parents[5]
spec=importlib.util.spec_from_file_location('handoff',ROOT/'docs/phase3-ai-evidence/L8/001/scripts/build_phase3_handoff.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def test_builds_handoff(tmp_path):
 p=tmp_path/'x.csv'; f=sorted(m.REQUIRED)
 with p.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=f); w.writeheader(); w.writerow({'variable_id':'L8-001','observation_date':'2026-07-31','etf_flow_tonnes':'-12.5','unit':'metric_tonnes','source_file':'etf.xlsx','source_publication_date':'2026-08-04','download_date':'2026-08-21','validation_status':'PASS','availability_status':'AVAILABLE'})
 assert m.build(p,'WGC ETF')[0]['value']==-12.5
def test_rejects_flag(tmp_path):
 p=tmp_path/'x.csv'; p.write_text('variable_id,observation_date,etf_flow_tonnes,unit,source_file,source_publication_date,download_date,validation_status,availability_status\nL8-001,2026-07-31,-12,metric_tonnes,e,p,d,FLAG,AVAILABLE\n')
 try: m.build(p,'source')
 except ValueError: pass
 else: raise AssertionError('expected rejection')
