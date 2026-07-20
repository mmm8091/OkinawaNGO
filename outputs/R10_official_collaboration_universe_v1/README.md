# R10 official collaboration source universe v1

This is the authoritative FY2024 S002 source-universe layer for R10. The
formal CSVs are the current inputs; do not rerun the historical PDF
extraction/builder against the merged project layer.

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

- `fig_r10_s002_issue_mechanism_matrix_current.svg/.html`: current pure 616-row aggregation, `ready_now / no HR gate`; recommended main-text figure.
- `fig_r10_s002_partner_department_resource_structure_current.svg/.html`: current raw-label aggregation using the disclosed fixed threshold `source_row_count >= 5` (17 labels); recommended supporting/main appendix figure.
- The two `*_v1.png` files and `validation_report_v1.md` are preserved historical extraction/render artifacts. They are not overwritten by the current renderer.
- `figure_registry_v1.csv`: historical package-level fact layer, gate and caption registry. Formal-report asset routing is current in `outputs/report_assembly_v1/figure_manifest_v1.csv`.

## Interpretation and human review

- `R10_official_collaboration_universe_brief_v1.md`: answers the R10 basic question while separating source universe, purposive sample, and HR018 relation layer.
- `HR032_partner_alias_crosswalk_review_v1.csv` and `HR032_crosswalk_merge_summary_v1.csv`: all eight crosswalk decisions are complete; they do not create actor, payment or relation edges and do not alter the raw-label source-universe figures.
- `validation_report_v1.md`: historical source SHA, extraction parity and legacy-PNG checks. Current table parity and render boundaries are tested in `tests/test_render_r10_official_universe_current.py`.

No output in this package is an actor registry, approved relation edge, award
table, payment table, alliance, or political-stance classification. Safely
redraw only the current F035/F036 assets with:

`python scripts/render_r10_official_universe_current.py`
