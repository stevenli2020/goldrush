# Governance / Handoff

**Project:** Gold Probability Engine for Weekly Gold Price Outlook
**Handoff status:** End of architecture/specification phase; Phase 1 is next.
**Date:** 2026-08-17
**Role of this file:** Governance and handoff SSOT for the next implementation agent.


# 1. STATUS

- **Project objective:** Build a weekly, repeatable, auditable gold-market decision-support system that estimates the probability of USD/oz gold spot ending in Bullish / Consolidation / Bearish states over four fixed horizons.
- **Weekly cadence:** Saturday or Sunday after the New York gold market close.
- **Target asset:** Gold spot price in USD per troy ounce.
- **Forecast horizons:** 1–5 days; 1–3 months; 1–3 years; 3–10 years.
- **Primary output:** P(Bullish), P(Consolidation), P(Bearish) for each horizon.
- **Net Index:** fixed directional-conviction score in [-1,+1]; +1 maximum bullish consensus, 0 neutral, -1 maximum bearish consensus. Binary reference mapping remains \(P(Higher)=((Net Index+1)/2)	imes100\%\), but it is not the final three-state output.
- **Causal architecture:** 12 locked layers; variables inside layers are expandable.
- **Data philosophy:** quantitative data is the backbone; AI is used for genuinely interpretive evidence.
- **Historical evidence philosophy:** historical events are contextual/supporting evidence, not an automatic weight optimizer; unavailable historical data must not be fabricated.
- **Weight philosophy:** initial weights are research-derived; later refinements are controlled, evidence-based, and not automatically changed after single forecast errors.
- **Implementation model:** worker agents operate at variable level; layer manager agents integrate and validate; worker agents can be released after acceptance and replaced for rework.
- **Random Forest:** optional supporting diagnostic only; not the core forecasting engine and not the authority for weights or final probabilities.

## Milestones completed
- Original deep-research report reviewed and upgraded into a causal framework.
- Gold Price Causal Model v2.1 and v2.2 developed; v2.2 is the current conceptual architecture.
- Project implementation proposal drafted.
- Spec C drafted and clarified for Phase 1 baseline handling.
- Spec D revised with confidence rubric and worked example.
- Spec A revised with numerical effective-weight example.
- Spec B revised with Range Propensity source and probability-mapping function; section numbering verified.
- External review completed for architecture/spec direction; outstanding issues from review were incorporated into Specs A/B/D.
- **Phase 1 has not started.** No variable registry has been built yet.


# 2. SSOT

## Definitive architecture
- Twelve causal layers are locked and must not be casually changed.
- Layer 0 — Gold Stock/Flow Architecture.
- Layer 1 — Real Rates / Opportunity Cost.
- Layer 2 — USD / FX.
- Layer 3 — Monetary-Policy Expectations.
- Layer 4 — Inflation, Purchasing Power & Fiscal Credibility.
- Layer 5 — Official-Sector Reserve Allocation.
- Layer 6 — Geopolitical Transmission: safe-haven; energy/inflation; reserve security; monetary fragmentation.
- Layer 7 — Global Liquidity & Financial Conditions.
- Layer 8 — Investment Flows.
- Layer 9 — Regional Physical Markets.
- Layer 10 — Market Microstructure & Derivatives.
- Layer 11 — Expectations, Psychology & Reflexivity.
- These are causal families, not twelve independent predictors. Double-counting must be controlled.

## Core scoring rules
- Variable stance \(S_i\): -1.0 to +1.0.
- Variable confidence \(C_i\): 0.0 to 1.0.
- Base variable contribution: \(B_i=w_i S_i C_i\).
- Layer score is normalized to [-1,+1].
- Layer weights are horizon-specific and sum to 1.0 for each horizon.
- Net Index is the single combined directional-conviction score in [-1,+1].
- Net Index must remain transparent and is not to be replaced by a black-box model.

## Interaction/dependency rules
- Three relationship classes: duplicate information; causal transmission; genuine interaction.
- Duplication and transmission are treated as effective-weight/dependency adjustments; genuine interaction is represented by an explicit interaction term where justified.
- Statistical correlation alone does not prove causality.
- No ad-hoc weekly interaction adjustment is permitted outside the defined framework.
- Production coefficients/parameters are not assumed to be fixed by the illustrative examples; those examples are reference implementation anchors only.

## Three-state probability rules
- Final decision surface is three-state: Bullish / Consolidation / Bearish.
- Probabilities must be in [0,1] and sum to 1.
- Net Index controls directional balance between Bullish and Bearish.
- Range Propensity controls how much probability mass may be allocated to Consolidation.
- Range Propensity is a deterministic composite market-state indicator using approved observable variables; it is not a free-form AI opinion in the base implementation.
- Consolidation is horizon-specific; the consolidation band is not one fixed percentage for all horizons.
- Current proposed functional form: \(P(C)=a_h R_h\), \(D_h=1-P(C)\), \(Q_B=(S_{total}+1)/2\), \(Q_{Be}=1-Q_B\), \(P(B)=D_h Q_B\), \(P(Be)=D_h Q_{Be}\).
- The \(a_h\) horizon parameters remain to be fixed during probability-engine implementation.

## Variable admission rules
- A candidate must pass five criteria: causal relevance; incremental information; data/evidence reliability; operational feasibility; forecast-horizon relevance.
- During Phase 1, the baseline is the approved causal architecture plus other candidates under consideration; obvious redundancy must be checked.
- After Phase 1, new variables are evaluated against the approved registry.
- Variable admission changes the composition/weights inside a layer; it does not automatically change layer-level weights.
- New variables are admitted/research-only/rejected.

## AI evidence rules
- Required analytical record: variable ID; observation timestamp; evidence; assessment; stance; confidence; counter-evidence; fact-vs-interpretation boundary; source provenance.
- Confidence uses the fixed five-factor rubric in Spec D.
- Counter-evidence reduces confidence first; it does not mechanically flip stance.
- Insufficient evidence may produce stance 0.00, confidence <=0.20, status Insufficient evidence.
- AI agents may not change layers, create production variables outside Spec C, modify weights, manufacture historical data, hide counter-evidence, or convert speculation into fact.

## Historical-data governance
- Preserve observation date, publication/release date, retrieval date, source, revision status.
- Live weekly runs may use the full currently available information set, but all timestamps must be preserved.
- Do not reconstruct unavailable 1970s/etc. quantitative history using present-day AI judgment and treat it as historical data.
- Historical events are evidence/context/counterexamples, not automatic weight optimization.

## Agent governance
- Worker agent = one variable; responsible for implementation, tests, usage manual, handoff.
- Layer manager = integration, interface consistency, validation, within-layer governance.
- Workers do not change layer architecture or cross-layer weights.
- Rework should be delegated to new workers by the layer manager when needed.

## Scope constraints
- No automatic portfolio allocation.
- No automatic trading/execution.
- No multi-asset forecasting.
- No intraday trading engine.
- No uncontrolled self-modifying weights.
- No unnecessary historical-news reconstruction.
- Do not expand scope merely because a feature is interesting.


# 3. NEXT STEPS

## Immediate micro-tasks
- **Phase 1: Build the Gold Variable Registry.** This is the next actual implementation phase.
- Populate every candidate variable under the 12 locked layers.
- Apply Spec C admission criteria to each candidate.
- For each admitted/conditional variable capture: ID, layer, mechanism, direction, incremental information, overlap, source, reliability, historical depth, frequency, freshness, accessibility, operational burden, horizon relevance, initial weight rationale, evidence references, decision, review date, reviewer.
- Identify obvious redundancy among Phase-1 candidates before finalizing the registry.
- Preserve Layer 1/Layer 2/other relationships for later Spec A dependency treatment; do not prematurely collapse variables.
- Identify candidate deterministic inputs for Range Propensity during the registry build.
- Keep the registry finite and purpose-driven; reject variables that do not materially help represent a layer/horizon.

## Pending dependencies by later phase
- **Before Phase 2:** Phase-1 registry must be accepted.
- **Before Phase 3:** Spec D confidence rubric is already documented; implement it exactly rather than inventing a new confidence method.
- **Before Phase 4:** Spec A numerical example is already documented; implementation must follow its architecture and use actual registry variables to instantiate production parameters.
- **Before Phase 5:** Spec B Range Propensity inputs, consolidation-band thresholds, and horizon parameters must be finalized using the Phase-1 approved variables; the functional form is already selected.
- **Before Phase 6:** End-to-end weekly pipeline, probability validity checks, evidence provenance, and archival must be tested.
- **Before Phase 7:** Forecast history must exist; weight-refinement proposals should not be generated from isolated forecast errors.

## Agent delegation next
- Use specialist research worker agents to populate variable candidates by layer.
- Use a layer manager per layer to resolve overlap, admission status, implementation ownership, and within-layer weight proposals.
- Release accepted workers; create replacement workers only for explicit rework.


# 4. LESSONS

- **Problem:** Initial seven-layer research taxonomy mixed causal drivers, transmission variables, amplifiers, and symptoms.
  - **Fix:** 12-layer causal-family model plus explicit driver/transmission/flow/amplifier distinctions.
- **Problem:** Gold was initially treated too much like a conventional commodity.
  - **Fix:** Layer 0 explicitly recognizes the enormous above-ground stock and marginal holder behavior.
- **Problem:** “Central-bank buying = de-dollarization” was too compressed.
  - **Fix:** Separate official reserve allocation, reserve diversification, sanctions/reserve-security effects, and monetary fragmentation.
- **Problem:** Historical backtesting was initially considered too broadly despite poor historical availability of several layers.
  - **Fix:** Historical events are evidence/context; quantitative backtesting is not required as the mechanism for setting initial weights.
- **Problem:** AI qualitative assessment risked becoming opaque opinion.
  - **Fix:** Spec D requires evidence, confidence, counter-evidence, provenance, timestamps, and fact/interpretation separation.
- **Problem:** Free-form AI confidence would be inconsistent.
  - **Fix:** Spec D fixed five-factor confidence rubric + counter-evidence adjustment + insufficient-evidence override.
- **Problem:** Variable addition could cause scope creep.
  - **Fix:** Spec C five-criterion admission gate and three statuses: Admit / Conditional-Research Only / Reject.
- **Problem:** Variable admission baseline was ambiguous during initial registry construction.
  - **Fix:** During Phase 1, baseline = causal architecture + other candidates under consideration; after Phase 1, baseline = approved registry.
- **Problem:** Interaction handling was too vague.
  - **Fix:** Spec A separates duplicate information, causal transmission, and genuine interaction and gives a reference numerical example.
- **Problem:** Correlation was at risk of being treated as causality.
  - **Fix:** Correlation alone is not enough; classify mechanism and provenance before dependency adjustment.
- **Problem:** Binary probability output did not represent genuine consolidation.
  - **Fix:** Preserve Net Index, add three-state probabilities and deterministic Range Propensity.
- **Problem:** Range Propensity had initially been undefined.
  - **Fix:** Spec B defines it as a deterministic composite of approved range/volatility market-state variables.
- **Problem:** Probability mapping was deferred without a target functional form.
  - **Fix:** Spec B selects a transparent bounded functional form; horizon parameters remain implementation work.
- **Problem:** Spec A/B had duplicate section numbers during revisions.
  - **Fix:** Section numbering was verified and corrected in the final v2 files.
- **Critical pitfall:** Do not interpret illustrative numbers in Specs A/B/D as production parameters. They are implementation anchors only.
- **Critical pitfall:** Do not automatically modify weights after a single forecast miss. Diagnose signal, data, regime, interaction, and weight separately.
- **Critical pitfall:** Do not let worker agents alter cross-layer architecture.
- **Critical pitfall:** Do not manufacture unavailable historical quantitative observations.


# 5. ARTIFACTS

The following are the finalized phase artifacts to carry forward. They are included in full, untruncated, as the textual SSOT. Superseded drafts are intentionally excluded.


## GOLD PRICE CAUSAL MODEL V2.2 — SSOT conceptual framework

**Source file:** `gold_price_causal_model_v2_2.md`

