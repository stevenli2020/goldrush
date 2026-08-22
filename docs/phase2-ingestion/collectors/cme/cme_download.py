"""Download both CME interest-rate bulletin sections and preserve raw PDFs."""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path
from curl_cffi import requests

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "cme"
RAW = DATA / "raw" / "interest-rates"
MANIFESTS = DATA / "manifests"
LOGS = DATA / "logs"
COOKIES = DATA / "cookies" / "cookies.json"
PAGE_URL = "https://www.cmegroup.com/market-data/daily-bulletin.html"
TARGETS = {
    "section09": "Section09_Interest_Rate_Futures.pdf",
    "section10": "Section10_Interest_Rate_Futures_Continued.pdf",
    "section62": "Section62_Metals_Futures_Products.pdf",
    "section02b": "Section02B_Summary_Volume_And_Open_Interest_Metals_Futures_And_Options.pdf",
}
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/151.0 Safari/537.36"

def load_cookies(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []

def save_cookies(path: Path, session) -> None:
    rotated = session.cookies.get_dict()
    if not rotated: return
    existing = load_cookies(path)
    by_name = {item.get("name"): item for item in existing if item.get("name")}
    for name, value in rotated.items():
        item = by_name.setdefault(name, {"domain": ".cmegroup.com", "path": "/", "secure": True, "name": name})
        item["value"] = value
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(list(by_name.values()), indent=2) + "\n", encoding="utf-8")

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def discover(session, verbose=False) -> dict[str, str]:
    response = session.get(PAGE_URL, headers={"User-Agent": UA}, impersonate="chrome")
    response.raise_for_status()
    found = {}
    for section, filename in TARGETS.items():
        match = re.search(r"/daily_bulletin/current/" + re.escape(filename), response.text, re.I)
        if match: found[section] = "https://www.cmegroup.com" + match.group(0)
        elif verbose: print(f"[debug] {filename}: link not found")
    return found

def download_one(session, section: str, url: str, force: bool, verbose: bool) -> dict:
    response = session.get(url, headers={"User-Agent": UA, "Accept": "application/pdf,*/*", "Referer": PAGE_URL}, impersonate="chrome")
    content, content_type = response.content, response.headers.get("Content-Type", "")
    if response.status_code != 200: raise RuntimeError(f"{section}: HTTP {response.status_code}")
    if not content.startswith(b"%PDF") or "html" in content_type.lower(): raise ValueError(f"{section}: response is not a PDF (content-type={content_type or 'unknown'})")
    digest, retrieved = sha256(content), datetime.now(timezone.utc)
    previous = sorted(MANIFESTS.glob(f"{section}-*.json"))
    prior = json.loads(previous[-1].read_text(encoding="utf-8")) if previous else None
    changed = force or not prior or prior.get("sha256") != digest
    if changed:
        RAW.mkdir(parents=True, exist_ok=True)
        raw_path = RAW / f"{section}-{retrieved.strftime('%Y%m%dT%H%M%SZ')}.pdf"
        raw_path.write_bytes(content)
    else: raw_path = Path(prior["raw_path"])
    record = {"target": section, "source_url": url, "raw_path": str(raw_path), "sha256": digest, "size_bytes": len(content), "retrieved_at": retrieved.isoformat(), "http_status": response.status_code, "content_type": content_type, "changed": changed, "forced": force}
    MANIFESTS.mkdir(parents=True, exist_ok=True)
    (MANIFESTS / f"{section}-{retrieved.strftime('%Y%m%dT%H%M%SZ')}.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    if verbose: print(f"[debug] {section}: changed={changed} sha256={digest}")
    return record

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Download CME Sections 09 and 10")
    parser.add_argument("--cookies", type=Path, default=COOKIES); parser.add_argument("--force", action="store_true"); parser.add_argument("--verbose", "--debug", action="store_true")
    args = parser.parse_args(argv); session = requests.Session()
    for cookie in load_cookies(args.cookies):
        if cookie.get("name") and cookie.get("value"): session.cookies.set(cookie["name"], cookie["value"], domain=cookie.get("domain", ".cmegroup.com"))
    try:
        links, results = discover(session, args.verbose), []
        for section in TARGETS:
            if section not in links: results.append({"target": section, "status": "NOT_FOUND"}); continue
            try: results.append({"target": section, "status": "PASS", **download_one(session, section, links[section], args.force, args.verbose)})
            except Exception as exc: results.append({"target": section, "status": "FAIL", "error": str(exc)})
        save_cookies(args.cookies, session)
        LOGS.mkdir(parents=True, exist_ok=True); stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        (LOGS / f"cme-download-{stamp}.json").write_text(json.dumps({"run_at": datetime.now(timezone.utc).isoformat(), "results": results}, indent=2) + "\n", encoding="utf-8")
        for result in results: print(f"{result['status']} {result['target']}")
        return int(any(result["status"] == "FAIL" for result in results))
    except Exception as exc:
        print(f"FAIL collector: {exc}", file=sys.stderr); return 1

if __name__ == "__main__": raise SystemExit(main())
