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

The grouping is a research selection frame, not a fixed pro-/anti-U.S. actor
classification. Function is coded later on dated actions or relations. All
human-decision cells remain blank, the central registry is unchanged, and the
overlay is not yet a frontend contract.

Related packages:

- `outputs/us_presence_network_architecture_v1/`
- `outputs/actor_directory_v1/`
- `outputs/us_presence_service_recon_v1/`
- `outputs/us_presence_accountability_recon_v1/`
- `outputs/us_presence_relation_retype_v1/`
- `outputs/us_presence_literature_positioning_v1/`

Rebuild:

```powershell
python scripts\make_us_origin_scope_overlay_v1.py
python -m unittest tests.test_make_us_origin_scope_overlay_v1
```
