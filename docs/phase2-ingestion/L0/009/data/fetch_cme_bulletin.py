"""
fetch_cme_bulletin.py — CME Daily Bulletin fetcher for L0-009
Fetches Section 62 (Metals) of the CME Daily Information Bulletin PDF,
extracts COMEX Gold (GC) settlement prices and expiry dates, and writes
cme_gc_settlement.csv in the exact format parse_gilr.py --manual expects,
so the two scripts chain directly:

    python fetch_cme_bulletin.py --date 2026-08-18 --out-dir raw/2026-08-18
    python parse_gilr.py --config config.yaml --date 2026-08-18 --manual

Output (in --out-dir):
    cme_gc_settlement.csv        date,front_contract,front_settle,far_contract,far_settle
    cme_gc_settlement_audit.csv  fuller record: expiries, span, source
    section62_raw.pdf            archived original bulletin

Dependencies:
    pypdf      (pip install pypdf)

No API key or login required. CME Daily Bulletin is a public document.
"""

import argparse
import csv
import io
import logging
import re
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

BULLETIN_URL = (
    "https://www.cmegroup.com/daily_bulletin/current/"
    "Section62_Metals_Futures_Products.pdf"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "application/pdf,application/octet-stream,*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.cmegroup.com/market-data/daily-bulletin.html",
    "Connection": "keep-alive",
}

DELIVERY_MONTHS = {
    "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
    "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12,
}
GC_DELIVERY_MONTHS = {2, 4, 6, 8, 10, 12}

MONTH_CODES = {
    1: "F", 2: "G", 3: "H", 4: "J", 5: "K", 6: "M",
    7: "N", 8: "Q", 9: "U", 10: "V", 11: "X", 12: "Z",
}


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(h)
    return logger


# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------

