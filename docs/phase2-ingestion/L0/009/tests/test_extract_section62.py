import sys
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
from extract_section62 import extract_rows_from_text


def test_extracts_gold_pair():
    text = """GC FUT               COMEX GOLD FUTURES
AUG26  4506.80  4530.00 /4484.00A  4516.30 + 26.90  478  ----  402 + 28
OCT26  4547.20  4562.30 /4472.50   4537.10 + 25.80  20961 403 55009 + 1099
DEC26  4580.00  4597.10 /4506.00   4571.40 + 26.10  184637 1838 328234 + 2020
TOTAL GC FUT"""
    rows = extract_rows_from_text(text, date(2026, 8, 20))
    assert rows[0]["near_settlement"] == 4516.3
    assert rows[0]["far_settlement"] == 4537.1
    assert rows[0]["days"] == 61
