"""Parse Treasury Monthly Treasury Statement Table 3 for L4-008."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

VARIABLE_ID = "L4-008"
PARSER_VERSION = "0.1.0"
ENDPOINT = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/mts/mts_table_3"
REQUIRED = {
    "130": "Total Receipts",
    "360": "Interest on Treasury Debt Securities (Gross)",
}
OUTPUT_FIELDS = [
    "variable_id", "observation_date", "fiscal_year", "gross_interest_expense_usd",
    "total_receipts_usd", "interest_expense_to_revenue_pct", "unit", "accounting_convention",
    "source_name", "endpoint", "query", "raw_file_paths", "manifest_path", "source_sha256",
    "retrieved_at", "validation_status", "availability_status", "parser_version",
]


def _load_manifest(path: Path) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("endpoint") != ENDPOINT:
        raise ValueError("manifest endpoint does not match L4-008 Treasury endpoint")
    raw_paths = manifest.get("raw_paths")
    hashes = manifest.get("page_sha256")
    if not isinstance(raw_paths, list) or not raw_paths or not isinstance(hashes, list):
        raise ValueError("manifest raw-page provenance is incomplete")
    if len(raw_paths) != len(hashes):
        raise ValueError("manifest raw paths and hashes differ in length")
    return manifest


def _raw_pages(manifest: dict[str, Any], manifest_path: Path) -> tuple[list[dict[str, Any]], list[Path]]:
    payloads, paths, contents = [], [], []
    for raw_text, expected_hash in zip(manifest["raw_paths"], manifest["page_sha256"]):
        raw_path = Path(raw_text)
        if not raw_path.is_absolute():
            raw_path = (manifest_path.parent / raw_path).resolve()
        content = raw_path.read_bytes()
        if hashlib.sha256(content).hexdigest() != expected_hash:
            raise ValueError("raw page SHA-256 does not match manifest")
        payload = json.loads(content)
        if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
            raise ValueError("raw Treasury page does not contain a data list")
        payloads.append(payload)
        paths.append(raw_path)
        contents.append(content)
    aggregate = hashlib.sha256(b"".join(contents)).hexdigest()
    if aggregate != manifest.get("source_sha256"):
        raise ValueError("aggregate raw SHA-256 does not match manifest")
    return payloads, paths


def _amount(value: Any, field: str) -> Decimal:
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"invalid {field}: {value}") from exc
    if not amount.is_finite():
        raise ValueError(f"invalid {field}: {value}")
    return amount


def parse_manifest(manifest_path: Path, *, stale_after_days: int = 450) -> list[dict[str, Any]]:
    manifest = _load_manifest(manifest_path)
    payloads, raw_paths = _raw_pages(manifest, manifest_path)
    pairs: dict[tuple[str, int], dict[str, Decimal]] = {}
    for payload in payloads:
        for item in payload["data"]:
            if not isinstance(item, dict):
                raise ValueError("Treasury data row must be an object")
            try:
                observation_date = date.fromisoformat(str(item.get("record_date", "")))
                fiscal_year = int(item.get("record_fiscal_year"))
            except (TypeError, ValueError) as exc:
                raise ValueError(f"invalid Treasury date or fiscal year: {item}") from exc
            if fiscal_year < 1900 or fiscal_year > observation_date.year + 1:
                raise ValueError(f"invalid Treasury fiscal year: {fiscal_year}")
            line_code = str(item.get("line_code_nbr", ""))
            if line_code not in REQUIRED:
                raise ValueError(f"unexpected Treasury line code: {line_code}")
            if item.get("classification_desc") != REQUIRED[line_code]:
                raise ValueError(f"classification mismatch for line {line_code}")
            amount = _amount(item.get("current_fytd_rcpt_outly_amt"), "FYTD amount")
            if observation_date.month != 9:
                continue
            if fiscal_year != observation_date.year:
                raise ValueError("September record fiscal year must equal calendar year")
            key = (observation_date.isoformat(), fiscal_year)
            values = pairs.setdefault(key, {})
            if line_code in values and values[line_code] != amount:
                raise ValueError(f"conflicting duplicate for {key}, line {line_code}")
            values[line_code] = amount
    if not pairs:
        raise ValueError("no September fiscal-year-end observations found")
    for key, values in pairs.items():
        if set(values) != set(REQUIRED):
            raise ValueError(f"missing paired Treasury row for {key}")
    latest_date = max(date.fromisoformat(key[0]) for key in pairs)
    availability = "STALE" if (datetime.now(timezone.utc).date() - latest_date).days > stale_after_days else "AVAILABLE"
    query_text = json.dumps(manifest.get("query", {}), sort_keys=True, separators=(",", ":"))
    raw_text = ";".join(str(path) for path in raw_paths)
    rows = []
    for (date_text, fiscal_year), values in sorted(pairs.items()):
        receipts = values["130"]
        interest = values["360"]
        if receipts <= 0:
            raise ValueError(f"receipts must be positive for fiscal year {fiscal_year}")
        if interest < 0:
            raise ValueError(f"gross interest must not be negative for fiscal year {fiscal_year}")
        ratio = interest / receipts * Decimal("100")
        ratio_float = float(ratio)
        if not math.isfinite(ratio_float):
            raise ValueError(f"invalid ratio for fiscal year {fiscal_year}")
        validation = "PASS" if Decimal("0") <= ratio <= Decimal("50") else "FLAG"
        rows.append({
            "variable_id": VARIABLE_ID,
            "observation_date": date_text,
            "fiscal_year": fiscal_year,
            "gross_interest_expense_usd": float(interest),
            "total_receipts_usd": float(receipts),
            "interest_expense_to_revenue_pct": ratio_float,
            "unit": "percent_of_federal_receipts",
            "accounting_convention": "Gross interest on Treasury debt securities / total federal receipts, fiscal-year-to-date at September month-end",
            "source_name": "U.S. Treasury Fiscal Data — Monthly Treasury Statement Table 3",
            "endpoint": ENDPOINT,
            "query": query_text,
            "raw_file_paths": raw_text,
            "manifest_path": str(manifest_path),
            "source_sha256": manifest["source_sha256"],
            "retrieved_at": manifest["retrieved_at"],
            "validation_status": validation,
            "availability_status": availability,
            "parser_version": PARSER_VERSION,
        })
    return rows


def carry_forward(prior_path: Path, *, retrieved_at: str | None = None) -> list[dict[str, Any]]:
    if not prior_path.exists():
        raise FileNotFoundError("no prior valid L4-008 output exists")
    with prior_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    valid = [row for row in rows if row.get("validation_status") in {"PASS", "FLAG"}]
    if not valid:
        raise ValueError("prior L4-008 output contains no valid observation")
    latest = max(valid, key=lambda row: row["observation_date"]).copy()
    latest["availability_status"] = "STALE"
    latest["retrieved_at"] = retrieved_at or datetime.now(timezone.utc).isoformat()
    latest["parser_version"] = PARSER_VERSION
    return [latest]


def write_csv(rows: list[dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    blocked = output_path.with_suffix(".status.json")
    if blocked.exists():
        blocked.unlink()
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_blocked(output_path: Path, reason: str) -> Path:
    path = output_path.with_suffix(".status.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "variable_id": VARIABLE_ID, "status": "BLOCKED", "availability_status": "BLOCKED",
        "validation_status": "FAIL", "reason": reason,
        "checked_at": datetime.now(timezone.utc).isoformat(), "parser_version": PARSER_VERSION,
    }, indent=2) + "\n", encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    cli = argparse.ArgumentParser(description="Parse Treasury MTS Table 3 for L4-008")
    cli.add_argument("--manifest", type=Path)
    cli.add_argument("--prior", type=Path)
    cli.add_argument("--output", type=Path, default=Path("data/processed/L4_008_observations.csv"))
    cli.add_argument("--stale-after-days", type=int, default=450)
    args = cli.parse_args(argv)
    try:
        if not args.manifest:
            raise ValueError("--manifest is required for normal collection")
        rows = parse_manifest(args.manifest, stale_after_days=args.stale_after_days)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        try:
            if not args.prior:
                raise FileNotFoundError("no prior valid L4-008 output exists")
            rows = carry_forward(args.prior)
        except (OSError, ValueError) as fallback_exc:
            path = write_blocked(args.output, str(fallback_exc))
            print(json.dumps({"status": "BLOCKED", "status_path": str(path)}))
            return 0
    write_csv(rows, args.output)
    print(f"Wrote {len(rows)} observations to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
