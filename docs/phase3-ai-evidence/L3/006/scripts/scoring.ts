export const RULE_VERSION = '0.5';
export const PERSONAS = ['CENTRAL_BANK_POLICY_ECONOMIST', 'GOLD_CROSS_ASSET_STRATEGIST', 'FINANCIAL_COMMUNICATIONS_ANALYST'] as const;
type Rule = { score: number; meaning: string; rank?: number };
type Definition = { weight: number; rules: Record<string, Rule> };
const rule = (score: number, meaning: string, rank?: number): Rule => ({ score, meaning, ...(rank === undefined ? {} : { rank }) });

// Scores live here, not in the AI response. This catalog also supplies the prompt.
export const DEFINITIONS: Record<string, Definition> = {
  'policy.rate_action': { weight: 0.60, rules: {
    rate_change_bps: rule(0, 'Explicit signed change in basis points; value is stated magnitude, not calculated from ranges'),
    rate_change_percentage_points: rule(0, 'Explicit signed change in percentage points; half-point cut = -0.5'),
    rate_target_ranges: rule(0, 'Separately quoted current and prior target endpoints; TypeScript computes the difference'),
    rate_hold: rule(50, 'Explicit unchanged/maintained target'),
    rate_lower: rule(0, 'Explicit cut, only when magnitude and comparable ranges unavailable'),
    rate_raise: rule(100, 'Explicit hike, only when magnitude and comparable ranges unavailable'),
  } },
  'policy.forward_guidance': { weight: 0.30, rules: {
    guidance_strong_dovish: rule(-20, 'Strong explicit commitment toward easing or maintaining low rates'),
    guidance_moderate_dovish: rule(-10, 'Explicit moderate easing bias or dovish support'),
    guidance_data_dependent: rule(0, 'Explicit neutral/data-dependent guidance'),
    guidance_moderate_hawkish: rule(10, 'Explicit moderate tightening bias or hawkish caution'),
    guidance_strong_hawkish: rule(20, 'Strong explicit commitment toward further tightening'),
  } },
  'policy.voting': { weight: 0.10, rules: {
    vote_unanimous: rule(0, 'Reported unanimous vote; count = 0'),
    vote_dovish_dissent: rule(-5, 'Dissent for easier action than adopted; count of dovish dissenters'),
    vote_hawkish_dissent: rule(5, 'Dissent for tighter action than adopted; count of hawkish dissenters'),
  } },
  'balance_sheet.asset_purchases': { weight: 0.60, rules: {
    balance_sheet_large_qe_expansion: rule(0, 'Large QE expansion', 0),
    balance_sheet_ongoing_purchases: rule(15, 'Ongoing purchases', 1),
    balance_sheet_tapering: rule(30, 'Purchases continue at a reduced pace', 2),
    balance_sheet_reinvestment_only: rule(50, 'Reinvestment only; no net purchases', 3),
    balance_sheet_reduction_runoff: rule(80, 'Reduction/runoff of holdings', 4),
  } },
  'balance_sheet.liquidity_operations': { weight: 0.40, rules: {
    balance_sheet_liquidity_expanded: rule(0, 'Explicit expanded liquidity operations', 0),
    balance_sheet_liquidity_normal: rule(50, 'Explicit normal liquidity operations', 1),
    balance_sheet_liquidity_reduced: rule(75, 'Explicit reduced liquidity operations', 2),
    balance_sheet_liquidity_tightening: rule(90, 'Explicit active liquidity tightening', 3),
  } },
  'inflation.level': { weight: 0.50, rules: {
    inflation_level_numeric: rule(0, 'Actual 12-month inflation rate; value in percent, not target or forecast'),
    inflation_level_well_below_2: rule(10, 'well/significantly below 2 percent'),
    inflation_level_below_2: rule(25, 'below 2 percent'),
    inflation_level_somewhat_below_2: rule(30, 'somewhat below 2 percent'),
    inflation_level_slightly_below_2: rule(35, 'running slightly below 2 percent'),
    inflation_level_close_to_2: rule(45, 'close to 2 percent'),
    inflation_level_near_2: rule(50, 'near/at/right at/around 2 percent'),
    inflation_level_slightly_above_2: rule(55, 'slightly above 2 percent'),
    inflation_level_somewhat_elevated: rule(55, 'somewhat elevated'),
    inflation_level_above_2: rule(75, 'above 2 percent'),
    inflation_level_elevated: rule(75, 'elevated'),
    inflation_level_well_above_2: rule(90, 'well/significantly above 2 percent'),
  } },
  'inflation.trend': { weight: 0.25, rules: {
    inflation_trend_declined_sharply: rule(10, 'inflation has declined sharply'),
    inflation_trend_declined: rule(20, 'inflation has declined/fallen/been falling'),
    inflation_trend_moved_lower: rule(25, 'inflation has moved lower'),
    inflation_trend_eased: rule(30, 'inflation has eased'),
    inflation_trend_little_changed: rule(50, 'inflation has been little changed/stable/roughly stable/about the same'),
    inflation_trend_firmed: rule(70, 'inflation has firmed'),
    inflation_trend_risen: rule(80, 'inflation has risen/increased/moved higher'),
  } },
  'inflation.expectations.market_based': { weight: 0.125, rules: {
    inflation_expectations_market_declined: rule(20, 'market-based measures of inflation compensation have declined/fallen'),
    inflation_expectations_market_moved_lower: rule(25, 'market-based measures of inflation compensation have moved lower'),
    inflation_expectations_market_stable: rule(50, 'market-based measures of inflation compensation are little changed'),
    inflation_expectations_market_risen: rule(80, 'market-based measures of inflation compensation have risen/increased'),
  } },
  'inflation.expectations.survey_based': { weight: 0.125, rules: {
    inflation_expectations_survey_declined: rule(20, 'survey-based measures of longer-term inflation expectations have declined/fallen'),
    inflation_expectations_survey_stable: rule(50, 'survey-based measures of longer-term inflation expectations are little changed/stable'),
    inflation_expectations_survey_risen: rule(80, 'survey-based measures of longer-term inflation expectations have risen'),
  } },
  'labour.unemployment_level': { weight: 0.20, rules: {
    labour_unemployment_low: rule(70, 'unemployment low/remained low'),
    labour_unemployment_high: rule(15, 'unemployment elevated/high'),
  } },
  'labour.unemployment_direction': { weight: 0.20, rules: {
    labour_unemployment_rising: rule(20, 'unemployment moved up/increased/rose'),
    labour_unemployment_stable: rule(50, 'unemployment little changed'),
    labour_unemployment_falling: rule(80, 'unemployment declined/fell'),
  } },
  'labour.job_gains': { weight: 0.35, rules: {
    labour_job_gains_solid: rule(65, 'solid job gains'),
    labour_job_gains_weak: rule(20, 'weak job gains'),
    labour_job_gains_moderated: rule(50, 'moderate/moderated/slowed job gains'),
  } },
  'labour.slack_wage_pressures': { weight: 0.25, rules: {
    labour_slack_remains: rule(25, 'slack remains'),
    labour_market_tight: rule(85, 'labour market tight'),
    labour_wage_pressures: rule(80, 'wage pressures building'),
    labour_underemployment: rule(30, 'underemployment'),
  } },
  'growth.current_activity': { weight: 0.50, rules: {
    growth_contraction: rule(10, 'contraction'),
    growth_moderate_pace: rule(55, 'moderate rate/pace'),
    growth_strong_footing: rule(65, 'strong footing'),
    growth_solid_pace: rule(70, 'solid pace'),
  } },
  'growth.forward_risks': { weight: 0.30, rules: {
    growth_downside_risks: rule(20, 'downside risks'),
    growth_activity_weighed_down: rule(20, 'will weigh on activity; uncertainty weighing on activity'),
    growth_below_potential: rule(20, 'below potential'),
    growth_upside_risks: rule(80, 'upside risks'),
    growth_above_potential: rule(80, 'above potential'),
  } },
  'growth.specific_sectors': { weight: 0.20, rules: {
    growth_business_fixed_investment_exports_weak: rule(25, 'business fixed investment and exports weak'),
    growth_consumer_spending_strong: rule(70, 'consumer spending strong'),
  } },
};

