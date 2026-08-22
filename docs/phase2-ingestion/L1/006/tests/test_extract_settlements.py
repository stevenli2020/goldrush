import sys
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
from extract_settlements import extract_rows_from_text

def test_extracts_zq_rows_and_expiry():
    text = "30D FED FD FUT\nAUG26 96.3675 (\nSEP26 96.3050 (\nTOTAL"
    rows = extract_rows_from_text(text, date(2026, 8, 20))
    assert rows[0]["contract"] == "ZQQ26"
    assert rows[0]["settlement_price"] == "96.3675"
    assert rows[0]["expiry_date"] == "2026-08-31"
