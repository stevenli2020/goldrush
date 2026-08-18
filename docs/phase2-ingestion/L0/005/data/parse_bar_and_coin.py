"""
parse_bar_and_coin.py — L0-005 parser
Extracts bar-and-coin demand data from WGC Gold Demand Trends quarterly workbook.

Usage:
    python parse_bar_and_coin.py \\
        --workbook gold-demand-trends/GDT_Tables_Q2\\'26_EN.xlsx \\
        --config config.yaml \\
        --publication-date 2026-08-07 \\
        --download-date 2026-08-18

Output:
    Appends records to processed/L0_005_observations.csv
    Logs run to archive/ingest.log
"""

import argparse
import csv
import hashlib
import json
import logging
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import openpyxl
import yaml

PARSER_VERSION = "1.0.0"
VARIABLE_ID = "L0-005"
UNDERLYING_PROVIDERS = (
    "Metals Focus; Refinitiv GFMS; ICE Benchmark Administration; World Gold Council"
)

ANNUAL_PATTERN = re.compile(r"^\d{4}$")
QUARTERLY_PATTERN = re.compile(r"^Q([1-4])'(\d{2})$")


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging(log_path: Path) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("L0-005")
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s UTC | %(levelname)s | %(message)s")
    fmt.converter = lambda *_: datetime.now(timezone.utc).timetuple()
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


# ---------------------------------------------------------------------------
# SHA-256
# ---------------------------------------------------------------------------

def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Workbook loading and column detection
# ---------------------------------------------------------------------------

def load_workbook(path: Path) -> openpyxl.Workbook:
    return openpyxl.load_workbook(path, read_only=True, data_only=True)


def detect_period_columns(ws, header_row: int) -> dict:
    """
    Returns {period_label: col_index} for all annual and quarterly columns.
    Detects positions dynamically from the header row; never hardcodes indices.
    """
    cols = {}
    headers = next(
        ws.iter_rows(min_row=header_row, max_row=header_row, values_only=True)
    )
    for idx, val in enumerate(headers):
        if val is None:
            continue
        label = str(val).strip() if not isinstance(val, int) else str(int(val))
        if ANNUAL_PATTERN.match(label):
            cols[label] = idx
        elif QUARTERLY_PATTERN.match(label):
            cols[label] = idx
    return cols


def get_row_values(ws, row_num: int) -> list:
    """Return all cell values for a given 1-based row number."""
    rows = list(ws.iter_rows(min_row=row_num, max_row=row_num, values_only=True))
    if not rows:
        raise ValueError(f"Row {row_num} not found in sheet '{ws.title}'")
    return list(rows[0])


# ---------------------------------------------------------------------------
# Period label → year / quarter
# ---------------------------------------------------------------------------

def parse_period(label: str):
    """Returns (year: int, quarter: int|None, period_type: str)."""
    if ANNUAL_PATTERN.match(label):
        return int(label), None, "annual"
    m = QUARTERLY_PATTERN.match(label)
    if m:
        q = int(m.group(1))
        yy = int(m.group(2))
        year = 2000 + yy
        return year, q, "quarterly"
    raise ValueError(f"Unrecognised period label: '{label}'")


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

def extract_gold_balance(wb: openpyxl.Workbook, cfg: dict, period_cols: dict) -> dict:
    """
    Extract rows 20-23 from Gold Balance sheet.
    Returns {period_label: {field: value}} for all detected periods.
    """
    sheet_cfg = cfg["extraction"]["gold_balance_sheet"]
    sheet_name = sheet_cfg["sheet_name"]
    if sheet_name not in wb.sheetnames:
        raise ValueError(f"Sheet '{sheet_name}' not found. Available: {wb.sheetnames}")

    ws = wb[sheet_name]
    header_row = sheet_cfg["header_row"]
    cols = detect_period_columns(ws, header_row)

    rows_cfg = sheet_cfg["targets"]
    row_map = {
        "total_bar_and_coin_tonnes": rows_cfg["total_bar_and_coin"]["row"],
        "bar_demand_tonnes":         rows_cfg["bars"]["row"],
        "official_coin_demand_tonnes": rows_cfg["official_coins"]["row"],
        "medals_imitation_coin_tonnes": rows_cfg["medals_imitation_coins"]["row"],
    }

    # Read all target rows once
    row_data = {}
    for field, rnum in row_map.items():
        row_data[field] = get_row_values(ws, rnum)

    result = {}
    for label, col_idx in cols.items():
        _, _, ptype = parse_period(label)
        rec = {"total_bar_and_coin_tonnes": row_data["total_bar_and_coin_tonnes"][col_idx]}
        if ptype == "annual":
            rec["bar_demand_tonnes"] = row_data["bar_demand_tonnes"][col_idx]
            rec["official_coin_demand_tonnes"] = row_data["official_coin_demand_tonnes"][col_idx]
            rec["medals_imitation_coin_tonnes"] = row_data["medals_imitation_coin_tonnes"][col_idx]
        else:
            rec["bar_demand_tonnes"] = None
            rec["official_coin_demand_tonnes"] = None
            rec["medals_imitation_coin_tonnes"] = None
        result[label] = rec

    return result


