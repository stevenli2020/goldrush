import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { BASELINE_SCHEMA, DEFINITIONS, JURY_SCHEMA, emptyExtraction, getComponent, labels, scoreBaseline, validateShape } from './scoring';
import { buildRequests, prepareOutput, runStudy } from './fomc_parser';

// Synthetic unit fixtures only. These are never saved as live/source evidence.
const source = 'Synthetic evidence for arithmetic tests.';
test('output is created or overwritten, but input statements are protected', () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'fomc-output-test-'));
  const input = path.join(directory, 'statement.md');
  const output = path.join(directory, 'result.json');
  try {
    fs.writeFileSync(input, 'source statement');
    prepareOutput(output, [input]);
    assert.equal(fs.readFileSync(output, 'utf8'), '{}\n');
    fs.writeFileSync(output, 'long obsolete output contents');
    prepareOutput(output, [input]);
    assert.equal(fs.readFileSync(output, 'utf8'), '{}\n');
    assert.throws(() => prepareOutput(input, [input]), /must not overwrite/);
    assert.equal(fs.readFileSync(input, 'utf8'), 'source statement');
  } finally {
    fs.unlinkSync(input);
    if (fs.existsSync(output)) fs.unlinkSync(output);
    fs.rmdirSync(directory);
  }
});
const near = (actual: number | null, expected: number) => assert.ok(actual !== null && Math.abs(actual - expected) < 1e-10, `${actual} != ${expected}`);
function set(data: any, key: string, id: string, extra: object = {}) {
  Object.assign(getComponent(data.components, key), { evidence: source, rule_id: id }, extra);
}
function balance(data: any, key: string, current: string | null, prior: string | null) {
  Object.assign(getComponent(data.components, `balance_sheet.${key}`), {
    current_evidence: current ? source : null, current_rule_id: current,
    prior_evidence: prior ? source : null, prior_rule_id: prior,
  });
}
function example() {
  const data = emptyExtraction();
  set(data, 'policy.rate_action', 'rate_change_bps', { value: -50 });
  set(data, 'policy.forward_guidance', 'guidance_data_dependent');
  set(data, 'policy.voting', 'vote_hawkish_dissent', { count: 1 });
  balance(data, 'asset_purchases', 'balance_sheet_reduction_runoff', 'balance_sheet_reduction_runoff');
  set(data, 'inflation.level', 'inflation_level_somewhat_elevated');
  set(data, 'inflation.trend', 'inflation_trend_eased');
  set(data, 'labour.unemployment_level', 'labour_unemployment_low');
  set(data, 'labour.unemployment_direction', 'labour_unemployment_rising');
  set(data, 'labour.job_gains', 'labour_job_gains_moderated');
  set(data, 'growth.current_activity', 'growth_solid_pace');
  return data;
}

test('agreed example: exact component arithmetic and final rounding', () => {
  const result = scoreBaseline(example(), source, source);
  near(result.category_scores.policy, 30);
  near(result.category_scores.inflation, 35 / .75);
  near(result.category_scores.labour, 35.5 / .75);
  near(result.category_scores.growth, 70);
  assert.equal(result.baseline_score, 43.9);
  assert.equal(result.coverage, 78.25);
  assert.equal(result.status, 'PASS');
  assert.equal(result.confidence, 'Medium');
  assert.deepEqual(scoreBaseline(example(), source, source), result);
});

test('all missing and missing policy anchor cannot get coverage from guidance/votes', () => {
  const data = emptyExtraction();
  set(data, 'policy.forward_guidance', 'guidance_strong_hawkish');
  set(data, 'policy.voting', 'vote_hawkish_dissent', { count: 2 });
  const result = scoreBaseline(data, source, null);
  assert.equal(result.category_scores.policy, null);
  assert.equal(result.category_completeness.policy, 0);
  assert.equal(result.baseline_score, null);
  assert.equal(result.coverage, 0);
  assert.equal(result.status, 'BLOCKED');
  assert.equal(result.confidence, 'Low');
});

test('optional policy adjustments are omitted, not counted as neutral evidence', () => {
  const data = emptyExtraction();
  set(data, 'policy.rate_action', 'rate_hold');
  const r = scoreBaseline(data, source, null);
  assert.equal(r.baseline_score, 50);
  near(r.category_completeness.policy, .6);
  assert.equal(r.coverage, 21);
  for (const count of [1, 2]) {
    set(data, 'policy.voting', 'vote_dovish_dissent', { count });
    assert.equal(scoreBaseline(data, source, null).baseline_score, count === 1 ? 45 : 42);
  }
});

