# Gold Probability Engine — Phase 1 Variable Registry
## Tranche 2 (T2) — Final Admission Records

**Status:** SIGNED OFF — 2026-08-17  
**Original sign-off date:** 2026-08-17  
**Original sign-off by:** Chris (Pragmatic Project Advisor)  
**Prepared by:** Grace (Task Agent)  
**Reviewed by:** Chris (Pragmatic Project Advisor)  
**Layers in scope:** Layer 4, Layer 5  
**Total candidates:** 16  
**ADMIT:** 12 | **CONDITIONAL / RESEARCH ONLY:** 4 | **REJECT:** 0

**Remediation note:** The registry was reopened after review identified an incorrect summary count, an inconsistent T3-baseline statement, and missing production-resolution conditions. No admission decision was changed by this remediation.

---

## Criterion B Baseline for T3

The T3 baseline is the full signed-off T1 approved registry in `docs/phase1-registry/T1-registry.md`. T2 candidates are not part of the T3 baseline until this reopened registry is reviewed and re-signed off. Every T3 candidate must demonstrate incremental information beyond T1 and flag any overlap with pending T2 candidates without treating those candidates as approved baseline variables.

T3 layers in scope: Layer 2 (USD & Global FX Regime) and Layer 7 (Global Liquidity & Financial Conditions).

---

## Amendment Applied at Sign-Off

**L5-006 upgraded from CONDITIONAL to ADMIT.** Rationale: asymmetrically admitting purchase flows (L5-001) but not sales/lending creates a one-sided Layer 5 that cannot signal de-accumulation regimes. Historical coverage (Washington Agreement, IMF sales, lending programs) is well-documented. Publication-lag and disclosure caveat applied matching L5-001.

---

## Open Items Carried Forward from T2

| ID | Item | Required Before |
|---|---|---|
| L4-003/004 | Breakevens interact with USD/FX in Layer 2 — Grace to flag during T3 assessment | T3 review |
| L4-005 | Survey methodology and source consistency must be established | Production admission |
| L4-010 | Incremental information vs. L1-005 Term Premium must be demonstrated | Production admission |
| L5-004 | Structured, retrievable source and Spec D compliance must be demonstrated | Production admission |
| L5-005 | Coverage improvement required before production admission | Production admission |

---

## Layer 4 — Inflation, Purchasing Power & Fiscal Credibility

### L4-001 — CPI Inflation Rate

* **Variable name:** CPI Inflation Rate
* **Layer:** 4
* **Variable ID:** L4-001
* **Causal mechanism:** Measures realized consumer-price inflation through the purchasing-power/debasement channel; persistent inflation can increase demand for gold as protection against erosion of fiat purchasing power.
* **Direction:** Conditional
* **Incremental information:** Provides the primary realized inflation measure for L4; adds current inflation information not contained in T1 real-rate or policy-expectation variables.
* **Overlap:** Core PCE Inflation Rate (L4-002) — **Duplicate candidate**; 5Y/10Y breakevens — **Transmission candidate**; L3-008 Inflation Surprise — **Transmission candidate**
* **Data/evidence source:** Official national inflation statistics.
* **Reliability:** High source authority and standardized methodology; revisions are generally limited but release calendars and methodological changes must be tracked.
* **Historical depth:** Very strong.
* **Frequency:** Monthly
* **Freshness:** Approximately one month; becomes stale as new releases arrive.
* **Accessibility:** Free / public
* **Operational burden:** Low
* **Relevant horizons:** 1–5 days; 1–3 months; 1–3 years — event-driven / cyclical
* **Initial weight rationale:** Primary L4 realized-inflation anchor; broad, timely, widely available, and directly measures purchasing-power erosion.
* **Evidence references:** T2 Brief; Causal Model v2.2 Layer 4.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Range Propensity candidate:** No

---

### L4-002 — Core PCE Inflation Rate

