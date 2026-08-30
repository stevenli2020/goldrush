# L5-006 — Official-Sector Gold Sales / Lending

Operational label retained for continuity. **Interpretation limitation:** this
variable is a net-reduction proxy, not a separately measured sales or lending
series. The source cannot distinguish outright sales, lending, swaps, reporting
adjustments, or other causes of a reduction.

The parser reads the shared WGC `official_changes` workbook `Monthly` sheet, retains canonical country rows (labels ending in `*`, including `Turkey*`, are excluded), and emits only negative signed changes as positive `official_sector_net_reduction_tonnes`. The adjusted canonical row is retained. Raw workbook and manifest provenance are preserved. Failed collection carries forward the latest valid row as `STALE`; without prior data it writes a machine-readable `BLOCKED` status artifact.
