# L9-004 changelog

2026-08-24 — Reworked against GDT Q2'26 workbook. Canonical India rows and separate import/demand components preserved. Quarter dates use documented quarter-end dates; annual labels normalize to `YYYY` and carry `observation_period_type=annual`; malformed cells fail and values over `10,000t` are `FLAG`.

Evidence: 308 rows, 2010–2026-06-30; identity `(component, observation_period_type, observation_period)` has zero duplicates. Latest Q2'26 jewellery 75.09821782t, bar-and-coin 50.25048632t, gross imports 98.392694375t, net imports 98.059694375t. Raw source metadata ``; processed source metadata ``. Package plus shared WGC tests: 17 passed.

Grace review and final approval: approved 2026-08-24; Complete. Annual and quarterly records remain separate through `observation_period_type`; WGC/Metals Focus import estimates are documented as the source limitation.
