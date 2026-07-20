# Exploration system data v1 — validation report

Status: **PASS**

## Checks

- PASS — unique actor IDs: 122 rows
- PASS — unique place IDs: 21 rows
- PASS — unique issue IDs: 26 rows
- PASS — unique venue IDs: 16 rows
- PASS — unique source IDs: 295 rows
- PASS — unique evidence IDs: 49 rows
- PASS — unique demo episode IDs: 9 rows
- PASS — unique research episode IDs: 4 rows
- PASS — unique genealogy anchor IDs: 5 rows
- PASS — episode layers disjoint: demo=9 research=4
- PASS — genealogy anchors are reviewed and actor-bounded: 5 reviewed lifecycle rows
- PASS — bounded genealogy anchors carry explicit gaps: supported_bounded lifecycle rows have confirmed and missing scope
- PASS — episode display overlay is complete and translation-only: episodes=13 fields=7 languages=3 gaps=0 rewrites=0
- PASS — unique demo relation IDs within relation type: 380 relation rows
- PASS — actor-issue references: 141 demo rows
- PASS — actor-issue display_state values are legal: illegal=0
- PASS — frozen_bounded actor-issue rows carry missing_scope: missing=0
- PASS — no fact-pending rows enter the demo actor-issue layer: pending=0
- PASS — actor-issue display_state counts cover every edge: accepted_unfrozen=58 fact_pending=114 frozen_bounded=83 scope_reviewed_fact_pending=28
- PASS — actor-place references: 53 demo rows with matching place key/label
- PASS — strict triple references: 81 demo rows
- PASS — actor-episode references: 15 demo rows
- PASS — event participation references: 63 demo rows
- PASS — legal role references: 27 demo rows
- PASS — typed relation review_status values are legal: 43 typed rows
- PASS — dyadic relation endpoints resolve to registry actors: 22 dyadic rows
- PASS — no leads enter dyadic relations: 22 dyadic rows
- PASS — supported_bounded rows carry scope boundaries: 15 supported_bounded rows
- PASS — rejected, duplicate, and E0 rows stay hidden: leaked=0
- PASS — typed relation rows carry schema v1 section 9 fields: missing=0
- PASS — R10R029 stays out of dyadic relations: aggregate observation only
- PASS — F025 keeps an empty amount: bounded KOSC to AWWA contribution without amount
- PASS — demo typed collections are reviewed tier only: candidates and leads stay out of the reviewed layer
- PASS — research typed collections contain candidates or explicitly gated leads: reviewed relation facts may remain research-only when endpoint graphing is gated
- PASS — case roles preserved without edge derivation: 27 case roles; non_party never derives edges
- PASS — all normalized source IDs resolve: unresolved=0
- PASS — demo rows have no unclassified unresolved source references: unresolved=0
- PASS — demo status gate: candidate and analytical episode layers excluded
- PASS — research status isolation: research rows remain explicitly marked
- PASS — event-only names do not enter actor collection: actors=122
- PASS — E0 sources cannot support claims: E0 sources=1
- PASS — archive manifest coverage: sources=295
- PASS — coverage dimensions complete: cells=120
- PASS — map geometry packaged: features=42
- PASS — presentation mappings cover current research objects: actor_classes=26 regions=6 periods=4

## Warnings

- 85 registry actors retain non-human review_status; registry membership is admitted for identity browsing, while their relations remain independently gated.
- 5 principal-reviewed lifecycle anchors are exported. They are bounded observations, not a complete post-1972 genealogy.
- The packaged GeoJSON supports municipality/region rendering, but the 21 place nodes have no approved point coordinates or municipality crosswalk; NR-03 must not invent precise site markers.
- 13 human-checked event participants are preserved only as typed participation records and never enter actors.json.
- 8 legacy actor identity references are not central source IDs and remain explicit on registry objects: X001;X002;X003;X008;X009;X010;X011;X012.
- 9 unresolved legacy research references remain isolated from demo: X001;X002;X003;X008;X009;X010;X011;X012;X013.
- 5 legacy X-code references remain explicit on human-reviewed demo rows and are not promoted to central source IDs: X001;X002;X003;X010;X012.
- 6 legacy typed-relation source references are not central source IDs and stay explicit on the rows: X001;X002;X008;X009;X010;X011.
- 1 rejected or duplicate funding rows are excluded from every typed relation collection: F008.

## Build counts

```json
{
  "actor_issue_states": {
    "display_state_counts": {
      "accepted_unfrozen": 58,
      "fact_pending": 114,
      "frozen_bounded": 83,
      "scope_reviewed_fact_pending": 28
    },
    "research_fact_gate_counts": {
      "fact_pending": 110,
      "needs_local_retrieval": 5,
      "needs_second_source": 27
    },
    "valid_edges": 283
  },
  "actor_registry": {
    "current_visible": 121,
    "hidden_provenance_rows": 1,
    "provenance_rows": 122
  },
  "demo": {
    "actor_aliases": 39,
    "actors": 121,
    "episodes": 9,
    "evidence_notes": 49,
    "historical_anchors": 5,
    "issues": 26,
    "map_geometry_features": 42,
    "outcomes": 27,
    "places": 21,
    "relations": {
      "actor_episode": 15,
      "actor_issue": 141,
      "actor_place": 53,
      "event_participation": 63,
      "legal_roles": 27,
      "strict_place_issue": 81
    },
    "sources": 295,
    "venues": 16
  },
  "episode_display": {
    "approved_translation_cells": 273,
    "episodes": 13,
    "fields_per_episode": 7,
    "source_text_fallbacks": 0
  },
  "research": {
    "episodes": 4,
    "outcomes": 12,
    "relations": {
      "actor_episode": 4,
      "actor_issue": 142,
      "actor_place": 77,
      "event_participation": 4,
      "strict_place_issue": 225
    }
  },
  "typed_relations": {
    "claim_status_counts": {
      "candidate": 13,
      "lead": 2,
      "supported": 13,
      "supported_bounded": 15
    },
    "demo": {
      "administrative_records": 6,
      "aggregate_observations": 2,
      "case_roles": 27,
      "dyadic_relations": 14,
      "event_participation": 4,
      "genealogy_anchors": 5,
      "relation_leads": 0
    },
    "excluded": 1,
    "input_observations": 44,
    "research": {
      "administrative_records": 5,
      "aggregate_observations": 0,
      "dyadic_relations": 8,
      "event_participation": 0,
      "genealogy_anchors": 0,
      "relation_leads": 4
    }
  }
}
```

The warnings are explicit research boundaries, not failed validation.
