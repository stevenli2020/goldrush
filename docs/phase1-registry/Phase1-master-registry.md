# Gold Probability Engine — Phase 1 Master Variable Registry

**Status:** SIGNED OFF — Phase 1 SSOT  
**Effective date:** 2026-08-17  
**Purpose:** Consolidated, frozen Phase 1 variable universe for Phase 2 data-ingestion planning.  
**Audit history:** Individual tranche registries T1–T5 remain unchanged as source records; this master registry consolidates their admission records and governance.

## 1. Phase 1 universe

| Tranche | Layers | Records | ADMIT | CONDITIONAL / RESEARCH ONLY | REJECT |
|---|---|---:|---:|---:|---:|
| T1 | 0, 1, 3 | 24 | 18 | 6 | 0 |
| T2 | 4, 5 | 16 | 12 | 4 | 0 |
| T3 | 2, 7 | 11 | 7 | 4 | 0 |
| T4 | 6, 9 | 10 | 4 | 6 | 0 |
| T5 | 8, 10, 11 | 13 | 3 | 10 | 0 |
| **Total** | **0–11** | **74** | **44** | **30** | **0** |

**Production-universe rule:** Only the 44 ADMIT variables are eligible for Phase 2 ingestion and eventual production scoring. The 30 CONDITIONAL / RESEARCH ONLY variables remain documented in this SSOT but are excluded until their open conditions are resolved and formally approved. No rejected variables exist in Phase 1.

## 2. Reconciliation and ownership

- All 74 variable IDs are unique; no ID renumbering or collision was found.
- The 12-layer architecture remains unchanged. Each variable retains its assigned primary layer.
- Cross-layer overlap flags are retained as qualitative governance metadata; no numerical D_i, T_i, or γ_ij values were assigned.
- Stock/flow distinctions remain explicit: L0 stocks versus L8 flows; L0/L5 ownership and allocation versus L9 regional physical behavior; L0-009 physical financing versus L10 derivatives basis.
- Upstream causes remain in their causal layers. L8 records investment flows, L10 records market amplification, and L11 records reflexive feedback rather than re-attributing macro, geopolitical, FX, or liquidity causes.
- L2-003 USD/CNY is not duplicated in Layer 9. L0-003 ETF holdings is not treated as an L8 flow. L0-009 lease/forward rates are not re-admitted in Layer 10 for the same physical-financing mechanism.

## 3. Consolidated open items for Phase 2

| ID | Item | Required Before |
|---|---|---|
| L0-001 | Name and validate the above-ground-stock production source, methodology, and revision policy | Phase 2 ingestion |
| L0-009 | Confirm a stable, licensed gold lease/forward-rate source | Phase 2 ingestion |
| L1-004 | Demonstrate incremental information beyond the L1-001/L1-002 real-yield slope | Production admission |
| L1-005 | Name the production Treasury term-premium model/series and preserve methodology/revisions | Phase 2 ingestion |
| L1-006/L3-001/002 | Designate primary policy-rate anchor and document the non-overlapping L1/L3 roles | Spec A implementation |
| L3-008 | Preserve point-in-time consensus vintages for the data-surprise source | Production admission |
| L4-005 | Lock a named survey source, methodology, retrieval process, and consistency review | Production admission |
| L4-010 | Demonstrate incremental information beyond L1-005 and document issuance-to-gold transmission | Production admission |
| L5-004 | Establish a structured, retrievable source and Spec D-compliant evidence process | Production admission |
| L5-005 | Improve custody coverage and distinguish custody/security from generic geopolitics | Production admission |
| L6-003 | Establish reproducible geopolitical-causality classification and separation from L4/L3 | Production admission |
| L6-004 | Establish repeatable evidence and scoring for forward-looking asset-access risk | Production admission |
| L6-005 | Define observable fragmentation milestones and auditable evidence rubric | Production admission |
| L8-002 | Lock geography set and separate physical investment flows from L0/L9 measures | Production admission |
| L8-003 | Validate institutional coverage universe and direct-versus-derivative exposure rule | Production admission |
| L8-004 | Validate a stable, non-duplicative retail-flow source | Production admission |
| L9-002 | Separate imports, exchange delivery, retail demand, and investment flows in a documented composite | Production admission |
| L9-003 | Lock a stable, reproducible India premium series and adjustment methodology | Production admission |
| L9-005 | Establish a stable aggregate series separating recycling from collateral finance | Production admission |
| L10-003 | Pre-specify options-surface construction, strike selection, and skew definition | Production admission |
| L10-004 | Demonstrate a derivatives-basis mechanism distinct from L0-009 and L7 stress | Production admission |
| L10-005 | Establish a reproducible liquidation proxy and validation event set | Production admission |
| L11-001 | Lock query bank, geography, anchor, normalization, and robustness procedure | Production admission |
| L11-002 | Lock media corpus, deduplication method, and narrative classifier | Production admission |
| L11-003 | Separate reflexive feedback from L10 trend/positioning and link it to later behavior | Production admission |
| L11-004 | Lock a stable sentiment source with documented sampling and manipulation controls | Production admission |

## 4. Phase 2 ingestion policy

Phase 2 begins with the 44 ADMIT variables only. Each source must preserve observation date, publication/release date, retrieval date, source, revision status, access conditions, and the exact transformation used. Conditional variables may be collected in a research quarantine where operationally useful, but they must not enter production scoring or alter the frozen Phase 1 universe without a separate admission review.

## 5. Consolidated audit-history records

## T1 audit-history records

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

## T2 audit-history records

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

## T3 audit-history records

## 2. Layer 2 — US Dollar and Global FX Regime

### Candidate list

| Variable ID | Candidate | Rationale |
|---|---|---|
| L2-001 | DXY US Dollar Index | Liquid, timely market measure of dollar valuation; captures the mechanical USD quotation channel but is partly downstream of L1/L3/L7. |
| L2-002 | Broad Trade-Weighted Nominal US Dollar Index | Broadens currency coverage beyond DXY and better represents non-US buyer purchasing-power transmission. |
| L2-003 | USD/CNY | Adds China-specific currency transmission to a major physical and investment gold market; not adequately represented by DXY alone. |
| L2-004 | Emerging-Market FX Stress Composite | Could capture broad non-US currency stress and demand effects, but source construction and maintenance require validation. |
| L2-005 | Cross-Currency Basis / USD Funding Stress | Captures FX-market-specific dollar scarcity; useful at crisis horizons but has substantial Layer 7 overlap and access constraints. |

### L2-001 — DXY US Dollar Index

* **Variable name:** DXY US Dollar Index
* **Layer:** 2
* **Variable ID:** L2-001
* **Causal mechanism:** Measures the USD against a fixed basket of major currencies. A stronger USD mechanically raises the USD price of gold for non-US buyers and can reduce their purchasing power; a weaker USD generally eases that burden. The measure can also transmit monetary-policy and funding shocks, but those channels must not be counted as independent L2 causes.
* **Direction:** Negative under the mechanical purchasing-power channel; conditional during acute dollar-funding crises.
* **Incremental information:** Provides a highly liquid, timely benchmark for the dollar-quotation and major-currency valuation channel. It adds FX transmission beyond T1 real-yield and policy-expectation variables, even though it is partly a downstream transmission signal.
* **Overlap:** L1 real yields — **Transmission candidate**; L3 policy-expectation variables — **Transmission candidate**; L7 funding-stress variables — **Transmission candidate**; broad trade-weighted USD — **Duplicate candidate**.
* **Data/evidence source:** ICE Benchmark Administration DXY methodology and licensed/market data; public market quotations may be used only where retrieval and licensing permit. Cross-check against Federal Reserve H.10 exchange-rate data.
* **Reliability:** Strong benchmark methodology and high liquidity; basket composition is narrow and euro-heavy, and the index is not a complete measure of global purchasing power.
* **Historical depth:** Good modern history; exact history depends on the production data source.
* **Frequency:** Intraday / daily.
* **Freshness:** Hours to one day.
* **Accessibility:** Mixed; public quotations may be crawlable, while authoritative historical data may be paid or restricted.
* **Operational burden:** Low to medium, depending on licensed-source access and timestamp handling.
* **Relevant horizons:** 1–5 days; 1–3 months; 1–3 years — cyclical and transmission-driven; conditional over 3–10 years.
* **Initial weight rationale:** Primary high-frequency L2 anchor, but its within-layer weight must be moderated relative to broader and regional measures to avoid treating one basket as the whole FX regime.
* **Implementation requirement:** Before Spec A implementation, designate the primary L2 dollar anchor or establish the dependency treatment for L2-001/L2-002 so the same broad-dollar move is not inadvertently double-weighted.
* **Evidence references:** Causal Model v2.2, Layer 2; T3 Brief, Layer 2 four-channel framework; ICE DXY methodology; Federal Reserve H.10 exchange-rate release.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L2-002 — Broad Trade-Weighted Nominal US Dollar Index

* **Variable name:** Broad Trade-Weighted Nominal US Dollar Index
* **Layer:** 2
* **Variable ID:** L2-002
* **Causal mechanism:** Measures the USD against a broader, trade-weighted group of currencies. USD appreciation increases the local-currency cost of gold across a wider set of non-US economies and provides a broader purchasing-power transmission measure than DXY.
* **Direction:** Negative under the normal purchasing-power channel; conditional during global dollar-liquidity stress.
* **Incremental information:** Adds broader currency coverage and a Federal Reserve-defined trade-weighted construction beyond DXY's narrow basket. It is complementary rather than automatically redundant because the covered currencies and weights differ.
* **Overlap:** DXY — **Duplicate candidate**; L3 policy expectations — **Transmission candidate**; L7 dollar-liquidity conditions — **Transmission candidate**; T2 L4-003/L4-004 breakevens — **Interaction candidate, T2 decision pending**.
* **Data/evidence source:** Federal Reserve H.10 / FRED series DTWEXBGS: https://fred.stlouisfed.org/series/DTWEXBGS
* **Reliability:** Strong primary-source methodology, public documentation, daily observations, and stable historical access. Revisions and methodology changes must be recorded.
* **Historical depth:** Good modern daily history, with coverage dependent on the Federal Reserve series start date.
* **Frequency:** Daily.
* **Freshness:** One day.
* **Accessibility:** Free / public.
* **Operational burden:** Low.
* **Relevant horizons:** 1–5 days; 1–3 months; 1–3 years; 3–10 years — cyclical, structural, and regime-dependent.
* **Initial weight rationale:** Broad-coverage L2 anchor complementary to DXY; should not receive a full independent weight for the same dollar move without later Spec A review.
* **Implementation requirement:** Before Spec A implementation, designate the primary L2 dollar anchor or establish the dependency treatment for L2-001/L2-002 so the same broad-dollar move is not inadvertently double-weighted.
* **Evidence references:** Federal Reserve H.10; FRED DTWEXBGS; Causal Model v2.2, Layer 2; T3 Brief L2/L4 boundary note.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L2-003 — USD/CNY

