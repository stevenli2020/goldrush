# L6-002 Step 5 — Deterministic scoring specification

Status: proposed specification; scoring is not implemented.

This specification applies only after the Phase 2 XML event has passed candidate triage and Phase 3 has retrieved a usable official primary document containing an exact official name from the XML (`target_name` or an official alias). The four narrative-only bootstrap files are not inputs to this score.

## Output

For a scorable `ADD` or `UPDATE`, emit an integer `score` from 0 to 100 and the four component values. For a `REMOVE`, emit `action_state: REVERSED`, `score: null`, and `reversal_flag: true`; a removal is not evidence of a current intervention. If the primary document is unavailable, the exact name is absent, or a required fact is ambiguous, emit no score and `evidence_state: INSUFFICIENT_EVIDENCE` with an explicit gap.

The score measures evidence that the official action is a sovereign-asset freeze intervention. It does not measure geopolitical importance, market impact, probability, or gold direction.

## Component rules

The rules are applied to the retrieved official document text after whitespace normalization. Matching is case-insensitive and phrase-based. Country names, linked-to text, XML `sanctions_type`, and legal-authority fields cannot by themselves earn points.

### 1. Legal action — maximum 40

Score 40 only when the primary document, in the action text for the matched official entity, contains:

`blocked` or `freeze` or `frozen`

and the same action text identifies the entity or its property/interests in property as subject to that action. The exact phrase `all property and interests in property ... are blocked` qualifies.

Score 0 when the document only says `designated`, `listed`, `added`, `amended`, `updated`, `sanctioned`, or similar without an explicit block/freeze statement tied to the matched entity. No partial points are awarded.

### 2. Sovereign relevance — maximum 30

Score 30 only when the primary document explicitly identifies the matched entity with one of these source-backed institutional descriptions:

`central bank`, `reserve bank`, `monetary authority`, `national treasury`, or `sovereign wealth fund`.

The description must occur in the same entity entry or sentence as the matched official name. A `Linked To:` reference, a country-only reference, or a generic `bank` description does not qualify. No partial points are awarded.

### 3. Asset scope — maximum 20

Score 20 when the primary document explicitly states that `all property` or `all interests in property` of the matched entity are blocked or frozen.

Score 10 when the document explicitly identifies blocked or frozen property/interests in property but limits the scope to specified accounts, assets, transactions, or other defined property.

Score 0 when asset scope is absent, merely implied by a designation, or concerns only a transaction prohibition without blocked/frozen property or interests in property. No points are awarded from silence.

### 4. Legal-authority character — maximum 10

Score 10 when the primary document explicitly cites a United Nations Security Council resolution as the legal authority for the action.

Score 0 for a standalone U.S. Executive Order, statute, regulation, agency designation, or when the authority is absent or ambiguous. This component is binary; it does not assess the importance of the authority.

## Evidence-state rules

`SCORABLE` requires all of the following:

- the event is `ADD` or `UPDATE`;
- the retrieved document is an official OFAC or Federal Register document;
- the document contains an exact official XML name;
- the legal action, institutional relevance, and asset-scope tests have determinate results;
- the source URL, matched name, evidence excerpt, and rule results are retained.

Otherwise emit `INSUFFICIENT_EVIDENCE`, no score, and one or more gaps such as `primary_document_missing`, `exact_name_not_found`, `legal_action_ambiguous`, `sovereign_relevance_not_explicit`, or `asset_scope_not_explicit`.

## Syria calibration example

The retrieved 30 June 2025 notice explicitly mentions the `Central Bank of Syria`, supporting institutional relevance. The corresponding XML event is `REMOVE`, and the notice describes removal from the SDN List. Under this specification it produces `REVERSED` with no current intervention score; it does not receive legal-action or asset-scope points. This is intentional and demonstrates that entity relevance is not equivalent to a freeze.

## Non-rules

The scorer must not use an LLM, human stance input, translation table, fuzzy matching, country-risk prior, silence-as-durability assumption, or inferred reserve ownership. No score is created from the XML candidate flag alone. This specification does not define downstream Phase 4 transformations.
