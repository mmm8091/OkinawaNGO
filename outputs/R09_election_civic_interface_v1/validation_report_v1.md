# R09 election-civic interface validation v1

Generated: 2026-07-13

- Event candidate rows: 19 ({'2014': 5, '2018': 7, '2022': 7}).
- Action types: {'endorsement': 4, 'issue_campaign': 4, 'observation': 5, 'public_meeting': 2, 'request': 4}; all five required types present.
- Year windows: 3; all `minimum_public_window_found`.
- Source proposals: 21; every `relation_or_claim_approved=no`.
- HR-026 rows: 19 stable IDs; 0 rows currently contain human/final/status values.
- Stable ID mapping: pre-existing `record_id` retains its `review_item_id`; new rows allocate only unused suffixes.
- HR preservation: 0 populated rows restored from the pre-existing file; 0 extra human columns retained.
- Temporary-copy sentinel test (`TEST_HUMAN_DECISION` plus final/status fields): passed; real HR table was not modified by the test.
- Online-exhausted bounded gaps: 5.
- Source foreign keys and record/proposal uniqueness: passed.
- Candidate/party node boundary: passed; no party is encoded as civic actor.
- Every event row has an explicit no-effect/no-alliance/no-endorsement-overreach boundary: passed.
- Two explanatory figures generated in PNG and SVG; SVG line-tail whitespace normalized after save: passed.
- Generated CSV/Markdown outputs are deterministic; figure metadata date is fixed.
