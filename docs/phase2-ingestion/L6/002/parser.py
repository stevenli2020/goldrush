"""Parse official namespaced OFAC published XML deltas."""
from __future__ import annotations
import argparse, csv, json, re
from datetime import datetime, timezone, date
from pathlib import Path
from xml.etree import ElementTree as ET
VARIABLE = 'L6-002'
VERSION = '0.3.0'
FIELDS = ['variable_id', 'event_date', 'publication_date', 'action_type', 'list_identifier', 'ofac_entity_id', 'target_name', 'target_type', 'program_tags', 'sanctions_type', 'legal_authorities_raw', 'is_candidate', 'matched_term', 'source_delta_path', 'source_url', 'manifest_path', 'retrieved_at', 'validation_status', 'availability_status', 'fallback_checked_at', 'parser_version']
CANDIDATE_RE = re.compile(r'(?i)\b(central\s+bank|reserve\s+bank|monetary\s+authority|national\s+treasury|sovereign\s+wealth)\b')
EXCLUSION_RE = re.compile(r'(?i)\b(commercial|plc|ltd|incorp(?:orated)?|private\s+bank)\b')

def metadata(p):
    return None

def local(tag):
    return tag.rsplit('}', 1)[-1]

def child_text(node, name):
    for x in node.iter():
        if local(x.tag) == name and x.text and x.text.strip():
            return x.text.strip()
    return ''

def child_texts(node, name):
    return [x.text.strip() for x in node.iter() if local(x.tag) == name and x.text and x.text.strip()]

def candidate_metadata(target_name):
    if not target_name or EXCLUSION_RE.search(target_name):
        return False, None
    match = CANDIDATE_RE.search(target_name)
    return bool(match), match.group(1) if match else None

def manifest(mp, rp):
    m = json.loads(mp.read_text(encoding='utf-8'))
    for k in ('source_url', 'retrieved_at', 'publication_date'):
        if not m.get(k):
            raise ValueError('manifest missing ' + k)
    datetime.fromisoformat(m['retrieved_at'].replace('Z', '+00:00'))
    date.fromisoformat(m['publication_date'])
    return m

def parse_xml(path, publication):
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise ValueError('invalid OFAC XML') from exc
    pub = child_text(root, 'datePublished') or publication
    try:
        event_date = datetime.fromisoformat(pub.replace('Z', '+00:00')).date().isoformat()
    except ValueError as exc:
        raise ValueError('invalid OFAC publication date') from exc
    out = []
    for e in [x for x in root.iter() if local(x.tag) == 'entity']:
        ident = e.attrib.get('id', '').strip()
        if not ident:
            raise ValueError('OFAC entity missing id')
        top = e.attrib.get('action', '').lower()
        actions = [x.attrib.get('action', '').lower() for x in e.iter() if x is not e and x.attrib.get('action')]
        action = {'add': 'ADD', 'remove': 'REMOVE', 'delete': 'REMOVE', 'update': 'UPDATE'}.get(top)
        if action is None:
            if any((a in {'add', 'remove', 'delete', 'update'} for a in actions)):
                action = 'UPDATE'
            else:
                raise ValueError(f'OFAC entity {ident} has no supported action')
        name = child_text(e, 'formattedFullName') or child_text(e, 'formattedLastName') or None
        typ = child_text(e, 'entityType') or 'Entity'
        programs = child_texts(e, 'sanctionsProgram')
        sanctions_types = child_texts(e, 'sanctionsType')
        legal_authorities = child_texts(e, 'legalAuthority')
        is_candidate, matched_term = candidate_metadata(name)
        out.append({'event_date': event_date, 'action_type': action, 'list_identifier': ident, 'ofac_entity_id': ident, 'target_name': name, 'target_type': typ, 'program_tags': ';'.join(dict.fromkeys(programs)), 'sanctions_type': ';'.join(dict.fromkeys(sanctions_types)), 'legal_authorities_raw': ';'.join(dict.fromkeys(legal_authorities)), 'is_candidate': is_candidate, 'matched_term': matched_term})
    return out

def parse(raw, mp, as_of=None):
    m = manifest(mp, raw)
    base = parse_xml(raw, m['publication_date'])
    seen = {}
    for r in base:
        key = (r['event_date'], r['action_type'], r['list_identifier'])
        if key in seen and seen[key] != r:
            raise ValueError('conflicting duplicate OFAC identity')
        seen[key] = r
    rh = None
    mh = None
    out = []
    for r in sorted(seen.values(), key=lambda x: (x['event_date'], x['list_identifier'])):
        out.append({'variable_id': VARIABLE, **r, 'publication_date': m['publication_date'], 'source_delta_path': str(raw), 'source_url': m['source_url'], 'manifest_path': str(mp), 'retrieved_at': m['retrieved_at'], 'validation_status': 'PASS', 'availability_status': 'AVAILABLE', 'fallback_checked_at': None, 'parser_version': VERSION})
    return out

def carry(prior, checked=None):
    if not prior or not prior.exists():
        raise FileNotFoundError('no prior L6-002 output exists')
    rows = list(csv.DictReader(prior.open(newline='', encoding='utf-8')))
    if not rows:
        raise ValueError('prior has no actions')
    for r in rows:
        pass
    for r in rows:
        r['availability_status'] = 'STALE'
        r['fallback_checked_at'] = checked or datetime.now(timezone.utc).isoformat()
        r['parser_version'] = VERSION
    return rows

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
    ap.add_argument('--output', type=Path, default=root / 'data/processed/l6_002.csv')
    a = ap.parse_args()
    try:
        if not a.raw or not a.manifest:
            raise ValueError('raw and manifest required')
        rows = parse(a.raw, a.manifest)
    except (OSError, ValueError, KeyError) as e:
        try:
            rows = carry(a.prior)
        except Exception as f:
            p = blocked(a.output, f'{e}; {f}')
            print(json.dumps({'status': 'BLOCKED', 'status_path': str(p)}))
            return 0
    write(rows, a.output)
    print(f'Wrote {len(rows)} rows to {a.output}')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
