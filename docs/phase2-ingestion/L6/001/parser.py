"""Parse the published GPR daily acts/headline/threat indices."""
from __future__ import annotations
import argparse, csv, json, math, re
from datetime import date, datetime, timezone
from pathlib import Path
import pandas as pd
VARIABLE = 'L6-001'
VERSION = '0.1.0'
FIELDS = ['variable_id', 'observation_date', 'gpr_headline_index', 'gpr_threat_index', 'gpr_act_index', 'unit', 'source_name', 'source_url', 'source_vintage_date', 'raw_path', 'manifest_path', 'retrieved_at', 'validation_status', 'availability_status', 'fallback_checked_at', 'parser_version']

def metadata(p):
    return None

def stamp(v, field):
    if not isinstance(v, str) or not v:
        raise ValueError(f'{field} missing')
    try:
        datetime.fromisoformat(v.replace('Z', '+00:00'))
    except ValueError as e:
        raise ValueError(f'{field} invalid') from e

def load_manifest(mp, rp):
    m = json.loads(mp.read_text(encoding='utf-8'))
    req = {'source_url', 'retrieved_at', 'source_vintage_date', 'raw_path', 'size_bytes', 'collector_version'}
    if not req.issubset(m):
        raise ValueError('manifest missing required fields')
    stamp(m['retrieved_at'], 'retrieved_at')
    date.fromisoformat(m['source_vintage_date'])
    return m

def parse(raw, manifest, as_of=None, stale_days=10):
    m = load_manifest(manifest, raw)
    df = pd.read_stata(raw, convert_categoricals=False)
    if not {'date', 'GPRD', 'GPRD_THREAT', 'GPRD_ACT'}.issubset(df.columns):
        raise ValueError('missing GPR columns')
    vals = {}
    try:
        parsed_dates = pd.to_datetime(df['date'], errors='raise')
    except Exception as e:
        raise ValueError('malformed GPR date') from e
    raw_columns = {c: df[c].tolist() for c in ('GPRD', 'GPRD_THREAT', 'GPRD_ACT')}
    numeric = {c: pd.to_numeric(df[c], errors='coerce').tolist() for c in ('GPRD', 'GPRD_THREAT', 'GPRD_ACT')}
    for i, dval in enumerate(parsed_dates):
        d = dval.date().isoformat()
        nums = []
        for col in ('GPRD', 'GPRD_THREAT', 'GPRD_ACT'):
            raw_value = raw_columns[col][i]
            if pd.isna(raw_value) or str(raw_value).strip() in {'.', ''}:
                nums.append(None)
                continue
            x = numeric[col][i]
            if pd.isna(x) or not math.isfinite(float(x)) or x < 0:
                raise ValueError(f'invalid {col}')
            nums.append(float(x))
        if any((x is None for x in nums)):
            continue
        if d in vals and vals[d] != nums:
            raise ValueError(f'conflicting duplicate date {d}')
        vals[d] = nums
    if not vals:
        raise ValueError('no valid GPR observations')
    today = date.fromisoformat(as_of) if as_of else datetime.now(timezone.utc).date()
    rh = None
    mh = None
    out = []
    for d, (h, t, a) in sorted(vals.items()):
        out.append({'variable_id': VARIABLE, 'observation_date': d, 'gpr_headline_index': h, 'gpr_threat_index': t, 'gpr_act_index': a, 'unit': 'published_index_points', 'source_name': 'Caldara-Iacoviello Daily Recent Geopolitical Risk', 'source_url': m['source_url'], 'source_vintage_date': m['source_vintage_date'], 'raw_path': str(raw), 'manifest_path': str(manifest), 'retrieved_at': m['retrieved_at'], 'validation_status': 'PASS', 'availability_status': 'AVAILABLE' if (today - date.fromisoformat(d)).days <= stale_days else 'STALE', 'fallback_checked_at': None, 'parser_version': VERSION})
    return out

def validate_prior(row):
    if row.get('variable_id') != VARIABLE or row.get('unit') != 'published_index_points' or row.get('validation_status') not in {'PASS', 'FLAG'}:
        raise ValueError('invalid prior identity/status')
    try:
        date.fromisoformat(row['observation_date'])
    except (KeyError, ValueError) as exc:
        raise ValueError('invalid prior observation date') from exc
    for c in ('gpr_headline_index', 'gpr_threat_index', 'gpr_act_index'):
        try:
            x = float(row[c])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f'invalid prior {c}') from exc
        if not math.isfinite(x) or x < 0:
            raise ValueError(f'invalid prior {c}')
    for c in ():
        if not re.fullmatch('[0-9a-f]{64}', row.get(c, '')):
            raise ValueError('invalid prior source metadata')
    for c in ('raw_path', 'manifest_path', 'source_url', 'source_vintage_date', 'retrieved_at', 'parser_version'):
        if not row.get(c):
            raise ValueError(f'missing prior provenance: {c}')
    stamp(row['retrieved_at'], 'prior retrieved_at')
    try:
        date.fromisoformat(row['source_vintage_date'])
    except ValueError as exc:
        raise ValueError('invalid prior source vintage') from exc
    if row.get('availability_status') not in {'AVAILABLE', 'STALE'}:
        raise ValueError('invalid prior availability status')

def carry_forward(prior, checked_at=None):
    if not prior or not prior.exists():
        raise FileNotFoundError('no prior L6-001 output exists')
    rows = list(csv.DictReader(prior.open(newline='', encoding='utf-8')))
    [validate_prior(r) for r in rows]
    if not rows:
        raise ValueError('prior has no valid rows')
    r = max(rows, key=lambda x: x['observation_date'])
    r['availability_status'] = 'STALE'
    r['fallback_checked_at'] = checked_at or datetime.now(timezone.utc).isoformat()
    r['parser_version'] = VERSION
    return [r]

def write(rows, out):
    out.parent.mkdir(parents=True, exist_ok=True)
    out.with_suffix('.status.json').unlink(missing_ok=True)
    with out.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

def blocked(out, reason):
    out.parent.mkdir(parents=True, exist_ok=True)
    p = out.with_suffix('.status.json')
    p.write_text(json.dumps({'variable_id': VARIABLE, 'status': 'BLOCKED', 'availability_status': 'BLOCKED', 'reason': reason, 'checked_at': datetime.now(timezone.utc).isoformat(), 'parser_version': VERSION}, indent=2) + '\n')
    return p

def main():
    root = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument('--raw', type=Path)
    ap.add_argument('--manifest', type=Path)
    ap.add_argument('--prior', type=Path)
    ap.add_argument('--output', type=Path, default=root / 'data/processed/l6_001.csv')
    ap.add_argument('--as-of')
    a = ap.parse_args()
    try:
        rows = parse(a.raw, a.manifest, as_of=a.as_of) if a.raw and a.manifest else (_ for _ in ()).throw(ValueError('raw and manifest required'))
    except (OSError, ValueError, KeyError) as e:
        try:
            rows = carry_forward(a.prior)
        except Exception as f:
            p = blocked(a.output, f'{e}; {f}')
            print(json.dumps({'status': 'BLOCKED', 'status_path': str(p)}))
            return 0
    write(rows, a.output)
    print(f'Wrote {len(rows)} rows to {a.output}')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