```text
# Gold Price Causal Model v2.2

## A Reconciled Critical Review, Corrected Causal Architecture, and Research Blueprint

**Prepared:** August 16, 2026  
**Basis:** Original AI-agent research report supplied by the user, plus the review and research inputs developed in this analysis.

> **Version 2.2 correction note:** This revision incorporates the latest review by correcting the layer-numbering/content mismatch in v2.1, standardizing the causal-layer structure, and making explicit that the layers are analytical causal families—not independent predictors. The stock/flow architecture remains foundational Layer 0; geopolitics remains simplified into four transmission channels; provisional rankings remain hypotheses; quantitative methods remain future validation tools; and Bitcoin remains a research question rather than an established core driver.

---

# Executive Summary

Gold is simultaneously a commodity, a currency-priced asset, a monetary reserve asset, a financial instrument, and a cultural store of value. Its price therefore cannot be adequately explained by a single variable such as inflation, the Federal Funds Rate, the US dollar, or mine supply.

The original agent report provides a strong first-generation framework. It organizes gold-price drivers into seven layers:

1. Monetary and interest-rate policy
2. US-dollar dynamics
3. Inflation and purchasing-power risk
4. Central-bank and sovereign behavior
5. Geopolitical risk and safe-haven demand
6. Physical supply and demand
7. Market structure, speculative positioning, and behavioral factors

This framework is directionally sound and captures most of the major themes that professional gold analysis should consider. The original report also makes several particularly useful observations: real yields have historically been important; gold's relationship with inflation is less mechanical than the common "inflation hedge" narrative suggests; central-bank demand has become much more important since the Global Financial Crisis and especially since 2022; Asian physical demand behaves differently from Western investment demand; and positioning can amplify fundamental shocks.

However, the original report should be treated as **Version 1: a taxonomy and hypothesis-generation framework**, rather than a finished causal model. The main improvement required is to distinguish among:

- structural drivers of long-run equilibrium,
- cyclical drivers of medium-term trends,
- event-driven shocks,
- transmission variables,
- market amplifiers,
- coincident indicators,
- lagging indicators,
- and behavioral/reflexive feedback loops.

The key research question should therefore become:

> **Which marginal holder changes their willingness to own gold, why does that willingness change, and through what market mechanism does the change reach the clearing price?**

This document combines the original report with a substantially expanded framework. The proposed second-generation model contains **12 analytical layers: one foundational Layer 0 and eleven sequential causal families (Layers 1–11)**. These layers are not independent predictors. They are interacting mechanisms through which macroeconomic conditions, official-sector behavior, physical demand, financial flows, market structure, and expectations can alter the marginal willingness to own gold. A separate classification distinguishes primary drivers, transmission variables, amplifiers, coincident indicators, and lagging indicators.

A central conclusion is that the most useful model is not simply:

> Gold ↑ when rates ↓.

It is:

> **Gold responds to changes in the expected relative attractiveness of owning gold versus competing stores of value, with the resulting move amplified or dampened by currency movements, liquidity, official-sector demand, investment flows, physical-market conditions, derivatives positioning, and expectations.**

The current 2022–2026 period should be studied as a potential regime change rather than assumed to be a simple continuation of the historical real-yield model.

---

# Part I — What the Original Agent Report Gets Right

## 1. Gold is multi-dimensional

The original report correctly states that gold is priced simultaneously as a commodity, currency, monetary reserve asset, and cultural/emotional store of value. This is an excellent starting point because it prevents an overly narrow macroeconomic interpretation.

The report also correctly distinguishes between:

### Structural / slow-moving forces

These include:

- central-bank reserve policy,
- real-rate regimes,
- monetary confidence and reserve diversification,
- mine-supply constraints.

### Cyclical / fast-moving forces

These include:

- FOMC meetings,
- US dollar movements,
- geopolitical shocks,
- inflation-data surprises,
- ETF flows,
- speculative futures positioning,
- seasonal demand.

The report adds a third layer—individual, behavioral, and cultural demand—which is also useful.

**Assessment:** Keep this structure, but make the time-horizon distinction more rigorous and add a separate distinction between causes and amplifiers.

---

# Part II — Critical Review of the Seven-Layer Model

## 2. Monetary policy and real interest rates

The original report identifies real rates as the traditional core economic driver. It explains the basic mechanism correctly: gold has no coupon or dividend, so the opportunity cost of holding gold changes when real yields change.

The report also cites the historical negative relationship between gold and 10-year TIPS yields and correctly emphasizes that the relationship has weakened substantially since 2022.

### Important improvement

Do not treat the real-yield relationship as a permanent law. Instead ask:

> **Under what regimes is the gold/real-yield relationship strong, weak, or reversed?**

For example:

| Regime | Real yields rising | Potential gold response |
|---|---:|---|
| Normal monetary regime | Yes | Usually negative |
| Inflation shock | Yes | Ambiguous |
| Banking/financial crisis | Yes | Can be positive |
| Geopolitical crisis | Yes | Can be positive |
| Sovereign-confidence crisis | Yes | Can be positive |
| Strong USD liquidity squeeze | Yes | Usually negative |
| Central-bank accumulation regime | Yes | Potentially muted |
| Fiscal-dominance regime | Yes | Potentially ambiguous |

The critical variable is therefore not simply the current real yield. It is the **expected future real return on competing assets** and the change in that expectation.

### Stronger formulation

Instead of:

> Gold falls when rates rise.

Use:

> **Gold tends to weaken when the expected real return on competing high-quality assets rises relative to the expected return from holding gold, all else equal.**

---

## 3. The US dollar

The original report correctly identifies the inverse relationship between gold and the dollar.

However, the USD should be treated as more than a mechanical pricing denominator.

The dollar affects gold through at least four channels:

1. **Mechanical translation:** gold is quoted in USD.
2. **Relative purchasing power:** USD strength makes dollar-priced gold more expensive for non-US buyers.
3. **US monetary policy:** policy expectations influence both USD and real yields.
4. **Global dollar liquidity:** funding stress can cause investors to liquidate gold in order to obtain USD cash.

Therefore DXY should not be treated as an independent causal variable in every episode. It may be an intermediate transmission variable reflecting monetary and global-liquidity conditions.

---

## 4. Inflation and purchasing-power risk

One of the strongest parts of the original report is its challenge to the simplistic statement that gold is mechanically an inflation hedge.

The better conceptual model is:

**Inflation shock → expectations of monetary response → real rates / USD → gold**

and simultaneously:

**Inflation shock → loss of purchasing-power confidence → gold demand**

These two channels can point in opposite directions.

A high CPI print can therefore be bearish for gold if it causes markets to expect much tighter real monetary policy. The same CPI print can become bullish if markets interpret it primarily as evidence of persistent currency debasement or policy credibility deterioration.

### New research requirement

Always distinguish:

- inflation level,
- inflation change,
- inflation surprise relative to consensus,
- inflation expectations,
- central-bank reaction function,
- fiscal credibility.

The CPI number alone is insufficient.

---

## 5. Central-bank and sovereign behavior

The original report is correct that official-sector demand is one of the defining structural features of the current cycle.

The World Gold Council's published data support the importance of continued central-bank demand in the 2020s. The report cites 2026 Q1 official-sector buying of approximately 244 tonnes, consistent with the published Q1 data.

### Important qualification

The statement that central-bank buying is "price-insensitive" is useful as a first approximation but too absolute for an institutional-quality model. Official buyers may be less short-term price-sensitive than speculators, but they can still react to valuations and reserve-allocation objectives.

A better research formulation is:

> **Central-bank demand is generally more strategic and longer-horizon than private investment demand, but it is not necessarily price-independent.**

### Separate five concepts

Do not automatically equate:

- gold accumulation,
- de-dollarization,
- reserve diversification,
- sanctions-risk hedging,
- monetary-system fragmentation.

They overlap but are not identical.

A central bank may buy gold because it wants greater reserve diversification without intending to abandon the dollar. Conversely, a country can reduce USD exposure by purchasing another currency rather than gold.

---

## 6. Geopolitical risk

The original report appropriately identifies geopolitical risk as a major safe-haven channel and lists numerous historical events.

But "geopolitical risk" is too broad to be a single explanatory variable.

Break it into:

- active conflict,
- probability of escalation,
- sanctions risk,
- reserve-security risk,
- financial-system fragmentation,
- energy-supply disruption,
- shipping disruption,
- sovereign-asset seizure risk,
- confidence in the international monetary system.

This matters because different geopolitical events affect gold through different mechanisms.

For example:

**Conflict → safe-haven demand**

versus

**Conflict → oil ↑ → inflation expectations ↑ → expected Fed tightening ↑ → real yields ↑ → gold ↓**

The two channels can offset one another.

---

## 7. Physical supply and demand

The original report correctly explains that mine production is slow to adjust and that recycling is more price-responsive.

However, gold requires special treatment because of the enormous stock of existing above-ground gold.

### Critical conceptual upgrade

For many commodities:

> annual production and annual consumption dominate price formation.

For gold:

> **the willingness of existing owners to hold or liquidate the existing stock is often more important than annual mine production.**

Therefore the research should distinguish:

### Flow supply

- mine production,
- recycling,
- producer hedging.

### Stock ownership

- central banks,
- households,
- jewelry holders,
- ETFs,
- investment funds,
- bullion banks,
- sovereign entities.

The research question becomes:

> **Who owns the existing gold stock, and under what conditions do they become marginal sellers?**

This is a major improvement over a conventional commodity-market model.

---

## 8. Market structure, positioning, and behavior

The original report is right to include COMEX positioning, ETF flows, retail psychology, and cultural demand.

But market structure should be expanded into a dedicated financial-market layer.

Important variables include:

- COMEX open interest,
- managed-money positioning,
- dealer positioning,
- futures basis,
- options skew,
- gamma exposure,
- CTA trend positioning,
- ETF creation/redemption,
- London OTC liquidity,
- Shanghai premium/discount,
- COMEX warehouse inventories,
- margin requirements,
- forced liquidation.

These are often **amplifiers rather than original causes**.

For example:

> Fed surprise → gold fundamental repricing → heavily long futures market liquidates → CTA selling → stop-losses → ETF outflows → larger gold decline.

The futures liquidation did not necessarily cause the original shock. It amplified it.

---

# Part III — The Revised 12-Layer Gold Price Causal Model

The following architecture contains **one foundational stock/flow layer plus eleven sequential causal layers**. The layers should not be read as twelve independent explanatory variables. A single shock may pass through several layers—for example, a change in Fed expectations can affect real yields, the dollar, liquidity, ETF flows, and derivatives positioning in sequence.

For consistency, every layer is described using the same analytical fields:

- **What it is** — the economic or market phenomenon.
- **Primary mechanism** — why it can affect gold.
- **Key observables** — variables that can be monitored.
- **Typical horizon** — the time scale on which the mechanism is most relevant.
- **Interaction note** — the main ways it can reinforce or offset other layers.

---

## Layer 0 — Gold's Stock/Flow Monetary Architecture

### What it is

Gold is unusual because almost all previously mined gold still exists. The existing above-ground stock is therefore far larger than annual new mine production.

### Primary mechanism

For gold, price formation depends heavily on the willingness of existing holders to buy, hold, or sell the existing stock. Annual mine supply matters, but the marginal willingness of current owners to release gold into the market can matter even more.

### Key observables

- approximate above-ground stock,
- central-bank holdings,
- ETF holdings,
- household/jewelry holdings,
- bar-and-coin ownership,
- vaulted versus potentially mobile holdings,
- recycling flows,
- producer hedging,
- gold-collateral activity where observable.

### Typical horizon

Years to decades for ownership structure; days to months when stock becomes active through selling or recycling.

### Interaction note

This layer changes how every supply/demand statistic should be interpreted. A 2% change in mine supply is not equivalent to a 2% change in the willingness of a huge stock of existing holders to sell.

---

## Layer 1 — Real Interest Rates and Opportunity Cost

### What it is

The expected real return available from competing assets, especially high-quality fixed-income instruments.

### Primary mechanism

Gold has no coupon or dividend. When the expected real return on competing assets rises, the opportunity cost of holding gold generally rises; when it falls, gold becomes relatively more attractive.

### Key observables

- 10Y TIPS yield,
- 5Y TIPS yield,
- forward real rates,
- real yield curve,
- term premium,
- expected policy rate.

### Typical horizon

Intraday to multi-year.

### Interaction note

The relationship is regime-dependent. Geopolitical stress, banking crises, reserve accumulation, or fiscal-confidence shocks can cause gold and real yields to rise together temporarily.

### Stronger formulation

> **Gold tends to weaken when the expected real return on competing high-quality assets rises relative to the expected return from holding gold, all else equal.**

---

## Layer 2 — US Dollar and Global FX Regime

### What it is

The value of the US dollar relative to major and emerging-market currencies and the availability of dollar funding.

### Primary mechanism

A stronger dollar raises the local-currency price of dollar-denominated gold for many non-US buyers. The dollar also transmits US monetary policy and global funding conditions.

### Key observables

- DXY,
- EUR/USD,
- USD/JPY,
- USD/CNY,
- emerging-market FX stress,
- cross-currency basis,
- broad dollar funding indicators.

### Typical horizon

Intraday to multi-year.

### Interaction note

DXY is not always an independent cause. It may be downstream from Fed expectations, real yields, or global dollar liquidity.

---

## Layer 3 — Monetary Policy Expectations

### What it is

The market's expected path for future central-bank policy rather than simply the current policy rate.

### Primary mechanism

Gold reacts strongly to revisions in the expected future path of real policy rates and liquidity conditions. A central bank can leave rates unchanged while gold rallies because the expected future path becomes more dovish.

### Key observables

- Fed Funds futures,
- OIS curves,
- dot plots,
- FOMC statements,
- speeches,
- terminal-rate expectations,
- probability distributions around future meetings.

### Typical horizon

Minutes to years, with the strongest effect around policy and macro-data events.

### Interaction note

Policy expectations often transmit through Layer 1 (real yields), Layer 2 (USD), Layer 7 (liquidity), and Layer 8 (investment flows). These should not be double-counted as independent shocks.

### Core principle

> **Gold responds to changes in expectations, not merely changes in current policy.**

---

## Layer 4 — Inflation, Purchasing Power, and Fiscal Credibility

### What it is

The credibility of fiat purchasing power and the sustainability of sovereign fiscal policy.

### Primary mechanism

Inflation can increase gold demand as a purchasing-power hedge, but the policy response to inflation can push real yields higher and weigh on gold. Fiscal deterioration can also increase longer-term concerns about currency debasement or sovereign debt sustainability.

### Key observables

**Inflation quantity**
- CPI,
- core CPI,
- PCE,
- core PCE.

**Inflation expectations**
- 5Y/10Y breakevens,
- inflation swaps,
- survey expectations.

**Fiscal credibility**
- fiscal deficit/GDP,
- debt/GDP,
- interest expense/revenue,
- Treasury issuance,
- maturity structure,
- term-premium indicators.

### Typical horizon

Months to decades, with inflation surprises creating much faster short-term moves.

### Interaction note

The same inflation shock can be bullish or bearish for gold depending on whether the dominant response is (a) higher inflation/fiat-confidence risk or (b) tighter real monetary policy.

### Important distinction

Do not equate:

> **high inflation**

with:

> **bullish gold**

without considering the expected policy response and change in real yields.

---

## Layer 5 — Official-Sector Reserve Allocation

### What it is

How central banks and other official-sector institutions allocate reserves among gold, USD assets, other currencies, and other reserve instruments.

### Primary mechanism

Strategic reserve allocation can create persistent demand for gold that is longer-horizon and generally less tactical than speculative investment demand.

### Key observables

- monthly/quarterly official-sector gold purchases,
- gold share of reserves,
- reserve composition changes,
- stated reserve objectives,
- central-bank survey responses,
- domestic versus foreign gold custody,
- official-sector sales or lending where disclosed.

### Typical horizon

Years to decades, with occasional monthly/quarterly effects.

### Interaction note

Separate:

- physical gold accumulation,
- reserve diversification,
- de-dollarization,
- sanctions-risk hedging,
- reserve-security concerns,
- monetary-system fragmentation.

These concepts overlap but are not interchangeable.

### Important qualification

Central-bank demand is often more strategic and longer-horizon than private investment demand, but it should not be assumed to be completely price-insensitive.

---

## Layer 6 — Geopolitical Transmission Channels

### What it is

Geopolitical events and international-system changes that affect gold through several distinct channels.

### Primary mechanism

Rather than treating geopolitical risk as one variable, analyze four main transmission channels:

#### A. Safe-haven channel

Fear and uncertainty increase demand for liquid, non-sovereign stores of value.

#### B. Energy / inflation channel

Conflict can disrupt energy or shipping supply, increasing oil prices and changing inflation and monetary-policy expectations.

#### C. Reserve-security channel

Sanctions, reserve freezes, or concerns about access to foreign assets can change official reserve preferences.

#### D. Monetary-system fragmentation channel

Geopolitical fragmentation can encourage diversification away from dependence on a single reserve currency or payment system.

### Key observables

- active conflict and escalation headlines,
- sanctions announcements,
- oil and shipping disruptions,
- geopolitical-risk indices where available,
- reserve-security policy changes,
- sanctions exposure,
- international monetary-system developments.

### Typical horizon

Intraday to decades.

### Interaction note

The four channels can reinforce or offset each other. A conflict can be bullish for gold through safe-haven demand but bearish through higher oil prices and tighter expected monetary policy.

---

## Layer 7 — Global Liquidity and Financial Conditions

### What it is

The availability of financial liquidity, credit, and balance-sheet capacity across the global system.

### Primary mechanism

Liquidity affects both the willingness to own gold and the ability to finance positions. During acute crises, gold can initially be sold to raise cash even when its longer-term fundamental case is improving.

### Key observables

- Fed balance sheet,
- ECB balance sheet,
- PBoC liquidity,
- global M2,
- bank credit,
- credit spreads,
- repo conditions,
- SOFR,
- Treasury General Account,
- reverse-repo balances,
- global financial-conditions indices,
- cross-border capital flows.

### Typical horizon

Days to years.

### Interaction note

The effect of rates cannot be interpreted independently of liquidity. High rates with abundant liquidity are not equivalent to high rates during a funding squeeze.

---

## Layer 8 — Investment Flows

### What it is

Actual capital allocation into and out of gold investment products and financial exposures.

### Primary mechanism

Investment flows can become the marginal price-setting force over short and medium horizons, particularly when flows enter highly liquid ETFs or derivatives-linked strategies.

### Key observables

- gold ETF inflows/outflows,
- institutional fund allocations,
- pension and mutual-fund exposure,
- bar-and-coin investment,
- large fund positioning,
- retail investment flows.

### Typical horizon

Days to quarters.

### Interaction note

Not every demand category has equal price impact. A key research task is to identify which flow categories are genuinely marginal at each horizon.

---

## Layer 9 — Regional Physical-Market Dynamics

### What it is

The regional systems through which households, institutions, importers, exchanges, and local financial markets interact with physical gold.

### Primary mechanism

Regional physical demand can create local premiums/discounts, alter import flows, change recycling incentives, and influence the marginal physical buyer or seller.

### China — key observables

- Shanghai Gold Exchange premium/discount,
- Chinese gold ETF flows,
- PBoC holdings,
- household investment demand,
- RMB performance,
- local interest rates,
- property-market confidence,
- capital controls.

### India — key observables

- INR/USD,
- domestic gold price,
- import duties,
- rural income,
- agricultural conditions,
- wedding calendar,
- Diwali and Akshaya Tritiya,
- local premiums,
- recycling,
- gold-loan activity.

### Typical horizon

Weeks to years, with strong seasonal components.

### Interaction note

Regional physical demand should be treated as a subsystem, not merely another row in a global demand table. Local physical conditions can feed into global flows, premiums, and inventories.

---

## Layer 10 — Market Microstructure and Derivatives

### What it is

The financial-market plumbing through which gold exposure is leveraged, hedged, financed, and mechanically traded.

### Primary mechanism

Microstructure determines how strongly a fundamental shock is transmitted into price. The same macro shock can produce a small move in one positioning environment and a much larger move during a crowded or illiquid market.

### Key observables

- COMEX futures open interest,
- CFTC COT positioning,
- managed-money net length,
- commercial positioning,
- options open interest,
- call/put skew,
- dealer gamma,
- futures basis,
- warehouse stocks,
- margin changes,
- CTA/systematic trend positioning,
- algorithmic flow proxies,
- gold lease/forward indicators where available.

### Typical horizon

Minutes to weeks.

### Interaction note

Positioning should usually be treated as an **amplifier or transmission mechanism**, not automatically as an independent fundamental driver.

---

## Layer 11 — Expectations, Psychology, and Reflexivity

### What it is

The interaction between price, narrative, expectations, and future flows.

### Primary mechanism

Gold price can influence future demand, meaning price is not only an outcome of fundamentals but can become an input into the next round of flows.

Example:

> Gold ↑ → media attention ↑ → retail interest ↑ → ETF flows ↑ → futures positioning ↑ → momentum buying ↑ → Gold ↑

The reverse loop can operate during liquidation.

### Key observables

- Google Trends,
- financial-media mentions,
- retail bar/coin demand,
- ETF flows,
- options activity,
- search intensity for gold-related terms,
- sentiment surveys,
- momentum/trend signals.

### Typical horizon

Days to years.

### Interaction note

Reflexivity can amplify a genuine fundamental shock, create overshoots, or temporarily sustain prices beyond what traditional valuation relationships would imply.

---

## Cross-Layer Principle: The Layers Are Not Independent Predictors

The twelve layers are an **analytical architecture**, not a twelve-factor regression model.

A single shock may propagate through several layers:

> FOMC expectation change → real yields → USD → ETF flows → futures positioning → gold price → narrative → further flows.

Therefore the next research phase must explicitly distinguish:

- **primary shock / driver**
- **transmission variable**
- **flow response**
- **market amplifier**
- **coincident indicator**
- **lagging indicator**
- **reflexive feedback**

This prevents double-counting the same underlying shock as multiple independent gold-price drivers.

---

# Part IV — Primary Drivers vs Transmission Variables vs Amplifiers

This distinction should become mandatory in future research.

## Primary drivers

Examples:

- monetary regime,
- fiscal credibility,
- reserve policy,
- geopolitical regime,
- global liquidity.

## Transmission variables

Examples:

- real yields,
- DXY,
- inflation expectations,
- Treasury term premium,
- credit spreads.

## Market amplifiers

Examples:

- futures liquidation,
- CTAs,
- options gamma,
- ETF flows,
- stop-loss orders.

## Coincident indicators

Examples:

- spot price momentum,
- volatility,
- intraday volume.

## Lagging indicators

Examples:

- jewelry demand,
- annual mine production,
- some central-bank disclosures.

This classification prevents correlation from being mistaken for causality.

---

# Part V — Historical Regime Framework

The original report's historical chronology is useful and should be retained, but upgraded from narrative description to event-study analysis.

## 1944–1971 — Bretton Woods

Gold was fixed at $35/oz under the Bretton Woods monetary system.

Key lesson:

> Gold price formation was constrained by the monetary regime itself.

---

## 1971–1980 — Monetary regime break and stagflation

Key events:

- Nixon Shock,
- end of dollar-gold convertibility,
- 1973 oil shock,
- 1979 Iranian Revolution,
- inflation acceleration,
- dollar-confidence deterioration,
- Soviet invasion of Afghanistan.

Key lesson:

> Gold can experience extraordinary upside when monetary regime credibility, purchasing power, and geopolitical risk deteriorate simultaneously.

---

## 1980–1999 — Volcker and disinflation

The key feature was not simply declining inflation.

The more important mechanism was:

> credible monetary tightening → positive real returns → restoration of confidence in fiat money and bonds → lower gold attractiveness.

This is an essential control case for the research model.

---

## 2001–2011 — Post-dot-com, 9/11, GFC, sovereign crisis

Key themes:

- falling real yields,
- monetary easing,
- geopolitical uncertainty,
- financial-system instability,
- increasing official-sector interest in gold.

The GFC is especially important because gold initially faced liquidation pressure and subsequently benefited from the monetary response.

This demonstrates the need to distinguish **shock phase** from **policy-response phase**.

---

## 2011–2015 — Gold correction

Key factors:

- improving US growth expectations,
- stronger dollar,
- less aggressive monetary easing,
- higher real-rate expectations,
- weakening investment enthusiasm.

This is useful as a historical control regime against the current bull market.

---

## 2015–2020 — Recovery and pandemic

Key drivers:

- renewed monetary easing,
- low/negative real rates,
- fiscal expansion,
- QE,
- ETF accumulation,
- COVID uncertainty.

The pandemic period demonstrates how monetary and fiscal policy can interact with safe-haven demand.

---

## 2022–2026 — Potential new structural regime

The original report identifies:

- central-bank accumulation,
- reserve diversification,
- sanctions concerns,
- fiscal deficits,
- geopolitical fragmentation,
- sticky inflation risk,
- periods of rising real yields alongside rising gold.

This period should be treated as an empirical test of whether the traditional real-yield framework has undergone a structural regime shift.

### Competing hypotheses

**H1 — Traditional model remains dominant**  
Real yields still ultimately determine gold, and central-bank demand is temporary noise.

**H2 — Official-sector demand has become co-dominant**  
Central-bank accumulation now materially changes the sensitivity of gold to real yields.

**H3 — Fiscal credibility has gained importance**  
Gold is increasingly responding to sovereign debt sustainability and debasement expectations.

**H4 — Global liquidity has become a stronger common factor**  
Gold increasingly responds to global liquidity conditions as a monetary asset.

**H5 — Reflexivity has increased**  
ETF flows, systematic positioning, and retail momentum amplify price moves sufficiently to change short-run market behavior.

These hypotheses should be formally tested.

---

# Part VI — Key Missing Factors Added to the Original Research

## 1. Global liquidity

Add:

- central-bank balance sheets,
- global M2,
- bank credit,
- financial conditions,
- repo,
- cross-border capital flows.

## 2. Gold as collateral

Investigate:

- gold lease rates,
- forwards,
- swaps,
- bullion-bank financing,
- collateral use,
- London OTC market structure.

## 3. Shanghai premium

A potentially useful high-frequency proxy for Chinese physical demand and local supply tightness.

## 4. Gold vs Bitcoin

Investigate whether Bitcoin is:

- substitute,
- complement,
- or unrelated.

This should be studied especially by investor cohort and liquidity regime.

## 5. Equities and credit

Add:

- S&P 500,
- Nasdaq,
- VIX,
- investment-grade spreads,
- high-yield spreads,
- bank equities.

Gold behaves differently during ordinary risk-off events versus true liquidity crises.

## 6. Oil as an intermediate variable

Oil can be bullish or bearish for gold depending on whether the dominant channel is:

- geopolitical risk,
- inflation,
- or monetary-policy expectations.

---

# Part VII — The Marginal Buyer/Seller Framework

The most useful microeconomic question is:

> **Who is the marginal buyer or seller at a particular moment?**

Potential marginal participants include:

- central banks,
- sovereign wealth funds,
- macro hedge funds,
- CTA/systematic funds,
- bullion banks,
- ETF investors,
- institutional allocators,
- Chinese households,
- Indian households,
- retail investors,
- jewelry consumers.

Each has a different:

- time horizon,
- price sensitivity,
- liquidity need,
- strategic objective,
- currency exposure,
- risk tolerance.

The gold price changes when the willingness of the marginal buyer and marginal seller changes.

This provides a better organizing principle than simply saying that “demand increased.”

---

# Part VIII — What Matters at Each Time Horizon?

## Intraday

Likely dominant variables:

1. US macro-data surprises
2. Fed expectations
3. Treasury yields
4. DXY
5. geopolitical headlines
6. futures/options positioning
7. liquidity
8. algorithmic flows

## 1–5 days

Likely dominant variables:

1. expected Fed path
2. real yields
3. DXY
4. geopolitical developments
5. ETF flows
6. futures positioning
7. oil
8. technical positioning

## 1–3 months

Likely dominant variables:

1. monetary-policy regime
2. real yields
3. USD trend
4. ETF flows
5. central-bank demand
6. geopolitical regime
7. inflation expectations
8. physical demand

## 1–5 years

Likely dominant variables:

1. monetary regime
2. fiscal credibility
3. reserve diversification
4. central-bank accumulation
5. global wealth and liquidity
6. geopolitical fragmentation
7. real-rate regime
8. supply constraints

## 5–30 years

Likely dominant variables:

1. global monetary architecture
2. reserve composition
3. sovereign fiscal credibility
4. global wealth
5. above-ground gold stock
6. demographic and cultural demand
7. financial-system architecture

---

# Part IX — Provisional Driver Hypotheses (Not Empirical Weights)

The table below is a **working research hypothesis**, not a statistically estimated scorecard. The labels are intended to organize the research agenda and prevent false precision. Final signs, importance, and confidence should be established through historical testing.

| Variable | Hypothesized Direction | Provisional Importance | Typical Speed | Evidence Status | Main Mechanism |
|---|---|---|---|---|---|
| 10Y real yield | Negative | Very high | Fast | Strong historical evidence, regime-dependent | Opportunity cost |
| Fed / policy expectations | Negative | Very high | Very fast | Strong mechanism | Expected future real rates |
| DXY / global USD regime | Negative | High | Fast | Strong historical relationship, partly downstream | Currency valuation / liquidity |
| Central-bank demand | Positive | High structural | Slow | Strong recent evidence | Reserve allocation |
| Fiscal credibility | Negative when credibility improves | High long term | Slow | Important hypothesis | Monetary/fiscal confidence |
| Geopolitical risk | Usually positive, channel-dependent | Medium/High | Fast | Strong historical precedent | Safe haven / fragmentation |
| Global liquidity | Usually positive | High | Medium | Important but regime-dependent | Availability of capital |
| ETF / investment flows | Positive | High short-medium term | Fast | Strong flow-price relationship | Marginal investment demand |
| COMEX / options positioning | Nonlinear | High as amplifier | Very fast | Strong microstructure rationale | Amplification / liquidation |
| Shanghai premium | Positive | Medium | Fast | Useful regional indicator | Physical tightness |
| Oil | Ambiguous | Medium | Fast | Dual-channel mechanism | Inflation + geopolitics |
| Jewelry demand | Positive | Low/Medium | Slow | Strong physical-market evidence | Consumption / recycling reservoir |
| Mine production | Negative for price at the margin | Low short term / higher structural | Very slow | Strong supply constraint evidence | Physical supply |
| Bitcoin flows | Ambiguous | Low / research question | Fast | Hypothesis only | Capital substitution / complementarity |

**Important:** “Importance” here means *research priority*, not measured causal contribution. No numerical weighting should be used in trading decisions until the proposed historical and quantitative tests have been completed.

## Scope Clarification

The methodology in this section is a **proposed validation program**, not evidence that these statistical tests have already been run. The current document distinguishes three categories: (1) evidence-supported observations drawn from the supplied report and cited external sources, (2) explicit hypotheses, and (3) proposed methods for testing those hypotheses.

# Part X — Research Methodology

## Stage 1 — Build the variable universe

Create a database of approximately 50–100 candidate explanatory variables.

Each variable should have:

- definition,
- source,
- frequency,
- time horizon,
- expected sign,
- causal mechanism,
- data quality,
- known limitations.

---

## Stage 2 — Historical event study

For major events from 1971–2026, measure gold's response at:

- 1 day,
- 1 week,
- 1 month,
- 3 months,
- 6 months,
- 1 year.

Compare simultaneously with:

- real yields,
- nominal yields,
- DXY,
- oil,
- S&P 500,
- VIX,
- inflation expectations,
- ETF flows,
- futures positioning.

The goal is to determine the transmission mechanism, not merely the correlation.

---

## Stage 3 — Quantitative testing

Potential methods:

- simple correlation,
- rolling correlation,
- multivariate regression,
- event studies,
- VAR models,
- regime-switching models,
- Granger-causality tests,
- principal-component analysis,
- nonlinear models.

Most importantly, estimate models separately for:

- intraday,
- daily,
- weekly,
- monthly,
- annual horizons.

A variable can be weak at one horizon and dominant at another.

---

## Stage 4 — Regime detection

Classify the market into regimes such as:

1. Disinflation
2. Inflation shock
3. Monetary easing
4. Monetary tightening
5. Financial crisis
6. Geopolitical crisis
7. Fiscal-confidence deterioration
8. Strong-USD liquidity squeeze
9. Central-bank accumulation regime
10. Speculative momentum regime

Then estimate gold's driver sensitivity separately for each regime.

---

## Stage 5 — Current-regime analysis

The 2022–2026 period should be analyzed as a live experiment.

Questions:

- Has gold become structurally less sensitive to real yields?
- How much of the rally can be attributed to official-sector demand?
- Has fiscal credibility become more important?
- Has geopolitical fragmentation changed reserve behavior?
- How important are ETF flows relative to Asian physical demand?
- Has derivatives positioning amplified the trend?
- Is the relationship between gold and the dollar changing?

---

# Part XI — Verification Standards

The original report contains many precise 2026 figures. These should not all be treated as equally reliable.

Every quantitative claim should be assigned a source tier:

### Tier A — Primary source

Examples:

- World Gold Council,
- Federal Reserve,
- US Treasury,
- CFTC,
- IMF,
- ECB,
- PBoC,
- Shanghai Gold Exchange,
- LBMA,
- official national statistics.

### Tier B — High-quality secondary source

Examples:

- major investment banks,
- reputable market-data providers,
- established financial newspapers.

### Tier C — Analyst interpretation

Useful for hypotheses but not as authoritative factual evidence.

### Tier D — Speculative / unverified

Should be clearly labelled and never presented as established fact.

Particular claims in the original report that should receive source-level re-verification include:

- 2026 Q2 central-bank purchase totals,
- 2026 mine-production estimates,
- 2026 global AISC estimates,
- the claim that sovereign entities may absorb approximately 93% of new mine supply,
- unusually large COMEX far-out-of-the-money call concentrations,
- specific 2026 institutional price targets.

The original report itself states that its numbers are subject to revision, which is appropriate.

---

# Part XII — Practical Gold Monitoring Dashboard

A real-time dashboard should ultimately contain at least the following groups.

## Monetary

- 10Y TIPS
- 5Y TIPS
- Fed Funds futures
- OIS curve
- FOMC probability distribution

## Currency

- DXY
- EUR/USD
- USD/CNY
- EM FX index

## Inflation

- CPI
- Core CPI
- PCE
- Core PCE
- 5Y breakeven
- 10Y breakeven
- inflation swaps

## Fiscal

- deficit/GDP
- debt/GDP
- Treasury issuance
- interest expense/revenue
- term premium

## Central banks

- monthly gold purchases
- gold share of reserves
- reserve composition
- major buyer activity

## Geopolitics

- conflict intensity
- sanctions
- shipping disruption
- oil
- VIX
- geopolitical-risk measures

## Liquidity

- central-bank balance sheets
- global M2
- bank credit
- financial conditions
- repo stress
- credit spreads

## Flows

- GLD flow
- IAU flow
- major Asian ETF flows
- bar/coin demand
- institutional positioning

## Physical market

- Shanghai premium/discount
- India premium/discount
- COMEX stocks
- London physical indicators
- recycling

## Futures and options

- CFTC managed money
- commercial positioning
- open interest
- options skew
- gamma
- CTA positioning

## Behavioral

- Google Trends
- search intensity
- retail sentiment
- social-media activity
- financial-media intensity

---

# Part XIII — Core Hypotheses to Test

The final research should not simply collect evidence supporting a preferred narrative. It should test competing hypotheses.

## Hypothesis 1 — Real-rate dominance

Gold remains fundamentally anchored to the expected real return on US Treasury assets.

## Hypothesis 2 — Official-sector regime shift

Central-bank accumulation has structurally reduced gold's sensitivity to real yields.

## Hypothesis 3 — Fiscal dominance

Markets increasingly use gold as protection against sovereign debt sustainability and monetary/fiscal credibility risk.

## Hypothesis 4 — Fragmentation premium

Geopolitical fragmentation and sanctions have created a durable reserve-demand premium for gold.

## Hypothesis 5 — Global-liquidity sensitivity

Gold is increasingly sensitive to global liquidity conditions, not only US monetary policy.

## Hypothesis 6 — Reflexivity

Investment flows and derivatives positioning amplify fundamental price movements enough to materially alter short-run price behavior.

## Hypothesis 7 — Regional substitution

Asian physical demand increasingly offsets the cyclical weakness of Western financial demand.

## Hypothesis 8 — Gold/BTC capital competition

Bitcoin may absorb some marginal investment demand that could otherwise enter gold, or the two assets may sometimes act as complements. This is a **research question, not an established gold-price driver**. The relationship should be tested by regime, liquidity condition, and investor cohort.

---

# Part XIV — The Ultimate Causal Architecture

```text
                         GLOBAL REGIME
                              |
           +------------------+------------------+
           |                  |                  |
      Monetary regime    Fiscal regime    Geopolitical regime
           |                  |                  |
           v                  v                  v
       Real rates       Sovereign risk     Safe-haven demand
           |                  |                  |
           +---------+--------+------------------+
                     |
                     v
                USD / FX regime
                     |
                     v
        RELATIVE GOLD ATTRACTIVENESS
                     |
          +----------+----------+
          |          |          |
          v          v          v
      ETF flows  Central banks  Physical demand
          |          |          |
          +----------+----------+
                     |
                     v
            MARKET POSITIONING
                     |
             +-------+-------+
             |       |       |
             v       v       v
          Futures  Options  CTAs
             |       |       |
             +-------+-------+
                     |
                     v
                 GOLD PRICE
                     |
                     v
          EXPECTATIONS / NARRATIVE
                     |
                     +-------------------------->
                              feedback into flows