* **Variable name:** Core PCE Inflation Rate
* **Layer:** 4
* **Variable ID:** L4-002
* **Causal mechanism:** Measures persistent underlying inflation through the purchasing-power/debasement channel, excluding more volatile components.
* **Direction:** Conditional
* **Incremental information:** Complementary measure of persistent inflation conditions; supplementary L4 inflation anchor relative to CPI.
* **Overlap:** CPI Inflation Rate (L4-001) — **Duplicate candidate**; breakevens — **Transmission candidate**; L3-008 — **Transmission candidate**
* **Data/evidence source:** Official PCE inflation statistics.
* **Reliability:** High; authoritative source and established methodology.
* **Historical depth:** Strong.
* **Frequency:** Monthly
* **Freshness:** Approximately one month
* **Accessibility:** Free / public
* **Operational burden:** Low
* **Relevant horizons:** 1–3 months; 1–3 years — cyclical / structural
* **Initial weight rationale:** Supplementary to CPI; emphasizes persistent underlying inflation rather than broad headline consumer-price movement.
* **Evidence references:** T2 Brief; Causal Model v2.2 Layer 4.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Range Propensity candidate:** No

---

### L4-003 — 5Y Breakeven Inflation

* **Variable name:** 5Y Breakeven Inflation
* **Layer:** 4
* **Variable ID:** L4-003
* **Causal mechanism:** Measures market-implied medium-term inflation expectations through the forward-looking purchasing-power/debasement channel.
* **Direction:** Conditional
* **Incremental information:** Adds forward-looking inflation expectations that realized CPI/PCE do not provide.
* **Overlap:** 10Y Breakeven (L4-004) — **Duplicate candidate**; 5Y TIPS (L1-002) — **Transmission candidate**; 10Y TIPS (L1-001) — **Transmission candidate**; L3 policy-path variables — **Transmission candidate**
* **Data/evidence source:** Treasury inflation-linked securities market data.
* **Reliability:** Strong market-based input with transparent construction; breakevens embed liquidity and risk-premium effects.
* **Historical depth:** Strong for the TIPS era.
* **Frequency:** Daily
* **Freshness:** Hours to one day
* **Accessibility:** Free / public
* **Operational burden:** Low
* **Relevant horizons:** 1–3 months; 1–3 years — cyclical
* **Initial weight rationale:** Medium-term forward inflation anchor; retained separately from 10Y because the horizon and information content differ.
* **Evidence references:** T2 Brief; Causal Model v2.2 Layer 4.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Range Propensity candidate:** No

---

### L4-004 — 10Y Breakeven Inflation

* **Variable name:** 10Y Breakeven Inflation
* **Layer:** 4
* **Variable ID:** L4-004
* **Causal mechanism:** Measures longer-run market-implied inflation expectations through the long-horizon purchasing-power/debasement channel.
* **Direction:** Conditional
* **Incremental information:** Captures longer-horizon inflation expectations and potential persistent fiat-confidence risk not represented adequately by the 5Y measure.
* **Overlap:** 5Y Breakeven — **Duplicate candidate**; 10Y TIPS (L1-001) — **Transmission candidate**; L3 policy expectations — **Transmission candidate**
* **Data/evidence source:** Treasury inflation-linked securities market data.
* **Reliability:** Strong market source; contains liquidity and risk-premium components.
* **Historical depth:** Strong for the TIPS era.
* **Frequency:** Daily
* **Freshness:** Hours to one day
* **Accessibility:** Free / public
* **Operational burden:** Low
* **Relevant horizons:** 1–3 years; 3–10 years — structural / cyclical
* **Initial weight rationale:** Long-run debasement-risk anchor; survives separately from 5Y because the horizon distinction is economically material.
* **Evidence references:** T2 Brief; Causal Model v2.2 Layer 4.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Range Propensity candidate:** No

---

### L4-005 — Long-Run Survey Inflation Expectations

