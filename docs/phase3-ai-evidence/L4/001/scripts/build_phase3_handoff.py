from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

REQUIRED = {
    'variable_id', 'observation_date', 'value', 'unit', 'raw_file_path',
    'retrieved_at', 'validation_status', 'availability_status',
}


def build(input_path: Path, source_reference: str) -> list[dict]:
    with input_path.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError('processed input is empty')
    output = []
    for row in rows:
        missing = REQUIRED - row.keys()
        if missing:
            raise ValueError(f'missing fields: {sorted(missing)}')
        if row['variable_id'] != 'L4-001' or row['unit'] != 'index':
            raise ValueError('invalid L4-001 row')
        if row['validation_status'] != 'PASS':
            raise ValueError('validation failure cannot enter handoff')
        output.append({
            'variable_id': 'L4-001',
            'observation_timestamp': f"{row['observation_date']}T00:00:00Z",
            'value': float(row['value']),
            'unit_or_scale': 'index',
            'availability_status': row['availability_status'],
            'source_reference': source_reference,
            'quality_flag': row['validation_status'],
        })
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--source-reference', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = build(args.input, args.source_reference)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(f'Wrote {len(result)} handoff rows to {args.output}')


if __name__ == '__main__':
    main()
