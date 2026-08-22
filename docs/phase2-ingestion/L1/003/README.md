# L1-003 — Forward Real Rates

This package preserves and parses the Federal Reserve Board Gürkaynak-Sack-Wright
(GS&W) zero-coupon TIPS curve CSV. The source is a staff research product and
may be delayed, revised, or changed methodologically without advance notice.

The CSV contains daily estimates but is generally refreshed approximately weekly.
`download.py` preserves the raw CSV and writes a SHA-256 manifest. `parser.py`
requires all six inputs and calculates five component forwards:

```text
2Y1Y   = 3 × y(3) − 2 × y(2)
3Y2Y   = [5 × y(5) − 3 × y(3)] / 2
5Y2Y   = [7 × y(7) − 5 × y(5)] / 2
7Y3Y   = [10 × y(10) − 7 × y(7)] / 3
10Y10Y = 2 × y(20) − y(10)
L1-003 = mean(all five components)
```

The source yields are continuously compounded percent per annum; outputs use the
same unit. Missing inputs are not interpolated and produce no record. The latest
aligned observation becomes `STALE` after seven days without a refreshed source.

## Run

```bash
python download.py --output-dir data/raw
python parser.py --raw data/raw/feds200805-<timestamp>.csv \
  --source-retrieved-at <download-timestamp> \
  --output data/processed/L1_003_observations.csv
```
