"""
test_parse_gilr.py — L0-009 test suite

Tests:
    T1  Contract expiry resolution — correct third-to-last business day
    T2  Contract pair selection — correct front/far within 60-120 day window
    T3  Contract pair selection — roll avoidance (front must be >= 5 days from expiry)
    T4  GILR computation — correct formula output
    T5  GILR computation — calculation reconciliation check
    T6  Validation — negative GILR is FLAG not FAIL
    T7  Validation — SOFR below -1.0% is FAIL
    T8  Validation — settlement price <= 0 is FAIL
    T9  Validation — contract ordering (far expiry <= front expiry) is FAIL
    T10 Validation — day span outside [60, 120] is FAIL
    T11 Validation — SOFR vintage forward-dated is FAIL
    T12 Validation — calculation mismatch is FAIL
    T13 Validation — near roll date is FLAG
    T14 Missing-data behavior — SOFR manual load from file
    T15 Nasdaq CME CSV parsing — correct column extraction

Run:
    cd docs/phase2-ingestion/L0/009/data
    python -m pytest tests/test_parse_gilr.py -v
"""

import csv
import io
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from parse_gilr import (
    compute_gilr,
    contract_expiry,
    infer_active_contracts,
    nth_to_last_business_day,
    parse_nasdaq_gc_csv,
    validate_record,
    verify_computation,
)

import logging
NULL_LOGGER = logging.getLogger("null")
NULL_LOGGER.addHandler(logging.NullHandler())

BASE_CFG = {
    "contract_selection": {
        "front_min_days_to_expiry": 5,
        "target_span_days": 90,
        "min_span_days": 60,
        "max_span_days": 120,
        "roll_proximity_flag_days": 10,
        "delivery_months": [2, 4, 6, 8, 10, 12],
    },
    "validation": {
        "sofr_min_pct_pa": 0.0,
        "sofr_fail_threshold_pct_pa": -1.0,
        "settlement_min": 0.0,
        "settlement_ratio_min": 0.85,
        "settlement_ratio_max": 1.15,
        "gilr_flag_min_pct_pa": -2.0,
        "gilr_flag_max_pct_pa": 4.0,
        "missing_day_flag_threshold": 3,
        "missing_day_block_threshold": 5,
    },
    "calculation": {
        "reconciliation_tolerance_pct": 0.0001,
    },
}


def make_rec(obs="2026-08-18", gilr=1.82, sofr=4.85, cme_fwd=3.03,
             front_code="GCQ26", front_settle=2485.30, front_expiry="2026-08-27",
             far_code="GCZ26", far_settle=2547.10, far_expiry="2026-11-25",
             days=90, sofr_vintage="2026-08-17"):
    return {
        "observation_date":               obs,
        "tenor":                          "3M",
        "gilr_cme_pct_pa":                gilr,
        "sofr_3m_pct_pa":                 sofr,
        "sofr_vintage_date":              sofr_vintage,
        "sofr_source":                    "FRED_SOFR3M",
        "cme_implied_forward_rate_pct_pa": cme_fwd,
        "cme_front_contract":             front_code,
        "cme_front_settlement":           front_settle,
        "cme_front_expiry":               front_expiry,
        "cme_far_contract":               far_code,
        "cme_far_settlement":             far_settle,
        "cme_far_expiry":                 far_expiry,
        "days_between_contracts":         days,
        "cme_source":                     "NASDAQ_CHRIS_CME",
        "is_revised":                     False,
    }


# ---------------------------------------------------------------------------
# T1 — Contract expiry resolution
# ---------------------------------------------------------------------------

def test_T1_expiry_known_month():
    """GCZ26 = December 2026; third-to-last business day."""
    expiry = contract_expiry("GCZ26")
    assert expiry.year == 2026
    assert expiry.month == 12
    expected = nth_to_last_business_day(2026, 12, 3)
    assert expiry == expected


def test_T1_expiry_august():
    """GCQ26 = August 2026."""
    expiry = contract_expiry("GCQ26")
    assert expiry.year == 2026
    assert expiry.month == 8
    expected = nth_to_last_business_day(2026, 8, 3)
    assert expiry == expected