* **Variable name:** USD/CNY
* **Layer:** 2
* **Variable ID:** L2-003
* **Causal mechanism:** Measures USD transmission into the Chinese renminbi, a major currency for a large physical and investment gold market. Renminbi weakness raises local gold costs and can affect local demand, while capital-management and policy-regime conditions make the relationship conditional.
* **Direction:** Positive for USD/CNY (renminbi depreciation) through local-currency gold-cost pressure; conditional when safe-haven or domestic financial stress dominates.
* **Incremental information:** Adds China-specific currency and purchasing-power information not adequately captured by the broad USD basket. It also provides regional information relevant to the future Layer 9 physical-market subsystem without pre-empting that layer.
* **Overlap:** DXY and broad USD index — **Transmission candidate**; L3 policy expectations — **Transmission candidate**; T2 L4 inflation/breakeven variables — **Interaction candidate, T2 decision pending**; future L9 regional physical demand — **Transmission candidate**.
* **Data/evidence source:** Federal Reserve H.10 exchange rates / FRED DEXCHUS; official Chinese foreign-exchange reference information where needed.
* **Reliability:** Strong for the published exchange-rate series; interpretation is complicated by managed exchange-rate policy, onshore/offshore market differences, capital controls, and possible source-timing differences.
* **Historical depth:** Good modern history; regime comparability varies across periods.
* **Frequency:** Daily.
* **Freshness:** One day.
* **Accessibility:** Free / public for the Federal Reserve series.
* **Operational burden:** Low to medium; requires consistent choice of onshore/offshore series and timezone.
* **Relevant horizons:** 1–5 days; 1–3 months; 1–3 years — cyclical and regional; conditional over 3–10 years.
* **Initial weight rationale:** Regional complement to broad USD variables; weight should reflect incremental China-specific information, not simply duplicate broad dollar direction.
* **Boundary requirement:** L2-003 is admitted in Layer 2 for its FX purchasing-power and dollar-transmission mechanism. It must not be re-admitted as an independent Layer 9 variable; Layer 9 should use its own regional observables such as SGE premium, local demand, and capital controls.
* **Evidence references:** Federal Reserve H.10; FRED DEXCHUS; Causal Model v2.2, Layers 2 and 9; T3 Brief L2 four-channel framework.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L2-004 — Emerging-Market FX Stress Composite

* **Variable name:** Emerging-Market FX Stress Composite
* **Layer:** 2
* **Variable ID:** L2-004
* **Causal mechanism:** Represents broad depreciation and volatility pressure across emerging-market currencies. EM currency stress can raise local gold costs, alter local demand, and signal dollar scarcity; the safe-haven and forced-liquidation effects can oppose one another.
* **Direction:** Conditional.
* **Incremental information:** Adds broad non-US and non-major-currency stress information that is not represented by DXY, the broad USD index, or USD/CNY alone. It may also identify regional purchasing-power stress before it appears in developed-market FX measures.
* **Overlap:** Broad USD index — **Transmission candidate**; USD/CNY — **Transmission candidate**; L7 credit/funding stress — **Interaction candidate**; future L9 regional physical markets — **Transmission candidate**.
* **Data/evidence source:** Candidate construction from publicly documented exchange-rate series, BIS effective exchange-rate data, or another stable institutional basket; production source not yet locked.
* **Reliability:** The underlying exchange rates can be reliable, but the composite requires explicit currency selection, weights, missing-data treatment, and regime review. A proprietary index without transparent methodology is insufficient.
* **Historical depth:** Uneven across countries; composite history depends on the final membership and source.
* **Frequency:** Daily or weekly, source-dependent.
* **Freshness:** Days.
* **Accessibility:** Mixed; free construction may be possible, but stable cross-country coverage must be verified.
* **Operational burden:** Medium to high due to currency roll, missing observations, weighting, and validation.
* **Relevant horizons:** 1–5 days; 1–3 months; 1–3 years — cyclical and regime-dependent.
* **Initial weight rationale:** Potentially valuable regime coverage, but no production weight until the basket, source, and missing-data policy are locked.
* **Evidence references:** BIS effective exchange-rate statistics; Causal Model v2.2, Layer 2; T3 Brief L2 observables and admission rules.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L2-005 — Cross-Currency Basis / USD Funding Stress

* **Variable name:** Cross-Currency Basis / USD Funding Stress
* **Layer:** 2
* **Variable ID:** L2-005
* **Causal mechanism:** Measures the deviation from covered-interest-parity pricing in FX swaps or related dollar-funding markets. A stressed basis can signal scarcity of USD funding, affect non-US investors' ability to finance gold, and cause forced liquidation; the short-run effect can therefore be bullish or bearish depending on whether scarcity or safe-haven demand dominates.
* **Direction:** Conditional.
* **Incremental information:** Adds FX-market-specific dollar funding information beyond spot USD valuation and beyond Layer 7's broader funding-system measures. The incremental case depends on retaining an FX-pricing mechanism rather than using it as a generic liquidity-stress proxy.
* **Overlap:** L7 repo/funding stress — **Transmission candidate**; L7 financial-system stress — **Interaction candidate**; DXY — **Transmission candidate**; L3 policy expectations — **Transmission candidate**.
* **Data/evidence source:** BIS international banking/FX statistics and transparent market-based cross-currency basis series; final production source and licensing must be confirmed.
* **Reliability:** Mechanistically strong, but public coverage, tenor selection, currency selection, and historical consistency vary. Basis can also reflect balance-sheet regulation and risk premia rather than pure USD scarcity.
* **Historical depth:** Good for selected major currencies and modern markets; uneven across tenors and currencies.
* **Frequency:** Daily or weekly, source-dependent.
* **Freshness:** Days.
* **Accessibility:** Mixed / potentially restricted.
* **Operational burden:** High due to source access, tenor normalization, currency selection, and interpretation during market stress.
* **Relevant horizons:** 1–5 days; 1–3 months — event-driven and conditional; possible 1–3-year regime monitoring.
* **Initial weight rationale:** Strong crisis-regime information, but production inclusion requires a stable source and an explicit boundary against L7.
* **Evidence references:** BIS international banking and FX statistics; Causal Model v2.2, Layers 2 and 7; T3 Brief L2/L7 boundary rule.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### Layer 2 summary

| Variable ID | Variable Name | Decision | Overlap Flags | Horizon(s) |
|---|---|---|---|---|
| L2-001 | DXY US Dollar Index | ADMIT | Transmission / Duplicate | 1–5D, 1–3M, 1–3Y, conditional 3–10Y |
| L2-002 | Broad Trade-Weighted Nominal US Dollar Index | ADMIT | Duplicate / Transmission / Interaction | All four |
| L2-003 | USD/CNY | ADMIT | Transmission / Interaction | 1–5D, 1–3M, 1–3Y, conditional 3–10Y |
| L2-004 | Emerging-Market FX Stress Composite | CONDITIONAL / RESEARCH ONLY | Transmission / Interaction | 1–5D, 1–3M, 1–3Y |
| L2-005 | Cross-Currency Basis / USD Funding Stress | CONDITIONAL / RESEARCH ONLY | Transmission / Interaction | 1–5D, 1–3M, conditional 1–3Y |

## 3. Layer 7 — Global Liquidity and Financial Conditions

### Candidate list

| Variable ID | Candidate | Rationale |
|---|---|---|
| L7-001 | Major Central-Bank Balance-Sheet Liquidity | Measures realized central-bank liquidity conditions, distinct from L3 forward policy expectations. |
| L7-002 | Global Broad Money Growth | Captures realized global monetary/liquidity expansion, but aggregation and source consistency require validation. |
| L7-003 | Global Private Non-Financial Credit Growth | Measures credit creation and financial capacity beyond central-bank policy signals. |
| L7-004 | Credit-Spread Financial Stress | Captures realized risk-bearing and financing conditions, with explicit separation from L1 opportunity cost. |
| L7-005 | Treasury Repo Funding Stress | Measures short-term secured funding-market conditions and acute liquidity stress. |
| L7-006 | US Reserve-Liquidity Plumbing Composite | Combines TGA, reverse-repo balances, and reserve balances as a US dollar-liquidity monitor; requires production formula review. |

### L7-001 — Major Central-Bank Balance-Sheet Liquidity

* **Variable name:** Major Central-Bank Balance-Sheet Liquidity
* **Layer:** 7
* **Variable ID:** L7-001
* **Causal mechanism:** Measures realized changes in the balance-sheet capacity and liquidity supplied by major central banks. Expansion can ease funding conditions and support risk-bearing; contraction can tighten liquidity. During acute stress, balance-sheet changes and market functioning can produce a two-phase gold response.
* **Direction:** Positive for realized broad liquidity expansion; conditional during acute crisis liquidation.
* **Incremental information:** Captures implemented liquidity conditions and balance-sheet realization beyond T1 Layer 3 variables that measure expected policy paths and repricing. It must not be scored as a proxy for anticipated future easing.
* **Overlap:** L3 expected policy variables — **Transmission candidate**; T1 L1 opportunity-cost variables — **Transmission candidate**; L7 reserve-liquidity plumbing — **Duplicate candidate** where the same central-bank balance-sheet component is reused; pending T2 fiscal variables — **Interaction candidate** where issuance changes alter liquidity transmission.
* **Data/evidence source:** Federal Reserve H.4.1; ECB financial-statement data; PBoC and other major-central-bank official balance-sheet releases, subject to a documented aggregation method.
* **Reliability:** Strong for individual official series; cross-country aggregation requires currency conversion, publication-calendar alignment, revisions, and central-bank comparability controls.
* **Historical depth:** Good for major developed-market central banks; uneven for China and other jurisdictions.
* **Frequency:** Weekly to monthly, depending on institution.
* **Freshness:** One week to one month.
* **Accessibility:** Free / public for major official series; some national series require additional processing.
* **Operational burden:** Medium to high because of aggregation, currency conversion, and revision tracking.
* **Relevant horizons:** 1–3 months; 1–3 years; 3–10 years — cyclical and structural regime conditions.
* **Initial weight rationale:** Core realized-liquidity anchor, but its within-layer weight must be kept distinct from L3 expectations and from any reserve-plumbing composite.
* **Evidence references:** Federal Reserve H.4.1: https://www.federalreserve.gov/releases/h41/current/h41.htm; Causal Model v2.2, Layer 7; T3 Brief L7/L3 boundary rule.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L7-002 — Global Broad Money Growth

