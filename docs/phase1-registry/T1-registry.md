# Gold Probability Engine — Phase 1 Variable Registry
## Tranche 1 (T1) — Final Admission Records

**Status:** SIGNED OFF — 2026-08-17  
**Original sign-off date:** 2026-08-17  
**Original sign-off by:** Chris (Pragmatic Project Advisor)  
**Prepared by:** Grace (Task Agent)  
**Reviewed by:** Chris (Pragmatic Project Advisor)  
**Layers in scope:** Layer 0, Layer 1, Layer 3  
**Total candidates:** 24  
**ADMIT:** 18 | **CONDITIONAL / RESEARCH ONLY:** 6 | **REJECT:** 0

**Remediation note:** The registry was reopened after review identified an incorrect summary count and missing production-boundary/source controls. No admission decision was changed by this remediation.

---

## Criterion B Baseline for T2

The T2 baseline is the full T1 approved registry below. Every T2 candidate must demonstrate incremental information beyond the variables admitted here.

---

## Open Items Carried Forward

| ID | Item | Required Before |
|---|---|---|
| L0-009 | Stable, verified gold lease/forward-rate source and licensing must be confirmed | Phase 2 |
| L0-001 | Name and validate the production above-ground-stock source, methodology, and revision policy | Phase 2 |
| L1-004 | Must demonstrate incremental information beyond slope of L1-001 minus L1-002 | Production admission |
| L1-005 | Name the production term-premium model/series and preserve its methodology and revisions | Phase 2 |
| L1-006 | Restrict production use to current real-opportunity-cost decomposition; reclassify to L3 if used for forward-path repricing | Scoring engine implementation |
| L3-001/002 | Designate primary Layer 3 quantitative anchor to prevent double-weighting | Spec A implementation |
| L1-006/L3-001/002 | Designate the primary policy-rate source and document the non-overlapping role of L1-006 versus L3-001/002 | Spec A implementation |
| L3-008 | Production source must preserve point-in-time consensus vintage | Production admission |

---

## Layer 0 — Gold's Stock/Flow Monetary Architecture

### L0-001 — Above-Ground Gold Stock

* **Variable name:** Above-Ground Gold Stock
* **Layer:** 0
* **Variable ID:** L0-001
* **Causal mechanism:** Measures the accumulated existing gold stock; because most previously mined gold remains available, marginal-holder behavior matters more than annual mine supply alone.
* **Direction:** Conditional
* **Incremental information:** Establishes the structural stock base against which all flow variables must be interpreted; no other candidate directly represents the scale of the existing stock.
* **Overlap:** Gold holdings — **Transmission candidate**; recycling flow — **Transmission candidate**
* **Data/evidence source:** Gold-market stock estimates and institutional industry research; exact production source to be finalized during implementation.
* **Reliability:** Conceptually strong, but total-stock estimates require methodology assumptions and periodic revisions.
* **Historical depth:** Long historical reconstruction possible, but precision varies by period.
* **Frequency:** Annual / irregular structural updates
* **Freshness:** Slow-moving; generally remains useful for years.
* **Accessibility:** Mixed / source-dependent
* **Operational burden:** Low
* **Relevant horizons:** 1–3 years; 3–10 years — structural
* **Initial weight rationale:** Foundational architecture variable; should have meaningful structural representation but is not itself a high-frequency price signal.
* **Evidence references:** Causal Model v2.2 Layer 0; T1 Brief.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

---

### L0-002 — Central-Bank Gold Holdings

* **Variable name:** Central-Bank Gold Holdings
* **Layer:** 0
* **Variable ID:** L0-002
* **Causal mechanism:** Measures the official-sector portion of the existing stock and therefore the strategic ownership base that may be relatively less price-sensitive than tactical investors.
* **Direction:** Conditional
* **Incremental information:** Adds ownership composition to total-stock measurement; distinct from Layer 5's reserve-allocation behavior.
* **Overlap:** Official-sector reserve allocation — **Transmission candidate**; above-ground stock — **Duplicate candidate** if used as a stock total without ownership decomposition.
* **Data/evidence source:** Official central-bank disclosures / institutional gold-market datasets.
* **Reliability:** Generally strong where holdings are officially reported; disclosure timing and coverage vary.
* **Historical depth:** Good for major reporting countries; uneven for some jurisdictions.
* **Frequency:** Monthly / quarterly / irregular depending on issuer
* **Freshness:** Months
* **Accessibility:** Mixed / largely public for disclosed holdings
* **Operational burden:** Medium
* **Relevant horizons:** 1–3 months; 1–3 years; 3–10 years — structural
* **Initial weight rationale:** Useful decomposition of the stock; should not be allowed to duplicate Layer 5 demand signals.
* **Evidence references:** Causal Model v2.2; Handoff official-sector distinction.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

