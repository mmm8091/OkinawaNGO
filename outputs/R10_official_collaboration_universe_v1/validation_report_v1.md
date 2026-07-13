# R10 official collaboration source-universe validation v1

Date: 2026-07-13

## Structural and scope checks

- PASS: authoritative extraction has sequential S002 rows 1-616
- PASS: 616 unique authoritative source-row IDs
- PASS: source rows preserve all PDF pages 1-86
- PASS: official mechanism counts match the verified S002 distribution
- PASS: official issue-field counts match the verified S002 distribution
- PASS: 390 distinct source-literal partner strings
- PASS: 365 machine display aliases; no actor identity count asserted
- PASS: partner display summary accounts for all 616 source rows
- PASS: partner-mechanism bimode edges account for all 616 source rows
- PASS: partner-department bimode edges account for all 616 source rows
- PASS: complete 19x10 issue-mechanism matrix sums to 616
- PASS: complete 15x10 department-mechanism matrix sums to 616
- PASS: official resource-type summary sums to 616
- PASS: exactly 10 S002 rows remain crosswalked to the separate purposive R10 layer
- PASS: no authoritative row is upgraded to actor identity
- PASS: no authoritative row is upgraded to a relation edge
- PASS: all eight HR032 human-decision fields remain blank
- PASS: second figure uses all 17 machine display labels meeting the disclosed >=5-row threshold
- PASS: all sixteen four-row tied labels are excluded; no arbitrary tie-break remains
- PASS: R10U-F01 renders at the expected 2808x2015 pixels
- PASS: R10U-F02 renders at the expected 3276x2700 pixels
- PASS: authoritative extraction exactly matches the previously validated 616-row audit index
- PASS: S002 PDF SHA matches the archive manifest

## Figure QA contract

- R10U-F01 uses only the 616-row authoritative source table and official code dictionaries; status `ready_now / no HR gate`.
- R10U-F02 uses department counts and all 17 machine display aliases meeting the disclosed `source_row_count >= 5` threshold; all sixteen four-row ties are excluded, so no arbitrary cutoff remains. The current figure is ready now, while canonical identity, JV-member split, registry crosswalk, and actor-level centrality remain gated by HR032.
- Both figures explicitly state that source-row counts are not organization, contract, award, payment, alliance, or political-stance claims.
- PASS (manual visual QA, 2026-07-13): R10U-F01 has readable labels, complete 19x10 cells, no clipping, no overlap, and no missing glyphs.
- PASS (manual visual QA, 2026-07-13): R10U-F02 has readable department and top-label panels, a separated legend/x-axis/caption, no clipping, and no missing glyphs.
- The generator additionally validates all figure input totals and exact PNG dimensions.

## Mutation boundary

- No central actor, actor-edge, amount, source-log, HR018, or registry file is written by this generator.
- The only human-review output is an eight-row HR032 queue with blank decision fields.
