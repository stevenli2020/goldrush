import tempfile
import unittest
from pathlib import Path
import pandas as pd
from parse_official_purchases import parse_file

class OfficialPurchaseTests(unittest.TestCase):

    def test_aggregates_monthly_country_changes(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'changes.xlsx'
            rows = [[None, 'Country', None, '2026-01-01', '2026-02-01'], ['A', 'A', None, 10, -3], ['B', 'B', None, 2, 4]]
            pd.DataFrame(rows).to_excel(p, sheet_name='Monthly', index=False, header=False)
            result = parse_file(p, '2026-08-20', '2026-08-21')
            self.assertEqual(result.iloc[0]['official_purchase_change_tonnes'], 12)
            self.assertEqual(result.iloc[1]['official_purchase_change_tonnes'], 1)

    def test_excludes_gross_star_series_but_keeps_adjusted_turkey(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'changes.xlsx'
            rows = [[None, 'Country', None, '2026-01-01'], ['x', 'Turkey*', None, 100], ['x', 'Turkey', None, 7], ['x', 'A', None, 3]]
            pd.DataFrame(rows).to_excel(p, sheet_name='Monthly', index=False, header=False)
            result = parse_file(p, '2026-08-20', '2026-08-21')
            self.assertEqual(result.iloc[0]['official_purchase_change_tonnes'], 10)
if __name__ == '__main__':
    unittest.main()
