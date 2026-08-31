"""Inspect preserved CME PDFs and dispatch the four CME variable parsers."""
from __future__ import annotations
import argparse, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data' / 'cme'
MANIFESTS, LOGS = (DATA / 'manifests', DATA / 'logs')
INTERMEDIATE = DATA / 'processed'
EXTRACTOR = ROOT / 'L1' / '006' / 'extract_settlements.py'
SECTION62_EXTRACTOR = ROOT / 'L0' / '009' / 'extract_section62.py'
PARSER = ROOT / 'L1' / '006' / 'parser.py'
OUTPUT = ROOT / 'L1' / '006' / 'data' / 'processed' / 'L1_006_observations.csv'
L10_PARSER = ROOT / 'L10' / '002' / 'parser.py'
L10_OUTPUT = ROOT / 'L10' / '002' / 'data' / 'processed' / 'L10_002_observations.csv'
DISPATCH = {'l0_009': (ROOT / 'L0' / '009' / 'parser.py', ROOT / 'data' / 'cme' / 'processed' / 'section62_normalized.csv', ROOT / 'L0' / '009' / 'data' / 'raw' / 'sofr3m.csv', ROOT / 'L0' / '009' / 'data' / 'processed' / 'L0_009_observations.csv'), 'l3_001': (ROOT / 'L3' / '001' / 'parser.py', ROOT / 'L3' / '001' / 'data' / 'raw' / 'fed_funds_strip.csv', None, ROOT / 'L3' / '001' / 'data' / 'processed' / 'L3_001_observations.csv')}

def latest_manifests() -> list[dict]:
    latest = {}
    for path in MANIFESTS.glob('*.json'):
        try:
            record = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, json.JSONDecodeError):
            continue
        if record.get('target') and (record['target'] not in latest or record.get('retrieved_at', '') > latest[record['target']].get('retrieved_at', '')):
            latest[record['target']] = record
    return list(latest.values())

def run(command: list[str], verbose: bool) -> tuple[int, str, str]:
    if verbose:
        print('[debug] ' + ' '.join(command))
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if verbose and result.stdout.strip():
        print(result.stdout.strip())
    if verbose and result.stderr.strip() and ('30D FED FD FUT section not found' not in result.stderr):
        print(result.stderr.strip(), file=sys.stderr)
    return (result.returncode, result.stdout, result.stderr)

def latest_download_status(target: str) -> str | None:
    for path in sorted(LOGS.glob('cme-download-*.json'), reverse=True):
        try:
            results = json.loads(path.read_text(encoding='utf-8'))['results']
        except (OSError, json.JSONDecodeError, KeyError):
            continue
        for result in results:
            if result.get('target') == target:
                return result.get('status')
    return None

def dispatch_normalized(results: list[dict], verbose: bool) -> None:
    for name, (parser, primary, secondary, output) in DISPATCH.items():
        if not primary.exists() or (secondary is not None and (not secondary.exists())):
            results.append({'target': name, 'status': 'SKIPPED', 'reason': 'normalized input not present'})
            continue
        command = [sys.executable, str(parser)]
        if name == 'l0_009':
            command += ['--cme', str(primary), '--sofr', str(secondary)]
        else:
            command += ['--input', str(primary)]
        command += ['--output', str(output)]
        code, out, err = run(command, verbose)
        results.append({'target': name, 'status': 'PASS' if code == 0 else 'FAIL', 'stage': 'parse', 'stdout': out[-1000:], 'stderr': err[-1000:]})