// JSON schema is shared by the API request and local validation.
type Schema = { type?: string; properties?: Record<string, Schema>; required?: string[]; additionalProperties?: boolean; anyOf?: Schema[]; enum?: unknown[]; items?: Schema; minimum?: number; maximum?: number; minLength?: number };
const object = (properties: Record<string, Schema>): Schema => ({ type: 'object', properties, required: Object.keys(properties), additionalProperties: false });
const nullable = (s: Schema): Schema => ({ anyOf: [s, { type: 'null' }] });
const str: Schema = { type: 'string', minLength: 1 };
const num: Schema = { type: 'number' };
const range = nullable(object({ evidence: str, lower: num, upper: num }));
const componentProperties: Record<string, Schema> = {};
for (const [key, def] of Object.entries(DEFINITIONS)) {
  const id = nullable({ type: 'string', enum: Object.keys(def.rules) });
  let properties: Record<string, Schema> = { evidence: nullable(str), rule_id: id };
  if (key.startsWith('balance_sheet.')) properties = { current_evidence: nullable(str), current_rule_id: id, prior_evidence: nullable(str), prior_rule_id: id };
  if (key === 'policy.rate_action') Object.assign(properties, { value: nullable(num), current_range: range, prior_range: range });
  if (key === 'policy.voting') properties.count = nullable({ type: 'integer', minimum: 0 });
  if (key === 'inflation.level') properties.value = nullable(num);
  const parts = key.split('.');
  let parent = componentProperties;
  for (let i = 0; i < parts.length - 1; i++) {
    const part = parts[i];
    parent[part] ??= object({});
    parent[part].required = [...new Set([...(parent[part].required ?? []), parts[i + 1]])];
    parent = parent[part].properties!;
  }
  parent[parts.at(-1)!] = object(properties);
}
const nil: Schema = { type: 'null' };
componentProperties.policy.properties!.rate_action = { anyOf: [
  object({ evidence: nil, rule_id: nil, value: nil, current_range: nil, prior_range: nil }),
  object({ evidence: str, rule_id: { type: 'string', enum: ['rate_change_bps', 'rate_change_percentage_points'] }, value: num, current_range: nil, prior_range: nil }),
  object({ evidence: str, rule_id: { type: 'string', enum: ['rate_hold', 'rate_lower', 'rate_raise'] }, value: nil, current_range: nil, prior_range: nil }),
  object({ evidence: str, rule_id: { type: 'string', enum: ['rate_target_ranges'] }, value: nil, current_range: range.anyOf![0], prior_range: range.anyOf![0] }),
] };
export const BASELINE_SCHEMA = object({
  components: object(componentProperties),
  diagnostics: object({ competing_matches: { type: 'array', items: object({ component: { type: 'string', enum: Object.keys(DEFINITIONS) }, evidence: str, reason: str }) } }),
  error: nullable(str),
});
export const JURY_SCHEMA = object({ jury_score: { type: 'number', minimum: 0, maximum: 100 }, supporting_statement: str });

