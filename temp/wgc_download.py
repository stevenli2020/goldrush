import json
import re
import urllib.parse
from curl_cffi import requests
COOKIE_FILE = 'cookies.json'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36'
TARGETS = [{'name': 'Above Ground Gold', 'url': 'https://www.gold.org/goldhub/data/how-much-gold', 'pattern': 'href=["\\\'](.*?/download/file/.*?above-ground-gold.*?\\.xlsx?)\\s*["\\\']'}, {'name': 'Gold ETF Holdings and Flows', 'url': 'https://www.gold.org/goldhub/data/gold-etfs-holdings-and-flows', 'pattern': 'href=["\\\'](.*?/download/file/.*?(?:etf.*?flow|flow.*?etf).*?\\.xlsx?)\\s*["\\\']'}, {'name': 'Gold Demand by Country (GDT)', 'url': 'https://www.gold.org/goldhub/data/gold-demand-by-country', 'pattern': 'href=["\\\'](.*?/download/file/.*?gdt.*?\\.xlsx?)\\s*["\\\']'}, {'name': 'World Official Gold Reserves', 'url': 'https://www.gold.org/goldhub/data/gold-reserves-by-country', 'pattern': 'href=["\\\'](.*?/download/file/.*?world.*?official.*?\\.xlsx?)\\s*["\\\']'}, {'name': 'Gold Reserves Changes', 'url': 'https://www.gold.org/goldhub/data/gold-reserves-by-country', 'pattern': 'href=["\\\'](.*?/download/file/.*?change.*?\\.xlsx?)\\s*["\\\']'}]

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
            cookie_map[name] = {'domain': '.gold.org', 'name': name, 'value': new_value, 'path': '/', 'secure': True, 'httpOnly': False}
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
    return filename or 'downloaded_file.xlsx'

def process_download(session, target, page_cache):
    """Handles parsing, link extraction, and downloading while using cached HTML when possible."""
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
            return False
        page_text = page_response.text
        page_cache[page_url] = page_text
    match = re.search(target['pattern'], page_text, re.IGNORECASE)
    if not match:
        print(f'❌ Could not find matching file link on the page.')
        return False
    file_path = match.group(1).strip()
    if file_path.startswith('/'):
        download_url = f'https://www.gold.org{file_path}'
    elif file_path.startswith('http'):
        download_url = file_path
    else:
        download_url = f'https://www.gold.org/{file_path}'
    print(f'[*] Found target download URL: {download_url}')
    headers['Referer'] = page_url
    print('[*] Downloading file...')
    download_response = session.get(download_url, headers=headers, impersonate='chrome')
    content_type = download_response.headers.get('Content-Type', '')
    if download_response.status_code == 200 and 'text/html' not in content_type:
        filename = get_filename_from_response(download_response, download_url)
        with open(filename, 'wb') as f:
            f.write(download_response.content)
        print(f"🎉 Success! File downloaded and saved as '{filename}'.")
        return True
    else:
        print(f'❌ Failed to download file. Status code: {download_response.status_code}')
        if 'text/html' in content_type:
            print('⚠️ Received HTML block instead of file. Session hard-expired or Cloudflare challenge triggered.')
        return False

def scrape_and_download():
    cookie_list = load_cookies(COOKIE_FILE)
    if not cookie_list:
        return
    session = requests.Session()
    for c in cookie_list:
        session.cookies.set(c['name'], c['value'], domain=c.get('domain', '.gold.org'))
    page_cache = {}
    results = {'success': [], 'failed': []}
    for target in TARGETS:
        success = process_download(session, target, page_cache)
        if success:
            results['success'].append(target['name'])
        else:
            results['failed'].append(target['name'])
        refreshed_cookies = session.cookies.get_dict()
        if refreshed_cookies:
            save_updated_cookies(COOKIE_FILE, refreshed_cookies)
    print('\n' + '=' * 50)
    print('📊 SCRIPT EXECUTION SUMMARY')
    print('=' * 50)
    print(f'Total Targets Evaluated: {len(TARGETS)}')
    print(f"✅ Successful Downloads: {len(results['success'])}")
    for name in results['success']:
        print(f'   - {name}')
    print(f"❌ Failed Downloads: {len(results['failed'])}")
    for name in results['failed']:
        print(f'   - {name}')
    print('=' * 50 + '\n')
if __name__ == '__main__':
    scrape_and_download()
