# L6-002 source-available bootstrap fixtures

This one-time integration fixture set preserves five XML deltas fetched from the official OFAC delta archive with the production collector. It tests the production XML path only; it does not create an HTML-history parser and contains no scoring output.

| Delta date | Why included | Parser result |
| --- | --- | --- |
| 2025-06-30 | Direct `CENTRAL BANK OF SYRIA` removal | Candidate: yes; aliases preserved |
| 2026-04-24 | Official action page updates Bank Markazi | No named central-bank entity in delta |
| 2025-11-04 | Official action page links DPRK bankers to central bank | No named central-bank entity in delta |
| 2024-03-26 | Official action page links designees to Central Bank of Syria | No named central-bank entity in delta |
| 2024-02-14 | Official action page concerns a network supporting Central Bank of Iran | No named central-bank entity in delta |

The latter four are retained as source-coverage boundary cases. They must not be counted as candidate-gate false negatives: their central-bank references occur in the action narrative, not in the corresponding XML entity names. The direct Syria event retrieved its dated official OFAC document using exact primary-name matching. It is a `REMOVE`, not a scored intervention.
