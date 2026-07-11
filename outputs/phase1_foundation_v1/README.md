# Phase-1 foundation seed package v0

Date: 2026-07-12

## Purpose

This package fills three missing Phase-1 foundation structures with runnable seed data derived only from existing repository tables and already archived sources. It does not modify or supersede the main tables under `data/interim/`.

## Files

- `evidence_notes_seed_v0.csv`: 49 short evidence-note seeds covering core report mechanisms, current specified-figure inputs, coaction events, legal roles, and sensitive funding/support claims.
- `venue_taxonomy_v0.csv`: 16 controlled venue categories for R7/R8/R9/R10/R11 expansion.
- `actor_event_venue_seed_v0.csv`: 64 rows: all 54 existing actor-event rows, 6 additional lawsuit-role rows, and 4 pathway-only actor rows.

## Seed and review status

Every newly created record is marked `ai_seeded`. Upstream rows may already be `verified`, `human_checked`, or `human_revised`, but that status is not copied into these new mappings: the evidence-note wording, source locator, venue, target, and pathway-stage choices still require human review.

Evidence summaries are short paraphrases, not long quotations. Evidence levels are inherited conservatively from the existing edge/source/role record; they are not an independent re-evaluation.

## R7 use

`actor_event_venue_seed_v0.csv` separates:

- action/event,
- venue,
- target,
- actor/counterpart role,
- pathway stage,
- and interpretation limit.

The 9 nonblank event IDs are foreign keys to `outputs/module_completion_v0/actor_relation_events_v1.csv`. The 4 `pathway_seed` rows intentionally have blank `event_id`: they represent analytical nodes from the existing Henoko/Oura Bay pathway, not newly observed events. Translation-frame nodes such as dugong/biodiversity, EIA/legal procedure, and autonomy are not actors and are therefore not forced into this actor-event table; a later frame-event table should model them.

## Current venue/target coverage

Mapped current venues include public statements, the U.S. Marine Mammal Commission, U.S. federal litigation, prefectural/municipal referenda, a public-opinion advertisement, and the Henoko on-site/pathway layer. Taxonomy-only categories are included for Japanese courts, administration, environmental procedure, UN mechanisms, policy forums, and service/charity sites so later R7 expansion can use stable IDs.

## Source-locator gaps

The following remain seed-level and must be resolved before final publication:

1. Many archived HTML sources have only file-level plus section-description locators because the pages lack stable paragraph anchors.
2. `S093` is a scanned court PDF; the exact caption page must be manually pinpointed and checked against the docket/case materials.
3. `S099` contains multiple FY2024 project statements; exact printed/PDF page numbers for F031–F033 must be manually recorded.
4. `S056` needs exact PDF pages for eligibility and award-range fields.
5. `S032` currently has a homepage-level locator and is insufficient as a final note for a specific legal/autonomy claim.
6. Negative legal-role claims for A002/A019 rely on caption comparison and must receive human legal review.
7. Yonaguni A014/A015 organization identity and continuity still require local/primary confirmation; these seeds support event context only.
8. No current event rows yet cover Japanese noise/environmental courts, EIA/administrative procedure, UN mechanisms, or a comparable second international pathway.

## Interpretation limits

- Co-signing, joint statements, requests, and shared event participation are event-level observations, not stable alliances.
- A named court party, legal counsel, non-party movement actor, and individual activist are distinct roles.
- A grant opportunity is not an award; project cost is not automatically contract payment; membership is not recipient funding.
- Service/charity presence does not imply a pro-base or anti-base stance.
- Yonaguni remains framed through security environment/frontline risk, autonomy, referendum, Taiwan proximity, and life safety rather than forced environmental obstruction.

## Validation

The package is complete only when:

- all CSVs parse with fixed header widths;
- evidence IDs, venue IDs, and actor-event record IDs are unique;
- every `source_id` exists in the current source log and has an archive directory;
- every nonblank event ID exists in the current 9-event side table;
- every venue foreign key exists in `venue_taxonomy_v0.csv`;
- registry actor IDs in actor-event rows exist in the actor registry;
- every evidence-note object ID resolves to an existing main-table object, event, funding edge, or actor-event record.

This v0 passes those structural checks, but all rows remain seeds until human review.