* **Variable name:** Global Broad Money Growth
* **Layer:** 7
* **Variable ID:** L7-002
* **Causal mechanism:** Measures the realized expansion or contraction of broad money across major economies. Stronger monetary aggregates can improve nominal liquidity and financing capacity; contraction can tighten conditions, although velocity, banking behavior, and inflation expectations make the gold response conditional.
* **Direction:** Positive in ordinary liquidity-expansion regimes; conditional when money growth reflects crisis deposits, inflation, or financial disintermediation.
* **Incremental information:** Adds realized private-sector money/liquidity conditions beyond T1 forward policy expectations and beyond central-bank asset stocks. It also captures commercial-bank money creation that balance sheets alone do not fully represent.
* **Overlap:** L7-001 central-bank balance sheets — **Transmission candidate**; L7-003 bank credit — **Interaction candidate**; T2 inflation and fiscal variables — **Interaction candidate, T2 decision pending**; L3 policy expectations — **Transmission candidate**.
* **Data/evidence source:** Official national monetary aggregates, BIS/IMF data where appropriate, and a transparent multi-country aggregation methodology; final production source not locked.
* **Reliability:** Individual national series are generally authoritative, but global aggregation has currency-conversion, definition, revision, and missing-country risks.
* **Historical depth:** Good for major economies; global coverage and consistent definitions are less reliable for older periods.
* **Frequency:** Monthly.
* **Freshness:** One to three months because of release lags and revisions.
* **Accessibility:** Mixed / largely public but processing-intensive.
* **Operational burden:** High due to harmonization, weighting, and revision-vintage preservation.
* **Relevant horizons:** 1–3 months; 1–3 years; 3–10 years — cyclical and structural.
* **Initial weight rationale:** Strong conceptual coverage, but production weight should remain provisional until a reproducible country set and aggregation method are validated.
* **Resolution condition:** Production admission requires a documented, reproducible multi-country aggregation methodology—including currency conversion, country set, weighting approach, and missing-data treatment—to be validated before Phase 2.
* **Evidence references:** Official national monetary-statistics releases; BIS monetary and financial statistics; Causal Model v2.2, Layer 7.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L7-003 — Global Private Non-Financial Credit Growth

* **Variable name:** Global Private Non-Financial Credit Growth
* **Layer:** 7
* **Variable ID:** L7-003
* **Causal mechanism:** Measures credit supplied to households and non-financial businesses. Expanding credit can increase financial-system capacity and risk-bearing; contracting credit can signal deleveraging and stress, with gold potentially benefiting from precautionary demand but suffering from forced liquidation in the acute phase.
* **Direction:** Conditional.
* **Incremental information:** Adds realized private credit creation and deleveraging beyond central-bank policy expectations, central-bank balance sheets, and T1 real yields. It measures the banking/private-finance transmission channel rather than policy intent.
* **Overlap:** L7 broad money — **Interaction candidate**; L7 credit spreads — **Transmission candidate**; L1 real yields — **Transmission candidate**; future L8 investment flows — **Transmission candidate**, not a flow substitute.
* **Data/evidence source:** BIS total credit statistics for the private non-financial sector: https://www.bis.org/statistics/tables_f.htm
* **Reliability:** Strong institutional source and transparent conceptual coverage; quarterly data, revisions, country comparability, and currency conversion limit timeliness.
* **Historical depth:** Good for many economies over several decades, with uneven country coverage.
* **Frequency:** Quarterly.
* **Freshness:** Several months.
* **Accessibility:** Free / public.
* **Operational burden:** Medium; requires vintage preservation and aggregation choices.
* **Relevant horizons:** 1–3 years; 3–10 years — structural and cyclical; limited direct 1–5-day use.
* **Initial weight rationale:** Admitted as a slower-moving financial-capacity anchor complementary to high-frequency stress measures; should not dominate short-horizon scoring.
* **Evidence references:** BIS total credit statistics; Causal Model v2.2, Layer 7; T3 Brief L7 mechanism definition.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L7-004 — Credit-Spread Financial Stress

* **Variable name:** Credit-Spread Financial Stress
* **Layer:** 7
* **Variable ID:** L7-004
* **Causal mechanism:** Measures the compensation required to finance or hold credit risk. Widening spreads indicate tighter financial conditions, weaker balance-sheet capacity, and potential forced deleveraging; gold may initially be sold for cash before safe-haven and policy-response effects dominate.
* **Direction:** Conditional; widening spreads are usually stress-positive for longer-horizon gold demand but can be negative during acute cash liquidation.
* **Incremental information:** Captures realized market stress and risk-bearing conditions beyond T1 real yields and L3 expected policy paths. Its L7 mechanism is financing capacity, not the opportunity cost of government bonds.
* **Overlap:** L1 Treasury term premium and real yields — **Transmission candidate**; L3 policy expectations — **Transmission candidate**; L7 global credit — **Transmission candidate**; future L10 derivatives stress — **Interaction candidate**.
* **Data/evidence source:** Publicly documented corporate option-adjusted spread series such as Federal Reserve/FRED ICE BofA measures, supplemented only where methodology is transparent.
* **Reliability:** Market-based and frequent, but vendor methodology, sector composition, liquidity, and index revisions require documentation. A single US spread is not a complete global measure.
* **Historical depth:** Good for major US credit benchmarks; older coverage and global comparability vary.
* **Frequency:** Daily.
* **Freshness:** Hours to one day.
* **Accessibility:** Public series may be free; underlying index methodology/data can be vendor-controlled.
* **Operational burden:** Low to medium if a stable public series is used; higher if global aggregation is attempted.
* **Relevant horizons:** 1–5 days; 1–3 months; 1–3 years — event-driven and cyclical.
* **Initial weight rationale:** Important high-frequency realized-stress indicator; use a transparent benchmark and keep its mechanism separate from L1 rate signals.
* **Evidence references:** Federal Reserve/FRED credit-spread series; Causal Model v2.2, Layer 7; T3 Brief L7/L1 boundary rule.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L7-005 — Treasury Repo Funding Stress

* **Variable name:** Treasury Repo Funding Stress
* **Layer:** 7
* **Variable ID:** L7-005
* **Causal mechanism:** Measures the cost and abnormality of secured overnight funding against Treasury collateral. Funding stress can force deleveraging and gold sales for cash, while subsequent liquidity support can improve gold's medium-term outlook.
* **Direction:** Conditional.
* **Incremental information:** Adds direct, high-frequency market-functioning information beyond L3 policy expectations, L1 yields, and broad balance-sheet aggregates. The mechanism is realized funding stress, not expected rate policy.
* **Overlap:** L2 cross-currency basis / USD funding stress — **Transmission candidate**; L7 reserve-liquidity plumbing — **Transmission candidate**; L7 credit spreads — **Interaction candidate**; L3 policy expectations — **Transmission candidate**.
* **Data/evidence source:** New York Federal Reserve SOFR, TGCR, and BGCR reference rates: https://www.newyorkfed.org/markets/reference-rates
* **Reliability:** Very strong official methodology and daily publication. The raw rate level is not itself stress; the production signal must use a documented spread, volatility, percentile, or abnormality transformation.
* **Historical depth:** SOFR history begins in the modern benchmark era; older repo proxies require separate validation.
* **Frequency:** Daily.
* **Freshness:** Same day / one business day.
* **Accessibility:** Free / public.
* **Operational burden:** Medium; requires holiday handling, benchmark continuity, and a pre-specified stress transformation.
* **Relevant horizons:** 1–5 days; 1–3 months — event-driven and conditional; 1–3 years for regime monitoring.
* **Initial weight rationale:** Strong short-horizon financial-functioning anchor; admit the observable family, while deferring the exact transformation to implementation.
* **Open item:** Pre-specify the stress-transformation rule (spread, percentile, or abnormality measure) and validate it against known funding-stress episodes before Phase 2.
* **Evidence references:** New York Fed reference-rate methodology; New York Fed SOFR data; Causal Model v2.2, Layer 7.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L7-006 — US Reserve-Liquidity Plumbing Composite

* **Variable name:** US Reserve-Liquidity Plumbing Composite
* **Layer:** 7
* **Variable ID:** L7-006
* **Causal mechanism:** Tracks the realized interaction among Federal Reserve reserve balances, the Treasury General Account, and the Federal Reserve's reverse-repurchase facility. These components affect the quantity and distribution of reserves available to the financial system and can condition the transmission of other shocks.
* **Direction:** Conditional.
* **Incremental information:** Adds a high-frequency US dollar-liquidity plumbing view that is more operationally specific than a total central-bank balance sheet. It can capture sterilization and Treasury-account effects that gross asset totals miss.
* **Overlap:** L7-001 central-bank balance sheets — **Duplicate candidate** for shared Fed components; L7-005 repo stress — **Transmission candidate**; L2 USD funding stress — **Transmission candidate**; T2 L4-009/L4-010 fiscal maturity and issuance variables — **Interaction candidate, T2 decision pending**; L3 policy expectations — **Transmission candidate**.
* **Data/evidence source:** Federal Reserve H.4.1 and FRED series for reserve balances and reverse repos; US Treasury Daily Treasury Statement / Fiscal Data for TGA.
* **Reliability:** Individual official series are strong, but the composite's economic interpretation depends on sign conventions, timing alignment, reserve-demand regime, and a transparent formula. Gross balances are not interchangeable with usable liquidity.
* **Historical depth:** Good for individual components, with comparability limited by facility and operating-regime changes.
* **Frequency:** Daily to weekly.
* **Freshness:** One business day to one week.
* **Accessibility:** Free / public.
* **Operational burden:** Medium to high due to alignment, transformations, regime changes, and formula governance.
* **Relevant horizons:** 1–5 days; 1–3 months; 1–3 years — cyclical and regime-dependent.
* **Initial weight rationale:** High-value diagnostic candidate, but production inclusion requires a validated composite definition that does not duplicate L7-001 or simply proxy for L3 easing expectations.
* **Resolution condition:** Production admission requires a pre-specified, documented composite formula—including TGA sign convention, component timing alignment, reserve-demand regime controls, and validation against known liquidity events—before Phase 2.
* **Evidence references:** Federal Reserve H.4.1: https://www.federalreserve.gov/releases/h41/current/h41.htm; New York Fed reference rates; US Treasury Fiscal Data; Causal Model v2.2, Layer 7.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### Layer 7 summary

| Variable ID | Variable Name | Decision | Overlap Flags | Horizon(s) |
|---|---|---|---|---|
| L7-001 | Major Central-Bank Balance-Sheet Liquidity | ADMIT | Transmission / Duplicate / Interaction | 1–3M, 1–3Y, 3–10Y |
| L7-002 | Global Broad Money Growth | CONDITIONAL / RESEARCH ONLY | Transmission / Interaction | 1–3M, 1–3Y, 3–10Y |
| L7-003 | Global Private Non-Financial Credit Growth | ADMIT | Transmission / Interaction | 1–3Y, 3–10Y |
| L7-004 | Credit-Spread Financial Stress | ADMIT | Transmission / Interaction | 1–5D, 1–3M, 1–3Y |
| L7-005 | Treasury Repo Funding Stress | ADMIT | Transmission / Interaction | 1–5D, 1–3M, 1–3Y |
| L7-006 | US Reserve-Liquidity Plumbing Composite | CONDITIONAL / RESEARCH ONLY | Duplicate / Transmission / Interaction | 1–5D, 1–3M, 1–3Y |

