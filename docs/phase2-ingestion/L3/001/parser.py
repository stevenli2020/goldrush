"""Build a simple forward Fed Funds futures path measure."""
from __future__ import annotations
import argparse
import csv
from datetime import date
from pathlib import Path

def parse(path: Path, max_months: int=12) -> list[dict]:
    with path.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    required = {'observation_date', 'contract', 'implied_rate_percent', 'months_ahead', 'source_manifest'}
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f'input must contain {sorted(required)}')
    grouped: dict[str, list[dict]] = {}
    for row in rows:
        obs = date.fromisoformat(row['observation_date'])
        months = int(row['months_ahead'])
        rate = float(row['implied_rate_percent'])
        if months < 1 or months > max_months or (not 0 <= rate <= 20):
            continue
        grouped.setdefault(obs.isoformat(), []).append({'contract': row['contract'], 'rate': rate, 'months': months, 'source_manifest': row['source_manifest']})
    output = []
    for obs, contracts in sorted(grouped.items()):
        if len({item['months'] for item in contracts}) < 2:
            continue
        value = sum((item['rate'] for item in contracts)) / len(contracts)
        output.append({'variable_id': 'L3-001', 'observation_date': obs, 'path_average_percent': value, 'contracts_used': len(contracts), 'horizon_months': max((item['months'] for item in contracts)), 'source_manifest': contracts[0]['source_manifest'], 'unit': 'percent_per_annum', 'source_series_id': 'CME_FED_FUNDS_FUTURES_STRIP', 'validation_status': 'PASS', 'availability_status': 'AVAILABLE'})
    if not output:
        raise ValueError('no observation has at least two eligible futures contracts')
    return output
if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--input', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--max-months', type=int, default=12)
    args = p.parse_args()
    output = parse(args.input, args.max_months)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=output[0])
        writer.writeheader()
        writer.writerows(output)
    print(f'Wrote {len(output)} observations to {args.output}')
