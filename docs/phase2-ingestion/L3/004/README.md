# L3-004 — Probability Distribution of Future Policy Outcomes

**Status:** Complete — approved 2026-08-24.

L3-004 is a calculated probability proxy for the next two scheduled FOMC
meetings. It is not official CME FedWatch output. The source/method label is
`Calculated CME-method policy outcome probability`.

## Method and scope

The collector preserves official CME 30-Day Federal Funds futures JSON, FRED
EFFR and target-range responses, and a `cme-fedwatch==0.1.3` FOMC schedule
snapshot. The parser uses the latest inputs available on or before the actual
CME settlement date, counts the decision date as pre-decision, applies exact
calendar-day weighting, and uses the following non-meeting-month contract when
a meeting leaves three or fewer post-decision calendar days.

Each expected transition becomes adjacent 25-basis-point outcomes. Conditional
transitions are convolved into cumulative unconditional distributions. Only the
next two meetings are emitted; the third meeting is recursive validation
evidence. No calibration factor or material force-normalization is used.

## Validation

The tree passed all nine official comparisons: three meeting dates for each
common observation date from 2026-08-19 through 2026-08-21. All modes agreed,
no material official bucket was omitted, and all sums were within 0.001. The
worst maximum bucket error and TVD were both 0.0178568571, below 0.10.

Evidence is preserved in
`data/validation/cumulative_tree_comparison_2026-08-19_to_2026-08-21.json`,
the unchanged official CSVs, and `data/raw/` plus `data/manifests/`.

## Output and behavior

The canonical CSV contains one row per observation date, meeting date, and
target range. It keeps the CME settlement date separate from retrieval time and
preserves detailed source paths, source metadata, EFFR date/value, versions,
validation, availability, and revision state.

Revision detection compares canonical probabilities. source metadata-only changes are not
revisions. Failure returns the latest complete prior distribution as `STALE`;
without prior data it writes `BLOCKED`. Successful recovery removes that
artifact. An expiring schedule produces `FLAG`; an expired schedule produces
`BLOCKED`.

## Run

From the repository root in WSL:

```bash
source .venv/bin/activate
python docs/phase2-ingestion/L3/004/collector.py
python docs/phase2-ingestion/L3/004/parser.py \
  --manifest docs/phase2-ingestion/L3/004/data/manifests/<latest-manifest>.json \
  --prior docs/phase2-ingestion/L3/004/data/processed/L3_004_probabilities.csv \
  --output docs/phase2-ingestion/L3/004/data/processed/L3_004_probabilities.csv
```

Preserved validation:

```bash
python docs/phase2-ingestion/L3/004/validate_alternative1.py \
  --official-dir docs/phase2-ingestion/L3/004/data/validation/official \
  --manifest docs/phase2-ingestion/L3/004/data/manifests/L3-004-2026-08-19-20260824T025547Z.json \
  --manifest docs/phase2-ingestion/L3/004/data/manifests/L3-004-2026-08-20-20260824T025550Z.json \
  --manifest docs/phase2-ingestion/L3/004/data/manifests/L3-004-2026-08-21-20260824T025554Z.json \
  --report docs/phase2-ingestion/L3/004/data/validation/cumulative_tree_comparison_2026-08-19_to_2026-08-21.json
```

Limitations: the finite package schedule must be refreshed before expiry.
Futures-derived probabilities are methodology- and liquidity-sensitive, and
production scope is deliberately limited to the next two meetings.
