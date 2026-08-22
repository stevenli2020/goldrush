"""Parse the L1-003 GS&W zero-coupon TIPS forward-rate summary."""
from __future__ import annotations
import argparse, csv, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

VARIABLE_ID = "L1-003"
INPUTS = ("TIPSY02", "TIPSY03", "TIPSY05", "TIPSY07", "TIPSY10", "TIPSY20")
FORMULA_VERSION = "gsw-forward-summary-v1"
PARSER_VERSION = "0.1.0"
FIELDS = ["variable_id", "observation_date", "value", "unit", "forward_2y1y", "forward_3y2y", "forward_5y2y", "forward_7y3y", "forward_10y10y", "source_name", "source_url", "raw_file_path", "raw_sha256", "source_retrieved_at", "formula_version", "parser_version", "is_revised", "prior_source_sha256", "revision_reason", "validation_status", "availability_status"]

def read_rows(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        lines = list(csv.reader(handle))
    header_index = next((i for i, row in enumerate(lines) if row and row[0].strip() == "Date"), None)
    if header_index is None: raise ValueError("GS&W CSV Date header not found")
    headers = lines[header_index]
    required = ["Date", *INPUTS]
    if any(name not in headers for name in required): raise ValueError("GS&W CSV missing required TIPSY columns")
    positions = {name: headers.index(name) for name in required}
    return [{name: row[positions[name]].strip() if len(row) > positions[name] else "" for name in required} for row in lines[header_index + 1:] if row]

def calculate_components(values):
    y2, y3, y5, y7, y10, y20 = (values[name] for name in INPUTS)
    return {"forward_2y1y": 3*y3 - 2*y2, "forward_3y2y": (5*y5 - 3*y3)/2, "forward_5y2y": (7*y7 - 5*y5)/2, "forward_7y3y": (10*y10 - 7*y7)/3, "forward_10y10y": 2*y20 - y10}

def parse_source(raw_path: Path, *, source_retrieved_at: str, previous_output: Path | None = None, stale_after_days: int = 7):
    raw_hash = hashlib.sha256(raw_path.read_bytes()).hexdigest(); source_rows = read_rows(raw_path); now = datetime.now(timezone.utc)
    prior = {}
    if previous_output and previous_output.exists():
        with previous_output.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle): prior[row.get("observation_date", "")] = row
    output=[]
    for item in source_rows:
        if any(item[name] in ("", ".", "NA", "N/A") for name in INPUTS): continue
        try:
            date = datetime.strptime(item["Date"], "%Y-%m-%d").date(); values = {name: float(item[name]) for name in INPUTS}
        except (TypeError, ValueError) as exc: raise ValueError(f"malformed GS&W row: {item}") from exc
        components = calculate_components(values); value = sum(components.values()) / len(components); previous = prior.get(item["Date"])
        revised = bool(previous and previous.get("value") and abs(float(previous["value"]) - value) > 1e-12)
        output.append({"variable_id": VARIABLE_ID, "observation_date": item["Date"], "value": value, **components, "unit": "percent", "source_name": "Federal Reserve GS&W", "source_url": "https://www.federalreserve.gov/data/yield-curve-tables/feds200805.csv", "raw_file_path": str(raw_path), "raw_sha256": raw_hash, "source_retrieved_at": source_retrieved_at, "formula_version": FORMULA_VERSION, "parser_version": PARSER_VERSION, "is_revised": revised, "prior_source_sha256": previous.get("raw_sha256") if revised else None, "revision_reason": "Source revision changed derived value" if revised else None, "validation_status": "PASS" if -10 <= value <= 20 else "FLAG", "availability_status": "STALE" if (now.date() - date).days > stale_after_days else "AVAILABLE"})
    if not output: raise ValueError("no complete six-input observations found")
    return output

def write_csv(rows, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle: writer=csv.DictWriter(handle, fieldnames=FIELDS); writer.writeheader(); writer.writerows(rows)

if __name__ == "__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--raw", type=Path, required=True); ap.add_argument("--source-retrieved-at", required=True); ap.add_argument("--output", type=Path, default=Path("data/processed/L1_003_observations.csv")); ap.add_argument("--previous-output", type=Path); args=ap.parse_args(); rows=parse_source(args.raw, source_retrieved_at=args.source_retrieved_at, previous_output=args.previous_output); write_csv(rows,args.output); print(f"Wrote {len(rows)} observations to {args.output}")