def fetch_bulletin_pdf(max_retries: int = 3, retry_delay: int = 5) -> bytes:
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(BULLETIN_URL, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                if len(data) < 10000:
                    raise ValueError(f"PDF suspiciously small: {len(data)} bytes")
                return data
        except Exception:
            if attempt == max_retries:
                raise
            time.sleep(retry_delay * attempt)


# ---------------------------------------------------------------------------
# Parse settlements
# ---------------------------------------------------------------------------

def extract_gc_text(pdf_bytes: bytes) -> tuple:
    try:
        from pypdf import PdfReader
    except ImportError:
        raise ImportError("pypdf is required: pip install pypdf")

    reader = PdfReader(io.BytesIO(pdf_bytes))
    page_texts = [page.extract_text() for page in reader.pages]
    full_text = "\n".join(page_texts)

    gc_start = full_text.find("GC FUT COMEX GOLD FUTURES")
    if gc_start < 0:
        raise ValueError("'GC FUT COMEX GOLD FUTURES' not found in bulletin PDF")
    gc_end = full_text.find("TOTAL GC FUT", gc_start)
    if gc_end < 0:
        gc_end = gc_start + 3000
    gc_block = full_text[gc_start:gc_end]

    gc_expiry_line = ""
    for text in page_texts:
        for m in re.finditer(r"GC FUT\s+([\d/\s]+)", text):
            candidate = m.group(0)
            if re.search(r"\d{2}/\d{2}", candidate):
                gc_expiry_line = candidate.strip()
                break
        if gc_expiry_line:
            break

    return gc_block, gc_expiry_line


def parse_gc_settlements(gc_block: str) -> list:
    """
    Returns list of dicts sorted by (year, month), GC delivery months only:
    [{"label": "AUG26", "month": 8, "year": 2026, "settle": 4366.0}, ...]
    """
    settle_re = re.compile(
        r"^([A-Z]{3})(\d{2})\s+.*?\d{2}\.\d{2}\s*(\d{4,5}\.\d{2})",
        re.MULTILINE,
    )
    results = []
    for m in settle_re.finditer(gc_block):
        month_str = m.group(1)
        yy = int(m.group(2))
        settle = float(m.group(3))
        month_num = DELIVERY_MONTHS.get(month_str)
        if month_num is None or month_num not in GC_DELIVERY_MONTHS:
            continue
        year = 2000 + yy
        results.append({
            "label":  f"{month_str}{m.group(2)}",
            "month":  month_num,
            "year":   year,
            "settle": settle,
        })

    results.sort(key=lambda x: (x["year"], x["month"]))
    return results


def parse_gc_expiries(gc_expiry_line: str, settlements: list) -> dict:
    """
    Parse MM/DD expiry dates from the bulletin expiry table line.

    IMPORTANT: the bulletin expiry table lists CONSECUTIVE calendar months
    (e.g. Aug, Sep, Oct, Nov, Dec, Jan, Feb, ...), not just the GC delivery
    months (Feb/Apr/Jun/Aug/Oct/Dec). Settlement rows exist only for delivery
    months. We build the full consecutive-month sequence starting from the
    first settlement's month, then select only entries matching a delivery-
    month settlement label. Never zip positionally against the settlement
    list directly — that causes silent misalignment.

    Returns {label: date}. Contracts beyond the bulletin's listed window
    (typically ~13 months) are correctly omitted rather than guessed.
    """
    dates_raw = re.findall(r"(\d{2})/(\d{2})", gc_expiry_line)
    if not dates_raw or not settlements:
        return {}

    start_month = settlements[0]["month"]
    start_year  = settlements[0]["year"]

    month_year_seq = []
    m, y = start_month, start_year
    for _ in dates_raw:
        month_year_seq.append((m, y))
        m += 1
        if m > 12:
            m = 1
            y += 1

    date_by_month_year = {}
    for (month, year), (mm_str, dd_str) in zip(month_year_seq, dates_raw):
        dd = int(dd_str)
        try:
            date_by_month_year[(month, year)] = date(year, month, dd)
        except ValueError:
            continue

    expiries = {}
    for c in settlements:
        key = (c["month"], c["year"])
        if key in date_by_month_year:
            expiries[c["label"]] = date_by_month_year[key]

    return expiries


# ---------------------------------------------------------------------------
# Contract selection
# ---------------------------------------------------------------------------

def select_contract_pair(
    settlements: list,
    expiries: dict,
    obs_date: date,
    min_days_to_expiry: int = 5,
    min_span: int = 60,
    max_span: int = 120,
) -> tuple:
    eligible = [
        c for c in settlements
        if c["label"] in expiries
        and (expiries[c["label"]] - obs_date).days >= min_days_to_expiry
    ]

    if len(eligible) < 2:
        raise ValueError(
            f"Not enough eligible contracts for {obs_date} "
            f"(found {len(eligible)}, need >= 2). Bulletin's expiry table "
            f"only covers ~13 months forward; contracts beyond that lack "
            f"expiry dates and are excluded."
        )

    for i, front in enumerate(eligible):
        front_exp = expiries[front["label"]]
        for far in eligible[i + 1:]:
            far_exp = expiries[far["label"]]
            span = (far_exp - front_exp).days
            if min_span <= span <= max_span:
                return (
                    front["label"], front["settle"], front_exp,
                    far["label"],   far["settle"],   far_exp,
                    span,
                )

    raise ValueError(
        f"No pair with span [{min_span}, {max_span}]d found for {obs_date}. "
        f"Eligible contracts: {[(c['label'], expiries[c['label']]) for c in eligible]}"
    )


def label_to_code(label: str) -> str:
    month_num = DELIVERY_MONTHS[label[:3]]
    return f"GC{MONTH_CODES[month_num]}{label[3:]}"


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def write_settlement_csv(out_path: Path, obs_date: date, front_code, front_settle,
                          far_code, far_settle):
    """
    Writes cme_gc_settlement.csv in the exact format expected by
    parse_gilr.py's --manual mode: date,front_contract,front_settle,far_contract,far_settle
    This lets fetch_cme_bulletin.py and parse_gilr.py chain directly.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "front_contract", "front_settle", "far_contract", "far_settle"])
        writer.writerow([str(obs_date), front_code, front_settle, far_code, far_settle])


def write_audit_csv(out_path: Path, obs_date: date,
                     front_code, front_settle, front_expiry,
                     far_code, far_settle, far_expiry, span):
    """Fuller audit record including expiry dates and span, for traceability."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "date", "front_contract", "front_settle", "front_expiry",
            "far_contract", "far_settle", "far_expiry", "span_days", "source"
        ])
        writer.writerow([
            str(obs_date),
            front_code, front_settle, str(front_expiry),
            far_code,   far_settle,   str(far_expiry),
            span,
            "CME_DAILY_BULLETIN_PDF",
        ])


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Fetch CME Daily Bulletin PDF and extract GC futures settlements"
    )
    ap.add_argument("--date",               required=True, help="Observation date YYYY-MM-DD")
    ap.add_argument("--out-dir",            required=True, help="Output directory (relative to script dir)")
    ap.add_argument("--min-span",           type=int, default=60)
    ap.add_argument("--max-span",           type=int, default=120)
    ap.add_argument("--min-days-to-expiry", type=int, default=5)
    args = ap.parse_args()

    obs_date = date.fromisoformat(args.date)
    out_dir  = SCRIPT_DIR / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    logger = setup_logger("cme_bulletin")
    logger.info(f"Fetching CME Bulletin for obs_date={obs_date}")

    pdf_bytes = fetch_bulletin_pdf()
    logger.info(f"Downloaded: {len(pdf_bytes):,} bytes")

    pdf_path = out_dir / "section62_raw.pdf"
    pdf_path.write_bytes(pdf_bytes)

    gc_block, gc_expiry_line = extract_gc_text(pdf_bytes)
    settlements = parse_gc_settlements(gc_block)
    expiries    = parse_gc_expiries(gc_expiry_line, settlements)

    logger.info(f"Settlements: {len(settlements)} GC delivery-month contracts")
    logger.info(f"Expiries mapped: {len(expiries)}")
    for c in settlements:
        exp = expiries.get(c["label"], "MISSING (beyond bulletin expiry table window)")
        logger.info(f"  {c['label']}: settle={c['settle']}, expiry={exp}")

    front_label, front_settle, front_expiry, \
    far_label,   far_settle,   far_expiry,   span = select_contract_pair(
        settlements, expiries, obs_date,
        args.min_days_to_expiry, args.min_span, args.max_span,
    )

    front_code = label_to_code(front_label)
    far_code   = label_to_code(far_label)

    logger.info(
        f"Selected: {front_code} (exp {front_expiry}, settle {front_settle}) / "
        f"{far_code} (exp {far_expiry}, settle {far_settle}), span={span}d"
    )

    csv_path = out_dir / "cme_gc_settlement.csv"
    write_settlement_csv(csv_path, obs_date, front_code, front_settle, far_code, far_settle)

    audit_path = out_dir / "cme_gc_settlement_audit.csv"
    write_audit_csv(
        audit_path, obs_date,
        front_code, front_settle, front_expiry,
        far_code,   far_settle,   far_expiry,
        span,
    )

    logger.info(f"Written: {csv_path}")
    logger.info(f"Written: {audit_path}")
    print(f"OK: {front_code}={front_settle}, {far_code}={far_settle}, span={span}d")


if __name__ == "__main__":
    main()
