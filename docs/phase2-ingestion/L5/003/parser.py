"""Parse IMF COFER world USD reserve-share observations for L5-003."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from datetime import date, datetime, timezone
from pathlib import Path

VARIABLE_ID = "L5-003"
DATASET_ID = "IMF.STA:COFER"
SERIES_ID = "G001.AFXRA.CI_USD.SHRO_PT.Q"
PARSER_VERSION = "0.1.0"
STALE_DAYS = 200
FIELDS = ["variable_id", "observation_date", "usd_reserve_share_pct", "usd_share_change_qoq_pp", "unit", "source_name", "source_dataset_id", "source_series_id", "raw_path", "raw_sha256", "manifest_path", "manifest_sha256", "retrieved_at", "validation_status", "availability_status", "fallback_checked_at", "parser_version"]
MANIFEST_FIELDS = {"dataset_id", "source_url", "retrieved_at", "raw_path", "size_bytes", "sha256", "http_status", "collector_version"}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_timestamp(value: object, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a non-empty ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} must be a valid ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include a timezone")
    return value


def load_manifest(manifest_path: Path, raw_path: Path) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("manifest must be a JSON object")
    missing = sorted(MANIFEST_FIELDS - manifest.keys())
    if missing:
        raise ValueError(f"manifest missing required fields: {', '.join(missing)}")
    if manifest["dataset_id"] != DATASET_ID:
        raise ValueError(f"manifest dataset_id must be {DATASET_ID}")
    parse_timestamp(manifest["retrieved_at"], "manifest retrieved_at")
    if not all(isinstance(manifest[field], str) and manifest[field] for field in ("source_url", "raw_path", "collector_version")):
        raise ValueError("manifest source_url, raw_path, and collector_version must be non-empty strings")
    if Path(manifest["raw_path"]).resolve() != raw_path.resolve():
        raise ValueError("manifest raw_path does not identify the supplied raw file")
    if not isinstance(manifest["size_bytes"], int) or manifest["size_bytes"] != raw_path.stat().st_size:
        raise ValueError("manifest size_bytes does not match the raw file")
    if manifest["http_status"] != 200:
        raise ValueError("manifest http_status must be 200")
    if not isinstance(manifest["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", manifest["sha256"]):
        raise ValueError("manifest sha256 must be a lowercase SHA-256 digest")
    return manifest


def quarter_end(period: str) -> date:
    match = re.fullmatch(r"(\d{4})-Q([1-4])", period)
    if not match:
        raise ValueError(f"invalid quarterly period: {period}")
    year, quarter = map(int, match.groups())
    return date(year, quarter * 3, (31, 30, 30, 31)[quarter - 1])


def prior_quarter(period: str) -> str:
    year, quarter = int(period[:4]), int(period[-1])
    return f"{year - 1}-Q4" if quarter == 1 else f"{year}-Q{quarter - 1}"


def parse(raw_path: Path, manifest_path: Path, *, as_of: str | None = None, stale_days: int = STALE_DAYS) -> list[dict]:
    manifest = load_manifest(manifest_path, raw_path)
    raw_hash = sha256_file(raw_path)
    if manifest.get("sha256") != raw_hash:
        raise ValueError("raw SHA-256 does not match manifest")
    values: dict[str, float] = {}
    with raw_path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            if not all(row.get(key) == value for key, value in {
                "COUNTRY": "G001", "INDICATOR": "AFXRA", "FXR_CURRENCY": "CI_USD",
                "TYPE_OF_TRANSFORMATION": "SHRO_PT", "FREQUENCY": "Q",
            }.items()):
                continue
            if not str(row.get("STRUCTURE_ID", "")).startswith(DATASET_ID):
                raise ValueError("unexpected IMF COFER structure identifier")
            period, raw_value = row.get("TIME_PERIOD", ""), row.get("OBS_VALUE", "")
            if raw_value in (None, "", "."):
                continue
            quarter_end(period)
            try:
                value = float(raw_value)
            except ValueError as exc:
                raise ValueError(f"invalid COFER value for {period}") from exc
            if not math.isfinite(value) or not 0 <= value <= 100:
                raise ValueError(f"COFER USD share out of bounds for {period}")
            if period in values and values[period] != value:
                raise ValueError(f"conflicting duplicate COFER period: {period}")
            values[period] = value
    if not values:
        raise ValueError("no world quarterly USD-share COFER observations found")
    today = date.fromisoformat(as_of) if as_of else datetime.now(timezone.utc).date()
    rows = []
    manifest_hash = sha256_file(manifest_path)
    for period in sorted(values):
        observation_date = quarter_end(period)
        value = values[period]
        previous = values.get(prior_quarter(period))
        change = None if previous is None else value - previous
        validation = "FLAG" if change is not None and abs(change) > 5 else "PASS"
        rows.append({
            "variable_id": VARIABLE_ID, "observation_date": observation_date.isoformat(),
            "usd_reserve_share_pct": value, "usd_share_change_qoq_pp": change,
            "unit": "percent_and_percentage_points", "source_name": "IMF COFER",
            "source_dataset_id": DATASET_ID, "source_series_id": SERIES_ID,
            "raw_path": str(raw_path), "raw_sha256": raw_hash,
            "manifest_path": str(manifest_path), "manifest_sha256": manifest_hash,
            "retrieved_at": manifest["retrieved_at"], "validation_status": validation,
            "availability_status": "STALE" if (today - observation_date).days > stale_days else "AVAILABLE",
            "fallback_checked_at": None, "parser_version": PARSER_VERSION,
        })
    return rows


def carry_forward(prior_path: Path, *, checked_at: str | None = None) -> list[dict]:
    if not prior_path.exists():
        raise FileNotFoundError("no prior L5-003 output exists")
    with prior_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not set(FIELDS).issubset(reader.fieldnames):
            raise ValueError("prior L5-003 output is missing required columns")
        valid = []
        for row in reader:
            validate_prior_row(row)
            if row["validation_status"] in {"PASS", "FLAG"}:
                valid.append(row)
    if not valid:
        raise ValueError("prior L5-003 output contains no valid observation")
    row = max(valid, key=lambda item: item["observation_date"])
    row["usd_reserve_share_pct"] = float(row["usd_reserve_share_pct"])
    row["usd_share_change_qoq_pp"] = float(row["usd_share_change_qoq_pp"]) if row["usd_share_change_qoq_pp"] else None
    row["availability_status"] = "STALE"
    row["fallback_checked_at"] = checked_at or datetime.now(timezone.utc).isoformat()
    row["parser_version"] = PARSER_VERSION
    return [row]


def validate_prior_row(row: dict) -> None:
    expected = {
        "variable_id": VARIABLE_ID, "unit": "percent_and_percentage_points",
        "source_name": "IMF COFER", "source_dataset_id": DATASET_ID,
        "source_series_id": SERIES_ID,
    }
    if any(row.get(field) != value for field, value in expected.items()):
        raise ValueError("prior row identity does not match L5-003")
    try:
        observation = date.fromisoformat(row.get("observation_date", ""))
        value = float(row.get("usd_reserve_share_pct", ""))
        change = None if row.get("usd_share_change_qoq_pp", "") == "" else float(row["usd_share_change_qoq_pp"])
    except (TypeError, ValueError) as exc:
        raise ValueError("prior L5-003 row has malformed date or numeric values") from exc
    if observation != quarter_end(f"{observation.year}-Q{(observation.month - 1) // 3 + 1}"):
        raise ValueError("prior L5-003 observation_date must be a quarter end")
    if not math.isfinite(value) or not 0 <= value <= 100 or (change is not None and not math.isfinite(change)):
        raise ValueError("prior L5-003 row has invalid numeric values")
    if row.get("validation_status") not in {"PASS", "FLAG"} or row.get("availability_status") not in {"AVAILABLE", "STALE"}:
        raise ValueError("prior L5-003 row has invalid status")
    for field in ("raw_sha256", "manifest_sha256"):
        if not re.fullmatch(r"[0-9a-f]{64}", row.get(field, "")):
            raise ValueError(f"prior L5-003 row has invalid {field}")
    if not all(row.get(field) for field in ("raw_path", "manifest_path", "parser_version")):
        raise ValueError("prior L5-003 row is missing provenance")
    parse_timestamp(row.get("retrieved_at"), "prior retrieved_at")
    if row.get("fallback_checked_at"):
        parse_timestamp(row["fallback_checked_at"], "prior fallback_checked_at")


def write_csv(rows: list[dict], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.with_suffix(".status.json").unlink(missing_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(rows)


def write_blocked(output: Path, reason: str) -> Path:
    path = output.with_suffix(".status.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"variable_id": VARIABLE_ID, "status": "BLOCKED", "availability_status": "BLOCKED", "reason": reason, "checked_at": datetime.now(timezone.utc).isoformat(), "parser_version": PARSER_VERSION}, indent=2) + "\n", encoding="utf-8")
    return path


def main() -> int:
    root = Path(__file__).resolve().parent
    cli = argparse.ArgumentParser(description="Parse IMF COFER USD reserve share")
    cli.add_argument("--raw", type=Path); cli.add_argument("--manifest", type=Path)
    cli.add_argument("--prior", type=Path); cli.add_argument("--as-of")
    cli.add_argument("--output", type=Path, default=root / "data/processed/L5_003_observations.csv")
    args = cli.parse_args()
    try:
        if not args.raw or not args.manifest:
            raise FileNotFoundError("raw COFER file and manifest are required")
        rows = parse(args.raw, args.manifest, as_of=args.as_of)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        try:
            rows = carry_forward(args.prior, checked_at=datetime.now(timezone.utc).isoformat()) if args.prior else carry_forward(Path("__missing__"))
        except (OSError, ValueError) as fallback_exc:
            path = write_blocked(args.output, f"{exc}; {fallback_exc}")
            print(json.dumps({"status": "BLOCKED", "status_path": str(path)})); return 0
    write_csv(rows, args.output)
    print(f"Wrote {len(rows)} observations to {args.output}"); return 0


if __name__ == "__main__":
    raise SystemExit(main())