---

### L0-003 — Gold ETF Holdings

* **Variable name:** Gold ETF Holdings
* **Layer:** 0
* **Variable ID:** L0-003
* **Causal mechanism:** Measures gold held through investment vehicles and identifies a potentially mobile component of the existing stock.
* **Direction:** Conditional
* **Incremental information:** Adds ownership/mobility information to Layer 0; differs from Layer 8 flows by measuring the stock of ETF-held gold rather than the weekly flow.
* **Overlap:** Investment flows — **Transmission candidate**; ETF flow — **Transmission candidate**
* **Data/evidence source:** Fund-reported holdings / established market datasets.
* **Reliability:** Generally strong for large funds, with routine publication; methodology is comparatively transparent.
* **Historical depth:** Good for major products; shorter than physical-market history.
* **Frequency:** Daily
* **Freshness:** Days
* **Accessibility:** Generally public / crawlable
* **Operational burden:** Low
* **Relevant horizons:** 1–5 days; 1–3 months; 1–3 years — cyclical
* **Initial weight rationale:** Important mobile-stock indicator; should remain distinct from flow variables.
* **Evidence references:** Causal Model v2.2 Layer 0 and Layer 8; T1 Brief.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

---

### L0-004 — Household / Jewelry Gold Stock

* **Variable name:** Household / Jewelry Gold Stock
* **Layer:** 0
* **Variable ID:** L0-004
* **Causal mechanism:** Represents privately held physical gold that can remain inactive or become a recycling/selling reservoir.
* **Direction:** Conditional
* **Incremental information:** Captures the non-financial ownership reservoir not represented by ETF or official holdings.
* **Overlap:** Gold recycling — **Transmission candidate**; bar-and-coin holdings — **Duplicate candidate**
* **Data/evidence source:** Industry estimates, national-market studies, physical-demand datasets.
* **Reliability:** Conceptually useful but measurement is less precise than listed financial holdings.
* **Historical depth:** Uneven across countries and historical periods.
* **Frequency:** Annual / irregular
* **Freshness:** Months to years
* **Accessibility:** Mixed / partly restricted
* **Operational burden:** Medium
* **Relevant horizons:** 1–3 years; 3–10 years — structural
* **Initial weight rationale:** Important conceptually, but measurement uncertainty limits weight until implementation-quality data is demonstrated.
* **Evidence references:** Causal Model v2.2 Layer 0.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

---

### L0-005 — Bar-and-Coin Investment Holdings / Demand

* **Variable name:** Bar-and-Coin Investment Holdings / Demand
* **Layer:** 0
* **Variable ID:** L0-005
* **Causal mechanism:** Represents physically held investment gold that may move between inactive ownership and active acquisition/sale.
* **Direction:** Positive
* **Incremental information:** More directly observable than the full household/jewelry stock and provides a practical physical-investment ownership signal.
* **Overlap:** Household/jewelry stock — **Duplicate candidate**; regional physical markets — **Transmission candidate**
* **Data/evidence source:** Institutional physical-demand datasets and national-market sources.
* **Reliability:** Generally useful, though household inventories are not directly observable.
* **Historical depth:** Good for recent decades; less complete for older periods.
* **Frequency:** Quarterly / annual
* **Freshness:** Months
* **Accessibility:** Mixed
* **Operational burden:** Medium
* **Relevant horizons:** 1–3 months; 1–3 years; 3–10 years — cyclical / structural
* **Initial weight rationale:** Preferable to trying to estimate the entire household stock; provides observable investment-ownership information.
* **Evidence references:** Causal Model v2.2 Layer 0; Regional Physical Markets.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

---

### L0-006 — Gold Recycling Flow

* **Variable name:** Gold Recycling Flow
* **Layer:** 0
* **Variable ID:** L0-006
* **Causal mechanism:** Measures active liquidation of existing gold stock into the market; a direct flow from stock to supply.
* **Direction:** Negative
* **Incremental information:** Converts the otherwise static stock architecture into an observable marginal-supply signal.
* **Overlap:** Household/jewelry stock — **Transmission candidate**; physical demand — **Transmission candidate**
* **Data/evidence source:** Institutional recycling estimates / physical-market data.
* **Reliability:** Established concept with reasonable aggregate estimates, but lag and estimation issues exist.
* **Historical depth:** Multi-decade availability, with quality varying by source and geography.
* **Frequency:** Quarterly / annual; some market indicators may be more frequent
* **Freshness:** Months
* **Accessibility:** Mixed
* **Operational burden:** Medium
* **Relevant horizons:** 1–3 months; 1–3 years — cyclical
* **Initial weight rationale:** One of the clearest observable stock-mobilization channels.
* **Evidence references:** Causal Model v2.2 Layer 0; Handoff stock/flow principle.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

