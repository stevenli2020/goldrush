# L1-007 Changelog

## 2026-08-21

- Added the 5Y5Y real-forward proxy parser.
- Locked formula version `5y5y-real-forward-compound-v1`.
- Documented constant-maturity TIPS approximation and non-interpolation rule.
- Live verification completed: 908 aligned observations, all PASS; latest aligned observation 2026-08-19 at 2.630768%.
- Historical pretest cache retained for regression context only. Its L1-007 column used the superseded `T5YIFR` nominal forward-inflation mapping and does not match this approved real-forward proxy; it was not used as a production source.
