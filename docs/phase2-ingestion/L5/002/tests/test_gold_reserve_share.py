import tempfile
import unittest
from pathlib import Path
import pandas as pd
from parse_gold_reserve_share import parse_file

class ReserveShareTests(unittest.TestCase):
    def test_extracts_share_and_holdings(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"holdings.xlsx"
            rows=[[None,None,None,None],[None,"Name","Tonnes","% of reserves**"],[1,"A",100,0.25],[2,"B",50,0.1]]
            pd.DataFrame(rows).to_excel(p,sheet_name="PDF",index=False,header=False)
            result=parse_file(p,"2026-08-20","2026-08-21")
            self.assertEqual(len(result),2); self.assertEqual(result.iloc[0]["gold_share_of_reserves"],0.25); self.assertEqual(result.iloc[0]["unit"],"fraction")

if __name__ == "__main__": unittest.main()