---

### L0-007 — Producer Hedging

* **Variable name:** Producer Hedging
* **Layer:** 0
* **Variable ID:** L0-007
* **Causal mechanism:** Miner hedging can move expected future production into financial-market supply and alter available forward supply.
* **Direction:** Negative
* **Incremental information:** Captures producer behavior that is not represented by mine output alone.
* **Overlap:** Gold forwards / lease rates — **Transmission candidate**; market microstructure — **Transmission candidate**
* **Data/evidence source:** Producer disclosures and institutional mining/market datasets.
* **Reliability:** Useful where disclosed but not uniformly transparent across producers.
* **Historical depth:** Multi-decade but inconsistent at aggregate level.
* **Frequency:** Quarterly / annual / event-driven
* **Freshness:** Months
* **Accessibility:** Mixed
* **Operational burden:** Medium
* **Relevant horizons:** 1–3 months; 1–3 years — cyclical / structural
* **Initial weight rationale:** Adds a distinct producer-response channel to stock/flow analysis.
* **Evidence references:** Causal Model v2.2 Layer 0.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

---

### L0-008 — Vaulted vs. Potentially Mobile Gold

* **Variable name:** Vaulted vs. Potentially Mobile Gold
* **Layer:** 0
* **Variable ID:** L0-008
* **Causal mechanism:** Attempts to distinguish nominal stock from gold plausibly available to enter the market.
* **Direction:** Conditional
* **Incremental information:** Directly targets the marginal-holder/mobility concept rather than merely measuring total holdings.
* **Overlap:** Above-ground stock — **Transmission candidate**; ETF holdings — **Transmission candidate**; lease/forward rates — **Interaction candidate**
* **Data/evidence source:** Vault, exchange, OTC and institutional market-structure data where observable.
* **Reliability:** Potentially valuable but coverage is incomplete and "mobile" stock is difficult to observe directly.
* **Historical depth:** Limited / uneven
* **Frequency:** Irregular / source-dependent
* **Freshness:** Weeks to months where data exists
* **Accessibility:** Restricted / mixed
* **Operational burden:** High
* **Relevant horizons:** 1–3 months; 1–3 years — conditional
* **Initial weight rationale:** Mechanistically attractive but currently too difficult to observe consistently for production.
* **Evidence references:** Causal Model v2.2 Layer 0; Part VI gold-as-collateral research direction.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

---

### L0-009 — Gold Lease Rates / Forward Rates

* **Variable name:** Gold Lease Rates / Forward Rates
* **Layer:** 0
* **Variable ID:** L0-009
* **Causal mechanism:** Measures the cost/conditions of borrowing and financing physical gold into the market, providing information about stock mobility and bullion-market tightness.
* **Direction:** Conditional
* **Incremental information:** Adds a market-observable measure of physical-stock accessibility and financing stress; distinct from L1 financial opportunity cost.
* **Overlap:** Vaulted vs. Potentially Mobile Gold — **Interaction candidate**; Producer Hedging — **Transmission candidate**; financial opportunity cost — **Duplicate candidate** only if interpreted incorrectly as a rates substitute.
* **Data/evidence source:** Gold lease, forward, swap and bullion-market data where reliably available.
* **Reliability:** Economically relevant, with public-data transparency and source coverage requiring validation.
* **Historical depth:** Partial; depth depends on the specific series.
* **Frequency:** Daily / market-dependent
* **Freshness:** Days
* **Accessibility:** Restricted / mixed
* **Operational burden:** High
* **Relevant horizons:** 1–5 days; 1–3 months; 1–3 years — cyclical / conditional
* **Initial weight rationale:** Strong causal relevance and direct measurement of physical-stock financing stress justify admission despite source-access limitations.
* **Evidence references:** Causal Model v2.2 Part VI Section 2; T1 candidate approval.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Mandatory source-locking note:** Production use is contingent on a stable, verified data source being confirmed before Phase 2.

---

## Layer 1 — Real Interest Rates & Opportunity Cost

### L1-001 — 10Y TIPS Real Yield