def extract_bar_and_coin_sheet(wb: openpyxl.Workbook, cfg: dict) -> dict:
    """
    Extract rows 44-46 from Bar and Coin sheet.
    Returns {period_label: {field: value}}.
    """
    sheet_cfg = cfg["extraction"]["bar_and_coin_sheet"]
    sheet_name = sheet_cfg["sheet_name"]
    if sheet_name not in wb.sheetnames:
        raise ValueError(f"Sheet '{sheet_name}' not found. Available: {wb.sheetnames}")

    ws = wb[sheet_name]
    header_row = sheet_cfg["header_row"]
    cols = detect_period_columns(ws, header_row)

    targets = sheet_cfg["targets"]
    row_named  = get_row_values(ws, targets["named_country_total"]["row"])
    row_other  = get_row_values(ws, targets["other_and_stock_change"]["row"])
    row_world  = get_row_values(ws, targets["world_total"]["row"])

    result = {}
    for label, col_idx in cols.items():
        result[label] = {
            "named_country_total_tonnes":           row_named[col_idx],
            "other_and_stock_change_tonnes":        row_other[col_idx],
            "world_total_bar_and_coin_sheet_tonnes": row_world[col_idx],
        }
    return result


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_record(rec: dict, cfg: dict, logger: logging.Logger) -> tuple:
    """
    Returns (validation_status, anomaly_notes).
    validation_status: "PASS" | "FLAG" | "FAIL"
    """
    vcfg = cfg["validation"]
    notes = []
    status = "PASS"

    total = rec.get("total_bar_and_coin_tonnes")
    ptype = rec["observation_period_type"]

    # 1. Global total non-negative
    if total is None or total < vcfg["global_total_min"]:
        return "FAIL", f"total_bar_and_coin_tonnes={total} is None or negative"

    # 2. Plausible range
    rng = vcfg["annual_plausible_range"] if ptype == "annual" else vcfg["quarterly_plausible_range"]
    if not (rng["min"] <= total <= rng["max"]):
        notes.append(
            f"total_bar_and_coin_tonnes={total:.5f} outside plausible {ptype} range "
            f"[{rng['min']}, {rng['max']}]t"
        )
        status = "FLAG"

    # 3. Sub-component consistency (annual only)
    if ptype == "annual":
        bar   = rec.get("bar_demand_tonnes")
        coins = rec.get("official_coin_demand_tonnes")
        medals = rec.get("medals_imitation_coin_tonnes")
        if all(v is not None for v in [bar, coins, medals]):
            comp_sum = bar + coins + medals
            diff_pct = abs(comp_sum - total) / total * 100 if total else 0
            if diff_pct > vcfg["subcomponent_fail_threshold_pct"]:
                return "FAIL", (
                    f"Sub-component sum {comp_sum:.5f} differs from total {total:.5f} "
                    f"by {diff_pct:.2f}% (exceeds FAIL threshold "
                    f"{vcfg['subcomponent_fail_threshold_pct']}%)"
                )
            if diff_pct > vcfg["subcomponent_tolerance_pct"]:
                notes.append(
                    f"Sub-component sum {comp_sum:.5f} differs from total {total:.5f} "
                    f"by {diff_pct:.2f}%"
                )
                status = "FLAG"

    # 4. Sheet reconciliation
    world = rec.get("world_total_bar_and_coin_sheet_tonnes")
    if world is not None and total:
        diff_pct = abs(world - total) / total * 100
        if diff_pct > vcfg["sheet_reconciliation_tolerance_pct"]:
            notes.append(
                f"Bar and Coin sheet world_total={world:.5f} differs from "
                f"Gold Balance total={total:.5f} by {diff_pct:.4f}%"
            )
            status = "FLAG"

    # 5. Period label format
    label = rec["observation_period"]
    if not (ANNUAL_PATTERN.match(label) or QUARTERLY_PATTERN.match(label)):
        return "FAIL", f"Period label '{label}' does not match expected format"

    anomaly_notes = "; ".join(notes) if notes else None
    return status, anomaly_notes


