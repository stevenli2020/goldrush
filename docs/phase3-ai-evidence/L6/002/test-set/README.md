# Locked L6-002 pilot test set

The known-positive and known-negative cases were locked on 2026-08-29 before candidate or retrieval code was run against them. Positives identify official action documents; they do not assert a score or that every case is represented in the currently retained OFAC delta sample. That distinction is intentional: the pilot must disclose detection coverage limits rather than hide them.

The required random sample of 50 historical OFAC delta events cannot be honestly fabricated from the one currently retained delta. `build_random_sample.py` must be run once against the official OFAC archive before the first pilot run; it selects records deterministically and writes the locked `random_sample.json` with source references.