def dispatch_l10_002(results: list[dict], verbose: bool) -> None:
    manifests = sorted(MANIFESTS.glob('section02b-*.json'))
    if not manifests:
        results.append({'target': 'l10_002', 'status': 'BLOCKED', 'reason': 'Section 02B manifest not present'})
        return
    manifest_path = manifests[-1]
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    raw = Path(manifest['raw_path'])
    download_status = latest_download_status('section02b')
    if download_status is not None and download_status != 'PASS':
        results.append({'target': 'l10_002', 'status': 'BLOCKED', 'stage': 'download', 'error': f'latest Section 02B download status: {download_status}'})
        return
    if not raw.exists():
        results.append({'target': 'l10_002', 'status': 'BLOCKED', 'stage': 'parse', 'error': 'Section 02B raw PDF not present'})
        return
    command = [sys.executable, str(L10_PARSER), '--pdf', str(raw), '--source-manifest', str(manifest_path), '--output', str(L10_OUTPUT)]
    code, out, err = run(command, verbose)
    results.append({'target': 'l10_002', 'status': 'PASS' if code == 0 else 'BLOCKED', 'stage': 'parse', 'stdout': out[-1000:], 'stderr': err[-1000:]})

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description='Extract L1-006 from preserved CME interest-rate PDFs')
    p.add_argument('--observation-date', help='ISO date; defaults to each manifest retrieval date')
    p.add_argument('--force', action='store_true', help='rerun unchanged manifests')
    p.add_argument('--verbose', '--debug', action='store_true', help='show discovery and parser commands')
    args = p.parse_args(argv)
    results = []
    candidates = []
    manifests = sorted(latest_manifests(), key=lambda item: item['target'])
    for manifest in manifests:
        target, raw = (manifest['target'], Path(manifest['raw_path']))
        if not raw.is_absolute():
            raw = (ROOT / raw).resolve()
        INTERMEDIATE.mkdir(parents=True, exist_ok=True)
        normalized = INTERMEDIATE / f'{target}_normalized.csv'
        obs_date = args.observation_date or manifest.get('observation_date') or manifest.get('retrieved_at', '')[:10]
        extractor = SECTION62_EXTRACTOR if target == 'section62' else EXTRACTOR
        command = [sys.executable, str(extractor), '--pdf', str(raw), '--observation-date', obs_date, '--output', str(normalized)] if target == 'section62' else [sys.executable, str(extractor), str(raw), '--observation-date', obs_date, '--output', str(normalized)]
        code, out, err = run(command, args.verbose)
        if code != 0:
            if '30D FED FD FUT section not found' in err:
                results.append({'target': target, 'status': 'INSPECTED_UNUSED', 'reason': 'required marker not present; raw file retained'})
            else:
                results.append({'target': target, 'status': 'FAIL', 'stage': 'extract', 'stderr': err[-1000:]})
            continue
        candidates.append((manifest, normalized, target))
    if candidates:
        manifest, normalized, target = candidates[0]
        code, out, err = run([sys.executable, str(PARSER), str(normalized), '--retrieved-at', manifest['retrieved_at'], '--output', str(OUTPUT)], args.verbose)
        results.append({'target': target, 'status': 'PASS' if code == 0 else 'FAIL', 'stage': 'parse', 'selected': True, 'stdout': out[-1000:], 'stderr': err[-1000:]})
        for other_manifest, _, other_target in candidates[1:]:
            results.append({'target': other_target, 'status': 'INSPECTED_UNUSED', 'reason': f'another section selected ({target}); raw file retained'})
    elif not any((item['status'] == 'FAIL' for item in results)):
        results.append({'target': 'L1-006', 'status': 'FAIL', 'stage': 'extract', 'error': 'no preserved CME section contains 30D FED FD FUT'})
    dispatch_l10_002(results, args.verbose)
    dispatch_normalized(results, args.verbose)
    LOGS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    (LOGS / f'cme-extract-{stamp}.json').write_text(json.dumps({'run_at': datetime.now(timezone.utc).isoformat(), 'results': results}, indent=2) + '\n', encoding='utf-8')
    for result in results:
        print(f"{result['status']} {result['target']}")
    return int(any((result['status'] in {'FAIL', 'BLOCKED'} for result in results)))
if __name__ == '__main__':
    raise SystemExit(main())
