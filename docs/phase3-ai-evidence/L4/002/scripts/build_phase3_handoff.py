from __future__ import annotations
import argparse, csv, json
from pathlib import Path

REQUIRED = {'variable_id','observation_date','value','unit','raw_file_path','retrieved_at','validation_status','availability_status'}

def build(input_path: Path, source_reference: str) -> list[dict]:
    with input_path.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    if not rows: raise ValueError('processed input is empty')
    result = []
    for row in rows:
        if REQUIRED - row.keys(): raise ValueError('processed input is missing required fields')
        if row['variable_id'] != 'L4-002' or row['unit'] != 'index' or row['validation_status'] != 'PASS':
            raise ValueError('invalid L4-002 row')
        result.append({'variable_id':'L4-002','observation_timestamp':f"{row['observation_date']}T00:00:00Z",'value':float(row['value']),'unit_or_scale':'index','availability_status':row['availability_status'],'source_reference':source_reference,'quality_flag':row['validation_status']})
    return result

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--input', type=Path, required=True); ap.add_argument('--source-reference', required=True); ap.add_argument('--output', type=Path, required=True); args = ap.parse_args()
    out = build(args.input, args.source_reference); args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(out, indent=2)+'\n', encoding='utf-8'); print(f'Wrote {len(out)} handoff rows to {args.output}')
