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
