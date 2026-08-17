# Gold Probability Engine — Spec B
## Three-State Probability Model

**Status:** Draft for external review  
**Purpose:** Define how the system converts the Net Index into three probabilities while preserving the Net Index as the transparent directional-conviction measure.

---

## 1. Objective

The production system uses two related but distinct outputs.

### Net Index

A single score:

\[
-1.00 \le S_{total} \le +1.00
\]

where:

- **+1.00** = maximum bullish consensus;
- **0.00** = perfectly neutral / signals cancel;
- **-1.00** = maximum bearish consensus.

### Three-State Probability

The system also produces:

- \(P(B)\) = probability of Bullish outcome;
- \(P(C)\) = probability of Consolidation / Range-bound outcome;
- \(P(Be)\) = probability of Bearish outcome.

with:

\[
P(B)+P(C)+P(Be)=1
\]

The Net Index remains the primary transparent measure of directional conviction.

---

## 2. Relationship Between Net Index and Probability

The existing binary interpretation is retained as a reference:

\[
P(Higher) =
\left(
\frac{S_{total}+1}{2}
\right)
\times 100\%
\]

This is interpreted as:

> **a binary directional probability if the only possible outcomes are higher or not higher.**

It is **not** the final three-state production output.

---

## 3. Three-State Model

The production probability model must transform the Net Index and the current market-state evidence into:

\[
P(B), P(C), P(Be)
\]

The model must preserve the core directional meaning of the Net Index:

- higher Net Index → higher relative Bullish probability;
- lower Net Index → higher relative Bearish probability;
- Net Index near zero → greater potential for Consolidation.

The model therefore has two conceptual dimensions:

### Directional conviction

Represented by Net Index.

### Range/consolidation propensity

Determined separately from the current forecast state.

---

## 4. Range Propensity

### Definition

For Spec B, **Range Propensity** means:

> **the estimated likelihood that gold's realized price movement over the forecast horizon will remain within the predefined consolidation band for that horizon.**

It is distinct from Net Index.

A near-zero Net Index can arise from genuine range-bound conditions or from strong opposing forces that may produce a large move in either direction.

### Source

Range Propensity is a **deterministic composite market-state indicator**, not a free-form AI opinion in the base implementation.

The initial composite is built from approved observable variables associated with the current range/volatility regime, selected through the Phase-1 variable registry. Candidate inputs include:

- realized volatility;
- ATR or comparable range measure;
- recent directional persistence/trend strength;
- recent breakout/range behavior;
- relevant market-structure stress measures.

For each horizon \(h\), the approved inputs are standardized and combined into:

\[
R_h\in[0,1]
\]

where:

- \(R_h=0\) = low range-bound propensity;
- \(R_h=1\) = high range-bound propensity.

The exact component set and weights are determined from approved Phase-1 variables and documented before Phase 5 implementation.

AI qualitative evidence may provide context, but it does not directly override the deterministic composite.

---

## 5. Consolidation Is Not Simply “Neutral”

Consolidation should represent a forecast that the gold price is likely to remain within a defined range rather than make a meaningful directional move.

Therefore:

> **Neutral layer signals do not automatically mean high P(Consolidation).**

A market can have conflicting strong bullish/bearish forces and therefore have Net Index near zero while still being expected to be volatile.

Conversely, weak directional forces may produce genuinely range-bound conditions.

The production model must distinguish:

- **directional cancellation**
from
- **true range-bound conditions**.

---

## 6. Horizon-Specific Consolidation Definition

The consolidation state must use a threshold appropriate to the forecast horizon.

For each horizon \(h\), define a range threshold:

\[
R_h
\]

The threshold represents the magnitude of price movement considered economically meaningful over that horizon.

Illustratively:

\[
|Return_h| < R_h
\]

may constitute a consolidation outcome.

The actual values of \(R_h\) must be determined during probability-model development using the behavior and volatility characteristics of each horizon.

