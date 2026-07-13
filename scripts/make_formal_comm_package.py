from __future__ import annotations

"""Build the second-round boss-facing communication package.

Output: outputs/formal_comm_v0/index.html  (single self-contained file)
        outputs/formal_comm_v0/README.md

Design goal: a figure-forward, web-native progress report with front-end
readability. All charts are inline SVG / CSS driven by the real project CSVs,
so the page reflects current data and needs no external assets to open.

Conservative-framing rules are enforced in the copy: candidate edges are not
final findings, co-signing is event participation not alliance, grant
opportunity is not awarded funding, service organisations are coded by
function, and Yonaguni uses the frontline / autonomy / life-safety frame.
"""

import csv
import html
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
EXPL = ROOT / "outputs" / "explanatory_v0"
MODULE = ROOT / "outputs" / "module_completion_v0"
ARCHIVE_MANIFEST = ROOT / "source_docs" / "source_archive" / "source_archive_manifest.csv"
OUT = ROOT / "outputs" / "formal_comm_v0"

REPORT_DATE = "2026-07-01"

# ---------------------------------------------------------------------------
# palette
# ---------------------------------------------------------------------------

INK = "#22303a"
BODY = "#4a5763"
MUTED = "#7c8791"
LINE = "#e3e8ec"
PANEL = "#ffffff"
PAGE = "#f4f6f8"
BRAND = "#1f4e5f"
BRAND_SOFT = "#eaf1f2"

EVIDENCE = {"E4": "#2f5d7c", "E3": "#5b8266", "E2": "#c99a3b"}

ORIGIN_COLOR = {
    "okinawa_local": "#2f6f73",
    "japan_domestic": "#9b5b4d",
    "international": "#5f5b99",
    "us_origin": "#7a6a3a",
    "mixed_or_network": "#4b7f52",
    "public_institution": "#68707a",
    "corporate": "#8a6f8f",
    "unclear": "#9aa0a6",
}
ORIGIN_LABEL = {
    "okinawa_local": "冲绳本地",
    "japan_domestic": "日本国内",
    "international": "国际",
    "us_origin": "美国来源",
    "mixed_or_network": "跨境 / 网络",
    "public_institution": "公共机构",
    "corporate": "企业",
    "unclear": "未定",
}

ISSUE_COLOR = {
    "anti_base": "#9b5b4d",
    "biodiversity": "#4b7f52",
    "international_advocacy": "#5f5b99",
    "local_autonomy": "#2f6f73",
    "legal": "#2f5d7c",
    "life_safety": "#c08a3b",
    "frontline_prevention": "#b06a3a",
    "military_family_service": "#7f8790",
}


# ---------------------------------------------------------------------------
# io helpers
# ---------------------------------------------------------------------------

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def lerp_color(c0: str, c1: str, t: float) -> str:
    t = max(0.0, min(1.0, t))
    a = tuple(int(c0[i : i + 2], 16) for i in (1, 3, 5))
    b = tuple(int(c1[i : i + 2], 16) for i in (1, 3, 5))
    r, g, bl = (round(a[i] + (b[i] - a[i]) * t) for i in range(3))
    return f"#{r:02x}{g:02x}{bl:02x}"


# ---------------------------------------------------------------------------
# metrics
# ---------------------------------------------------------------------------

def load_metrics() -> dict[str, int]:
    actors = read_csv(DATA / "01_actor_registry_initial_v0.csv")
    issue_edges = read_csv(DATA / "07_actor_issue_edges_initial_v0.csv")
    place_edges = read_csv(DATA / "08_actor_place_edges_initial_v0.csv")
    funding = read_csv(DATA / "15_funding_or_support_edges_sample_v0.csv")
    issues = read_csv(DATA / "03_issue_taxonomy_v0.csv")
    places = read_csv(DATA / "04_place_registry_v0.csv")
    manifest = read_csv(ARCHIVE_MANIFEST)
    candidates = read_csv(MODULE / "actor_registry_extension_candidates_2020_mmc_v0.csv")

    arch = Counter(r["archive_status"] for r in manifest)
    local_archived = arch.get("archived", 0) + arch.get("manual_archived", 0)
    failed = arch.get("failed", 0)
    real_url = local_archived + failed
    inferred = arch.get("skipped_inferred_url", 0)
    non_url = arch.get("skipped_non_url_reference", 0)

    return {
        "actors": len(actors),
        "issue_edges": len(issue_edges),
        "place_edges": len(place_edges),
        "funding": len(funding),
        "issues": len(issues),
        "places": len(places),
        "sources": len(manifest),
        "real_url": real_url,
        "local_archived": local_archived,
        "failed": failed,
        "inferred": inferred,
        "non_url": non_url,
        "archived": arch.get("archived", 0),
        "manual_archived": arch.get("manual_archived", 0),
        "candidates": len(candidates),
    }


# ---------------------------------------------------------------------------
# reusable fragments
# ---------------------------------------------------------------------------

def kicker(text: str) -> str:
    return f'<div class="kicker">{esc(text)}</div>'


def caveat_note(text: str) -> str:
    return f'<p class="readnote">{text}</p>'


# ---------------------------------------------------------------------------
# chart 1 — place x issue frame matrix (CSS grid heatmap)
# ---------------------------------------------------------------------------

FRAME_ORDER = [
    ("base / anti-military", "F1", "反基地 / 反军事"),
    ("ecology / environment", "F2", "环保 / 生态"),
    ("life / health safety", "F3", "生活 / 健康安全"),
    ("autonomy / referendum", "F4", "地方自治 / 公投"),
    ("legal / procedure", "F5", "法律 / 程序"),
    ("international route", "F6", "国际路径"),
    ("frontline / Taiwan", "F7", "前线 / 台湾"),
]
PLACE_ORDER = [
    "Henoko", "Oura Bay", "Ishigaki", "Miyako", "Yonaguni",
    "Kadena", "Futenma", "Camp Foster",
    "U.S. Consulate General Naha", "JICA Okinawa",
]


