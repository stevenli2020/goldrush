# L3-006 core scoring scripts

This folder contains the runnable TypeScript package, two prompts, scoring rules,
tests, package manifest/lockfile, and installed dependencies. Inputs and results
are outside the package in `../data/statements` and `../data/results`. The local `api_key`
was moved here with the package; it is private and must not be committed or shared.

## Requirements and setup

- Node.js 20 or newer and npm. Verified locally with Node 24.18.0 and npm 11.16.0.
- Internet access and a Gemini API key with access/quota for the configured model.
- UTF-8 current/prior FOMC statement files; Markdown/plain text is accepted. This
  package does not download statements or extract HTML/PDF.
- Installed `node_modules` is included for this Windows environment. On a fresh
  machine or another platform, run `npm ci` inside this folder to install the exact
  locked dependencies, including development dependencies used by the TS runner.
- Credentials: use the `GEMINI_API_KEY` environment variable, or a plain-text
  `api_key` file beside `fomc_parser.ts`. The environment variable takes priority.
  Do not include your real key when distributing this folder.

All user-supplied input/output paths resolve from the current working directory.
Prompts and the local key resolve relative to the runner, not the working directory.

The current rules are in [CONSOLIDATED-SCORING-SPEC.md](CONSOLIDATED-SCORING-SPEC.md).

For a live end-to-end run, use `run_live_l3_006.py` from this directory. It
calls the shared official FOMC collector, uses the existing Phase 2 parser to
extract the latest current/prior statement text, and passes only that text to
`fomc_parser.ts`:

```powershell
python run_live_l3_006.py --start-date 2026-01-01 --end-date 2026-12-31 --output ../data/results/live-l3-006.json
```

The bridge uses a temporary workspace for downloaded/extracted inputs and
fails if collection, extraction, input validation, or scoring fails.
One command makes **four sequential API calls**: one persona-neutral extraction,
then one independent assessment for each of the three jury personas. Add `--parallel`
to run the three jury calls concurrently after baseline completion; sequential is
the default. Parallel mode still makes four calls and may encounter API rate limits.
There is no
batch repetition or automatic retry.

## Run from PowerShell

```powershell
cd D:\Projects\GoldRush\docs\phase3-ai-evidence\L3\006\scripts
npm run ai:score -- --statement ../data/statements/statement4.md --previous ../data/statements/previous4.md --output ../data/results/manual-statement4.json
```

No `--persona` argument: all three personas run automatically. Replace `4` in
both input paths to select another paired statement. Existing output files are
overwritten when a new run starts, including if that run later fails. Use a new
filename to preserve an earlier result. Input statements cannot be overwritten.
`--previous` may be omitted
when genuinely unavailable. A specified but missing/empty input file is an error.

Concurrent jury calls:

```powershell
npm run ai:score -- --statement ../data/statements/statement4.md --previous ../data/statements/previous4.md --output ../data/results/manual-statement4-parallel.json --parallel
```

The output records `jury_execution`. In parallel mode, if a jury call fails, the
runner waits for the other calls and saves their responses before marking the run
failed. Each failed call records its error. Baseline failure starts no jury calls.

Run `npm run ai:score -- --help` to see the command syntax. `--statement` and
`--output` are required; `--previous` and the boolean `--parallel` flag are optional.
Absolute paths and quoted paths containing spaces are supported.

The installed dependencies are sufficient. On a fresh checkout run `npm ci`.
The runner reads `GEMINI_API_KEY` or the existing local `api_key`; neither is
printed or saved in results. Model: `gemini-3.5-flash-lite`, medium thinking;
baseline temperature 0, jury temperature 0.2. Each manual run consumes API usage.

## Files and output

| File | Purpose |
|---|---|
| `CONSOLIDATED-SCORING-SPEC.md` | Sole current scoring specification |
| `PASS1-BASELINE-PROMPT.md` | Neutral extraction instructions; runtime inserts rule catalog |
| `PASS2-JURY-PROMPT.md` | Jury instructions and three persona definitions |
| `scoring.ts` | Fixed rules, schemas, validation, and arithmetic |
| `fomc_parser.ts` | Four-call runner and output persistence |
| `scoring.test.ts` | Synthetic unit/orchestration tests, not source evidence |

The console displays baseline, coverage, status, confidence, and each jury result.
The output JSON contains:

- `run_status`: `completed` only after all four responses validate; otherwise `failed`.
- `phase4`: lean baseline score, coverage, status, confidence.
- `baseline`: validated components, computed component/category scores, completeness,
  diagnostics, and unrounded totals.
- `jury`: three separate persona responses; they do not modify the baseline.
- `avg_jury_score`: root-level arithmetic mean of the three validated jury scores,
  also shown in the console summary. It remains null until all three succeed;
  the mean is rounded to one decimal place.
- `final_score`: root-level `(baseline_score + avg_jury_score) / 2`, rounded to
  one decimal using those reported scores. It stays null if the baseline is
  unavailable or any jury call fails. Underlying scores remain unchanged.
  This 50/50 blend is provisional; coverage/status/confidence still describe
  baseline evidence completeness, not confidence in the blended result.
- `calls`: exact prompts, statement inputs, response schemas, raw responses, returned
  model versions, and token-usage metadata for audit and reproduction.
- Rule/prompt versions, timestamps, model/settings, and any error.

The runner saves progress after each call. If an API or structural validation
failure occurs, it exits unsuccessfully and preserves the partial record; it does
not invent missing responses. Invalid quotations are excluded from scoring and
coverage with diagnostics. Coverage labels are not correctness probabilities.

## Verification

```powershell
npm run check
npm test
```

The archived live smoke output is `../../../study-history/results/v05-smoke-statement4-verified.json`:
four completed calls, no invalid components or verbatim failures, baseline 45.6,
coverage 73.25%, PASS, Medium; jury scores 20, 25, 25. These are observed smoke
results, not calibrated targets or repeatability claims.

`../../../study-history/results/v05-smoke-statement4.json` is the earlier diagnostic smoke run: it
exposed unnecessary range fields alongside a direct rate-change input. The
response schema was tightened to make rate-input modes mutually exclusive.
Historical results, comparison/tracker documents, the Statement 4 analysis, and
older smoke/manual outputs are retained in [study-history](../../../study-history).
Statements and current manual results remain in the variable data folder;
dependencies and credentials are beside this README. No evidence was deleted.

## Troubleshooting and integration

- Missing module or wrong-platform dependency: run `npm ci` here.
- Authentication/quota/network error: check your key, model access, and quota.
  Parallel calls can hit rate limits sooner; omit `--parallel` to run sequentially.
- A failed run exits nonzero and retains available responses in the output file.
  There is no automatic retry. Inspect `error`, call errors, and diagnostics.
- `PASS` is an evidence-coverage label, not an assertion of score accuracy.
- Treat `run_status: completed` as workflow completion. The root `final_score`
  is the agreed blended result; the nested `phase4` object still describes the
  baseline alone. Do not silently substitute its baseline score for `final_score`.
- `scoring.ts` and `runStudy` in `fomc_parser.ts` expose the existing calculation
  and orchestration functions for later L3-006 integration. The command-line entry
  point is the supported manual execution path; no separate build is required.

The superseded `SCORING-RULES.md` and `AI-JURY-OVERLAY-PROMPT.md` were removed;
old archived reports may still mention them as historical references.
