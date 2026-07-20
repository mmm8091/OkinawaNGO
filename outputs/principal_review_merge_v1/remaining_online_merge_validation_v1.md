# Remaining-online human-review merge validation v1

Date: 2026-07-20

Status: **PASS**

Validated boundaries:

- 145 dependency-ordered online decisions are principal-confirmed.
- HR-035 batch 01 has 15 principal-confirmed fact decisions.
- Central actor registry has 122 history rows; the current actor layer has 121 active actors.
- Central actor–issue history has 294 rows; the rebuilt active layer has 283 edges (125 human-reviewed / 158 candidate), 116 connected actors and 5 isolated actors.
- HR-010 materialized 46 accepted rows as AI249–AI294; one deferred item was not materialized.
- HR-034 status semantics, four lifecycle decisions, HR-029 schema/alias freeze and HR-031 option-B interpretations are applied.
- The upstream and freeze stages were each rerun with byte-stable central outputs, confirming idempotent reconstruction.
- This validation does not approve alliances, funding, causality, continuity beyond the four reviewed lifecycle cases, or the 12 local/new-primary-material items.

Errors: none.
