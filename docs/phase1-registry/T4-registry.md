# Gold Probability Engine — Phase 1 Variable Registry
## Tranche 4 (T4) — Final Admission Records

**Status:** SIGNED OFF — 2026-08-17  
**Tranche:** T4 — Layers 6 and 9  
**Prepared:** 2026-08-17  
**Prepared by:** Grace  
**Criterion B baseline:** Closed T1 and T3 approved registries  
**T2 treatment:** T2 is treated as closed per current project direction; T2 overlaps are flagged where relevant and do not alter the T4 layer ownership.

## 1. Scope and candidate selection

Layer 6 is split into the four approved geopolitical channels: safe haven, energy/inflation, reserve security, and monetary-system fragmentation. Layer 9 is split into China and India physical-market subsystems. L2-003 USD/CNY is not re-admitted in Layer 9; Layer 8 investment flows, Layer 10 market microstructure, and Layer 11 psychology remain outside T4.

Most Layer 6 variables are Type B analytical variables. Any weekly production assessment must separately record facts, evidence, assessment, stance, confidence, counter-evidence, the confidence rubric, fact/interpretation boundaries, timestamps, and provenance under Spec D. An admission record is not a substitute for that weekly evidence record.

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

## 4. Cross-layer overlap notes

- **L6 versus L4/L3:** L6-003 captures geopolitical energy/shipping disruption as the causal trigger. T2 inflation variables and T1/L3 policy variables capture the resulting inflation and policy repricing. Do not score the same oil move as a full independent contribution in both layers.
- **L6 versus L5:** L6-002 and L6-004 capture geopolitical reserve-security triggers and access risk. L5 captures the resulting official-sector allocation behavior. A sanctions event is not itself a gold-purchase variable.
- **L6 versus L7:** L6-005 captures the geopolitical driver of monetary fragmentation; L7 captures realized liquidity and funding conditions. Avoid double-counting the same fragmentation development through both layers.
- **L6 analytical governance:** L6-001, L6-003, L6-004, and L6-005 require Spec D weekly evidence records. No free-form geopolitical confidence or automatic bullish label is permitted.
- **L9 versus L2:** L2-003 USD/CNY is not re-admitted in Layer 9. L9-001 and L9-002 measure Chinese physical-market behavior; currency effects are contextual or interaction evidence, not a second L2 signal.
- **L9 versus L0:** L9 records regional demand, premium, supply, and financing behavior. L0 stock/ownership variables remain distinct; a regional central-bank holding change belongs in L0/L5 unless its specific mechanism is local physical-market price formation.
- **L9 versus future L8:** Chinese ETF flows and other financial investment flows are not admitted as standalone T4 production variables. If later included in L9, the mechanism must be regional physical-demand transmission rather than generic investment allocation.
- **L9 versus future L10:** Gold-loan activity may interact with financing and market plumbing, but T4 does not admit derivatives, positioning, margin, or forced-liquidation variables.
- **T2 overlap:** T2 inflation, fiscal, and reserve-allocation candidates are treated as closed per current project direction. Their related channels are flagged for mechanism separation, not used to change T4 decisions.

## 5. T4 decision summary

| Layer | Candidates | ADMIT | CONDITIONAL / RESEARCH ONLY | REJECT |
|---|---:|---:|---:|---:|
| Layer 6 | 5 | 2 | 3 | 0 |
| Layer 9 | 5 | 2 | 3 | 0 |
| **Total** | **10** | **4** | **6** | **0** |

## 6. Governance notes

- No layer-level weights were changed.
- No numerical duplication factors, transmission factors, or interaction coefficients were assigned.
- L2-003 USD/CNY was not re-admitted in Layer 9.
- No historical quantitative observations were fabricated.
- Conditional variables remain research-only until their stated source, methodology, and operational requirements are resolved.
- Layer 6 analytical variables require the complete Spec D evidence record during weekly production.
- Initial weights remain research-derived implementation work; admission does not set production parameters.

## 7. Open Items Carried Forward

| ID | Item | Required Before |
|---|---|---|
| L6-003 | Establish a reproducible geopolitical-causality classification and explicitly separate the signal from T2 inflation and L3 policy repricing | Production admission |
| L6-004 | Establish a repeatable evidence and scoring procedure for forward-looking sovereign-asset access risk | Production admission |
| L6-005 | Define observable fragmentation milestones and an auditable Spec D evidence rubric | Production admission |
| L9-002 | Define a documented composite separating imports, exchange delivery, retail demand, and investment flows | Production admission |
| L9-003 | Lock a stable, reproducible India local-premium series and adjustment methodology | Production admission |
| L9-005 | Establish a stable aggregate series and separate recycling from collateral-finance activity | Production admission |
