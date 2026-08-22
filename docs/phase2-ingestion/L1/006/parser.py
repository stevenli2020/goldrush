"""Parse normalized 30-Day Fed Funds futures settlements into L1-006."""
from __future__ import annotations
import argparse, csv, json, re
from datetime import date, datetime
from pathlib import Path

PARSER_VERSION = "0.1.0"
REQUIRED = {"observation_date", "contract", "settlement_price", "expiry_date"}
CONTRACT_RE = re.compile(r"^ZQ[A-Z]\d{2}$")

def parse(path: Path, retrieved_at: str, source_pdf_sha256: str = "", source_url: str = "https://www.cmegroup.com/daily_bulletin/current/Section10_Interest_Rate_Futures_Continued.pdf") -> list[dict]:
    candidates = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            raise ValueError(f"missing required columns: {sorted(REQUIRED - set(reader.fieldnames or []))}")
        for row in reader:
            try:
                obs = date.fromisoformat(row["observation_date"])
                expiry = date.fromisoformat(row["expiry_date"])
                contract = row["contract"].strip()
                if not CONTRACT_RE.fullmatch(contract):
                    continue
                settle = float(row["settlement_price"])
                if not obs or not expiry or settle <= 0: raise ValueError
                value = 100.0 - settle
                retrieved = datetime.fromisoformat(retrieved_at.replace("Z", "+00:00"))
                if expiry <= obs:
                    continue
                age = (retrieved.date() - obs).days
                availability = "STALE" if age > 3 else "AVAILABLE"
                validation = "FLAG" if not 0 <= value <= 20 else "PASS"
                candidates.append({"variable_id":"L1-006", "observation_date":obs.isoformat(), "value":value, "unit":"percent_per_annum",
                    "source_name":"CME 30-Day Fed Funds futures", "source_series_id":contract, "settlement_price":settle,
                    "expiry_date":expiry.isoformat(), "source_url":source_url, "source_pdf_sha256":source_pdf_sha256,
                    "retrieved_at":retrieved_at, "formula_version":"1.0.0", "parser_version":PARSER_VERSION,
                    "validation_status":validation, "availability_status":availability})
            except (TypeError, ValueError) as exc:
                raise ValueError(f"malformed settlement row: {row}") from exc
    # Keep only the nearest contract still beyond the observation date.
    rows = []
    seen = set()
    for obs in sorted({r["observation_date"] for r in candidates}):
        eligible = [r for r in candidates if r["observation_date"] == obs]
        duplicate_keys = [(r["observation_date"], r["source_series_id"]) for r in eligible]
        if len(set(duplicate_keys)) != len(duplicate_keys):
            raise ValueError(f"duplicate observation/contract row for {obs}")
        if eligible:
            rows.append(min(eligible, key=lambda r: r["expiry_date"]))
    if not rows:
        raise ValueError("no eligible ZQ 30-Day Fed Funds contract rows found")
    return rows

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("csv_path", type=Path); p.add_argument("--retrieved-at", required=True); p.add_argument("--sha256", default=""); p.add_argument("--output", type=Path, required=True)
    a = p.parse_args(); out = parse(a.csv_path, a.retrieved_at, a.sha256); a.output.parent.mkdir(parents=True, exist_ok=True)
    with a.output.open("w", newline="", encoding="utf-8") as f: w=csv.DictWriter(f, fieldnames=out[0].keys()); w.writeheader(); w.writerows(out)
    print(json.dumps({"rows":len(out), "latest":out[-1] if out else None}, indent=2))
