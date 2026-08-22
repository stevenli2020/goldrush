# Shared CME collector

`cme_download.py` downloads both Interest Rate bulletin sections 09 and 10 using the local cookie jar, validates the PDF signature, preserves raw files, and writes SHA-256 manifests under `data/cme/`.

`cme_extract.py` is the orchestration layer. It attempts extraction against every preserved section, classifies a section as `INSPECTED_UNUSED` only after the required `30D FED FD FUT` marker is absent, selects the first matching section, and invokes the existing L1-006 parser. Raw sections are retained for provenance; the unused section is not silently deleted.

Run from WSL:

```bash
cd /mnt/d/Projects/GoldRush
source .venv/bin/activate
python docs/phase2-ingestion/collectors/cme/cme_download.py --verbose
python docs/phase2-ingestion/collectors/cme/cme_extract.py --verbose
```

Use `--force` only for deliberate reruns. Use `--observation-date YYYY-MM-DD` when the bulletin publication date must override the retrieval date. Cookies are local-only and must never be committed.
