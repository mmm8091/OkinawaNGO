# Schema / alias freeze validation v1

Generated: 2026-07-20

- Actor registry: 122 actors; 366 actor-field cells covered exactly as dynamic N×3.
- Aliases: 39 rows; zero normalized cross-actor collisions; one documented same-actor punctuation collision.
- Places: 21 nodes and 135 actor–place edges; zero cross-key mismatches after HR-025 fixed AP123 to P007 Camp Foster and approved P021 for explicit Sakishima-wide evidence.
- Venues: 16 taxonomy rows; 18 orphan `R10_VENUE` references captured; 13 require HR-029.
- Relation types: 29 values over 78 rows; full mapping coverage.
- Action types: 14 values over 255 rows; full mapping coverage.
- Unified candidates: 505 unique rows; every row has a proposed value and explicit interpretation boundary.
- HR-029: 41 stable rows; 0 currently contain human/final/status values; cross-linked one-to-one.
- Stable ID mapping: the `(domain, object_id, field_name)` review item retains its prior `review_item_id`; new items allocate unused suffixes.
- HR preservation: 0 populated rows restored from the pre-existing file; 0 extra human columns retained.
- Temporary-copy sentinel test (`TEST_HUMAN_DECISION` plus final/status fields): passed; real HR table was not modified by the test.
- Workflow guard: HR-027/019/024/025/032 decisions are merged before this regeneration; all post-merge actors appear in N×3 audit cells.
- Synthetic post-HR027 actor coverage test: passed; the added actor receives actor_class, legal_status_guess and origin_type audit rows.
- No automatic entity-merge disposition exists; predecessor, case-round and national/local brand boundaries are explicit.
- Two figures generated in PNG/SVG; SVG line-tail whitespace normalized after save; deterministic non-figure digest: `99a0661b112895a7`.