```

This architecture captures an important principle:

> **Gold price is simultaneously an outcome of fundamentals and an input into future expectations and flows.**

---

# Part XV — Revised Assessment of the Original Agent Report

| Dimension | Assessment |
|---|---:|
| Conceptual framework | 8/10 |
| Breadth | 8.5/10 |
| Historical coverage | 7.5/10 |
| Current-market coverage | 8/10 |
| Causal rigor | 6/10 |
| Quantitative rigor | 5/10 |
| Source verification | 6/10 |
| Trading usefulness | 6.5/10 |
| Potential after restructuring | 9.5/10 |

The report should therefore be regarded as a **strong foundation, not a finished institutional model**.

---

# Part XV-A — Version 2.2 Reconciliation: What We Correct, What We Keep, What We Change

The latest AI-agent feedback identifies a mechanical layer-numbering/content mismatch in v2.1. That error is corrected here. The following principles are now explicit:

1. **Keep the stock/flow insight.** Gold's very large existing stock means marginal holder behavior matters at least as much as annual mine production for understanding price formation.

2. **Keep the cause/transmission/amplifier distinction.** DXY, ETF flows, futures positioning, and other market variables should not automatically be treated as independent causes.

3. **Separate official-sector behaviors.** Central-bank gold accumulation, de-dollarization, reserve diversification, sanctions hedging, and monetary fragmentation are related but distinct hypotheses.

4. **Keep global liquidity.** It is necessary to explain crisis episodes in which gold initially falls because of forced cash demand before later benefiting from monetary easing.

5. **Keep oil as a dual-channel variable.** Oil can be bearish for gold through tighter monetary expectations and bullish through geopolitical stress; the net effect is regime-dependent.

6. **Simplify geopolitics.** Use the four transmission channels—safe haven, energy/inflation, reserve security, and monetary fragmentation—instead of treating every geopolitical concept as a separate measurable variable.

7. **Demote subjective rankings.** Any importance or confidence score in this document is provisional research judgment, not an empirical result.

8. **Separate research design from findings.** VARs, Granger causality, PCA, regime-switching models, and other advanced methods are future validation tools, not conclusions already established by this document.

9. **Keep the causal diagram as a conceptual map.** Its purpose is to prevent double-counting and clarify transmission pathways, not to claim an empirically estimated structural model.

10. **Keep Bitcoin as a hypothesis only.** It is worth testing as a possible substitute/complement, but the current evidence here does not justify treating it as a core gold-price driver.

11. **Treat the layers as causal families, not independent variables.** A single macro or geopolitical shock may propagate through monetary expectations, real yields, the USD, liquidity, investment flows, and market positioning. The architecture exists to map transmission pathways and prevent double-counting.

12. **Standardize every layer.** Each layer should identify what it is, its primary mechanism, key observables, typical horizon, and interaction with other layers. This makes the framework usable as both a research reference and the eventual dashboard index.

# Part XVI — Final Conclusions

The original report's most important insight is that gold does not have one master variable. Its price emerges from interacting structural and cyclical forces.

The most important additions required for a second-generation model are:

1. **Gold's enormous existing stock and the behavior of existing holders**
2. **Expected future real rates rather than only current rates**
3. **Global liquidity and financial conditions**
4. **A sharper distinction between central-bank buying and de-dollarization**
5. **Fiscal credibility and sovereign-debt sustainability**
6. **Detailed gold-market microstructure**
7. **Shanghai and Indian physical-market signals**
8. **Derivatives, systematic positioning, and forced liquidation**
9. **Behavioral reflexivity**
10. **Separate analysis by investment horizon**

The deepest research question should be:

> **At any given time, what has changed the willingness of the marginal holder to own gold, what economic or geopolitical information caused that change, and through which financial-market mechanisms was the resulting imbalance transmitted into the price?**

That question is more powerful than simply asking which variables are correlated with gold.

It allows the research to separate:

- cause from consequence,
- fundamentals from positioning,
- structural demand from tactical flow,
- headline shocks from policy responses,
- and long-term valuation from short-term volatility.

The next stage should therefore be a **quantitative validation program**, built around historical event studies, regime analysis, a 50–100 variable database, and a live monitoring dashboard. The output should distinguish empirical findings from hypotheses and update the model as new evidence arrives. The final product should be capable of explaining not only **why gold has moved historically**, but also **which forces are dominant now, which are likely to dominate next, and which indicators would falsify the current market thesis**.

---

# Source and Evidence Note

This document incorporates and critiques the user-supplied AI-agent report, *What Moves the Price of Gold: A Comprehensive Framework of Deciding Factors*, compiled August 16, 2026. The supplied report contains its own source list, including the World Gold Council, J.P. Morgan Global Research, RBC Wealth Management, Metals Focus / Kitco, Erb & Harvey, and Federal Reserve historical material.

For quantitative implementation, the next research phase should prioritize primary-source datasets and explicitly record the source, publication date, methodology, and any revisions for every material number.

**Important:** This document is a research framework, not investment advice. Forecast ranges and empirical relationships should be treated as hypotheses to be tested rather than recommendations.
```


