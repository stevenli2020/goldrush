import argparse
import json
import re
import urllib.parse
from curl_cffi import requests
COOKIE_FILE = 'cookies.json'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36'
TARGETS = [{'name': 'CME Daily Bulletin - Interest Rate Futures', 'url': 'https://www.cmegroup.com/market-data/daily-bulletin.html', 'section_patterns': ['href=["\\\'](/daily_bulletin/current/[^"\\\'/]*?(?<!\\d)09_[^"\\\']*?\\.pdf)\\s*["\\\']', 'href=["\\\'](/daily_bulletin/current/[^"\\\'/]*?(?<!\\d)10_[^"\\\']*?\\.pdf)\\s*["\\\']'], 'keywords': ['interest', 'rate', 'futures']}, {'name': 'CME Daily Bulletin - Metals Futures Products', 'url': 'https://www.cmegroup.com/market-data/daily-bulletin.html', 'section_patterns': ['href=["\\\'](/daily_bulletin/current/[^"\\\'/]*?(?<!\\d)62_[^"\\\']*?\\.pdf)\\s*["\\\']'], 'keywords': ['metal', 'future']}, {'name': 'CME Daily Bulletin - Summary Volume And Open Interest, Metals Futures And Options', 'url': 'https://www.cmegroup.com/market-data/daily-bulletin.html', 'section_patterns': ['href=["\\\'](/daily_bulletin/current/[^"\\\'/]*?(?<!\\d)02B_[^"\\\']*?\\.pdf)\\s*["\\\']'], 'keywords': ['volume', 'interest', 'future', 'option']}]

