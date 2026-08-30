# L2-001 — DXY US Dollar Index

Phase 3 uses the live Yahoo Finance `DX-Y.NYB` OHLC snapshot retrieved through
OpenBB/yfinance. The canonical value is `dxy_close`, in index units. Missing
close data causes the parser to use the documented prior-valid observation as
`STALE`; no current value is invented or interpolated.
