import json, tempfile, unittest, importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location('l4_004_parser', Path(__file__).parents[1] / 'parser.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
parse = module.parse

class TestParser(unittest.TestCase):

    def test_valid_and_outlier(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'raw.json'
            p.write_text(json.dumps({'observations': [{'date': '2026-08-20', 'value': '2.28'}, {'date': '2026-08-19', 'value': '25'}]}))
            rows = parse(p)
            self.assertEqual(rows[0]['source_series_id'], 'T10YIE')
            self.assertEqual(rows[1]['validation_status'], 'FLAG')