test('numeric rate units, target midpoint calculation, hold and direction fallback', () => {
  for (const [id, extra, expected] of [
    ['rate_change_bps', { value: -50 }, 25],
    ['rate_change_percentage_points', { value: -.5 }, 25],
    ['rate_change_bps', { value: 200 }, 100],
    ['rate_change_bps', { value: -200 }, 0],
    ['rate_hold', {}, 50], ['rate_lower', {}, 0], ['rate_raise', {}, 100],
    ['rate_target_ranges', { current_range: { evidence: source, lower: 4.75, upper: 5 }, prior_range: { evidence: source, lower: 5.25, upper: 5.5 } }, 25],
  ] as const) {
    const data = emptyExtraction();
    set(data, 'policy.rate_action', id, extra);
    const r = scoreBaseline(data, source, source);
    assert.equal(r.baseline_score, expected);
    assert.equal(r.diagnostics.rate_fallback_used, ['rate_lower', 'rate_raise'].includes(id));
  }
});

test('balance rank directions, unchanged, per-component fallback penalties and missing current', () => {
  const asset = ['balance_sheet_large_qe_expansion', 'balance_sheet_ongoing_purchases', 'balance_sheet_tapering', 'balance_sheet_reinvestment_only', 'balance_sheet_reduction_runoff'];
  for (let c = 0; c < asset.length; c++) for (let p = 0; p < asset.length; p++) {
    const data = emptyExtraction();
    balance(data, 'asset_purchases', asset[c], asset[p]);
    const diff = c - p;
    assert.equal(scoreBaseline(data, source, source).baseline_score, diff <= -2 ? 0 : diff === -1 ? 20 : diff === 0 ? 50 : diff === 1 ? 80 : 100);
  }
  for (const [assetPrior, liquidPrior, expected] of [[true, true, 1], [false, true, .88], [true, false, .92], [false, false, .8]] as const) {
    const data = emptyExtraction();
    balance(data, 'asset_purchases', asset[4], assetPrior ? asset[4] : null);
    balance(data, 'liquidity_operations', 'balance_sheet_liquidity_normal', liquidPrior ? 'balance_sheet_liquidity_normal' : null);
    near(scoreBaseline(data, source, source).category_completeness.balance_sheet, expected);
  }
  const data = emptyExtraction();
  balance(data, 'asset_purchases', asset[4], null);
  near(scoreBaseline(data, source, source).category_completeness.balance_sheet, .48);
  balance(data, 'asset_purchases', null, asset[4]);
  assert.equal(scoreBaseline(data, source, source).baseline_score, null);
});

test('inflation independent expectations and numerical level', () => {
  const data = emptyExtraction();
  set(data, 'inflation.level', 'inflation_level_somewhat_elevated');
  set(data, 'inflation.trend', 'inflation_trend_eased');
  set(data, 'inflation.expectations.market_based', 'inflation_expectations_market_declined');
  const r = scoreBaseline(data, source, null);
  near(r.category_scores.inflation, 37.5 / .875);
  near(r.category_completeness.inflation, .875);
  set(data, 'inflation.expectations.survey_based', 'inflation_expectations_survey_stable');
  near(scoreBaseline(data, source, null).category_scores.inflation, 43.75);
  const numeric = emptyExtraction();
  set(numeric, 'inflation.level', 'inflation_level_numeric', { value: 1.5 });
  assert.equal(scoreBaseline(numeric, source, null).baseline_score, 37.5);
});

test('verbatim failures, wrong source and conflicts are removed with diagnostics; raw input preserved', () => {
  const data = example();
  data.components.inflation.level.evidence = 'not a substring';
  data.components.balance_sheet.asset_purchases.prior_evidence = 'not in prior';
  data.diagnostics.competing_matches = [{ component: 'labour.job_gains', evidence: source, reason: 'unresolved' }];
  const r = scoreBaseline(data, source, source);
  assert.equal(r.component_scores['inflation.level'].available, false);
  assert.equal(r.components.inflation.level.rule_id, null);
  assert.equal(r.component_scores['labour.job_gains'].available, false);
  assert.equal(r.diagnostics.verbatim_check_failed.length, 2);
  assert.equal(r.diagnostics.balance_sheet_fallback_used, true);
  assert.equal(data.components.inflation.level.evidence, 'not a substring');
  assert.equal(scoreBaseline(example(), source, null).diagnostics.balance_sheet_fallback_used, true);
});

