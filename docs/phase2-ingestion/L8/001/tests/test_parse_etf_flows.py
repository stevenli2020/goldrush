import tempfile
import unittest
from pathlib import Path
import pandas as pd
from parse_etf_flows import parse_file

class ETFFlowTests(unittest.TestCase):

    def test_monthly_tonnes_are_extracted(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'flows.xlsx'
            rows = [
                ['Date', 'Gold, US$/oz', 'Ounces', 'Tonnes', 'Value (USD)', 'Fund A', 'Fund B'],
                ['2026-07-31', 3300, 1, 999, 1, 10.0, 2.5],
                ['2026-08-31', 3300, 1, 999, 1, -3.2, 0.0],
            ]
            pd.DataFrame(rows).to_excel(p, sheet_name='Demand by month', index=False, header=False)
            result = parse_file(p, '2026-08-04', '2026-08-21')
            self.assertEqual(len(result), 2)
            self.assertEqual(result.iloc[0]['etf_flow_tonnes'], 12.5)
            self.assertEqual(result.iloc[0]['unit'], 'metric_tonnes')
if __name__ == '__main__':
    unittest.main()
