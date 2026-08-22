"""Parse CME metals open-interest summaries for COMEX Gold."""
from __future__ import annotations

import argparse
import csv
import re
from datetime import date
from pathlib import Path


def parse(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    required = {"observation_date", "product", "open_interest", "source_pdf_sha256", "source_manifest"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f"input must contain {sorted(required)}")
    selected = []
    seen = set()
    for row in rows:
        if row["product"].strip().upper() != "COMEX GOLD":
            continue
        obs = date.fromisoformat(row["observation_date"])
        if obs.isoformat() in seen:
            raise ValueError(f"duplicate COMEX GOLD observation: {obs.isoformat()}")
        value = int(row["open_interest"])
        if value < 0:
            raise ValueError(f"negative open interest: {row}")
        if not re.fullmatch(r"[a-f0-9]{64}", row["source_pdf_sha256"]):
            raise ValueError("source_pdf_sha256 must be a 64-character lowercase SHA-256")
        if not row["source_manifest"].strip():
            raise ValueError("source_manifest must not be empty")
        seen.add(obs.isoformat())
        selected.append({"variable_id": "L10-002", "observation_date": obs.isoformat(),
                         "product": "COMEX GOLD", "open_interest_contracts": value,
                         "unit": "contracts", "source_series_id": "COMEX_GOLD",
                         "source_pdf_sha256": row["source_pdf_sha256"],
                         "source_manifest": row["source_manifest"],
                         "validation_status": "PASS", "availability_status": "AVAILABLE"})
    if not selected:
        raise ValueError("no COMEX GOLD open-interest row found")
    return sorted(selected, key=lambda row: row["observation_date"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--input", type=Path, required=True); p.add_argument("--output", type=Path, required=True)
    args = p.parse_args(); output = parse(args.input); args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=output[0]); writer.writeheader(); writer.writerows(output)
    print(f"Wrote {len(output)} observations to {args.output}")