## T4 audit-history records

## 2. Layer 6 — Geopolitical Transmission Channels

### Candidate list

| Variable ID | Candidate | Channel | Rationale |
|---|---|---|---|
| L6-001 | Active Conflict and Escalation Signal | Safe haven | Direct event-driven measure of conflict intensity and escalation risk; distinct from broad geopolitical-news volume. |
| L6-002 | Sanctions and Sovereign-Asset Freeze Events | Reserve security | Captures concrete actions that alter perceived accessibility of sovereign assets and reserve security. |
| L6-003 | Geopolitical Energy and Shipping Disruption Signal | Energy/inflation | Captures the geopolitical supply-disruption trigger, not ordinary oil inflation or freight conditions. |
| L6-004 | Reserve-Security and Sovereign-Asset Access Risk Signal | Reserve security | Captures forward-looking risk of asset seizure, access restriction, or counterparty vulnerability beyond realized sanctions events. |
| L6-005 | Monetary-System Fragmentation Signal | Fragmentation | Captures geopolitical developments affecting reserve currencies, payment rails, settlement access, and monetary-system dependence. |

### L6-001 — Active Conflict and Escalation Signal

* **Variable name:** Active Conflict and Escalation Signal
* **Layer:** 6
* **Variable ID:** L6-001
* **Causal mechanism:** Structured assessment of active armed conflict, escalation, military buildups, and credible escalation warnings. The primary Layer 6 mechanism is safe-haven demand for liquid, non-sovereign assets. Energy, inflation, and policy channels must be recorded as possible offsets rather than silently included in the same score.
* **Direction:** Conditional; usually positive through safe haven, but the net effect can be offset by energy-driven tightening, USD funding stress, or rapid de-escalation.
* **Incremental information:** Adds event-driven geopolitical shock information not represented by T1/T3 rates, FX, liquidity, or market variables. It captures the geopolitical trigger before any resulting safe-haven flow or market-price response.
* **Overlap:** L7 credit/funding stress — **Transmission candidate**; L3 policy expectations — **Transmission candidate** through the energy channel; L6 GPR index — **Duplicate candidate** if both measure the same news intensity; future L10 positioning — **Transmission candidate**.
* **Data/evidence source:** ACLED or another documented conflict-event database; official statements and primary reporting from governments and international organizations; Caldara-Iacoviello GPR threat/acts data as a benchmark: https://www.matteoiacoviello.com/gpr.htm
* **Reliability:** Event databases provide structured observations but differ in coverage, verification, and lag. Official statements are authoritative as statements of fact or position, not necessarily as neutral assessments. Spec D must document source agreement and counter-evidence.
* **Historical depth:** Good for major modern conflicts; consistent event-level coverage varies by geography and period.
* **Frequency:** Daily / event-driven.
* **Freshness:** Hours to days; materially stale after new developments or de-escalation.
* **Accessibility:** Mixed / public for major sources; some structured event data may be paid or restricted.
* **Operational burden:** High because weekly retrieval, event deduplication, source verification, and analytical audit trails are required.
* **Relevant horizons:** 1–5 days; 1–3 months — event-driven; 1–3 years — conditional regime risk.
* **Initial weight rationale:** Core short-horizon safe-haven variable, but its weight must reflect evidence quality and avoid treating every headline as a persistent geopolitical shock.
* **Evidence references:** Causal Model v2.2, Layer 6; T4 Brief safe-haven channel; Caldara and Iacoviello, "Measuring Geopolitical Risk," AER 2022: https://doi.org/10.1257/aer.20191823; Spec D v2.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L6-002 — Sanctions and Sovereign-Asset Freeze Events

* **Variable name:** Sanctions and Sovereign-Asset Freeze Events
* **Layer:** 6
* **Variable ID:** L6-002
* **Causal mechanism:** Records implemented sanctions, reserve freezes, capital controls imposed for geopolitical reasons, and other official restrictions that alter the perceived accessibility of sovereign assets. The Layer 6 mechanism is the geopolitical reserve-security trigger; resulting reserve purchases or allocation changes belong in Layer 5.
* **Direction:** Conditional; positive when the event increases reserve-security demand for gold, but potentially mixed when sanctions reduce liquidity or trigger broad deleveraging.
* **Incremental information:** Adds concrete reserve-security actions beyond T1/T3 market conditions and beyond Layer 5's resulting official-sector allocation behavior. It distinguishes realized policy action from general geopolitical rhetoric.
* **Overlap:** L5 official-sector reserve allocation — **Transmission candidate**; L7 liquidity/funding stress — **Transmission candidate**; L6 reserve-security risk — **Transmission candidate**; T2 fiscal variables — **Interaction candidate** where sanctions affect sovereign financing.
* **Data/evidence source:** US Treasury OFAC sanctions programs and designations; UN Security Council sanctions; EU sanctions database and official national measures.
* **Reliability:** Strong for officially implemented measures and dates; scope, enforcement, exemptions, and economic impact require careful classification. Different jurisdictions may disagree on legal status or implementation.
* **Historical depth:** Good modern history for major sanctions regimes; older records require normalization.
* **Frequency:** Event-driven / daily.
* **Freshness:** Days to weeks, with durable structural effects after major actions.
* **Accessibility:** Free / public for major official sources.
* **Operational burden:** Medium to high due to legal-text interpretation, deduplication, jurisdiction mapping, and impact classification.
* **Relevant horizons:** 1–5 days; 1–3 months; 1–3 years — event-driven and structural; 3–10 years for persistent reserve-security regimes.
* **Initial weight rationale:** Directly observable reserve-security trigger with stronger fact status than a narrative risk index; weight should reflect event severity and not the subsequent L5 allocation response.
* **Evidence references:** OFAC Sanctions List Service; UN Security Council sanctions: https://main.un.org/securitycouncil/en/sanctions/information; Causal Model v2.2, Layer 6; T4 Brief L6/L5 boundary.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L6-003 — Geopolitical Energy and Shipping Disruption Signal

* **Variable name:** Geopolitical Energy and Shipping Disruption Signal
* **Layer:** 6
* **Variable ID:** L6-003
* **Causal mechanism:** Captures geopolitical conflict or disruption that constrains oil, gas, or shipping supply. The Layer 6 mechanism is the geopolitical supply shock; subsequent inflation and policy repricing belong in L4/L3, while realized financial stress belongs in L7.
* **Direction:** Conditional; safe-haven and supply-disruption effects may support gold, while higher energy prices can increase expected policy tightening and weigh on gold.
* **Incremental information:** Adds the geopolitical cause of energy/shipping disruption beyond T2 inflation variables, T1/T3 policy and FX variables, and ordinary oil-price movements. It is not an admission of oil price level as a second L4 variable.
* **Overlap:** T2 L4 inflation variables — **Transmission candidate**; L3 policy expectations — **Transmission candidate**; L7 funding stress — **Interaction candidate**; future L9 regional physical supply — **Transmission candidate**.
* **Data/evidence source:** Official incident and disruption reports; US EIA energy data for realized market context; IMO/official maritime advisories and documented shipping disruption datasets. Final event-classification source is not locked.
* **Reliability:** Energy prices and official incident reports are generally reliable, but attributing a price move to geopolitics rather than ordinary supply/demand is difficult. Shipping coverage can be incomplete and delayed.
* **Historical depth:** Good for major energy shocks; event classification is uneven across older episodes.
* **Frequency:** Daily / event-driven.
* **Freshness:** Hours to days.
* **Accessibility:** Mixed / mostly public, with some shipping data restricted.
* **Operational burden:** High due to event attribution, duplicate reporting, route classification, and offsetting-channel assessment.
* **Relevant horizons:** 1–5 days; 1–3 months — event-driven; 1–3 years — conditional structural disruption.
* **Initial weight rationale:** Useful channel-specific variable, but production use requires a reproducible geopolitical-causality classification and explicit separation from T2 inflation and L3 policy repricing.
* **Evidence references:** Causal Model v2.2, Layer 6 energy/inflation channel; T4 Brief L6/L4 boundary; US EIA energy data: https://www.eia.gov/; IMO maritime safety information.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L6-004 — Reserve-Security and Sovereign-Asset Access Risk Signal

* **Variable name:** Reserve-Security and Sovereign-Asset Access Risk Signal
* **Layer:** 6
* **Variable ID:** L6-004
* **Causal mechanism:** Structured assessment of the risk that sovereign reserves or foreign-held assets could be frozen, seized, restricted, or made inaccessible because of geopolitical conflict or legal action. The Layer 6 mechanism is the geopolitical risk trigger; official reserve reallocation belongs in Layer 5.
* **Direction:** Conditional; higher risk can support gold's reserve-security demand, but evidence may be anticipatory and can coexist with liquidity-driven selling.
* **Incremental information:** Captures forward-looking reserve-access risk not represented by realized sanctions events, T1/T3 market variables, or L5 observed allocation behavior.
* **Overlap:** L6-002 sanctions/freezes — **Transmission candidate**; L5 reserve objectives and allocation — **Transmission candidate**; monetary-system fragmentation — **Interaction candidate**; L7 liquidity stress — **Transmission candidate**.
* **Data/evidence source:** Official legal and policy documents, sanctions announcements, sovereign statements, treaty/international-organization material, and documented expert analysis.
* **Reliability:** Strong for announced rules and official actions; weaker for inferred future seizure risk. This is a Type B analytical variable and requires full Spec D evidence, counter-evidence, confidence rubric, and fact/interpretation separation.
* **Historical depth:** Event-based historical evidence is available, but comparable quantitative history is limited and must not be fabricated.
* **Frequency:** Event-driven / weekly assessment.
* **Freshness:** Days to weeks; reassess after legal or policy developments.
* **Accessibility:** Free / public for primary documents; specialist analysis may be paid.
* **Operational burden:** High because legal interpretation, source provenance, and analyst consistency are required.
* **Relevant horizons:** 1–3 months; 1–3 years; 3–10 years — conditional and structural.
* **Initial weight rationale:** Strong conceptual fit but weaker observability than realized sanctions events; retain as research-only until repeatable evidence and scoring procedures are demonstrated.
* **Evidence references:** Causal Model v2.2, Layer 6 reserve-security channel; T4 Brief L6/L5 boundary; Spec D v2.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L6-005 — Monetary-System Fragmentation Signal