* **Variable name:** Long-Run Survey Inflation Expectations
* **Layer:** 4
* **Variable ID:** L4-005
* **Causal mechanism:** Captures long-run purchasing-power expectations through a non-market survey channel.
* **Direction:** Conditional
* **Incremental information:** Cross-checks market-implied breakevens using a different information source; avoids relying entirely on market pricing.
* **Overlap:** 10Y Breakeven — **Duplicate candidate**; 5Y Breakeven — **Transmission candidate**
* **Data/evidence source:** Established official or institutional inflation-expectation surveys.
* **Reliability:** Generally strong if the survey methodology is stable; survey revisions, sample composition, and response behavior require monitoring.
* **Historical depth:** Moderate to strong depending on selected survey.
* **Frequency:** Monthly / quarterly
* **Freshness:** Weeks to months
* **Accessibility:** Generally public
* **Operational burden:** Low
* **Relevant horizons:** 1–3 years; 3–10 years — structural
* **Initial weight rationale:** Useful independent cross-check; should not receive equal weight to market breakevens unless incremental predictive value is demonstrated.
* **Evidence references:** T2 Brief.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Range Propensity candidate:** No
* **Resolution condition:** Production admission requires a named survey source, documented methodology, stable retrieval, and a consistency review against the admitted market-based inflation-expectation variables.

---

### L4-006 — Fiscal Deficit / GDP

* **Variable name:** Fiscal Deficit / GDP
* **Layer:** 4
* **Variable ID:** L4-006
* **Causal mechanism:** Measures the scale of ongoing fiscal imbalance through the fiscal-credibility/debasement channel.
* **Direction:** Conditional
* **Incremental information:** Adds a direct fiscal-flow measure that T1 real-rate and policy variables do not capture.
* **Overlap:** Debt/GDP — **Transmission candidate**; Interest Expense/Revenue — **Transmission candidate**; Treasury Issuance — **Transmission candidate**
* **Data/evidence source:** Official fiscal statistics.
* **Reliability:** High for reported fiscal data; revisions and accounting differences require version control.
* **Historical depth:** Strong.
* **Frequency:** Monthly / quarterly / annual
* **Freshness:** Weeks to quarters
* **Accessibility:** Free / public
* **Operational burden:** Low
* **Relevant horizons:** 1–3 years; 3–10 years — structural
* **Initial weight rationale:** Core fiscal-pressure measure; interpretation should emphasize credibility rather than assume deficits are mechanically bullish for gold.
* **Evidence references:** T2 Brief; Causal Model v2.2 Layer 4.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Range Propensity candidate:** No

---

### L4-007 — Debt / GDP

* **Variable name:** Debt / GDP
* **Layer:** 4
* **Variable ID:** L4-007
* **Causal mechanism:** Measures accumulated sovereign leverage and structural fiscal vulnerability through the fiscal-credibility/debasement channel.
* **Direction:** Conditional
* **Incremental information:** Captures accumulated debt burden rather than annual fiscal flow.
* **Overlap:** Fiscal Deficit/GDP — **Transmission candidate**; Interest Expense/Revenue — **Transmission candidate**
* **Data/evidence source:** Official sovereign fiscal data.
* **Reliability:** High; gross/net debt definitions and national accounting conventions must be standardized.
* **Historical depth:** Strong.
* **Frequency:** Quarterly / annual
* **Freshness:** Months
* **Accessibility:** Free / public
* **Operational burden:** Low
* **Relevant horizons:** 1–3 years; 3–10 years — structural
* **Initial weight rationale:** Provides the stock dimension of fiscal sustainability; complements deficit flow measures.
* **Evidence references:** T2 Brief; Causal Model v2.2 Layer 4.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Range Propensity candidate:** No

---

### L4-008 — Interest Expense / Government Revenue

* **Variable name:** Interest Expense / Government Revenue
* **Layer:** 4
* **Variable ID:** L4-008
* **Causal mechanism:** Measures how much sovereign revenue is absorbed by debt servicing, directly indicating fiscal vulnerability and reduced policy flexibility.
* **Direction:** Conditional
* **Incremental information:** Provides a debt-service burden measure not captured by debt/GDP alone.
* **Overlap:** Debt/GDP — **Transmission candidate**; Fiscal Deficit/GDP — **Transmission candidate**; Treasury Maturity Structure — **Interaction candidate**
* **Data/evidence source:** Official government budget/fiscal reports.
* **Reliability:** Strong for reported data; comparability across periods requires accounting-definition controls.
* **Historical depth:** Strong for major sovereigns.
* **Frequency:** Quarterly / annual
* **Freshness:** Months
* **Accessibility:** Free / public
* **Operational burden:** Low
* **Relevant horizons:** 1–3 years; 3–10 years — structural
* **Initial weight rationale:** More directly tied to fiscal stress than debt/GDP alone; high-value complementary fiscal variable.
* **Evidence references:** T2 Brief.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Range Propensity candidate:** No