export function validateShape(value: unknown, schema: Schema, at = 'response'): void {
  if (schema.anyOf) {
    if (schema.anyOf.some(s => { try { validateShape(value, s, at); return true; } catch { return false; } })) return;
    throw new Error(`${at}: invalid type or value`);
  }
  if (schema.enum && !schema.enum.includes(value)) throw new Error(`${at}: unknown rule/value`);
  if (schema.type === 'null' && value !== null) throw new Error(`${at}: expected null`);
  if (schema.type === 'string' && (typeof value !== 'string' || value.length < (schema.minLength ?? 0))) throw new Error(`${at}: expected nonempty string`);
  if (schema.type === 'number' || schema.type === 'integer') {
    if (typeof value !== 'number' || !Number.isFinite(value) || (schema.type === 'integer' && !Number.isInteger(value)) || value < (schema.minimum ?? -Infinity) || value > (schema.maximum ?? Infinity)) throw new Error(`${at}: invalid number`);
  }
  if (schema.type === 'array') {
    if (!Array.isArray(value)) throw new Error(`${at}: expected array`);
    value.forEach((v, i) => validateShape(v, schema.items!, `${at}[${i}]`));
  }
  if (schema.type === 'object') {
    if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error(`${at}: expected object`);
    const record = value as Record<string, unknown>;
    for (const name of schema.required ?? []) if (!(name in record)) throw new Error(`${at}.${name}: required`);
    for (const [name, v] of Object.entries(record)) {
      if (!schema.properties?.[name]) throw new Error(`${at}.${name}: unexpected field`);
      validateShape(v, schema.properties[name], `${at}.${name}`);
    }
  }
}

