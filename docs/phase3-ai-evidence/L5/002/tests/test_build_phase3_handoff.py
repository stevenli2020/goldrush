import csv, importlib.util
from pathlib import Path
ROOT=Path(__file__).parents[5]
spec=importlib.util.spec_from_file_location('handoff',ROOT/'docs/phase3-ai-evidence/L5/002/scripts/build_phase3_handoff.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def test_builds_handoff(tmp_path):
 p=tmp_path/'x.csv'; f=sorted(m.REQUIRED)
 with p.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=f); w.writeheader(); w.writerow({'variable_id':'L5-002','country':'A','panel':'left','gold_share_of_reserves':'0.25','holdings_tonnes':'100','holdings_as_of':'2026-06-30','unit':'fraction','source_file':'wgc.xlsx','source_publication_date':'2026-08-20','download_date':'2026-08-21','validation_status':'PASS','availability_status':'AVAILABLE'})
 assert m.build(p,'WGC workbook')[0]['value']==0.25
def test_rejects_invalid(tmp_path):
 p=tmp_path/'x.csv'; p.write_text('variable_id,country,panel,gold_share_of_reserves,holdings_tonnes,holdings_as_of,unit,source_file,source_publication_date,download_date,validation_status,availability_status\nL5-002,A,left,1.2,100,2026-06-30,fraction,w,p,d,PASS,AVAILABLE\n')
 try: m.build(p,'source')
 except ValueError: pass
 else: raise AssertionError('expected rejection')
