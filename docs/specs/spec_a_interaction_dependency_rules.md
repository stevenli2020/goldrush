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

## 10. What Spec A Does Not Decide

Spec A does not determine:

- final variable weights;
- final layer weights;
- empirical coefficient values;
- weekly manual adjustments;
- the statistical method used to estimate future coefficients.

Those are handled through the research-derived weighting process and later controlled refinement.

---

## 11. Acceptance Criteria for Spec A

Before scoring-engine implementation, the project must be able to:

1. identify a candidate duplication/transmission/interaction relationship;
2. classify it consistently;
3. explain why;
4. apply a documented effective-weight treatment;
5. add explicit interaction terms only where justified;
6. demonstrate that no information is being counted twice merely because it appears in multiple variables.

**End of Spec A — Draft for External Review**