## GOLD PROBABILITY ENGINE PROJECT PROPOSAL — SSOT implementation plan

**Source file:** `gold_probability_engine_project_proposal.md`

```text
# Gold Probability Engine — Pre-Phase-1 Project Proposal
## Consolidated Architecture for External Review

**Status:** Pre-Phase-1 proposal  
**Purpose:** External review before implementation begins

---

## 1. Project Objective

Build a **weekly, repeatable, auditable gold-market decision-support system** for investment portfolio planning.

The system will run once per week, on **Saturday or Sunday after the New York gold market close**, and will estimate the probability of the USD gold spot price being in one of three states at each future horizon:

- **Bullish**
- **Consolidation / Range-bound**
- **Bearish**

The four forecast horizons are fixed:

1. **1–5 days**
2. **1–3 months**
3. **1–3 years**
4. **3–10 years**

The system is intended to support investment decision-making. It is **not** intended to execute trades or automatically manage a portfolio.

---

## 2. Target Definition

### Reference asset

**Gold spot price, USD per troy ounce.**

### Forecast origin

The latest valid gold reference price available after the New York market close and before the weekly run.

### Primary forecast target

For each horizon, estimate:

- **P(Bullish)**
- **P(Consolidation)**
- **P(Bearish)**

with:

**P(Bullish) + P(Consolidation) + P(Bearish) = 100%**

The exact quantitative definition of the consolidation/range-bound state will be established before implementation of the scoring engine and should be horizon-specific rather than using one arbitrary percentage threshold for all horizons.

---

## 3. Core Economic Framework

The project uses a fixed **12-layer causal architecture**.

### Layer 0 — Gold Stock/Flow Architecture
Existing above-ground gold, ownership structure, and marginal willingness to buy, hold, or sell.

### Layer 1 — Real Rates / Opportunity Cost
Real yields and the relative attractiveness of holding a non-yielding asset.

### Layer 2 — USD / FX
Dollar valuation and currency effects on gold.

### Layer 3 — Monetary-Policy Expectations
Expected future monetary-policy paths rather than only current policy rates.

### Layer 4 — Inflation, Purchasing Power & Fiscal Credibility
Inflation, inflation expectations, fiscal sustainability and monetary-confidence effects.

### Layer 5 — Official-Sector Reserve Allocation
Central-bank gold purchases, reserve diversification, sanctions/reserve-security considerations.

### Layer 6 — Geopolitical Transmission
Four main channels:
- safe-haven;
- energy/inflation;
- reserve security;
- monetary fragmentation.

### Layer 7 — Global Liquidity & Financial Conditions
Global liquidity, credit conditions, funding conditions and related financial stress.

### Layer 8 — Investment Flows
Gold ETFs, bars/coins, institutional flows and other financial investment demand.

### Layer 9 — Regional Physical Markets
China, India, regional premiums, seasonal demand and physical-market conditions.

### Layer 10 — Market Microstructure & Derivatives
COMEX, futures, options, positioning, systematic flows and related market mechanics.

### Layer 11 — Expectations, Psychology & Reflexivity
Investor expectations, fear/greed, narrative, momentum and feedback effects.

### Fundamental architecture rule

These 12 layers are **causal families, not 12 independent predictors**.

The system must distinguish between:
- primary drivers;
- transmission variables;
- flows;
- amplifiers;
- indicators.

This is necessary to avoid double-counting the same underlying shock through multiple layers.

---

## 4. Variable Architecture

The 12 layers are **locked**.

The variables inside each layer are **expandable**.

A new variable may be added when research establishes that it adds meaningful information to a layer.

Adding a variable should normally:

1. define and document the variable;
2. validate its data source and implementation;
3. determine its role and horizon relevance;
4. assign an initial variable weight;
5. redistribute weights **within that layer**.

Adding a variable should **not automatically change other layer-level weights**.

A change to layer-level weights requires separate research evidence and review.

This preserves architectural stability while allowing the system to improve over time.

---

## 5. Variable Types

Variables will initially be divided into three categories.

### A. Quantitative / Machine-observable

Data that can be retrieved, calculated or transformed deterministically.

Examples:
- DXY
- real yields
- CPI
- inflation expectations
- ETF flows
- oil
- VIX
- CFTC positioning
- gold momentum
- regional premiums

### B. Analytical / Evidence-interpretive

Phenomena that cannot be adequately represented by one deterministic observable and require structured assessment from evidence.

Examples:
- geopolitical escalation;
- sanctions implications;
- monetary-system fragmentation;
- fiscal-policy credibility;
- policy-regime interpretation.

### C. Composite / Model-derived

Indicators derived from multiple quantitative and/or analytical inputs.

Examples:
- monetary-policy pressure;
- geopolitical pressure;
- liquidity regime.

Composite indicators must remain transparent and traceable to their underlying inputs.

---

## 6. Variable Registry

Before implementation, every variable will have a permanent registry entry.

The registry should include at least:

| Field | Purpose |
|---|---|
| Variable ID | Permanent identifier |
| Layer | Assigned causal layer |
| Description | What the variable measures |
| Primary mechanism | Why it can affect gold |
| Horizon relevance | Relevant forecast horizons |
| Data type | Quantitative / analytical / composite |
| Source | Primary source or provider |
| Cost/access | Free / crawlable / paid / restricted |
| Frequency | Daily / weekly / monthly / quarterly etc. |
| Historical depth | Available historical coverage |
| Data quality | Reliability assessment |
| Freshness | How long an observation remains usable |
| Signal direction | Relationship to gold |
| Calculation | Deterministic calculation, if applicable |
| Initial weight | Research-derived starting weight |
| Confidence | Confidence in the initial weight |
| Evidence | Supporting research |
| Last review | Weight/definition review date |

---

## 7. Data Integrity Principle

Every observation should preserve:

- observation date;
- publication/release date;
- retrieval date;
- source;
- revision status.

The system must be able to distinguish:

> **what happened** from **when the information became knowable**.

The weekly production system may use the **full currently available information set**, including older information that remains relevant.

However, timestamps must be preserved so that future historical evaluation does not accidentally use information that was unavailable at the time of an earlier forecast.

---

## 8. Weekly Information Processing

The weekly run should follow this broad sequence:

```text
Current information set
        ↓