---

### L4-009 — Treasury Maturity Structure

* **Variable name:** Treasury Maturity Structure
* **Layer:** 4
* **Variable ID:** L4-009
* **Causal mechanism:** Measures refinancing concentration and maturity vulnerability, supporting the fiscal-credibility channel rather than simply measuring current interest rates.
* **Direction:** Conditional
* **Incremental information:** Adds refinancing-risk structure that debt/GDP and deficit/GDP cannot capture.
* **Overlap:** Treasury Term Premium (L1-005) — **Interaction candidate**; Treasury Issuance Volume (L4-010) — **Transmission candidate**; Debt/GDP — **Transmission candidate**
* **Data/evidence source:** Official Treasury debt-management and issuance data.
* **Reliability:** Strong primary source; definitions and maturity buckets are transparent.
* **Historical depth:** Strong.
* **Frequency:** Daily / monthly / auction schedule depending on measure
* **Freshness:** Days to weeks
* **Accessibility:** Free / public
* **Operational burden:** Low
* **Relevant horizons:** 1–3 months; 1–3 years; 3–10 years — structural / cyclical
* **Initial weight rationale:** Stronger fiscal-credibility case than issuance volume; captures refinancing vulnerability rather than market supply.
* **Evidence references:** T2 Brief.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Range Propensity candidate:** No

---

### L4-010 — Treasury Issuance Volume

* **Variable name:** Treasury Issuance Volume
* **Layer:** 4
* **Variable ID:** L4-010
* **Causal mechanism:** Measures near-term sovereign debt supply that can pressure financing conditions and influence perceptions of fiscal sustainability.
* **Direction:** Conditional
* **Incremental information:** Adds debt-supply volume; direct gold transmission is substantially mediated through market yields and term premium.
* **Overlap:** Treasury Maturity Structure — **Transmission candidate**; Treasury Term Premium (L1-005) — **Transmission candidate**; L3 policy expectations — **Transmission candidate**
* **Data/evidence source:** Official Treasury issuance schedules and results.
* **Reliability:** Very strong primary-source data.
* **Historical depth:** Strong.
* **Frequency:** Daily / weekly / monthly
* **Freshness:** Days
* **Accessibility:** Free / public
* **Operational burden:** Low
* **Relevant horizons:** 1–5 days; 1–3 months; 1–3 years — cyclical
* **Initial weight rationale:** Useful fiscal-supply signal but incremental information versus L1-005 is uncertain; retained for research rather than presupposed as a production driver.
* **Evidence references:** T2 Brief; Causal Model v2.2 Layer 4.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Range Propensity candidate:** No
* **Resolution condition:** Production admission requires demonstrating incremental information beyond L1-005 Treasury Term Premium and documenting the issuance-to-gold transmission mechanism.

---

## Layer 5 — Official-Sector Reserve Allocation

### L5-001 — Monthly Official-Sector Gold Purchase Volume

* **Variable name:** Monthly Official-Sector Gold Purchase Volume
* **Layer:** 5
* **Variable ID:** L5-001
* **Causal mechanism:** Measures the physical gold accumulation component of official reserve allocation and therefore the actual strategic demand flow.
* **Direction:** Positive
* **Incremental information:** Adds realized official-sector purchase flow beyond L0-002's stock-level holdings.
* **Overlap:** L0-002 Central-Bank Gold Holdings — **Transmission candidate**
* **Data/evidence source:** Official central-bank disclosures and established institutional gold-market datasets.
* **Reliability:** Strong at aggregate level; publication lags and later revisions are important operational constraints.
* **Historical depth:** Good for recent decades; coverage varies across countries.
* **Frequency:** Monthly / quarterly
* **Freshness:** Weeks to months
* **Accessibility:** Generally public / mixed for some institutions
* **Operational burden:** Medium
* **Relevant horizons:** 1–3 months; 1–3 years; 3–10 years — structural / cyclical
* **Initial weight rationale:** Core realized official-demand-flow anchor; distinct from stock holdings.
* **Evidence references:** T2 Brief; Causal Model v2.2 Layer 5.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Range Propensity candidate:** No