test('bad shape/rules/numeric types fail; inconsistent numeric inputs excluded', () => {
  for (const mutate of [
    (d: any) => { delete d.components.growth; },
    (d: any) => { d.baseline_score = 50; },
    (d: any) => { d.components.policy.rate_action.rule_id = 'growth_solid_pace'; },
    (d: any) => { d.components.policy.rate_action.value = '50'; },
    (d: any) => { d.components.policy.voting.count = 1.5; },
  ]) {
    const d = example(); mutate(d);
    assert.throws(() => scoreBaseline(d, source, source));
  }
  const d = example(); d.components.policy.rate_action.value = null;
  assert.throws(() => scoreBaseline(d, source, source));
  const range = emptyExtraction();
  set(range, 'policy.rate_action', 'rate_target_ranges', { current_range: { evidence: source, lower: 5, upper: 4 }, prior_range: { evidence: source, lower: 5, upper: 6 } });
  assert.equal(scoreBaseline(range, source, source).baseline_score, null);
});

test('thresholds use unrounded coverage, including near displayed boundaries', () => {
  for (const [n, status, confidence] of [[39.999, 'BLOCKED', 'Low'], [40, 'FLAG', 'Low'], [59.999, 'FLAG', 'Low'], [60, 'PASS', 'Low'], [69.999, 'PASS', 'Low'], [70, 'PASS', 'Medium'], [89.999, 'PASS', 'Medium'], [90, 'PASS', 'High']] as const) {
    assert.deepEqual(labels(n), { status, confidence });
  }
});

test('exact 40% coverage stays FLAG after weighted accumulation', () => {
  const d = emptyExtraction();
  set(d, 'policy.rate_action', 'rate_hold');
  set(d, 'policy.forward_guidance', 'guidance_data_dependent');
  set(d, 'policy.voting', 'vote_unanimous', { count: 0 });
  set(d, 'inflation.trend', 'inflation_trend_eased');
  const r = scoreBaseline(d, source, null);
  assert.equal(r.unrounded.coverage, 40);
  assert.equal(r.status, 'FLAG');
  assert.equal(r.category_completeness.policy, 1);
});

test('every defined rule is accepted only by its own component schema', () => {
  validateShape(emptyExtraction(), BASELINE_SCHEMA);
  for (const [key, def] of Object.entries(DEFINITIONS)) for (const id of Object.keys(def.rules)) {
    const d = emptyExtraction();
    if (key.startsWith('balance_sheet.')) balance(d, key.split('.')[1], id, null);
    else if (key === 'policy.rate_action') {
      const extra = id === 'rate_target_ranges' ? { current_range: { evidence: source, lower: 5, upper: 5 }, prior_range: { evidence: source, lower: 5, upper: 5 } }
        : id.startsWith('rate_change_') ? { value: -0.5 } : {};
      set(d, key, id, extra);
    } else set(d, key, id);
    validateShape(d, BASELINE_SCHEMA);
  }
  assert.throws(() => validateShape({ jury_score: 101, supporting_statement: 'x' }, JURY_SCHEMA));
  assert.throws(() => validateShape({ jury_score: 50, supporting_statement: 'x', baseline_score: 50 }, JURY_SCHEMA));
});

