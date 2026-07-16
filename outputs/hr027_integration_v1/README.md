# HR-027 integration v1

Project-principal decisions dated 2026-07-16 are merged as A112–A115. Registry identity, continuity, class, primary-place and issue-tag fields are human-checked at E4.

Layer boundaries:

- 19 issue edges and 6 place edges are `ai_seeded` candidate formulations; registry admission does not publication-approve each edge.
- 17 event descriptions are held in `event_candidates_v1.csv` with `central_aev_status=not_inserted`.
- Three near-name warnings are stored separately from aliases and actors.
- No inter-actor relation, alliance or funding edge was created.
- S272 and S284 metadata corrections remain for HR-030 or explicit principal approval; S279 archive retry succeeded.

The authoritative human narrative is `docs/human_review_return_HR027_v1.md`; the idempotent merge is `scripts/merge_hr027.py`.