Data collection and validation
        ↓
Deterministic calculations
        ↓
AI evidence analysis for qualitative variables
        ↓
Variable signals
        ↓
Layer scores
        ↓
Horizon-specific weighting
        ↓
Interaction / dependency adjustment
        ↓
Historical evidence and counterexamples
        ↓
Three-state probability assessment
        ↓
Weekly report
        ↓
Forecast archive
```

---

## 9. Variable Signal

Each variable will ultimately produce:

### Stance

- **+1.0** = Bullish
- **0.0** = Neutral
- **-1.0** = Bearish

### Confidence

A value between **0.0 and 1.0** representing confidence in the variable assessment.

The initial layer-scoring structure is:

$$
L_k =
\frac{
\sum_{i=1}^{N_k}
(w_i \cdot S_i \cdot C_i)
}{
\sum_{i=1}^{N_k} w_i
}
$$

where:

- $S_i$ = variable stance;
- $C_i$ = variable confidence;
- $w_i$ = variable weight within its layer.

The resulting layer score is bounded between **-1.0 and +1.0**.

---

## 10. Interaction and Weight Adjustment

This is an area requiring explicit design before implementation.

The system should distinguish three cases.

### A. Duplicate information

Two variables substantially represent the same underlying information.

The system should reduce **double-counting of their combined contribution**, rather than mechanically reducing both weights simply because their statistical correlation is high.

### B. Causal transmission

One variable is a downstream transmission of another.

Example:

> monetary-policy expectations → real yields → USD → gold

The system should recognize the dependency and avoid treating each downstream variable as a fully independent causal shock.

### C. Genuine interaction

Two variables may have a materially different joint effect from their individual effects.

Example:

> real rates × geopolitical risk

In such cases, an explicit **interaction adjustment/multiplier** may be applied.

Therefore the intended structure is:

> **Base variable weight → dependency/duplication adjustment → genuine interaction adjustment → effective contribution**

The detailed rules and formulas for these adjustments must be specified before coding the scoring engine.

---

## 11. Layer Score and System Score

Each layer produces a score from **-1.0 to +1.0**.

The layers are combined using horizon-specific macro weights:

$$
S_{total,h} =
\sum_{k=1}^{12}
W_{k,h} \cdot L_{k,h}
$$

where:

- $W_{k,h}$ = research-derived weight of layer $k$ for horizon $h$;
- the layer weights for each horizon sum to 1.0.

Layer weights are therefore allowed to differ by forecast horizon.

The combined score is a **Net Index**, bounded between **-1.0 and +1.0**.

---

## 12. Three-State Probability Output

The final system must produce three probabilities:

- **P(Bullish)**
- **P(Consolidation)**
- **P(Bearish)**

The three probabilities must sum to 100%.

The exact mapping from Net Index and supporting evidence to the three probabilities will be specified during the scoring-engine phase.

A simple binary mapping such as:

$$
P(Bullish)=\frac{S_{total}+1}{2}
$$

is **not sufficient as the final production method**, because the production system explicitly recognizes consolidation/range-bound conditions.

---

## 13. Weekly Report Format

The weekly report should use the following core table and **no additional columns in this table**:

| Horizon | Net Index | P(Bullish) | P(Consolidation) | P(Bearish) | Signal Strength | Primary Layer Drivers |
|---|---:|---:|---:|---:|---|---|
| 1–5 Days | ... | ...% | ...% | ...% | ... | ... |
| 1–3 Months | ... | ...% | ...% | ...% | ... | ... |
| 1–3 Years | ... | ...% | ...% | ...% | ... | ... |
| 3–10 Years | ... | ...% | ...% | ...% | ... | ... |

The surrounding report may provide concise explanation, evidence, important developments and confidence/context, but the core comparison table remains fixed.

---

## 14. Historical Events and History

Historical information is **not the primary mechanism for automatically optimizing weights**.

Historical events serve as an **evidence and context engine**.

For the current weekly situation, the system may ask:

- What historical episodes had similar mechanisms?
- What were the important similarities?
- What were the important differences?
- What happened in those historical episodes?
- Were there counterexamples where apparently similar conditions produced opposite outcomes?

Historical evidence should therefore:

- support or challenge current assumptions;
- provide context;
- identify regime similarities;
- highlight counterexamples;
- affect confidence where appropriate.

It should **not automatically change weights simply because the current situation resembles a historical event**.

No unavailable historical information should be reconstructed with present-day AI judgment and treated as if it were historical quantitative data.

---

## 15. Initial Weighting Philosophy

Initial variable and layer weights will be established through **extensive research**, not automatically learned from a historical backtest.

Evidence may include:

- economic theory;
- academic research;
- central-bank research;
- market studies;
- historical observations;
- event studies;
- research-agent assessments;
- repeated empirical observations.

The weights are therefore **research-derived initial parameters**.

They should be treated as reviewable assumptions rather than permanent truths.

---

## 16. Feedback and Adaptive Weight Refinement

The production system should record every forecast and its eventual outcome.

After sufficient outcomes accumulate, the system should review:

- forecast errors;
- layer-level performance;
- variable-level performance;
- signal interpretation errors;
- interaction errors;
- data-quality problems;
- regime-dependent failures.

The system may then generate a **Weight Refinement Proposal**.

Example:

```text
Layer: L6 Geopolitical Transmission
Horizon: 1–3 months

Current weight: 8%
Proposed weight: 10%

Reason:
Repeated underestimation of geopolitical transmission
across several relevant forecast cycles.

Evidence strength:
Moderate

