# W2-00 system/accountability package validation v1

Date: 2026-08-22

Result: **PASS**

Scope: `outputs/us_presence_network_wave2_w2_00_system_accountability_v1/`

## Checks

| Check | Result | Detail |
|---|---|---|
| CSV parsing | PASS | Five CSV files parse with Python `csv.DictReader`. |
| Primary keys | PASS | 37 unique `anchor_id`; 17 unique `receipt_id`; 9 unique `denominator_id`; 3 unique `selection_frame_id`; 8 unique `change_note_id`. |
| Review-status schema | PASS | All 37 anchors, 9 denominator options and 3 frames use the legal value `ai_seeded`. |
| Anchor → receipt | PASS | Every receipt in every anchor's `source_receipt_ids` resolves to `source_receipts_v1.csv`; no missing backlink remains. |
| Receipt → anchor | PASS | Every anchor in every receipt's `supports_anchor_ids` resolves to `anchor_candidates_v1.csv` and contains the same receipt in `source_receipt_ids`. |
| Bidirectional crosswalk | PASS | Symmetric difference between the two anchor–receipt pair sets is empty. W2C-SR004–W2C-SR008 explicitly backlink W2C-A017. |
| Denominator references | PASS | Every nonblank anchor `denominator_id` resolves to `population_denominator_options_v1.csv`. |
| Artifact hashes | PASS | All 15 locally archived artifacts match their recorded SHA-256. W2C-SR004 and W2C-SR008 remain explicitly `blocked_403_web_observed` with blank artifact/hash fields. |
| Positive-entry frame | PASS | `USF-W2C-ENTRY13-2026-08-22` contains exactly TE01–TE13. |
| Empty search frames | PASS | The two not-yet-populated search frames leave `unit_count` blank; neither is encoded as zero cases. |
| Publication/write gates | PASS | All three frames are `research_only / not_frontend_ready / central_writeback=no`. |

No fact value, evidence interpretation, central table or frontend payload changed during the backlink repair.
