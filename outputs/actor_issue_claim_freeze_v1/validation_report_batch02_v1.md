# HR-035 Batch 2 validation

- PASS — 18 active E4 actor–issue facts selected.
- PASS — all 18 retain `ai_seeded` fact status and have completed human scope review.
- PASS — 5 `ai_seeded` actor identities receive one companion decision each; no identity decision is duplicated per edge.
- PASS — 19 unique edge-source IDs and 20 unique package source IDs resolved.
- PASS — AI044/AI119/AI121/AI232/AI234 carry source-level ceiling warnings; AI016 carries the single-statement continuity warning.
- PASS — all source artifacts are `archived` or `manual_archived`; rejected S051 is absent.
- PASS — all 23 human decision rows are blank.
- PASS — central tables and frontend artifacts were not modified.

This assignment does not reopen HR-019 scope decisions. Edge acceptance
does not create actor–actor, funding, alliance, causal, place or event
relations. For the five companion actors, default reviewed-graph activation
requires both an accepted/revised identity decision and an accepted/revised
edge decision.
