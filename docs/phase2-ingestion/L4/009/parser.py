"""Calculate L4-009 Treasury refinancing concentration from preserved MSPD pages."""
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

VARIABLE_ID = "L4-009"
PARSER_VERSION = "0.1.0"
ENDPOINT = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/debt/mspd/mspd_table_3_market"
REQUIRED_FIELDS = {
    "record_date", "security_type_desc", "security_class1_desc",
    "maturity_date", "outstanding_amt", "src_line_nbr",
}
OUTPUT_FIELDS = [
    "variable_id", "observation_date", "maturing_within_1y_mil_usd",
    "total_marketable_outstanding_mil_usd", "dated_detail_outstanding_mil_usd",
    "classification_coverage_pct", "marketable_debt_maturing_within_1y_pct",
    "unit", "measure_definition", "source_name", "endpoint", "query",
    "raw_file_paths", "manifest_path", "page_count", "source_sha256", "retrieved_at",
    "validation_status", "availability_status", "parser_version",
]
MISSING = {None, "", "null", "*"}


def _normalized(value: Any) -> Any:
    return value.strip() if isinstance(value, str) else value


def _load_manifest(path: Path) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("endpoint") != ENDPOINT:
        raise ValueError("manifest endpoint does not match L4-009 Treasury endpoint")
    query = manifest.get("query")
    if not isinstance(query, dict) or set(str(query.get("fields", "")).split(",")) != REQUIRED_FIELDS:
        raise ValueError("manifest must request exactly the L4-009 fields")
    paths, hashes = manifest.get("raw_paths"), manifest.get("page_sha256")
    if not isinstance(paths, list) or not paths or not isinstance(hashes, list) or len(paths) != len(hashes):
        raise ValueError("manifest raw-page provenance is incomplete")
    if manifest.get("page_count") != len(paths):
        raise ValueError("manifest page count does not match raw paths")
    return manifest


def _raw_rows(manifest: dict[str, Any], manifest_path: Path) -> tuple[list[dict[str, Any]], list[Path]]:
    rows: list[dict[str, Any]] = []
    paths, contents = [], []
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
        rows.extend(payload["data"])
        paths.append(raw_path)
        contents.append(content)
    if hashlib.sha256(b"".join(contents)).hexdigest() != manifest.get("source_sha256"):
        raise ValueError("aggregate raw SHA-256 does not match manifest")
    return rows, paths


def _optional_date(value: Any, field: str) -> date | None:
    value = _normalized(value)
    if value in MISSING:
        return None
    try:
        return date.fromisoformat(str(value))
    except ValueError as exc:
        raise ValueError(f"invalid {field}: {value}") from exc


def _amount(value: Any) -> Decimal | None:
    value = _normalized(value)
    if value in MISSING:
        return None
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"invalid outstanding amount: {value}") from exc
    if not amount.is_finite() or amount < 0:
        raise ValueError(f"invalid outstanding amount: {value}")
    return amount


def _calendar_year_after(value: date) -> date:
    try:
        return value.replace(year=value.year + 1)
    except ValueError:
        return value.replace(year=value.year + 1, day=28)