* **Variable name:** Monetary-System Fragmentation Signal
* **Layer:** 6
* **Variable ID:** L6-005
* **Causal mechanism:** Assesses geopolitical developments that increase reliance on alternative reserve currencies, payment systems, settlement arrangements, or bilateral trade mechanisms. The Layer 6 mechanism is the geopolitical driver; realized liquidity effects belong in L7 and reserve-allocation behavior in L5.
* **Direction:** Conditional; fragmentation may support gold as a non-sovereign reserve asset, but alternative fiat arrangements may compete with gold and the effect can be slow-moving.
* **Incremental information:** Captures geopolitical monetary-system drivers not adequately represented by T1/T3 rates, FX valuation, liquidity conditions, or L5 realized reserve allocation.
* **Overlap:** L5 reserve diversification and allocation intent — **Transmission candidate**; L7 liquidity conditions — **Transmission candidate**; L2 FX regime — **Interaction candidate**; L6 reserve-security risk — **Interaction candidate**.
* **Data/evidence source:** Official central-bank and government announcements, payment-system agreements, treaty documents, BIS/IMF institutional material, and structured Spec D analytical evidence.
* **Reliability:** Primary documents are reliable for announced arrangements, but implementation, scale, and gold relevance are often uncertain. Evidence is heterogeneous and vulnerable to narrative overreach.
* **Historical depth:** Good contextual history; weak comparable quantitative history.
* **Frequency:** Event-driven / monthly or quarterly review.
* **Freshness:** Weeks to months.
* **Accessibility:** Free / public for official announcements; some settlement data is restricted.
* **Operational burden:** High due to slow-moving evidence, implementation assessment, and risk of converting policy rhetoric into fact.
* **Relevant horizons:** 1–3 years; 3–10 years — structural and conditional.
* **Initial weight rationale:** Important long-horizon channel, but retain as research-only until observable milestones and an auditable evidence rubric are established.
* **Evidence references:** Causal Model v2.2, Layer 6 fragmentation channel; T4 Brief L6/L7 boundary; Spec D v2; BIS institutional material.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### Layer 6 summary

| Variable ID | Variable Name | Decision | Overlap Flags | Horizon(s) |
|---|---|---|---|---|
| L6-001 | Active Conflict and Escalation Signal | ADMIT | Transmission / Duplicate | 1–5D, 1–3M, conditional 1–3Y |
| L6-002 | Sanctions and Sovereign-Asset Freeze Events | ADMIT | Transmission / Interaction | 1–5D, 1–3M, 1–3Y, 3–10Y |
| L6-003 | Geopolitical Energy and Shipping Disruption Signal | CONDITIONAL / RESEARCH ONLY | Transmission / Interaction | 1–5D, 1–3M, conditional 1–3Y |
| L6-004 | Reserve-Security and Sovereign-Asset Access Risk Signal | CONDITIONAL / RESEARCH ONLY | Transmission / Interaction | 1–3M, 1–3Y, 3–10Y |
| L6-005 | Monetary-System Fragmentation Signal | CONDITIONAL / RESEARCH ONLY | Transmission / Interaction | 1–3Y, 3–10Y |

## 3. Layer 9 — Regional Physical-Market Dynamics

### Candidate list

| Variable ID | Candidate | Subsystem | Rationale |
|---|---|---|---|
| L9-001 | Shanghai Gold Exchange Premium/Discount | China | Direct local physical-market price signal and a measure of local tightness or demand relative to international pricing. |
| L9-002 | China Physical Gold Demand and Import Signal | China | Captures regional physical acquisition and supply availability beyond L0 stock measures and L5 official-sector behavior. |
| L9-003 | India Local Gold Premium/Discount | India | Measures local physical tightness, import friction, and demand relative to international pricing. |
| L9-004 | India Physical Gold Imports and Consumer Demand | India | Captures regional physical acquisition through official trade and demand indicators. |
| L9-005 | India Gold Recycling and Gold-Loan Activity | India | Captures regional supply response and financing-linked physical-market behavior, distinct from global recycling and financial flows. |

### L9-001 — Shanghai Gold Exchange Premium/Discount

* **Variable name:** Shanghai Gold Exchange Premium/Discount
* **Layer:** 9
* **Variable ID:** L9-001
* **Causal mechanism:** Measures the price of deliverable Chinese gold relative to a comparable international reference after currency and unit conversion. A premium can indicate local physical tightness or demand; a discount can indicate weaker local demand or improved supply. VAT, contract choice, timing, and market-hour differences must be controlled.
* **Direction:** Conditional; a rising premium generally signals stronger local physical demand or tighter supply, but can also reflect taxes, capital controls, currency conversion, or reference-price timing.
* **Incremental information:** Adds direct Chinese physical-market price formation beyond L2-003 USD/CNY, T1/T3 global market variables, L0 ownership stocks, and L5 official allocation behavior.
* **Overlap:** L2-003 USD/CNY — **Transmission candidate**, but not re-admitted; future L8 Chinese ETF flows — **Transmission candidate**; L0-005 physical holdings — **Transmission candidate**; L9-002 physical demand/imports — **Interaction candidate**.
* **Data/evidence source:** Shanghai Gold Exchange market data: https://en.sge.com.cn/; World Gold Council Chinese premium/discount methodology: https://www.gold.org/sites/default/files/downloads/2019-01/Chinese-premium-discount-methodology.pdf
* **Reliability:** SGE is the authoritative market venue, but international comparison requires consistent benchmark selection, currency conversion, VAT treatment, contract choice, and timestamp alignment.
* **Historical depth:** Good modern history where SGE and international reference data are available; methodology changes require versioning.
* **Frequency:** Daily / market-day.
* **Freshness:** One day.
* **Accessibility:** Mixed; official data is public, while clean historical series may require processing or licensed distribution.
* **Operational burden:** Medium due to conversion, holidays, tax treatment, and benchmark alignment.
* **Relevant horizons:** 1–5 days; 1–3 months; 1–3 years — cyclical and regional.
* **Initial weight rationale:** Primary China physical-market anchor because it measures local price formation directly rather than inferring demand from global holdings.
* **Evidence references:** Shanghai Gold Exchange official market data; World Gold Council methodology; Causal Model v2.2, Layer 9; T4 Brief L9/L2 boundary.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L9-002 — China Physical Gold Demand and Import Signal

* **Variable name:** China Physical Gold Demand and Import Signal
* **Layer:** 9
* **Variable ID:** L9-002
* **Causal mechanism:** Measures Chinese physical acquisition and supply availability through import, retail, and institutional physical-demand indicators. Strong demand can support local premiums and alter global physical flows; weak demand can increase discounts or recycling.
* **Direction:** Conditional; stronger demand is generally supportive, but high prices, policy restrictions, property stress, and import bottlenecks can produce mixed signals.
* **Incremental information:** Adds China regional demand behavior beyond L2-003 currency transmission, L0 stock measures, L5 official-sector allocation, and L9-001 local price premium.
* **Overlap:** L9-001 SGE premium — **Interaction candidate**; L0-005 bar-and-coin holdings — **Transmission candidate**; future L8 investment flows — **Transmission candidate** where financial products are included; PBoC holdings — **Transmission candidate**, not a standalone L9 variable.
* **Data/evidence source:** Chinese official trade/customs data where accessible; SGE delivery and market reports; World Gold Council or other institutional physical-demand datasets with methodology disclosure.
* **Reliability:** Official trade data can be strong but may not capture all channels or end-use demand. Institutional demand estimates may be revised and methodology-dependent. Coverage of household demand is inherently indirect.
* **Historical depth:** Moderate to strong for trade and exchange data; weaker for household demand.
* **Frequency:** Monthly / quarterly.
* **Freshness:** Weeks to months.
* **Accessibility:** Mixed / some data is restricted or paid.
* **Operational burden:** Medium to high due to customs classification, proxy selection, revisions, and triangulation.
* **Relevant horizons:** 1–3 months; 1–3 years — cyclical and structural.
* **Initial weight rationale:** Important regional-demand candidate, but production use requires a documented composite that separates imports, exchange delivery, retail demand, and financial investment flows.
* **Evidence references:** SGE market reports; World Gold Council physical-demand methodology; Causal Model v2.2, Layer 9; T4 Brief L9/L8 boundary.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L9-003 — India Local Gold Premium/Discount

* **Variable name:** India Local Gold Premium/Discount
* **Layer:** 9
* **Variable ID:** L9-003
* **Causal mechanism:** Measures the local Indian price relative to an internationally comparable gold price after currency, duty, tax, and unit adjustments. Premiums can indicate local physical tightness or demand; discounts can indicate weak demand, abundant supply, or import friction.
* **Direction:** Conditional; a rising adjusted premium is generally supportive of regional demand, but the signal can be dominated by duties, taxes, logistics, currency moves, or reporting gaps.
* **Incremental information:** Adds India-specific physical-market price formation beyond T1/T3 global variables, L2 FX transmission, L0 holdings, and L9-004 trade/demand data.
* **Overlap:** L2 FX regime — **Transmission candidate**, not re-admitted; L9-004 imports/demand — **Interaction candidate**; L9-005 recycling/loans — **Interaction candidate**; T2 inflation variables — **Transmission candidate, now closed**.
* **Data/evidence source:** Indian bullion-market price/premium sources, official import-duty and tax data, and institutional physical-market research; final stable public series is not locked.
* **Reliability:** Local premium data is less standardized than developed-market financial data. Methodology, tax treatment, location, purity, product form, and source consistency require validation.
* **Historical depth:** Uneven; good anecdotal and market history, but consistent quantitative series are source-dependent.
* **Frequency:** Daily / weekly where available.
* **Freshness:** Days.
* **Accessibility:** Mixed / potentially paid or restricted.
* **Operational burden:** High due to source fragmentation, adjustment rules, and regional representativeness.
* **Relevant horizons:** 1–5 days; 1–3 months; 1–3 years — cyclical and seasonal.
* **Initial weight rationale:** Strong mechanism but insufficiently standardized data for immediate production; retain research-only until a stable, reproducible series is locked.
* **Evidence references:** Causal Model v2.2, Layer 9 India subsystem; T4 Brief L9 data-quality caution; official Indian customs/tax sources where applicable.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L9-004 — India Physical Gold Imports and Consumer Demand

* **Variable name:** India Physical Gold Imports and Consumer Demand
* **Layer:** 9
* **Variable ID:** L9-004
* **Causal mechanism:** Measures Indian physical acquisition through official imports and consumer-demand indicators. Higher physical demand can support local premiums and global flows; high prices, duty changes, seasonality, rural income, and recycling can offset the relationship.
* **Direction:** Conditional.
* **Incremental information:** Adds India-specific physical demand beyond L0 stock/flow variables, L2 FX conditions, T1/T3 macro variables, and L9-003 local premium data.
* **Overlap:** L0-005 bar-and-coin demand — **Transmission candidate**; L0-006 recycling — **Transmission candidate**; L9-003 premium — **Interaction candidate**; future L8 investment flows — **Transmission candidate** where financial products are included; T2 fiscal/inflation variables — **Transmission candidate, now closed**.
* **Data/evidence source:** Government of India Department of Commerce / DGCI&S trade statistics; World Gold Council and other transparent institutional demand datasets. Example official source: https://www.commerce.gov.in/
* **Reliability:** Official import statistics are strong for recorded trade but do not equal end-consumer demand and can be revised or affected by classification changes. Survey-based demand estimates require methodology review.
* **Historical depth:** Good for official imports; moderate for consumer-demand estimates.
* **Frequency:** Monthly / quarterly.
* **Freshness:** Weeks to months.
* **Accessibility:** Free / public for official trade data; institutional demand estimates may be paid.
* **Operational burden:** Medium due to customs classifications, seasonal adjustment, duty changes, and proxy interpretation.
* **Relevant horizons:** 1–3 months; 1–3 years — cyclical, seasonal, and structural.
* **Initial weight rationale:** Important India physical-demand anchor, but use imports as a supply/demand proxy rather than treating them as pure demand without triangulation.
* **Evidence references:** Government of India Department of Commerce; World Gold Council demand methodology; Causal Model v2.2, Layer 9; T4 Brief L9/L0 boundary.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L9-005 — India Gold Recycling and Gold-Loan Activity