---

### L5-002 — Gold Share of Official Reserves

* **Variable name:** Gold Share of Official Reserves
* **Layer:** 5
* **Variable ID:** L5-002
* **Causal mechanism:** Measures strategic allocation weight toward gold rather than absolute gold ownership.
* **Direction:** Positive
* **Incremental information:** Distinguishes active reserve-allocation preference from the quantity of gold already held.
* **Overlap:** L0-002 Central-Bank Gold Holdings — **Transmission candidate**; Reserve Composition Change — **Duplicate candidate**
* **Data/evidence source:** Official reserve data / institutional reserve-composition datasets.
* **Reliability:** Strong where reported; coverage varies by jurisdiction.
* **Historical depth:** Moderate to strong.
* **Frequency:** Monthly / quarterly / annual
* **Freshness:** Weeks to months
* **Accessibility:** Mixed / public for many major institutions
* **Operational burden:** Medium
* **Relevant horizons:** 1–3 years; 3–10 years — structural
* **Initial weight rationale:** Captures strategic allocation intensity; complements realized purchase flows.
* **Evidence references:** T2 Brief.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Range Propensity candidate:** No
* **Valuation-control requirement:** Production use must distinguish active reserve-allocation changes from mechanical changes in gold's market value; the variable must not be treated as evidence of new buying without a flow or composition adjustment.

---

### L5-003 — Reserve Composition Change / USD Share Change

* **Variable name:** Reserve Composition Change / USD Share Change
* **Layer:** 5
* **Variable ID:** L5-003
* **Causal mechanism:** Captures broader reserve-allocation changes and distinguishes gold accumulation from changing dependence on USD assets.
* **Direction:** Conditional
* **Incremental information:** Directly measures portfolio-composition change rather than gold ownership level.
* **Overlap:** Gold Share of Official Reserves — **Duplicate candidate**; L5-001 — **Transmission candidate**; stated reserve objectives — **Transmission candidate**
* **Data/evidence source:** Official reserve-composition statistics and institutional reserve datasets.
* **Reliability:** Useful but less complete than gold-purchase data; reserve composition can be partially undisclosed.
* **Historical depth:** Moderate.
* **Frequency:** Quarterly / annual
* **Freshness:** Months
* **Accessibility:** Mixed / some restricted components
* **Operational burden:** Medium
* **Relevant horizons:** 1–3 years; 3–10 years — structural
* **Initial weight rationale:** Adds the broader diversification context needed to avoid misinterpreting every gold purchase as de-dollarization.
* **Evidence references:** T2 Brief's explicit distinction among diversification and de-dollarization.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Range Propensity candidate:** No
* **Boundary requirement:** Production interpretation must distinguish gold accumulation, non-gold currency diversification, sanctions/reserve-security hedging, and broader monetary fragmentation. A falling USD share alone is not evidence of gold allocation or de-dollarization.

---

### L5-004 — Central-Bank Reserve Objectives & Allocation Intent

