# GoldRush — Claude Agent Handoff
**Generated:** 2026-08-17
**Last updated:** 2026-08-17 — Phase 1 frozen; Phase 2 data ingestion initiated
**Prepared by:** Chris (Pragmatic Project Advisor)
**Project root:** /mnt/d/Projects/GoldRush
**Connector:** GR

---

## 1. STATUS

### Completed Milestones
- **Pre-Phase-1 architectural review** — Project proposal (`docs/gold_probability_engine_project_proposal.md`) reviewed and approved with documented gaps
- **Causal model locked** — 12-layer causal architecture finalized in `docs/gold_price_causal_model_v2_2.md`; layers are frozen
- **All four specs reviewed and approved (v2):**
  - Spec A v2 — Interaction & Dependency Rules ✓
  - Spec B v2 — Three-State Probability Model ✓
  - Spec C v2 — Variable Admission Criteria ✓
  - Spec D v2 — AI Evidence Protocol ✓
- **Phase 1 formally unblocked** — all pre-Phase-1 blockers resolved
- **Phase 1 T1 signed off** — Layers 0, 1, 3; 18 ADMIT, 6 CONDITIONAL, 0 REJECT
- **Phase 1 T2 signed off** — Layers 4, 5; 12 ADMIT, 4 CONDITIONAL, 0 REJECT
- **Phase 1 T3 signed off** — Layers 2, 7; 7 ADMIT, 4 CONDITIONAL, 0 REJECT
- **Phase 1 T4 signed off** — Layers 6, 9; 4 ADMIT, 6 CONDITIONAL, 0 REJECT

### Current State
- Phase 1 is **COMPLETE and FROZEN** — all five tranches closed; 74 records, 44 admitted, 30 conditional, 0 rejected
- Phase 2 is **INITIATED** — source-lock inventory and ingestion contract at `docs/phase2-data-ingestion-plan.md`
- T5 scope: Layers 8, 10, 11 — closed at `docs/phase1-registry/T5-registry.md`
- No code written yet; `mcp_server.py` exists at project root (purpose not reviewed)
- All authoritative specs are in `docs/specs/v2/`; v1 specs are superseded

---

## 2. SSOT

### Immutable Architecture
- **12 causal layers are locked.** Layers 0–11 defined in `gold_price_causal_model_v2_2.md`. No new layers. No renaming.
- **Four forecast horizons are fixed:** 1–5 days / 1–3 months / 1–3 years / 3–10 years
- **Three output states only:** Bullish / Consolidation / Bearish; P(B)+P(C)+P(Be)=1
- **Net Index scale is fixed:** −1.00 (max bearish) → 0.00 (neutral) → +1.00 (max bullish)
- **Binary reference formula retained but NOT the production output:** P(Higher) = (S_total + 1) / 2
- **Variable admission does NOT change layer-level weights.** Only within-layer variable weights redistribute on admission.
- **Layer-level weights are horizon-specific:** W_{k,h} per layer per horizon; sum to 1.0 per horizon.

### Core Scoring Formula
```
Base contribution:     B_i = w_i · S_i · C_i
Effective contribution: E_i = w_i · D_i · T_i · S_i · C_i
  D_i = duplication factor (0 < D_i ≤ 1; default 1.0 if not applicable)
  T_i = transmission factor (0 < T_i ≤ 1; default 1.0 if not applicable)

Interaction term (only where approved):
  I_ij = γ_ij · S_i · S_j · C_i · C_j

Layer score:
  L_k = Σ(E_i) / Σ(w_i · D_i · T_i)   bounded [-1, +1]

System score per horizon:
  S_total,h = Σ W_{k,h} · L_{k,h}       bounded [-1, +1]
```