def build_place_matrix() -> str:
    rows = read_csv(EXPL / "place_issue_matrix.csv")
    counts: dict[tuple[str, str], int] = {}
    for r in rows:
        counts[(r["place"], r["frame"])] = int(r["actor_count"])
    vmax = max(counts.values()) or 1

    header = '<div class="hm-cell hm-corner"></div>'
    for _frame, code, _cn in FRAME_ORDER:
        header += f'<div class="hm-cell hm-head" title="{esc(_frame)}">{code}</div>'

    body = ""
    for place in PLACE_ORDER:
        body += f'<div class="hm-cell hm-row">{esc(place)}</div>'
        for frame, _code, _cn in FRAME_ORDER:
            v = counts.get((place, frame), 0)
            if v == 0:
                bg, fg, val = "#f2f5f6", "#c3ccd2", ""
            else:
                t = (v / vmax) ** 0.72
                bg = lerp_color("#dcebe8", BRAND, t)
                fg = "#ffffff" if t > 0.45 else "#20343b"
                val = str(v)
            body += (
                f'<div class="hm-cell hm-val" style="background:{bg};color:{fg}">{val}</div>'
            )

    legend = "".join(
        f'<li><span class="fk-code">{code}</span>{esc(cn)} '
        f'<span class="fk-en">{esc(en)}</span></li>'
        for en, code, cn in FRAME_ORDER
    )

    return f"""
<div class="hm-wrap">
  <div class="hm-grid">{header}{body}</div>
  <ul class="frame-key">{legend}</ul>
</div>
"""


# ---------------------------------------------------------------------------
# chart 2 — Henoko internationalization pathway (inline SVG)
# ---------------------------------------------------------------------------

PATHWAY_LAYERS = [
    ("地方现场", "#e7f0f1", [(["Henoko /", "Oura Bay"], "P002 / P003")]),
    ("地方 actor", "#e8f2ea", [
        (["A019", "ヘリ基地反対協"], "E4"),
        (["A003", "ジュゴンネットワーク沖縄"], "E3"),
        (["A076", "Save the Dugong Fdn."], "E3"),
    ]),
    ("日本 NGO / 法律", "#f4ece6", [
        (["A004", "NACSJ"], "E4"),
        (["A005", "WWF Japan"], "E4"),
        (["A020", "JELF"], "E4"),
    ]),
    ("转译框架", "#f4f0dc", [
        (["dugong /", "biodiversity"], "E4"),
        (["EIA / 法律", "程序"], "E3/E4"),
        (["local", "autonomy"], "E3"),
    ]),
    ("国际路径", "#eae8f2", [
        (["A001", "OEJP → MMC"], "E4"),
        (["A009", "Earthjustice"], "E4"),
        (["2015 / 2020", "署名网络"], "署名限定"),
    ]),
]


def build_pathway_svg() -> str:
    W, H = 1000, 384
    pad_top, pad_bottom = 54, 30
    n_cols = len(PATHWAY_LAYERS)
    nw, nh = 168, 60
    col_x = [40 + i * ((W - 80 - nw) / (n_cols - 1)) for i in range(n_cols)]

    # vertical centres per column
    positions: list[list[tuple[float, float]]] = []
    for _title, _c, nodes in PATHWAY_LAYERS:
        n = len(nodes)
        span = (H - pad_top - pad_bottom)
        gap = span / max(n, 1)
        ys = [pad_top + gap * (i + 0.5) - nh / 2 for i in range(n)]
        positions.append([(0.0, y) for y in ys])

    parts = [f'<svg viewBox="0 0 {W} {H}" class="pathway" role="img" '
             f'aria-label="边野古国际化路径图">']

    # connectors first (behind nodes)
    for li in range(n_cols - 1):
        left_nodes = PATHWAY_LAYERS[li][2]
        right_nodes = PATHWAY_LAYERS[li + 1][2]
        for i, _ln in enumerate(left_nodes):
            x1 = col_x[li] + nw
            y1 = positions[li][i][1] + nh / 2
            for j, _rn in enumerate(right_nodes):
                x2 = col_x[li + 1]
                y2 = positions[li + 1][j][1] + nh / 2
                if len(left_nodes) > 2 and len(right_nodes) > 2 and abs(i - j) >= 2:
                    continue
                mx = (x1 + x2) / 2
                parts.append(
                    f'<path d="M{x1:.0f},{y1:.0f} C{mx:.0f},{y1:.0f} {mx:.0f},{y2:.0f} '
                    f'{x2:.0f},{y2:.0f}" fill="none" stroke="#9aa8b0" '
                    f'stroke-width="1.1" opacity="0.5"/>'
                )

    # column titles + nodes
    for li, (title, color, nodes) in enumerate(PATHWAY_LAYERS):
        cx = col_x[li]
        parts.append(
            f'<text x="{cx + nw/2:.0f}" y="30" text-anchor="middle" '
            f'class="pw-title">{esc(title)}</text>'
        )
        for i, (lines, tag) in enumerate(nodes):
            y = positions[li][i][1]
            parts.append(
                f'<rect x="{cx:.0f}" y="{y:.0f}" width="{nw}" height="{nh}" rx="9" '
                f'fill="{color}" stroke="#c2ccd1" stroke-width="1"/>'
            )
            if len(lines) == 1:
                parts.append(
                    f'<text x="{cx+nw/2:.0f}" y="{y+nh/2-2:.0f}" text-anchor="middle" '
                    f'class="pw-node">{esc(lines[0])}</text>'
                )
            else:
                parts.append(
                    f'<text x="{cx+nw/2:.0f}" y="{y+20:.0f}" text-anchor="middle" '
                    f'class="pw-node">{esc(lines[0])}</text>'
                )
                parts.append(
                    f'<text x="{cx+nw/2:.0f}" y="{y+36:.0f}" text-anchor="middle" '
                    f'class="pw-node">{esc(lines[1])}</text>'
                )
            ecol = EVIDENCE.get(tag, "#8b96a0")
            parts.append(
                f'<text x="{cx+nw/2:.0f}" y="{y+nh-9:.0f}" text-anchor="middle" '
                f'class="pw-tag" fill="{ecol}">{esc(tag)}</text>'
            )

    parts.append("</svg>")
    return "".join(parts)


# ---------------------------------------------------------------------------
# chart 3 — bridge actor shortlist (chips)
# ---------------------------------------------------------------------------