def test_T1_invalid_code():
    with pytest.raises(ValueError, match="Cannot parse"):
        contract_expiry("INVALID")


# ---------------------------------------------------------------------------
# T2 — Contract pair selection within span window
# ---------------------------------------------------------------------------

def test_T2_pair_within_window():
    """Front and far contracts selected with span in [60, 120] days."""
    obs = date(2026, 7, 1)
    front_code, far_code = infer_active_contracts(obs, BASE_CFG["contract_selection"])
    front_exp = contract_expiry(front_code)
    far_exp   = contract_expiry(far_code)
    days = (far_exp - front_exp).days
    assert 60 <= days <= 120, f"Span {days} outside [60, 120]"
    assert far_exp > front_exp


def test_T2_front_not_too_close_to_expiry():
    """Front contract expiry must be >= 5 days from obs_date."""
    obs = date(2026, 7, 1)
    front_code, _ = infer_active_contracts(obs, BASE_CFG["contract_selection"])
    front_exp = contract_expiry(front_code)
    assert (front_exp - obs).days >= 5


# ---------------------------------------------------------------------------
# T3 — Roll avoidance
# ---------------------------------------------------------------------------

def test_T3_roll_period_skips_near_expiry():
    """When obs_date is within 5 days of a contract expiry, that contract is skipped."""
    front_aug_expiry = nth_to_last_business_day(2026, 8, 3)
    obs = front_aug_expiry - timedelta(days=3)  # 3 days before — inside min window

    front_code, _ = infer_active_contracts(obs, BASE_CFG["contract_selection"])
    front_exp = contract_expiry(front_code)
    assert (front_exp - obs).days >= 5, (
        f"Front expiry {front_exp} is less than 5 days from obs {obs}"
    )


# ---------------------------------------------------------------------------
# T4 — GILR computation
# ---------------------------------------------------------------------------

def test_T4_gilr_formula_normal():
    """GILR = SOFR - CME forward; verify formula output."""
    front, far, days, sofr = 2485.30, 2547.10, 90, 4.85
    cme_fwd, gilr = compute_gilr(sofr, front, far, days)
    expected_fwd  = ((far / front) - 1) * (360 / days) * 100
    expected_gilr = sofr - expected_fwd
    assert abs(cme_fwd - expected_fwd)  < 1e-4
    assert abs(gilr - expected_gilr) < 1e-4


def test_T4_gilr_negative_when_forward_exceeds_sofr():
    """
    GILR is negative when CME implied forward rate exceeds SOFR3M.
    Scenario: steep contango (far >> front) relative to low SOFR.
    front=2901.20, far=2937.03, days=90 => CME_fwd ≈ 4.94% > SOFR=4.60%
    => GILR ≈ -0.34%
    """
    front, far, days, sofr = 2901.20, 2937.03, 90, 4.60
    _, gilr = compute_gilr(sofr, front, far, days)
    assert gilr < 0, f"Expected negative GILR when CME forward > SOFR, got {gilr:.4f}"


# ---------------------------------------------------------------------------
# T5 — Calculation reconciliation
# ---------------------------------------------------------------------------

def test_T5_reconciliation_passes():
    front, far, days, sofr = 2485.30, 2547.10, 90, 4.85
    _, gilr = compute_gilr(sofr, front, far, days)
    assert verify_computation(gilr, sofr, front, far, days, 0.0001)


def test_T5_reconciliation_fails_on_tampered_value():
    front, far, days, sofr = 2485.30, 2547.10, 90, 4.85
    _, gilr = compute_gilr(sofr, front, far, days)
    tampered = gilr + 0.5
    assert not verify_computation(tampered, sofr, front, far, days, 0.0001)


# ---------------------------------------------------------------------------
# T6 — Negative GILR is FLAG not FAIL
# ---------------------------------------------------------------------------

