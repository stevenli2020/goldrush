"""
test_fetch_cme_bulletin.py — Tests for the automated CME Daily Bulletin fetcher.

Tests:
    A1  Settlement extraction — correct prices from real bulletin text
    A2  Settlement extraction — only GC delivery months included
    A3  Expiry parsing — correct month/day mapping, not positional zip
    A4  Expiry parsing — contracts beyond table window are omitted, not guessed
    A5  Contract pair selection — matches manually-verified pair for 2026-08-18
    A6  Label to contract code conversion

Run:
    cd docs/phase2-ingestion/L0/009/data
    python -m pytest tests/test_fetch_cme_bulletin.py -v
"""

import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from fetch_cme_bulletin import (
    label_to_code,
    parse_gc_expiries,
    parse_gc_settlements,
    select_contract_pair,
)

# Real text block extracted from the CME Daily Bulletin PDF, 2026-08-18 issue.
REAL_GC_BLOCK = """GC FUT COMEX GOLD FUTURES
AUG26  - 128351.80 4489.404434.10 /4330.70 1119 + 7554415.20 ----
SEP26  - 276152.20 4372.204443.40 /4340.40 5753 + 4874423.00 ----
OCT26  - 1356752.30 4511.304459.30 /4352.00 52856 - 2774439.00 173
NOV26  - 12252.70 4405.004464.40 /4376.80 628 - 164460.60 ----
DEC26  - 12935653.10 4545.304493.10 /4383.30 312507 - 5534473.40 1794
JAN27  - 7253.30 4439.804444.00 /4432.30 458 + 494444.00 ----
FEB27  - 333153.80 4581.204528.20B/4418.60 21076 + 6534510.20 ----
MAR27  - ----54.20 4470.90---- 28 UNCH---- ----
APR27  - 98154.60 4615.504560.00B/4453.20A 7499 + 434519.20 ----
MAY27  - 354.70 4506.504505.70 /4505.60 12 UNCH4505.60 ----
JUN27  - 52455.10 4651.204591.60 /4501.00 1940 + 684591.60 ----
JUL27  - ----55.40 4540.80---- 8 UNCH---- ----
AUG27  - 7755.70 4687.304560.20B/4558.40 958 + 144558.40 ----
"""

REAL_EXPIRY_LINE = (
    "GC FUT 08/27 09/28 10/28 11/25 12/29 01/27 02/24 03/29 "
    "04/28 05/26 06/28 07/28 08/27"
)


# ---------------------------------------------------------------------------
# A1 — Settlement extraction correctness
# ---------------------------------------------------------------------------

def test_A1_settlement_prices_correct():
    settlements = parse_gc_settlements(REAL_GC_BLOCK)
    by_label = {s["label"]: s["settle"] for s in settlements}

    assert abs(by_label["AUG26"] - 4489.40) < 1e-4
    assert abs(by_label["OCT26"] - 4511.30) < 1e-4
    assert abs(by_label["DEC26"] - 4545.30) < 1e-4
    assert abs(by_label["FEB27"] - 4581.20) < 1e-4
    assert abs(by_label["APR27"] - 4615.50) < 1e-4
    assert abs(by_label["JUN27"] - 4651.20) < 1e-4
    assert abs(by_label["AUG27"] - 4687.30) < 1e-4


# ---------------------------------------------------------------------------
# A2 — Only GC delivery months included
# ---------------------------------------------------------------------------

def test_A2_only_delivery_months():
    """SEP26, NOV26, JAN27, MAR27, MAY27, JUL27 are NOT GC delivery months and must be excluded."""
    settlements = parse_gc_settlements(REAL_GC_BLOCK)
    labels = {s["label"] for s in settlements}

    expected_delivery_labels = {"AUG26", "OCT26", "DEC26", "FEB27", "APR27", "JUN27", "AUG27"}
    non_delivery_labels = {"SEP26", "NOV26", "JAN27", "MAR27", "MAY27", "JUL27"}

    assert expected_delivery_labels.issubset(labels)
    assert labels.isdisjoint(non_delivery_labels), (
        f"Non-delivery months leaked into settlements: {labels & non_delivery_labels}"
    )


# ---------------------------------------------------------------------------
# A3 — Expiry parsing: correct month/day mapping
# ---------------------------------------------------------------------------

