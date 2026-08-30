# L3-006 study

The runnable core is in [scripts/](scripts/README.md), including both AI prompts,
the scoring specification, TypeScript runner/calculator, tests, and dependencies.

```powershell
cd D:\Projects\GoldRush\docs\phase3-ai-evidence\L3\006\scripts
npm run ai:score -- --statement ../data/statements/statement4.md --previous ../data/statements/previous4.md --output ../data/results/manual-statement4.json --parallel
```

Omit `--parallel` for sequential jury calls. Existing output files are overwritten.
See [scripts/README.md](scripts/README.md) for setup, credentials, options, and outputs.

- `data/statements/`: current and prior statement inputs plus their manifest.
- `data/results/`: live and manual results.
- [study-history/](../../study-history): archived tests and analysis outside this folder.

The former manually entered Phase 2 `HAWKISH` annotation is superseded and is
not an input to the packaged scorer. The live path is now collector → existing
Phase 2 statement extraction → `scripts/fomc_parser.ts`; the completed live
verification is recorded in `results/live-l3-006-rerun.json`. More than 300
live/internal and external review tests were also completed during method
validation; those results remain supporting study evidence, not source data.

The private local API key is now in `scripts/api_key`; do not share it with the package.
