import json, tempfile, unittest, importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location('l4_002_parser', Path(__file__).parents[1] / 'parser.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
parse = module.parse

class TestParser(unittest.TestCase):

    def test_valid_and_invalid(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'raw.json'
            p.write_text(json.dumps({'observations': [{'date': '2026-08-01', 'value': '130.2'}]}))
            rows = parse(p)
            self.assertEqual(rows[0]['source_series_id'], 'PCEPILFE')
            p.write_text(json.dumps({'observations': [{'date': 'bad', 'value': '.'}]}))
            with self.assertRaises(ValueError):
                parse(p)
