# Gold Probability Engine — Phase 1 Variable Registry
## Tranche 5 (T5) — Final Admission Records

**Status:** SIGNED OFF
**Sign-off date:** 2026-08-17
**Signed off by:** Chris (Pragmatic Project Advisor)
**Reviewed by:** Chris (Pragmatic Project Advisor)  
**Tranche:** T5 — Layers 8, 10, and 11  
**Prepared:** 2026-08-17  
**Prepared by:** Grace  
**Criterion B baseline:** Closed T1, T2, T3, and T4 registries  
**Scope note:** T5 closes Phase 1. Upstream causes remain in their causal layers; T5 records flows, amplifiers, market plumbing, and reflexive feedback only.

## 1. Candidate selection

Layer 8 captures actual investment allocation flows. Layer 10 captures market amplification and transmission mechanics. Layer 11 captures feedback between price, narrative, attention, and subsequent behavior. The same observable is not admitted independently into multiple layers when its primary mechanism can be assigned clearly.

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

## 5. Cross-layer overlap notes

- **L8 versus L0:** L0-003 is the stock of ETF-held gold; L8-001 is the change in that stock through net investment flows. They may coexist only with explicit stock-versus-flow separation.
- **L8 versus L9:** L8-002 and L9 regional demand variables can use related data, but L8 owns investment-allocation flow and L9 owns regional physical-market price formation. Chinese ETF flows should not be admitted independently in both layers.
- **L8 versus L11:** L8-004 owns direct retail allocation flow. L11 owns the feedback mechanism between attention, price, narrative, and later behavior. Do not score the same retail-flow observation twice.
- **L10 versus L0:** L0-009 remains the physical-stock mobility/financing variable. L10-004 is conditional and would require a distinct derivatives-basis mechanism before production admission.
- **L10 versus L8:** ETF creation/redemption plumbing is a market-mechanics question; net ETF flow demand remains L8. Attribute any future variable to one primary layer.
- **L10 versus L11:** Positioning and options variables remain L10 when the mechanism is leverage, convexity, or stress. They belong in L11 only when the evidence specifically supports sentiment/reflexive feedback.
- **L11 versus L6:** News attention may respond to geopolitical events. L6 owns the geopolitical trigger; L11 owns any separately demonstrated attention-to-behavior feedback.
- **L11 versus T1–T4:** Price trend, search, and narrative variables must not be used as substitutes for causal macro, FX, liquidity, geopolitical, or regional physical variables. Their role is feedback amplification only.
- **T2/T4 overlap:** T2 and T4 are treated as closed project context. Their flow, regional, and narrative-adjacent variables remain mechanism-specific and are not duplicated by T5 records.

## 6. T5 decision summary

| Layer | Candidates | ADMIT | CONDITIONAL / RESEARCH ONLY | REJECT |
|---|---:|---:|---:|---:|
| Layer 8 | 4 | 1 | 3 | 0 |
| Layer 10 | 5 | 2 | 3 | 0 |
| Layer 11 | 4 | 0 | 4 | 0 |
| **Total** | **13** | **3** | **10** | **0** |

## 7. Open Items Carried Forward

| ID | Item | Required Before |
|---|---|---|
| L8-002 | Lock a documented geography set and separate physical investment flows from L0 ownership and T4 regional-demand measures | Production admission |
| L8-003 | Validate a stable institutional coverage universe and direct-versus-derivative exposure rule | Production admission |
| L8-004 | Validate a stable, non-duplicative retail-flow source | Production admission |
| L10-003 | Pre-specify options-surface construction, strike selection, and skew definition | Production admission |
| L10-004 | Demonstrate a derivatives-basis mechanism distinct from L0-009 and L7 funding stress | Production admission |
| L10-005 | Establish a reproducible liquidation proxy and validation event set | Production admission |
| L11-001 | Lock a query bank, geography, anchor, normalization, and robustness procedure | Production admission |
| L11-002 | Lock a reproducible media corpus, deduplication method, and narrative classifier | Production admission |
| L11-003 | Demonstrate separation from L10 trend/positioning signals and linkage to subsequent behavior | Production admission |
| L11-004 | Lock a stable survey or platform source with documented sampling and manipulation controls | Production admission |

## 8. Governance notes

- No layer-level weights were changed.
- No numerical duplication factors, transmission factors, or interaction coefficients were assigned.
- L0-003 ETF holdings and L8-001 ETF flows were kept mechanistically distinct.
- L0-009 lease/forward rates were not re-admitted in Layer 10 for the same physical-financing mechanism.
- No historical quantitative observations were fabricated.
- Conditional variables remain research-only until their stated source, methodology, and operational requirements are resolved.
- Initial weights remain research-derived implementation work; admission does not set production parameters.

## 9. Spec A implementation note (added at sign-off)

When Spec A implementation assigns numerical D_i and T_i values in a later phase, L10-001 (COMEX Managed-Money Net Positioning) and L11-003 (Price-Trend and Reflexive Momentum Signal) are expected to carry the heaviest transmission discounts in the system. Both are downstream amplifiers or feedback variables whose information largely reflects upstream causal drivers already captured in T1–T4. Their effective weights must reflect this amplifier-only role rather than treating them as independent fundamental signals.

## 10. Phase 1 completion

T5 is the final Phase 1 tranche. With T5 signed off, the Phase 1 Variable Registry is complete across all 12 causal layers.

**Full Phase 1 registry totals:**

| Tranche | Layers | ADMIT | CONDITIONAL | REJECT |
|---|---|---:|---:|---:|
| T1 | 0, 1, 3 | 16 | 8 | 0 |
| T2 | 4, 5 | 10 | 6 | 0 |
| T3 | 2, 7 | 7 | 4 | 0 |
| T4 | 6, 9 | 4 | 6 | 0 |
| T5 | 8, 10, 11 | 3 | 10 | 0 |
| **Phase 1 Total** | **All 12** | **40** | **34** | **0** |

Phase 2 (Data Ingestion) is the next milestone.