* **Variable name:** India Gold Recycling and Gold-Loan Activity
* **Layer:** 9
* **Variable ID:** L9-005
* **Causal mechanism:** Measures regional supply from recycling and the use of gold as collateral through gold-loan activity. Rising recycling can add local physical supply, while loan activity can alter the timing and mobility of privately held gold.
* **Direction:** Conditional; increased recycling is generally negative for gold through supply, while loan activity can either mobilize supply or reflect financial stress and demand for liquidity.
* **Incremental information:** Adds India-specific physical supply and collateral behavior beyond global L0 recycling, L0 stock ownership, L7 funding conditions, and L9 demand variables.
* **Overlap:** L0-006 recycling — **Transmission candidate**; L0-008 potentially mobile gold — **Transmission candidate**; L7 financial stress — **Interaction candidate**; future L10 gold financing/microstructure — **Transmission candidate**.
* **Data/evidence source:** Indian official/statistical sources where available; RBI-regulated lender disclosures; institutional physical-market research and documented industry data.
* **Reliability:** Recycling is difficult to observe directly and gold-loan reporting is fragmented across regulated and informal channels. Public data may be incomplete and definitions may change.
* **Historical depth:** Limited to moderate, depending on the selected lender and industry series.
* **Frequency:** Monthly / quarterly / event-driven.
* **Freshness:** Weeks to months.
* **Accessibility:** Mixed / partly restricted.
* **Operational burden:** High due to fragmented coverage, lender consolidation, informal activity, and methodology changes.
* **Relevant horizons:** 1–3 months; 1–3 years — cyclical and conditional.
* **Initial weight rationale:** Mechanistically useful but not production-grade without a stable aggregate series and explicit separation of recycling from collateral-finance activity.
* **Evidence references:** Causal Model v2.2, Layer 9 India subsystem; T4 Brief L9 data-quality caution; RBI and Indian official statistical sources.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### Layer 9 summary

| Variable ID | Variable Name | Decision | Overlap Flags | Horizon(s) |
|---|---|---|---|---|
| L9-001 | Shanghai Gold Exchange Premium/Discount | ADMIT | Transmission / Interaction | 1–5D, 1–3M, 1–3Y |
| L9-002 | China Physical Gold Demand and Import Signal | CONDITIONAL / RESEARCH ONLY | Transmission / Interaction | 1–3M, 1–3Y |
| L9-003 | India Local Gold Premium/Discount | CONDITIONAL / RESEARCH ONLY | Transmission / Interaction | 1–5D, 1–3M, 1–3Y |
| L9-004 | India Physical Gold Imports and Consumer Demand | ADMIT | Transmission / Interaction | 1–3M, 1–3Y |
| L9-005 | India Gold Recycling and Gold-Loan Activity | CONDITIONAL / RESEARCH ONLY | Transmission / Interaction | 1–3M, 1–3Y |

## T5 audit-history records

## 2. Layer 8 — Investment Flows

### Candidate list

| Variable ID | Candidate | Rationale |
|---|---|---|
| L8-001 | Gold ETF Net Flows | Direct, timely investment-flow signal; distinct from L0-003 ETF holdings stock. |
| L8-002 | Bar-and-Coin Investment Flow | Physical investment demand flow; distinct from L0-005 ownership stock and regional L9 premiums. |
| L8-003 | Institutional Gold Allocation Flow | Captures fund, pension, and institutional allocation changes not fully represented by ETF flows. |
| L8-004 | Retail Gold Investment Flow | Captures smaller-investor allocation behavior, with higher measurement and interpretation risk. |

### L8-001 — Gold ETF Net Flows

* **Variable name:** Gold ETF Net Flows
* **Layer:** 8
* **Variable ID:** L8-001
* **Causal mechanism:** Measures net capital creation/redemption or equivalent gold-backed ETF demand over the observation period. Positive flows can require additional gold exposure or buying; negative flows can create supply or reduce marginal demand. The mechanism is the flow, not the monetary, geopolitical, or rate shock that caused it.
* **Direction:** Positive for net inflows; negative for net outflows.
* **Incremental information:** Adds marginal investment demand beyond L0-003 ETF holdings, which measures the stock of ETF-held gold. It is also distinct from T4 regional premiums because it measures financial allocation rather than local physical-market price formation.
* **Overlap:** L0-003 ETF holdings — **Transmission candidate**; L11-003 price-trend feedback — **Transmission candidate**; L10 ETF creation/redemption mechanics — **Interaction candidate**; T4 L9 Chinese physical demand — **Transmission candidate**.
* **Data/evidence source:** World Gold Council gold ETF holdings and flows dataset; issuer filings and fund-reported holdings; SEC filings for US products. WGC methodology/data: https://www.gold.org/goldhub/data/gold-etfs-holdings-and-flows
* **Reliability:** Strong for large physically backed products and issuer-reported holdings; global coverage, timing, fund classification, and revisions require a documented methodology. Flows may be inferred from holdings changes and price changes, so the calculation must be auditable.
* **Historical depth:** Good for major ETFs; global coverage is shorter and uneven across products.
* **Frequency:** Weekly / monthly, with some daily issuer information.
* **Freshness:** Days to one week.
* **Accessibility:** Mixed; public issuer data, with comprehensive institutional datasets potentially paid.
* **Operational burden:** Medium.
* **Relevant horizons:** 1–5 days; 1–3 months; 1–3 years — cyclical and flow-driven.
* **Initial weight rationale:** Primary L8 short-horizon flow anchor; should not receive duplicate full weight with L0-003 or L10 ETF plumbing variables.
* **Evidence references:** World Gold Council ETF methodology; issuer filings; Causal Model v2.2, Layer 8; T5 Brief L8/L0 boundary.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L8-002 — Bar-and-Coin Investment Flow

* **Variable name:** Bar-and-Coin Investment Flow
* **Layer:** 8
* **Variable ID:** L8-002
* **Causal mechanism:** Measures changes in investor purchases or sales of physical bars and coins. Positive net investment demand can absorb available supply; selling or weak demand can reduce marginal physical demand. The Layer 8 mechanism is investment allocation, not regional premium formation.
* **Direction:** Positive for net investment demand; negative for net selling.
* **Incremental information:** Adds physical-investment flow information beyond T1 L0-005 holdings/ownership and beyond T4 L9 regional premiums and import indicators.
* **Overlap:** L0-005 bar-and-coin holdings/demand — **Transmission candidate**; T4 L9 physical-demand variables — **Transmission candidate**; L11 retail sentiment — **Transmission candidate**; L0-006 recycling — **Interaction candidate**.
* **Data/evidence source:** World Gold Council investment-demand datasets, national-market sources, and transparent industry reporting; final consistent global aggregation source is not locked.
* **Reliability:** Stronger for selected major markets than for global household demand. Estimates can be survey- or model-based, with revisions, informal-market omissions, and reporting lags.
* **Historical depth:** Moderate to strong for major markets; consistent global history is uneven.
* **Frequency:** Quarterly / monthly where available.
* **Freshness:** Weeks to months.
* **Accessibility:** Mixed / some institutional data paid.
* **Operational burden:** Medium to high.
* **Relevant horizons:** 1–3 months; 1–3 years — cyclical, seasonal, and structural.
* **Initial weight rationale:** Useful physical-investment flow candidate, but production use requires a documented geography set and separation from T4 regional demand and L0 ownership measures.
* **Evidence references:** World Gold Council demand methodology; Causal Model v2.2, Layers 0, 8, and 9; T5 Brief L8/L9 boundary.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L8-003 — Institutional Gold Allocation Flow

* **Variable name:** Institutional Gold Allocation Flow
* **Layer:** 8
* **Variable ID:** L8-003
* **Causal mechanism:** Measures changes in institutional, mutual-fund, pension, or strategic portfolio allocation to gold. The flow can affect marginal price when large portfolios rebalance, but the underlying macro or risk motivation belongs elsewhere.
* **Direction:** Conditional; net allocation inflows are generally supportive, but hedging, rebalancing, and derivative overlays can make the observed allocation signal ambiguous.
* **Incremental information:** Adds institutional allocation behavior beyond ETF flows, CFTC positioning, and L0 ETF holdings. It targets capital that may be implemented through products not captured by a single ETF-flow series.
* **Overlap:** L8-001 ETF flows — **Transmission candidate**; L10 COT positioning — **Transmission candidate**; L11 narrative feedback — **Transmission candidate**; T1/T3 macro variables — **Transmission candidate**.
* **Data/evidence source:** Fund filings, institutional surveys, public portfolio disclosures, and transparent allocation datasets; comprehensive global coverage is not locked.
* **Reliability:** Public filings are authoritative but lagged and incomplete; surveys can be biased and portfolio exposures may be indirect or derivative-based.
* **Historical depth:** Uneven; good for selected funds and surveys, limited for comprehensive global flows.
* **Frequency:** Monthly / quarterly.
* **Freshness:** Weeks to quarters.
* **Accessibility:** Mixed / often paid or restricted.
* **Operational burden:** High.
* **Relevant horizons:** 1–3 months; 1–3 years — cyclical and structural.
* **Initial weight rationale:** Potentially important but insufficiently standardized for production; retain until a stable coverage universe and direct-versus-derivative exposure rule are documented.
* **Evidence references:** Public fund filings; institutional allocation surveys; Causal Model v2.2, Layer 8; T5 Brief L8 scope.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L8-004 — Retail Gold Investment Flow

