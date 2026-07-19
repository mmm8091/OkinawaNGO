# Exploration system data v1 — validation report

Status: **PASS**

## Checks

- PASS — unique actor IDs: 122 rows
- PASS — unique place IDs: 20 rows
- PASS — unique issue IDs: 26 rows
- PASS — unique venue IDs: 16 rows
- PASS — unique source IDs: 295 rows
- PASS — unique evidence IDs: 49 rows
- PASS — unique demo episode IDs: 9 rows
- PASS — unique research episode IDs: 4 rows
- PASS — episode layers disjoint: demo=9 research=4
- PASS — unique demo relation IDs within relation type: 247 relation rows
- PASS — actor-issue references: 59 demo rows
- PASS — actor-place references: 16 demo rows with matching place key/label
- PASS — strict triple references: 67 demo rows
- PASS — actor-episode references: 15 demo rows
- PASS — event participation references: 63 demo rows
- PASS — legal role references: 27 demo rows
- PASS — all normalized source IDs resolve: unresolved=0
- PASS — demo rows have no unresolved source references: unresolved=0
- PASS — demo status gate: candidate and analytical episode layers excluded
- PASS — research status isolation: research rows remain explicitly marked
- PASS — event-only names do not enter actor collection: actors=122
- PASS — E0 sources cannot support claims: E0 sources=1
- PASS — archive manifest coverage: sources=295
- PASS — coverage dimensions complete: cells=125
- PASS — map geometry packaged: features=42

## Warnings

- 92 registry actors retain non-human review_status; registry membership is admitted for identity browsing, while their relations remain independently gated.
- historical_anchors is intentionally empty until NR-04/NR-05 candidates receive human continuity decisions.
- The packaged GeoJSON supports municipality/region rendering, but the 20 place nodes have no approved point coordinates or municipality crosswalk; NR-03 must not invent precise site markers.
- 13 human-checked event participants are preserved only as typed participation records and never enter actors.json.
- 8 legacy actor identity references are not central source IDs and remain explicit on registry objects: X001;X002;X003;X008;X009;X010;X011;X012.
- 11 unresolved legacy research references remain isolated from demo: X001;X002;X003;X008;X009;X010;X011;X012;X013;X014;X015.
- 1 human-reviewed actor-place edge is quarantined for a place key/label conflict: AP123.

## Build counts

```json
{
  "demo": {
    "actor_aliases": 27,
    "actors": 122,
    "episodes": 9,
    "evidence_notes": 49,
    "historical_anchors": 0,
    "issues": 26,
    "map_geometry_features": 42,
    "outcomes": 27,
    "places": 20,
    "relations": {
      "actor_episode": 15,
      "actor_issue": 59,
      "actor_place": 16,
      "event_participation": 63,
      "legal_roles": 27,
      "strict_place_issue": 67
    },
    "sources": 295,
    "venues": 16
  },
  "research": {
    "episodes": 4,
    "outcomes": 12,
    "relations": {
      "actor_episode": 4,
      "actor_issue": 182,
      "actor_place": 119,
      "event_participation": 4,
      "strict_place_issue": 263
    }
  }
}
```

The warnings are explicit research boundaries, not failed validation.
