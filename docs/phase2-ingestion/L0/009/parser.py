"""Calculate a simple gold forward-rate minus SOFR3M proxy."""
from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path


def parse(cme_csv: Path, sofr_csv: Path) -> list[dict]:
    with cme_csv.open(newline="", encoding="utf-8") as f:
        cme = list(csv.DictReader(f))
    with sofr_csv.open(newline="", encoding="utf-8") as f:
        sofr = {row["observation_date"]: float(row["sofr3m_percent"]) for row in csv.DictReader(f)}
    required = {"observation_date", "near_settlement", "far_settlement", "days"}
    if not cme or not required.issubset(cme[0]):
        raise ValueError(f"CME input must contain {sorted(required)}")
    rows = []
    for row in cme:
        obs = date.fromisoformat(row["observation_date"])
        near, far, days = float(row["near_settlement"]), float(row["far_settlement"]), int(row["days"])
        if near <= 0 or far <= 0 or days <= 0:
            raise ValueError(f"invalid CME row: {row}")
        if row["observation_date"] not in sofr:
            continue
        forward = ((far / near) ** (365.0 / days) - 1.0) * 100.0
        value = forward - sofr[row["observation_date"]]
        rows.append({"variable_id": "L0-009", "observation_date": obs.isoformat(), "value": value,
                     "unit": "percent_per_annum", "forward_rate_percent": forward,
                     "sofr3m_percent": sofr[row["observation_date"]],
                     "validation_status": "PASS" if abs(value) <= 20 else "FLAG",
                     "availability_status": "AVAILABLE"})
    if not rows:
        raise ValueError("no overlapping CME/SOFR3M observations")
    return rows


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--cme", type=Path, required=True)
    p.add_argument("--sofr", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    rows = parse(args.cme, args.sofr)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0]); writer.writeheader(); writer.writerows(rows)
    print(f"Wrote {len(rows)} observations to {args.output}")