def test_T6_negative_gilr_is_flag():
    """
    Negative GILR must produce FLAG, not FAIL.
    front=2901.20, far=2937.03 => CME_fwd ≈ 4.94% > SOFR=4.60% => GILR ≈ -0.34%
    """
    front, far, days, sofr = 2901.20, 2937.03, 90, 4.60
    cme_fwd, gilr = compute_gilr(sofr, front, far, days)
    assert gilr < 0, f"Fixture must produce negative GILR; got {gilr:.4f}"

    rec = make_rec(
        gilr=gilr, sofr=sofr, cme_fwd=cme_fwd,
        front_settle=front, far_settle=far, days=days,
        front_expiry="2026-08-27", far_expiry="2026-11-25",
    )
    status, notes = validate_record(rec, BASE_CFG, NULL_LOGGER)
    assert status == "FLAG", f"Expected FLAG for negative GILR, got {status}"
    assert notes and "backwardation" in notes.lower(), (
        f"Expected 'backwardation' in anomaly notes; got: {notes}"
    )


# ---------------------------------------------------------------------------
# T7 — SOFR below -1.0% is FAIL
# ---------------------------------------------------------------------------

def test_T7_sofr_below_fail_threshold():
    front, far, days = 2485.30, 2547.10, 90
    sofr = -1.5
    cme_fwd, gilr = compute_gilr(sofr, front, far, days)
    rec = make_rec(
        gilr=gilr, sofr=sofr, cme_fwd=cme_fwd,
        front_settle=front, far_settle=far, days=days,
        front_expiry="2026-08-27", far_expiry="2026-11-25",
    )
    status, _ = validate_record(rec, BASE_CFG, NULL_LOGGER)
    assert status == "FAIL", f"Expected FAIL for SOFR={sofr}%, got {status}"


# ---------------------------------------------------------------------------
# T8 — Settlement price <= 0 is FAIL
# ---------------------------------------------------------------------------

def test_T8_zero_settlement_fails():
    rec = make_rec(front_settle=0.0)
    status, _ = validate_record(rec, BASE_CFG, NULL_LOGGER)
    assert status == "FAIL"


def test_T8_negative_settlement_fails():
    rec = make_rec(far_settle=-10.0)
    status, _ = validate_record(rec, BASE_CFG, NULL_LOGGER)
    assert status == "FAIL"


# ---------------------------------------------------------------------------
# T9 — Contract ordering: far expiry <= front expiry is FAIL
# ---------------------------------------------------------------------------

def test_T9_inverted_contract_order():
    rec = make_rec(front_expiry="2026-11-25", far_expiry="2026-08-27")
    status, _ = validate_record(rec, BASE_CFG, NULL_LOGGER)
    assert status == "FAIL", f"Expected FAIL for inverted contract order, got {status}"


# ---------------------------------------------------------------------------
# T10 — Day span outside [60, 120] is FAIL
# ---------------------------------------------------------------------------

def test_T10_span_too_short():
    rec = make_rec(days=45, far_expiry="2026-10-11")
    status, _ = validate_record(rec, BASE_CFG, NULL_LOGGER)
    assert status == "FAIL", f"Expected FAIL for span=45d, got {status}"


def test_T10_span_too_long():
    rec = make_rec(days=130, far_expiry="2027-01-05")
    status, _ = validate_record(rec, BASE_CFG, NULL_LOGGER)
    assert status == "FAIL", f"Expected FAIL for span=130d, got {status}"


# ---------------------------------------------------------------------------
# T11 — SOFR vintage forward-dated is FAIL
# ---------------------------------------------------------------------------

def test_T11_sofr_vintage_future():
    rec = make_rec(obs="2026-08-18", sofr_vintage="2026-08-19")
    status, _ = validate_record(rec, BASE_CFG, NULL_LOGGER)
    assert status == "FAIL", f"Expected FAIL for forward-dated SOFR vintage, got {status}"


# ---------------------------------------------------------------------------
# T12 — Calculation mismatch is FAIL
# ---------------------------------------------------------------------------

def test_T12_calculation_mismatch():
    """Stored GILR does not match recomputed value."""
    front, far, days, sofr = 2485.30, 2547.10, 90, 4.85
    cme_fwd, gilr = compute_gilr(sofr, front, far, days)
    tampered_gilr = gilr + 0.5
    rec = make_rec(
        gilr=tampered_gilr, sofr=sofr, cme_fwd=cme_fwd,
        front_settle=front, far_settle=far, days=days,
        front_expiry="2026-08-27", far_expiry="2026-11-25",
    )
    status, _ = validate_record(rec, BASE_CFG, NULL_LOGGER)
    assert status == "FAIL", f"Expected FAIL for computation mismatch, got {status}"


