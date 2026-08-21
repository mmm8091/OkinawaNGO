# U.S.-presence network wave 1 index

This folder contains the bounded 17-row `us_origin` analytical scope used by
the first U.S.-presence network wave.

## Exact denominator

- 9 service/charity comparison actors
- 6 accountability comparison actors
- 1 public-diplomacy program node
- 1 funder watchlist node

The two 9/6 groups contain 15 organizations used for comparison. X013 and X014
are retained as separate program/institutional observation nodes, so 9+6 is not
the full registry total of 17 U.S.-origin rows.

## Files

- `us_origin_actor_scope_v1.csv`: one row per selected actor, joined to the
  candidate official-page directory.
- `us_origin_actor_scope_summary_v1.csv`: exact group counts.
- `manifest.json`: input hashes, counts, output hashes and package boundary.
- `post_principal_validation_report_v1.json`: consolidated validation result for
  the four formal return packets and the five architecture decisions.
- `post_principal_manifest_v1.json`: SHA-256 receipt for the authoritative
  post-principal return and handoff files.

The grouping is a research selection frame, not a fixed pro-/anti-U.S. actor
classification. The principal confirmed this exact 17-row 9/6/1/1 frame on
2026-08-21 as the frozen `USF-US-ORIGIN17-2026-08-19` baseline. The physical
CSV remains an immutable pre-checkpoint artifact with blank decision cells;
those blanks no longer mean the frame is undecided. Newly approved service
actors require a successor frame. The central registry is unchanged, and the
overlay is not yet a frontend contract.

Related packages:

- `outputs/us_presence_network_architecture_v1/`
- `outputs/actor_directory_v1/`
- `outputs/us_presence_service_recon_v1/`
- `outputs/us_presence_accountability_recon_v1/`
- `outputs/us_presence_relation_retype_v1/`
- `outputs/us_presence_literature_positioning_v1/`
- `docs/human_review_return_USN_architecture_checkpoint_v1.md`
- `docs/us_presence_network_wave1_merge_handoff_v1.md`

All four formal review packets and the five architecture checkpoint decisions
are principal-confirmed as of 2026-08-21. This package records that review
closure only: it does not expand the six relation rules into the 43-row
crosswalk and does not authorize central data, publication-adapter or frontend
writeback. The architecture CSVs still expose the pre-return `L1/L2/L3`
machine aliases; migration to the approved `LEG0`-`LEG3` names is a separate
mechanical follow-up.

Rebuild:

```powershell
python scripts\make_us_origin_scope_overlay_v1.py
python -m unittest tests.test_make_us_origin_scope_overlay_v1
```