def build_bridge_chips(limit: int = 14) -> str:
    rows = read_csv(EXPL / "actor_issue_bridge_nodes.csv")
    rows = [r for r in rows if int(r["issue_count"]) >= 2]
    rows.sort(key=lambda r: (-int(r["issue_count"]), r["actor_id"]))
    rows = rows[:limit]

    items = ""
    for r in rows:
        origin = r["origin_type"]
        ocol = ORIGIN_COLOR.get(origin, "#888")
        chips = "".join(
            f'<span class="issue-chip" style="background:{ISSUE_COLOR.get(x, "#889")}22;'
            f'color:{ISSUE_COLOR.get(x, "#556")};border-color:{ISSUE_COLOR.get(x, "#889")}55">'
            f'{esc(x)}</span>'
            for x in r["issues"].split(";")
        )
        ev = r["evidence_level"]
        items += f"""
    <li class="bridge-row">
      <span class="bridge-dot" style="background:{ocol}" title="{esc(ORIGIN_LABEL.get(origin, origin))}"></span>
      <span class="bridge-id">{esc(r['actor_id'])}</span>
      <span class="bridge-name">{esc(r['canonical_name'])}</span>
      <span class="bridge-issues">{chips}</span>
      <span class="ev-badge" style="background:{EVIDENCE.get(ev, '#888')}">{esc(ev)}</span>
    </li>"""

    origins_present = []
    seen = set()
    for r in rows:
        o = r["origin_type"]
        if o not in seen:
            seen.add(o)
            origins_present.append(o)
    legend = "".join(
        f'<span class="olg"><i style="background:{ORIGIN_COLOR.get(o, "#888")}"></i>'
        f'{esc(ORIGIN_LABEL.get(o, o))}</span>'
        for o in origins_present
    )
    return f"""
<ul class="bridge-list">{items}
</ul>
<div class="bridge-legend">{legend}
  <span class="olg olg-note">左侧圆点＝组织来源类型 · 右侧徽章＝证据等级</span>
</div>
"""


# ---------------------------------------------------------------------------
# chart 4 — co-action sample composition (CSS stacked bars)
# ---------------------------------------------------------------------------

COACTION_EVENTS = [
    ("2010 WWF 共同要请", "S003", 67),
    ("2015 NACSJ 共同声明", "S004", 31),
    ("2020 OEJP/MMC 71 团体", "S006", 71),
]
COACTION_ORIGINS = [
    "okinawa_local", "japan_domestic", "international",
    "us_origin", "mixed_or_network", "unclear",
]


def build_coaction_bars() -> str:
    rows = read_csv(EXPL / "coaction_sample_composition.csv")
    by_event: dict[str, dict[str, int]] = defaultdict(dict)
    for r in rows:
        if r["origin_type"] == "actor_ids":
            continue
        by_event[r["source_id"]][r["origin_type"]] = int(r["count"])

    max_total = 0
    for _label, sid, _orig in COACTION_EVENTS:
        max_total = max(max_total, sum(by_event.get(sid, {}).values()))
    max_total = max(max_total, 1)

    bars = ""
    for label, sid, original in COACTION_EVENTS:
        comp = by_event.get(sid, {})
        total = sum(comp.values())
        segs = ""
        for o in COACTION_ORIGINS:
            v = comp.get(o, 0)
            if v <= 0:
                continue
            w = v / max_total * 100
            segs += (
                f'<span class="cbar-seg" style="width:{w:.1f}%;background:{ORIGIN_COLOR[o]}" '
                f'title="{esc(ORIGIN_LABEL.get(o, o))}: {v}"></span>'
            )
        bars += f"""
    <div class="cbar-block">
      <div class="cbar-label">{esc(label)}</div>
      <div class="cbar-track">{segs}</div>
      <div class="cbar-meta">原文署名 <b>{original}</b> 团体 · 当前录入 registry <b>{total}</b></div>
    </div>"""

    legend = "".join(
        f'<span class="olg"><i style="background:{ORIGIN_COLOR[o]}"></i>{esc(ORIGIN_LABEL.get(o, o))}</span>'
        for o in COACTION_ORIGINS
    )
    return f"""
<div class="cbar-wrap">{bars}
</div>
<div class="bridge-legend">{legend}</div>
"""


# ---------------------------------------------------------------------------
# roadmap + LR tables
# ---------------------------------------------------------------------------

def build_roadmap_table(m: dict[str, int]) -> str:
    rows = [
        ("MT-001", "R5 / R11", "P1", "抽取完成 · 待审入",
         f"2020 MMC 71 团体已抽全，产出 {m['candidates']} 个 registry 扩展候选，逐条 add/defer/exclude。",
         "线上决策 · 低"),
        ("MT-003", "R14 / R3", "P1", "进行中",
         f"剩余 {m['inferred']} 条 inferred_url 占位来源核实归档（先岛 / 法院 / 地方新闻为主）。",
         "线上核实 · 低"),
        ("MT-004", "R3 / R4", "P1", "待启动",
         "与那国 A014/A015 地方证据包：地方报纸、意见广告实物、议会 / 住民投票资料。",
         "需当地 / 馆内 · 高"),
        ("MT-005", "R8 / R14", "P2", "待启动",
         "AWWA / 军属配偶俱乐部慈善 recipient 网络：按年份、来源、证据等级建 recipient 边。",
         "线上为主 · 中"),
        ("MT-006", "R8", "P2", "待启动",
         "ONC / JICA / 外务省 关系链：区分行政协作与抗争网络，找合同 / 项目 / 报告证据。",
         "线上为主 · 中"),
        ("MT-007", "R10 / R11", "P2", "待启动",
         "儒艮诉讼原告映射：把 plaintiff / support actor 对应到有来源支撑的法律角色。",
         "线上核实 · 中"),
        ("MT-008", "R2 / R5", "P2", "待启动",
         "关系边加 event_id / action_type / relation_strength，把静态议题标签变成事件感知网络。",
         "数据加工 · 中"),
    ]
    body = ""
    for tid, mod, pr, status, what, cost in rows:
        prcls = "pri-p1" if pr == "P1" else "pri-p2"
        body += f"""
    <tr>
      <td class="mono">{esc(tid)}</td>
      <td class="mono dim">{esc(mod)}</td>
      <td><span class="pill {prcls}">{esc(pr)}</span></td>
      <td>{esc(status)}</td>
      <td class="lead">{esc(what)}</td>
      <td class="dim nowrap">{esc(cost)}</td>
    </tr>"""
    return f"""
<table class="grid-table">
  <thead><tr>
    <th>任务</th><th>模块</th><th>优先</th><th>状态</th><th>做什么 / 为什么现在更清晰</th><th>路径 · 成本</th>
  </tr></thead>
  <tbody>{body}
  </tbody>
</table>
"""