# ---------------------------------------------------------------------------
# T13 — Near roll date is FLAG
# ---------------------------------------------------------------------------

def test_T13_near_roll_date_flag():
    """Front contract expiring in 3 days → FLAG."""
    front, far, days, sofr = 2485.30, 2547.10, 90, 4.85
    cme_fwd, gilr = compute_gilr(sofr, front, far, days)
    rec = make_rec(
        obs="2026-08-24",
        gilr=gilr, sofr=sofr, cme_fwd=cme_fwd,
        front_settle=front, far_settle=far, days=days,
        front_expiry="2026-08-27",  # 3 days away — within roll_proximity_flag_days=10
        far_expiry="2026-11-25",
    )
    status, notes = validate_record(rec, BASE_CFG, NULL_LOGGER)
    assert status == "FLAG", f"Expected FLAG near roll, got {status}"
    assert notes and "roll" in notes.lower(), f"Expected 'roll' in notes; got: {notes}"


# ---------------------------------------------------------------------------
# T14 — Manual SOFR load from file
# ---------------------------------------------------------------------------

def test_T14_manual_sofr_load():
    """SOFR3M loads correctly from manually placed CSV file."""
    from parse_gilr import load_sofr3m_manual

    content = "date,value\n2026-08-17,4.85\n2026-08-18,4.84\n"
    with tempfile.TemporaryDirectory() as tmpdir:
        raw_dir = Path(tmpdir)
        (raw_dir / "sofr3m.csv").write_text(content, encoding="utf-8")

        val, vintage, source = load_sofr3m_manual(raw_dir, date(2026, 8, 18), NULL_LOGGER)
        assert abs(val - 4.84) < 1e-6
        assert vintage == date(2026, 8, 18)
        assert source == "FRED_SOFR3M"


def test_T14_manual_sofr_uses_latest_on_or_before():
    """Uses latest date <= obs_date, not a future date."""
    from parse_gilr import load_sofr3m_manual

    content = "date,value\n2026-08-15,4.90\n2026-08-16,4.88\n"
    with tempfile.TemporaryDirectory() as tmpdir:
        raw_dir = Path(tmpdir)
        (raw_dir / "sofr3m.csv").write_text(content, encoding="utf-8")

        val, vintage, _ = load_sofr3m_manual(raw_dir, date(2026, 8, 18), NULL_LOGGER)
        assert abs(val - 4.88) < 1e-6
        assert vintage == date(2026, 8, 16)


# ---------------------------------------------------------------------------
# T15 — Nasdaq CME CSV parsing
# ---------------------------------------------------------------------------

def test_T15_nasdaq_csv_parse():
    """Correct settlement value extracted from Nasdaq CHRIS/CME_GC CSV format."""
    content = (
        "Date,Open,High,Low,Last,Volume,Open Int,Settle\n"
        "2026-08-17,2480.0,2490.0,2478.0,2485.0,12345,67890,2485.30\n"
        "2026-08-18,2485.0,2495.0,2483.0,2490.0,11111,66666,2490.50\n"
    )
    rows = parse_nasdaq_gc_csv(content, date(2026, 8, 18))
    assert len(rows) == 2
    assert abs(rows[-1][1] - 2490.50) < 1e-4


def test_T15_nasdaq_csv_filters_future_dates():
    """Rows after obs_date are excluded."""
    content = (
        "Date,Open,High,Low,Last,Volume,Open Int,Settle\n"
        "2026-08-17,2480.0,2490.0,2478.0,2485.0,1,1,2485.30\n"
        "2026-08-19,2490.0,2500.0,2488.0,2495.0,1,1,2495.00\n"
    )
    rows = parse_nasdaq_gc_csv(content, date(2026, 8, 18))
    assert len(rows) == 1
    assert abs(rows[0][1] - 2485.30) < 1e-4


def test_T15_missing_settle_column_raises():
    """Raises ValueError if 'settle' column not found."""
    content = "Date,Open,High,Low,Last\n2026-08-18,1,2,3,4\n"
    with pytest.raises(ValueError, match="settle"):
        parse_nasdaq_gc_csv(content, date(2026, 8, 18))