Status:
Pending research review
```

Weights should **not automatically change after a single forecast error**.

The objective is controlled, evidence-based adaptation rather than an unstable self-modifying model.

---

## 17. Random Forest Role

Random Forest is **not the core forecasting engine**.

It is a supporting empirical/diagnostic tool that may be used after sufficient reliable historical forecast data has accumulated.

Its purpose is to investigate:

- nonlinear relationships;
- interactions;
- threshold effects;
- combinations of variables that may not be captured by the research-derived scoring model.

Its role is:

> **diagnose potentially missing structure in the existing scoring model.**

It should not automatically determine:

- layer weights;
- variable weights;
- final probabilities.

If sufficient reliable historical data is unavailable for a horizon, Random Forest should simply not be used for that horizon.

---

## 18. Historical Data Availability Principle

The 12-layer framework does **not** require every layer to have identical historical depth.

Historical evidence will have uneven availability.

Therefore:

### Long-history quantitative variables
May support deeper empirical analysis.

### Shorter-history quantitative variables
May support modern-period analysis only.

### Historical qualitative/event evidence
May be used for contextual/regime research but not manufactured into artificial quantitative training data.

This prevents the research system from creating false historical precision.

---

## 19. Multi-Agent Implementation Architecture

The same modular agent approach used for research will be used for implementation.

### Worker Agent

Each worker agent is assigned an individual variable.

Its responsibilities are limited to that variable and include:

- implementation/retrieval;
- deterministic processing, where applicable;
- tests;
- brief usage manual;
- handoff document;
- any required supporting scripts.

The worker agent does **not** modify:

- layer architecture;
- other variables;
- cross-layer weights.

### Layer Manager Agent

Each layer has a manager responsible for:

- coordinating variable workers;
- integration;
- interface consistency;
- validation;
- layer-level weighting;
- resolving implementation conflicts.

When rework is required, the Layer Manager may assign a new Worker Agent to the relevant variable.

Once a worker's deliverables are accepted, the worker agent can be released.

This keeps agent context small and makes the implementation modular.

---

## 20. Research/Implementation Phases

The project remains **one project**. The following are implementation phases, not separate product versions.

### Phase 1 — Variable Registry

Deliver:

- complete variable inventory;
- definitions;
- mechanisms;
- sources;
- availability;
- quality;
- horizons;
- initial weights.

### Phase 2 — Data Ingestion

Deliver:

- source retrieval;
- validation;
- timestamps;
- freshness management;
- derived quantitative variables.

### Phase 3 — AI Evidence Processing

Deliver:

- structured qualitative assessments;
- confidence;
- evidence citations;
- counterarguments.

### Phase 4 — Scoring Engine

Deliver:

- variable signals;
- layer scores;
- variable weights;
- horizon-specific layer weights;
- interaction/dependency adjustments;
- Net Index.

### Phase 5 — Probability Engine

Deliver:

- Bullish / Consolidation / Bearish probabilities;
- signal strength;
- consistent probability mapping.

### Phase 6 — Weekly Production Engine

Deliver:

- automated Saturday/Sunday run;
- complete weekly report;
- full archival of inputs and outputs.

### Phase 7 — Feedback Review

Deliver:

- forecast/outcome tracking;
- performance diagnostics;
- evidence-based weight refinement proposals.

Random Forest may be introduced as a diagnostic during later phases only if sufficient reliable data exists.

---

## 21. Scope Control

The project objective remains:

> **Produce a systematic weekly probability assessment of USD gold price direction over four future horizons, supported by a transparent causal framework and evidence.**

The following are outside the initial scope:

- automatic portfolio allocation;
- automatic trading;
- trade execution;
- intraday prediction;
- prediction of other asset classes;
- uncontrolled self-modifying weights;
- large-scale historical reconstruction where reliable data does not exist.

New features should only be added when they are **necessary to achieve the core objective or clearly required to make an existing component work correctly**.

---

## 22. Proposed Phase-1 Entry Condition

Before Phase 1 begins, the final v2.2 causal framework and this implementation proposal should be reviewed externally.

After review, Phase 1 begins with:

> **Building the Gold Variable Registry for all 12 locked layers.**

The registry should be the single source of truth for what the weekly system will monitor.

---

## 23. Key Design Principles

1. **Keep the 12-layer causal architecture stable.**
2. **Allow variables within layers to expand as evidence justifies.**
3. **Use quantitative data as the backbone and AI for genuinely interpretive evidence.**
4. **Treat historical events as evidence and context, not automatic weight optimizers.**
5. **Use research-derived weights initially.**
6. **Refine weights through controlled feedback, not weekly self-modification.**
7. **Prevent double-counting through explicit dependency and interaction rules.**
8. **Preserve point-in-time data integrity.**
9. **Keep Random Forest as an optional diagnostic, not the core forecast engine.**
10. **Keep the project focused on four weekly gold-probability outputs.**

---

**Document status: Proposed architecture for external review before Phase 1.**
```


## SPEC C V2 — VARIABLE ADMISSION CRITERIA — finalized

**Source file:** `spec_c_variable_admission_criteria_v2.md`

```text
# Gold Probability Engine — Spec C
## Variable Admission Criteria

**Status:** Draft for external review  
**Purpose:** Define when a new variable may be admitted into one of the 12 locked causal layers.

---

## 1. Objective

The 12-layer causal architecture is fixed.

The variables within each layer are expandable when a genuinely useful new variable is identified.

Spec C establishes a consistent admission gate so that:

- useful variables can be added;
- redundant variables are not added merely because they are available;
- weak or unreliable data does not enter the production model;
- variable expansion does not alter the layer architecture;
- a new variable does not automatically change cross-layer weights.

The goal is controlled extensibility, not exhaustive collection of every variable that could possibly affect gold.

---

## 2. Core Principle

A candidate variable should be admitted only when there is sufficient evidence that it:

> **adds useful, credible, operationally feasible information to an existing layer for at least one forecast horizon.**

“Useful” does not require decades of historical quantitative data.

A variable may qualify through strong causal or domain evidence even when its historical quantitative coverage is limited, provided its limitations are explicitly recorded.

---

## 3. Admission Gate

Every candidate variable must pass all five core criteria.

### Criterion A — Causal Relevance

There must be a credible mechanism through which the variable can affect gold.

The submission must explain:

1. What phenomenon does the variable represent?
2. Through what mechanism can it affect gold?
3. Which direction is expected under normal conditions?
4. Can the relationship become conditional or reverse under specific regimes?

**Minimum requirement:**

A concise, evidence-supported causal rationale.

### Criterion B — Incremental Information

The candidate must add information that is not already adequately represented by the existing variable set.

**During Phase 1 registry construction, the baseline is the approved causal architecture and the other candidates under consideration. Each candidate must demonstrate causal relevance to its assigned layer and be checked for obvious redundancy with other Phase-1 candidates. Once Phase 1 is complete, all new variables are evaluated against the approved registry.**

The candidate does not need to be completely unique.

It may still qualify when it:

- measures the same broad phenomenon more directly;
- captures a different transmission channel;
- provides information at a different frequency;
- provides earlier information;
- improves regional or regime-specific coverage;
- captures an interaction or condition not represented elsewhere.

The submission must explicitly state:

> **What information does this variable add that the current system does not capture adequately?**

### Criterion C — Data / Evidence Reliability

The information must be sufficiently reliable for its intended use.

For quantitative variables, assess:

- source authority;
- methodology;
- consistency;
- revision behavior;
- historical coverage;
- missing-data risk;
- publication frequency;
- access stability.

For analytical variables, assess:

- source quality;
- evidence traceability;
- consistency of interpretation;
- susceptibility to subjective judgment.

A variable with attractive theoretical relevance but unreliable evidence should not be admitted to production merely because the concept is interesting.

### Criterion D — Operational Feasibility

The variable must be practical to collect and maintain in the weekly production system.

Assess:

- data accessibility;
- cost;
- retrieval reliability;
- processing complexity;
- freshness;
- licensing/use restrictions;
- dependence on manual intervention;
- expected maintenance burden.

A variable may be scientifically useful but rejected from production if maintaining it is disproportionately difficult relative to its expected benefit.

### Criterion E — Forecast-Horizon Relevance

The variable must have a meaningful role in at least one of the four fixed horizons:

- 1–5 days
- 1–3 months
- 1–3 years
- 3–10 years

The admission record must specify:

- relevant horizon(s);
- expected importance by horizon;
- whether relevance is structural, cyclical, event-driven, or conditional.

A variable does not need to be relevant to all four horizons.

---

## 4. Admission Decision

A candidate variable receives one of three statuses.

### ADMIT

All five core criteria are sufficiently satisfied.

The variable can proceed to implementation and receive an initial research-derived weight.

### CONDITIONAL / RESEARCH ONLY

The causal case is useful, but one or more implementation criteria are not yet strong enough for production.

Examples:

- data availability is currently inadequate;
- historical evidence is limited;
- source quality needs further validation;
- the variable is potentially useful but overlaps heavily with existing variables.

A Research-Only variable is retained in the research registry but is not included in the production scoring system.

### REJECT

The candidate fails one or more fundamental criteria.

Typical reasons:

- weak causal rationale;
- essentially duplicate information;
- unreliable source;
- impractical maintenance burden;
- no meaningful relevance to the approved horizons.

A rejected variable can be reconsidered later if evidence or data availability materially changes.

---

## 5. Admission Record

Every proposed variable should have a standardized admission record.

| Field | Required content |
|---|---|
| Variable name | Proposed variable |
| Layer | Target layer |
| Variable ID | Proposed permanent ID |
| Causal mechanism | Why/how it can affect gold |
| Direction | Expected gold relationship |
| Incremental information | What it adds beyond current variables |
| Overlap | Existing/candidate variables with similar information |
| Data/evidence source | Primary source(s) |
| Reliability | Assessment |
| Historical depth | Available coverage |
| Frequency | Update frequency |
| Freshness | Validity window |
| Accessibility | Free / crawlable / paid / restricted |
| Operational burden | Low / medium / high |
| Relevant horizons | One or more of the four horizons |
| Initial weight rationale | Why it deserves its proposed weight |
| Evidence references | Supporting material |
| Decision | Admit / Conditional / Reject |
| Review date | Date of admission decision |
| Reviewer | Responsible reviewer/agent |

---

## 6. Weight Handling After Admission

Adding a variable does not automatically change layer weights or other layers.

When a new variable is admitted:

1. assign an initial variable weight within its layer;
2. redistribute existing within-layer variable weights as necessary;
3. document the rationale for the redistribution;
4. preserve all existing layer-level weights.

A layer-level weight change requires a separate review under the future weight-governance process.

Therefore:

> **Variable admission changes the composition of a layer; it does not automatically redesign the causal architecture.**

---

## 7. Information Overlap Does Not Mean Automatic Rejection

High correlation or conceptual similarity is a reason for investigation, not automatic exclusion.

A candidate may still be admitted if it provides meaningful incremental value through:

- different timing;
- different geography;
- different transmission mechanism;
- better data quality;
- lower latency;
- greater robustness;
- regime-specific information.

The system should distinguish:

> **“Redundant”**

from:

> **“Related but complementary.”**

Detailed interaction and dependency treatment belongs to **Spec A**, not this admission specification.

---

## 8. Example Admission Test — Gold/Silver Ratio

### Candidate

**Gold/Silver Ratio**

### Possible layer

Potentially relevant to Layer 1 or another layer depending on the researched mechanism.

### Causal relevance

Potentially relevant because the ratio may contain information about relative precious-metals demand, monetary stress, industrial-cycle conditions, or changes in the relative attractiveness of monetary versus industrial metals.

### Incremental-information question

The variable should not be admitted merely because it correlates with gold.

The key question is:

> **Does the gold/silver ratio provide information about future gold direction that is not already adequately represented by the existing variable set?**

If it merely repackages variables already in the model, its admission case is weak.

If research shows it captures an additional monetary/precious-metals regime signal, it may qualify.

### Data/evidence

Gold and silver prices have strong historical availability, making the raw ratio operationally feasible.

However, historical availability alone is insufficient. The variable still needs a credible causal rationale and incremental-information case.

### Decision

**Not automatically admitted.**

It would go through the same five-criterion gate as every other candidate.

---

## 9. Research Evidence Standard

The admission process should not require a single type of evidence.

Useful evidence can include:

- academic research;
- central-bank or institutional research;
- high-quality market studies;
- primary-source data;
- established economic theory;
- robust historical observations;
- well-supported specialist research.

Evidence strength should be documented as part of the admission record.

A variable should not be admitted solely because:

- an AI agent suggests it;
- traders frequently discuss it;
- it appears correlated over a short period;
- it is easy to retrieve;
- it sounds economically logical.

---

## 10. AI Agent Role in Admission

AI Agents may:

- identify candidate variables;
- research causal mechanisms;
- find supporting evidence;
- identify potential overlap;
- assess data availability;
- prepare the admission record;
- recommend Admit / Conditional / Reject.

AI Agents should **not unilaterally change the 12-layer architecture**.

The final admission decision should be made through the defined project review process.

---

## 11. Scope-Control Rules

1. A variable should not be added merely because it is available.
2. A variable should not be added merely because it has a historical correlation with gold.
3. A variable should not be added if its information is already adequately captured elsewhere without a clear incremental benefit.
4. Every admitted variable must have an identified horizon of relevance.
5. Every admitted variable must have a documented source/evidence trail.
6. New variables do not automatically alter layer-level weights.
7. The number of variables should remain only as large as necessary to represent the layer adequately.

---

## 12. Acceptance Criteria for Spec C

Spec C is considered ready for implementation when the project can take any proposed variable and produce a consistent answer to:

1. Why does it belong in this layer?
2. What new information does it add?
3. Is its evidence/data reliable enough?
4. Can we operate it reliably every week?
5. Which forecast horizon(s) does it matter for?
6. Should it be admitted, research-only, or rejected?
7. What initial within-layer weight should it receive, and why?

---

## 13. Guiding Principle

> **The purpose of variable admission is not to collect every potentially relevant indicator. It is to build the smallest credible set of variables that adequately represents each causal layer and supports the four forecast horizons.**

**End of Spec C — Draft for External Review**
```


