# L3-002 — Forward Policy Rate Curve

**Status:** Complete — approved 2026-08-24.

Phase 2 uses the clarified name **Forward Policy Rate Curve**. The Phase 1
registry retains the obsolete OIS wording and is not modified here.

The parser consumes the normalized CME 30-Day Fed Funds futures settlements
already produced for L1-006/L3-001 and preserves every unexpired ZQ contract.
For each contract:

```text
implied_policy_rate_pct = 100 - settlement_price
```

It validates the selected Section 09 or Section 10 PDF against its manifest SHA-256 and
retains PDF, manifest, URL, publication date, and retrieval timestamp provenance.
Changed settlement values are revisions; a hash-only retrieval change is not.
On source failure, the latest valid curve is returned as `STALE`. Without prior
data, a machine-readable `BLOCKED` status is written. Successful recovery clears
that status. No dates or curve points are synthesized.

## Run after shared CME extraction

From the repository root in WSL, first run the shared extractor:

```bash
cd /mnt/d/Projects/GoldRush
source .venv/bin/activate
python docs/phase2-ingestion/collectors/cme/cme_extract.py --verbose
```

Then run L3-002 with the normalized CSV, manifest, and raw PDF for the section
selected by that extraction. For the current preserved Section 10 evidence:

```bash
python docs/phase2-ingestion/L3/002/parser.py \
  --input docs/phase2-ingestion/data/cme/processed/section10_normalized.csv \
  --manifest docs/phase2-ingestion/data/cme/manifests/section10-20260821T120040Z.json \
  --source-pdf docs/phase2-ingestion/L1/006/data/raw/section10-manual-20260820.pdf \
  --prior docs/phase2-ingestion/L3/002/data/processed/L3_002_curve.csv \
  --output docs/phase2-ingestion/L3/002/data/processed/L3_002_curve.csv
```

If Section 09 was selected, use its `section09_normalized.csv`, matching
`section09` manifest, and manifest-referenced raw PDF instead. Then run L3-003:

```bash
python docs/phase2-ingestion/L3/003/parser.py \
  --curve docs/phase2-ingestion/L3/002/data/processed/L3_002_curve.csv \
  --prior docs/phase2-ingestion/L3/003/data/processed/L3_003_observations.csv \
  --output docs/phase2-ingestion/L3/003/data/processed/L3_003_observations.csv
```