* **Variable name:** 10Y TIPS Real Yield
* **Layer:** 1
* **Variable ID:** L1-001
* **Causal mechanism:** Measures the real yield available from a major competing high-quality asset; higher real return generally raises gold's opportunity cost.
* **Direction:** Negative
* **Incremental information:** Core benchmark for current long-duration real opportunity cost.
* **Overlap:** 5Y TIPS — **Duplicate candidate**; 5Y5Y forward real rate — **Interaction candidate**; expected policy rate — **Transmission candidate**
* **Data/evidence source:** US Treasury / Federal Reserve market data.
* **Reliability:** Strong primary institutional source, high consistency and transparent methodology.
* **Historical depth:** Good for modern TIPS era; limited before TIPS.
* **Frequency:** Daily
* **Freshness:** Hours to one day
* **Accessibility:** Free / public
* **Operational burden:** Low
* **Relevant horizons:** All four — cyclical / structural
* **Initial weight rationale:** Primary Layer 1 anchor with broad horizon applicability.
* **Evidence references:** Causal Model v2.2 Layer 1; Handoff core-scoring framework.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

---

### L1-002 — 5Y TIPS Real Yield

* **Variable name:** 5Y TIPS Real Yield
* **Layer:** 1
* **Variable ID:** L1-002
* **Causal mechanism:** Measures shorter/intermediate current real opportunity cost.
* **Direction:** Negative
* **Incremental information:** Adds maturity-specific information to the 10Y measure, particularly relevant when front/intermediate real rates diverge from long rates.
* **Overlap:** 10Y TIPS — **Duplicate candidate**; 5Y5Y forward real rate — **Interaction candidate**
* **Data/evidence source:** US Treasury / institutional market data.
* **Reliability:** Strong and consistently measured.
* **Historical depth:** Good for TIPS era.
* **Frequency:** Daily
* **Freshness:** Hours to one day
* **Accessibility:** Free / public
* **Operational burden:** Low
* **Relevant horizons:** 1–5 days; 1–3 months; 1–3 years — cyclical
* **Initial weight rationale:** Retain because maturity shape can carry incremental information rather than relying on the 10Y alone.
* **Evidence references:** Causal Model v2.2 Layer 1; T1 Brief.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

---

### L1-003 — Forward Real Rates

* **Variable name:** Forward Real Rates
* **Layer:** 1
* **Variable ID:** L1-003
* **Causal mechanism:** Measures implied real-rate conditions over future intervals rather than only current maturity yields.
* **Direction:** Negative
* **Incremental information:** Captures the term structure of current/implied real opportunity cost and can distinguish spot from forward conditions.
* **Overlap:** 5Y/10Y TIPS — **Transmission candidate**; 5Y5Y forward real rate — **Duplicate candidate** where identical construction is used.
* **Data/evidence source:** Derived from Treasury/institutional yield and inflation-linked market data.
* **Reliability:** Strong where construction is transparent; quality depends on methodology.
* **Historical depth:** TIPS-era dependent.
* **Frequency:** Daily / derived
* **Freshness:** Hours to one day
* **Accessibility:** Free / derivable using public inputs
* **Operational burden:** Medium
* **Relevant horizons:** 1–3 months; 1–3 years; 3–10 years — structural / cyclical
* **Initial weight rationale:** Adds curve information not captured by individual spot maturities.
* **Evidence references:** Causal Model v2.2 Layer 1 observable categories.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

---

### L1-004 — Real Yield Curve / Slope

* **Variable name:** Real Yield Curve / Slope
* **Layer:** 1
* **Variable ID:** L1-004
* **Causal mechanism:** Measures where real-rate opportunity-cost pressure is concentrated across maturities.
* **Direction:** Conditional
* **Incremental information:** A curve shape can change the interpretation of a single real-yield level, but its incremental production value must be demonstrated against admitted component variables.
* **Overlap:** 5Y TIPS Real Yield (L1-002) + 10Y TIPS Real Yield (L1-001) — **Duplicate candidate**; Forward Real Rates — **Duplicate candidate**
* **Data/evidence source:** Derived from institutional real-yield curves.
* **Reliability:** Strong inputs; derived measure depends on construction.
* **Historical depth:** TIPS-era dependent.
* **Frequency:** Daily
* **Freshness:** Hours to one day
* **Accessibility:** Free / derivable
* **Operational burden:** Low
* **Relevant horizons:** 1–3 months; 1–3 years; 3–10 years — cyclical / structural
* **Initial weight rationale:** Potentially useful as a shape measure, but directly derived from admitted L1-001 and L1-002; requires proof of incremental information before production.
* **Evidence references:** Causal Model v2.2 Layer 1; T1 Brief.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Implementation requirement:** Production admission requires demonstrating incremental information beyond the slope implied by L1-001 minus L1-002.

---

### L1-005 — Treasury Term Premium

