# Prototype Instructions

Run the local server yourself and open the preview in the browser available to this environment. Do not give the user server-start instructions when you can run it.

Before making substantial visual changes, use the Product Design plugin's `get-context` skill when the visual source is unclear or no longer matches the current goal. When the user gives durable prototype-specific design feedback, preferences, or decisions, record them in `AGENTS.md`.

When implementing from a selected generated mock, treat that image as the source of truth for layout, component anatomy, density, spacing, color, typography, visible content, and hierarchy.

Session progress, QA evidence and iteration history do NOT belong here: QA goes to the repo-root `design-qa.md`, current status goes to `docs/phase1_workbench.md`. This file keeps only durable rules.

## NR-03 Durable Design Decisions

- Data: the frontend reads only the active, method-gated publication snapshot. Core data comes from the compiler-created `core/` projections, research families are separate files below `research/`, and complete exhibits are discovered through `views/exhibits.json`. Never read central CSVs, raw module directories, `demo/relations.json` or a mixed `research/candidates.json`; never invent coordinates (map uses the packaged 42-feature municipal GeoJSON only), and never write region/actor/issue prose in components. Missing required JSON is a load error, not an empty array.
- Publication: `npm run dev` and `npm run build` first compile an immutable `client_preview` snapshot and atomically activate its channel. The compiler requires every core-builder output to be decided by `research_publication_core_surfaces_v1.json` and projects only the exact path/JSON pointer permitted for the profile. Every production build or development-server generation binds one verified immutable release; development watches the channel and restarts Vite when it advances, so one page load cannot mix rows from two releases. The development middleware also returns JSON 404 for missing publication paths instead of SPA HTML. Public snapshots strip machine-local archive paths/hashes and internal review notes; `dist/release.json` binds the data release, frontend tree, base path, Git commit and dirty state.
- Pages: Overview (map states 全域/先岛聚焦 only), Actors, Time (fifth page, principal 2026-07-19), Pathways (six-stage ladder), Evidence (V4 coverage dimensions with per-facet bars and the implication panel). All five IA engines are live. IA amendments are recorded in `docs/exploration_system_information_architecture_v1.md` §12.
- Research view (topbar 已核/研究): pending candidates render with dashed edges/rings and 待审 badges; they never change reviewed-layer copy, relation types, or status semantics. The reviewed layer is named 已核视图 in the UI (the internal `demo/` directory name stays for compatibility).
- Copy discipline: nothing non-permanent appears (no NR-round stamps, no placeholder buttons, no "稍后" badges). Page titles are chart names; how-to-read and interpretation boundaries live only in the `ChartHelp` "?" popover. Per-object data fields (e.g. `interpretation_limit`) stay with their object.
- Typography: 11 overline / 12 small / 13 body / 14 lead / 19 h2 / 22 page title / 24 metric. Nothing below 11px; canvas labels render in screen space so zoom never shrinks them.
- Labels: issue/place/action/route codes are taxonomy codes, not "English text". The zh/ja/en formal mapping is a data-layer deliverable; the frontend consumes it only through `labelOf()` (`display_label_zh` fallback `display_label`) and never hardcodes translations.
- Interaction: both canvases support wheel zoom-to-cursor, drag pan, buttons, and reset. Map selection is point-in-polygon; region labels are anchored to projected geography and track zoom/pan; actor-class groups/colors, regions, place-display-region mappings and time periods come from `core/presentation/rules.json`, never from parallel React constants or regexes.
- Safety: node size ≠ influence; counts ≠ alliance; co-signing/shared events ≠ alliance; no evidence-depth color coding on the overview map; event years are not organizational continuity.
- QA: `npm run build` plus headless-Chrome screenshots at 1488 × 1024 into `prototypes/nr3_explorer/qa/` before claiming any visual pass; log results in the repo-root `design-qa.md`. Never leave unscoped element selectors (e.g. `.page-intro span`) — they silently override component rules.

## Exhibit Kit (2026-07-21)

- All published research exhibits use the shared kit in `src/components/exhibit/` (`ExhibitKit.jsx` + `exhibit.css`): ExhibitHeader, BoundaryNote, TierBadge, ExhibitTabs, RecordCard, MetaGrid, LimitLine, Unavailable. New exhibits compose these; do not fork per-exhibit card anatomy.
- Exhibit chrome copy is short; every data value, status label, denominator and interpretation_limit text renders from the payload. Never translate or paraphrase research content in components.
- Layer switching must never unmount pages: the reviewed core renders as soon as loaded; research candidates merge in asynchronously. A research-overlay failure shows a non-blocking banner, never a full-page loading state.
- The relation graph keeps the coordination family visible by default in research view, hidden by default in reviewed view.