### Three-State Output
- Inputs: Net Index (S_total) + Range Propensity (R_h)
- Range Propensity = **deterministic composite** from observable market-state variables (realized volatility, ATR, directional persistence, breakout behavior, market-structure stress); R_h ∈ [0,1]
- AI context may inform but **cannot override** the deterministic composite
- P(Consolidation) ≠ neutral Net Index — directional cancellation ≠ range-bound conditions
- Exact functional form for mapping (S_total, R_h) → (P(B), P(C), P(Be)): **deferred to Phase 5 pre-condition**

### AI Evidence Protocol (Spec D v2)
- Every analytical variable requires 9 fields: Variable ID, Observation timestamp, Evidence, Assessment, Stance, Confidence, Counter-evidence, Fact/Interpretation boundary, Source provenance
- **Confidence is computed by rubric** (not free-form):
  - Five factors scored 0–2: Evidence quality, Evidence sufficiency, Source agreement, Recency, Mechanism clarity
  - R = sum of scores (0–10); C_base = R/10
  - Counter-evidence penalty: C = C_base × (1 − 0.20 × E_counter/2), where E_counter ∈ {0,1,2}
  - Insufficient evidence override: STANCE=0.00, CONFIDENCE≤0.20, STATUS=Insufficient evidence
- **AI Agents must not:** change layer definitions, create production variables without admission process, modify any weights, manufacture historical data, hide counter-evidence

### Variable Admission Gate (Spec C v2)
All five criteria must pass:
- **A** — Causal Relevance: credible mechanism documented
- **B** — Incremental Information: adds what existing set does not already capture; Phase 1 master registry is now the frozen SSOT baseline
- **C** — Data/Evidence Reliability: source quality, revision behavior, historical coverage
- **D** — Operational Feasibility: weekly retrieval, cost, maintenance burden
- **E** — Forecast-Horizon Relevance: relevant to at least one of the four fixed horizons

Decisions: ADMIT / CONDITIONAL (Research Only) / REJECT

### Interaction Classification Rules (Spec A v2)
- **Case A — Duplicate:** apply D_i < 1; sum of effective weights ≤ information content deserved
- **Case B — Transmission:** apply T_i reflecting non-overlapping contribution only; downstream ≠ automatically lower
- **Case C — Genuine Interaction:** add explicit I_ij term; must be documented; never introduced from correlation alone
- Triggers for dependency review: provenance overlap / mechanism overlap / strong observed relationship / explicit causal relationship / joint-response hypothesis
- No weekly discretionary adjustments outside this framework
- **Phase 1 rule:** qualitative flags only (Duplicate / Transmission / Interaction candidate); no numerical D_i/T_i values assigned until Spec A implementation

### Weight Governance Principles
- Initial weights = **research-derived**, not backtested
- Weight changes require **separate research evidence and review** — not triggered by single forecast errors
- Weight Refinement Proposals require: layer, horizon, current weight, proposed weight, reason, evidence strength, status
- Random Forest = optional diagnostic only, after sufficient reliable data exists; never determines weights or final probabilities

### Data Integrity Rules
- Every observation preserves: observation date / publication date / retrieval date / source / revision status
- System must distinguish **what happened** from **when information became knowable**
- No historical data fabrication or reconstruction from AI judgment

---

## 3. NEXT STEPS

### Phase 1 — Variable Registry (COMPLETE — SSOT frozen)

| Tranche | Layers | Status |
|---|---|---|
| T1 | 0, 1, 3 | **CLOSED — signed off 2026-08-17** |
| T2 | 4, 5 | **CLOSED — signed off 2026-08-17** |
| T3 | 2, 7 | **CLOSED — signed off 2026-08-17** |
| T4 | 6, 9 | **CLOSED — signed off 2026-08-17** |
| T5 | 8, 10, 11 | **CLOSED — signed off 2026-08-17** |

### Phase 2 Immediate Task

Begin source locking and raw-observation storage for the 44 ADMIT variables using `docs/phase2-data-ingestion-plan.md`. T5 closes Phase 1.