LR_TIER1 = [
    ("LR-003", "军属配偶俱乐部慈善 recipient", "X004 AWWA / X005 NOSCO / X006 KOSC / X007 OESC",
     "官网、Facebook / Instagram 公共页、基地社区报（Stripes / DVIDS）公开 recipient 与活动手册。"),
    ("LR-004", "USO Okinawa 赞助与服务网络", "X001 USO Okinawa / X002 Phoenix / X003 AEC",
     "USO 官网、USO Pacific 新闻、本地 sponsor 公司公开页；建 sponsor 边与 site-presence 表。"),
    ("LR-008", "失效网站 Web Archive 回捞", "A002 SDCC / A008 非戦ネット / A019 反対協 等",
     "Internet Archive 抓取旧官网 / 声明页，登记 archived_url + capture_date，评估能否升到 E3。"),
    ("LR-001*", "冲绳本地 NPO 法人公开报告（线上部分）", "A003 / A012 / A017 / X010 ONC",
     "内阁府 NPO 法人 portal 与组织官网可下载的事業報告書 / 財務諸表，先取线上可得部分。"),
    ("LR-006*", "外务省 / JICA / ONC 已公开报告（线上部分）", "X010 ONC / X011 JICA 沖縄",
     "外务省 NGO 相談員页面、JICA Okinawa、ONC 公开年报中已发布的协作 / 项目记载。"),
]
LR_TIER2 = [
    ("LR-002", "与那国早期反部署组织", "A014 / A015 / A016",
     "地方新闻原文、町议会记录、住民投票资料、意见广告实物 —— 需县立图书馆 / 馆内数据库或当地保存材料。"),
    ("LR-007", "先岛 / 边野古核心组织报刊数据库", "A010 / A011 / A012 / A013 / A019",
     "沖縄タイムス / 琉球新報馆内数据库时间线、代表人物、名称变化 —— 需馆内数据库权限。"),
    ("LR-005", "美领馆 / 公共外交 recipient（需谨慎）", "X012 TOMODACHI / X013 Consulate Youth",
     "只有 award / recipient 才写入；仅 NOFO / grant opportunity 标 no_public_evidence，不得写成已资助。"),
]


def build_lr_tables() -> str:
    def render(rows: list[tuple[str, str, str, str]], cls: str) -> str:
        body = ""
        for tid, name, targets, how in rows:
            body += f"""
    <tr>
      <td class="mono {cls}">{esc(tid)}</td>
      <td class="lead"><b>{esc(name)}</b><br><span class="dim mono small">{esc(targets)}</span></td>
      <td>{esc(how)}</td>
    </tr>"""
        return body

    return f"""
<div class="lr-block">
  <h4 class="lr-h lr-h-go">Tier 1 · 本轮锁定 · 线上可完成 · 高价值低成本（可随沟通稿一并交付）</h4>
  <table class="grid-table">
    <thead><tr><th>任务</th><th>对象</th><th>公开可得材料 / 做法</th></tr></thead>
    <tbody>{render(LR_TIER1, "go")}
    </tbody>
  </table>
  <p class="readnote">标注 <span class="mono">*</span> 的任务只承诺其“线上可得”部分；需要现场 / 纸质 / 馆内数据库的深层材料留在 Tier 2。</p>
</div>
<div class="lr-block">
  <h4 class="lr-h lr-h-hold">Tier 2 · 需当地协作者 / 馆内数据库 · 后续正式派单（本轮不承诺时间）</h4>
  <table class="grid-table">
    <thead><tr><th>任务</th><th>对象</th><th>为什么需要当地 / 谨慎</th></tr></thead>
    <tbody>{render(LR_TIER2, "hold")}
    </tbody>
  </table>
</div>
"""


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

