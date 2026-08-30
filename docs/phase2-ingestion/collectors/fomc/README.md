# Shared FOMC publication downloader

**Status:** Complete for the approved L3-005 and L3-006 scope as of 2026-08-24.

`fomc_download.py` preserves the official FOMC calendar and only the statement
and Summary of Economic Projections HTML/PDF documents needed by L3-005 and
L3-006. It uses ordinary HTTPS requests with a descriptive user agent and no
cookies or credentials.

Document discovery follows each visible `fomc-meeting` block: it uses the
`Statement` and `Projection Materials` labels, then captures links labeled
`PDF` and `HTML`. URL-pattern classification remains as a fallback for older
or irregular historical pages, so current discovery does not depend on hidden
filenames.

```bash
python fomc_download.py --start-date 2026-06-01 --end-date 2026-08-24
```

Raw documents are stored unchanged under `docs/phase2-ingestion/data/fomc/raw/`.
Manifests under `data/fomc/manifests/` record URL, type, release/meeting date,
retrieval time, content type, byte size, raw path, and source metadata. An unchanged
document reuses the source metadata-named raw file. The bounded date range limits downloads.

Federal Reserve HTML responses can contain request-specific Cloudflare email
protection and challenge tokens. Those bytes are part of the raw response, so a
new source metadata-named snapshot is retained when they change even if the statement or SEP
article is unchanged. Stable PDFs are skipped when their source metadata already exists.

If discovery changes, download the official file manually and use
`preserve_manual()` with its original Federal Reserve URL, document type, and
release date. Manual files receive the same validation and manifest format.