export function emptyExtraction(): any {
  const blank = (s: Schema): unknown => s.anyOf ? (s.anyOf.some(v => v.type === 'null') ? null : blank(s.anyOf[0])) : s.type === 'object' ? Object.fromEntries(Object.entries(s.properties!).map(([k, v]) => [k, blank(v)])) : s.type === 'array' ? [] : null;
  return blank(BASELINE_SCHEMA);
}
export const getComponent = (root: any, key: string): any => key.split('.').reduce((v, k) => v[k], root);
const clamp = (n: number): number => Math.max(0, Math.min(100, n));
export function labels(coverage: number) {
  return { status: coverage >= 60 ? 'PASS' : coverage >= 40 ? 'FLAG' : 'BLOCKED', confidence: coverage >= 90 ? 'High' : coverage >= 70 ? 'Medium' : 'Low' };
}

export function scoreBaseline(input: unknown, current: string, prior: string | null) {
  validateShape(input, BASELINE_SCHEMA);
  const data = structuredClone(input) as any;
  if (data.error !== null) throw new Error(`Extraction error: ${data.error}`);
  const diagnostics = {
    competing_matches: data.diagnostics.competing_matches,
    verbatim_check_failed: [] as { component: string; evidence: string }[],
    invalid_components: [] as { component: string; reason: string }[],
    prior_statement_missing: prior === null,
    balance_sheet_fallback_used: false,
    fallback_components: [] as string[],
    rate_fallback_used: false,
  };
  const invalid = (key: string, reason: string) => { diagnostics.invalid_components.push({ component: key, reason }); return false; };
  const quoted = (evidence: string | null, source: string | null, key: string): boolean => {
    if (evidence !== null && source !== null && source.includes(evidence)) return true;
    if (evidence !== null) diagnostics.verbatim_check_failed.push({ component: key, evidence });
    return false;
  };
  const selected = (leaf: any, source: string | null, key: string): boolean => {
    if (leaf.rule_id === null && leaf.evidence === null) return false;
    if (leaf.rule_id === null || leaf.evidence === null) return invalid(key, 'Evidence and rule must both be present or both null');
    return quoted(leaf.evidence, source, key);
  };
  const scores: Record<string, number | null> = {};
  const completeness: Record<string, number> = {};
  const ledger: Record<string, { score: number | null; available: boolean; fallback: boolean }> = {};
  for (const [key, def] of Object.entries(DEFINITIONS)) {
    const leaf = getComponent(data.components, key);
    let score: number | null = null;
    let fallback = false;
    const conflict = data.diagnostics.competing_matches.some((c: any) => c.component === key);
    if (conflict) invalid(key, 'Unresolved extraction conflict');
    else if (key.startsWith('balance_sheet.')) {
      const validCurrent = selected({ evidence: leaf.current_evidence, rule_id: leaf.current_rule_id }, current, key);
      const validPrior = selected({ evidence: leaf.prior_evidence, rule_id: leaf.prior_rule_id }, prior, `${key}.prior`);
      if (validCurrent) {
        const cur = def.rules[leaf.current_rule_id];
        fallback = !validPrior;
        if (fallback) score = cur.score;
        else {
          const diff = cur.rank! - def.rules[leaf.prior_rule_id].rank!;
          score = diff <= -2 ? 0 : diff === -1 ? 20 : diff === 0 ? 50 : diff === 1 ? 80 : 100;
        }
      }
      if (!validCurrent) { leaf.current_evidence = null; leaf.current_rule_id = null; }
      if (!validPrior) { leaf.prior_evidence = null; leaf.prior_rule_id = null; }
    } else if (selected(leaf, current, key)) {
      const id = leaf.rule_id as string;
      score = def.rules[id].score;
      if (key === 'policy.rate_action') {
        const rangeValid = (r: any, source: string | null, name: string) => r !== null && quoted(r.evidence, source, name) && (r.lower <= r.upper || invalid(name, 'Reversed target endpoints'));
        if (id === 'rate_target_ranges') {
          const a = rangeValid(leaf.current_range, current, `${key}.current_range`);
          const b = rangeValid(leaf.prior_range, prior, `${key}.prior_range`);
          if (!a || !b || leaf.value !== null) { invalid(key, 'Range mode requires valid current/prior endpoints and null value'); score = null; }
          else score = clamp(50 + 0.5 * 100 * ((leaf.current_range.lower + leaf.current_range.upper - leaf.prior_range.lower - leaf.prior_range.upper) / 2));
        } else if (id === 'rate_change_bps' || id === 'rate_change_percentage_points') {
          if (leaf.value === null) { invalid(key, 'Explicit magnitude requires numeric value'); score = null; }
          else score = clamp(50 + 0.5 * leaf.value * (id === 'rate_change_bps' ? 1 : 100));
        } else {
          if (leaf.value !== null) { invalid(key, 'Direction/hold requires null value'); score = null; }
          else diagnostics.rate_fallback_used = id !== 'rate_hold';
        }
        if (id !== 'rate_target_ranges' && (leaf.current_range !== null || leaf.prior_range !== null)) { invalid(key, 'Unused ranges must be null'); score = null; }
      }
      if (key === 'inflation.level') {
        if (id === 'inflation_level_numeric') {
          if (leaf.value === null) { invalid(key, 'Numerical inflation needs value'); score = null; }
          else score = clamp(50 + 25 * (leaf.value - 2));
        } else if (leaf.value !== null) { invalid(key, 'Descriptive inflation needs null value'); score = null; }
      }
      if (key === 'policy.voting') {
        if (id === 'vote_unanimous') {
          if (leaf.count !== 0) { invalid(key, 'Unanimous vote requires count zero'); score = null; }
        } else if (leaf.count === null || leaf.count < 1) { invalid(key, 'Dissent requires positive count'); score = null; }
        else score = Math.sign(score!) * (leaf.count === 1 ? 5 : 8);
      }
    }
    if (score === null) {
      for (const field of Object.keys(leaf)) leaf[field] = null;
    }
    if (fallback) diagnostics.fallback_components.push(key);
    ledger[key] = { score, available: score !== null, fallback };
  }
  diagnostics.balance_sheet_fallback_used = diagnostics.fallback_components.length > 0;
  const weights: Record<string, number> = { policy: .35, balance_sheet: .20, inflation: .20, labour: .15, growth: .10 };
  const completenessUnits: Record<string, number> = {};
  for (const category of Object.keys(weights)) {
    const entries = Object.entries(ledger).filter(([k]) => k.startsWith(`${category}.`));
    const available = entries.filter(([, v]) => v.available);
    const totalWeight = available.reduce((n, [k]) => n + DEFINITIONS[k].weight, 0);
    scores[category] = totalWeight ? available.reduce((n, [k, v]) => n + DEFINITIONS[k].weight * v.score!, 0) / totalWeight : null;
    // Fixed weights are exact integer thousandths; discounts are integer percent.
    // Avoid turning an exact 40% into 39.99999999999999 at a status boundary.
    completenessUnits[category] = available.reduce((n, [k, v]) => n + (DEFINITIONS[k].weight * 1000) * (v.fallback ? 80 : 100), 0);
    completeness[category] = completenessUnits[category] / 100000;
  }
  const anchor = ledger['policy.rate_action'].score;
  scores.policy = anchor === null ? null : clamp(anchor + (ledger['policy.forward_guidance'].score ?? 0) + (ledger['policy.voting'].score ?? 0));
  if (anchor === null) { completeness.policy = 0; completenessUnits.policy = 0; }
  const present = Object.keys(weights).filter(k => scores[k] !== null);
  const baseline = present.length ? present.reduce((n, k) => n + weights[k] * scores[k]!, 0) / present.reduce((n, k) => n + weights[k], 0) : null;
  const coverage = Object.keys(weights).reduce((n, k) => n + (weights[k] * 100) * completenessUnits[k], 0) / 100000;
  return {
    baseline_score: baseline === null ? null : Number(baseline.toFixed(1)),
    coverage: Number(coverage.toFixed(2)), ...labels(coverage),
    category_scores: scores, category_completeness: completeness,
    unrounded: { baseline_score: baseline, coverage },
    components: data.components, component_scores: ledger, diagnostics,
  };
}