CSS = f"""
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{
  margin: 0; background: {PAGE}; color: {BODY};
  font-family: -apple-system, "Segoe UI", "Microsoft YaHei", "Yu Gothic UI",
    Meiryo, "Noto Sans CJK SC", sans-serif;
  font-size: 15px; line-height: 1.7; -webkit-font-smoothing: antialiased;
}}
a {{ color: {BRAND}; text-decoration: none; }}
.wrap {{ max-width: 1080px; margin: 0 auto; padding: 0 26px 90px; }}

/* top bar */
.topbar {{
  position: sticky; top: 0; z-index: 20; background: rgba(255,255,255,0.92);
  backdrop-filter: blur(8px); border-bottom: 1px solid {LINE};
}}
.topbar .inner {{ max-width: 1080px; margin: 0 auto; padding: 11px 26px;
  display: flex; align-items: center; gap: 18px; flex-wrap: wrap; }}
.topbar .brand {{ font-weight: 700; color: {INK}; letter-spacing: .2px; }}
.topbar nav {{ display: flex; gap: 16px; flex-wrap: wrap; margin-left: auto; }}
.topbar nav a {{ color: {MUTED}; font-size: 13.5px; }}
.topbar nav a:hover {{ color: {BRAND}; }}

/* hero */
.hero {{ padding: 54px 0 30px; border-bottom: 1px solid {LINE}; }}
.hero .tag {{ display:inline-block; background:{BRAND_SOFT}; color:{BRAND};
  font-size:12.5px; font-weight:600; padding:4px 12px; border-radius:999px;
  letter-spacing:.4px; }}
.hero h1 {{ color:{INK}; font-size:30px; line-height:1.3; margin:16px 0 10px;
  letter-spacing:.3px; }}
.hero .sub {{ font-size:16px; color:{BODY}; max-width:760px; }}
.hero .meta {{ margin-top:16px; color:{MUTED}; font-size:13.5px; }}

/* sections */
section {{ padding: 40px 0 8px; scroll-margin-top: 64px; }}
.kicker {{ color:{BRAND}; font-size:12.5px; font-weight:700; letter-spacing:1.4px;
  text-transform: uppercase; margin-bottom:8px; }}
h2 {{ color:{INK}; font-size:22px; margin:2px 0 6px; letter-spacing:.3px; }}
h3 {{ color:{INK}; font-size:16.5px; margin:26px 0 4px; }}
.section-lead {{ color:{BODY}; max-width:820px; margin:6px 0 20px; }}
p {{ margin: 10px 0; }}

/* metric cards */
.metrics {{ display:grid; grid-template-columns: repeat(4,1fr); gap:14px; margin:14px 0 6px; }}
.metric {{ background:{PANEL}; border:1px solid {LINE}; border-radius:14px;
  padding:16px 18px; box-shadow:0 1px 2px rgba(30,50,60,.04); }}
.metric .num {{ font-size:27px; font-weight:700; color:{BRAND}; letter-spacing:.4px; }}
.metric .lab {{ font-size:13px; color:{MUTED}; margin-top:2px; }}
.metric .sub {{ font-size:12px; color:{MUTED}; margin-top:6px; border-top:1px dashed {LINE};
  padding-top:6px; }}

/* value cards */
.vgrid {{ display:grid; grid-template-columns: repeat(3,1fr); gap:16px; margin-top:10px; }}
.vcard {{ background:{PANEL}; border:1px solid {LINE}; border-radius:14px; padding:20px;
  box-shadow:0 1px 2px rgba(30,50,60,.04); }}
.vcard .n {{ display:inline-flex; width:28px; height:28px; border-radius:8px;
  background:{BRAND_SOFT}; color:{BRAND}; font-weight:700; align-items:center;
  justify-content:center; font-size:14px; }}
.vcard h4 {{ color:{INK}; font-size:15.5px; margin:12px 0 6px; }}
.vcard p {{ font-size:14px; margin:0; color:{BODY}; }}

/* plan alignment strip */
.plan {{ display:grid; grid-template-columns: repeat(4,1fr); gap:12px; margin-top:18px; }}
.pstep {{ border:1px solid {LINE}; border-radius:12px; padding:14px 16px; background:{PANEL}; }}
.pstep .ph {{ font-weight:700; color:{INK}; }}
.pstep .st {{ font-size:12.5px; font-weight:700; padding:2px 9px; border-radius:999px;
  display:inline-block; margin-top:8px; }}
.st-done {{ background:#e7f1ea; color:#3a6b4d; }}
.st-prog {{ background:#fdf1dc; color:#9a6a1c; }}
.pstep p {{ font-size:13px; color:{MUTED}; margin:8px 0 0; }}

/* figure card */
.figure {{ background:{PANEL}; border:1px solid {LINE}; border-radius:16px;
  padding:24px 26px 20px; margin:18px 0; box-shadow:0 2px 10px rgba(30,50,60,.05); }}
.figure .fig-h {{ color:{INK}; font-weight:700; font-size:16px; }}
.figure .fig-sub {{ color:{MUTED}; font-size:13px; margin:2px 0 16px; }}
.readnote {{ font-size:12.8px; color:{MUTED}; margin:14px 0 0; padding:10px 14px;
  background:#f8fafb; border-left:3px solid #c9d5da; border-radius:0 8px 8px 0; }}
.readnote b {{ color:{BODY}; }}

/* heatmap */
.hm-wrap {{ display:flex; gap:26px; flex-wrap:wrap; align-items:flex-start; }}
.hm-grid {{ display:grid; grid-template-columns: 180px repeat(7, 1fr);
  gap:4px; flex:1 1 560px; min-width:520px; }}
.hm-cell {{ height:38px; display:flex; align-items:center; justify-content:center;
  font-size:13px; border-radius:6px; }}
.hm-corner {{ background:transparent; }}
.hm-head {{ background:{BRAND_SOFT}; color:{BRAND}; font-weight:700; }}
.hm-row {{ justify-content:flex-end; padding-right:10px; color:{INK}; font-weight:600;
  font-size:12.5px; text-align:right; }}
.hm-val {{ font-weight:700; font-variant-numeric:tabular-nums; }}
.frame-key {{ list-style:none; margin:0; padding:0; flex:0 0 210px; font-size:13px; }}
.frame-key li {{ padding:5px 0; color:{BODY}; border-bottom:1px dashed {LINE}; }}
.fk-code {{ display:inline-block; width:30px; font-weight:700; color:{BRAND}; }}
.fk-en {{ color:{MUTED}; font-size:11.5px; }}

/* pathway svg */
.pathway {{ width:100%; height:auto; display:block; }}
.pw-title {{ font-size:13px; font-weight:700; fill:{INK}; }}
.pw-node {{ font-size:11px; fill:{INK}; }}
.pw-tag {{ font-size:10px; font-weight:700; }}

/* bridge list */
.bridge-list {{ list-style:none; margin:6px 0 0; padding:0; }}
.bridge-row {{ display:flex; align-items:center; gap:12px; padding:9px 4px;
  border-bottom:1px solid {LINE}; }}
.bridge-dot {{ width:11px; height:11px; border-radius:50%; flex:0 0 auto; }}
.bridge-id {{ font-family:ui-monospace,Consolas,monospace; font-size:12.5px;
  color:{MUTED}; flex:0 0 46px; }}
.bridge-name {{ color:{INK}; font-weight:600; font-size:13.5px; flex:1 1 200px;
  min-width:150px; }}
.bridge-issues {{ display:flex; gap:5px; flex-wrap:wrap; flex:2 1 300px; }}
.issue-chip {{ font-size:11px; padding:2px 8px; border-radius:999px; border:1px solid;
  white-space:nowrap; }}
.ev-badge {{ color:#fff; font-size:11px; font-weight:700; padding:2px 8px;
  border-radius:6px; flex:0 0 auto; }}
.bridge-legend {{ display:flex; gap:16px; flex-wrap:wrap; margin-top:14px;
  font-size:12.5px; color:{BODY}; align-items:center; }}
.olg {{ display:inline-flex; align-items:center; gap:6px; }}
.olg i {{ width:11px; height:11px; border-radius:3px; display:inline-block; }}
.olg-note {{ color:{MUTED}; margin-left:auto; }}

/* coaction bars */
.cbar-wrap {{ display:flex; flex-direction:column; gap:18px; margin-top:4px; }}
.cbar-label {{ font-weight:700; color:{INK}; font-size:14px; margin-bottom:6px; }}
.cbar-track {{ display:flex; height:26px; border-radius:7px; overflow:hidden;
  background:#eef2f4; }}
.cbar-seg {{ height:100%; }}
.cbar-meta {{ font-size:12.5px; color:{MUTED}; margin-top:5px; }}
.cbar-meta b {{ color:{BODY}; }}

/* tables */
.grid-table {{ width:100%; border-collapse:collapse; margin:8px 0; font-size:13.5px;
  background:{PANEL}; border:1px solid {LINE}; border-radius:12px; overflow:hidden; }}
.grid-table th {{ background:#f4f7f8; color:{INK}; text-align:left; font-weight:700;
  padding:11px 13px; font-size:12.5px; border-bottom:1px solid {LINE}; }}
.grid-table td {{ padding:11px 13px; border-bottom:1px solid {LINE}; vertical-align:top;
  color:{BODY}; }}
.grid-table tr:last-child td {{ border-bottom:none; }}
.grid-table .lead {{ color:{INK}; }}
.mono {{ font-family:ui-monospace,Consolas,monospace; font-size:12.5px; }}
.mono.go {{ color:#3a6b4d; font-weight:700; }}
.mono.hold {{ color:#9a6a1c; font-weight:700; }}
.small {{ font-size:11.5px; }}
.dim {{ color:{MUTED}; }}
.nowrap {{ white-space:nowrap; }}
.pill {{ font-size:11.5px; font-weight:700; padding:2px 9px; border-radius:999px; }}
.pri-p1 {{ background:#e9f0f4; color:{BRAND}; }}
.pri-p2 {{ background:#f1f0f4; color:#6a5f8f; }}
.lr-block {{ margin:18px 0; }}
.lr-h {{ font-size:14px; margin:0 0 8px; padding:8px 14px; border-radius:9px; }}
.lr-h-go {{ background:#e7f1ea; color:#356048; }}
.lr-h-hold {{ background:#fbf0dc; color:#8a611c; }}

/* caveats */
.caveats {{ display:grid; grid-template-columns: repeat(2,1fr); gap:14px; margin-top:8px; }}
.cav {{ background:{PANEL}; border:1px solid {LINE}; border-left:4px solid #c98e56;
  border-radius:10px; padding:14px 16px; }}
.cav b {{ color:{INK}; }}
.cav p {{ margin:4px 0 0; font-size:13.5px; }}

footer {{ margin-top:40px; padding-top:22px; border-top:1px solid {LINE};
  color:{MUTED}; font-size:12.5px; }}

@media (max-width: 860px) {{
  .metrics, .vgrid, .plan, .caveats {{ grid-template-columns: 1fr 1fr; }}
  .hm-grid {{ grid-template-columns: 120px repeat(7,1fr); min-width:0; }}
}}
@media print {{
  .topbar {{ position:static; }}
  body {{ background:#fff; }}
  .figure, .metric, .vcard {{ box-shadow:none; }}
}}
"""


