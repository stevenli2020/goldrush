# Gold Probability Engine — Spec D
## AI Evidence Protocol

**Status:** Draft for external review  
**Purpose:** Define how AI Agents assess qualitative or evidence-interpretive variables without turning unsupported judgment into model input.

---

## 1. Objective

AI Agents are used where a phenomenon cannot be adequately represented by a deterministic quantitative variable.

The protocol must ensure every analytical assessment is:

- evidence-backed;
- timestamped;
- explicit about uncertainty;
- separated into fact and interpretation;
- reversible/auditable;
- comparable across weekly runs.

AI output is an **input to the scoring system**, not an independent authority.

---

## 2. Required Evidence Record

Every analytical assessment must return the following fields:

| Field | Requirement |
|---|---|
| Variable ID | Exact registry identifier |
| Observation timestamp | When the assessment applies |
| Evidence | Specific supporting facts/sources |
| Assessment | Current interpretation |
| Stance | -1.0 to +1.0 |
| Confidence | 0.0 to 1.0 |
| Counter-evidence | Material evidence against the assessment |
| Fact vs interpretation | Clearly separated |
| Source provenance | Source names/links and publication dates |

No field should be omitted unless the variable's defined method explicitly does not require it.

---

## 3. Fact vs Interpretation

AI Agents must separate:

### Facts

Observable statements supported by sources.

Example:

> “The central bank announced X on [date].”

### Interpretation

Reasoned assessment derived from the facts.

Example:

> “This may increase the probability of tighter monetary policy.”

The model must never present an interpretation as though it were an observed fact.

---

## 4. Evidence Sufficiency

An analytical assessment should not be based on a single weak assertion when the variable materially affects the forecast.

Evidence should be assessed for:

- source quality;
- recency;
- relevance;
- independence;
- consistency.

When evidence is insufficient:

> **Confidence should fall.**

The system should not manufacture certainty simply because a directional stance is required.

---

## 5. Counter-Evidence

Every non-neutral analytical assessment should actively consider material evidence against the chosen stance.

### Counter-evidence should normally affect:

**confidence first**, rather than automatically reversing stance.

For example:

- strong bullish evidence + weak counter-evidence → bullish stance, high confidence;
- strong bullish evidence + strong bearish counter-evidence → bullish/neutral stance with lower confidence;
- evidence genuinely balanced → neutral stance.

A stance should flip only when the total evidence supports the opposite interpretation.

This prevents a single contradictory fact from mechanically reversing a broader assessment.

---

## 6. Analytical Stance

The standard stance scale is:

- **+1.0** = strongly bullish;
- **0.0** = neutral / insufficient directional evidence;
- **-1.0** = strongly bearish.

Intermediate values are allowed when the evidence is directional but not extreme.

The stance represents:

> **directional assessment of the variable's expected effect on gold for its defined horizon.**

It does not represent confidence.

Confidence is captured separately.

---

## 7. Confidence

Confidence is a separate value:

> **0.0 ≤ C ≤ 1.0**

Confidence should consider:

- evidence quality;
- evidence sufficiency;
- source agreement;
- recency;
- uncertainty;
- ambiguity of the mechanism.

Confidence is **not** simply “how strongly the agent feels.”

---

## 8. Conflicting Sources

When credible sources disagree:

1. record the disagreement;
2. identify the basis of the disagreement where possible;
3. do not hide conflicting evidence;
4. reduce confidence when the disagreement materially affects the assessment;
5. use the stronger evidence to determine stance where justified.

The AI Agent should not force false consensus.

---

## 9. News and Event Processing

For current events, the AI Agent should identify:

- event;
- affected country/region;
- mechanism;
- likely direction for gold;
- relevant forecast horizon;
- potential offsetting channels.

For geopolitics, the four approved channels should be considered where relevant:

1. safe-haven;
2. energy/inflation;
3. reserve security;
4. monetary fragmentation.

An event should not automatically be treated as bullish or bearish merely because it is “geopolitical.”

---

## 10. Historical Evidence in AI Assessment

Historical events may be used as contextual evidence.

The Agent may report:

- similar historical mechanisms;
- similarities;
- differences;
- historical outcomes;
- counterexamples.

It must not fabricate quantitative historical values where reliable data is unavailable.

Historical analogy must be presented as:

> **context/evidence, not proof that the current outcome will repeat.**

---

## 11. Source Hierarchy

Where available, prefer:

1. primary official sources;
2. established institutional research;
3. high-quality specialist sources;
4. reputable financial/news organizations;
5. secondary commentary;
6. low-quality aggregators/social content only when necessary and explicitly flagged.

The source hierarchy affects evidence quality and confidence.

---

## 12. AI Output Template

Each analytical variable should return a structured record similar to:

```text
Variable ID:
Observation timestamp:

FACTS:
- ...

EVIDENCE:
- Source / publication date / key fact
- Source / publication date / key fact

ASSESSMENT:
- ...

STANCE:
+0.00

CONFIDENCE:
0.00

COUNTER-EVIDENCE:
- ...

FACT / INTERPRETATION BOUNDARY:
- Facts:
- Interpretation:

RELEVANT HORIZONS:
- 1–5 days: ...
- 1–3 months: ...
- 1–3 years: ...
- 3–10 years: ...
```

---

## 13. Failure Handling

The Agent must be able to return:

> **Insufficient evidence**

rather than inventing an assessment.

Possible output:

```text
STANCE: 0.00
CONFIDENCE: 0.15
STATUS: Insufficient evidence
```

This is preferable to false precision.

---

## 14. AI Agent Restrictions

AI Agents must not:

- change layer definitions;
- create new production variables without the admission process;
- modify variable weights;
- modify layer weights;
- manufacture historical data;
- hide counter-evidence;
- convert speculation into fact.

Their role is:

> **structured evidence interpretation within an approved variable.**

---

## 15. Acceptance Criteria for Spec D

A qualitative-variable implementation is compliant when:

1. evidence is traceable;
2. facts and interpretations are separated;
3. stance and confidence are separate;
4. counter-evidence is explicitly considered;
5. timestamps are preserved;
6. inadequate evidence can result in a low-confidence/insufficient-evidence outcome;
7. the Agent cannot change model architecture or weights.

**End of Spec D — Draft for External Review**