* **Variable name:** Treasury Term Premium
* **Layer:** 1
* **Variable ID:** L1-005
* **Causal mechanism:** Measures compensation for holding long-duration nominal Treasuries beyond expected short rates, affecting relative attractiveness of duration versus gold.
* **Direction:** Conditional
* **Incremental information:** Distinguishes duration compensation from expected short-rate conditions.
* **Overlap:** 10Y real yield — **Transmission candidate**; expected policy rate — **Transmission candidate**
* **Data/evidence source:** Institutional/model-derived Treasury term-premium estimates.
* **Reliability:** Useful but model-dependent; not directly observed.
* **Historical depth:** Substantial for established model series, methodology-dependent.
* **Frequency:** Daily
* **Freshness:** Daily
* **Accessibility:** Generally public for established model series
* **Operational burden:** Low
* **Relevant horizons:** 1–3 months; 1–3 years — cyclical
* **Initial weight rationale:** Valuable decomposition of the 10Y opportunity-cost signal, but model dependence argues for a moderate initial role.
* **Evidence references:** Causal Model v2.2 Layer 1 observable categories.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

---

### L1-006 — Expected Policy Rate

* **Variable name:** Expected Policy Rate
* **Layer:** 1
* **Variable ID:** L1-006
* **Causal mechanism:** In Layer 1, represents the expected policy-rate component embedded in the current real opportunity-cost environment — the rate component against which current inflation expectations and asset yields are being priced. Layer 3 separately captures revisions in the future policy path.
* **Direction:** Negative
* **Incremental information:** Provides the policy-rate component needed to interpret current real opportunity cost; Layer 3 uses policy expectations specifically as a change/repricing in the forward path.
* **Overlap:** Layer 3 Fed Funds/OIS expectations — **Transmission candidate**; 10Y/5Y TIPS — **Transmission candidate**
* **Data/evidence source:** Market-implied policy-rate data / official policy information.
* **Reliability:** Strong where market-implied rates are available; interpretation must preserve the L1/L3 mechanism distinction.
* **Historical depth:** Modern market-based history; longer historical policy data exists but is not directly equivalent.
* **Frequency:** Daily / event-driven
* **Freshness:** Hours to one day
* **Accessibility:** Generally public
* **Operational burden:** Low
* **Relevant horizons:** 1–5 days; 1–3 months; 1–3 years — cyclical
* **Initial weight rationale:** Retain because it decomposes current real opportunity cost; forward-path repricing belongs in L3.
* **Evidence references:** T1 Brief L1/L3 distinction.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Implementation monitor note:** If the production system uses this variable to signal forward-path repricing rather than current opportunity-cost decomposition, its contribution must be reclassified to L3 at that point.
* **Boundary requirement:** Before scoring-engine implementation, document the distinct L1 decomposition role of L1-006 and prevent it from receiving an independent full policy-expectation contribution alongside L3-001/L3-002.

---

### L1-007 — 5Y5Y Forward Real Rate

* **Variable name:** 5Y5Y Forward Real Rate
* **Layer:** 1
* **Variable ID:** L1-007
* **Causal mechanism:** Measures market-implied real rates for the five-year period beginning five years forward, representing a structurally longer opportunity-cost expectation than spot TIPS yields.
* **Direction:** Negative
* **Incremental information:** Adds a specific long-forward real-rate horizon that is not equivalent to today's 5Y/10Y real yield.
* **Overlap:** Forward real rates — **Duplicate candidate** if broader forward series includes the same point; 10Y TIPS — **Interaction candidate**
* **Data/evidence source:** Derived market-based real-rate data.
* **Reliability:** Economically useful, but methodology and inflation-linked term-structure construction must be validated.
* **Historical depth:** Modern TIPS-era only.
* **Frequency:** Daily
* **Freshness:** Hours to one day
* **Accessibility:** Free / derivable where inputs are public
* **Operational burden:** Medium
* **Relevant horizons:** 1–3 years; 3–10 years — structural / cyclical
* **Initial weight rationale:** Explicitly approved because it represents a structurally distinct long-forward opportunity-cost horizon.
* **Evidence references:** T1 candidate approval; Causal Model v2.2 Layer 1 forward-real-rate category.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

---

## Layer 3 — Monetary Policy Expectations

### L3-001 — Fed Funds Futures Expected Policy Rate

