# Shared WGC downloader

`wgc_download.py` is the transport layer for World Gold Council workbooks used
by GoldRush. It locates the current workbook link, downloads the raw bytes,
validates that the response is an XLSX file, calculates source metadata, and writes a
manifest and run log.

It does not parse workbook rows or apply variable-specific rules. Those remain
in the existing parsers for L0-001, L0-003, L0-005, L0-006, L5-001, and L8-001.

## Layout

```text
collectors/wgc/
├── wgc_download.py
├── wgc_extract.py
├── config.yaml
├── README.md
├── CHANGELOG.md
└── tests/test_wgc_download.py

data/wgc/
├── raw/{above-ground,central-bank,etf,gdt,premiums}/
├── manifests/
├── logs/
└── cookies/                 # local only; never commit
```

## Run

```bash
cd /mnt/d/Projects/GoldRush
source .venv/bin/activate
cd docs/phase2-ingestion/collectors/wgc
python wgc_download.py
```

Run tests with `PYTHONPATH=. pytest -q tests/test_wgc_download.py tests/test_wgc_extract.py`.
The L9-001 package tests additionally verify the `gold_premiums` target and
manifest pass-through.

## Extract/dispatch

`wgc_extract.py` reads the latest downloader manifests and runs only parsers
listed explicitly under `extractors` in `config.yaml`. It skips unchanged
workbooks unless `--force` is supplied, records parser output and status in a
run log, and reports targets without a verified mapping as `SKIPPED`.

```bash
python wgc_extract.py
python wgc_extract.py --force
```

Parser mappings are intentionally added one at a time because the existing
variable parsers have different command-line interfaces.

The `gold_premiums` target downloads `gold-premiums.xlsx` to
`data/wgc/raw/premiums/` and dispatches it to the L9-001 parser with its
manifest and existing processed output as the parser prior. On unchanged
`gold_premiums` manifests, the extractor refreshes L9 availability status so an
old latest row can become `STALE`. Manual authenticated download plus
`create_manifest.py` remains the fallback if the shared cookie session is
unavailable.

Each successful target produces a raw workbook, a JSON manifest containing the
source URL, timestamp, size, and source metadata, and a run summary under
`data/wgc/logs/`. If the source metadata matches the latest manifest, the raw file is not
rewritten and `changed` is `false`.

The optional cookie jar is `data/wgc/cookies/cookies.json`. Manual workbook
placement remains the fallback if WGC access changes. Never print, commit, or
share cookie contents.

Update `config.yaml` when WGC page URLs or link patterns change. Do not add
variable-specific extraction logic here; `wgc_extract.py` will later dispatch
files to the existing parsers.
