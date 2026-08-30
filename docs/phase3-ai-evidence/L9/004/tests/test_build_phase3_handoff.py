import csv, importlib.util
from pathlib import Path
ROOT=Path(__file__).parents[5]
spec=importlib.util.spec_from_file_location('handoff',ROOT/'docs/phase3-ai-evidence/L9/004/scripts/build_phase3_handoff.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def test_builds_handoff(tmp_path):
 p=tmp_path/'x.csv'; f=sorted(m.REQUIRED)
 with p.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=f); w.writeheader(); w.writerow({'variable_id':'L9-004','observation_period':'Q2\'26','observation_period_type':'quarterly','observation_date':'2026-06-30','component':'jewellery_demand_tonnes','value':'10','unit':'metric_tonnes','value_definition':'India jewellery demand','source_workbook':'gdt.xlsx','manifest_path':'m','validation_status':'PASS','availability_status':'AVAILABLE'})
 assert m.build(p,'WGC GDT')[0]['value']==10.0
def test_rejects_flag(tmp_path):
 p=tmp_path/'x.csv'; p.write_text('variable_id,observation_period,observation_period_type,observation_date,component,value,unit,value_definition,source_workbook,manifest_path,validation_status,availability_status\nL9-004,Q2,quarterly,2026-06-30,jewellery,10,metric_tonnes,x,w,m,FLAG,AVAILABLE\n')
 try: m.build(p,'source')
 except ValueError: pass
 else: raise AssertionError('expected rejection')
