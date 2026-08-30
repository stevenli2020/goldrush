"""Dispatch changed WGC workbooks to explicitly configured variable parsers."""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
import yaml

def load_config(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding='utf-8'))

def latest_manifests(root: Path) -> list[dict]:
    latest = {}
    for path in root.glob('*.json'):
        try:
            record = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, json.JSONDecodeError):
            continue
        if 'target' not in record or 'raw_path' not in record:
            continue
        prior = latest.get(record['target'])
        if not prior or record.get('downloaded_at', '') > prior.get('downloaded_at', ''):
            latest[record['target']] = record
    return list(latest.values())

def run_parser(mapping: dict, raw_path: Path, project_root: Path, manifest: dict, verbose: bool=False) -> dict:
    command = [sys.executable, str(project_root / mapping['script']), *mapping.get('args', [])]
    replacements = {'{input}': str(raw_path), '{manifest}': str(manifest.get('manifest_path', '')), '{download_date}': manifest.get('downloaded_at', '')[:10], '{publication_date}': mapping.get('publication_date', '')}
    command = [next((item.replace(token, value) for token, value in replacements.items() if token in item), item) for item in command]
    if verbose:
        print(f"[extract] running: {' '.join(command)}", flush=True)
    completed = subprocess.run(command, cwd=project_root, capture_output=True, text=True, check=False)
    if verbose:
        print(f'[extract] parser return code: {completed.returncode}', flush=True)
        if completed.stdout.strip():
            print(f'[extract] stdout: {completed.stdout.strip()[-1000:]}', flush=True)
        if completed.stderr.strip():
            print(f'[extract] stderr: {completed.stderr.strip()[-1000:]}', flush=True)
    return {'command': command, 'returncode': completed.returncode, 'stdout': completed.stdout[-2000:], 'stderr': completed.stderr[-2000:]}

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description='Dispatch WGC workbooks to variable parsers')
    parser.add_argument('--config', type=Path, default=Path(__file__).with_name('config.yaml'))
    parser.add_argument('--force', action='store_true', help='run parsers even when manifest changed=false')
    parser.add_argument('--verbose', '--debug', action='store_true', help='print extraction progress and parser output')
    args = parser.parse_args(argv)
    config_path = args.config.resolve()
    config = load_config(config_path)
    project_root = config_path.parents[4]
    base = config_path.parent
    manifest_root = (base / config['collector']['manifest_root']).resolve()
    log_root = (base / config['collector']['log_root']).resolve()
    mappings = config.get('extractors', {})
    results = []
    manifests = latest_manifests(manifest_root)
    if args.verbose:
        print(f'[extract] loaded {len(manifests)} latest manifest(s) from {manifest_root}', flush=True)
    for manifest in manifests:
        target = manifest['target']
        if args.verbose:
            print(f"[extract] target={target} changed={manifest.get('changed', True)} =", flush=True)
        mapping = mappings.get(target)
        if not mapping:
            if args.verbose:
                print(f'[extract] {target}: no parser mapping; skipped', flush=True)
            results.append({'target': target, 'status': 'SKIPPED', 'reason': 'no parser mapping configured'})
            continue
        raw_path = Path(manifest['raw_path'])
        if not raw_path.is_absolute():
            raw_path = (project_root / raw_path).resolve()
        if not args.force and (not manifest.get('changed', True)):
            if target == 'gold_premiums' and isinstance(mapping, dict) and mapping.get('unchanged_args'):
                refresh_mapping = {'script': mapping['script'], 'args': mapping['unchanged_args']}
                refresh = run_parser(refresh_mapping, raw_path, project_root, manifest, args.verbose)
                status = 'PASS' if refresh['returncode'] == 0 else 'FAIL'
                results.append({'target': target, 'status': status, 'parser': refresh})
                if args.verbose:
                    print(f'[extract] {target}: availability refreshed ({status})', flush=True)
                continue
            if args.verbose:
                print(f'[extract] {target}: unchanged; skipped (use --force to rerun)', flush=True)
            results.append({'target': target, 'status': 'UNCHANGED'})
            continue
        try:
            mapping_list = mapping if isinstance(mapping, list) else [mapping]
            parser_results = [run_parser(item, raw_path, project_root, manifest, args.verbose) for item in mapping_list]
            result = {'parsers': parser_results, 'returncode': max((item['returncode'] for item in parser_results))}
            result.update({'target': target, 'status': 'PASS' if result['returncode'] == 0 else 'FAIL'})
        except OSError as exc:
            result = {'target': target, 'status': 'FAIL', 'error': str(exc)}
        results.append(result)
    log_root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    output = {'run_at': datetime.now(timezone.utc).isoformat(), 'results': results}
    (log_root / f'wgc-extract-{stamp}.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    if args.verbose:
        print(f"[extract] run log: {log_root / f'wgc-extract-{stamp}.json'}", flush=True)
    for result in results:
        print(f"{result['status']} {result['target']}")
    return int(any((result['status'] == 'FAIL' for result in results)))
if __name__ == '__main__':
    raise SystemExit(main())