## SPEC D V2 — AI EVIDENCE PROTOCOL — finalized

**Source file:** `spec_d_ai_evidence_protocol_v2.md`

```text
# Gold Probability Engine — Spec D
## AI Evidence Protocol

**Status:** Draft for external review  
**Purpose:** Define how AI Agents assess qualitative or evidence-interpretive variables without turning unsupported judgment into model input.

---

## 1. Objective

AI Agents are used where a phenomenon cannot be adequately represented by a deterministic quantitative variable.

The protocol must ensure every analytical assessment is:

- evidence-backed;
- timestamped;
- explicit about uncertainty;
- separated into fact and interpretation;
- reversible/auditable;
- comparable across weekly runs.

AI output is an **input to the scoring system**, not an independent authority.

---

## 2. Required Evidence Record

Every analytical assessment must return the following fields:

| Field | Requirement |
|---|---|
| Variable ID | Exact registry identifier |
| Observation timestamp | When the assessment applies |
| Evidence | Specific supporting facts/sources |
| Assessment | Current interpretation |
| Stance | -1.0 to +1.0 |
| Confidence | 0.0 to 1.0 |
| Counter-evidence | Material evidence against the assessment |
| Fact vs interpretation | Clearly separated |
| Source provenance | Source names/links and publication dates |

No field should be omitted unless the variable's defined method explicitly does not require it.

---

## 3. Fact vs Interpretation

AI Agents must separate:

### Facts

Observable statements supported by sources.

Example:

> “The central bank announced X on [date].”

### Interpretation

Reasoned assessment derived from the facts.

Example:

> “This may increase the probability of tighter monetary policy.”

The model must never present an interpretation as though it were an observed fact.

---

## 4. Evidence Sufficiency

An analytical assessment should not be based on a single weak assertion when the variable materially affects the forecast.

Evidence should be assessed for:

- source quality;
- recency;
- relevance;
- independence;
- consistency.

When evidence is insufficient:

> **Confidence should fall.**

The system should not manufacture certainty simply because a directional stance is required.

---

## 5. Counter-Evidence

Every non-neutral analytical assessment should actively consider material evidence against the chosen stance.

### Counter-evidence should normally affect:

**confidence first**, rather than automatically reversing stance.

For example:

- strong bullish evidence + weak counter-evidence → bullish stance, high confidence;
- strong bullish evidence + strong bearish counter-evidence → bullish/neutral stance with lower confidence;
- evidence genuinely balanced → neutral stance.

A stance should flip only when the total evidence supports the opposite interpretation.

This prevents a single contradictory fact from mechanically reversing a broader assessment.

---

## 6. Analytical Stance

The standard stance scale is:

- **+1.0** = strongly bullish;
- **0.0** = neutral / insufficient directional evidence;
- **-1.0** = strongly bearish.

Intermediate values are allowed when the evidence is directional but not extreme.

The stance represents:

> **directional assessment of the variable's expected effect on gold for its defined horizon.**

It does not represent confidence.

Confidence is captured separately.

---

## 7. Confidence Operationalization

Confidence is:

> **0.0 ≤ C ≤ 1.0**

Confidence is generated from a fixed five-factor rubric rather than free-form AI judgment.

Each factor is scored from **0 to 2**:

| Factor | 0 — Weak | 1 — Moderate | 2 — Strong |
|---|---|---|---|
| Evidence quality | Weak/indirect sources | Mixed/acceptable sources | Strong primary/institutional sources |
| Evidence sufficiency | Sparse evidence | Some supporting evidence | Multiple adequate pieces |
| Source agreement | Major disagreement | Mixed/partial agreement | Strong agreement |
| Recency | Stale/possibly obsolete | Still relevant | Current/recent |
| Mechanism clarity | Highly ambiguous | Plausible/conditional | Clear and well-supported |

Let:

\[
R=q+s+a+r+m
\]

where each component is 0–2, so \(0\le R\le10\).

Base confidence:

\[
C_{base}=R/10
\]

Counter-evidence is scored:

- 0 = little/no material counter-evidence
- 1 = meaningful counter-evidence
- 2 = strong counter-evidence

Final confidence:

\[
C=C_{base}\times\left(1-0.20\times\frac{E_{counter}}{2}\right)
\]

Thus material counter-evidence reduces confidence rather than automatically reversing stance.

### Confidence bands

| Confidence | Band |
|---:|---|
| 0.00–0.29 | Low |
| 0.30–0.59 | Moderate |
| 0.60–0.79 | Strong |
| 0.80–1.00 | Very strong |

These are confidence bands, not probabilities of being correct.

### Insufficient-evidence override

If evidence is inadequate or source quality is unacceptable:

```text
STANCE: 0.00
CONFIDENCE: ≤ 0.20
STATUS: Insufficient evidence
```

This override takes precedence over the normal rubric.

Confidence is **not** simply “how strongly the agent feels.”

---

## 8. Conflicting Sources

When credible sources disagree:

1. record the disagreement;
2. identify the basis of the disagreement where possible;
3. do not hide conflicting evidence;
4. reduce confidence when the disagreement materially affects the assessment;
5. use the stronger evidence to determine stance where justified.

The AI Agent should not force false consensus.

---

## 9. News and Event Processing

For current events, the AI Agent should identify:

- event;
- affected country/region;
- mechanism;
- likely direction for gold;
- relevant forecast horizon;
- potential offsetting channels.

For geopolitics, the four approved channels should be considered where relevant:

1. safe-haven;
2. energy/inflation;
3. reserve security;
4. monetary fragmentation.

An event should not automatically be treated as bullish or bearish merely because it is “geopolitical.”

---

## 10. Historical Evidence in AI Assessment

Historical events may be used as contextual evidence.

The Agent may report:

- similar historical mechanisms;
- similarities;
- differences;
- historical outcomes;
- counterexamples.

It must not fabricate quantitative historical values where reliable data is unavailable.

Historical analogy must be presented as:

> **context/evidence, not proof that the current outcome will repeat.**

---

## 11. Source Hierarchy

Where available, prefer:

1. primary official sources;
2. established institutional research;
3. high-quality specialist sources;
4. reputable financial/news organizations;
5. secondary commentary;
6. low-quality aggregators/social content only when necessary and explicitly flagged.

The source hierarchy affects evidence quality and confidence.

---

## 12. AI Output Template

Each analytical variable should return a structured record similar to:

```text
Variable ID:
Observation timestamp:

FACTS:
- ...

EVIDENCE:
- Source / publication date / key fact
- Source / publication date / key fact

ASSESSMENT:
- ...

STANCE:
+0.00

CONFIDENCE:
0.00

COUNTER-EVIDENCE:
- ...

COUNTER-EVIDENCE SCORE:
0 / 1 / 2

CONFIDENCE RUBRIC:
- Evidence quality: 0/1/2
- Evidence sufficiency: 0/1/2
- Source agreement: 0/1/2
- Recency: 0/1/2
- Mechanism clarity: 0/1/2

FACT / INTERPRETATION BOUNDARY:
- Facts:
- Interpretation:

RELEVANT HORIZONS:
- 1–5 days: ...
- 1–3 months: ...
- 1–3 years: ...
- 3–10 years: ...
```

### Completed Example — Geopolitical Escalation

```text
Variable ID:
L06.GEO_ESCALATION

Observation timestamp:
2026-08-16

FACTS:
- A material geopolitical development was reported by multiple reputable sources.
- The event has potential regional-security and energy implications.

EVIDENCE:
- Primary/official source: publication date and event fact.
- Reputable financial/news source: publication date and independent confirmation.
- Specialist source: analysis of likely transmission mechanism.

ASSESSMENT:
The event increases near-term safe-haven demand and may raise energy/inflation
risk. The effect is likely more relevant over 1–3 months than 3–10 years unless
the situation becomes structural.

STANCE:
+0.65

COUNTER-EVIDENCE:
- No immediate evidence of broad financial-system disruption.
- De-escalation remains possible.
- Higher oil prices could eventually induce tighter monetary expectations,
  partially offsetting the safe-haven effect.

COUNTER-EVIDENCE SCORE:
1

CONFIDENCE RUBRIC:
- Evidence quality: 2/2
- Evidence sufficiency: 2/2
- Source agreement: 1/2
- Recency: 2/2
- Mechanism clarity: 1/2

BASE CONFIDENCE:
(2+2+1+2+1)/10 = 0.80

COUNTER-EVIDENCE ADJUSTMENT:
0.80 × (1 - 0.20×1/2) = 0.72

FINAL CONFIDENCE:
0.72

FACT / INTERPRETATION BOUNDARY:
- Facts: reported development and official responses.
- Interpretation: expected safe-haven, energy/inflation and policy transmission.

RELEVANT HORIZONS:
- 1–5 days: +0.55
- 1–3 months: +0.65
- 1–3 years: +0.20
- 3–10 years: 0.00
```

The numeric values are illustrative and are not production parameters.

---

## 13. Failure Handling

The Agent must be able to return:

> **Insufficient evidence**

rather than inventing an assessment.

Possible output:

```text
STANCE: 0.00
CONFIDENCE: 0.15
STATUS: Insufficient evidence
```

This is preferable to false precision.

---

## 14. AI Agent Restrictions

AI Agents must not:

- change layer definitions;
- create new production variables without the admission process;
- modify variable weights;
- modify layer weights;
- manufacture historical data;
- hide counter-evidence;
- convert speculation into fact.

Their role is:

> **structured evidence interpretation within an approved variable.**

---

## 15. Acceptance Criteria for Spec D

A qualitative-variable implementation is compliant when:

1. evidence is traceable;
2. facts and interpretations are separated;
3. stance and confidence are separate;
4. counter-evidence is explicitly considered;
5. timestamps are preserved;
6. inadequate evidence can result in a low-confidence/insufficient-evidence outcome;
7. the Agent cannot change model architecture or weights.

**End of Spec D — Draft for External Review**
```


## SPEC A V2 — INTERACTION & DEPENDENCY RULES — finalized

**Source file:** `spec_a_interaction_dependency_rules_v2.md`

