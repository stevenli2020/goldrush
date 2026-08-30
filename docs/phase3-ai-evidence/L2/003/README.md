# L2-003 — USD/CNY

Phase 3 uses the FRED `DEXCHUS` H.10 series, the Chinese yuan renminbi per one
US dollar noon buying rate. The canonical value is in CNY per USD. Missing
observations are skipped, stale status is preserved explicitly, and no
synthetic daily observation is created.
