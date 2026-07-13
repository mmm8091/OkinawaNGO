# R10 official collaboration source universe v1

This is the authoritative, rerunnable FY2024 S002 source-universe layer for R10.

## Formal source tables

- `official_collaboration_source_universe_v1.csv`: all 616 authoritative mechanical source rows, preserving `source_row_number` and `pdf_page`.
- `official_resource_type_summary_v1.csv`: the 10 official collaboration mechanisms and descriptive counts.
- `issue_mechanism_matrix_v1.csv`: full 19×10 matrix, including zero cells.
- `department_mechanism_matrix_v1.csv`: full 15×10 matrix, including zero cells.
- `partner_mechanism_bimode_edges_v1.csv`: source-label × official-mechanism bimode aggregation.
- `partner_department_bimode_edges_v1.csv`: source-label × department aggregation.
- `partner_display_alias_summary_v1.csv`: 365 machine display labels; these are not actor identities.
- `machine_display_alias_collision_audit_v1.csv`: PDF-wrap normalization collisions only.
- `department_resource_summary_v1.csv` and `descriptive_statistics_v1.csv`: descriptive source-universe statistics.

## Figures and report roles

- `fig_r10_s002_issue_mechanism_matrix_v1.png`: pure 616-row aggregation, `ready_now / no HR gate`; recommended main-text figure.
- `fig_r10_s002_partner_department_resource_structure_v1.png`: current raw-label aggregation uses the disclosed fixed threshold `source_row_count >= 5` (17 labels) and is ready now; HR032 applies only if future writing turns a label into a canonical actor, splits JV members, or creates a registry crosswalk. Recommended supporting/main appendix figure.
- `figure_registry_v1.csv`: exact fact layer, gate, suggested report role, and conservative caption for both figures.

## Interpretation and human review

- `R10_official_collaboration_universe_brief_v1.md`: answers the R10 basic question while separating source universe, purposive sample, and HR018 relation layer.
- `HR032_partner_alias_crosswalk_review_v1.csv` and `HR032_review_guide_v1.md`: eight high-value ambiguities only; all human decision fields are blank.
- `validation_report_v1.md`: source SHA, extraction parity, row/code, aggregation, gate, and cleanliness checks.

No output in this package is an actor registry, approved relation edge, award table, payment table, alliance, or political-stance classification. Run with `python scripts/make_r10_official_collaboration_universe_v1.py`.
