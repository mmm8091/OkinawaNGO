# R3 spatial dossier validation v1

- Central actor-place input: 135 unique edges.
- Derived semantics: 135 unique rows; six allowed candidate values; no default or missing classification.
- Underlying review layer: 17 human-reviewed / 118 candidate or evidence-gap rows.
- HR-025: 47 semantic items; 0 rows contain preserved human fields and reruns retain them by stable `object_id`.
- Sakishima: 14/14 rows (Yonaguni 6 / Ishigaki 4 / Miyako 4).
- Source crosswalk: 214 rows; actor-place refs expanded 186.
- Place-key integrity: one explicit mismatch, AP123, retained for human review.
- SVG XML parse and trailing-whitespace check: pass for 3/3 figures. PNG size check: pass for 3/3 figures.
- Yonaguni guardrail: frontline/Taiwan proximity, autonomy/referendum and life-safety retained; no forced environmental framing.

Deterministic artifact hashes are generated in-memory for the checks above; the
report intentionally omits them so reruns remain concise. No base central
table was modified; derived interim32 was regenerated.