* **Variable name:** Fed Funds Futures Expected Policy Rate
* **Layer:** 3
* **Variable ID:** L3-001
* **Causal mechanism:** Market-implied expected path of Fed policy; repricing changes expected future real rates and liquidity conditions.
* **Direction:** Negative
* **Incremental information:** Direct, timely market measure of policy-path expectations and repricing.
* **Overlap:** OIS curve — **Duplicate candidate**; expected terminal rate — **Transmission candidate**; Layer 1 expected policy rate — **Transmission candidate**
* **Data/evidence source:** Fed funds futures market.
* **Reliability:** Strong market-based signal; affected by market microstructure and contract-specific details.
* **Historical depth:** Good for modern futures era.
* **Frequency:** Intraday / daily
* **Freshness:** Hours
* **Accessibility:** Mixed / market-data dependent
* **Operational burden:** Low to Medium
* **Relevant horizons:** 1–5 days; 1–3 months; 1–3 years — event-driven / cyclical
* **Initial weight rationale:** Primary Layer 3 quantitative anchor.
* **Evidence references:** Causal Model v2.2 Layer 3; T1 Brief.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

---

### L3-002 — OIS Forward Policy Curve

* **Variable name:** OIS Forward Policy Curve
* **Layer:** 3
* **Variable ID:** L3-002
* **Causal mechanism:** Captures market pricing of future overnight policy conditions across maturities.
* **Direction:** Negative
* **Incremental information:** Provides a broader forward curve than a single futures contract and can identify where policy expectations are moving.
* **Overlap:** Fed Funds Futures Expected Policy Rate (L3-001) — **Duplicate candidate**; Layer 1 Expected Policy Rate — **Transmission candidate**
* **Data/evidence source:** OIS market data.
* **Reliability:** Strong market signal, subject to provider/source and market-liquidity considerations.
* **Historical depth:** Modern period; exact series depth is source-dependent.
* **Frequency:** Daily / intraday where available
* **Freshness:** Hours
* **Accessibility:** Mixed / possibly paid
* **Operational burden:** Medium
* **Relevant horizons:** 1–5 days; 1–3 months; 1–3 years — cyclical
* **Initial weight rationale:** Retain because forward-curve information may be more comprehensive than a single futures contract.
* **Evidence references:** Causal Model v2.2 Layer 3; T1 Brief.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Primary-anchor designation note:** Before Spec A implementation, designate which of L3-001 or L3-002 is the primary Layer 3 quantitative anchor to prevent inadvertent double-weighting of the same policy-path signal. This is not a Phase 1 decision but must be resolved before scoring-engine implementation.

---

### L3-003 — Expected Terminal Policy Rate

* **Variable name:** Expected Terminal Policy Rate
* **Layer:** 3
* **Variable ID:** L3-003
* **Causal mechanism:** Measures the market's expected endpoint of the tightening/easing cycle and therefore changes expected long-run policy restrictiveness.
* **Direction:** Negative
* **Incremental information:** Isolates the cycle endpoint from the full policy curve and can move materially without an immediate current-rate change.
* **Overlap:** Fed Funds futures — **Transmission candidate**; OIS curve — **Transmission candidate**
* **Data/evidence source:** Market-implied curve / policy-market pricing.
* **Reliability:** Strong when derived consistently from liquid market instruments; methodology must be fixed.
* **Historical depth:** Modern market data.
* **Frequency:** Daily / event-driven
* **Freshness:** Hours to one day
* **Accessibility:** Mixed
* **Operational burden:** Low
* **Relevant horizons:** 1–3 months; 1–3 years — cyclical
* **Initial weight rationale:** Useful summary of the expected policy regime.
* **Evidence references:** Causal Model v2.2 Layer 3; T1 Brief.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

---

### L3-004 — Probability Distribution of Future Policy Outcomes

* **Variable name:** Probability Distribution of Future Policy Outcomes
* **Layer:** 3
* **Variable ID:** L3-004
* **Causal mechanism:** Measures uncertainty/distribution around future policy outcomes rather than only the modal expected rate.
* **Direction:** Conditional
* **Incremental information:** Captures uncertainty and tail repricing that a single expected rate does not capture.
* **Overlap:** Fed Funds futures — **Transmission candidate**; OIS curve — **Transmission candidate**
* **Data/evidence source:** Market-implied probabilities / futures and options where appropriate.
* **Reliability:** Strong when derived transparently; tail probabilities can be sensitive to methodology and liquidity.
* **Historical depth:** Modern market era.
* **Frequency:** Daily / intraday
* **Freshness:** Hours
* **Accessibility:** Mixed
* **Operational burden:** Medium
* **Relevant horizons:** 1–5 days; 1–3 months — event-driven
* **Initial weight rationale:** Retain because uncertainty itself can matter during policy meetings and macro shocks.
* **Evidence references:** Causal Model v2.2 Layer 3 observable categories.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

---

### L3-005 — FOMC Dot Plot Path

