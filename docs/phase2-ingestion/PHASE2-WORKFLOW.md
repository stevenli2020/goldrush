# Phase 2 Workflow

**Purpose:** Move admitted variables from source selection to reliable, reviewable data collectors.

This workflow is self-contained. It does not require participants to understand the wider project context beyond the variable currently assigned.

**Operational tracker:** Grace must update [SOURCE-IMPLEMENTATION-TRACKER.md](SOURCE-IMPLEMENTATION-TRACKER.md) whenever a variable task closes, recording the final source, fallback, collection method, reuse decision, collector, review outcome, and `Complete` or `Deferred` decision.

## Roles

- **Implementation owner:** Proposes the source, fallback, collection method, and collector changes.
- **Grace:** Opens tasks, acts as quality gatekeeper, reviews against the acceptance criteria, and requests adjustments.
- **Final approver:** Approves Grace’s recommendation to mark the variable `Complete` or `Deferred`.

Additional Grace members may work in parallel, provided each variable has one owner and one tracker record.

## Variable loop

1. Grace selects the next admitted variable from the tracker.
2. Grace checks whether an existing source adapter, collector, or transformation can be reused before a new implementation is proposed.
3. The implementation owner proposes:
   - primary source;
   - fallback source;
   - programmatic collection method;
   - collector module location;
   - expected fields, units, and timestamps.
4. Grace reviews the proposal and requests specific changes where necessary.
5. The implementation owner reworks the collector and returns it for review.
6. Grace validates the result and recommends `Complete` or `Deferred`.
7. The final approver accepts the recommendation.
8. Grace updates `SOURCE-IMPLEMENTATION-TRACKER.md` with the completed review record and final status.
9. The next variable begins.

## Reuse-first rule

Before creating a new collector, Grace must check the tracker and existing implementation for:

- the same source or provider;
- a reusable API, file format, authentication method, or retrieval pattern;
- another series that can use the same source adapter;
- shared timestamp, validation, fallback, or error-handling logic;
- differences that require separate transformation logic.

The default is to reuse or extend an existing source adapter. Create a new collector only when the source, retrieval method, schema, or maintenance requirements are materially different. Record the reuse decision in the tracker.

## Acceptance criteria

A variable may be recommended `Complete` only when:

- the primary source is identified and accessible;
- fallback behavior is documented;
- collection runs programmatically and reproducibly;
- fields, units, timestamps, and publication timing are clear;
- freshness and missing-data behavior are defined;
- raw observations are preserved;
- basic validation passes;
- the collection method is briefly documented.

## Deferral criteria

Recommend `Deferred` when the variable has an unresolved blocker, such as:

- no reliable or accessible source;
- no workable fallback;
- unstable or restricted access;
- unresolved methodology or unit definition;
- insufficient historical coverage;
- a collector that cannot be made reproducible.

Every deferral must state the blocker and the condition required to reopen the task.

## Tracker statuses

`Not done` → `Complete` or `Deferred`

## Tracker fields

| Field | Required content |
|---|---|
| Variable ID | Stable registry ID |
| Variable name | Registry name |
| Owner | Implementation owner |
| Primary source | Named source and endpoint |
| Fallback source | Named fallback or `None identified` |
| Collection method | API, file download, feed, or documented extraction |
| Collector | Module or function location |
| Status | Current workflow status |
| Review notes | Grace’s findings and requested changes |
| Reuse check | Existing adapter reused, extended, or reason a new collector is required |
| Final decision | Approval, completion date, or deferral reason |

## Operating rules

- Work on one variable per task.
- Keep implementation notes short and practical.
- Do not silently change source, schema, units, or transformation rules.
- Do not promote deferred variables into production collection.
- Do not allow parallel work to overwrite another owner’s tracker record.
- Resolve disagreements through the review loop before final approval.
- A variable task is not closed until Grace has updated `SOURCE-IMPLEMENTATION-TRACKER.md`.
