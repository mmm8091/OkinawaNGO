# R05 validation report v0

- Events: 3
- Participation observations / bipartite edges: 169
- Event observation status: accepted=167; source_segmentation_pending=2
- Identity rows: registry_actor=63; event_only_name=84; alias_pending=22
- Confirmed repeat-participation bridges: 15
- HR-020 questions: 14; all decision/reviewer/date/note fields blank

## Checks

- PASS — event counts exact: 67 / 31 / 71 = 169
- PASS — 2010 source anomaly retained: 66 comma tokens, 67 structured rows, HR020-06 pending
- PASS — participant keys and within-event source names unique
- PASS — bipartite edges exact: 169
- PASS — identity statuses exclusive; actor ids only on confirmed registry matches
- PASS — HR-020 exact: 14 questions; decision fields blank; participant FKs valid
- PASS — repeat bridge table conservative: 15 confirmed actors; pending identities excluded
- PASS — three pairwise event overlaps generated from confirmed registry identities
- PASS — S003-S006 archive paths and SHA-256 hashes verified
- PASS — two PNG figures generated and nontrivial in size


## Interpretation assertion

The package contains event-to-participant observations and repeated-public-participation indicators only. It contains no actor-to-actor stable-alliance edge and does not infer membership, funding, hierarchy or continuous coordination from co-signing.