test('four independent requests, correct temperatures, no baseline/persona leakage', async () => {
  const requests = buildRequests(source, 'prior');
  assert.equal(requests.length, 4);
  assert.equal(requests[0].temperature, 0);
  assert.ok(!requests[0].systemInstruction.includes('CENTRAL_BANK_POLICY_ECONOMIST'));
  for (const r of requests.slice(1)) {
    assert.equal(r.temperature, .2);
    assert.deepEqual(JSON.parse(r.contents), { CURRENT_STATEMENT: source, PRIOR_STATEMENT: 'prior' });
    assert.ok(!r.systemInstruction.includes('inflation_level_somewhat_elevated'));
  }
  let calls = 0;
  const saved: any[] = [];
  const result = await runStudy(source, source, async () => ({ text: JSON.stringify(calls++ === 0 ? example() : { jury_score: 40, supporting_statement: 'Synthetic test reply' }) }), r => saved.push(structuredClone(r)));
  assert.equal(calls, 4);
  assert.equal(result.run_status, 'completed');
  assert.equal(result.phase4.baseline_score, 43.9);
  assert.equal(result.avg_jury_score, 40);
  assert.equal(result.final_score, 42);
  assert.equal(Object.keys(result.jury).length, 3);
  assert.ok(saved.some(r => r.baseline && Object.keys(r.jury).length === 0));
});

test('failed response is archived without fabricated completion or extra calls', async () => {
  let latest: any;
  let calls = 0;
  await assert.rejects(runStudy(source, null, async () => { calls++; return { text: 'not json' }; }, r => { latest = structuredClone(r); }));
  assert.equal(calls, 1);
  assert.equal(latest.run_status, 'failed');
  assert.equal(latest.calls[0].response.text, 'not json');
  assert.equal(latest.baseline, null);
});

test('jury concurrency is opt-in and baseline always completes first', async () => {
  for (const parallel of [false, true]) {
    let calls = 0;
    const releases: (() => void)[] = [];
    let latest: any;
    const running = runStudy(source, source, async () => {
      const index = calls++;
      await new Promise<void>(resolve => releases[index] = resolve);
      return { text: JSON.stringify(index === 0 ? example() : { jury_score: index === 3 ? 32 : index * 10, supporting_statement: 'Synthetic test' }) };
    }, r => { latest = structuredClone(r); }, parallel);
    assert.equal(calls, 1);
    releases[0]();
    await new Promise(setImmediate);
    assert.equal(calls, parallel ? 4 : 2);
    assert.equal(latest.baseline.baseline_score, 43.9);
    if (parallel) {
      releases[3](); releases[2](); releases[1]();
    } else {
      releases[1](); await new Promise(setImmediate);
      assert.equal(calls, 3);
      releases[2](); await new Promise(setImmediate);
      assert.equal(calls, 4);
      releases[3]();
    }
    const r = await running;
    assert.equal(r.jury_execution, parallel ? 'parallel' : 'sequential');
    assert.equal(r.jury.CENTRAL_BANK_POLICY_ECONOMIST.jury_score, 10);
    assert.equal(r.jury.GOLD_CROSS_ASSET_STRATEGIST.jury_score, 20);
    assert.equal(r.jury.FINANCIAL_COMMUNICATIONS_ANALYST.jury_score, 32);
    assert.equal(r.avg_jury_score, 20.7);
    assert.equal(r.final_score, 32.3);
    assert.equal(r.run_status, 'completed');
  }
});

test('parallel jury failure waits for and preserves remaining responses', async () => {
  let calls = 0;
  let release!: () => void;
  let latest: any;
  const running = runStudy(source, source, async () => {
    const index = calls++;
    if (index === 0) return { text: JSON.stringify(example()) };
    if (index === 1) throw new Error('Synthetic API failure');
    if (index === 3) await new Promise<void>(resolve => release = resolve);
    return { text: JSON.stringify({ jury_score: 40, supporting_statement: 'Synthetic success' }) };
  }, r => { latest = structuredClone(r); }, true);
  const rejected = assert.rejects(running, /Synthetic API failure/);
  await new Promise(setImmediate);
  assert.equal(calls, 4);
  assert.equal(latest.run_status, 'in_progress');
  release();
  await rejected;
  assert.equal(latest.run_status, 'failed');
  assert.equal(Object.keys(latest.jury).length, 2);
  assert.equal(latest.avg_jury_score, null);
  assert.equal(latest.final_score, null);
  assert.equal(latest.calls[1].error, 'Synthetic API failure');
  assert.ok(latest.calls[3].response);
});

test('final score stays null when baseline is missing even with three jury scores', async () => {
  let calls = 0;
  const result = await runStudy(source, null, async () => ({ text: JSON.stringify(calls++ === 0
    ? emptyExtraction() : { jury_score: 20, supporting_statement: 'Synthetic test' }) }));
  assert.equal(result.avg_jury_score, 20);
  assert.equal(result.final_score, null);
});