* **Variable name:** Central-Bank Reserve Objectives & Allocation Intent
* **Layer:** 5
* **Variable ID:** L5-004
* **Causal mechanism:** Structured interpretation of official statements and survey evidence covering reserve diversification, de-dollarization, sanctions-risk hedging, reserve security, and broader monetary-system fragmentation.
* **Direction:** Conditional
* **Incremental information:** Captures why official institutions allocate toward gold, which realized purchase/holdings data cannot directly reveal.
* **Overlap:** L5-001 purchase volume — **Transmission candidate**; L5-002 gold share — **Transmission candidate**; L5-003 reserve composition — **Transmission candidate**; L0-002 holdings — **Transmission candidate**
* **Data/evidence source:** Official central-bank statements, reserve-policy publications, and structured institutional survey evidence where consistently retrievable.
* **Reliability:** Primary-source statements are authoritative as statements of intent but do not prove actual behavior; interpretation must follow Spec D evidence, counter-evidence, timestamps, provenance, and fact-vs-interpretation separation.
* **Historical depth:** Moderate; quality varies substantially by institution and period.
* **Frequency:** Event-driven / quarterly / annual
* **Freshness:** Weeks to months
* **Accessibility:** Public but uneven
* **Operational burden:** High
* **Relevant horizons:** 1–3 years; 3–10 years — structural / conditional
* **Initial weight rationale:** Captures strategic intent unavailable from quantitative holdings data; interpretive burden warrants conservative initial treatment.
* **Evidence references:** T2 Brief; Spec D analytical-variable requirements.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Range Propensity candidate:** No
* **Resolution condition:** Production admission requires a structured, retrievable source set and a Spec D-compliant evidence record separating official facts, stated intent, interpretation, counter-evidence, and confidence.
* **Consolidation note:** Central-Bank Stated Reserve Objectives and Central-Bank Gold-Allocation Survey Responses are consolidated into this single analytical variable because both primarily measure official-sector allocation intent.

---

### L5-005 — Domestic vs. Foreign Gold Custody

* **Variable name:** Domestic vs. Foreign Gold Custody
* **Layer:** 5
* **Variable ID:** L5-005
* **Causal mechanism:** Captures the reserve-security dimension of official allocation by indicating whether institutions favor domestic control over foreign custody.
* **Direction:** Conditional
* **Incremental information:** Adds custody/security preference that purchase volumes and reserve shares cannot directly observe.
* **Overlap:** Central-Bank Reserve Objectives & Allocation Intent — **Transmission candidate**; L5-003 — **Transmission candidate**
* **Data/evidence source:** Official central-bank disclosures and custody statements.
* **Reliability:** High when officially disclosed; coverage is sparse and changes are infrequent.
* **Historical depth:** Limited / uneven.
* **Frequency:** Event-driven / irregular
* **Freshness:** Months to years
* **Accessibility:** Mixed
* **Operational burden:** Medium
* **Relevant horizons:** 1–3 years; 3–10 years — structural
* **Initial weight rationale:** Mechanistically distinct reserve-security signal; limited coverage prevents treating it as a dominant production input.
* **Evidence references:** T2 Brief; Causal Model v2.2 Layer 5.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Range Propensity candidate:** No
* **Resolution condition:** Production admission requires materially improved coverage, a stable source, and a documented rule distinguishing custody/security information from a generic geopolitical signal.

---

### L5-006 — Official-Sector Gold Sales / Lending

* **Variable name:** Official-Sector Gold Sales / Lending
* **Layer:** 5
* **Variable ID:** L5-006
* **Causal mechanism:** Measures active official-sector reduction or mobilization of gold reserves and therefore the supply side of strategic reserve allocation.
* **Direction:** Negative
* **Incremental information:** Captures official-sector selling/lending behavior not represented by net purchase flows alone.
* **Overlap:** L5-001 purchases — **Duplicate candidate** if represented only as net flow; L0-002 holdings — **Transmission candidate**
* **Data/evidence source:** Official disclosures and institutional gold-market reporting where transactions are observable.
* **Reliability:** Strong when disclosed; incomplete because many transactions are not publicly observable at high frequency. Publication-lag and disclosure caveat apply matching L5-001.
* **Historical depth:** Moderate; Washington Agreement, IMF sales, and lending programs are well-documented.
* **Frequency:** Event-driven / monthly / quarterly
* **Freshness:** Weeks to months
* **Accessibility:** Mixed
* **Operational burden:** Medium
* **Relevant horizons:** 1–3 months; 1–3 years — cyclical / structural
* **Initial weight rationale:** Captures the opposite side of official allocation; asymmetrically admitting purchases but not sales would create a one-sided Layer 5.
* **Evidence references:** T2 Brief.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Range Propensity candidate:** No
* **Amendment note:** Upgraded from CONDITIONAL to ADMIT at sign-off. Rationale: same disclosure and publication-lag constraints apply to L5-001 which was admitted; historical coverage is sufficient; omitting sales creates structural one-sidedness in Layer 5.