* **Variable name:** Retail Gold Investment Flow
* **Layer:** 8
* **Variable ID:** L8-004
* **Causal mechanism:** Measures retail allocation into gold ETFs, funds, digital products, or other investment vehicles where the primary mechanism is direct investment flow. Retail behavior can become marginal at scale, but sentiment feedback belongs in Layer 11 when that is the stronger mechanism.
* **Direction:** Conditional.
* **Incremental information:** Adds retail-specific allocation behavior beyond aggregate ETF flows and L0 bar-and-coin holdings, potentially identifying a different marginal-holder segment.
* **Overlap:** L11 search/media sentiment — **Transmission candidate**; L8-001 ETF flows — **Duplicate candidate** where the same product is used; T4 L9 regional physical demand — **Transmission candidate**; L10 positioning — **Interaction candidate**.
* **Data/evidence source:** Product-level issuer data, retail broker/platform aggregates, and institutional retail-demand datasets; final source not locked.
* **Reliability:** Fragmented and vulnerable to survivorship, platform coverage, product reclassification, and privacy limitations. Retail flow proxies may not measure actual net gold exposure.
* **Historical depth:** Limited to moderate, source-dependent.
* **Frequency:** Daily to monthly, source-dependent.
* **Freshness:** Days to weeks.
* **Accessibility:** Mixed / often restricted or paid.
* **Operational burden:** High.
* **Relevant horizons:** 1–5 days; 1–3 months — cyclical and reflexive.
* **Initial weight rationale:** Strong conceptual relevance but weak production observability; research-only until a stable, non-duplicative retail-flow source is validated.
* **Evidence references:** Issuer disclosures; documented retail-flow datasets; Causal Model v2.2, Layer 8; T5 Brief L8/L11 boundary.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### Layer 8 summary

| Variable ID | Variable Name | Decision | Overlap Flags | Horizon(s) |
|---|---|---|---|---|
| L8-001 | Gold ETF Net Flows | ADMIT | Transmission / Interaction | 1–5D, 1–3M, 1–3Y |
| L8-002 | Bar-and-Coin Investment Flow | CONDITIONAL / RESEARCH ONLY | Transmission / Interaction | 1–3M, 1–3Y |
| L8-003 | Institutional Gold Allocation Flow | CONDITIONAL / RESEARCH ONLY | Transmission / Interaction | 1–3M, 1–3Y |
| L8-004 | Retail Gold Investment Flow | CONDITIONAL / RESEARCH ONLY | Duplicate / Transmission / Interaction | 1–5D, 1–3M |

## 3. Layer 10 — Market Microstructure and Derivatives

### Candidate list

| Variable ID | Candidate | Classification | Rationale |
|---|---|---|---|
| L10-001 | COMEX Managed-Money Net Positioning | Leading positioning signal / amplifier | Measures crowded speculative exposure that can amplify moves. |
| L10-002 | COMEX Gold Futures Open Interest | Amplifier / market-activity indicator | Measures leverage, participation, and capacity for forced repositioning. |
| L10-003 | Gold Options Implied Volatility and Skew | Amplifier / market-stress indicator | Captures priced tail risk and demand for convexity. |
| L10-004 | Gold Futures Basis and Funding Stress | Amplifier / market-stress indicator | Measures futures-cash dislocation and financing conditions; distinct from L0 lease-rate stock mobility. |
| L10-005 | Margin and Forced-Liquidation Stress | Market-stress indicator | Captures mechanical deleveraging and liquidation risk during sharp moves. |

### L10-001 — COMEX Managed-Money Net Positioning

* **Variable name:** COMEX Managed-Money Net Positioning
* **Layer:** 10
* **Variable ID:** L10-001
* **Causal mechanism:** Measures net long or short futures exposure of the CFTC managed-money category. Crowded positioning can amplify a fundamental shock through liquidation, stop-losses, or trend-following, but is generally an amplifier rather than an independent fundamental cause.
* **Direction:** Conditional; extreme net length can increase downside liquidation risk, while extreme net short exposure can increase squeeze risk.
* **Incremental information:** Adds observable speculative positioning beyond T1/T3 macro variables, L8 flows, and L0 stock measures. It captures market crowding and asymmetric mechanical response.
* **Overlap:** L8 institutional flows — **Transmission candidate**; L10 open interest — **Interaction candidate**; L11 trend/reflexivity — **Transmission candidate**; CFTC commercial positioning — **Duplicate candidate** if combined without distinct interpretation.
* **Data/evidence source:** CFTC Disaggregated Commitments of Traders reports: https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm
* **Reliability:** Strong official weekly source with defined trader categories; data is as of Tuesday and released later, classifications are aggregate, and positions are not a complete view of OTC/options exposure.
* **Historical depth:** Good modern history; CFTC historical files support long back series with classification caveats.
* **Frequency:** Weekly.
* **Freshness:** Several days; stale during fast markets.
* **Accessibility:** Free / public.
* **Operational burden:** Low to medium.
* **Relevant horizons:** 1–5 days; 1–3 months — cyclical and amplifier-driven.
* **Initial weight rationale:** Primary L10 positioning anchor, used as an amplifier/leading positioning signal rather than a standalone directional fundamental driver.
* **Evidence references:** CFTC COT methodology and release schedule; Causal Model v2.2, Layer 10; T5 Brief amplifier classification rule.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L10-002 — COMEX Gold Futures Open Interest

* **Variable name:** COMEX Gold Futures Open Interest
* **Layer:** 10
* **Variable ID:** L10-002
* **Causal mechanism:** Measures outstanding futures contracts and therefore the scale of leveraged participation and potential repositioning. Rising open interest can reinforce trends or increase future liquidation capacity; interpretation is conditional on price, volume, and trader composition.
* **Direction:** Conditional.
* **Incremental information:** Adds total futures-market participation and leverage capacity beyond COT category positioning and L8 flows. It is a market-plumbing measure, not a claim that open interest independently causes gold direction.
* **Overlap:** L10 managed-money positioning — **Interaction candidate**; L10 margin/liquidation stress — **Transmission candidate**; L8 ETF flows — **Transmission candidate**; future L11 trend signal — **Interaction candidate**.
* **Data/evidence source:** CME Group daily volume/open-interest reports: https://www.cmegroup.com/market-data/volume-open-interest.html
* **Reliability:** Exchange-reported data is authoritative; contract rolls, spreads, delivery months, and post-settlement revisions require consistent treatment.
* **Historical depth:** Good modern exchange history, with contract and reporting-method changes requiring documentation.
* **Frequency:** Daily.
* **Freshness:** One business day.
* **Accessibility:** Free / public summary data; granular data may be paid.
* **Operational burden:** Low to medium.
* **Relevant horizons:** 1–5 days; 1–3 months — amplifier and market-activity regime.
* **Initial weight rationale:** Admitted as a market-capacity amplifier; should not be interpreted directionally without positioning, price, volume, or stress context.
* **Evidence references:** CME Group volume/open-interest data; Causal Model v2.2, Layer 10; T5 Brief amplifier classification rule.
* **Decision:** **ADMIT**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L10-003 — Gold Options Implied Volatility and Skew

* **Variable name:** Gold Options Implied Volatility and Skew
* **Layer:** 10
* **Variable ID:** L10-003
* **Causal mechanism:** Measures the market price of expected volatility and asymmetric protection in gold options. Elevated implied volatility or downside skew can indicate stress and increase the transmission magnitude of a shock; the variable is an amplifier/market-stress indicator.
* **Direction:** Conditional; volatility and skew do not determine direction without identifying whether demand is for upside or downside protection.
* **Incremental information:** Adds priced tail-risk and convexity information beyond futures positioning, open interest, and L11 sentiment variables.
* **Overlap:** L11 options sentiment — **Interaction candidate**; L10 open interest — **Transmission candidate**; L10 margin/liquidation stress — **Interaction candidate**; L8 institutional flows — **Transmission candidate**.
* **Data/evidence source:** CME/COMEX options data and transparent options-implied-volatility calculations; vendor data may be required for complete surface history.
* **Reliability:** Exchange inputs are strong, but surface construction, stale strikes, sparse liquidity, contract rolls, and skew definitions create methodology risk.
* **Historical depth:** Moderate; continuous clean surface history is source-dependent.
* **Frequency:** Daily / intraday.
* **Freshness:** Hours to one day.
* **Accessibility:** Mixed / granular data may be paid.
* **Operational burden:** High.
* **Relevant horizons:** 1–5 days; 1–3 months — event-driven and market-stress.
* **Initial weight rationale:** Strong mechanism but production requires a reproducible surface-selection and skew definition; retain research-only until validated.
* **Evidence references:** CME options data; Causal Model v2.2, Layer 10; T5 Brief L10/L11 boundary.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L10-004 — Gold Futures Basis and Funding Stress

* **Variable name:** Gold Futures Basis and Funding Stress
* **Layer:** 10
* **Variable ID:** L10-004
* **Causal mechanism:** Measures futures-cash dislocation, roll yield, and related financing stress in gold derivatives. The L10 mechanism is derivatives-market transmission and stress; L0-009 remains the stock-mobility/physical-financing variable.
* **Direction:** Conditional; abnormal positive or negative basis can signal differing scarcity, funding, or positioning conditions.
* **Incremental information:** Adds derivatives-market dislocation beyond L0-009's bullion-stock mobility mechanism, L7 funding stress, and L10 positioning variables.
* **Overlap:** L0-009 lease/forward rates — **Transmission candidate** with a distinct mechanism; L7 repo/funding stress — **Interaction candidate**; L10 open interest — **Interaction candidate**; L8 ETF flows — **Transmission candidate**.
* **Data/evidence source:** CME futures prices, spot/reference prices, lease/financing data where available, and transparent roll/basis calculations.
* **Reliability:** Futures prices are strong; spot comparison, contract timing, financing assumptions, and lease-rate access can limit reliability. Basis can be distorted by delivery, convenience yield, and contract rolls.
* **Historical depth:** Moderate to strong for futures; clean comparable basis history depends on spot and financing sources.
* **Frequency:** Daily / intraday.
* **Freshness:** Hours to one day.
* **Accessibility:** Mixed / some inputs restricted.
* **Operational burden:** High.
* **Relevant horizons:** 1–5 days; 1–3 months — market-stress and amplifier.
* **Initial weight rationale:** Useful microstructure candidate, but retain research-only until the calculation is demonstrably distinct from L0-009 and L7 funding measures.
* **Evidence references:** CME futures data; Causal Model v2.2, Layers 0, 7, and 10; T5 Brief L10/L0 boundary.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L10-005 — Margin and Forced-Liquidation Stress

