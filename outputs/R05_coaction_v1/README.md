# R05 co-action network v1

Event-aware co-action package for the original Phase-1 R5 module.

## Files

- `../../data/interim/25_coaction_event_participation_v0.csv` — all 169 source-list observations across 67/31/71 events.
- `event_catalog_v0.csv` — event/action/target/source metadata and identity-layer counts.
- `actor_event_bipartite_edges_v0.csv` — 169 actor/name-to-event edges; no actor-to-actor alliance projection.
- `repeat_participation_bridges_v0.csv` — 15 confirmed current-registry actors appearing in at least two sampled events.
- `event_overlap_v0.csv` — pairwise overlap using confirmed registry identities only.
- `source_register_v0.csv` — module-local source locators, archive paths and hashes.
- `hr020_review_queue_v0.csv` / `HR020_review_packet_v0.md` — 14 unresolved segmentation/alias questions with blank decision fields.
- `fig_r05_event_bipartite_v0.png` — full event-participant bipartite view; repeated actors labelled, one-off nodes unlabelled.
- `fig_r05_repeat_bridges_v0.png` — identity composition and readable repeated-participation matrix.
- `R05_explanatory_brief_v0.md` — what R5 now answers, what it cannot answer, and the mechanism interpretation.
- `validation_report_v0.md` — generated checks and counts.

## Identity rules

- `registry_actor`: source name is accepted as a match to a current registry actor; only these rows may enter the formal repeated-participation bridge table.
- `event_only_name`: literal name observed in one source list; it is not silently promoted to the registry or merged across languages.
- `alias_pending`: possible alias, translation, entity boundary or source-name segmentation requiring HR-020. It remains event-specific until a human decision.

## Relation rule

Every edge is an event participation observation. `repeated_public_participation_*` means repeated appearance across the three sampled actions only. It does not mean stable alliance, membership, funding, hierarchy or continuing coordination.

Rebuild with:

```powershell
python scripts\make_r05_coaction_v1.py
```
