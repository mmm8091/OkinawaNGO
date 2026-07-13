# NW2-H validation report

- central source rows: 295
- source IDs: unique continuous S001-S295
- integrated new unique URLs: 47 (S248-S294)
- reused existing URLs: 2 (S158, S204)
- new-to-new or new-to-old normalized URL collisions: 0
- grandfathered pre-NW2 duplicate URL groups: 1 (S022/S024 only; unchanged)
- archive manifest rows: 295
- S248-S294 archived: 40
- S248-S294 failed: 7
- S248-S294 not yet in manifest: 0
- preserved artifacts hash-checked: 267; mismatches: 0
- HR-030 unique URL rows: 22; stable source/audit IDs: yes; rows with populated human fields preserved: 0
- central source-log commit: prevalidated temporary CSV + atomic os.replace; no validation occurs after commit
- relation_or_claim_approved: 0 yes / 49 no unique URLs / 50 no proposal rows
- protected actor/edge tables: 14; SHA changes: 0
- unauthorized actor/edge/event writes by this integration script: 0
