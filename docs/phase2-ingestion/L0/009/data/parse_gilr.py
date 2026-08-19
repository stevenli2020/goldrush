"""
parse_gilr.py — L0-009 parser and collector
Fetches SOFR3M and CME COMEX gold futures settlements, computes the
3-month CME-derived Gold Implied Lease Rate proxy (GILR-CME), validates,
and appends to the processed store.

All paths resolved relative to this script's directory.

Usage (automated):
    python parse_gilr.py --config config.yaml --date 2026-08-18

Usage (manual fallback):
    python parse_gilr.py --config config.yaml --date 2026-08-18 --manual
    (expects raw/2026-08-18/sofr3m.csv and raw/2026-08-18/cme_gc_settlement.csv)

Usage (dry run):
    python parse_gilr.py --config config.yaml --date 2026-08-18 --dry-run
"""

import argparse
import csv
import io
import logging
import os
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import yaml

try:
    import urllib.request as urlrequest
except ImportError:
    urlrequest = None

PARSER_VERSION = "1.0.0"
VARIABLE_ID = "L0-009"
TENOR = "3M"

# COMEX gold futures month codes
MONTH_CODES = {
    "F": 1, "G": 2, "H": 3, "J": 4, "K": 5, "M": 6,
    "N": 7, "Q": 8, "U": 9, "V": 10, "X": 11, "Z": 12
}

SCRIPT_DIR = Path(__file__).parent


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging(log_path: Path) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("L0-009")
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s UTC | %(levelname)s | %(message)s")
    fmt.converter = lambda *_: datetime.now(timezone.utc).timetuple()
    if not logger.handlers:
        fh = logging.FileHandler(log_path, encoding="utf-8")
        fh.setFormatter(fmt)
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(fmt)
        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger


# ---------------------------------------------------------------------------
# HTTP fetch (no third-party dependencies)
# ---------------------------------------------------------------------------

