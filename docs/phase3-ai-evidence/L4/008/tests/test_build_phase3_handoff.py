import csv, importlib.util
from pathlib import Path
ROOT=Path(__file__).parents[5]
spec=importlib.util.spec_from_file_location('handoff',ROOT/'docs/phase3-ai-evidence/L4/008/scripts/build_phase3_handoff.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def test_builds_handoff(tmp_path):
 p=tmp_path/'x.csv'; f=sorted(m.REQUIRED)
 with p.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=f); w.writeheader(); w.writerow({'variable_id':'L4-008','observation_date':'2025-09-30','gross_interest_expense_usd':'100','total_receipts_usd':'1000','interest_expense_to_revenue_pct':'10','unit':'percent_of_federal_receipts','accounting_convention':'gross interest / receipts','manifest_path':'m','validation_status':'PASS','availability_status':'AVAILABLE'})
 assert m.build(p,'Treasury MTS manifest')[0]['value']==10.0
def test_rejects_flag(tmp_path):
 p=tmp_path/'x.csv'; p.write_text('variable_id,observation_date,gross_interest_expense_usd,total_receipts_usd,interest_expense_to_revenue_pct,unit,accounting_convention,manifest_path,validation_status,availability_status\nL4-008,2025-09-30,100,1000,60,percent_of_federal_receipts,x,m,FLAG,AVAILABLE\n')
 try: m.build(p,'source')
 except ValueError: pass
 else: raise AssertionError('expected rejection')