```text
# Gold Probability Engine — Spec A
## Interaction & Dependency Rules

**Status:** Draft for external review  
**Purpose:** Define how the scoring system handles duplicated information, causal transmission and genuine interactions without double-counting or arbitrary weekly adjustments.

---

## 1. Objective

The 12 layers are causal families, not independent predictors.

Variables can be related in three fundamentally different ways:

1. **Duplicate information**
2. **Causal transmission**
3. **Genuine interaction**

Spec A defines the conceptual and computational treatment of each case.

The specification establishes the framework before implementation. It does **not** determine final empirical parameter values.

---

## 2. Base Contribution

For variable \(i\) in layer \(k\):

\[
B_i = w_i \cdot S_i \cdot C_i
\]

where:

- \(w_i\) = base variable weight;
- \(S_i\) = stance, bounded [-1,+1];
- \(C_i\) = confidence, bounded [0,1].

The normal layer calculation uses the sum of effective contributions.

---

## 3. Case A — Duplicate Information

### Definition

Two variables are duplicative when they materially represent the same underlying information and adding both at full weight would count the same information more than once.

Examples may include:

- two highly similar measures of the same market condition;
- two derived indicators built from the same underlying source;
- a level and a near-identical transformation that adds little new information.

### Treatment

Do not automatically delete one variable.

Instead:

1. identify the shared information;
2. determine whether either variable has superior quality, timing or coverage;
3. allocate an effective combined weight that reflects the information content rather than the number of representations.

Conceptually:

\[
w_i^{eff} = w_i \cdot D_i
\]

where \(D_i\) is a dependency/duplication factor satisfying:

\[
0 < D_i \le 1
\]

For a clearly redundant pair, the sum of their effective weights should not materially exceed the weight the underlying information deserves as a whole.

The exact pairwise/cluster calculation is an implementation parameter to be finalized after the actual variable registry exists.

---

## 4. Case B — Causal Transmission

### Definition

Variable A influences B, and B transmits part of the same underlying shock toward gold.

Example:

> Monetary-policy expectations → real yields → USD → gold

Treating all three as independent full-strength drivers can double-count a single shock.

### Treatment

The system should identify:

- upstream driver;
- downstream transmission variable;
- whether the downstream variable contains incremental information beyond the upstream variable.

The downstream variable receives full weight only to the extent that it adds information not already represented by the upstream driver.

Conceptually:

\[
w_i^{eff} = w_i \cdot T_i
\]

where \(T_i\) represents the non-overlapping contribution of the transmission variable.

This is **not** a rule that downstream variables should always receive lower weights. A transmission variable may contain important independent information and therefore retain substantial effective weight.

---

## 5. Case C — Genuine Interaction

### Definition

Two or more variables jointly influence gold in a way that cannot be represented adequately by simply adding their independent contributions.

Example:

> Real rates × geopolitical risk

The effect of real rates may be weaker when geopolitical risk is exceptionally high.

### Treatment

Keep the individual contributions, then add an explicit interaction term:

\[
I_{ij} = \gamma_{ij} \cdot S_i \cdot S_j \cdot C_i \cdot C_j
\]

where:

- \(\gamma_{ij}\) = interaction coefficient;
- \(S_i,S_j\) = variable stances;
- \(C_i,C_j\) = confidences.

The interaction coefficient may be:

- positive: joint effect reinforces;
- negative: joint effect offsets;
- zero: no interaction applied.

Interaction terms must be explicitly documented.

They must not be introduced merely because two variables are correlated.

---

## 6. Effective Layer Contribution

The conceptual structure is:

\[
E_i =
w_i \cdot
D_i \cdot
T_i \cdot
S_i \cdot
C_i
\]

plus explicit interaction terms where approved.

This should not be interpreted as saying every variable receives all three modifiers below 1.0.

For variables where a modifier is not applicable:

\[
D_i = 1
\]

or

\[
T_i = 1
\]

as appropriate.

The intended logic is:

> **Base weight → dependency/duplication treatment → genuine interaction treatment → effective contribution.**

---

## 7. Trigger for Dependency Review

Interaction/dependency review should be triggered when at least one of the following is true:

### Trigger 1 — Provenance overlap
Variables are derived from the same underlying source or calculation.

### Trigger 2 — Mechanism overlap
Variables represent the same economic mechanism.

### Trigger 3 — Strong observed relationship
Data shows a persistent strong relationship that suggests information overlap.

### Trigger 4 — Explicit causal relationship
Research identifies an upstream/downstream relationship.

### Trigger 5 — Joint-response hypothesis
Research indicates that the effect of one variable changes materially conditional on another.

A statistical correlation alone is **not sufficient** to establish causality.

---

## 8. Interaction Review Workflow

When a trigger occurs:

1. classify the relationship;
2. document the reason;
3. determine whether information is duplicated, transmitted, or genuinely interactive;
4. assign the appropriate treatment;
5. record the effective contribution rule;
6. test the resulting layer behavior for obvious double-counting or distortion.

No weekly discretionary adjustment should be made outside this framework.

---

## 9. Worked Conceptual Example

Suppose:

- Fed expectation signal = +0.60
- real-yield signal = +0.40
- DXY signal = +0.20

Research determines:

> Fed expectations are upstream; real yields and DXY partially transmit the same monetary shock but contain some additional information.

The system should **not** simply count all three at full independent weight.

Instead:

- Fed expectation receives its base contribution;
- real yield receives an effective contribution after transmission/dependency treatment;
- DXY receives an effective contribution after transmission/dependency treatment;
- any genuine interaction is separately added only if supported.

This preserves information while limiting double-counting.

---

## 10. Worked Numerical Example

This example is illustrative and establishes the reference implementation structure, not production parameter values.

Suppose a simplified layer contains three variables:

| Variable | Base weight \(w_i\) | Stance \(S_i\) | Confidence \(C_i\) | Duplication \(D_i\) | Transmission \(T_i\) |
|---|---:|---:|---:|---:|---:|
| Fed expectations | 0.40 | +0.60 | 0.90 | 1.00 | 1.00 |
| Real yields | 0.35 | +0.40 | 0.80 | 1.00 | 0.75 |
| DXY | 0.25 | +0.20 | 0.70 | 1.00 | 0.60 |

Effective contributions:

\[
E_{Fed}=0.40\times0.60\times0.90=0.216
\]

\[
E_{RealYield}=0.35\times1.00\times0.75\times0.40\times0.80=0.084
\]

\[
E_{DXY}=0.25\times1.00\times0.60\times0.20\times0.70=0.021
\]

Total effective contribution:

\[
E_{sum}=0.216+0.084+0.021=0.321
\]

Effective denominator:

\[
W_{eff}=0.40+(0.35\times0.75)+(0.25\times0.60)=0.8125
\]

Illustrative layer score:

\[
L_k=\frac{0.321}{0.8125}\approx+0.395
\]

So the illustrative layer score is approximately:

> **+0.40**

The example demonstrates the intended treatment of an upstream policy variable and downstream transmission variables. The numbers are illustrative only.

### Genuine interaction illustration

Suppose research has approved an interaction between real yields and geopolitical risk:

\[
I_{ij}=\gamma S_iS_jC_iC_j
\]

with:

\[
\gamma=-0.10,\quad S_i=0.40,\quad S_j=0.70,\quad C_i=0.80,\quad C_j=0.70
\]

Then:

\[
I_{ij}=-0.01568
\]

The interaction slightly offsets the independent contributions. The coefficient is illustrative only.

---

## 11. What Spec A Does Not Decide

Spec A does not determine:

- final variable weights;
- final layer weights;
- empirical coefficient values;
- weekly manual adjustments;
- the statistical method used to estimate future coefficients.

Those are handled through the research-derived weighting process and later controlled refinement.

---

## 12. Acceptance Criteria for Spec A

Before scoring-engine implementation, the project must be able to:

1. identify a candidate duplication/transmission/interaction relationship;
2. classify it consistently;
3. explain why;
4. apply a documented effective-weight treatment;
5. add explicit interaction terms only where justified;
6. demonstrate that no information is being counted twice merely because it appears in multiple variables.

**End of Spec A — Draft for External Review**
```


## SPEC B V2 — THREE-STATE PROBABILITY MODEL — finalized

**Source file:** `spec_b_three_state_probability_model_v2.md`

```text
# Gold Probability Engine — Spec B
## Three-State Probability Model

**Status:** Draft for external review  
**Purpose:** Define how the system converts the Net Index into three probabilities while preserving the Net Index as the transparent directional-conviction measure.

---

## 1. Objective

The production system uses two related but distinct outputs.

### Net Index

A single score:

\[
-1.00 \le S_{total} \le +1.00
\]

where:

- **+1.00** = maximum bullish consensus;
- **0.00** = perfectly neutral / signals cancel;
- **-1.00** = maximum bearish consensus.

### Three-State Probability

The system also produces:

- \(P(B)\) = probability of Bullish outcome;
- \(P(C)\) = probability of Consolidation / Range-bound outcome;
- \(P(Be)\) = probability of Bearish outcome.

with:

\[
P(B)+P(C)+P(Be)=1
\]

The Net Index remains the primary transparent measure of directional conviction.

---

## 2. Relationship Between Net Index and Probability

The existing binary interpretation is retained as a reference:

\[
P(Higher) =
\left(
\frac{S_{total}+1}{2}
\right)
\times 100\%
\]

This is interpreted as:

> **a binary directional probability if the only possible outcomes are higher or not higher.**

It is **not** the final three-state production output.

---

## 3. Three-State Model

The production probability model must transform the Net Index and the current market-state evidence into:

\[
P(B), P(C), P(Be)
\]

The model must preserve the core directional meaning of the Net Index:

- higher Net Index → higher relative Bullish probability;
- lower Net Index → higher relative Bearish probability;
- Net Index near zero → greater potential for Consolidation.

The model therefore has two conceptual dimensions:

### Directional conviction

Represented by Net Index.

### Range/consolidation propensity

Determined separately from the current forecast state.

---

## 4. Range Propensity

### Definition

For Spec B, **Range Propensity** means:

> **the estimated likelihood that gold's realized price movement over the forecast horizon will remain within the predefined consolidation band for that horizon.**

It is distinct from Net Index.

A near-zero Net Index can arise from genuine range-bound conditions or from strong opposing forces that may produce a large move in either direction.

### Source

Range Propensity is a **deterministic composite market-state indicator**, not a free-form AI opinion in the base implementation.

The initial composite is built from approved observable variables associated with the current range/volatility regime, selected through the Phase-1 variable registry. Candidate inputs include:

- realized volatility;
- ATR or comparable range measure;
- recent directional persistence/trend strength;
- recent breakout/range behavior;
- relevant market-structure stress measures.

For each horizon \(h\), the approved inputs are standardized and combined into:

\[
R_h\in[0,1]
\]

where:

- \(R_h=0\) = low range-bound propensity;
- \(R_h=1\) = high range-bound propensity.

The exact component set and weights are determined from approved Phase-1 variables and documented before Phase 5 implementation.

AI qualitative evidence may provide context, but it does not directly override the deterministic composite.

---

## 5. Consolidation Is Not Simply “Neutral”

Consolidation should represent a forecast that the gold price is likely to remain within a defined range rather than make a meaningful directional move.

Therefore:

> **Neutral layer signals do not automatically mean high P(Consolidation).**

A market can have conflicting strong bullish/bearish forces and therefore have Net Index near zero while still being expected to be volatile.

Conversely, weak directional forces may produce genuinely range-bound conditions.

The production model must distinguish:

- **directional cancellation**
from
- **true range-bound conditions**.

---

## 6. Horizon-Specific Consolidation Definition

The consolidation state must use a threshold appropriate to the forecast horizon.

For each horizon \(h\), define a range threshold:

\[
R_h
\]

The threshold represents the magnitude of price movement considered economically meaningful over that horizon.

Illustratively:

\[
|Return_h| < R_h
\]

may constitute a consolidation outcome.

The actual values of \(R_h\) must be determined during probability-model development using the behavior and volatility characteristics of each horizon.

No single fixed percentage should be imposed across all four horizons.

---

## 7. Probability Mapping Principle

The final three-state probability should be based on:

1. **Net Index**
2. **Consolidation/range propensity**
3. **Horizon-specific characteristics**
4. **Signal strength**

Conceptually:

### Strong positive Net Index

Higher:

> P(Bullish)

Lower:

> P(Bearish)

Consolidation depends on whether the system also indicates a range-bound environment.

### Strong negative Net Index

Higher:

> P(Bearish)

Lower:

> P(Bullish)

Consolidation again depends on range propensity.

### Net Index near zero

Potential outcomes include:

- high P(Consolidation) if the market is genuinely range-bound;
- relatively balanced P(Bullish)/P(Bearish) if directional uncertainty is high.

Therefore:

> **Net Index near zero does not automatically imply P(Consolidation) = high.**

---

## 8. Illustrative Mapping

The following example is conceptual and does **not** establish final production thresholds.

Suppose:

\[
S_{total}=+0.25
\]

The binary interpretation would be:

\[
P(Higher)=62.5\%
\]

A possible three-state outcome might be:

| Horizon | P(Bullish) | P(Consolidation) | P(Bearish) |
|---|---:|---:|---:|
| 1–5 days | 55% | 30% | 15% |
| 1–3 months | 62% | 23% | 15% |
| 1–3 years | 67% | 20% | 13% |
| 3–10 years | 64% | 21% | 15% |

These are illustrative only.

The final mapping must be determined systematically.

---

## 9. Signal Strength

Signal strength describes the magnitude of directional conviction represented by the Net Index.

A starting interpretation may retain:

\[
|S_{total}| \ge 0.50
\]

as a strong directional signal,

\[
0.20 \le |S_{total}| < 0.50
\]

as a medium directional signal,

and:

\[
|S_{total}| < 0.20
\]

as a low/neutral directional signal.

These thresholds are **provisional** and may be reviewed after the probability model is implemented.

Signal strength is distinct from probability.

A market can have:

> low directional signal + high consolidation probability

or:

> low directional signal + high uncertainty between Bullish/Bearish.

---

## 10. Asymmetry by Horizon

The three-state mapping may be horizon-specific because:

- expected volatility differs;
- meaningful price ranges differ;
- consolidation durations differ;
- structural trends may dominate longer horizons.

Therefore the model may use different mapping parameters for:

- 1–5 days;
- 1–3 months;
- 1–3 years;
- 3–10 years.

However, the core interpretation of the Net Index remains the same across horizons.

---

## 11. Probability Integrity

For every weekly forecast and every horizon:

\[
0 \le P(B),P(C),P(Be) \le 1
\]

and:

\[
P(B)+P(C)+P(Be)=1
\]

The system must reject or flag invalid probability outputs.

---

## 12. Calibration Principle

The probability model should eventually be evaluated for calibration.

For example:

> Forecasts near 70% Bullish should, over a sufficiently large sample, produce Bullish outcomes at approximately the same frequency.

However, initial probability parameters may be research-derived and provisional.

The production system should retain the forecast probabilities and eventual outcomes for later calibration review.

Calibration should refine the mapping rather than redefine the Net Index itself.

---

## 13. Acceptance Criteria for Spec B

Before Phase 5 implementation, the project must have:

1. a deterministic method for calculating the three probabilities;
2. a defined horizon-specific consolidation criterion;
3. a clear relationship between Net Index and the three probabilities;
4. valid probability normalization;
5. a defined signal-strength interpretation;
6. treatment for near-zero Net Index;
7. treatment for strong positive/negative Net Index;
8. a method for later calibration.

---

## 14. Guiding Principle

> **Net Index remains the transparent measure of net directional conviction. The three-state probability model is the decision surface that translates that conviction, together with range/consolidation conditions, into Bullish / Consolidation / Bearish probabilities.**

**End of Spec B — Draft for External Review**
```
