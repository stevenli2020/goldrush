# L0-009 — Gold Lease Rates / Forward Rates

The first implementation is a small, transparent proxy for physical-gold
financing conditions. It uses CME Section 62 gold futures settlements and the
FRED `SOFR90DAYAVG` (90-day average SOFR) funding proxy:

`annualized futures forward rate - SOFR90DAYAVG`

The parser consumes normalized CSV files. PDF extraction remains a separate
input-preparation step so the variable parser stays simple. The Section 62
adapter requires Poppler's `pdftotext` command and uses layout-preserved text
to select the CME settlement column.

Run:

```bash
python parser.py --cme data/raw/cme_gc_settlement.csv \
  --sofr data/raw/sofr3m.csv \
  --output data/processed/L0_009_observations.csv
```

The shared CME collector preserves Section 62 and its source metadata manifest. SOFR3M
is preserved separately. The parser joins the completed inputs by observation date
and emits the most recent common date; it does not pair different dates. If no
overlap exists, carry forward the last valid observation with `STALE` for up to
five trading days, or record `BLOCKED` when no prior is available; do not
substitute a policy rate. This proxy is intentionally distinct from L1-006
policy expectations and L10-002 open interest.