* **Variable name:** Margin and Forced-Liquidation Stress
* **Layer:** 10
* **Variable ID:** L10-005
* **Causal mechanism:** Measures exchange margin changes, leveraged-position stress, liquidation cascades, and related mechanical selling or buying. It is a market-stress indicator and amplifier, not an independent fundamental cause.
* **Direction:** Conditional; forced selling is usually negative in the acute phase, while short-covering or restored market function can produce the opposite effect.
* **Incremental information:** Adds mechanical liquidation conditions beyond COT positioning, open interest, credit spreads, and repo stress. It captures the immediate market-plumbing pathway from stress to price.
* **Overlap:** L10 open interest and positioning — **Transmission candidate**; L7 funding stress — **Interaction candidate**; L8 ETF redemptions — **Transmission candidate**; L11 reflexive liquidation narrative — **Interaction candidate**.
* **Data/evidence source:** CME margin advisories, exchange notices, open-interest/volume data, and documented liquidation proxies; complete forced-liquidation data is not generally public.
* **Reliability:** Margin notices are authoritative; actual liquidation estimates are indirect and can be highly uncertain. Attribution must not convert price declines into proof of liquidation.
* **Historical depth:** Event-based history is available; consistent quantitative liquidation history is limited.
* **Frequency:** Event-driven / daily.
* **Freshness:** Hours to days.
* **Accessibility:** Free/public for notices; liquidation estimates mixed or restricted.
* **Operational burden:** High.
* **Relevant horizons:** 1–5 days; 1–3 months — event-driven market stress.
* **Initial weight rationale:** Strong amplifier concept but weak direct observability; research-only until a reproducible proxy and validation set are established.
* **Evidence references:** CME margin and market notices; Causal Model v2.2, Layer 10; T5 Brief amplifier classification rule.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### Layer 10 summary

| Variable ID | Variable Name | Decision | Overlap Flags | Horizon(s) |
|---|---|---|---|---|
| L10-001 | COMEX Managed-Money Net Positioning | ADMIT | Transmission / Interaction | 1–5D, 1–3M |
| L10-002 | COMEX Gold Futures Open Interest | ADMIT | Transmission / Interaction | 1–5D, 1–3M |
| L10-003 | Gold Options Implied Volatility and Skew | CONDITIONAL / RESEARCH ONLY | Transmission / Interaction | 1–5D, 1–3M |
| L10-004 | Gold Futures Basis and Funding Stress | CONDITIONAL / RESEARCH ONLY | Transmission / Interaction | 1–5D, 1–3M |
| L10-005 | Margin and Forced-Liquidation Stress | CONDITIONAL / RESEARCH ONLY | Transmission / Interaction | 1–5D, 1–3M |

## 4. Layer 11 — Expectations, Psychology, and Reflexivity

### Candidate list

| Variable ID | Candidate | Rationale |
|---|---|---|
| L11-001 | Gold Search-Intensity Signal | Observable attention/interest input, but sampled and normalized data requires candid quality controls. |
| L11-002 | Financial-Media Gold Narrative Intensity | Captures narrative propagation and attention beyond direct flows and positioning. |
| L11-003 | Price-Trend and Reflexive Momentum Signal | Captures the price-to-attention-to-flow feedback loop rather than treating price trend as a fundamental cause. |
| L11-004 | Retail Sentiment and Speculative-Attention Survey | Captures self-reported or measured sentiment, with source and manipulation risk. |

### L11-001 — Gold Search-Intensity Signal

* **Variable name:** Gold Search-Intensity Signal
* **Layer:** 11
* **Variable ID:** L11-001
* **Causal mechanism:** Measures public search attention for gold-related topics. Rising attention can increase narrative salience and feed subsequent retail demand, media coverage, and flows; the signal is reflexive only when linked to subsequent behavior, not merely because searches rise.
* **Direction:** Conditional; attention can accompany buying enthusiasm, fear-driven safe-haven demand, or liquidation interest.
* **Incremental information:** Adds public attention and narrative salience beyond L8 flows, L10 positioning, and T1–T4 fundamental variables.
* **Overlap:** L8 retail flows — **Transmission candidate**; L11 media narrative — **Interaction candidate**; L11 price-trend signal — **Interaction candidate**; L6 geopolitical news — **Transmission candidate**.
* **Data/evidence source:** Google Trends: https://trends.google.com/; official methodology and limitations: https://support.google.com/trends/answer/4365533?hl=en
* **Reliability:** Google states that Trends is a normalized sample, not a poll; results are affected by sampling, query choice, seasonality, low-volume noise, and rare irregular activity. Criterion C is therefore weak-to-moderate and requires fixed topics, geographies, anchors, and robustness checks.
* **Historical depth:** Good for selected terms, but comparable history is affected by normalization and query/topic changes.
* **Frequency:** Daily / weekly.
* **Freshness:** Days to weeks.
* **Accessibility:** Free / public.
* **Operational burden:** Medium to high due to query governance, sampling instability, geographic selection, and preprocessing.
* **Relevant horizons:** 1–5 days; 1–3 months — reflexive and cyclical; conditional 1–3 years.
* **Initial weight rationale:** Important attention candidate but too noisy for immediate production without a pre-specified query bank and validation against actual flows.
* **Evidence references:** Google Trends methodology and FAQ; Causal Model v2.2, Layer 11; T5 Brief L11 Criterion C scrutiny.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L11-002 — Financial-Media Gold Narrative Intensity

* **Variable name:** Financial-Media Gold Narrative Intensity
* **Layer:** 11
* **Variable ID:** L11-002
* **Causal mechanism:** Measures the volume and direction of gold-related financial-media narratives. Repeated coverage can increase attention, perceived confirmation, and subsequent allocation, creating feedback between price, narrative, and flows.
* **Direction:** Conditional; positive narrative intensity can reflect bullish enthusiasm or crisis fear and therefore requires direction classification and counter-evidence.
* **Incremental information:** Adds narrative propagation beyond realized investment flows, COT positioning, and formal geopolitical or macro variables.
* **Overlap:** L6 geopolitical-news signals — **Transmission candidate**; L11 search intensity — **Interaction candidate**; L8 flows — **Transmission candidate**; L10 positioning — **Interaction candidate**.
* **Data/evidence source:** Reproducible news archive or licensed media dataset with documented corpus, deduplication, language coverage, and sentiment/topic methodology.
* **Reliability:** Narrative volume is not equivalent to investor belief or buying; source selection, repeated syndication, automated text classification, and editorial bias are material risks. No production source is locked.
* **Historical depth:** Source-dependent; long archives exist but methodology consistency is uncertain.
* **Frequency:** Daily / weekly.
* **Freshness:** Hours to days.
* **Accessibility:** Mixed / often paid or restricted.
* **Operational burden:** High.
* **Relevant horizons:** 1–5 days; 1–3 months — reflexive and event-driven; conditional 1–3 years.
* **Initial weight rationale:** Strong conceptual reflexivity case but source and classification risks require research-only status until a reproducible corpus and validation process are established.
* **Evidence references:** Causal Model v2.2, Layer 11; T5 Brief L11 scope and Criterion C rules; candidate news-archive methodology to be locked.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L11-003 — Price-Trend and Reflexive Momentum Signal

* **Variable name:** Price-Trend and Reflexive Momentum Signal
* **Layer:** 11
* **Variable ID:** L11-003
* **Causal mechanism:** Measures whether recent gold price gains or losses are persistent enough to plausibly influence attention, trend-following, and subsequent flows. The Layer 11 mechanism is the price-to-behavior feedback loop; raw momentum as a market signal belongs in Layer 10 unless this feedback mechanism is explicitly established.
* **Direction:** Conditional; positive trend can reinforce buying and negative trend can reinforce liquidation, but reversals and crowded positioning can dominate.
* **Incremental information:** Adds reflexive feedback information beyond L10 positioning and L8 flows by measuring the potential behavioral response to prior price movement.
* **Overlap:** L10 positioning/trend mechanics — **Transmission candidate**; L8 ETF and retail flows — **Transmission candidate**; L11 search/media attention — **Interaction candidate**; T1/T3 directional variables — **Transmission candidate**.
* **Data/evidence source:** Gold spot/futures price history and a pre-specified trend construction; final separation between L10 technical signal and L11 reflexivity is not locked.
* **Reliability:** Price data is strong, but the reflexive interpretation is not directly observed and is vulnerable to hindsight, parameter selection, and double-counting with L10.
* **Historical depth:** Good for gold price history; reflexivity validation requires a defined historical event and flow framework.
* **Frequency:** Daily / weekly.
* **Freshness:** One day to one week.
* **Accessibility:** Free / public for major price series.
* **Operational burden:** Medium.
* **Relevant horizons:** 1–5 days; 1–3 months; 1–3 years — cyclical and reflexive.
* **Initial weight rationale:** Potentially useful bridge between price and behavior, but research-only until its construction is demonstrably distinct from L10 and linked to subsequent flows or attention.
* **Evidence references:** Causal Model v2.2, Layer 11; T5 Brief L10/L11 boundary; approved price-series sources to be documented in implementation.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### L11-004 — Retail Sentiment and Speculative-Attention Survey

* **Variable name:** Retail Sentiment and Speculative-Attention Survey
* **Layer:** 11
* **Variable ID:** L11-004
* **Causal mechanism:** Measures self-reported or observed retail expectations and speculative attention that may influence subsequent gold purchases, narratives, and positioning. The variable is a feedback indicator, not a direct demand-flow measure.
* **Direction:** Conditional.
* **Incremental information:** Adds explicit sentiment/attention information beyond L8 retail flows, L11 search data, and L10 positioning, if the survey reaches a distinct population and preserves time consistency.
* **Overlap:** L8 retail flow — **Transmission candidate**; L11 search/media variables — **Interaction candidate**; L10 positioning — **Interaction candidate**; L6 event narratives — **Transmission candidate**.
* **Data/evidence source:** A stable, repeated, transparent survey or platform dataset with documented sampling, question wording, population, and revision policy; no production source is currently locked.
* **Reliability:** High risk of sampling bias, nonresponse, changing platform composition, strategic responses, and manipulation. A convenient social-media proxy is not sufficient for admission to production.
* **Historical depth:** Limited to moderate, source-dependent.
* **Frequency:** Weekly / monthly.
* **Freshness:** Days to weeks.
* **Accessibility:** Mixed / potentially restricted.
* **Operational burden:** High.
* **Relevant horizons:** 1–3 months; 1–3 years — reflexive and cyclical.
* **Initial weight rationale:** Retain only as research because the causal role is plausible but Criterion C and operational feasibility are currently weak.
* **Evidence references:** Spec D v2; Causal Model v2.2, Layer 11; T5 Brief L11 Criterion C scrutiny.
* **Decision:** **CONDITIONAL / RESEARCH ONLY**
* **Review date:** 2026-08-17
* **Reviewer:** Grace

### Layer 11 summary

| Variable ID | Variable Name | Decision | Overlap Flags | Horizon(s) |
|---|---|---|---|---|
| L11-001 | Gold Search-Intensity Signal | CONDITIONAL / RESEARCH ONLY | Transmission / Interaction | 1–5D, 1–3M, conditional 1–3Y |
| L11-002 | Financial-Media Gold Narrative Intensity | CONDITIONAL / RESEARCH ONLY | Transmission / Interaction | 1–5D, 1–3M, conditional 1–3Y |
| L11-003 | Price-Trend and Reflexive Momentum Signal | CONDITIONAL / RESEARCH ONLY | Transmission / Interaction | 1–5D, 1–3M, 1–3Y |
| L11-004 | Retail Sentiment and Speculative-Attention Survey | CONDITIONAL / RESEARCH ONLY | Transmission / Interaction | 1–3M, 1–3Y |