def parse_manifest(manifest_path: Path, *, stale_after_days: int = 62) -> list[dict[str, Any]]:
    manifest = _load_manifest(manifest_path)
    source_rows, raw_paths = _raw_rows(manifest, manifest_path)
    grouped: dict[date, list[dict[str, Any]]] = {}
    seen: dict[tuple[date, int], tuple[str, ...]] = {}
    for item in source_rows:
        if not isinstance(item, dict) or set(item) != REQUIRED_FIELDS:
            raise ValueError("Treasury row fields do not match L4-009 request")
        observation_date = _optional_date(item["record_date"], "record_date")
        if observation_date is None:
            raise ValueError("record_date is required")
        try:
            line = int(item["src_line_nbr"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"invalid source line number: {item['src_line_nbr']}") from exc
        signature = tuple(str(item[field]) for field in sorted(REQUIRED_FIELDS))
        key = (observation_date, line)
        if key in seen:
            if seen[key] != signature:
                raise ValueError(f"conflicting duplicate source line: {observation_date}, {line}")
            continue
        seen[key] = signature
        grouped.setdefault(observation_date, []).append(item)
    if not grouped:
        raise ValueError("no Treasury maturity rows found")

    latest_date = max(grouped)
    availability = "STALE" if (datetime.now(timezone.utc).date() - latest_date).days > stale_after_days else "AVAILABLE"
    query_text = json.dumps(manifest["query"], sort_keys=True, separators=(",", ":"))
    raw_text = ";".join(str(path) for path in raw_paths)
    output = []
    for observation_date, items in sorted(grouped.items()):
        summaries: list[Decimal] = []
        dated_total = Decimal("0")
        within_year = Decimal("0")
        cutoff = _calendar_year_after(observation_date)
        for item in items:
            if _normalized(item["security_type_desc"]) != "Marketable":
                raise ValueError("unexpected non-marketable Treasury row")
            maturity = _optional_date(item["maturity_date"], "maturity_date")
            amount = _amount(item["outstanding_amt"])
            is_summary = _normalized(item["security_class1_desc"]) == "Total Marketable"
            if is_summary:
                if maturity is not None or amount is None:
                    raise ValueError("Total Marketable summary is malformed")
                summaries.append(amount)
                continue
            if maturity is None or amount is None or amount == 0:
                continue
            dated_total += amount
            if observation_date < maturity <= cutoff:
                within_year += amount
        if len(summaries) != 1:
            raise ValueError(f"expected one Total Marketable summary for {observation_date}")
        denominator = summaries[0]
        if denominator <= 0:
            raise ValueError(f"Total Marketable must be positive for {observation_date}")
        if within_year > denominator:
            raise ValueError(f"one-year maturity amount exceeds Total Marketable for {observation_date}")
        coverage = dated_total / denominator * Decimal("100")
        ratio = within_year / denominator * Decimal("100")
        coverage_float, ratio_float = float(coverage), float(ratio)
        if not math.isfinite(coverage_float) or not math.isfinite(ratio_float):
            raise ValueError(f"non-finite L4-009 result for {observation_date}")
        validation = "PASS" if coverage >= Decimal("95") and Decimal("5") <= ratio <= Decimal("80") else "FLAG"
        output.append({
            "variable_id": VARIABLE_ID,
            "observation_date": observation_date.isoformat(),
            "maturing_within_1y_mil_usd": float(within_year),
            "total_marketable_outstanding_mil_usd": float(denominator),
            "dated_detail_outstanding_mil_usd": float(dated_total),
            "classification_coverage_pct": coverage_float,
            "marketable_debt_maturing_within_1y_pct": ratio_float,
            "unit": "percent_of_marketable_treasury_debt",
            "measure_definition": "Positive dated marketable debt maturing after record date and within one calendar year / Total Marketable outstanding * 100",
            "source_name": "U.S. Treasury Fiscal Data — Monthly Statement of the Public Debt Table 3",
            "endpoint": ENDPOINT,
            "query": query_text,
            "raw_file_paths": raw_text,
            "manifest_path": str(manifest_path),
            "page_count": len(raw_paths),
            "source_sha256": manifest["source_sha256"],
            "retrieved_at": manifest["retrieved_at"],
            "validation_status": validation,
            "availability_status": availability,
            "parser_version": PARSER_VERSION,
        })
    return output


def carry_forward(prior_path: Path, *, retrieved_at: str | None = None) -> list[dict[str, Any]]:
    if not prior_path.exists():
        raise FileNotFoundError("no prior valid L4-009 output exists")
    with prior_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    valid = [row for row in rows if row.get("validation_status") in {"PASS", "FLAG"}]
    if not valid:
        raise ValueError("prior L4-009 output contains no valid observation")
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
    cli = argparse.ArgumentParser(description="Parse Treasury MSPD Table 3 for L4-009")
    cli.add_argument("--manifest", type=Path)
    cli.add_argument("--prior", type=Path)
    cli.add_argument("--output", type=Path, default=Path("data/processed/L4_009_observations.csv"))
    cli.add_argument("--stale-after-days", type=int, default=62)
    args = cli.parse_args(argv)
    try:
        if not args.manifest:
            raise ValueError("--manifest is required for normal collection")
        rows = parse_manifest(args.manifest, stale_after_days=args.stale_after_days)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        try:
            if not args.prior:
                raise FileNotFoundError("no prior valid L4-009 output exists")
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
