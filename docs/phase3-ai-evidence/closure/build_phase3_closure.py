"""Build and validate the single-record Phase 3 handoff for all admitted variables."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
from datetime import UTC, date, datetime, timedelta
import calendar
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PHASE3 = ROOT / "docs" / "phase3-ai-evidence"
OUT = PHASE3 / "closure"
FIELDS = (
    "variable_id",
    "observation_timestamp",
    "value",
    "unit_or_scale",
    "availability_status",
    "source_reference",
    "quality_flag",
)
STATUSES = {"AVAILABLE", "STALE", "BLOCKED", "FLAG"}
QUALITY_FLAGS = {"OK", "STALE_MAX_AGE_EXCEEDED", "COLLECTOR_LAG", "LOW_COVERAGE", "NO_OVERLAPPING_OBSERVATION_DATE"}

# Verification from the already-preserved 2026-08-30 source snapshots.  False
# means the source itself had no newer observation; true means the source had a
# newer observation that was not present in the canonical handoff.
SOURCE_VERIFICATION = {
    "L1-003": ("2026-08-30T10:18:02Z", "2026-08-21T00:00:00Z", False),
    "L1-005": ("2026-08-30T10:09:17Z", "2026-08-21T00:00:00Z", False),
    "L2-001": ("2026-08-30T10:20:39Z", "2026-08-27T00:00:00Z", False),
    "L2-002": ("2026-08-30T10:09:20Z", "2026-08-21T00:00:00Z", False),
    "L2-003": ("2026-08-30T10:09:22Z", "2026-08-21T00:00:00Z", False),
}

# Cadence and publication-lag policy is source-specific.  The values below are
# taken from the variable package documentation/configuration; variables whose
# release timing cannot be represented safely are explicitly marked for review.
CADENCE = {
    "L0-001": ("annual", 180, "year_end", False),
    "L0-002": ("monthly", 20, "as_of", True),
    "L0-003": ("monthly", 4, "month_end", False),
    "L0-005": ("quarterly", 38, "quarter_end", False),
    "L0-006": ("quarterly", 38, "quarter_end", False),
    "L0-009": ("daily", 1, "business_day", False),
    "L1-001": ("daily", 1, "business_day", False),
    "L1-002": ("daily", 1, "business_day", False),
    "L1-003": ("weekly", 0, "friday", False),
    "L1-005": ("daily", 1, "business_day", False),
    "L1-006": ("daily", 0, "business_day", False),
    "L1-007": ("daily", 1, "business_day", False),
    "L2-001": ("daily", 1, "business_day", False),
    "L2-002": ("daily", 1, "business_day", False),
    "L2-003": ("daily", 1, "business_day", False),
    "L3-001": ("daily", 0, "business_day", False),
    "L3-002": ("daily", 0, "business_day", False),
    "L3-003": ("daily", 0, "business_day", False),
    "L3-004": ("irregular", 0, "event", True),
    "L3-005": ("irregular", 0, "event", True),
    "L3-006": ("irregular", 0, "event", True),
    "L4-001": ("monthly", 15, "month_start", False),
    "L4-002": ("monthly", 15, "month_start", False),
    "L4-003": ("daily", 1, "business_day", False),
    "L4-004": ("daily", 1, "business_day", False),
    "L4-006": ("annual", 550, "year_start", False),
    "L4-007": ("quarterly", 190, "quarter_start", False),
    "L4-008": ("annual", 450, "fiscal_year_end", False),
    "L4-009": ("monthly", 31, "month_end", False),
    "L5-001": ("monthly", 60, "month_start", False),
    "L5-002": ("irregular", 0, "as_published", True),
    "L5-003": ("quarterly", 200, "quarter_end", False),
    "L5-006": ("monthly", 60, "month_start", False),
    "L6-001": ("daily", 1, "business_day", True),
    "L6-002": ("irregular", 0, "event", True),
    "L7-001": ("weekly", 1, "wednesday", False),
    "L7-003": ("quarterly", 270, "quarter_end", False),
    "L7-004": ("daily", 1, "business_day", False),
    "L7-005": ("daily", 1, "business_day", False),
    "L8-001": ("monthly", 4, "month_end", False),
    "L9-001": ("weekly", 0, "date", True),
    "L9-004": ("quarterly", 38, "quarter_end", False),
    "L10-001": ("weekly", 3, "tuesday", False),
    "L10-002": ("daily", 1, "business_day", False),
}

TOLERANCE_DAYS = {"daily": 1, "weekly": 3, "monthly": 3, "quarterly": 7, "annual": 14, "irregular": 0}


# These are the approved publication/freshness windows documented during Phase 2/3.
# They deliberately describe source cadence, not a fabricated replacement value.
MAX_AGE_DAYS = {
    "L0-001": 366, "L0-002": 45, "L0-003": 45, "L0-005": 120,
    "L0-006": 120, "L0-009": 7, "L1-001": 7, "L1-002": 7,
    "L1-003": 7, "L1-005": 7, "L1-006": 3, "L1-007": 7,
    "L2-001": 7, "L2-002": 7, "L2-003": 7, "L3-001": 5,
    "L3-002": 5, "L3-003": 5, "L3-004": 5, "L3-005": 120,
    "L3-006": 60, "L4-001": 45, "L4-002": 45, "L4-003": 7,
    "L4-004": 7, "L4-006": 120, "L4-007": 120, "L4-008": 120,
    "L4-009": 120, "L5-001": 120, "L5-002": 120, "L5-003": 120,
    "L5-006": 120, "L6-001": 7, "L6-002": 7, "L7-001": 14,
    "L7-003": 120, "L7-004": 7, "L7-005": 7, "L8-001": 45,
    "L9-001": 14, "L9-004": 120, "L10-001": 10, "L10-002": 7,
}


def utc(timestamp: str) -> datetime:
    duplicate_midnight = re.fullmatch(r"(\d{4}-\d{2}-\d{2}) 00:00:00T00:00:00Z", timestamp)
    if duplicate_midnight:
        timestamp = duplicate_midnight.group(1)
    normalized = timestamp.replace("Z", "+00:00")
    try:
        value = datetime.fromisoformat(normalized)
    except ValueError:
        for pattern in ("%m/%d/%Y %H:%M:%S", "%b %Y"):
            try:
                value = datetime.strptime(timestamp, pattern)
                break
            except ValueError:
                continue
        else:
            raise ValueError(f"unsupported timestamp: {timestamp}")
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def iso(date_or_timestamp: str) -> str:
    return utc(date_or_timestamp).isoformat().replace("+00:00", "Z")


def expected_latest_observation(variable_id: str, today: date) -> date | None:
    """Return the latest period that should have been released by today."""
    frequency, lag_days, convention, needs_review = CADENCE[variable_id]
    if needs_review or frequency == "irregular":
        return None
    release_cutoff = today - timedelta(days=lag_days)
    if frequency == "daily":
        candidate = release_cutoff
        while candidate.weekday() >= 5:
            candidate -= timedelta(days=1)
        return candidate
    if frequency == "weekly":
        weekdays = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4}
        target = weekdays.get(convention, 4)
        candidate = release_cutoff - timedelta(days=(release_cutoff.weekday() - target) % 7)
        return candidate
    if frequency == "monthly":
        year, month = release_cutoff.year, release_cutoff.month
        while True:
            last_day = date(year, month, calendar.monthrange(year, month)[1])
            if last_day <= release_cutoff:
                return last_day if convention == "month_end" else date(year, month, 1)
            month -= 1
            if month == 0:
                year, month = year - 1, 12
    if frequency == "quarterly":
        year = release_cutoff.year
        quarter = (release_cutoff.month - 1) // 3 + 1
        while True:
            end_month = quarter * 3
            quarter_end = date(year, end_month, calendar.monthrange(year, end_month)[1])
            if quarter_end <= release_cutoff:
                return quarter_end if convention == "quarter_end" else date(year, end_month - 2, 1)
            quarter -= 1
            if quarter == 0:
                year, quarter = year - 1, 4
    if frequency == "annual":
        year = release_cutoff.year
        while True:
            period_end = date(year, 9, 30) if convention == "fiscal_year_end" else date(year, 12, 31)
            if period_end <= release_cutoff:
                return period_end if convention in {"year_end", "fiscal_year_end"} else date(year, 1, 1)
            year -= 1
    raise ValueError(f"unsupported release frequency for {variable_id}: {frequency}")


def repo_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def ids_from_tracker() -> list[str]:
    text = (PHASE3 / "PHASE3-TRACKER.md").read_text(encoding="utf-8")
    return re.findall(r"^\| (L\d+-\d{3}) \|", text, flags=re.MULTILINE)


def normalized_source(output: Path, source: str | None = None) -> str:
    parts = [f"transform={repo_path(output)}"]
    if source:
        source = source.replace("/mnt/d/Projects/GoldRush/", "")
        parts.append(f"source={source}")
    return "::".join(parts)


def generic_record(variable_id: str) -> tuple[dict, Path]:
    layer, number = variable_id.split("-")
    data_dir = PHASE3 / layer / number / "data"
    candidates = sorted(data_dir.glob("*handoff.json"))
    if not candidates:
        raise FileNotFoundError(variable_id)
    path = candidates[0]
    rows = json.loads(path.read_text(encoding="utf-8"))
    if variable_id == "L3-004":
        earliest = min(row["meeting_date"] for row in rows)
        rows = [row for row in rows if row["meeting_date"] == earliest and row["unit_or_scale"] == "expected_target_change_bps"]
    rows = [row for row in rows if row["variable_id"] == variable_id]
    valid_rows = []
    for row in rows:
        try:
            utc(row["observation_timestamp"])
        except ValueError:
            continue
        valid_rows.append(row)
    if not valid_rows:
        raise ValueError(f"{variable_id} has no valid output timestamp")
    return max(valid_rows, key=lambda row: utc(row["observation_timestamp"])), path


def csv_last(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"no rows: {path}")
    return rows[-1]


def special_record(variable_id: str) -> tuple[dict, Path]:
    phase2 = ROOT / "docs" / "phase2-ingestion"
    if variable_id == "L0-009":
        path = PHASE3 / "L0/009/data/l0_009_phase3_handoff.json"
        rows = json.loads(path.read_text(encoding="utf-8"))
        if not rows:
            raise ValueError("L0-009 aligned handoff is empty")
        row = max(rows, key=lambda item: utc(item["observation_timestamp"]))
        if row["availability_status"] != "AVAILABLE" or row["quality_flag"] not in {"OK", "PASS"}:
            raise ValueError("L0-009 aligned handoff is not available")
        source = "CME:docs/phase2-ingestion/data/cme/manifests/section62-20260830T102041Z.json;FRED:docs/phase2-ingestion/L0/009/data/raw/sofr3m-refresh-20260830.manifest.json;aligned-v2"
        return {"variable_id": variable_id, "observation_timestamp": row["observation_timestamp"], "value": float(row["value"]),
                "unit_or_scale": "percent_per_annum", "availability_status": "AVAILABLE",
                "source_reference": normalized_source(path, source), "quality_flag": "OK"}, path
    if variable_id == "L0-002":
        path = phase2 / "L0/002/processed/L0_002_observations.csv"
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        row = max(rows, key=lambda item: item["source_publication_date"])
        source_manifest = phase2 / "data/wgc/manifests/official_holdings-20260830T100640Z.json"
        return {"variable_id": variable_id, "observation_timestamp": iso(row["source_publication_date"]), "value": float(row["holdings_tonnes"]), "unit_or_scale": row["unit"], "availability_status": row["availability_status"], "source_reference": normalized_source(path, source_manifest.as_posix()), "quality_flag": row["validation_status"]}, path
    if variable_id == "L0-006":
        path = phase2 / "L0/006/processed/L0_006_observations.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        rows = payload["observations"]
        row = max(rows, key=lambda item: item["observation_date"])
        source_manifest = payload.get("ingestion_metadata", {}).get("source_manifest")
        return {"variable_id": variable_id, "observation_timestamp": iso(row["observation_date"]), "value": float(row["value"]), "unit_or_scale": "metric_tonnes", "availability_status": payload["availability_status"], "source_reference": normalized_source(path, source_manifest), "quality_flag": "PASS"}, path
    if variable_id in {"L1-006", "L10-002"}:
        suffix = "L1/006/data/processed/L1_006_observations.csv" if variable_id == "L1-006" else "L10/002/data/processed/L10_002_observations-refresh-20260830.csv"
        path = phase2 / suffix
        row = csv_last(path)
        value = row["value"] if variable_id == "L1-006" else row["open_interest_contracts"]
        source = (phase2 / "data/cme/manifests/section10-20260830T102041Z.json").as_posix() if variable_id == "L1-006" else row.get("source_manifest")
        return {"variable_id": variable_id, "observation_timestamp": iso(row["observation_date"]), "value": float(value), "unit_or_scale": row["unit"], "availability_status": row["availability_status"], "source_reference": normalized_source(path, source), "quality_flag": row["validation_status"]}, path
    if variable_id == "L3-006":
        path = PHASE3 / "L3/006/data/results/live-l3-006-refresh-20260830.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        return {"variable_id": variable_id, "observation_timestamp": iso(payload["completed_at"]), "value": float(payload["final_score"]), "unit_or_scale": "hawkishness_score_0_to_100", "availability_status": "FLAG", "source_reference": normalized_source(path), "quality_flag": "LOW_COVERAGE"}, path
    if variable_id == "L6-002":
        path = PHASE3 / "L6/002/refresh-20260830/silent-monitor-20260830T100610Z.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload["candidate_count"] != 0:
            raise ValueError("L6-002 closure source is not the zero-event run")
        return {"variable_id": variable_id, "observation_timestamp": iso(payload["run_at"]), "value": 0.0, "unit_or_scale": "sovereign_asset_freeze_score_0_to_100", "availability_status": "AVAILABLE", "source_reference": normalized_source(path, payload["source_manifest"]), "quality_flag": "OK"}, path
    raise KeyError(variable_id)


def record_for(variable_id: str) -> tuple[dict, Path]:
    special_ids = {"L0-002", "L0-006", "L0-009", "L1-006", "L3-006", "L6-002", "L10-002"}
    if variable_id in special_ids:
        record, output = special_record(variable_id)
    else:
        row, output = generic_record(variable_id)
        record = {field: row[field] for field in FIELDS}
        record["source_reference"] = normalized_source(output, row.get("source_reference"))
    record["quality_flag"] = "OK" if record["quality_flag"] == "PASS" else record["quality_flag"]
    if record["availability_status"] == "BLOCKED":
        record["value"] = None
        if record["quality_flag"] == "OK":
            record["quality_flag"] = "SOURCE_BLOCKED"
    elif record["availability_status"] == "AVAILABLE" and record["quality_flag"] != "OK":
        record["availability_status"] = "FLAG"
    record["observation_timestamp"] = iso(record["observation_timestamp"])
    return {field: record[field] for field in FIELDS}, output


def build() -> tuple[list[dict], list[dict]]:
    records, register = [], []
    for variable_id in ids_from_tracker():
        record, output = record_for(variable_id)
        records.append(record)
        register.append({
            "variable_id": variable_id,
            "unit_or_scale": record["unit_or_scale"],
            "max_age_days": MAX_AGE_DAYS[variable_id],
            "release_frequency": CADENCE[variable_id][0],
            "publication_lag_days": CADENCE[variable_id][1],
            "observation_date_convention": CADENCE[variable_id][2],
            "freshness_review": "needs_review" if CADENCE[variable_id][3] else None,
            "freshness_policy": "source-availability-aware",
            "source_latest_verified_ts": SOURCE_VERIFICATION.get(variable_id, (None, None, None))[0],
            "source_latest_observation_ts": SOURCE_VERIFICATION.get(variable_id, (None, None, None))[1],
            "source_has_newer_data": SOURCE_VERIFICATION.get(variable_id, (None, None, None))[2],
            "approved_source_reference": record["source_reference"],
            "transformation_output": repo_path(output),
        })
    return records, register


def write_artifacts(records: list[dict], register: list[dict]) -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / "variable_register.json").write_text(json.dumps(register, indent=2) + "\n", encoding="utf-8")
    (OUT / "canonical_dataset.jsonl").write_text("".join(json.dumps(row, separators=(",", ":")) + "\n" for row in records), encoding="utf-8")


def validate(records: list[dict], register: list[dict], now: datetime) -> list[str]:
    failures: list[str] = []
    expected = [row["variable_id"] for row in register]
    actual = [row.get("variable_id") for row in records]
    if len(records) != 44: failures.append(f"record count {len(records)} != 44")
    if actual != expected or len(set(actual)) != len(actual): failures.append("variable IDs are missing, extra, duplicated, or unordered")
    by_id = {row["variable_id"]: row for row in register}
    transformed_records, _ = build()
    transformed_by_id = {row["variable_id"]: row for row in transformed_records}
    seen_values: set[tuple] = set()
    for row in records:
        if tuple(row) != FIELDS: failures.append(f"{row.get('variable_id')}: field order/schema differs")
        variable_id = row.get("variable_id", "unknown")
        if row.get("availability_status") not in STATUSES: failures.append(f"{variable_id}: invalid availability status")
        if row.get("quality_flag") not in QUALITY_FLAGS: failures.append(f"{variable_id}: invalid quality flag")
        if row.get("unit_or_scale") != by_id.get(variable_id, {}).get("unit_or_scale"): failures.append(f"{variable_id}: unit differs from register")
        try:
            timestamp = utc(row["observation_timestamp"])
            if timestamp > now: failures.append(f"{variable_id}: timestamp is in the future")
        except Exception as exc: failures.append(f"{variable_id}: invalid timestamp ({exc})"); continue
        value = row["value"]
        transformed = transformed_by_id.get(variable_id)
        if not transformed or any(row[field] != transformed[field] for field in ("observation_timestamp", "value", "unit_or_scale", "source_reference")):
            failures.append(f"{variable_id}: canonical value does not match its transformation output")
        if row["availability_status"] == "BLOCKED":
            if value is not None or row["quality_flag"] == "OK": failures.append(f"{variable_id}: blocked value/flag invalid")
        elif not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value): failures.append(f"{variable_id}: non-blocked value is not finite")
        expected = expected_latest_observation(variable_id, now.date())
        if expected is not None and variable_id not in SOURCE_VERIFICATION:
            tolerance = TOLERANCE_DAYS[by_id[variable_id]["release_frequency"]]
            stale = utc(row["observation_timestamp"]).date() < expected - timedelta(days=tolerance)
            if stale and row["availability_status"] != "STALE": failures.append(f"{variable_id}: cadence-aware stale rule violated")
            if not stale and row["availability_status"] == "STALE": failures.append(f"{variable_id}: cadence-aware status should be AVAILABLE")
        if row["availability_status"] == "FLAG" and row["quality_flag"] == "OK": failures.append(f"{variable_id}: flagged record lacks reason")
        if not row["source_reference"].startswith("transform=") or "placeholder" in row["source_reference"].lower(): failures.append(f"{variable_id}: untraceable source reference")
        for reference_path in re.findall(r"docs/[A-Za-z0-9_./-]+", row["source_reference"]):
            if not (ROOT / reference_path).exists(): failures.append(f"{variable_id}: missing referenced artifact {reference_path}")
        signature = (row["observation_timestamp"], row["value"], row["unit_or_scale"], row["source_reference"])
        if signature in seen_values: failures.append(f"{variable_id}: duplicate cross-variable observation")
        seen_values.add(signature)
    return failures


def write_report(failures: list[str], records: list[dict], now: datetime) -> None:
    checks = [
        ("44 records and exact variable IDs", not any("record count" in item or "variable IDs" in item for item in failures)),
        ("Seven-field schema and types", not any("field order" in item or "value is not finite" in item for item in failures)),
        ("Timestamp, cadence, and stale detection", not any("timestamp" in item or "stale maximum" in item or "cadence-aware" in item for item in failures)),
        ("Status and quality-flag rules", not any("availability" in item or "blocked" in item or "flagged" in item or "quality flag" in item for item in failures)),
        ("Units, traceable references, and direct transformation comparison", not any("unit" in item or "source reference" in item or "does not match" in item for item in failures)),
        ("No accidental cross-variable copies", not any("duplicate cross-variable" in item for item in failures)),
    ]
    lines = ["# Phase 3 integration check", "", f"Checked at: `{now.isoformat().replace('+00:00', 'Z')}`", "", "| Check | Result |", "|---|---|"]
    lines.extend(f"| {name} | {'PASS' if passed else 'FAIL'} |" for name, passed in checks)
    lines.extend(["", f"Records checked: **{len(records)}**."])
    if failures:
        lines.extend(["", "## Failures", *[f"- {failure}" for failure in failures]])
    else:
        lines.extend(["", "All integration checks passed. Every canonical value was selected directly from a recorded transformation output; no substitute values were created."])
    (OUT / "integration_check_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    records, register = build()
    now = datetime.now(UTC)
    # Apply cadence-aware expected-release logic.  Review-marked variables keep
    # their source/parser status until their timing is confirmed.
    for record in records:
        variable_id = record["variable_id"]
        if variable_id in SOURCE_VERIFICATION:
            _, _, source_has_newer_data = SOURCE_VERIFICATION[variable_id]
            if source_has_newer_data:
                record["availability_status"] = "STALE"
                record["quality_flag"] = "COLLECTOR_LAG"
            elif record["availability_status"] == "STALE":
                record["availability_status"] = "AVAILABLE"
                record["quality_flag"] = "OK"
            continue
        expected = expected_latest_observation(variable_id, now.date())
        if expected is None or record["availability_status"] == "BLOCKED":
            continue
        tolerance = TOLERANCE_DAYS[CADENCE[variable_id][0]]
        stale = utc(record["observation_timestamp"]).date() < expected - timedelta(days=tolerance)
        if stale:
            record["availability_status"] = "STALE"
            record["quality_flag"] = "STALE_MAX_AGE_EXCEEDED"
        elif record["availability_status"] == "STALE":
            record["availability_status"] = "AVAILABLE"
            record["quality_flag"] = "OK"
    write_artifacts(records, register)
    failures = validate(records, register, now)
    write_report(failures, records, now)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