---

## Range Propensity Screening Note

All T2 variables are marked **No** for direct Range Propensity use. This is intentional: T2 variables describe inflation, fiscal credibility, and official-sector reserve allocation, not the observable current range/volatility state specified by Spec B. They may condition interpretation of range behavior, but they are not direct inputs to the deterministic Range Propensity composite. Candidate inputs remain reserved for approved Layer 7, Layer 10, and other market-state variables evaluated in later tranches.

## T2 Summary Table

| Variable ID | Variable Name | Decision | Overlap Flags | Horizons | Range Propensity |
|---|---|---|---|---|---|
| L4-001 | CPI Inflation Rate | ADMIT | Duplicate / Transmission | 1–5D, 1–3M, 1–3Y | No |
| L4-002 | Core PCE Inflation Rate | ADMIT | Duplicate / Transmission | 1–3M, 1–3Y | No |
| L4-003 | 5Y Breakeven Inflation | ADMIT | Duplicate / Transmission | 1–3M, 1–3Y | No |
| L4-004 | 10Y Breakeven Inflation | ADMIT | Duplicate / Transmission | 1–3Y, 3–10Y | No |
| L4-005 | Long-Run Survey Inflation Expectations | CONDITIONAL | Duplicate / Transmission | 1–3Y, 3–10Y | No |
| L4-006 | Fiscal Deficit / GDP | ADMIT | Transmission | 1–3Y, 3–10Y | No |
| L4-007 | Debt / GDP | ADMIT | Transmission | 1–3Y, 3–10Y | No |
| L4-008 | Interest Expense / Government Revenue | ADMIT | Transmission / Interaction | 1–3Y, 3–10Y | No |
| L4-009 | Treasury Maturity Structure | ADMIT | Interaction / Transmission | 1–3M, 1–3Y, 3–10Y | No |
| L4-010 | Treasury Issuance Volume | CONDITIONAL | Transmission | 1–5D, 1–3M, 1–3Y | No |
| L5-001 | Monthly Official-Sector Gold Purchase Volume | ADMIT | Transmission | 1–3M, 1–3Y, 3–10Y | No |
| L5-002 | Gold Share of Official Reserves | ADMIT | Transmission | 1–3Y, 3–10Y | No |
| L5-003 | Reserve Composition Change / USD Share Change | ADMIT | Duplicate / Transmission | 1–3Y, 3–10Y | No |
| L5-004 | Central-Bank Reserve Objectives & Allocation Intent | CONDITIONAL | Transmission | 1–3Y, 3–10Y | No |
| L5-005 | Domestic vs. Foreign Gold Custody | CONDITIONAL | Transmission | 1–3Y, 3–10Y | No |
| L5-006 | Official-Sector Gold Sales / Lending | ADMIT | Duplicate / Transmission | 1–3M, 1–3Y | No |

---

## T2 Cross-Layer Notes for T3

- L4-001/L4-002: CPI is the primary L4 realized-inflation anchor; Core PCE is supplementary. Neither operates through L3's policy-repricing mechanism.
- L4-003/L4-004: Breakevens are L4 forward purchasing-power variables. USD strength (Layer 2) compresses breakevens mechanically — Grace must flag this interaction during T3 Layer 2 assessment.
- L4-009: Maturity structure belongs to fiscal credibility; L1-005 Treasury Term Premium remains the market-pricing transmission variable.
- L4-010: Issuance volume is conditional because gold effect is heavily mediated through yields/term premium.
- L5-001 vs L0-002: Official purchase flow is Layer 5; official gold stock remains Layer 0.
- L5-004: The consolidated qualitative variable captures intent, not realized allocation. Must remain auditable under Spec D standards.
- L5-003: Reserve diversification must not be treated as synonymous with de-dollarization.
- L5-005: Custody is specifically a reserve-security signal; must not be transformed into a generic geopolitical variable in T4.
