# R10 completeness audit v1

This package separates exact within-package accounting from external-source completeness.

- `R10_bounded_completeness_brief_v1.md`: conclusion, safe wording, exact online gaps.
- `source_universe_coverage_v1.csv`: 13 bounded universes and permitted/prohibited claims.
- `relation_source_universe_crosswalk_v1.csv`: all 35 R10 relations mapped to their selection design and human gate.
- `s002_universe_index_v1.csv`: mechanical index of all 616 FY2024 official survey rows; it is not an approved relation table.
- `s099_program_cost_crosswalk_v1.csv`: page-level six-row non-zero program-cost crosswalk; S099 is image-only and this enumeration is not human review.
- `central_relation_sample_crosswalk_v1.csv`: all 43 central F rows mapped to R10 or an explicit exclusion class.
- `online_gap_and_human_task_suggestions_v1.csv`: conditional purposive-layer gaps and human-gate suggestions; the 616-row source extraction itself is complete.
- `validation_report_v1.md`: structural, SHA, foreign-key, and scope checks.

The full S002 source universe is now formalized in `outputs/R10_official_collaboration_universe_v1/`, including an authoritative 616-row table, source-label bimode tables, two figures, and the compact HR032 identity/crosswalk queue.  The audit index remains the independent extraction-parity check.

The audit never mutates central research tables and never upgrades a review status.