No single fixed percentage should be imposed across all four horizons.

---

## 7. Probability Mapping Principle

The final three-state probability should be based on:

1. **Net Index**
2. **Consolidation/range propensity**
3. **Horizon-specific characteristics**
4. **Signal strength**

Conceptually:

### Strong positive Net Index

Higher:

> P(Bullish)

Lower:

> P(Bearish)

Consolidation depends on whether the system also indicates a range-bound environment.

### Strong negative Net Index

Higher:

> P(Bearish)

Lower:

> P(Bullish)

Consolidation again depends on range propensity.

### Net Index near zero

Potential outcomes include:

- high P(Consolidation) if the market is genuinely range-bound;
- relatively balanced P(Bullish)/P(Bearish) if directional uncertainty is high.

Therefore:

> **Net Index near zero does not automatically imply P(Consolidation) = high.**

---

## 8. Illustrative Mapping

The following example is conceptual and does **not** establish final production thresholds.

Suppose:

\[
S_{total}=+0.25
\]

The binary interpretation would be:

\[
P(Higher)=62.5\%
\]

A possible three-state outcome might be:

| Horizon | P(Bullish) | P(Consolidation) | P(Bearish) |
|---|---:|---:|---:|
| 1–5 days | 55% | 30% | 15% |
| 1–3 months | 62% | 23% | 15% |
| 1–3 years | 67% | 20% | 13% |
| 3–10 years | 64% | 21% | 15% |

These are illustrative only.

The final mapping must be determined systematically.

---

## 9. Signal Strength

Signal strength describes the magnitude of directional conviction represented by the Net Index.

A starting interpretation may retain:

\[
|S_{total}| \ge 0.50
\]

as a strong directional signal,

\[
0.20 \le |S_{total}| < 0.50
\]

as a medium directional signal,

and:

\[
|S_{total}| < 0.20
\]

as a low/neutral directional signal.

These thresholds are **provisional** and may be reviewed after the probability model is implemented.

Signal strength is distinct from probability.

A market can have:

> low directional signal + high consolidation probability

or:

> low directional signal + high uncertainty between Bullish/Bearish.

---

## 10. Asymmetry by Horizon

The three-state mapping may be horizon-specific because:

- expected volatility differs;
- meaningful price ranges differ;
- consolidation durations differ;
- structural trends may dominate longer horizons.

Therefore the model may use different mapping parameters for:

- 1–5 days;
- 1–3 months;
- 1–3 years;
- 3–10 years.

However, the core interpretation of the Net Index remains the same across horizons.

---

## 11. Probability Integrity

For every weekly forecast and every horizon:

\[
0 \le P(B),P(C),P(Be) \le 1
\]

and:

\[
P(B)+P(C)+P(Be)=1
\]

The system must reject or flag invalid probability outputs.

---

## 12. Calibration Principle

The probability model should eventually be evaluated for calibration.

For example:

> Forecasts near 70% Bullish should, over a sufficiently large sample, produce Bullish outcomes at approximately the same frequency.

However, initial probability parameters may be research-derived and provisional.

The production system should retain the forecast probabilities and eventual outcomes for later calibration review.

Calibration should refine the mapping rather than redefine the Net Index itself.

---

## 13. Acceptance Criteria for Spec B

Before Phase 5 implementation, the project must have:

1. a deterministic method for calculating the three probabilities;
2. a defined horizon-specific consolidation criterion;
3. a clear relationship between Net Index and the three probabilities;
4. valid probability normalization;
5. a defined signal-strength interpretation;
6. treatment for near-zero Net Index;
7. treatment for strong positive/negative Net Index;
8. a method for later calibration.

---

## 14. Guiding Principle

> **Net Index remains the transparent measure of net directional conviction. The three-state probability model is the decision surface that translates that conviction, together with range/consolidation conditions, into Bullish / Consolidation / Bearish probabilities.**

**End of Spec B — Draft for External Review**
