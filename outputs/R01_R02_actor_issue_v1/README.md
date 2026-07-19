
# R01/R02 actor–issue v1

This module package implements the original Phase-1 acceptance outputs for R1
and R2 without changing the central registry or source log. Run:

```powershell
python scripts/make_r01_r02_actor_issue.py
```

Primary reading order: `R01_R02_explanatory_brief_v1.md`, figures 1–4,
`validation_metrics_v1.csv`, then `HR019/HR019_review_guide_v0.md`.

The central registry and layered edge derivative retain the complete historical
audit (122 actor rows; 248 edge rows).
Current figures, co-occurrence, bridge and coverage outputs use only
121 active actors and 238 active edges. The legacy filename
`actor_class_audit_118_v1.csv` is retained for downstream compatibility; its
rows now carry explicit `analysis_inclusion` and exclusion-reason fields.

Rejected, unsupported, excluded, retired, deactivated and inactive-endpoint
records are historical audit rows, never candidate network edges. Event
participation and issue co-occurrence are not treated as stable alliances.
