# Gold Probability Engine — Phase 1 Variable Registry
## Tranche 3 (T3) — Final Admission Records

**Status:** SIGNED OFF — 2026-08-17  
**Tranche:** T3 — Layers 2 and 7  
**Prepared:** 2026-08-17  
**Prepared by:** Grace  
**Criterion B baseline:** Signed-off T1 approved registry in `docs/phase1-registry/T1-registry.md`  
**T2 treatment:** T2 registry exists as a pending working document. T2 candidates are not part of the T3 baseline; possible overlaps are flagged below.

## 1. Scope and candidate selection

T3 uses a deliberately limited set. Layer 2 captures FX valuation, non-US purchasing-power transmission, regional currency transmission, and FX-specific dollar-funding conditions. Layer 7 captures realized liquidity, credit capacity, funding stress, and financial-system balance-sheet conditions. Forward monetary-policy expectations remain Layer 3; investment flows remain reserved for Layer 8.

The candidate set excludes EUR/USD and USD/JPY as standalone production variables because their broad information is substantially represented by the dollar-index variables, while their regional mechanisms can be monitored as diagnostic context. It also excludes cross-border capital flows from Layer 7 because resulting asset flows belong primarily in Layer 8.

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

## 4. Cross-layer overlap notes

- **L2 versus L1/L3:** DXY, broad USD, and USD/CNY must be scored for FX valuation and non-US purchasing-power transmission. Their use as proxies for expected Fed tightening belongs in Layer 3, not Layer 2. Their shared movement with T1 real yields is a transmission flag, not automatic rejection.
- **L2 versus L4:** T2 breakevens are forward purchasing-power variables. USD strength can affect breakeven pricing through liquidity and imported-price channels. This is an interaction to document after T2 review; it does not transfer the L2 FX variables into L4 or vice versa.
- **L2 versus future L9:** L2-003 USD/CNY is admitted in Layer 2 for its FX purchasing-power and dollar-transmission mechanism. The T4 Layer 9 brief should reference L2-003 and should not re-admit USD/CNY as an independent Layer 9 variable; regional physical-market conditions should instead use Layer 9 observables such as SGE premium, local demand, and capital controls.
- **L2 versus L7:** Cross-currency basis is retained as a research-only L2 candidate because it measures FX-market pricing of dollar funding. Repo stress and reserve plumbing remain L7 because their primary mechanism is realized funding-market function and balance-sheet capacity.
- **L7 versus L3:** L7-001 and L7-006 must use realized balance-sheet/liquidity conditions. Expected future easing remains in T1 Layer 3. No numerical dependency treatment is assigned in T3.
- **L7 versus L1:** L7-004 credit spreads represent financing capacity and stress. L1 real yields and term premium represent opportunity cost and government-bond pricing. Their interaction is plausible, but neither is rejected for being downstream of a common macro shock.
- **L7 versus T2 fiscal variables:** T2 Treasury maturity and issuance candidates may interact with reserve plumbing and funding stress. T2 decisions are pending and do not form the T3 Criterion B baseline.
- **L7 versus future L8:** No investment-flow variable is admitted in T3. Credit and liquidity conditions may transmit into future investment flows, but the resulting flows remain Layer 8 scope.
- **L7 versus future L10:** Repo and credit stress are system-financing conditions. Futures positioning, options, margin, and forced liquidation mechanics remain Layer 10 scope.

## 5. T3 decision summary

| Layer | Candidates | ADMIT | CONDITIONAL / RESEARCH ONLY | REJECT |
|---|---:|---:|---:|---:|
| Layer 2 | 5 | 3 | 2 | 0 |
| Layer 7 | 6 | 4 | 2 | 0 |
| **Total** | **11** | **7** | **4** | **0** |

## 6. Governance notes

- No layer-level weights were changed.
- No numerical duplication factors, transmission factors, or interaction coefficients were assigned.
- T2 candidates were not used as the Criterion B baseline.
- No historical quantitative observations were fabricated.
- Conditional variables remain research-only and are not production scoring inputs until their stated source, methodology, and operational requirements are resolved.
- Initial weights remain research-derived implementation work; admission does not set production parameters.

## 7. Open Items Carried Forward

| ID | Item | Required Before |
|---|---|---|
| L2-001/L2-002 | Designate the primary L2 dollar anchor or establish dependency treatment to prevent double-weighting | Spec A implementation |
| L7-002 | Validate the multi-country aggregation methodology, country set, currency conversion, weighting, and missing-data treatment | Phase 2 |
| L7-005 | Pre-specify the stress-transformation rule and validate it against known funding-stress episodes | Phase 2 |
| L7-006 | Validate the composite formula, including sign convention, timing alignment, and reserve-demand regime controls | Phase 2 |
