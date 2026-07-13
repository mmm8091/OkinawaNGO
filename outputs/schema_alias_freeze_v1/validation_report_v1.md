# Schema / alias freeze validation v1

Generated: 2026-07-13

- Actor registry: 118 actors; 354 actor-field cells covered exactly as dynamic N×3.
- Aliases: 23 rows; zero normalized cross-actor collisions; one documented same-actor punctuation collision.
- Places: 20 nodes and 129 actor–place edges; AP123 captured as `defer_to_HR025` / needs-human, with no HR-029 duplicate and no silent P007 proposal.
- Venues: 16 taxonomy rows; 9 orphan `R10_VENUE` references captured; six require HR-029.
- Relation types: 28 values over 78 rows; full mapping coverage.
- Action types: 14 values over 255 rows; full mapping coverage.
- Unified candidates: 467 unique rows; every row has a proposed value and explicit interpretation boundary.
- HR-029: 34 stable rows; 0 currently contain human/final/status values; cross-linked one-to-one.
- Stable ID mapping: the `(domain, object_id, field_name)` review item retains its prior `review_item_id`; new items allocate unused suffixes.
- HR preservation: 0 populated rows restored from the pre-existing file; 0 extra human columns retained.
- Temporary-copy sentinel test (`TEST_HUMAN_DECISION` plus final/status fields): passed; real HR table was not modified by the test.
- Workflow guard: HR-027 merge precedes schema regeneration; all post-merge actors must appear in N×3 audit cells.
- Synthetic post-HR027 actor coverage test: passed; the added actor receives actor_class, legal_status_guess and origin_type audit rows.
- No automatic entity-merge disposition exists; predecessor, case-round and national/local brand boundaries are explicit.
- Two figures generated in PNG/SVG; SVG line-tail whitespace normalized after save; deterministic non-figure digest: `66cba89acebf20ec`.
