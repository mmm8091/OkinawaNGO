# Prototype Instructions

Run the local server yourself and open the preview in the browser available to this environment. Do not give the user server-start instructions when you can run it.

Before making substantial visual changes, use the Product Design plugin's `get-context` skill when the visual source is unclear or no longer matches the current goal. When the user gives durable prototype-specific design feedback, preferences, or decisions, record them in `AGENTS.md`.

When implementing from a selected generated mock, treat that image as the source of truth for layout, component anatomy, density, spacing, color, typography, visible content, and hierarchy.

Session progress, QA evidence and iteration history do NOT belong here: QA goes to the repo-root `design-qa.md`, current status goes to `docs/phase1_workbench.md`. This file keeps only durable rules.

## NR-03 Durable Design Decisions

- Data: the frontend reads only the NR-02 package (`demo/` + `views/`; `research/candidates.json` only after the user switches to research view). Never read central CSVs, never invent coordinates (map uses the packaged 42-feature municipal GeoJSON only), never write region/actor/issue prose in components.
- Pages: Overview (map states 全域/先岛聚焦 only), Actors, Time (fifth page, principal 2026-07-19), Pathways (six-stage ladder), Evidence (V4 coverage dimensions with per-facet bars and the implication panel). All five IA engines are live. IA amendments are recorded in `docs/exploration_system_information_architecture_v1.md` §12.
- Research view (topbar 已核/研究): pending candidates render with dashed edges/rings and 待审 badges; they never change reviewed-layer copy, relation types, or status semantics. The reviewed layer is named 已核视图 in the UI (the internal `demo/` directory name stays for compatibility).
- Copy discipline: nothing non-permanent appears (no NR-round stamps, no placeholder buttons, no "稍后" badges). Page titles are chart names; how-to-read and interpretation boundaries live only in the `ChartHelp` "?" popover. Per-object data fields (e.g. `interpretation_limit`) stay with their object.
- Typography: 11 overline / 12 small / 13 body / 14 lead / 19 h2 / 22 page title / 24 metric. Nothing below 11px; canvas labels render in screen space so zoom never shrinks them.
- Labels: issue/place/action/route codes are taxonomy codes, not "English text". The zh/ja/en formal mapping is a data-layer deliverable; the frontend consumes it only through `labelOf()` (`display_label_zh` fallback `display_label`) and never hardcodes translations.
- Interaction: both canvases support wheel zoom-to-cursor, drag pan, buttons, and reset. Map selection is point-in-polygon; region labels are anchored to projected geography and track zoom/pan; registry places map to display regions via the explicit `PLACE_DISPLAY_REGION` table (P011/P012→yaeyama, P013→miyako, default→okinawa), never by regexing `place.region`.
- Safety: node size ≠ influence; counts ≠ alliance; co-signing/shared events ≠ alliance; no evidence-depth color coding on the overview map; event years are not organizational continuity.
- QA: `npm run build` plus headless-Chrome screenshots at 1488 × 1024 into `prototypes/nr3_explorer/qa/` before claiming any visual pass; log results in the repo-root `design-qa.md`. Never leave unscoped element selectors (e.g. `.page-intro span`) — they silently override component rules.