* **Variable name:** FOMC Dot Plot Path
* **Layer:** 3
* **Variable ID:** L3-005
* **Causal mechanism:** Official projection of policymakers' expected policy path can alter market expectations and the perceived reaction function.
* **Direction:** Negative
* **Incremental information:** Adds official policy-maker guidance that can differ from market pricing.
* **Overlap:** Fed Funds futures/OIS — **Transmission candidate**; FOMC statement — **Transmission candidate**
* **Data/evidence source:** Federal Reserve / FOMC primary publication.
* **Reliability:** Very strong source authority; interpretation requires careful distinction between individual projections and Committee policy.
* **Historical depth:** Good for the modern dot-plot period.
* **Frequency:** Quarterly / FOMC schedule
* **Freshness:** Until next policy communication; may become stale rapidly after major data.
* **Accessibility:** Free / public
* **Operational burden:** Low
* **Relevant horizons:** 1–3 months; 1–3 years — event-driven / cyclical
* **Initial weight rationale:** Valuable official-vs-market expectation comparison.
* **Evidence references:** T1 Brief; Spec D source/provenance standards.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

---

### L3-006 — FOMC Statements / Forward-Guidance Signal

* **Variable name:** FOMC Statements / Forward-Guidance Signal
* **Layer:** 3
* **Variable ID:** L3-006
* **Causal mechanism:** Interprets changes in official forward guidance that can shift expected future policy without an immediate rate change.
* **Direction:** Conditional
* **Incremental information:** Textual policy communication can provide new information before quantitative market measures fully adjust.
* **Overlap:** Dot plot — **Transmission candidate**; speeches — **Transmission candidate**; Fed Funds/OIS — **Transmission candidate**
* **Data/evidence source:** FOMC statements and official Federal Reserve communications.
* **Reliability:** Source authority is very strong; interpretation consistency and traceability are the key limitation. Spec D requires facts, interpretation, evidence, counter-evidence, timestamps, and provenance.
* **Historical depth:** Good over modern FOMC communication history; textual comparability varies across eras.
* **Frequency:** Event-driven
* **Freshness:** Days to weeks, but can change immediately after new data/events.
* **Accessibility:** Free / public
* **Operational burden:** Medium
* **Relevant horizons:** 1–5 days; 1–3 months — event-driven
* **Initial weight rationale:** Core qualitative communication variable; constrained to structured, auditable interpretation.
* **Evidence references:** T1 Brief; Spec D analytical-variable requirements.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

---

### L3-007 — Fed Speeches / Communication Signal

* **Variable name:** Fed Speeches / Communication Signal
* **Layer:** 3
* **Variable ID:** L3-007
* **Causal mechanism:** Captures forward-guidance information between formal FOMC decisions that can shift policy expectations.
* **Direction:** Conditional
* **Incremental information:** Adds inter-meeting communication that neither current rates nor scheduled FOMC statements capture.
* **Overlap:** FOMC statements — **Transmission candidate**; OIS/Fed Funds futures — **Transmission candidate**
* **Data/evidence source:** Official Federal Reserve speeches and communications.
* **Reliability:** Source authority is high; individual speaker status and messages can vary, creating interpretation risk.
* **Historical depth:** Good for modern digital publication era, but speaker/event coverage is uneven.
* **Frequency:** Event-driven / multiple times weekly
* **Freshness:** Hours to days
* **Accessibility:** Free / public
* **Operational burden:** High — weekly retrieval, speaker weighting, relevance filtering, interpretation consistency, and audit trail required.
* **Relevant horizons:** 1–5 days; 1–3 months — event-driven
* **Initial weight rationale:** Potentially useful but operational burden is the decisive constraint; production admission depends on a repeatable scoring process.
* **Evidence references:** T1 Brief; Spec D analytical evidence/provenance requirements.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

---

### L3-008 — Inflation Surprise / Data-Surprise Index

* **Variable name:** Inflation Surprise / Data-Surprise Index
* **Layer:** 3
* **Variable ID:** L3-008
* **Causal mechanism:** Measures unexpected macro-data outcomes that force repricing of the expected monetary-policy path; the Layer 3 mechanism is policy-expectation repricing, not inflation itself.
* **Direction:** Conditional
* **Incremental information:** Captures the surprise component of incoming data and therefore the trigger for policy-expectation revision rather than the underlying inflation level.
* **Overlap:** Inflation variables in L4 — **Transmission candidate**; Fed Funds/OIS — **Transmission candidate**
* **Data/evidence source:** Economic-release surprise datasets / established surprise indices; exact production source to be selected later.
* **Reliability:** Depends materially on methodology, consensus-vintage integrity, and source consistency.
* **Historical depth:** Source-dependent; longer histories possible for standardized surprise indices.
* **Frequency:** Daily / event-driven
* **Freshness:** Hours to days
* **Accessibility:** Mixed / potentially paid
* **Operational burden:** Medium
* **Relevant horizons:** 1–5 days; 1–3 months — event-driven
* **Initial weight rationale:** Strong conceptual fit as the trigger of policy repricing, but production source/vintage methodology must be locked.
* **Evidence references:** T1 candidate approval; Handoff point-in-time data-integrity rule.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace
* **Vintage integrity requirement:** The production source must preserve point-in-time consensus vintage — the consensus estimate used must be what was known before the data release, not a revised consensus. This is a Handoff data-integrity rule. Failure to enforce this introduces look-ahead bias into the policy-repricing signal.