def fetch_url(url: str, timeout: int = 30) -> str:
    """Fetch URL content as text using stdlib urllib."""
    with urlrequest.urlopen(url, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


# ---------------------------------------------------------------------------
# SOFR3M retrieval
# ---------------------------------------------------------------------------

def fetch_sofr3m(cfg: dict, obs_date: date, raw_dir: Path, logger: logging.Logger) -> tuple:
    """
    Returns (sofr_value: float, sofr_vintage_date: date, source: str).
    Saves raw CSV to raw_dir/sofr3m.csv.
    """
    raw_path = raw_dir / "sofr3m.csv"
    endpoint = cfg["sofr"]["endpoint"]
    logger.info(f"Fetching SOFR3M from {endpoint}")

    content = fetch_url(endpoint)
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(content, encoding="utf-8")

    # Parse CSV: rows are date,value; skip header
    rows = []
    for line in content.strip().splitlines():
        parts = line.strip().split(",")
        if len(parts) != 2:
            continue
        try:
            d = date.fromisoformat(parts[0])
            v = float(parts[1])
            rows.append((d, v))
        except (ValueError, TypeError):
            continue

    if not rows:
        raise ValueError("SOFR3M CSV contained no parseable rows")

    # Use latest row at or before obs_date
    eligible = [(d, v) for d, v in rows if d <= obs_date]
    if not eligible:
        raise ValueError(f"No SOFR3M data available on or before {obs_date}")

    vintage_date, value = max(eligible, key=lambda x: x[0])
    logger.info(f"SOFR3M: {value}% p.a. (vintage {vintage_date})")
    return value, vintage_date, cfg["sofr"]["source_label"]


def load_sofr3m_manual(raw_dir: Path, obs_date: date, logger: logging.Logger) -> tuple:
    """Load SOFR3M from manually placed raw file."""
    raw_path = raw_dir / "sofr3m.csv"
    if not raw_path.exists():
        raise FileNotFoundError(f"Manual SOFR3M file not found: {raw_path}")

    rows = []
    for line in raw_path.read_text(encoding="utf-8").strip().splitlines():
        parts = line.strip().split(",")
        if len(parts) != 2:
            continue
        try:
            rows.append((date.fromisoformat(parts[0]), float(parts[1])))
        except (ValueError, TypeError):
            continue

    eligible = [(d, v) for d, v in rows if d <= obs_date]
    if not eligible:
        raise ValueError(f"No SOFR3M data on or before {obs_date} in manual file")

    vintage_date, value = max(eligible, key=lambda x: x[0])
    logger.info(f"SOFR3M (manual): {value}% p.a. (vintage {vintage_date})")
    return value, vintage_date, "FRED_SOFR3M"


# ---------------------------------------------------------------------------
# CME contract expiry resolution
# ---------------------------------------------------------------------------

def nth_to_last_business_day(year: int, month: int, n: int) -> date:
    """
    Return the nth-to-last business day of the given month.
    n=1 means last business day; n=3 means third-to-last.
    """
    # Find last day of month
    if month == 12:
        last = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last = date(year, month + 1, 1) - timedelta(days=1)

    count = 0
    d = last
    while True:
        if d.weekday() < 5:  # Mon-Fri
            count += 1
            if count == n:
                return d
        d -= timedelta(days=1)


def contract_expiry(code: str) -> date:
    """
    Resolve COMEX gold futures contract code (e.g. GCQ26) to its expiry date.
    Expiry = third-to-last business day of the delivery month.
    """
    m = re.match(r"^GC([FGHJKMNQUVXZ])(\d{2})$", code)
    if not m:
        raise ValueError(f"Cannot parse contract code: {code}")
    month = MONTH_CODES[m.group(1)]
    year = 2000 + int(m.group(2))
    return nth_to_last_business_day(year, month, 3)


# ---------------------------------------------------------------------------
# CME settlement retrieval
# ---------------------------------------------------------------------------

def fetch_cme_settlements(cfg: dict, obs_date: date, raw_dir: Path,
                           logger: logging.Logger) -> tuple:
    """
    Returns (gc1_rows, gc2_rows) each as list of (date, settle, contract_code).
    Saves raw CSVs.
    """
    results = {}
    for label, series in [("gc1", cfg["cme"]["front_series"]),
                           ("gc2", cfg["cme"]["far_series"])]:
        url = cfg["cme"]["endpoint_pattern"].format(series=series)
        api_key = os.environ.get("NASDAQ_API_KEY", "")
        if api_key:
            url += f"&api_key={api_key}"
        logger.info(f"Fetching CME {series} from {url}")

        content = fetch_url(url)
        raw_path = raw_dir / f"cme_{label}.csv"
        raw_path.write_text(content, encoding="utf-8")

        rows = parse_nasdaq_gc_csv(content, obs_date)
        results[label] = rows
        logger.info(f"CME {series}: {len(rows)} rows parsed; latest = {rows[-1] if rows else 'none'}")

    return results["gc1"], results["gc2"]


def parse_nasdaq_gc_csv(content: str, obs_date: date) -> list:
    """
    Parse Nasdaq Data Link CHRIS/CME_GC CSV.
    Returns list of (date, settle_price) for dates <= obs_date, sorted ascending.
    Nasdaq CHRIS format columns: Date, Open, High, Low, Last, Volume, Open Int, Settle (index 7).
    """
    rows = []
    reader = csv.reader(io.StringIO(content))
    header = next(reader, None)
    if header is None:
        return rows

    # Locate Date and Settle columns
    header_lower = [h.strip().lower() for h in header]
    try:
        date_col = header_lower.index("date")
        settle_col = next(i for i, h in enumerate(header_lower) if "settle" in h)
    except (ValueError, StopIteration):
        raise ValueError(f"Expected 'date' and 'settle' columns; got: {header}")

    for row in reader:
        if len(row) <= max(date_col, settle_col):
            continue
        try:
            d = date.fromisoformat(row[date_col].strip())
            v = float(row[settle_col].strip())
            if d <= obs_date:
                rows.append((d, v))
        except (ValueError, TypeError):
            continue

    rows.sort(key=lambda x: x[0])
    return rows


def load_cme_manual(raw_dir: Path, obs_date: date, cfg: dict,
                    logger: logging.Logger) -> tuple:
    """
    Load CME settlement from manually placed file.
    Expected: raw_dir/cme_gc_settlement.csv with columns:
        date, front_contract, front_settle, far_contract, far_settle
    """
    raw_path = raw_dir / "cme_gc_settlement.csv"
    if not raw_path.exists():
        raise FileNotFoundError(f"Manual CME file not found: {raw_path}")

    with open(raw_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                d = date.fromisoformat(row["date"].strip())
                if d == obs_date:
                    front_code    = row["front_contract"].strip()
                    front_settle  = float(row["front_settle"].strip())
                    far_code      = row["far_contract"].strip()
                    far_settle    = float(row["far_settle"].strip())
                    logger.info(f"CME manual: {front_code}={front_settle}, {far_code}={far_settle}")
                    return front_code, front_settle, far_code, far_settle
            except (KeyError, ValueError, TypeError):
                continue

    raise ValueError(f"No manual CME row found for {obs_date}")


# ---------------------------------------------------------------------------
# Contract pair selection
# ---------------------------------------------------------------------------

def select_contract_pair(gc1_rows: list, gc2_rows: list, obs_date: date,
                          cfg: dict, logger: logging.Logger) -> tuple:
    """
    From GC1 and GC2 settlement rows, identify front and far contracts.

    Nasdaq CHRIS/CME_GC1 provides the continuous front-month series (rolled);
    CHRIS/CME_GC2 provides the continuous second-month series.

    Returns (front_code, front_settle, front_expiry, far_code, far_settle, far_expiry, days).
    """
    sel = cfg["contract_selection"]

    # Get latest available settlement for obs_date
    gc1_latest = next((s for d, s in reversed(gc1_rows) if d <= obs_date), None)
    gc2_latest = next((s for d, s in reversed(gc2_rows) if d <= obs_date), None)

    if gc1_latest is None or gc2_latest is None:
        raise ValueError(f"No CME settlement data available for {obs_date}")

    # For continuous series, contract codes must be inferred from the delivery calendar
    # The continuous series GC1 = front month; GC2 = second month
    # We identify which actual contract GC1/GC2 corresponds to on obs_date
    front_code, far_code = infer_active_contracts(obs_date, sel)

    front_expiry = contract_expiry(front_code)
    far_expiry   = contract_expiry(far_code)
    days         = (far_expiry - front_expiry).days

    # Validate span
    if not (sel["min_span_days"] <= days <= sel["max_span_days"]):
        raise ValueError(
            f"Contract span {days} days outside [{sel['min_span_days']}, "
            f"{sel['max_span_days']}] for pair {front_code}/{far_code}"
        )

    logger.info(
        f"Contract pair: {front_code} (exp {front_expiry}, settle {gc1_latest}) / "
        f"{far_code} (exp {far_expiry}, settle {gc2_latest}); span={days}d"
    )
    return front_code, gc1_latest, front_expiry, far_code, gc2_latest, far_expiry, days


def infer_active_contracts(obs_date: date, sel: dict) -> tuple:
    """
    Determine which COMEX gold delivery month contracts are active as front and far
    on obs_date, respecting the minimum days-to-expiry rule.
    Returns (front_code, far_code) as strings like 'GCQ26'.
    """
    delivery_months = sel["delivery_months"]
    min_days = sel["front_min_days_to_expiry"]

    # Generate candidate contracts: current year ±1 year
    candidates = []
    for year in [obs_date.year - 1, obs_date.year, obs_date.year + 1]:
        for month in delivery_months:
            try:
                exp = nth_to_last_business_day(year, month, 3)
                if (exp - obs_date).days >= min_days:
                    # Build contract code
                    month_code = next(k for k, v in MONTH_CODES.items() if v == month)
                    code = f"GC{month_code}{str(year)[-2:]}"
                    candidates.append((exp, code))
            except Exception:
                continue

    candidates.sort(key=lambda x: x[0])
    if len(candidates) < 2:
        raise ValueError(f"Cannot find two valid delivery contracts from {obs_date}")

    # Front = earliest candidate; far = next candidate within span window
    front_exp, front_code = candidates[0]
    target = sel["target_span_days"]
    min_s  = sel["min_span_days"]
    max_s  = sel["max_span_days"]

    for far_exp, far_code in candidates[1:]:
        days = (far_exp - front_exp).days
        if min_s <= days <= max_s:
            return front_code, far_code

    raise ValueError(
        f"No far contract within [{min_s}, {max_s}] days of front {front_code} (exp {front_exp})"
    )


# ---------------------------------------------------------------------------
# GILR computation
# ---------------------------------------------------------------------------

def compute_gilr(sofr: float, front_settle: float, far_settle: float, days: int) -> tuple:
    """
    Returns (cme_forward_rate_pct_pa, gilr_cme_pct_pa).
    Formula: CME forward = ((far/front) - 1) * (360/days) * 100
             GILR-CME = SOFR3M - CME forward rate
    """
    cme_fwd = ((far_settle / front_settle) - 1) * (360 / days) * 100
    gilr    = sofr - cme_fwd
    return round(cme_fwd, 6), round(gilr, 6)


def verify_computation(gilr_stored: float, sofr: float, front: float,
                        far: float, days: int, tolerance: float) -> bool:
    """Recompute and verify stored GILR matches within tolerance."""
    _, gilr_check = compute_gilr(sofr, front, far, days)
    return abs(gilr_stored - gilr_check) <= tolerance


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_record(rec: dict, cfg: dict, logger: logging.Logger) -> tuple:
    vcfg = cfg["validation"]
    notes = []
    status = "PASS"

    sofr  = rec["sofr_3m_pct_pa"]
    gilr  = rec["gilr_cme_pct_pa"]
    days  = rec["days_between_contracts"]
    front = rec["cme_front_settlement"]
    far   = rec["cme_far_settlement"]

    # 1. SOFR non-negative
    if sofr < vcfg["sofr_fail_threshold_pct_pa"]:
        return "FAIL", f"SOFR3M={sofr}% below FAIL threshold {vcfg['sofr_fail_threshold_pct_pa']}%"
    if sofr < vcfg["sofr_min_pct_pa"]:
        notes.append(f"SOFR3M={sofr}% is negative (unusual policy environment)")
        status = "FLAG"

    # 2. Settlements positive
    if front <= 0 or far <= 0:
        return "FAIL", f"Settlement prices must be > 0; got front={front}, far={far}"

    # 3. Settlement ratio
    ratio = far / front
    if not (vcfg["settlement_ratio_min"] <= ratio <= vcfg["settlement_ratio_max"]):
        notes.append(f"far/front ratio={ratio:.4f} outside [{vcfg['settlement_ratio_min']}, {vcfg['settlement_ratio_max']}]")
        status = "FLAG"

    # 4. Contract ordering
    front_exp = date.fromisoformat(rec["cme_front_expiry"])
    far_exp   = date.fromisoformat(rec["cme_far_expiry"])
    if far_exp <= front_exp:
        return "FAIL", f"far_expiry {far_exp} must be after front_expiry {front_exp}"

    # 5. Day span
    if not (60 <= days <= 120):
        return "FAIL", f"days_between_contracts={days} outside [60, 120]"

    # 6. SOFR vintage not forward-dated
    obs  = date.fromisoformat(rec["observation_date"])
    vint = date.fromisoformat(rec["sofr_vintage_date"])
    if vint > obs:
        return "FAIL", f"sofr_vintage_date={vint} is after observation_date={obs}"

    # 7. Derived calculation reconciliation
    tol = cfg["calculation"]["reconciliation_tolerance_pct"]
    if not verify_computation(gilr, sofr, front, far, days, tol):
        _, expected = compute_gilr(sofr, front, far, days)
        return "FAIL", f"GILR recomputation mismatch: stored={gilr}, recomputed={expected}"

    # 8. Negative GILR
    if gilr < 0:
        notes.append(
            f"Negative GILR-CME ({gilr:.4f}% p.a.) indicates backwardation or tight "
            "physical financing conditions; economically valid"
        )
        status = "FLAG"

    # 9. GILR outside broad range
    if not (vcfg["gilr_flag_min_pct_pa"] <= gilr <= vcfg["gilr_flag_max_pct_pa"]):
        notes.append(
            f"GILR-CME={gilr:.4f}% outside broad historical range "
            f"[{vcfg['gilr_flag_min_pct_pa']}, {vcfg['gilr_flag_max_pct_pa']}]"
        )
        status = "FLAG"

    # 10. Contract roll proximity
    obs_date = date.fromisoformat(rec["observation_date"])
    days_to_front_exp = (front_exp - obs_date).days
    if days_to_front_exp <= cfg["contract_selection"]["roll_proximity_flag_days"]:
        notes.append(
            f"Front contract expires in {days_to_front_exp} days; "
            "near roll date — proxy may show transient basis effects"
        )
        status = "FLAG"

    return status, ("; ".join(notes) if notes else None)


# ---------------------------------------------------------------------------
# Processed store
# ---------------------------------------------------------------------------

FIELDNAMES = [
    "variable_id", "observation_date", "tenor",
    "gilr_cme_pct_pa", "sofr_3m_pct_pa", "sofr_vintage_date", "sofr_source",
    "cme_implied_forward_rate_pct_pa",
    "cme_front_contract", "cme_front_settlement", "cme_front_expiry",
    "cme_far_contract", "cme_far_settlement", "cme_far_expiry",
    "days_between_contracts", "cme_source",
    "ingested_at", "parser_version",
    "is_revised", "prior_gilr_cme_pct_pa", "revision_reason",
    "validation_status", "availability_status", "anomaly_notes",
]


def load_existing(processed_path: Path) -> dict:
    """Returns {observation_date_str: gilr_cme_pct_pa}."""
    existing = {}
    if not processed_path.exists():
        return existing
    with open(processed_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            d = row.get("observation_date")
            v = row.get("gilr_cme_pct_pa")
            if d and v:
                try:
                    existing[d] = float(v)
                except ValueError:
                    pass
    return existing


def append_record(rec: dict, processed_path: Path):
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not processed_path.exists()
    with open(processed_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerow(rec)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="L0-009 GILR-CME parser")
    ap.add_argument("--config",  required=True, help="Path to config.yaml (relative to script dir)")
    ap.add_argument("--date",    required=True, help="Observation date YYYY-MM-DD")
    ap.add_argument("--manual",  action="store_true", help="Use manually placed raw files")
    ap.add_argument("--dry-run", action="store_true", help="Parse and validate; do not write output")
    args = ap.parse_args()

    obs_date = date.fromisoformat(args.date)

    config_path = SCRIPT_DIR / args.config
    with open(config_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    log_path       = SCRIPT_DIR / "archive" / "ingest.log"
    processed_path = SCRIPT_DIR / "processed" / "L0_009_observations.csv"
    raw_dir        = SCRIPT_DIR / "raw" / str(obs_date)

    logger = setup_logging(log_path)
    logger.info(f"--- L0-009 run: observation_date={obs_date} manual={args.manual} ---")

    raw_dir.mkdir(parents=True, exist_ok=True)
    existing = load_existing(processed_path)

    # Fetch or load SOFR3M
    if args.manual:
        sofr_val, sofr_vintage, sofr_source = load_sofr3m_manual(raw_dir, obs_date, logger)
    else:
        sofr_val, sofr_vintage, sofr_source = fetch_sofr3m(cfg, obs_date, raw_dir, logger)

    # Fetch or load CME settlements
    if args.manual:
        front_code, front_settle, far_code, far_settle = load_cme_manual(
            raw_dir, obs_date, cfg, logger
        )
        front_expiry = contract_expiry(front_code)
        far_expiry   = contract_expiry(far_code)
        days         = (far_expiry - front_expiry).days
        cme_source   = cfg["cme"]["source_label_manual"]

        if not (60 <= days <= 120):
            logger.error(f"Manual contract span {days}d outside [60, 120]; aborting")
            sys.exit(2)
    else:
        gc1_rows, gc2_rows = fetch_cme_settlements(cfg, obs_date, raw_dir, logger)
        front_code, front_settle, front_expiry, far_code, far_settle, far_expiry, days = \
            select_contract_pair(gc1_rows, gc2_rows, obs_date, cfg, logger)
        cme_source = cfg["cme"]["source_label_auto"]

    # Compute GILR
    cme_fwd, gilr = compute_gilr(sofr_val, front_settle, far_settle, days)
    logger.info(
        f"SOFR3M={sofr_val}%, CME_fwd={cme_fwd}%, GILR-CME={gilr}% p.a."
    )

    # Revision check
    prior = existing.get(str(obs_date))
    is_revised = prior is not None and abs(gilr - prior) > 1e-6
    ingested_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    rec = {
        "variable_id":                    VARIABLE_ID,
        "observation_date":               str(obs_date),
        "tenor":                          TENOR,
        "gilr_cme_pct_pa":                gilr,
        "sofr_3m_pct_pa":                 sofr_val,
        "sofr_vintage_date":              str(sofr_vintage),
        "sofr_source":                    sofr_source,
        "cme_implied_forward_rate_pct_pa": cme_fwd,
        "cme_front_contract":             front_code,
        "cme_front_settlement":           front_settle,
        "cme_front_expiry":               str(front_expiry),
        "cme_far_contract":               far_code,
        "cme_far_settlement":             far_settle,
        "cme_far_expiry":                 str(far_expiry),
        "days_between_contracts":         days,
        "cme_source":                     cme_source,
        "ingested_at":                    ingested_at,
        "parser_version":                 PARSER_VERSION,
        "is_revised":                     is_revised,
        "prior_gilr_cme_pct_pa":         prior if is_revised else None,
        "revision_reason": (
            f"GILR changed from {prior:.6f}% to {gilr:.6f}% on re-run"
            if is_revised else None
        ),
        "validation_status":  None,
        "availability_status": None,
        "anomaly_notes":       None,
    }

    status, notes = validate_record(rec, cfg, logger)
    rec["validation_status"]  = status
    rec["availability_status"] = "AVAILABLE" if status in ("PASS", "FLAG") else "INCOMPLETE"
    rec["anomaly_notes"]       = notes

    logger.info(f"Validation: {status}" + (f" — {notes}" if notes else ""))

    if status == "FAIL":
        logger.error("FAIL — record not written.")
        sys.exit(2)

    if args.dry_run:
        logger.info("Dry run — no output written.")
        return

    append_record(rec, processed_path)
    logger.info(f"Appended record for {obs_date} to {processed_path}")


if __name__ == "__main__":
    main()
