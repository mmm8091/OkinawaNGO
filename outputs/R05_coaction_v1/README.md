# R05 co-action network v1

HR-020 is merged: all 14 identity/segmentation decisions are
`human_checked`. The package contains 169 source-list observations,
21 strict repeated identities (15
registry actors and 6 human-reviewed event-only
identities).

`source_name` remains literal. Event-only identities remain outside the
actor registry. Repeated participation and co-signing are event-level
observations, not stable alliances, membership, funding, hierarchy or
continuous coordination.

Regeneration order:

```powershell
python scripts\make_r05_coaction_v1.py
python scripts\merge_hr020_hr026_v1.py
```
