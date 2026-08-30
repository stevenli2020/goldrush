"""Run the live L3-006 pipeline: collect, extract, then score."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'docs' / 'phase2-ingestion' / 'collectors' / 'fomc'))
sys.path.insert(0, str(ROOT / 'docs' / 'phase2-ingestion' / 'L3' / '006'))
from fomc_download import collect  # noqa: E402
from parser import parse_statement  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description='Run the live L3-006 collector and AI scorer')
    ap.add_argument('--start-date', type=date.fromisoformat, required=True)
    ap.add_argument('--end-date', type=date.fromisoformat, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--parallel', action='store_true')
    args = ap.parse_args()

    with TemporaryDirectory(prefix='goldrush-l3-006-') as temporary:
        work = Path(temporary)
        raw = work / 'raw'
        manifests = work / 'manifests'
        records = collect(args.start_date, args.end_date, raw_dir=raw, manifest_dir=manifests)
        statements = sorted(
            (r for r in records if r['document_type'] == 'statement_html'),
            key=lambda r: r['release_date'],
        )
        if not statements:
            raise RuntimeError('collector returned no statement HTML')
        current = statements[-1]
        matching_pdf = manifests / f"{current['release_date']}-statement_pdf-.json"
        current_manifest = manifests / f"{current['release_date']}-statement_html-.json"
        row = parse_statement(current_manifest, matching_pdf)[0]
        if not row['statement_text'].strip():
            raise RuntimeError('Phase 2 parser returned empty statement text')

        prior_text = None
        prior = [r for r in statements if r['release_date'] < current['release_date']]
        if prior:
            prior_html = manifests / f"{prior[-1]['release_date']}-statement_html-.json"
            prior_pdf = manifests / f"{prior[-1]['release_date']}-statement_pdf-.json"
            prior_row = parse_statement(prior_html, prior_pdf)[0]
            prior_text = work / 'previous.md'
            prior_text.write_text(prior_row['statement_text'] + '\n', encoding='utf-8')

        current_text = work / 'current.md'
        current_text.write_text(row['statement_text'] + '\n', encoding='utf-8')
        command = ['npm', 'run', 'ai:score', '--', '--statement', str(current_text), '--output', str(args.output)]
        if prior_text:
            command.extend(['--previous', str(prior_text)])
        if args.parallel:
            command.append('--parallel')
        subprocess.run(command, cwd=Path(__file__).parent, check=True)
        result = json.loads(args.output.read_text(encoding='utf-8'))
        if result.get('run_status') != 'completed':
            raise RuntimeError(f"AI scorer did not complete: {result.get('error')}")
        print(json.dumps({'release_date': current['release_date'], 'run_status': result['run_status'], 'final_score': result.get('final_score')}, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
