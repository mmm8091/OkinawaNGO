# research_wave_h3_frontline_memory_v1

Independent research package for the hypothesis that frontline/Taiwan-contingency language and Okinawa-war memory may provide a recent common vocabulary across otherwise heterogeneous civic actors.

## Reproduce

```powershell
python scripts\make_h3_frontline_memory_v1.py
python -m unittest tests.test_make_h3_frontline_memory_v1
```

## Data boundary

- Reads local files for S022, S023, S036, S119, S148 and S246 plus the source log, archive manifest and current actor/AEV/actor–issue tables. S022/S036 remain metadata-correction-gated and S119 remains archive-reconciliation-gated.
- Writes only this output directory.
- Every factual-looking row is `research_only` and `candidate`; `central_writeback=no`.
- Event participation, endorsement, speaking, organizing and personnel carriage are distinct roles. None is a stable alliance edge.
- H3a/H3b/H3c are separate tests. Schema tag growth is never used as evidence of historical vocabulary growth.

## Files

- `hypothesis_layers_v1.csv` — falsifiable H3a/H3b/H3c definitions.
- `source_observations_v1.csv` — short exact excerpts with explicit context actor, claim subject, target and locator.
- `diffusion_carrier_candidates_v1.csv` — event-bounded contact/carrier candidates; direction and adoption remain unconfirmed.
- `event_participant_candidates_v1.csv` — named event participants/endorsers, including provisional identities.
- `control_corpus_plan_v1.csv` and `negative_case_plan_v1.csv` — matched controls and disconfirming-case design.
- `human_review_queue_v1.csv` and `local_retrieval_queue_v1.csv` — explicit gates.
- `source_governance_v1.csv` — archive/source-log mismatch and reconciliation gate.
- `evidence_graph_v1.json` — visualization-ready candidate hypergraph, not a relation network.
- `brief_v1.md` — current interpretation and limits.
- `manifest.json` — inputs, current counts, package counts and boundary metadata.
