import importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location("l10_002_parser", Path(__file__).parents[1] / "parser.py")
parser_module = importlib.util.module_from_spec(spec); spec.loader.exec_module(parser_module)
parse = parser_module.parse

def test_extracts_comex_gold(tmp_path):
    source = tmp_path / "x.csv"; source.write_text("observation_date,product,open_interest,source_pdf_sha256,source_manifest\n2026-08-20,COMEX GOLD,367046," + "a" * 64 + ",manifest.json\n2026-08-20,COMEX SILVER,95999," + "a" * 64 + ",manifest.json\n", encoding="utf-8")
    row = parse(source)[0]; assert row["open_interest_contracts"] == 367046; assert row["source_pdf_sha256"] == "a" * 64; assert row["validation_status"] == "PASS"

def test_duplicate_gold_rejected(tmp_path):
    source = tmp_path / "x.csv"; source.write_text("observation_date,product,open_interest,source_pdf_sha256,source_manifest\n2026-08-20,COMEX GOLD,367046," + "a" * 64 + ",manifest.json\n2026-08-20,COMEX GOLD,367047," + "a" * 64 + ",manifest.json\n", encoding="utf-8")
    try: parse(source)
    except ValueError as exc: assert "duplicate" in str(exc)
    else: raise AssertionError("duplicate observation was accepted")
