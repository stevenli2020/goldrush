"""Read-only official-document retrieval for selected L6-002 pilot events."""
from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

USER_AGENT = 'GoldRush/0.3 Phase-3 research (+https://ofac.treasury.gov/)'
RECENT_ACTIONS_URL = 'https://ofac.treasury.gov/recent-actions/sanctions-list-updates'
FEDERAL_REGISTER_API = 'https://www.federalregister.gov/api/v1/documents.json'


def robots_allowed(url, session, cache):
    parsed = urlparse(url)
    root = f'{parsed.scheme}://{parsed.netloc}'
    if root not in cache:
        robots_url = f'{root}/robots.txt'
        response = session.get(robots_url, headers={'User-Agent': USER_AGENT}, timeout=30)
        if response.status_code != 200:
            cache[root] = None
        else:
            parser = RobotFileParser()
            parser.parse(response.text.splitlines())
            cache[root] = parser
    parser = cache[root]
    return parser is None or parser.can_fetch(USER_AGENT, url)


def fetch(url, session, robots_cache):
    if not robots_allowed(url, session, robots_cache):
        return None, {'url': url, 'status': 'ROBOTS_DENIED'}
    response = session.get(url, headers={'User-Agent': USER_AGENT, 'Accept': 'text/html,application/pdf;q=0.9'}, timeout=60)
    attempt = {'url': url, 'status': response.status_code, 'content_type': response.headers.get('content-type', '')}
    if response.status_code != 200:
        return None, attempt
    return response, attempt


def recent_action_links(html, target_name):
    soup = BeautifulSoup(html, 'html.parser')
    needle = (target_name or '').casefold()
    if not needle:
        return []
    links = []
    for anchor in soup.find_all('a', href=True):
        context = ' '.join(anchor.parent.stripped_strings) if anchor.parent else anchor.get_text(' ', strip=True)
        if needle in context.casefold():
            links.append(urljoin(RECENT_ACTIONS_URL, anchor['href']))
    return list(dict.fromkeys(links))


def legal_authority_query(value):
    match = re.search(r'(?i)\b(?:e\.?o\.?|executive\s+order)\s*(\d+)\b', value or '')
    return f'E.O. {match.group(1)}' if match else (value or '')[:15].strip()


def is_matching_primary_document(text, target_name):
    if not text or not target_name:
        return False
    lowered = text.casefold()
    return target_name.casefold() in lowered and 'federal register :: request access' not in lowered


def federal_register_urls(event, session, robots_cache):
    authority = legal_authority_query(event.get('legal_authorities_raw'))
    if not authority:
        return [], []
    params = {'conditions[publication_date]': event['publication_date'], 'conditions[term]': authority, 'per_page': 20}
    if not robots_allowed(FEDERAL_REGISTER_API, session, robots_cache):
        return [], [{'url': FEDERAL_REGISTER_API, 'status': 'ROBOTS_DENIED', 'query': params}]
    response = session.get(FEDERAL_REGISTER_API, params=params, headers={'User-Agent': USER_AGENT, 'Accept': 'application/json'}, timeout=60)
    attempt = {'url': response.url, 'status': response.status_code, 'content_type': response.headers.get('content-type', ''), 'query': params}
    if response.status_code != 200:
        return [], [attempt]
    try:
        results = response.json().get('results', [])
    except ValueError:
        return [], [attempt | {'status': 'INVALID_JSON'}]
    urls = [result.get('html_url') or result.get('raw_text_url') for result in results]
    return [url for url in urls if url], [attempt]


def retrieve_event(event, session=None):
    client = session or requests.Session()
    robots_cache = {}
    attempts = []
    page, attempt = fetch(RECENT_ACTIONS_URL, client, robots_cache)
    attempts.append(attempt)
    urls = recent_action_links(page.text, event.get('target_name')) if page is not None else []
    if not urls:
        fallback_urls, fallback_attempts = federal_register_urls(event, client, robots_cache)
        attempts.extend(fallback_attempts)
        urls = fallback_urls
    for url in urls:
        response, attempt = fetch(url, client, robots_cache)
        attempts.append(attempt)
        if response is None:
            continue
        content_type = response.headers.get('content-type', '').lower()
        if 'text/html' in content_type:
            text = BeautifulSoup(response.text, 'html.parser').get_text('\n', strip=True)
            if is_matching_primary_document(text, event.get('target_name')):
                return evidence_record(event, 'FOUND', text, url, attempts)
        if 'application/pdf' in content_type:
            try:
                text = '\n'.join(page.extract_text() or '' for page in PdfReader(BytesIO(response.content)).pages).strip()
            except Exception:
                continue
            if is_matching_primary_document(text, event.get('target_name')):
                return evidence_record(event, 'FOUND', text, url, attempts)
    return evidence_record(event, 'NOT_FOUND', None, None, attempts)


def evidence_record(event, status, text, source_url, attempts):
    return {
        'variable_id': 'L6-002',
        'ofac_entity_id': event['ofac_entity_id'],
        'publication_date': event['publication_date'],
        'target_name': event.get('target_name'),
        'retrieval_status': status,
        'primary_document_url': source_url,
        'primary_document_text': text,
        'retrieval_attempts': attempts,
        'retrieved_at': datetime.now(timezone.utc).isoformat(),
    }


def selected_events(path, entity_ids):
    rows = list(csv.DictReader(path.open(newline='', encoding='utf-8')))
    wanted = set(entity_ids)
    return [row for row in rows if row['ofac_entity_id'] in wanted]


def main():
    root = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument('--phase2-csv', type=Path, required=True)
    ap.add_argument('--entity-id', action='append', required=True, help='Explicit event selection; this tool does not inspect is_candidate.')
    ap.add_argument('--output', type=Path, default=root / 'data/retrieval-pilot.json')
    args = ap.parse_args()
    records = [retrieve_event(event) for event in selected_events(args.phase2_csv, args.entity_id)]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
    print(f'Wrote {len(records)} evidence records to {args.output}')


if __name__ == '__main__':
    main()
