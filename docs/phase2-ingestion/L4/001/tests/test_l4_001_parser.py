import json, tempfile, unittest, importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location("l4_001_parser", Path(__file__).parents[1]/"parser.py"); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); parse=module.parse
class TestParser(unittest.TestCase):
    def test_valid_and_invalid(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"raw.json"; p.write_text(json.dumps({"observations":[{"date":"2026-08-01","value":"332.8"},{"date":"2020-01-01","value":"300"}]}))
            rows=parse(p, retrieved_at="2026-08-21T00:00:00+00:00"); self.assertEqual(rows[0]["variable_id"],"L4-001"); self.assertEqual(rows[1]["availability_status"],"STALE")
            p.write_text(json.dumps({"observations":[{"date":"bad","value":"."}]}))
            with self.assertRaises(ValueError): parse(p)