**T5 key risks to brief Grace on:**
- L8/L0 boundary: ETF flow (L8) vs. ETF holdings stock (L0-003) — distinct mechanisms, both admissible if separated
- L10 amplifier classification: every L10 variable must state whether it is admitted as amplifier, leading signal, or market-stress indicator
- L0-009 Gold Lease Rates already admitted in Layer 0 — do not re-admit in Layer 10 without a distinct documented mechanism
- L11 Criterion C scrutiny: sentiment and search-trend variables require candid data-quality assessment; do not admit on conceptual appeal alone
- L11 is not a catch-all: the mechanism must be reflexivity and sentiment feedback specifically
- T5 closes Phase 1 — cross-layer overlap notes will be the primary Spec A dependency-review input

### Open Items Carried Forward — T1

| ID | Item | Required Before |
|---|---|---|
| L0-009 | Stable, verified data source must be confirmed | Phase 2 |
| L1-004 | Must demonstrate incremental information beyond slope of L1-001 minus L1-002 | Production admission |
| L1-006 | Monitor: if used as forward-path repricing signal, reclassify to L3 | Scoring engine implementation |
| L3-001/002 | Designate primary Layer 3 quantitative anchor | Spec A implementation |
| L3-008 | Production source must preserve point-in-time consensus vintage | Production admission |

### Open Items Carried Forward — T2

| ID | Item | Required Before |
|---|---|---|
| L4-005 | Survey methodology and source consistency must be established | Production admission |
| L4-010 | Incremental information vs. L1-005 Term Premium must be demonstrated | Production admission |
| L5-004 | Structured, retrievable source and Spec D compliance must be demonstrated | Production admission |
| L5-005 | Coverage improvement required before production admission | Production admission |

### Open Items Carried Forward — T3

| ID | Item | Required Before |
|---|---|---|
| L2-001/L2-002 | Designate primary L2 dollar anchor or establish dependency treatment to prevent double-weighting | Spec A implementation |
| L7-002 | Validate multi-country aggregation methodology, country set, currency conversion, weighting, and missing-data treatment | Phase 2 |
| L7-005 | Pre-specify stress-transformation rule and validate against known funding-stress episodes | Phase 2 |
| L7-006 | Validate composite formula including sign convention, timing alignment, and reserve-demand regime controls | Phase 2 |

### Open Items Carried Forward — T4

| ID | Item | Required Before |
|---|---|---|
| L6-003 | Establish a reproducible geopolitical-causality classification and explicitly separate the signal from T2 inflation and L3 policy repricing | Production admission |
| L6-004 | Establish a repeatable evidence and scoring procedure for forward-looking sovereign-asset access risk | Production admission |
| L6-005 | Define observable fragmentation milestones and an auditable Spec D evidence rubric | Production admission |
| L9-002 | Define a documented composite separating imports, exchange delivery, retail demand, and investment flows | Production admission |
| L9-003 | Lock a stable, reproducible India local-premium series and adjustment methodology | Production admission |
| L9-005 | Establish a stable aggregate series and separate recycling from collateral-finance activity | Production admission |

### Deferred Items (not Phase 1 blockers)

| Item | Required Before | Detail |
|---|---|---|
| Spec B: Range Propensity component set and weights | Phase 5 | Candidate inputs listed; exact set confirmed from Phase-1 approved variables |
| Spec B: Probability mapping functional form | Phase 5 | Simple bounded function preferred; no lookup tables; no over-engineering |

### Pending Decisions (must resolve before Phase 5)
- What specific observable variables constitute the Range Propensity composite?
- What is the chosen functional form for (Net Index, R_h) → (P(B), P(C), P(Be))?

### Cosmetic Fixes Outstanding (low priority)
- Spec A v2: duplicate Section 10 numbering (second "Section 10" should be Section 11)
- Spec B v2: duplicate Section 5 numbering (second "Section 5" should be Section 6)

---

## 4. LESSONS

