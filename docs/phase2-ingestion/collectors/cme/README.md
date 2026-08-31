# Shared CME collector

`cme_download.py` discovers and downloads bulletin Sections 09, 10, 62, and 02B using the protected local cookie jar. It validates HTTPS CME URLs and PDF responses, retries transient failures up to three times with a 30-second request timeout, preserves raw files, and writes source metadata manifests under `data/cme/`. Interest-rate Sections 09 and 10 are stored in `data/cme/raw/interest-rates/`; metals Sections 62 and 02B are stored in `data/cme/raw/metals/`.

Unchanged files are detected by comparing the downloaded PDF bytes with the prior preserved file. No file hash is calculated or stored. Missing required sections, invalid URLs, invalid PDF responses, and exhausted retries produce a non-zero exit; no synthetic source is substituted.

`cme_extract.py` is the orchestration layer. It attempts extraction against every preserved section, classifies a section as `INSPECTED_UNUSED` only after the required `30D FED FD FUT` marker is absent, selects the first matching section, and invokes the existing L1-006 parser. Raw sections are retained for provenance; the unused section is not silently deleted.

Run from WSL:

```bash
cd /mnt/d/Projects/GoldRush
source .venv/bin/activate
python docs/phase2-ingestion/collectors/cme/cme_download.py --verbose
python docs/phase2-ingestion/collectors/cme/cme_extract.py --verbose
```

Use `--force` only for deliberate reruns. Use `--observation-date YYYY-MM-DD` when the bulletin publication date must override the retrieval date. Cookies are local-only, may require manual refresh when CME expires the session, and must never be committed or printed.

Focused downloader tests:

```bash
pytest -q docs/phase2-ingestion/collectors/cme/tests/test_cme_download.py
```

Approval verification on 2026-08-29: compilation passed, all three focused tests passed, and a live cookie-authenticated run returned `PASS` for Sections 09, 10, 62, and 02B. The no-hash byte-comparison implementation was approved for the project.