---

## T1 Summary Table

| Variable ID | Variable Name | Decision | Overlap Flags | Horizon(s) |
|---|---|---|---|---|
| L0-001 | Above-Ground Gold Stock | ADMIT | Transmission | 1–3Y, 3–10Y |
| L0-002 | Central-Bank Gold Holdings | ADMIT | Transmission / Duplicate | 1–3M, 1–3Y, 3–10Y |
| L0-003 | Gold ETF Holdings | ADMIT | Transmission | 1–5D, 1–3M, 1–3Y |
| L0-004 | Household / Jewelry Gold Stock | CONDITIONAL | Transmission / Duplicate | 1–3Y, 3–10Y |
| L0-005 | Bar-and-Coin Investment Holdings / Demand | ADMIT | Duplicate / Transmission | 1–3M, 1–3Y, 3–10Y |
| L0-006 | Gold Recycling Flow | ADMIT | Transmission | 1–3M, 1–3Y |
| L0-007 | Producer Hedging | CONDITIONAL | Transmission | 1–3M, 1–3Y |
| L0-008 | Vaulted vs. Potentially Mobile Gold | CONDITIONAL | Transmission / Interaction | 1–3M, 1–3Y |
| L0-009 | Gold Lease Rates / Forward Rates | ADMIT | Interaction / Transmission | 1–5D, 1–3M, 1–3Y |
| L1-001 | 10Y TIPS Real Yield | ADMIT | Duplicate / Interaction / Transmission | All |
| L1-002 | 5Y TIPS Real Yield | ADMIT | Duplicate / Interaction | 1–5D, 1–3M, 1–3Y |
| L1-003 | Forward Real Rates | ADMIT | Duplicate / Transmission | 1–3M, 1–3Y, 3–10Y |
| L1-004 | Real Yield Curve / Slope | CONDITIONAL | Duplicate | 1–3M, 1–3Y, 3–10Y |
| L1-005 | Treasury Term Premium | ADMIT | Transmission | 1–3M, 1–3Y |
| L1-006 | Expected Policy Rate | ADMIT | Transmission | 1–5D, 1–3M, 1–3Y |
| L1-007 | 5Y5Y Forward Real Rate | ADMIT | Duplicate / Interaction | 1–3Y, 3–10Y |
| L3-001 | Fed Funds Futures Expected Policy Rate | ADMIT | Duplicate / Transmission | 1–5D, 1–3M, 1–3Y |
| L3-002 | OIS Forward Policy Curve | ADMIT | Duplicate / Transmission | 1–5D, 1–3M, 1–3Y |
| L3-003 | Expected Terminal Policy Rate | ADMIT | Transmission | 1–3M, 1–3Y |
| L3-004 | Probability Distribution of Future Policy Outcomes | ADMIT | Transmission | 1–5D, 1–3M |
| L3-005 | FOMC Dot Plot Path | ADMIT | Transmission | 1–3M, 1–3Y |
| L3-006 | FOMC Statements / Forward-Guidance Signal | ADMIT | Transmission | 1–5D, 1–3M |
| L3-007 | Fed Speeches / Communication Signal | CONDITIONAL | Transmission | 1–5D, 1–3M |
| L3-008 | Inflation Surprise / Data-Surprise Index | CONDITIONAL | Transmission | 1–5D, 1–3M |

---

## T1 Cross-Layer Notes for T2

- L1 vs L3 must remain separate. L1 = current real opportunity cost; L3 = expected forward policy path/repricing mechanism.
- Expected Policy Rate (L1-006) is the highest-risk boundary variable. Monitor at implementation.
- L3-008 Inflation Surprise is not an L4 inflation-level variable. Its mechanism is policy-expectation repricing.
- Gold lease/forward rates remain L0. Mechanism is stock mobility/physical financing, not financial opportunity cost.
- ETF holdings are Layer 0 stock; ETF flows belong in Layer 8.
- No numerical D/T treatment assigned. Reserved for Spec A implementation.
- Conditional variables are not failed candidates. They remain research-registry entries pending resolution of reliability or operational constraints.