### What Failed → What Fixed It
- **Gap: Section 10 interaction rules deferred entirely** → Fixed: Spec A v2 added numerical worked example
- **Gap: Binary probability formula insufficient for three states** → Fixed: Net Index preserved as directional-conviction measure; three-state mapping made a separate output
- **Gap: "Meaningful information" for variable admission was undefined** → Fixed: Spec C v2 Criterion B defines Phase-1 baseline explicitly
- **Gap: AI confidence was free-form** → Fixed: Spec D v2 five-factor rubric with 0–2 scoring
- **Spec C v1 had no Phase-1 baseline** → Fixed in v2
- **Spec A and Spec B v2 have duplicate section numbers** → Not yet fixed; cosmetic only

### Critical Pitfalls to Avoid
- **Do not treat the 12 layers as independent predictors.** A single macro shock propagates through multiple layers. Double-counting is the primary modeling risk.
- **Do not infer Consolidation from neutral Net Index.** Directional cancellation ≠ range-bound market. Requires separate Range Propensity signal.
- **Do not add variables because they correlate with gold or are easy to retrieve.** All five Spec C criteria must pass.
- **Do not let AI agents invent confidence values.** The five-factor rubric is mandatory.
- **Do not change layer-level weights on variable admission.** Only within-layer variable weights redistribute.
- **Do not fabricate historical quantitative data.**
- **Do not introduce interaction terms (γ_ij) from correlation alone.**
- **Do not use Random Forest as the core engine.**
- **Do not reject a variable solely because it is downstream or correlated with another variable.** Reject only on Spec C criterion failure.
- **Do not collapse Layer 1 and Layer 3.** Shared observables ≠ same mechanism.
- **Do not assign numerical D_i/T_i values in Phase 1.** Qualitative flags only.
- **Do not treat geopolitical risk as a single variable.** Attribute to one of the four approved channels.
- **Do not automatically label geopolitical developments as bullish for gold.** Offsetting channels must be acknowledged.
- **Do not re-admit L2-003 USD/CNY in Layer 9.** Already admitted in Layer 2; Layer 9 uses its own regional observables.
- **Do not re-admit L0-009 Gold Lease Rates in Layer 10 without a distinct documented mechanism.**
- **Do not treat Layer 11 as a catch-all.** Mechanism must be reflexivity and sentiment feedback specifically.

### Key Design Principles (Grace's)
1. Keep 12-layer causal architecture stable
2. Allow variables within layers to expand as evidence justifies
3. Use quantitative data as backbone; AI for genuinely interpretive evidence only
4. Treat historical events as evidence and context, not automatic weight optimizers
5. Use research-derived weights initially
6. Refine weights through controlled feedback, not weekly self-modification
7. Prevent double-counting through explicit dependency and interaction rules
8. Preserve point-in-time data integrity
9. Keep Random Forest as optional diagnostic only
10. Keep project focused on four weekly gold-probability outputs

---

## 5. ARTIFACTS

### File Tree
```
docs/
  gold_price_causal_model_v2_2.md              ← Authoritative 12-layer causal model
  gold_price_causal_model_v2_2_zh.md           ← Chinese translation (informational)
  gold_probability_engine_project_proposal.md  ← Original proposal (approved, reviewed)
  specs/
    v1/                                        ← SUPERSEDED — do not use
    v2/                                        ← AUTHORITATIVE — use these only
      spec_a_interaction_dependency_rules_v2.md
      spec_b_three_state_probability_model_v2.md
      spec_c_variable_admission_criteria_v2.md
      spec_d_ai_evidence_protocol_v2.md
  phase1-registry/
    T1-registry.md                             ← CLOSED — signed off (L0, L1, L3)
    T2-registry.md                             ← CLOSED — signed off (L4, L5)
    T3-registry.md                             ← CLOSED — signed off (L2, L7)
    T4-registry.md                             ← CLOSED — signed off (L6, L9)
mcp_server.py                                  ← Exists; purpose not reviewed
handoff/
  Claude-Handoff.md                            ← This file
  T1-Grace-Brief.md                            ← Reference only; T1 closed
  T3-Grace-Brief.md                            ← Reference only; T3 closed
  T4-Grace-Brief.md                            ← Reference only; T4 closed
  T5-Grace-Brief.md                            ← Reference only; T5 closed
  phase2-data-ingestion-plan.md                ← Phase 2 source-lock inventory and ingestion contract
```

