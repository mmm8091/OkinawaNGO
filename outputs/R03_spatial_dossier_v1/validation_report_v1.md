# R3 spatial dossier validation v1

- Central actor-place input: 135 unique historical edges; 130 active / 5 retired.
- Derived semantics: 135 unique rows; six allowed values; human-frozen and machine-candidate semantics remain distinct.
- Active review layer: 53 human-reviewed / 77 candidate or evidence-gap rows.
- HR-025: complete; 47 historical items and 47 preserved human rows.
- Sakishima: 13 active rows (Yonaguni 6 / Ishigaki 3 / Miyako 4); one rejected Ishigaki row remains in the 135-row audit layer only.
- Source crosswalk: 216 rows; actor-place refs expanded 183.
- Place-key integrity: zero mismatches; AP123 is P007 Camp Foster and retains its original key in the central audit fields.
- SVG XML parse and trailing-whitespace check: pass for 3/3 figures. PNG size check: pass for 3/3 figures.
- Yonaguni guardrail: frontline/Taiwan proximity, autonomy/referendum and life-safety retained; no forced environmental framing.

Deterministic artifact hashes are generated in-memory for the checks above; the
report intentionally omits them so reruns remain concise. No base central
table was modified; derived interim32 was regenerated.
