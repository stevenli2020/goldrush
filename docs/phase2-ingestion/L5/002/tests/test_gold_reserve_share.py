import tempfile
import unittest
from pathlib import Path
import pandas as pd
from parse_gold_reserve_share import parse_file

class ReserveShareTests(unittest.TestCase):
    def test_extracts_share_and_holdings(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"holdings.xlsx"
            rows=[[None,None,None,None,None,None,None,None,None,None],[None,"Name","Tonnes","% of reserves**","Holdings as of",None,"Name","Tonnes","% of reserves**","Holdings as of"],[1,"A",100,0.25,"2026-06-30",1,"C",80,0.4,"2026-05-31"],[2,"B",50,0.1,"2026-06-30",2,"D",40,0.2,"2026-04-30"]]
            pd.DataFrame(rows).to_excel(p,sheet_name="PDF",index=False,header=False)
            result=parse_file(p,"2026-08-20","2026-08-21")
            self.assertEqual(len(result),4); self.assertEqual(result.iloc[0]["gold_share_of_reserves"],0.25); self.assertEqual(result.iloc[0]["holdings_as_of"],"2026-06-30"); self.assertEqual(set(result["panel"]), {"left", "right"})

    def test_rejects_share_out_of_bounds(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"holdings.xlsx"
            rows=[[None,None,None,None,None,None,None,None,None,None],[None,"Name","Tonnes","% of reserves**","Holdings as of",None,"Name","Tonnes","% of reserves**","Holdings as of"],[1,"A",100,1.2,"2026-06-30",None,None,None,None,None]]
            pd.DataFrame(rows).to_excel(p,sheet_name="PDF",index=False,header=False)
            with self.assertRaises(ValueError): parse_file(p,"2026-08-20","2026-08-21")

if __name__ == "__main__": unittest.main()