### Phase 1 Registry — Running Totals (signed-off tranches only)

| Tranche | Layers | ADMIT | CONDITIONAL | REJECT |
|---|---|---:|---:|---:|
| T1 | 0, 1, 3 | 18 | 6 | 0 |
| T2 | 4, 5 | 12 | 4 | 0 |
| T3 | 2, 7 | 7 | 4 | 0 |
| T4 | 6, 9 | 4 | 6 | 0 |
| **Signed-off total** | | **41** | **20** | **0** |

T5 (Layers 8, 10, 11) closed: 3 ADMIT, 10 CONDITIONAL, 0 REJECT.

### Authoritative Spec Locations
- `docs/specs/v2/spec_a_interaction_dependency_rules_v2.md`
- `docs/specs/v2/spec_b_three_state_probability_model_v2.md`
- `docs/specs/v2/spec_c_variable_admission_criteria_v2.md`
- `docs/specs/v2/spec_d_ai_evidence_protocol_v2.md`

### AI Evidence Output Template (Phase 3)
```
Variable ID:
Observation timestamp:
FACTS:
EVIDENCE:
ASSESSMENT:
STANCE: +0.00
CONFIDENCE: 0.00
COUNTER-EVIDENCE:
COUNTER-EVIDENCE SCORE: [0 / 1 / 2]
CONFIDENCE RUBRIC:
- Evidence quality:     [0/1/2]
- Evidence sufficiency: [0/1/2]
- Source agreement:     [0/1/2]
- Recency:              [0/1/2]
- Mechanism clarity:    [0/1/2]
BASE CONFIDENCE: (sum)/10
COUNTER-EVIDENCE ADJUSTMENT: C_base × (1 - 0.20 × E_counter/2)
FINAL CONFIDENCE: 0.00
FACT / INTERPRETATION BOUNDARY:
RELEVANT HORIZONS:
- 1–5 days:
- 1–3 months:
- 1–3 years:
- 3–10 years:
```

### Weekly Report Core Table
| Horizon | Net Index | P(Bullish) | P(Consolidation) | P(Bearish) | Signal Strength | Primary Layer Drivers |
|---|---:|---:|---:|---:|---|---|
| 1–5 Days | ... | ...% | ...% | ...% | ... | ... |
| 1–3 Months | ... | ...% | ...% | ...% | ... | ... |
| 1–3 Years | ... | ...% | ...% | ...% | ... | ... |
| 3–10 Years | ... | ...% | ...% | ...% | ... | ... |

### Signal Strength Thresholds
| Range | Strength |
|---|---|
| \|S_total\| ≥ 0.50 | Strong |
| 0.20 ≤ \|S_total\| < 0.50 | Medium |
| \|S_total\| < 0.20 | Low / Neutral |

### Confidence Bands (Spec D v2)
| Confidence | Band |
|---:|---|
| 0.00–0.29 | Low |
| 0.30–0.59 | Moderate |
| 0.60–0.79 | Strong |
| 0.80–1.00 | Very Strong |

### Implementation Phases
| Phase | Deliverable | Status |
|---|---|---|
| 1 | Variable Registry | **COMPLETE — Phase 1 SSOT frozen** |
| 2 | Data Ingestion | **IN PROGRESS — source-lock inventory initiated** |
| 3 | AI Evidence Processing | Not started |
| 4 | Scoring Engine | Not started |
| 5 | Probability Engine | Not started |
| 6 | Weekly Production Engine | Not started |
| 7 | Feedback Review | Not started |
