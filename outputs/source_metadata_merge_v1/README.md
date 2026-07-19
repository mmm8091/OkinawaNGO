# Source metadata merge v1

HR-022 and HR-030 principal decisions were applied to the central source log.

- 71 reviewed source rows received revised metadata, locators and bounded support scopes.
- S158 and S204 preserve their earlier `human_checked` status; the other reviewed rows use `human_revised`.
- `relation_or_claim_approved=no` is explicit on every reviewed row.
- S137/S197/S198 URL corrections are in the source log; archive retry remains a separate technical step.
- Archive success or failure never expands the approved support scope.
