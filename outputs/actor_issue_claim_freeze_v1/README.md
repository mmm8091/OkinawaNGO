# HR-035 actor–issue claim freeze v1

Current assignment: Batch 1, 15 case/referendum/procedure-bounded actor–issue facts.

Files:

- `HR035_actor_issue_fact_review_batch01_v1.csv` — principal decision sheet;
- `HR035_source_bundle_batch01_v1.csv` — one row per task edge × source;
- `validation_report_v1.md` — assignment integrity checks.

Regenerate:

```powershell
python scripts\make_hr035_actor_issue_claim_freeze_v1.py
```

All decision fields are intentionally blank. The package writes no central table and no
frontend artifact. It preserves HR-019 scope decisions as read-only context and asks only
whether the underlying actor–issue fact is adequately supported.
