"""Build the Phase-1 coverage-bias audit and explanatory figure.

The audit is descriptive of the current public-material-driven working sample.
It never treats registry/source counts as estimates of a population.
"""

from __future__ import annotations

import csv
import html
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
OUT = ROOT / "outputs" / "coverage_audit_v1"

ACTORS = DATA / "01_actor_registry_initial_v0.csv"
SOURCES = DATA / "05_source_log_initial_v0.csv"
ACTOR_ISSUES = DATA / "24_r01_r02_actor_issue_layered_v0.csv"
ACTOR_PLACES = DATA / "08_actor_place_edges_initial_v0.csv"
ARCHIVE = ROOT / "source_docs" / "source_archive" / "source_archive_manifest.csv"

CELLS = DATA / "27_coverage_audit_cells_v1.csv"
IMPLICATIONS = OUT / "coverage_bias_implications_v1.csv"
BRIEF = OUT / "coverage_audit_brief_v1.md"
HR023 = OUT / "HR023_status_v0.md"
SVG = OUT / "fig_coverage_bias_core_v1.svg"
HTML = OUT / "fig_coverage_bias_core_v1.html"


CELL_FIELDS = [
    "dimension_id",
    "dimension_label",
    "facet",
    "category",
    "subcategory",
    "count",
    "denominator",
    "share_pct",
    "unit",
    "inclusion_rule",
    "interpretive_limit",
]

