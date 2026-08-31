import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
TESTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_DIR.parent
SCRIPTS_DIR = PROJECT_ROOT / 'scripts'
sys.path.insert(0, str(SCRIPTS_DIR))
from parse_above_ground import SCHEMA_COLUMNS, parse_above_ground_data, run_validations_and_log, compare_revisions
WORKBOOK_PATH = str(PROJECT_ROOT / 'data' / 'above-ground-gold-stocks' / '2026' / 'above-ground-gold-stocks.xlsx')

class TestAboveGroundCollector(unittest.TestCase):

    def setUp(self):
        self.workbook_exists = os.path.exists(WORKBOOK_PATH)
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_parse_real_workbook_schema_and_provenance(self):
        if not self.workbook_exists:
            self.skipTest(f'Source file {WORKBOOK_PATH} not found.')
        df = parse_above_ground_data(WORKBOOK_PATH, sheet_name='Above-ground stocks')
        self.assertListEqual(list(df.columns), SCHEMA_COLUMNS)
        self.assertGreater(len(df), 0)
        self.assertTrue(df['ingested_at'].str.contains('T').all())
        self.assertTrue((df['source_citation'] != '').all())
        for field in ['jewellery_tonnes', 'private_investment_tonnes', 'etfs_tonnes', 'total_above_ground_tonnes']:
            self.assertFalse(df[field].isnull().all(), f'Field {field} should contain values')

    def test_validations_and_revision_logging(self):
        if not self.workbook_exists:
            self.skipTest(f'Source file {WORKBOOK_PATH} not found.')
        df = parse_above_ground_data(WORKBOOK_PATH)
        log_path = os.path.join(self.temp_dir.name, 'validation_warnings.log')
        rev_path = os.path.join(self.temp_dir.name, 'revision_log.json')
        csv_path = os.path.join(self.temp_dir.name, 'test_out.csv')
        df.to_csv(csv_path, index=False)
        self.assertTrue(os.path.exists(csv_path))
        try:
            parquet_path = os.path.join(self.temp_dir.name, 'test_out.parquet')
            df.to_parquet(parquet_path, index=False)
            self.assertTrue(os.path.exists(parquet_path))
        except ImportError:
            pass
        warnings = run_validations_and_log(df, log_path)
        self.assertTrue(os.path.exists(log_path))
        revisions = compare_revisions(df, csv_path, rev_path)
        self.assertTrue(os.path.exists(rev_path))
        self.assertEqual(len(revisions), 0)
        df_mod = df.copy()
        df_mod.loc[0, 'jewellery_tonnes'] += 100.0
        revisions_mod = compare_revisions(df_mod, csv_path, rev_path)
        self.assertEqual(len(revisions_mod), 1)
        self.assertEqual(revisions_mod[0]['field'], 'jewellery_tonnes')

    def test_malformed_and_sum_mismatch_fail(self):
        source = Path(WORKBOOK_PATH)
        raw = __import__('pandas').read_excel(source, sheet_name='Above-ground stocks', header=None)
        malformed = raw.astype(object).copy()
        malformed.iloc[4, 2] = 'not-a-number'
        malformed_path = Path(self.temp_dir.name) / 'malformed.xlsx'
        malformed.to_excel(malformed_path, sheet_name='Above-ground stocks', header=False, index=False)
        with self.assertRaises(ValueError):
            parse_above_ground_data(str(malformed_path))
        mismatch = raw.copy()
        mismatch.iloc[9, 2] = float(mismatch.iloc[9, 2]) + 1.0
        mismatch_path = Path(self.temp_dir.name) / 'mismatch.xlsx'
        mismatch.to_excel(mismatch_path, sheet_name='Above-ground stocks', header=False, index=False)
        mismatch_df = parse_above_ground_data(str(mismatch_path))
        with self.assertRaises(ValueError):
            run_validations_and_log(mismatch_df, os.path.join(self.temp_dir.name, 'mismatch.log'))
if __name__ == '__main__':
    unittest.main()
