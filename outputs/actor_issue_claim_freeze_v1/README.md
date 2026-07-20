# HR-035 actor–issue claim freeze v1

Batch 1 is a completed historical assignment: 15 case/referendum/procedure-bounded
actor–issue facts. Batch 2 is the current formal assignment: 18 E4, scope-reviewed facts
plus five one-per-actor identity companion decisions.

## Batch 2 — current

- `HR035_actor_issue_fact_review_batch02_v1.csv` — 18 fact decisions;
- `HR035_actor_identity_companion_batch02_v1.csv` — five identity decisions;
- `HR035_source_bundle_batch02_v1.csv` — one row per review item × source;
- `validation_report_batch02_v1.md` — assignment integrity checks.

Regenerate:

```powershell
python scripts\make_hr035_batch02_v1.py
```

## Batch 1 — completed provenance

- `HR035_actor_issue_fact_review_batch01_v1.csv`;
- `HR035_source_bundle_batch01_v1.csv`;
- `validation_report_v1.md`.

Historical regeneration:

```powershell
python scripts\make_hr035_actor_issue_claim_freeze_v1.py
```

All Batch 2 decision fields are intentionally blank. The package writes no central table
or frontend artifact. It preserves HR-019 scope decisions as read-only context and asks
only whether each identity and underlying actor–issue fact are adequately supported.
