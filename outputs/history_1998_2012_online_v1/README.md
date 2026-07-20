# history_1998_2012_online_v1

Isolated NR-05 research package for the Phase-1 Okinawa NGO/civic-organization project.

## Contract files

- `historical_anchor_candidates.csv` — 15 dated event/context anchors.
- `organization_status_candidates.csv` — formation, legal-status, minimum-active-date and round-label candidates.
- `source_candidates.csv` — exact source/date/locator/support-scope crosswalk.
- `search_log.md` — query tracks, date protocol and known exclusions.
- `online_exhausted_gaps.csv` — online exhaustion and local/new-primary needs.
- `human_review_queue.csv` — 20-row research candidate pool; explicitly **not** a formally dispatched HR task.
- `brief.md` — empirical judgment, interpretation candidates and novelty boundaries.
- `fig1_carrier_venue_trace_timeline_v1.svg` — separated macro-context and carrier/venue/record timeline.
- `fig1_carrier_venue_trace_timeline_v1_brief.md` — figure encoding and non-inference contract.
- `validation_report.md` — machine gates and file hashes.

## Reproduce

```powershell
python scripts\make_history_1998_2012_online_v1.py
python -m unittest discover -s tests -p "test_make_history_1998_2012_online_v1.py" -v
```

To test in another directory:

```powershell
python scripts\make_history_1998_2012_online_v1.py --output-dir $env:TEMP\nr05_check
```

## Hard boundaries

This package does not approve any actor, source, edge, alliance, funding relation, genealogy or continuity
claim. It does not write central tables, source archives, frontend contracts or control documents. Every CSV
row remains `research_only / candidate / ai_seeded / not_frontend_ready / central_writeback=no`.
