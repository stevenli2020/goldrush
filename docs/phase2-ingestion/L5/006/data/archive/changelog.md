# L5-006 changelog

2026-08-24 — Reworked against `Changes_latest_as_of_Aug2026_IFS.xlsx`, Monthly sheet. Lending is not separately observable; scope is official-sector net reductions proxy. De-minimis tolerance `0.0001t` excludes floating-point noise; malformed cells fail and values over `10,000t` are `FLAG`.

Evidence: 2,724 rows, 2002-01-01–2026-06-01; complete-period fallback retains every valid country row. Raw source metadata ``; processed source metadata ``. Package plus shared WGC tests: 17 passed.

Grace review and final approval: approved 2026-08-24; Complete. The production interpretation remains official-sector net reduction proxy; lending is not separately observable.
