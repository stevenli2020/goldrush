"""Convert normalized CME Fed Funds settlements into the L3-001 strip input."""
from __future__ import annotations
import argparse
import csv
from datetime import date
from pathlib import Path

def extract(source: Path, output: Path, metadata: str, manifest: str) -> int:
    with source.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    normalized = []
    for row in rows:
        obs = date.fromisoformat(row['observation_date'])
        expiry = date.fromisoformat(row['expiry_date'])
        months = (expiry.year - obs.year) * 12 + expiry.month - obs.month + 1
        if 1 <= months <= 12:
            normalized.append({'observation_date': obs.isoformat(), 'contract': row['contract'], 'implied_rate_percent': f"{100.0 - float(row['settlement_price']):.4f}", 'months_ahead': str(months), 'source_manifest': manifest})
    if not normalized:
        raise ValueError('no eligible Fed Funds contracts found')
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=normalized[0])
        writer.writeheader()
        writer.writerows(normalized)
    return len(normalized)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--source-metadata', required=True)
    parser.add_argument('--manifest', required=True)
    args = parser.parse_args()
    print(f'Wrote {extract(args.input, args.output, args.source_metadata, args.manifest)} strip rows')
