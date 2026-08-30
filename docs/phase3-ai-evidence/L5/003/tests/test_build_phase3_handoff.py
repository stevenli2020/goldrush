import csv, importlib.util
from pathlib import Path
ROOT=Path(__file__).parents[5]
spec=importlib.util.spec_from_file_location('handoff',ROOT/'docs/phase3-ai-evidence/L5/003/scripts/build_phase3_handoff.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def test_builds_handoff_with_initial_missing_change(tmp_path):
 p=tmp_path/'x.csv'; f=sorted(m.REQUIRED)
 with p.open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=f); w.writeheader(); w.writerow({'variable_id':'L5-003','observation_date':'2020-03-31','usd_reserve_share_pct':'60','usd_share_change_qoq_pp':'','unit':'percent_and_percentage_points','source_dataset_id':'IMF.STA:COFER','source_series_id':'G001.AFXRA.CI_USD.SHRO_PT.Q','manifest_path':'m','validation_status':'PASS','availability_status':'AVAILABLE'})
 assert m.build(p,'IMF COFER')[0]['value'] is None
def test_rejects_flag(tmp_path):
 p=tmp_path/'x.csv'; p.write_text('variable_id,observation_date,usd_reserve_share_pct,usd_share_change_qoq_pp,unit,source_dataset_id,source_series_id,manifest_path,validation_status,availability_status\nL5-003,2020-03-31,60,1,percent_and_percentage_points,IMF.STA:COFER,G001.AFXRA.CI_USD.SHRO_PT.Q,m,FLAG,AVAILABLE\n')
 try: m.build(p,'source')
 except ValueError: pass
 else: raise AssertionError('expected rejection')