def load_cookies(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ '{filepath}' not found.")
        return None

def save_updated_cookies(filepath, session_cookies_dict):
    """Reads current cookies from disk, merges rotated tokens, and saves back."""
    try:
        with open(filepath, 'r') as f:
            cookie_list = json.load(f)
    except FileNotFoundError:
        cookie_list = []
    cookie_map = {c['name']: c for c in cookie_list}
    for name, new_value in session_cookies_dict.items():
        if name in cookie_map:
            cookie_map[name]['value'] = new_value
        else:
            cookie_map[name] = {'domain': '.cmegroup.com', 'name': name, 'value': new_value, 'path': '/', 'secure': True, 'httpOnly': False}
    with open(filepath, 'w') as f:
        json.dump(list(cookie_map.values()), f, indent=4)
    print("🔄 Session refreshed: Saved rotated tokens to 'cookies.json'.")

def get_filename_from_response(download_response, download_url):
    """Extracts the original filename from response headers or the URL path."""
    filename = None
    content_disposition = download_response.headers.get('Content-Disposition', '')
    if 'filename=' in content_disposition:
        match = re.search('filename=["\\\']?(.*?)["\\\']?(?:;|$)', content_disposition)
        if match:
            filename = match.group(1)
    if not filename:
        raw_name = download_url.split('/')[-1].split('?')[0]
        filename = urllib.parse.unquote(raw_name)
    return filename or 'downloaded_file.pdf'

def download_file(session, download_url, page_url, dry_run=False):
    """Downloads (or, in dry-run mode, verifies) a single file. Returns True/False."""
    headers = {'User-Agent': USER_AGENT, 'Accept': 'application/pdf,*/*;q=0.8', 'Referer': page_url}
    print(f'[*] Found target download URL: {download_url}')
    if dry_run:
        print('[DRY RUN] Verifying link without saving file...')
    else:
        print('[*] Downloading file...')
    download_response = session.get(download_url, headers=headers, impersonate='chrome')
    content_type = download_response.headers.get('Content-Type', '')
    size_bytes = len(download_response.content)
    if download_response.status_code == 200 and 'text/html' not in content_type:
        filename = get_filename_from_response(download_response, download_url)
        if dry_run:
            print(f"✅ [DRY RUN] Link OK — would save as '{filename}' ({size_bytes:,} bytes, {content_type or 'unknown type'}).")
        else:
            with open(filename, 'wb') as f:
                f.write(download_response.content)
            print(f"🎉 Success! File downloaded and saved as '{filename}'.")
        return True
    else:
        print(f'❌ Failed to download file. Status code: {download_response.status_code}')
        if 'text/html' in content_type:
            print('⚠️ Received HTML block instead of file. Session hard-expired or Cloudflare challenge triggered.')
        return False

def find_section_matches(page_text, section_patterns, keywords):
    """
    Finds files by anchoring on the number patterns, then cross-checks each
    match against the keyword tripwire.
    Returns (unique_matches, warnings).
    """
    all_matches = []
    for pattern in section_patterns:
        all_matches.extend(re.findall(pattern, page_text, re.IGNORECASE))
    seen = set()
    unique_matches = []
    for m in all_matches:
        if m not in seen:
            seen.add(m)
            unique_matches.append(m)
    warnings = []
    for file_path in unique_matches:
        lower_path = file_path.lower()
        missing = [kw for kw in keywords if kw.lower() not in lower_path]
        if missing:
            warnings.append(f"⚠️ WARNING: '{file_path}' matched by number anchor but is missing expected keyword(s) {missing}. CME may have renumbered/restructured the bulletin — please verify this is still the correct file.")
    return (unique_matches, warnings)

def process_target(session, target, page_cache, dry_run=False):
    """Handles parsing, link extraction (possibly multiple files), and downloading."""
    page_url = target['url']
    headers = {'User-Agent': USER_AGENT, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    if page_url in page_cache:
        print(f"\n[*] [{target['name']}] Using cached HTML for page: {page_url}")
        page_text = page_cache[page_url]
    else:
        print(f"\n[*] [{target['name']}] Accessing page: {page_url}")
        page_response = session.get(page_url, headers=headers, impersonate='chrome')
        if page_response.status_code != 200:
            print(f'❌ Failed to load page. Status code: {page_response.status_code}')
            return []
        page_text = page_response.text
        page_cache[page_url] = page_text
    unique_matches, warnings = find_section_matches(page_text, target['section_patterns'], target['keywords'])
    if not unique_matches:
        print('❌ Could not find matching file link(s) on the page.')
        return []
    print(f'[*] Found {len(unique_matches)} matching file(s) on page.')
    for w in warnings:
        print(w)
    results = []
    for file_path in unique_matches:
        file_path = file_path.strip()
        if file_path.startswith('/'):
            download_url = f'https://www.cmegroup.com{file_path}'
        elif file_path.startswith('http'):
            download_url = file_path
        else:
            download_url = f'https://www.cmegroup.com/{file_path}'
        success = download_file(session, download_url, page_url, dry_run=dry_run)
        results.append((download_url, success))
    return results

def scrape_and_download(dry_run=False):
    cookie_list = load_cookies(COOKIE_FILE)
    if not cookie_list:
        return
    session = requests.Session()
    for c in cookie_list:
        session.cookies.set(c['name'], c['value'], domain=c.get('domain', '.cmegroup.com'))
    page_cache = {}
    results = {'success': [], 'failed': []}
    if dry_run:
        print('=' * 50)
        print('🧪 DRY RUN MODE — no files will be written to disk')
        print('=' * 50)
    for target in TARGETS:
        target_results = process_target(session, target, page_cache, dry_run=dry_run)
        if not target_results:
            results['failed'].append(f"{target['name']} (no files found)")
        else:
            for download_url, success in target_results:
                label = f"{target['name']}: {download_url.split('/')[-1]}"
                if success:
                    results['success'].append(label)
                else:
                    results['failed'].append(label)
        refreshed_cookies = session.cookies.get_dict()
        if refreshed_cookies:
            save_updated_cookies(COOKIE_FILE, refreshed_cookies)
    print('\n' + '=' * 50)
    if dry_run:
        print('📊 DRY RUN SUMMARY (no files saved)')
    else:
        print('📊 SCRIPT EXECUTION SUMMARY')
    print('=' * 50)
    print(f"Total Files Found: {len(results['success']) + len(results['failed'])}")
    verb = 'Verified' if dry_run else 'Successful Downloads'
    print(f"✅ {verb}: {len(results['success'])}")
    for name in results['success']:
        print(f'   - {name}')
    print(f"❌ Failed: {len(results['failed'])}")
    for name in results['failed']:
        print(f'   - {name}')
    print('=' * 50 + '\n')
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download CME Daily Bulletin PDFs.')
    parser.add_argument('--dry-run', action='store_true', help='Fetch the page and verify matching download links (status code, content-type, size) without writing any files to disk.')
    args = parser.parse_args()
    scrape_and_download(dry_run=args.dry_run)
