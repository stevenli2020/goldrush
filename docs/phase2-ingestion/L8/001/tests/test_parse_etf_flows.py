import tempfile
import unittest
from pathlib import Path
import pandas as pd
from parse_etf_flows import parse_file

class ETFFlowTests(unittest.TestCase):

    def test_monthly_tonnes_are_extracted(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'flows.xlsx'
            pd.DataFrame([['Date', 'Tonnes'], ['2026-07-31', 12.5], ['2026-08-31', -3.2]]).to_excel(p, sheet_name='Fund flows by month', index=False, header=False)
            result = parse_file(p, '2026-08-04', '2026-08-21')
            self.assertEqual(len(result), 2)
            self.assertEqual(result.iloc[0]['unit'], 'metric_tonnes')
if __name__ == '__main__':
    unittest.main()