IMPLICATION_FIELDS = [
    "dimension_id",
    "dimension_label",
    "observed_skew",
    "visibility_mechanism",
    "impact_on_q1_q3",
    "affected_modules",
    "interpretation_boundary",
    "online_gap_action",
    "local_gap_action",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def pct(count: int, denominator: int) -> str:
    return f"{count / denominator * 100:.1f}" if denominator else "0.0"


def add_cell(
    rows: list[dict[str, str]],
    dimension_id: str,
    dimension_label: str,
    facet: str,
    category: str,
    count: int,
    denominator: int,
    unit: str,
    inclusion_rule: str,
    interpretive_limit: str,
    subcategory: str = "",
) -> None:
    rows.append(
        {
            "dimension_id": dimension_id,
            "dimension_label": dimension_label,
            "facet": facet,
            "category": category,
            "subcategory": subcategory,
            "count": str(count),
            "denominator": str(denominator),
            "share_pct": pct(count, denominator),
            "unit": unit,
            "inclusion_rule": inclusion_rule,
            "interpretive_limit": interpretive_limit,
        }
    )


def source_period(year: str) -> str:
    if not year.isdigit():
        return "unknown/undated"
    value = int(year)
    if 1972 <= value <= 1997:
        return "1972-1997"
    if 1998 <= value <= 2012:
        return "1998-2012"
    if 2013 <= value <= 2019:
        return "2013-2019"
    if value >= 2020:
        return "2020-current"
    return "pre-1972/other"


def review_bucket(value: str) -> str:
    if value in {"human_checked", "human_revised"}:
        return "human-reviewed"
    if value == "ai_seeded":
        return "ai-seeded"
    return "follow-up/limited"


def top_categories(counter: Counter[str], keep: int) -> tuple[list[str], set[str]]:
    ordered = sorted(counter, key=lambda item: (-counter[item], item))
    return ordered[:keep], set(ordered[keep:])


def build_cells(
    actors: list[dict[str, str]],
    sources: list[dict[str, str]],
    issues: list[dict[str, str]],
    places: list[dict[str, str]],
    archive: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    public_sample_limit = (
        "Describes the working sample only; no population denominator or overall-distribution estimate."
    )

    # D1 — source-document time, not organizational activity.
    periods = ["1972-1997", "1998-2012", "2013-2019", "2020-current", "unknown/undated"]
    period_counts = Counter(source_period(row["year"]) for row in sources)
    for period in periods:
        add_cell(
            rows, "D1", "时间", "source_year_period", period,
            period_counts[period], len(sources), "source-log records",
            "Source year binned to the Phase-1 plan periods.",
            "Source counts measure documentary visibility, not organization activity. " + public_sample_limit,
        )

    # D2 — exact actor-place pairs; no duplicate pair exists in the current table.
    place_counts = Counter(row["place_name"] for row in places)
    for place in sorted(place_counts, key=lambda item: (-place_counts[item], item)):
        add_cell(
            rows, "D2", "地点", "actor_place_pair", place,
            place_counts[place], len(places), "distinct actor-place observations",
            "Exact place_name values; one row per actor-place pair.",
            "Presence in the table is not frequency or intensity of activity. " + public_sample_limit,
        )

    # D3 — retain exact actor classes and origins rather than recoding functions by judgment.
    for facet, field in (("actor_class", "actor_class"), ("origin_type", "origin_type")):
        counts = Counter(row[field] for row in actors)
        for category in sorted(counts, key=lambda item: (-counts[item], item)):
            add_cell(
                rows, "D3", "actor 功能／来源层", facet, category,
                counts[category], len(actors), "registry actors",
                f"Exact {field} values from the actor registry; no new recoding.",
                "Registry composition reflects discoverability and inclusion choices, not the population of Okinawa civil society."
            )

    # D4 — unique actors per current issue group; shares are non-additive.
    issue_actors: dict[str, set[str]] = defaultdict(set)
    for row in issues:
        issue_actors[row["issue_group"]].add(row["actor_id"])
    for issue_group in sorted(issue_actors, key=lambda item: (-len(issue_actors[item]), item)):
        add_cell(
            rows, "D4", "议题", "unique_actor_by_issue_group", issue_group,
            len(issue_actors[issue_group]), len(actors), "unique registry actors",
            "Distinct actor_id within each existing issue_group.",
            "Actors may appear in multiple groups; percentages do not sum to 100%. Labels are evidence-bounded, not activity volumes."
        )

    # D5 — top exact source types plus a mechanical remainder, crossed with archive status.
    archive_by_id = {row["source_id"]: row["archive_status"] for row in archive}
    type_counts = Counter(row["source_type"] for row in sources)
    top_types, remainder_types = top_categories(type_counts, 7)
    type_rows = top_types + ["other source types"]
    statuses = ["archived", "manual_archived", "failed", "skipped_non_url_reference"]
    cross: Counter[tuple[str, str]] = Counter()
    for row in sources:
        source_type = row["source_type"] if row["source_type"] in top_types else "other source types"
        cross[(source_type, archive_by_id[row["source_id"]])] += 1
    for source_type in type_rows:
        for status in statuses:
            add_cell(
                rows, "D5", "source type／archive", "source_type_x_archive", source_type,
                cross[(source_type, status)], len(sources), "source-log records",
                "Seven most frequent exact source_type values; all remaining exact types mechanically pooled as other.",
                "Archive failure is a capture status, not evidence absence; archived status does not guarantee evidentiary sufficiency.",
                subcategory=status,
            )
    assert sum(type_counts[item] for item in remainder_types) == sum(
        cross[("other source types", status)] for status in statuses
    )

    # D6 — exact evidence/review states plus deterministic display buckets.
    corpora = (("actor_registry", actors), ("actor_issue_observations", issues))
    for corpus_name, corpus in corpora:
        for field, facet in (("evidence_level", "evidence_level"), ("review_status", "review_status_exact")):
            counts = Counter(row[field] for row in corpus)
            for category in sorted(counts, key=lambda item: (-counts[item], item)):
                add_cell(
                    rows, "D6", "review／evidence", f"{corpus_name}_{facet}", category,
                    counts[category], len(corpus), corpus_name,
                    f"Exact {field} values in {corpus_name}.",
                    "Evidence level and review state are different axes; E4 does not itself mean a claim was human accepted."
                )
        review_counts = Counter(review_bucket(row["review_status"]) for row in corpus)
        for category in ("human-reviewed", "ai-seeded", "follow-up/limited"):
            add_cell(
                rows, "D6", "review／evidence", f"{corpus_name}_review_bucket", category,
                review_counts[category], len(corpus), corpus_name,
                "Deterministic display bucket: human_checked/revised; ai_seeded; all remaining follow-up statuses.",
                "Display aggregation only; exact statuses remain in companion rows."
            )
    return rows


def build_implications(cells: list[dict[str, str]]) -> list[dict[str, str]]:
    by_key = {(row["facet"], row["category"], row["subcategory"]): row for row in cells}
    recent = by_key[("source_year_period", "2020-current", "")]
    early = by_key[("source_year_period", "1972-1997", "")]
    henoko = by_key[("actor_place_pair", "Henoko", "")]
    prefecture = by_key[("actor_place_pair", "Okinawa Prefecture", "")]
    local = by_key[("origin_type", "okinawa_local", "")]
    archived = sum(
        int(row["count"]) for row in cells
        if row["facet"] == "source_type_x_archive" and row["subcategory"] in {"archived", "manual_archived"}
    )
    failed = sum(
        int(row["count"]) for row in cells
        if row["facet"] == "source_type_x_archive" and row["subcategory"] == "failed"
    )
    source_total = int(recent["denominator"])
    place_total = int(henoko["denominator"])
    actor_total = int(local["denominator"])
    return [
        {
            "dimension_id": "D1", "dimension_label": "时间",
            "observed_skew": f"2020-current {recent['count']}/{source_total} ({recent['share_pct']}%); 1972-1997 {early['count']}/{source_total} ({early['share_pct']}%).",
            "visibility_mechanism": "Current official and organization pages survive and are searchable; early informal groups and renamed organizations leave thinner web traces.",
            "impact_on_q1_q3": "Q1/Q2 become a present-biased inventory/classification; longitudinal claims about organizational ecology are weakest.",
            "affected_modules": "R1;R5;R6;R7;R8;R10;R11",
            "interpretation_boundary": "Do not read source-year concentration as growth in organizations or mobilization.",
            "online_gap_action": "Search web archives, historical organization histories, court/legal databases and digitized newspaper indexes by former names.",
            "local_gap_action": "Retrieve pre-web newsletters, local newspaper holdings, flyers and organization files for 1972-2012."
        },
        {
            "dimension_id": "D2", "dimension_label": "地点",
            "observed_skew": f"Henoko {henoko['count']} plus Okinawa Prefecture {prefecture['count']} = {int(henoko['count']) + int(prefecture['count'])}/{place_total} actor-place observations.",
            "visibility_mechanism": "Henoko produces durable litigation, statement and NGO records; broad prefecture coding absorbs records without a more precise location.",
            "impact_on_q1_q3": "Q3 and comparisons among Henoko, Futenma, Kadena, Yonaguni, Ishigaki and Miyako are not symmetric.",
            "affected_modules": "R3;R4;R5;R8;R9",
            "interpretation_boundary": "Place counts are observed actor-place pairs, not event frequency, local support or organizational density.",
            "online_gap_action": "Deepen municipal minutes, local official records and place-specific organization/event searches outside Henoko.",
            "local_gap_action": "Prioritize Sakishima and base-adjacent local newspaper archives, council records, referendum materials and physical notices."
        },
        {
            "dimension_id": "D3", "dimension_label": "actor 功能／来源层",
            "observed_skew": f"Okinawa-local actors are {local['count']}/{actor_total} ({local['share_pct']}%); registry visibility is concentrated in citizen networks/groups and web-visible domestic/international NGOs.",
            "visibility_mechanism": "Named, incorporated or networked actors are easier to identify than short-lived committees, informal neighborhood groups and legacy names.",
            "impact_on_q1_q3": "Q1/Q2 and R1 may overstate durable/networked forms; R10/R11 layers are deliberately sampled and cannot be treated as complete sectors.",
            "affected_modules": "R1;R2;R5;R10;R11",
            "interpretation_boundary": f"The {actor_total} actors are a value-driven working registry, not a census or a functional population distribution.",
            "online_gap_action": "Resolve aliases, defunct sites, directories, membership pages and event lists for under-visible functional forms.",
            "local_gap_action": "Verify temporary committees, neighborhood groups, former names, continuity and representatives through local holdings."
        },
        {
            "dimension_id": "D4", "dimension_label": "议题",
            "observed_skew": "Base politics, environment and transnational issue groups have the broadest actor coverage; collective action, external-network and several life-safety subtopics are thinner.",
            "visibility_mechanism": "Project search paths and high-documentation controversies yield more explicit issue labels than diffuse welfare, labor, gender and health work.",
            "impact_on_q1_q3": "Q2 bridge-actor claims and Q3 issue-linkage comparisons may privilege already explicit base/environment/international framing.",
            "affected_modules": "R2;R3;R4;R5;R6;R11",
            "interpretation_boundary": "Issue-tag counts indicate documented association, not issue salience, effort or public support.",
            "online_gap_action": "Target labor, women/human-rights, health, groundwater, noise, welfare and local-autonomy organization records.",
            "local_gap_action": "Use local newsletters, issue campaigns and newspaper databases where organizational issue framing is not indexed online."
        },
        {
            "dimension_id": "D5", "dimension_label": "source type／archive",
            "observed_skew": f"{archived}/{source_total} records are archived/manual archived; {failed}/{source_total} are failed captures. Organization sites and local news are the largest exact source types.",
            "visibility_mechanism": "The sample favors discoverable web pages and official/public records; transient pages and non-indexed local materials are disadvantaged.",
            "impact_on_q1_q3": "All three questions inherit survival, institutional-record and web-search bias; event/relationship modules are especially sensitive.",
            "affected_modules": "R1-R11",
            "interpretation_boundary": "Failed archive does not mean evidence is absent; successful archive does not mean the source proves every coded claim.",
            "online_gap_action": "Retry failed captures, use alternate official URLs/PDFs and manual snapshots, and inspect content sufficiency separately.",
            "local_gap_action": "Retrieve print or database copies only where reasonable online routes are exhausted or the source was never public online."
        },
        {
            "dimension_id": "D6", "dimension_label": "review／evidence",
            "observed_skew": "Most actor and actor-issue rows are E4, while many remain ai_seeded; source grade and human-review status therefore diverge.",
            "visibility_mechanism": "Official/primary records can raise evidence level before actor identity, role boundaries or analytical interpretation receive human review.",
            "impact_on_q1_q3": "Q1 descriptive existence is stronger than Q2 classification and Q3 linkage interpretation; relation-heavy modules require the strictest boundary.",
            "affected_modules": "R1-R11; especially R5-R11",
            "interpretation_boundary": "E4 is not synonymous with human acceptance, stable alliance, funding, causality or political stance.",
            "online_gap_action": "Complete existing review queues and source/claim cross-checks; keep candidate and analytical-seed layers separate.",
            "local_gap_action": "Reserve local verification for identity, continuity, representative and source-text gaps that remain after online review."
        },
    ]


def esc(value: object) -> str:
    return html.escape(str(value))


def bar_rows(items: list[tuple[str, int]], x: int, y: int, width: int, row_h: int = 28) -> str:
    maximum = max((value for _, value in items), default=1)
    output = []
    for index, (label, value) in enumerate(items):
        yy = y + index * row_h
        bar_w = value / maximum * width
        output.append(f'<text x="{x}" y="{yy + 17}" class="lab">{esc(label)}</text>')
        output.append(f'<rect x="{x + 185}" y="{yy + 3}" width="{bar_w:.1f}" height="18" rx="4" class="bar"/>')
        output.append(f'<text x="{x + 195 + bar_w:.1f}" y="{yy + 17}" class="val">{value}</text>')
    return "".join(output)


def panel(x: int, y: int, title: str, subtitle: str, content: str, note: str) -> str:
    return (
        f'<g transform="translate({x},{y})">'
        '<rect width="750" height="390" rx="14" class="panel"/>'
        f'<text x="24" y="36" class="ph">{esc(title)}</text>'
        f'<text x="24" y="60" class="sub">{esc(subtitle)}</text>'
        f'{content}'
        '<rect x="20" y="329" width="710" height="43" rx="8" class="note-bg"/>'
        f'<text x="32" y="347" class="note">{esc(note[:92])}</text>'
        f'<text x="32" y="365" class="note">{esc(note[92:184])}</text>'
        '</g>'
    )


def render_svg(
    actors: list[dict[str, str]],
    sources: list[dict[str, str]],
    issues: list[dict[str, str]],
    places: list[dict[str, str]],
    archive: list[dict[str, str]],
) -> str:
    actor_total = len(actors)
    source_total = len(sources)
    issue_total = len(issues)
    place_total = len(places)
    period_counts = Counter(source_period(row["year"]) for row in sources)
    period_items = [(label, period_counts[label]) for label in ("1972-1997", "1998-2012", "2013-2019", "2020-current", "unknown")]
    period_items[-1] = ("unknown", period_counts["unknown/undated"])

    place_counts = Counter(row["place_name"] for row in places)
    broad_place_count = place_counts["Henoko"] + place_counts["Okinawa Prefecture"]
    place_top, place_rest = top_categories(place_counts, 7)
    place_items = [(label, place_counts[label]) for label in place_top]
    place_items.append(("other places", sum(place_counts[label] for label in place_rest)))

    class_counts = Counter(row["actor_class"] for row in actors)
    class_top, class_rest = top_categories(class_counts, 6)
    class_items = [(label, class_counts[label]) for label in class_top]
    class_items.append(("other classes", sum(class_counts[label] for label in class_rest)))
    origin_counts = Counter(row["origin_type"] for row in actors)

    issue_actors: dict[str, set[str]] = defaultdict(set)
    for row in issues:
        issue_actors[row["issue_group"]].add(row["actor_id"])
    issue_counts = Counter({label: len(ids) for label, ids in issue_actors.items()})
    issue_top, issue_rest = top_categories(issue_counts, 8)
    issue_items = [(label, issue_counts[label]) for label in issue_top]
    issue_items.append(("other groups*", sum(issue_counts[label] for label in issue_rest)))

    archive_by_id = {row["source_id"]: row["archive_status"] for row in archive}
    failed_total = sum(status == "failed" for status in archive_by_id.values())
    type_counts = Counter(row["source_type"] for row in sources)
    type_top, _ = top_categories(type_counts, 7)
    status_order = ["archived", "manual", "failed", "non-URL"]
    status_key = {"archived": "archived", "manual": "manual_archived", "failed": "failed", "non-URL": "skipped_non_url_reference"}
    cross = Counter()
    for row in sources:
        label = row["source_type"] if row["source_type"] in type_top else "other types"
        cross[(label, archive_by_id[row["source_id"]])] += 1

    review_sets = (("actors", actors), ("actor-issue", issues))
    review_data = []
    evidence_data = []
    for label, corpus in review_sets:
        review_data.append((label, Counter(review_bucket(row["review_status"]) for row in corpus), len(corpus)))
        evidence_data.append((label, Counter(row["evidence_level"] for row in corpus), len(corpus)))

    content_time = bar_rows(period_items, 24, 82, 430, 42)
    content_place = bar_rows(place_items, 24, 78, 430, 30)
    content_actor = bar_rows(class_items, 24, 76, 365, 28)
    content_actor += '<text x="24" y="285" class="mini">origin: ' + esc(" · ".join(
        f"{label} {origin_counts[label]}" for label in sorted(origin_counts, key=lambda v: (-origin_counts[v], v))
    )) + '</text>'
    content_issue = bar_rows(issue_items, 24, 72, 430, 27)

    # Source type × archive heatmap.
    heat_rows = type_top + ["other types"]
    content_source = ''
    for col, label in enumerate(status_order):
        content_source += f'<text x="{365 + col * 82}" y="84" text-anchor="middle" class="mini">{esc(label)}</text>'
    max_cell = max(cross.values()) or 1
    for row_index, label in enumerate(heat_rows):
        yy = 99 + row_index * 27
        content_source += f'<text x="24" y="{yy + 18}" class="lab">{esc(label)}</text>'
        for col, status in enumerate(status_order):
            value = cross[(label, status_key[status])]
            opacity = 0.08 + 0.82 * value / max_cell
            xx = 330 + col * 82
            content_source += f'<rect x="{xx}" y="{yy}" width="70" height="22" rx="4" fill="#26735f" opacity="{opacity:.2f}"/>'
            content_source += f'<text x="{xx + 35}" y="{yy + 16}" text-anchor="middle" class="cell">{value}</text>'

    # Review and evidence normalized bars.
    content_review = '<text x="24" y="88" class="mini">review status — human / AI-seeded / follow-up</text>'
    review_colors = {"human-reviewed": "#26735f", "ai-seeded": "#d59a3a", "follow-up/limited": "#b9b5aa"}
    for idx, (label, counts, total) in enumerate(review_data):
        yy = 105 + idx * 55
        content_review += f'<text x="24" y="{yy + 18}" class="lab">{label}</text>'
        xx = 155
        for key in ("human-reviewed", "ai-seeded", "follow-up/limited"):
            width = counts[key] / total * 500
            content_review += f'<rect x="{xx:.1f}" y="{yy}" width="{width:.1f}" height="24" fill="{review_colors[key]}"/>'
            if width > 38:
                content_review += f'<text x="{xx + width/2:.1f}" y="{yy + 17}" text-anchor="middle" class="inside">{counts[key]}</text>'
            xx += width
    content_review += '<text x="24" y="228" class="mini">evidence level — E4 / E3 / E2</text>'
    evidence_colors = {"E4": "#26735f", "E3": "#70a99a", "E2": "#c8d9d4"}
    for idx, (label, counts, total) in enumerate(evidence_data):
        yy = 245 + idx * 42
        content_review += f'<text x="24" y="{yy + 17}" class="lab">{label}</text>'
        xx = 155
        for key in ("E4", "E3", "E2"):
            width = counts[key] / total * 500
            content_review += f'<rect x="{xx:.1f}" y="{yy}" width="{width:.1f}" height="22" fill="{evidence_colors[key]}"/>'
            if width > 32:
                content_review += f'<text x="{xx + width/2:.1f}" y="{yy + 16}" text-anchor="middle" class="inside">{counts[key]}</text>'
            xx += width

    body = ''.join([
        panel(30, 170, "D1 时间", f"source-log 年份分箱（n={source_total}）", content_time,
              f"2020+ 资料占 {period_counts['2020-current'] / source_total * 100:.1f}%；这反映网页存续与检索路径，不是组织增长。"),
        panel(820, 170, "D2 地点", f"actor-place 观察（n={place_total}）", content_place,
              f"Henoko 与全县宽泛编码占 {broad_place_count}/{place_total}；关键地点之间不能作对称密度比较。"),
        panel(30, 580, "D3 actor 功能／来源层", f"registry 原始 class 与 origin（n={actor_total}）", content_actor,
              f"名单偏向具名、网络化、网页可见 actor；{actor_total} 是工作 registry，不是总体普查。"),
        panel(820, 580, "D4 议题", f"每组去重 actor；组间可重叠（n={actor_total}）", content_issue,
              "base/environment/transnational 更可见；标签数量不是议题投入、声量或支持度。"),
        panel(30, 990, "D5 source type × archive", f"前 7 类 + 机械合并其余类型（n={source_total}）", content_source,
              f"failed={failed_total} 只表示抓取失败，不表示证据不存在；archived 也不保证结论充分。"),
        panel(820, 990, "D6 review × evidence", f"actors n={actor_total}；actor-issue n={issue_total}", content_review,
              "E4 与 human-reviewed 是不同轴；高来源等级不能替代身份、关系和解释复核。"),
    ])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1420" viewBox="0 0 1600 1420" role="img" aria-labelledby="title desc">
<title id="title">一期公开资料样本的六维覆盖偏差审计</title>
<desc id="desc">Six-panel audit of time, place, actor class and origin, issue, source type and archive status, and review and evidence status for {actor_total} registry actors and {source_total} sources.</desc>
<rect width="1600" height="1420" fill="#f3f0e8"/>
<style>
text{{font-family:"Noto Sans CJK SC","Microsoft YaHei",Arial,sans-serif;fill:#19312b}} .title{{font-size:32px;font-weight:700}} .subtitle{{font-size:16px;fill:#52635d}} .sample{{font-size:14px;fill:#6a4b16}} .panel{{fill:#fffdf8;stroke:#d7d3c8;stroke-width:1}} .ph{{font-size:22px;font-weight:700}} .sub{{font-size:13px;fill:#66736e}} .lab{{font-size:12px}} .mini{{font-size:11px;fill:#66736e}} .val{{font-size:12px;font-weight:700}} .bar{{fill:#26735f}} .cell{{font-size:11px;font-weight:700;fill:#15342c}} .inside{{font-size:11px;font-weight:700;fill:#ffffff}} .note-bg{{fill:#f2e5c9}} .note{{font-size:12px;fill:#5b431c}}
</style>
<text x="45" y="52" class="title">一期公开资料样本：六维 coverage bias 核心图 v1</text>
<text x="45" y="82" class="subtitle">偏差审计说明“当前资料让什么更可见”，不估计冲绳民间组织总体分布。</text>
<rect x="45" y="105" width="1510" height="44" rx="8" fill="#f2e5c9"/>
<text x="62" y="123" class="sample">{actor_total} actors + {source_total} sources 均为公开资料驱动的工作样本；无总体分母。source 条数不等于组织活跃度；archive failed 不等于证据不存在。</text>
<text x="62" y="141" class="sample">每个面板的计数单位不同，不能跨面板相加或排序为“研究完成度”。</text>
{body}
<text x="45" y="1402" class="mini">* D4 “other groups” 是剩余 issue-group 的 actor-group presence 合计；同一 actor 可跨组，因此不构成互斥分布。</text>
</svg>'''


def render_brief(cells: list[dict[str, str]], implications: list[dict[str, str]]) -> str:
    time = {row["category"]: row for row in cells if row["facet"] == "source_year_period"}
    archive_counts = Counter()
    for row in cells:
        if row["facet"] == "source_type_x_archive":
            archive_counts[row["subcategory"]] += int(row["count"])
    actor_total = int(next(row["denominator"] for row in cells if row["facet"] == "origin_type"))
    source_total = int(next(row["denominator"] for row in cells if row["facet"] == "source_year_period"))
    place_total = int(next(row["denominator"] for row in cells if row["facet"] == "actor_place_pair"))
    place_counts = {
        row["category"]: int(row["count"])
        for row in cells
        if row["facet"] == "actor_place_pair"
    }
    broad_place_count = place_counts.get("Henoko", 0) + place_counts.get("Okinawa Prefecture", 0)
    return f"""# Coverage audit v1：公开资料样本的可见性偏差

日期：2026-07-13

## 结论先行

当前 **{actor_total} actor registry** 与 **{source_total} source log** 是公开资料驱动的工作样本，不是冲绳民间组织或资料总体的概率样本，也没有可用于估计覆盖率的总体分母。因此，本审计解释的是“哪些对象在当前检索路径下更可见”，不估计总体分布。

- 时间：2020 年以来资料 {time['2020-current']['count']}/{source_total}（{time['2020-current']['share_pct']}%），1972–1997 仅 {time['1972-1997']['count']}/{source_total}。早期组织谱系和更名连续性明显更弱。
- 地点：Henoko 与 Okinawa Prefecture 宽泛节点合计 {broad_place_count}/{place_total} 个 actor-place 观察，不能把关键地点间计数差解释为真实组织密度差。
- actor 功能／来源层：registry 偏向具名、网络化、有持续网页或正式记录的 actor；短期委员会、社区小组和旧名称更难被捕捉。
- 议题：基地政治、环境与跨国议题覆盖较宽；劳动、女性／人权、健康及若干生活安全子题更依赖专项补查。
- source/archive：{archive_counts['archived'] + archive_counts['manual_archived']}/{source_total} 已归档或人工归档，{archive_counts['failed']}/{source_total} 抓取失败。**archive failed 不等于证据不存在**；反过来，archived 也不保证某项编码结论充分。
- review/evidence：E4 与 human-reviewed 是不同维度；官方或一手资料等级较高，不代表 actor 身份、关系边界或分析结论已经人工接受。

## 对基础问题的影响

- **Q1“有哪些组织”**：可回答为公开资料中已识别的工作名册；不能称为完整总体。时间、网页存续和地点检索偏差会漏掉早期、短期、地方性 actor。
- **Q2“如何分类、谁是桥梁”**：分类可作证据分层描述，但 registry 构成与 issue 标签可见性会放大网络化、正式化和跨国倡议 actor；桥梁性不能脱离候选边与人审状态。
- **Q3“关键地点如何连接议题”**：Henoko 的资料密度远高于 Futenma、Kadena 与 Sakishima 地点；现有图适合解释已观察机制，不适合比较真实组织密度或支持度。

## 对 R1–R11 的解释边界

`coverage_bias_implications_v1.csv` 逐维给出影响。概括而言：R1/R2 受 registry、功能和议题可见性影响；R3/R4/R9 受地点不对称影响；R5–R8 受事件、法律与跨期记录存续影响；R10/R11 是价值驱动的行政／外来 actor 样本层，不能当作完整部门分布。所有关系型模块都必须继续区分候选、事实、人审与 analytical seed。

## 补查分流

线上继续：历史网页和旧称、数字报刊索引、地方政府／议会记录、专题组织资料、失败归档的替代 URL/PDF 与内容充分性核验。

当地协作者：1972–2012 报刊和通讯、先岛地方馆藏／议会资料、短期委员会和组织更名／代表／持续性、未在线保存的意见广告与活动材料。当地任务应由具体缺字段驱动，而非为提高 registry/source 数字而泛搜。

## 三条不可跨越的解释边界

1. source 条数不等于组织活跃度、社会支持度或事件频率。
2. archive failed 是技术／可得性状态，不等于证据不存在；archived 也不等于证据充分。
3. {actor_total} actors 与 {source_total} sources 仅描述当前公开资料样本，不能估计冲绳民间组织总体分布。

## HR-023

本轮不创建 HR-023 决策项。六维统计、Top-N 展示和 review bucket 均为可复现机械审计，没有新增 actor 分类、关系接受、证据等级修改或研究口径决定。需要人审的既有关系和身份问题继续留在原有 HR 队列；不为凑任务重复创建。
"""


def main() -> None:
    actors = read_csv(ACTORS)
    sources = read_csv(SOURCES)
    issues = read_csv(ACTOR_ISSUES)
    places = read_csv(ACTOR_PLACES)
    archive = read_csv(ARCHIVE)

    if not actors or not sources or not issues or not places:
        raise ValueError("coverage audit inputs must be non-empty")
    source_ids = {row["source_id"] for row in sources}
    archive_ids = {row["source_id"] for row in archive}
    if len(source_ids) != len(sources) or source_ids != archive_ids:
        raise ValueError("source log and archive manifest IDs must form the same unique source set")
    actor_ids = {row["actor_id"] for row in actors}
    if len(actor_ids) != len(actors):
        raise ValueError("actor registry contains duplicate actor IDs")
    if not {row["actor_id"] for row in issues}.issubset(actor_ids):
        raise ValueError("actor-issue table contains an actor outside the registry")
    if not {row["actor_id"] for row in places}.issubset(actor_ids):
        raise ValueError("actor-place table contains an actor outside the registry")
    if len({(row["actor_id"], row["place_name"]) for row in places}) != len(places):
        raise ValueError("actor-place table contains duplicate actor/place pairs")

    cells = build_cells(actors, sources, issues, places, archive)
    implications = build_implications(cells)
    if {row["dimension_id"] for row in cells} != {"D1", "D2", "D3", "D4", "D5", "D6"}:
        raise ValueError("six-dimensional audit is incomplete")
    if len(implications) != 6:
        raise ValueError("expected six bias implication rows")

    svg = render_svg(actors, sources, issues, places, archive)
    html_page = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Coverage bias core v1</title><style>body{{margin:0;background:#e9e6de}}main{{max-width:1600px;margin:20px auto;background:#f3f0e8;box-shadow:0 8px 28px #0002}}svg{{display:block;width:100%;height:auto}}@media(max-width:700px){{main{{margin:0;box-shadow:none}}}}</style></head>
<body><main>{svg}</main></body></html>"""

    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(CELLS, CELL_FIELDS, cells)
    write_csv(IMPLICATIONS, IMPLICATION_FIELDS, implications)
    SVG.write_text(svg, encoding="utf-8")
    HTML.write_text(html_page, encoding="utf-8")
    BRIEF.write_text(render_brief(cells, implications), encoding="utf-8")
    HR023.write_text(
        "# HR-023 status\n\n"
        "本轮无需创建 HR-023 决策项。coverage audit 仅执行可复现的机械统计与展示聚合，"
        "没有新增 actor 分类、关系接受、证据等级修改或口径决策。既有人审问题继续使用原 HR 队列，"
        "不在此重复造任务。\n",
        encoding="utf-8",
    )

    if read_csv(CELLS) != cells or read_csv(IMPLICATIONS) != implications:
        raise ValueError("CSV roundtrip mismatch")
    if f"{len(actors)} actors + {len(sources)} sources" not in svg:
        raise ValueError("sample boundary missing from core figure")
    print(
        f"coverage audit OK: {len(cells)} cells; 6 dimensions; "
        f"{len(actors)} actors; {len(sources)} sources; {len(implications)} implication rows"
    )


if __name__ == "__main__":
    main()
