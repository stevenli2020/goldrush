import csv, importlib.util
from pathlib import Path
ROOT=Path(__file__).parents[5]
spec=importlib.util.spec_from_file_location('handoff',ROOT/'docs/phase3-ai-evidence/L4/009/scripts/build_phase3_handoff.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def test_builds_handoff(tmp_path):
 p=tmp_path/'x.csv'; f=sorted(m.REQUIRED)
 with p.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=f); w.writeheader(); w.writerow({'variable_id':'L4-009','observation_date':'2026-07-31','maturing_within_1y_mil_usd':'100','total_marketable_outstanding_mil_usd':'1000','dated_detail_outstanding_mil_usd':'990','classification_coverage_pct':'99','marketable_debt_maturing_within_1y_pct':'10','unit':'percent_of_marketable_treasury_debt','measure_definition':'maturity','manifest_path':'m','validation_status':'PASS','availability_status':'AVAILABLE'})
 assert m.build(p,'Treasury MSPD')[0]['value']==10.0
def test_rejects_flag(tmp_path):
 p=tmp_path/'x.csv'; p.write_text('variable_id,observation_date,maturing_within_1y_mil_usd,total_marketable_outstanding_mil_usd,dated_detail_outstanding_mil_usd,classification_coverage_pct,marketable_debt_maturing_within_1y_pct,unit,measure_definition,manifest_path,validation_status,availability_status\nL4-009,2026-07-31,100,1000,990,99,10,percent_of_marketable_treasury_debt,m,m,FLAG,AVAILABLE\n')
 try: m.build(p,'source')
 except ValueError: pass
 else: raise AssertionError('expected rejection')