# ---------------------------------------------------------------------------
# Revision detection
# ---------------------------------------------------------------------------

def load_existing_records(processed_path: Path) -> dict:
    """
    Returns {observation_period: total_bar_and_coin_tonnes} from existing CSV.
    """
    existing = {}
    if not processed_path.exists():
        return existing
    with open(processed_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            period = row.get("observation_period")
            total = row.get("total_bar_and_coin_tonnes")
            if period and total:
                try:
                    existing[period] = float(total)
                except ValueError:
                    pass
    return existing


# ---------------------------------------------------------------------------
# Record assembly
# ---------------------------------------------------------------------------

def assemble_records(
    gb_data: dict,
    bc_data: dict,
    workbook_name: str,
    sha256: str,
    publication_date: str,
    download_date: str,
    ingested_at: str,
    existing: dict,
    cfg: dict,
    logger: logging.Logger,
) -> list:
    """Merge Gold Balance and Bar and Coin sheet data into observation records."""
    records = []

    all_periods = sorted(
        set(gb_data.keys()) | set(bc_data.keys()),
        key=lambda p: (parse_period(p)[0], parse_period(p)[1] or 0),
    )

    for label in all_periods:
        if label not in gb_data:
            logger.warning(f"Period {label} in Bar and Coin sheet but not Gold Balance — skipping")
            continue

        year, quarter, ptype = parse_period(label)
        gb = gb_data[label]
        bc = bc_data.get(label, {})

        # Revision detection
        prior_total = existing.get(label)
        total = gb["total_bar_and_coin_tonnes"]
        is_revised = False
        prior_sha = None
        revision_reason = None

        if prior_total is not None and total is not None:
            if abs(float(total) - float(prior_total)) > 1e-6:
                is_revised = True
                prior_sha = "see_prior_workbook_sha256_in_prior_record"
                revision_reason = (
                    f"Value changed from {prior_total:.5f}t to {total:.5f}t "
                    f"in workbook {workbook_name}"
                )

        rec = {
            "variable_id": VARIABLE_ID,
            "observation_period": label,
            "observation_period_type": ptype,
            "observation_year": year,
            "observation_quarter": quarter,
            "bar_demand_tonnes": gb.get("bar_demand_tonnes"),
            "official_coin_demand_tonnes": gb.get("official_coin_demand_tonnes"),
            "medals_imitation_coin_tonnes": gb.get("medals_imitation_coin_tonnes"),
            "total_bar_and_coin_tonnes": total,
            "named_country_total_tonnes": bc.get("named_country_total_tonnes"),
            "other_and_stock_change_tonnes": bc.get("other_and_stock_change_tonnes"),
            "world_total_bar_and_coin_sheet_tonnes": bc.get("world_total_bar_and_coin_sheet_tonnes"),
            "unit": "metric_tonnes",
            "source_name": "WGC_GDT",
            "source_workbook": workbook_name,
            "source_publication_date": publication_date,
            "download_date": download_date,
            "workbook_sha256": sha256,
            "ingested_at": ingested_at,
            "parser_version": PARSER_VERSION,
            "underlying_providers": UNDERLYING_PROVIDERS,
            "is_revised": is_revised,
            "prior_workbook_sha256": prior_sha,
            "prior_total_bar_and_coin_tonnes": prior_total if is_revised else None,
            "revision_reason": revision_reason,
            "validation_status": None,
            "availability_status": None,
            "anomaly_notes": None,
        }

        status, notes = validate_record(rec, cfg, logger)
        rec["validation_status"] = status
        rec["availability_status"] = "AVAILABLE" if status in ("PASS", "FLAG") else "INCOMPLETE"
        rec["anomaly_notes"] = notes

        records.append(rec)

    return records


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

FIELDNAMES = [
    "variable_id", "observation_period", "observation_period_type",
    "observation_year", "observation_quarter",
    "bar_demand_tonnes", "official_coin_demand_tonnes", "medals_imitation_coin_tonnes",
    "total_bar_and_coin_tonnes",
    "named_country_total_tonnes", "other_and_stock_change_tonnes",
    "world_total_bar_and_coin_sheet_tonnes",
    "unit", "source_name", "source_workbook",
    "source_publication_date", "download_date", "workbook_sha256",
    "ingested_at", "parser_version", "underlying_providers",
    "is_revised", "prior_workbook_sha256", "prior_total_bar_and_coin_tonnes",
    "revision_reason", "validation_status", "availability_status", "anomaly_notes",
]


def append_to_csv(records: list, processed_path: Path):
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not processed_path.exists()
    with open(processed_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerows(records)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="L0-005 Bar-and-Coin parser")
    parser.add_argument("--workbook",          required=True, help="Path to GDT .xlsx workbook")
    parser.add_argument("--config",            required=True, help="Path to config.yaml")
    parser.add_argument("--publication-date",  required=True, help="WGC publication date YYYY-MM-DD")
    parser.add_argument("--download-date",     required=True, help="Operator download date YYYY-MM-DD")
    parser.add_argument("--dry-run",           action="store_true", help="Parse and validate; do not write output")
    args = parser.parse_args()

    with open(args.config, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    log_path = Path(cfg["storage"]["log_path"])
    logger = setup_logging(log_path)

    workbook_path = Path(args.workbook)
    if not workbook_path.exists():
        logger.error(f"Workbook not found: {workbook_path}")
        sys.exit(1)

    logger.info(f"Workbook: {workbook_path.name}")
    sha256 = sha256_of_file(workbook_path)
    logger.info(f"SHA-256: {sha256}")

    ingested_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    processed_path = Path(cfg["storage"]["processed_path"])

    # Load existing records for revision detection
    existing = load_existing_records(processed_path)
    logger.info(f"Existing periods in processed store: {len(existing)}")

    # Load workbook
    wb = load_workbook(workbook_path)

    # Extract
    logger.info("Extracting Gold Balance sheet...")
    gb_data = extract_gold_balance(wb, cfg, {})
    annual_count   = sum(1 for l in gb_data if ANNUAL_PATTERN.match(l))
    quarterly_count = sum(1 for l in gb_data if QUARTERLY_PATTERN.match(l))
    logger.info(f"Gold Balance: {annual_count} annual, {quarterly_count} quarterly periods")

    logger.info("Extracting Bar and Coin sheet...")
    bc_data = extract_bar_and_coin_sheet(wb, cfg)

    # Assemble and validate
    records = assemble_records(
        gb_data, bc_data,
        workbook_path.name,
        sha256,
        args.publication_date,
        args.download_date,
        ingested_at,
        existing,
        cfg,
        logger,
    )

    n_pass  = sum(1 for r in records if r["validation_status"] == "PASS")
    n_flag  = sum(1 for r in records if r["validation_status"] == "FLAG")
    n_fail  = sum(1 for r in records if r["validation_status"] == "FAIL")
    n_rev   = sum(1 for r in records if r["is_revised"])
    n_annual    = sum(1 for r in records if r["observation_period_type"] == "annual")
    n_quarterly = sum(1 for r in records if r["observation_period_type"] == "quarterly")

    logger.info(
        f"Records assembled: {len(records)} total "
        f"({n_annual} annual, {n_quarterly} quarterly)"
    )
    logger.info(f"Validation: {n_pass} PASS, {n_flag} FLAG, {n_fail} FAIL")
    logger.info(f"Revisions detected: {n_rev}")

    if n_fail > 0:
        for r in records:
            if r["validation_status"] == "FAIL":
                logger.error(
                    f"FAIL — {r['observation_period']}: {r['anomaly_notes']}"
                )
        logger.error("FAIL records present. Output not written. Resolve before re-running.")
        sys.exit(2)

    if n_flag > 0:
        for r in records:
            if r["validation_status"] == "FLAG":
                logger.warning(
                    f"FLAG — {r['observation_period']}: {r['anomaly_notes']}"
                )
        logger.warning("FLAG records require operator review before scoring.")

    if args.dry_run:
        logger.info("Dry run — no output written.")
        return

    append_to_csv(records, processed_path)
    logger.info(f"Appended {len(records)} records to {processed_path}")


if __name__ == "__main__":
    main()
