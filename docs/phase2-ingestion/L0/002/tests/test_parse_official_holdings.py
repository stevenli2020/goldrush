import tempfile
import unittest
from pathlib import Path
import pandas as pd
from parse_official_holdings import parse_file

class OfficialHoldingsTests(unittest.TestCase):

    def make_workbook(self, rows):
        path = Path(self.temp.name) / 'holdings.xlsx'
        pd.DataFrame(rows).to_excel(path, index=False, header=False)
        return path

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp.cleanup()

    def test_extracts_holdings_and_metadata(self):
        path = self.make_workbook([['World official gold holdings'], ['Country', 'Gold holdings (tonnes)'], ['Australia', 79.85], ['Canada', 6.84]])
        result = parse_file(path, '2026-08-20', '2026-08-21')
        self.assertEqual(len(result), 2)
        self.assertEqual(set(result['country']), {'Australia', 'Canada'})
        self.assertEqual(result.iloc[0]['unit'], 'metric_tonnes')

    def test_rejects_missing_holdings_column(self):
        path = self.make_workbook([['Country', 'Value'], ['Australia', 1]])
        with self.assertRaises(ValueError):
            parse_file(path, '2026-08-20', '2026-08-21')
if __name__ == '__main__':
    unittest.main()