def test_A3_expiry_mapping_correct():
    """
    Regression test: expiry table lists CONSECUTIVE months, not delivery
    months. A naive positional zip against settlements would misassign
    OCT26's settlement to September's expiry date. This must not happen.
    """
    settlements = parse_gc_settlements(REAL_GC_BLOCK)
    expiries = parse_gc_expiries(REAL_EXPIRY_LINE, settlements)

    assert expiries["AUG26"] == date(2026, 8, 27)
    assert expiries["OCT26"] == date(2026, 10, 28)   # NOT September's 09/28
    assert expiries["DEC26"] == date(2026, 12, 29)   # NOT October's 10/28
    assert expiries["FEB27"] == date(2027, 2, 24)
    assert expiries["APR27"] == date(2027, 4, 28)
    assert expiries["JUN27"] == date(2027, 6, 28)
    assert expiries["AUG27"] == date(2027, 8, 27)


def test_A3_year_rollover_handled():
    """Year increments correctly when month sequence wraps from Dec to Jan."""
    settlements = parse_gc_settlements(REAL_GC_BLOCK)
    expiries = parse_gc_expiries(REAL_EXPIRY_LINE, settlements)

    # FEB27 (Feb 2027) must be year 2027, not 2026
    assert expiries["FEB27"].year == 2027
    assert expiries["DEC26"].year == 2026


# ---------------------------------------------------------------------------
# A4 — Contracts beyond table window are omitted, not guessed
# ---------------------------------------------------------------------------

def test_A4_contracts_beyond_window_omitted():
    """
    The expiry table only covers ~13 months. Settlement rows for contracts
    beyond that (e.g. far-dated contracts like DEC28, JUN29) must NOT appear
    in the expiries dict — they must be omitted, never assigned a guessed date.
    """
    extended_block = REAL_GC_BLOCK + "DEC28  - 256.70 4967.50---- 140 UNCH---- ----\n"
    settlements = parse_gc_settlements(extended_block)
    expiries = parse_gc_expiries(REAL_EXPIRY_LINE, settlements)

    assert "DEC28" not in expiries, (
        "DEC28 is beyond the bulletin's expiry table window and must be omitted"
    )
    # But contracts within the table window must still be present
    assert "AUG27" in expiries


# ---------------------------------------------------------------------------
# A5 — Contract pair selection matches manual verification
# ---------------------------------------------------------------------------

def test_A5_pair_selection_matches_manual_check():
    """
    Cross-check against the manually verified pair for obs_date=2026-08-18:
    GCQ26 (front, exp 2026-08-27) / GCV26 (far, exp 2026-10-28), span=62 days.
    This was independently confirmed by reading the bulletin PDF directly.
    """
    settlements = parse_gc_settlements(REAL_GC_BLOCK)
    expiries = parse_gc_expiries(REAL_EXPIRY_LINE, settlements)
    obs_date = date(2026, 8, 18)

    front_label, front_settle, front_exp, far_label, far_settle, far_exp, span = \
        select_contract_pair(settlements, expiries, obs_date)

    assert front_label == "AUG26"
    assert far_label == "OCT26"
    assert front_exp == date(2026, 8, 27)
    assert far_exp == date(2026, 10, 28)
    assert span == 62
    assert abs(front_settle - 4489.40) < 1e-4
    assert abs(far_settle - 4511.30) < 1e-4


def test_A5_front_min_days_to_expiry_respected():
    """If obs_date is within min_days_to_expiry of AUG26, it must be skipped as front."""
    settlements = parse_gc_settlements(REAL_GC_BLOCK)
    expiries = parse_gc_expiries(REAL_EXPIRY_LINE, settlements)
    obs_date = date(2026, 8, 24)  # 3 days before AUG26 expiry (08/27)

    front_label, _, front_exp, _, _, _, _ = select_contract_pair(
        settlements, expiries, obs_date, min_days_to_expiry=5
    )
    # AUG26 excluded (only 3 days away); next eligible is OCT26
    assert front_label != "AUG26"
    assert (front_exp - obs_date).days >= 5


# ---------------------------------------------------------------------------
# A6 — Label to contract code conversion
# ---------------------------------------------------------------------------

def test_A6_label_to_code():
    assert label_to_code("AUG26") == "GCQ26"
    assert label_to_code("OCT26") == "GCV26"
    assert label_to_code("DEC26") == "GCZ26"
    assert label_to_code("FEB27") == "GCG27"
    assert label_to_code("APR27") == "GCJ27"
    assert label_to_code("JUN27") == "GCM27"
