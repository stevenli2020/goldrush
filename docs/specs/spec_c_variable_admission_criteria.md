# Gold Probability Engine — Spec C
## Variable Admission Criteria

**Status:** Draft for external review  
**Purpose:** Define when a new variable may be admitted into one of the 12 locked causal layers.

---

## 1. Objective

The 12-layer causal architecture is fixed.

The **variables within each layer are expandable** when a genuinely useful new variable is identified.

Spec C establishes a consistent admission gate so that:

- useful variables can be added;
- redundant variables are not added merely because they are available;
- weak or unreliable data does not enter the production model;
- variable expansion does not silently alter the layer architecture;
- a new variable does not automatically change cross-layer weights.

The goal is **controlled extensibility**, not exhaustive collection of every variable that could possibly affect gold.

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

---

### Criterion B — Incremental Information

The candidate must add information that is not already adequately represented by the existing variable set.

The baseline for this assessment is:

> **the currently approved variable set within the proposed layer, plus materially overlapping variables in other layers where relevant.**

The candidate does **not** need to be completely unique.

It may still qualify when it:

- measures the same broad phenomenon more directly;
- captures a different transmission channel;
- provides information at a different frequency;
- provides earlier information;
- improves regional or regime-specific coverage;
- captures an interaction or condition not represented elsewhere.

The submission must explicitly state:

> **What information does this variable add that the current system does not already capture adequately?**

---

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

---

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

---

### Criterion E — Forecast-Horizon Relevance

The variable must have a meaningful role in at least one of the four fixed horizons:

- **1–5 days**
- **1–3 months**
- **1–3 years**
- **3–10 years**

The admission record must specify:

- relevant horizon(s);
- expected importance by horizon;
- whether relevance is structural, cyclical, event-driven, or conditional.

A variable does **not** need to be relevant to all four horizons.

---

## 4. Admission Decision

A candidate variable receives one of three statuses:

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
| Overlap | Existing variables with similar information |
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

Adding a variable does **not** automatically change layer weights or other layers.

When a new variable is admitted:

1. assign an initial variable weight within its layer;
2. redistribute existing **within-layer variable weights** as necessary;
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

Primarily **Layer 1 — Real Rates / Opportunity Cost** or another layer depending on the researched mechanism.

### Causal relevance

Potentially relevant because the ratio may contain information about relative precious-metals demand, monetary stress, industrial-cycle conditions, or changes in the relative attractiveness of monetary versus industrial metals.

### Incremental-information question

The variable should not be admitted merely because it correlates with gold.

The key question is:

> **Does the gold/silver ratio provide information about future gold direction that is not already adequately represented by the existing Layer 1/other-layer variables?**

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

A variable should **not** be admitted solely because:

- an AI agent suggests it;
- traders frequently discuss it;
- it appears correlated over a short period;
- it is easy to retrieve;
- it “sounds economically logical.”

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

The following rules prevent variable proliferation:

### Rule 1
A variable should not be added merely because it is available.

### Rule 2
A variable should not be added merely because it has a historical correlation with gold.

### Rule 3
A variable should not be added if its information is already adequately captured elsewhere without a clear incremental benefit.

### Rule 4
Every admitted variable must have an identified horizon of relevance.

### Rule 5
Every admitted variable must have a documented source/evidence trail.

### Rule 6
New variables do not automatically alter layer-level weights.

### Rule 7
The number of variables should remain **only as large as necessary to represent the layer adequately**.

---

## 12. Acceptance Criteria for Spec C

Spec C is considered ready for implementation when the project can take any proposed variable and produce a consistent answer to:

1. **Why does it belong in this layer?**
2. **What new information does it add?**
3. **Is its evidence/data reliable enough?**
4. **Can we operate it reliably every week?**
5. **Which forecast horizon(s) does it matter for?**
6. **Should it be admitted, research-only, or rejected?**
7. **What initial within-layer weight should it receive, and why?**

---

## 13. Guiding Principle

> **The purpose of variable admission is not to collect every potentially relevant indicator. It is to build the smallest credible set of variables that adequately represents each causal layer and supports the four forecast horizons.**

**End of Spec C — Draft for External Review**
