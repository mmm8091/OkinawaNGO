# HR-035 Batch 2 validation

Packet-level state: **principal confirmation complete**. This report validates the filled review packet
before central mutation; the later controlled merge is validated separately in
`outputs/hr035_batch02_integration_v1/validation_report_v1.md`.

- PASS — 18 actor–issue rows and 5 identity-companion rows remain present.
- PASS — all 23 rows contain an explicit AI-assisted proposed decision.
- PASS — reviewer is `project_principal_user` on all 23 rows.
- PASS — `review_date=2026-07-20` on all 23 rows.
- PASS — identity decisions: 1 `accept_identity`, 4 `revise_identity`.
- PASS — edge decisions: 7 `accept`, 9 `revise`, 2 `defer_second_source`.
- PASS — every `supported_bounded` edge has `confirmed_scope`, `missing_scope` and `interpretation_limit`.
- PASS — AI119/AI121/AI232/AI234 are reduced to their E3 direct-source ceiling.
- PASS — AI044 replaces the mismatched S024 edge citation with direct A018 source S023.
- PASS — AI016 and AI233 explicitly set `scope_revision_required=yes`; no HR-019 scope change is silent.
- PASS — 20 unique package source IDs resolve to existing local artifacts; rejected S051 is absent.
- PASS — the principal-confirmation step itself did not modify central tables or frontend artifacts.

Principal confirmation is complete. A Batch-2-specific merger subsequently updated the central actor
and actor–issue tables and regenerated downstream artifacts. Edge acceptance does not create
actor–actor, funding, alliance, causal, place or event relations. For the five companion actors,
default reviewed-graph activation requires both an accepted/revised identity decision and an
accepted/revised edge decision.