# ---------------------------------------------------------------------------
# page assembly
# ---------------------------------------------------------------------------

def build_html(m: dict[str, int]) -> str:
    metrics = f"""
<div class="metrics">
  <div class="metric"><div class="num">{m['actors']}</div><div class="lab">actor 登记</div>
    <div class="sub">首轮 HR 复核 · 保留 P1/P2/P3 复核优先级</div></div>
  <div class="metric"><div class="num">{m['sources']}</div><div class="lab">信息源</div>
    <div class="sub">{m['real_url']} 真实 URL · {m['inferred']} 占位待核 · {m['non_url']} 非 URL</div></div>
  <div class="metric"><div class="num">{m['issue_edges']}+{m['place_edges']}+{m['funding']}</div>
    <div class="lab">候选关系边</div>
    <div class="sub">议题 {m['issue_edges']} · 地点 {m['place_edges']} · 资助样本 {m['funding']}（均为候选）</div></div>
  <div class="metric"><div class="num">{m['local_archived']}/{m['real_url']}</div><div class="lab">HTTP 来源本地归档</div>
    <div class="sub">{m['archived']} archived + {m['manual_archived']} manual · {m['failed']} access failed</div></div>
</div>
<div class="metrics" style="margin-top:14px">
  <div class="metric"><div class="num">5</div><div class="lab">R 模块 v0 交付</div>
    <div class="sub">R2 · R3/R4 · R5 · R11 · R14</div></div>
  <div class="metric"><div class="num">{m['issues']} / {m['places']}</div><div class="lab">议题 / 地点节点</div>
    <div class="sub">一级议题 {m['issues']} · 地点 / 场域 {m['places']}</div></div>
  <div class="metric"><div class="num">71</div><div class="lab">2020 MMC 团体已抽全</div>
    <div class="sub">产出 {m['candidates']} 个 registry 扩展候选</div></div>
  <div class="metric"><div class="num">3</div><div class="lab">MT 具体产出</div>
    <div class="sub">MT-001 抽取 · MT-002 归档 · MT-003 首轮 URL 核实</div></div>
</div>
"""

    value_cards = """
<div class="vgrid">
  <div class="vcard"><span class="n">1</span>
    <h4>方向是自然的，不是硬凑的</h4>
    <p>一期不追"复归以来全量 NGO 网络"这种不可复核的目标，而是问一个可核对的小问题：民间组织如何把基地问题<b>转译</b>为环保、生活安全、地方自治、人权、法律程序、国际倡议等框架，并在边野古、与那国、先岛等场域扮演什么公开角色。这正是这些组织在公开材料里<b>自己使用</b>的话语方式。</p></div>
  <div class="vcard"><span class="n">2</span>
    <h4>方法本身会不断产出下一步方向</h4>
    <p>每一轮不仅出结论，还出"下一步查什么、缺什么材料"：证据分级（E1–E4）、人工复核（HR）、来源本地归档（防链接失效）、覆盖 / 偏差审计（R14）把边界写明。于是可调查方向越滚越清晰——本轮就析出了 52 个 MMC 候选、14 条待核 URL、与那国证据包、军属慈善 recipient、ONC/JICA/外务省关系链。</p></div>
  <div class="vcard"><span class="n">3</span>
    <h4>守住保守口径，可对外可复核</h4>
    <p>候选边不当结论、共同署名不写联盟、grant opportunity 不写拨款、军属服务组织按功能编码、与那国按前线 / 自治 / 生命安全读取。这些护栏让每一条能对外的表述都<b>可追溯到一手来源</b>，减少解释和政治风险。</p></div>
</div>
"""

    plan_strip = """
<h3>是否符合一开始的规划</h3>
<p class="section-lead">符合。当前进展落在既定的 A→B→C→D 四阶段上，偏差都是"更保守"而非"跑偏"：把候选关系保留为候选、不夸大资助与联盟。</p>
<div class="plan">
  <div class="pstep"><div class="ph">阶段 A</div><div class="st st-done">已完成</div>
    <p>主问题、actor 边界、证据分级、编码规则、工作台。</p></div>
  <div class="pstep"><div class="ph">阶段 B</div><div class="st st-done">已完成并扩充</div>
    <p>样本与 registry：93 actor、180+124+27 边、19 议题、20 地点。</p></div>
  <div class="pstep"><div class="ph">阶段 C</div><div class="st st-prog">首轮完成 · 持续</div>
    <p>HR-001~009 复核、来源归档首轮、inferred_url 核实进行中。</p></div>
  <div class="pstep"><div class="ph">阶段 D</div><div class="st st-prog">进行中</div>
    <p>R2/R3-4/R5/R11/R14 已有可解释 v0 交付；本沟通包即为其成果。</p></div>
</div>
"""

    fig1 = f"""
<div class="figure" id="fig1">
  <div class="fig-h">图 1 · 地点 × 议题框架矩阵</div>
  <div class="fig-sub">数字＝同时连接该地点与该议题框架的 actor 数（E2 及以上）。深色越强表示该场域越集中。</div>
  {build_place_matrix()}
  {caveat_note('<b>读法：</b>边野古 / 大浦湾集中承接环保 + 反基地 + 国际路径；石垣 / 宫古偏生活安全、地下水、住民投票；<b>与那国按前线 / 台湾、地方自治、住民投票读取，不强行环保化。</b>矩阵反映公开资料驱动的覆盖，不代表冲绳全量组织生态。')}
</div>
"""

    fig2 = f"""
<div class="figure" id="fig2">
  <div class="fig-h">图 2 · 边野古 / 大浦湾：地方基地争议如何被转译为国际倡议</div>
  <div class="fig-sub">五层路径：地方现场 → 地方 actor → 日本 NGO / 法律 → 转译框架 → 国际路径。方框内标注证据等级。</div>
  {build_pathway_svg()}
  {caveat_note('<b>读法：这是路径图，不是资金链，也不是稳定联盟图。</b>共同署名只表示共同发声；Earthjustice / MMC 路径不写成"外部操控"或资助关系；A002 SDCC 不写成美国诉讼原告。')}
</div>
"""

    fig3 = f"""
<div class="figure" id="fig3">
  <div class="fig-h">图 3 · 跨议题桥接组织清单（Top 14）</div>
  <div class="fig-sub">这些组织在公开资料中同时连接 2 个及以上重点议题，是"把基地问题接到环保 / 自治 / 法律 / 国际倡议"的桥接点。</div>
  {build_bridge_chips()}
  {caveat_note('桥接 actor 大致分三类：本地运动 / 法律节点、日本国内 NGO / 倡议节点、海外签名 / 国际倡议节点。此图只说明"公开资料中的议题连接"，<b>不代表组织长期主打议题，也不能把共同署名写成稳定联盟；</b>多数条目仍为 <span class="mono">ai_seeded</span>，需继续补证。')}
</div>
"""

    fig4 = f"""
<div class="figure" id="fig4">
  <div class="fig-h">图 4 · 共同行动样本构成（2010 / 2015 / 2020）</div>
  <div class="fig-sub">三次共同署名 / 共同要请样本中，<b>当前已录入 registry</b> 的参与组织按来源类型构成。</div>
  {build_coaction_bars()}
  {caveat_note('<b>注意：色条统计的是当前 registry 中带对应 source_id 的 actor，不是声明原文全量署名数。</b>2020 MMC 71 团体已完整抽取，但多数尚未审入 registry（故当前录入数小）——这正是 MT-001 的下一步：从 52 个候选逐条决定 add / defer / exclude。')}
</div>
"""

    caveats = """
<div class="caveats">
  <div class="cav"><b>共同署名 ≠ 稳定联盟</b>
    <p>共同署名、共同请求、共同在场只写为"事件参与"，进入联盟网络前须先区分一次性署名、重复发声与长期协作。</p></div>
  <div class="cav"><b>grant opportunity ≠ 已拨款</b>
    <p>没有官方 grant / award / contract / 财报 / 项目报告，不写成资金链；仅有 NOFO 标 <span class="mono">no_public_evidence</span>。</p></div>
  <div class="cav"><b>服务型组织按功能编码</b>
    <p>美军军属服务 / 慈善组织不默认为亲基地或反基地，按观察到的功能编码。</p></div>
  <div class="cav"><b>候选边不是最终结论</b>
    <p>issue / place / funding 边均为候选关系；敏感关系须人工复核，不做 AI 写 AI 审。</p></div>
</div>
<p class="readnote">旧的 <span class="mono">docs/progress_report_v1.md</span> 是内部草稿，不作为本次对外交付；本沟通包（formal_comm_v0）才是第二轮对外沟通材料。</p>
"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>冲绳民间组织网络研究 · 第二轮进度沟通</title>
<style>{CSS}</style>
</head>
<body>
<div class="topbar"><div class="inner">
  <span class="brand">冲绳民间组织网络研究 · Phase 1</span>
  <nav>
    <a href="#overview">进度总览</a>
    <a href="#value">价值与方向</a>
    <a href="#figures">正式图表</a>
    <a href="#roadmap">调查路线图</a>
    <a href="#lr">当地材料</a>
    <a href="#caveats">风险边界</a>
  </nav>
</div></div>

<div class="wrap">

<header class="hero">
  <span class="tag">第二轮对外沟通 · v0</span>
  <h1>冲绳民间组织 / NGO 如何把基地问题<br>转译为环保、安全、自治、法律与国际倡议</h1>
  <p class="sub">本轮从"统计更新"进到"可解释机制 + 下一轮调查路线"。R2、R3/R4、R5、R11、R14 五个模块已有可解释 v0 交付；MT-001 抽取、MT-002 归档、MT-003 首轮 URL 核实是最具体的完工产出。</p>
  <div class="meta">更新时间 {REPORT_DATE} · 范围：边野古 / 大浦湾 · 与那国 · 先岛 · 相关国际倡议场域 · 全部口径保守、可复核</div>
</header>

<section id="overview">
  {kicker("一页进度总览")}
  <h2>当前底盘与本轮完工产出</h2>
  <p class="section-lead">数字来自当前数据表实时统计。所有关系边均为<b>候选</b>，用于分析与继续补证，不作为最终结论。</p>
  {metrics}
</section>

<section id="value">
  {kicker("为什么做这些方向")}
  <h2>价值：一个能不断"生出下一个调查方向"的方法</h2>
  <p class="section-lead">甲方关心的是"这条线值不值得继续、下一步查什么更清楚"。本项目的核心价值就在这里——它是自证式、可累积的。</p>
  {value_cards}
  {plan_strip}
</section>

<section id="figures">
  {kicker("正式图表集")}
  <h2>四张主图（网页原生 · 缩放不糊）</h2>
  <p class="section-lead">全部图表由项目 CSV 实时生成，随数据更新。图注保持保守口径。</p>
  {fig1}
  {fig2}
  {fig3}
  {fig4}
</section>

<section id="roadmap">
  {kicker("调查路线图")}
  <h2>下一轮为什么更清晰：MT-001 ~ MT-008</h2>
  <p class="section-lead">这些不是"卡住的前置任务"，而是本轮成果<b>析出的</b>可执行方向，按优先级与成本排列。</p>
  {build_roadmap_table(m)}
</section>

<section id="lr">
  {kicker("当地材料收集 · LR v1")}
  <h2>先锁定"高价值 · 低成本 · 可立即执行"的部分</h2>
  <p class="section-lead">把当地材料任务分成两层：线上可完成的先锁定、随本沟通稿一并交付；真正需要当地协作者 / 馆内数据库的留作后续正式派单。详见 <span class="mono">docs/local_retrieval_tasks_v1.md</span>。</p>
  {build_lr_tables()}
</section>

<section id="caveats">
  {kicker("风险与解释边界")}
  <h2>对外时必须守住的四条线</h2>
  {caveats}
</section>

<footer>
  冲绳 NGO / 民间组织网络研究 · Phase 1 · 第二轮对外沟通包（formal_comm_v0）· 生成日期 {REPORT_DATE}<br>
  数据来源：data/interim 各表 · outputs/explanatory_v0 · outputs/module_completion_v0 · source_docs/source_archive。本页可离线打开、可打印。
</footer>

</div>
</body>
</html>
"""


