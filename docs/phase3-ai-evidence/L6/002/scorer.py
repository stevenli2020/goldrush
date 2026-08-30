"""Deterministic Step 5 scorer for L6-002 retrieval evidence."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ACTION_RE = re.compile(r'\b(?:blocked|freeze|frozen)\b', re.I)
RELEVANCE_RE = re.compile(r'\b(?:central\s+bank|reserve\s+bank|monetary\s+authority|national\s+treasury|sovereign\s+wealth\s+fund)\b', re.I)
BROAD_SCOPE_RE = re.compile(r'\ball\s+property\s+and\s+interests\s+in\s+property\b', re.I)
LIMITED_SCOPE_RE = re.compile(r'\b(?:specified|specific|certain)\s+(?:property|assets?|accounts?|interests?\s+in\s+property)\b', re.I)
AUTHORITY_RE = re.compile(r'\b(?:UN\s+Security\s+Council\s+Resolution|United\s+Nations\s+Security\s+Council\s+Resolution|UNSCR)\b', re.I)


def _contexts(text: str, name: str, radius: int = 600) -> list[str]:
    lowered = text.casefold()
    needle = name.casefold()
    contexts = []
    start = lowered.find(needle)
    while start >= 0:
        contexts.append(text[max(0, start - radius):start + len(name) + radius])
        start = lowered.find(needle, start + len(needle))
    return contexts


def score_record(record: dict) -> dict:
    base = {
        'score': None,
        'score_breakdown': {'legal_action': 0, 'sovereign_relevance': 0, 'asset_scope': 0, 'legal_authority': 0},
        'evidentiary_gaps': [],
        'scoring_status': 'INSUFFICIENT_EVIDENCE',
        'action_state': None,
        'reversal_flag': False,
    }
    if str(record.get('action_type', '')).upper() == 'REMOVE':
        base.update({'action_state': 'REVERSED', 'scoring_status': 'REVERSED', 'reversal_flag': True})
        return base
    if record.get('retrieval_status') != 'FOUND' or not record.get('primary_document_text'):
        base['evidentiary_gaps'] = ['primary_document_missing']
        return base
    name = record.get('matched_official_name') or record.get('target_name')
    text = record.get('primary_document_text') or ''
    if not name or name.casefold() not in text.casefold():
        base['evidentiary_gaps'] = ['exact_name_not_found']
        return base

    contexts = _contexts(text, name)
    action = any(ACTION_RE.search(context) for context in contexts)
    relevance = any(RELEVANCE_RE.search(context) for context in contexts)
    if any(BROAD_SCOPE_RE.search(context) for context in contexts):
        scope = 20
    elif any(LIMITED_SCOPE_RE.search(context) and ACTION_RE.search(context) for context in contexts):
        scope = 10
    else:
        scope = 0
    authority = 10 if any(AUTHORITY_RE.search(context) for context in contexts) else 0
    base['score_breakdown'] = {
        'legal_action': 40 if action else 0,
        'sovereign_relevance': 30 if relevance else 0,
        'asset_scope': scope,
        'legal_authority': authority,
    }
    base['evidentiary_gaps'] = []
    if not action:
        base['evidentiary_gaps'].append('legal_action_not_explicit')
    if not relevance:
        base['evidentiary_gaps'].append('sovereign_relevance_not_explicit')
    if scope == 0:
        base['evidentiary_gaps'].append('asset_scope_not_explicit')
    if authority == 0:
        base['evidentiary_gaps'].append('legal_authority_not_explicit')
    base['score'] = sum(base['score_breakdown'].values())
    base['scoring_status'] = 'SCORABLE'
    base['action_state'] = 'ACTIVE'
    return base


def score_file(input_path: Path, output_path: Path) -> None:
    records = json.loads(input_path.read_text(encoding='utf-8'))
    scored = [{**record, **score_record(record)} for record in records]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(scored, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'Wrote {len(scored)} scored records to {output_path}')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    score_file(args.input, args.output)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
