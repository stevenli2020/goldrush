"""Build the L3-002 Forward Policy Rate Curve from normalized CME ZQ settlements."""
from __future__ import annotations
import argparse
import csv
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path
VARIABLE_ID = 'L3-002'
PARSER_VERSION = '0.1.1'
FORMULA_VERSION = '1.0.0'
CONTRACT_RE = re.compile('^ZQ[FGHJKMNQUVXZ]\\d{2}$')
REQUIRED = {'observation_date', 'contract', 'settlement_price', 'expiry_date'}
FIELDS = ['variable_id', 'observation_date', 'contract', 'settlement_price', 'implied_policy_rate_pct', 'expiry_date', 'months_ahead', 'curve_position', 'unit', 'source_name', 'source_url', 'source_pdf_path', 'source_manifest_path', 'retrieved_at', 'formula_version', 'parser_version', 'is_revised', 'prior_settlement_price', 'validation_status', 'availability_status']

def metadata_file(path: Path) -> str:
    return None

def load_manifest(path: Path, source_pdf: Path) -> dict:
    manifest = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(manifest, dict) or manifest.get('target') not in {'section09', 'section10'}:
        raise ValueError('manifest must describe CME section09 or section10')
    metadata = None
    for field in ('source_url', 'retrieved_at'):
        if not manifest.get(field):
            raise ValueError(f'manifest missing {field}')
    if not source_pdf.is_file():
        raise ValueError('source PDF does not exist')
    return manifest

def prior_values(path: Path | None) -> dict[tuple[str, str], float]:
    if path is None or not path.exists():
        return {}
    with path.open(newline='', encoding='utf-8') as handle:
        return {(row['observation_date'], row['contract']): float(row['settlement_price']) for row in csv.DictReader(handle) if row.get('validation_status') == 'PASS'}

def parse_curve(source: Path, manifest_path: Path, source_pdf: Path, prior_path: Path | None=None, stale_after_days: int=3) -> list[dict]:
    manifest = load_manifest(manifest_path, source_pdf)
    retrieved = datetime.fromisoformat(manifest['retrieved_at'].replace('Z', '+00:00'))
    previous = prior_values(prior_path)
    with source.open(newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            raise ValueError(f'missing required columns: {sorted(REQUIRED - set(reader.fieldnames or []))}')
        input_rows = list(reader)
    candidates: dict[tuple[str, str], dict] = {}
    for row in input_rows:
        try:
            obs = date.fromisoformat(row['observation_date'])
            expiry = date.fromisoformat(row['expiry_date'])
            contract = row['contract'].strip()
            settlement = float(row['settlement_price'])
        except (TypeError, ValueError) as exc:
            raise ValueError(f'malformed settlement row: {row}') from exc
        if not CONTRACT_RE.fullmatch(contract):
            raise ValueError(f'malformed ZQ contract: {contract}')
        if not 80 <= settlement <= 101:
            raise ValueError(f'invalid ZQ settlement price: {settlement}')
        if manifest.get('observation_date') and obs.isoformat() != manifest['observation_date']:
            raise ValueError('settlement observation date does not match manifest')
        if expiry <= obs:
            continue
        key = (obs.isoformat(), contract)
        normalized = {'observation_date': obs, 'contract': contract, 'settlement_price': settlement, 'expiry_date': expiry}
        if key in candidates and candidates[key] != normalized:
            raise ValueError(f'conflicting duplicate settlement: {key}')
        candidates[key] = normalized
    if not candidates:
        raise ValueError('no eligible unexpired ZQ contracts')
    rows = []
    ordered = sorted(candidates.values(), key=lambda item: (item['observation_date'], item['expiry_date']))
    positions: dict[str, int] = {}
    for item in ordered:
        obs, expiry = (item['observation_date'], item['expiry_date'])
        positions[obs.isoformat()] = positions.get(obs.isoformat(), 0) + 1
        settlement = item['settlement_price']
        rate = round(100.0 - settlement, 6)
        prior = previous.get((obs.isoformat(), item['contract']))
        age = (retrieved.date() - obs).days
        rows.append({'variable_id': VARIABLE_ID, 'observation_date': obs.isoformat(), 'contract': item['contract'], 'settlement_price': settlement, 'implied_policy_rate_pct': rate, 'expiry_date': expiry.isoformat(), 'months_ahead': (expiry.year - obs.year) * 12 + expiry.month - obs.month + 1, 'curve_position': positions[obs.isoformat()], 'unit': 'percent_per_annum', 'source_name': 'CME 30-Day Fed Funds futures', 'source_url': manifest['source_url'], 'source_pdf_path': str(source_pdf), 'source_manifest_path': str(manifest_path), 'retrieved_at': manifest['retrieved_at'], 'formula_version': FORMULA_VERSION, 'parser_version': PARSER_VERSION, 'is_revised': prior is not None and prior != settlement, 'prior_settlement_price': prior if prior is not None and prior != settlement else None, 'validation_status': 'PASS' if 0 <= rate <= 20 else 'FLAG', 'availability_status': 'STALE' if age > stale_after_days else 'AVAILABLE'})
    return rows

def carry_forward(prior_path: Path) -> list[dict]:
    if not prior_path.exists():
        raise FileNotFoundError('no prior L3-002 curve is available')
    with prior_path.open(newline='', encoding='utf-8') as handle:
        rows = [row for row in csv.DictReader(handle) if row.get('validation_status') == 'PASS']
    if not rows:
        raise ValueError('prior L3-002 output contains no valid curve')
    latest_date = max((row['observation_date'] for row in rows))
    result = [row for row in rows if row['observation_date'] == latest_date]
    for row in result:
        row['availability_status'] = 'STALE'
    return result

def write_csv(rows: list[dict], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.with_suffix('.status.json').unlink(missing_ok=True)
    with output.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

def write_blocked(output: Path, reason: str) -> Path:
    path = output.with_suffix('.status.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({'variable_id': VARIABLE_ID, 'status': 'BLOCKED', 'availability_status': 'BLOCKED', 'reason': reason, 'checked_at': datetime.now(timezone.utc).isoformat(), 'parser_version': PARSER_VERSION}, indent=2) + '\n', encoding='utf-8')
    return path

def main(argv: list[str] | None=None) -> int:
    cli = argparse.ArgumentParser(description='Build L3-002 Forward Policy Rate Curve')
    cli.add_argument('--input', type=Path)
    cli.add_argument('--manifest', type=Path)
    cli.add_argument('--source-pdf', type=Path)
    cli.add_argument('--prior', type=Path)
    cli.add_argument('--output', type=Path, default=Path('data/processed/L3_002_curve.csv'))
    args = cli.parse_args(argv)
    try:
        if args.input and args.manifest and args.source_pdf:
            rows = parse_curve(args.input, args.manifest, args.source_pdf, args.prior)
        elif args.prior:
            rows = carry_forward(args.prior)
        else:
            raise ValueError('provide source input, manifest, and PDF, or --prior')
    except (OSError, ValueError) as exc:
        if args.prior:
            try:
                rows = carry_forward(args.prior)
            except (OSError, ValueError) as fallback_exc:
                path = write_blocked(args.output, str(fallback_exc))
                print(json.dumps({'status': 'BLOCKED', 'status_path': str(path)}))
                return 0
        else:
            path = write_blocked(args.output, str(exc))
            print(json.dumps({'status': 'BLOCKED', 'status_path': str(path)}))
            return 0
    write_csv(rows, args.output)
    print(json.dumps({'rows': len(rows), 'observation_date': rows[-1]['observation_date']}))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