README = f"""# 第二次进度同步包 formal_comm_v0

日期：{REPORT_DATE}

本目录是面向甲方的第二次进度同步材料，文风对齐第一次同步（简洁、保守、图表截图嵌入）。

## 对外交付物（发飞书云文档用）

- `第二次进度同步_v0.md` — **主交付物**，手写的简洁进度稿。结构：本轮进展、研究模块菜单进度、
  是否符合七周工期、核心图表、人工复核与口径、下一步。图片用相对路径引用 `fig/` 下的截图。

## 图源（由脚本生成，用于截图嵌入 MD）

- `fig/fig1_place_issue.png` — 地点 × 议题框架矩阵（R3 / R4）
- `fig/fig2_pathway.png` — 边野古 / 大浦湾国际化路径（R6 / R11）
- `fig/fig3_bridge.png` — 跨议题桥接组织 Top 14（R2）
- `fig/fig4_coaction.png` — 共同行动样本构成 2010 / 2015 / 2020（R5）
- `index.html` — 四张图合成的单页网页预览（内部用，非对外文风）。
- `fig/*.html` — 单图页，供导出上面的 PNG。

## 生成图表

```powershell
python scripts\\make_formal_comm_package.py
```

脚本读取 `data/interim` 各表、`outputs/explanatory_v0` 的矩阵 / 桥接 / 共同行动 CSV、
`source_docs/source_archive` 归档 manifest 与 2020 MMC 候选表，因此图表数字始终反映当前数据。
数据更新后重跑脚本，再用无头浏览器重截 `fig/*.png` 即可刷新。

## 口径

全部保守：候选关系不当结论、共同署名不写联盟、grant opportunity 不写拨款、
军属服务组织按功能编码、与那国按前线 / 自治 / 生命安全读取。旧的
`docs/progress_report_v1.md` 是内部草稿，不作为本次对外交付。
"""


def _fig_page(title: str, sub: str, body: str) -> str:
    return (
        "<!DOCTYPE html><html lang='zh-CN'><head><meta charset='utf-8'>"
        f"<style>{CSS}</style></head><body style='background:#eef1f3'>"
        "<div style='max-width:940px;padding:18px'>"
        "<div class='figure' style='margin:0'>"
        f"<div class='fig-h'>{title}</div>"
        f"<div class='fig-sub'>{sub}</div>{body}</div></div></body></html>"
    )


def write_figure_pages() -> None:
    """Standalone one-figure pages, for exporting clean PNG screenshots into MD."""
    figdir = OUT / "fig"
    figdir.mkdir(parents=True, exist_ok=True)
    pages = {
        "fig1_place_issue": (
            "地点 × 议题框架矩阵",
            "数字＝同时连接该地点与该议题框架的组织数（E2 及以上）；深色越强表示越集中。",
            build_place_matrix(),
        ),
        "fig2_pathway": (
            "边野古 / 大浦湾：地方基地争议如何被转译为国际倡议",
            "五层路径：地方现场 → 地方组织 → 日本 NGO / 法律 → 转译框架 → 国际路径；标注证据等级。",
            build_pathway_svg(),
        ),
        "fig3_bridge": (
            "跨议题桥接组织（Top 14）",
            "在公开资料中同时连接 2 个及以上重点议题的组织。",
            build_bridge_chips(),
        ),
        "fig4_coaction": (
            "共同行动样本构成（2010 / 2015 / 2020）",
            "三次共同署名 / 共同要请样本中，当前已录入 registry 的参与组织按来源类型构成。",
            build_coaction_bars(),
        ),
    }
    for key, (title, sub, body) in pages.items():
        (figdir / f"{key}.html").write_text(_fig_page(title, sub, body), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    m = load_metrics()
    (OUT / "index.html").write_text(build_html(m), encoding="utf-8")
    (OUT / "README.md").write_text(README, encoding="utf-8")
    write_figure_pages()
    print(f"Wrote formal communication package to {OUT.relative_to(ROOT)}")
    print(f"  actors={m['actors']} sources={m['sources']} "
          f"real_url={m['real_url']} candidates={m['candidates']}")


if __name__ == "__main__":
    main()
