"""Build a read-only cross-module source-log merge proposal.

The generator reads R4/R9/R10 source candidates plus the current main source
log and archive manifest.  It writes only outputs/phase1_source_integration_v1;
it never edits the source log and never archives a URL.
"""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
R4 = ROOT / "outputs" / "R04_sakishima_frame_corpus_v0" / "online_evidence_safe_sources_v0.csv"
R9 = ROOT / "outputs" / "R09_referendum_process_v0" / "source_register_v0.csv"
R10 = ROOT / "outputs" / "R10_administrative_collaboration_v0" / "source_crosswalk_v1.csv"
MAIN = ROOT / "data" / "interim" / "05_source_log_initial_v0.csv"
MANIFEST = ROOT / "source_docs" / "source_archive" / "source_archive_manifest.csv"
OUT = ROOT / "outputs" / "phase1_source_integration_v1"
OUT_CSV = OUT / "source_merge_candidates_v0.csv"
README = OUT / "README.md"

R9_ALLOWED = {"accepted", "usable_with_limit"}
R10_ALLOWED = {"module_candidate_not_in_main_log"}
TRACKING_QUERY_PREFIXES = ("utm_",)
TRACKING_QUERY_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid"}
MODULE_PRIORITY = {"R9": 0, "R4": 1, "R10": 2}
INTEGRATION_NOTE_MARKER = "Phase-1 module source integration "

FIELDS = [
    "proposal_row_id",
    "merge_status",
    "current_main_match",
    "cross_module_duplicate",
    "proposed_new",
    "normalized_url",
    "original_urls",
    "current_main_source_ids",
    "declared_existing_source_ids",
    "proposed_source_id",
    "module_source_refs",
    "support_modules",
    "module_record_count",
    "proposed_title",
    "proposed_source_type",
    "proposed_year_or_period",
    "proposed_evidence_level",
    "module_dispositions",
    "what_it_supports",
    "review_boundary",
    "main_archive_status",
    "archive_prerequisite",
    "human_review_required",
    "human_review_prerequisite",
    "metadata_conflicts",
    "recommended_action",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def normalize_url(url: str) -> str:
    """Conservatively normalize for deduplication without changing resource identity."""
    raw = url.strip()
    parts = urlsplit(raw)
    scheme = parts.scheme.lower()
    hostname = (parts.hostname or "").lower()
    port = parts.port
    if port and not ((scheme == "http" and port == 80) or (scheme == "https" and port == 443)):
        netloc = f"{hostname}:{port}"
    else:
        netloc = hostname
    path = re.sub(r"/{2,}", "/", parts.path or "/")
    if path != "/":
        path = path.rstrip("/")
    query_items = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if key.lower() not in TRACKING_QUERY_KEYS
        and not key.lower().startswith(TRACKING_QUERY_PREFIXES)
    ]
    query = urlencode(sorted(query_items))
    return urlunsplit((scheme, netloc, path, query, ""))


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value.strip() for value in values if value and value.strip()))


def joined(values: list[str], separator: str = ";") -> str:
    return separator.join(unique(values))


def first_year(value: str, title: str) -> str:
    for text in (value, title):
        match = re.search(r"(?:19|20)\d{2}", text or "")
        if match:
            return match.group(0)
    if (value or "").lower() == "current":
        return "2026"
    return value or "undated"


def canonical_source_type(raw: str, title: str, url: str) -> str:
    text = f"{raw} {title} {url}".lower()
    if "court" in text or "判決" in text or "裁判" in text:
        return "court_record"
    if "legislative" in text or "council" in text or "議会" in text or "决议" in text or "決議" in text:
        return "official_legislative_record"
    if "defense" in text or "mod.go.jp" in text or "防衛" in text or "自衛隊" in text:
        return "official_defense"
    if "organization_blog" in text or "ti-da.net" in text:
        return "organization_blog"
    if "organization" in text or "oki-ngo.org" in text:
        return "organization_site"
    if "news" in text or "新聞" in text or "報道" in text:
        return "local_news"
    if "pref" in text or "okinawa.lg.jp" in text or "沖縄県" in text:
        return "prefectural_official"
    if "national" in text or "cabinet" in text or "kokuminhogo.go.jp" in text or "内閣" in text:
        return "national_official"
    if "city" in text or "town" in text or "municipal" in text or "市" in text or "町" in text:
        return "local_official"
    return "official_or_primary_web_record"


def infer_r10_type(row: dict[str, str]) -> str:
    return canonical_source_type("", row["title"], row["url"])


def collect_module_records() -> tuple[list[dict[str, str]], dict[str, set[str]]]:
    records: list[dict[str, str]] = []
    selected_ids: dict[str, set[str]] = {"R4": set(), "R9": set(), "R10": set()}

    for row in read_csv(R4):
        module_id = row["corpus_source_id"]
        selected_ids["R4"].add(module_id)
        records.append(
            {
                "module": "R4",
                "module_id": module_id,
                "url": row["url"],
                "declared_existing_id": row.get("existing_source_id", ""),
                "title": row["title"],
                "source_type": canonical_source_type(row["source_type"], row["title"], row["url"]),
                "year": first_year(row["date_or_period"], row["title"]),
                "evidence_level": row["evidence_level"],
                "disposition": row["qa_disposition"],
                "supports": f"{row['place']}: {row['paraphrase_zh']} [{row['frame_candidates']}]",
                "boundary": joined([row["interpretation_limit"], row["qa_reason"]], " | "),
                "metadata_review_hint": (
                    "confirm_year_or_period" if row["date_or_period"] in {"current", "undated"} else ""
                ),
            }
        )

    all_r9 = read_csv(R9)
    for row in all_r9:
        if row["disposition"] not in R9_ALLOWED:
            continue
        module_id = row["source_id"]
        selected_ids["R9"].add(module_id)
        records.append(
            {
                "module": "R9",
                "module_id": module_id,
                "url": row["url"],
                "declared_existing_id": row.get("existing_source_id", ""),
                "title": row["title"],
                "source_type": canonical_source_type(row["source_type"], row["title"], row["url"]),
                "year": first_year(row["year"], row["title"]),
                "evidence_level": row["evidence_level"],
                "disposition": row["disposition"],
                "supports": f"{row['case_id']}: {row['supports']}",
                "boundary": joined([row["interpretation_limit"], row["notes"]], " | ")
                or "Process/source fact only; do not infer organization continuity, alliance, or later authorization.",
                "metadata_review_hint": (
                    "retain_usable_with_limit_boundary"
                    if row["disposition"] == "usable_with_limit"
                    else ""
                ),
            }
        )

    for row in read_csv(R10):
        if row["status"] not in R10_ALLOWED:
            continue
        module_id = row["source_ref"]
        selected_ids["R10"].add(module_id)
        records.append(
            {
                "module": "R10",
                "module_id": module_id,
                "url": row["url"],
                "declared_existing_id": "",
                "title": row["title"],
                "source_type": infer_r10_type(row),
                "year": first_year("", row["title"]),
                "evidence_level": "E4",
                "disposition": row["status"],
                "supports": f"R10 administrative-collaboration evidence: {row['locator_coverage']}",
                "boundary": joined(
                    [row["merge_note"], "source metadata inferred from crosswalk; no archive performed"],
                    " | ",
                ),
                "metadata_review_hint": "confirm_R10_inferred_type_year_and_support_scope",
            }
        )
    return records, selected_ids


def choose_record(records: list[dict[str, str]]) -> dict[str, str]:
    return sorted(
        records,
        key=lambda row: (MODULE_PRIORITY[row["module"]], -len(row["title"]), row["module_id"]),
    )[0]


def is_own_integrated_row(row: dict[str, str]) -> bool:
    """Exclude this proposal's later merge rows from its historical baseline."""
    return INTEGRATION_NOTE_MARKER in row.get("notes", "")


def build_rows() -> tuple[list[dict[str, str]], dict[str, int]]:
    module_records, selected_ids = collect_module_records()
    main_rows = read_csv(MAIN)
    manifest_by_id = {row["source_id"]: row for row in read_csv(MANIFEST)}
    main_by_id = {row["source_id"]: row for row in main_rows}
    main_by_url: dict[str, list[dict[str, str]]] = defaultdict(list)
    integrated_source_ids = {
        row["source_id"] for row in main_rows if is_own_integrated_row(row)
    }
    for row in main_rows:
        if row["source_id"] in integrated_source_ids:
            continue
        main_by_url[normalize_url(row["url"])].append(row)

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for record in module_records:
        record["normalized_url"] = normalize_url(record["url"])
        grouped[record["normalized_url"]].append(record)

    provisional: list[dict[str, object]] = []
    for normalized_url in sorted(grouped):
        records = grouped[normalized_url]
        modules = sorted({row["module"] for row in records})
        url_main_ids = {row["source_id"] for row in main_by_url.get(normalized_url, [])}
        declared_ids = {row["declared_existing_id"] for row in records if row["declared_existing_id"]}
        valid_declared = declared_ids & set(main_by_id)
        current_ids = sorted(url_main_ids | valid_declared)
        if current_ids:
            merge_status = "current_main_match"
        elif len(modules) > 1:
            merge_status = "cross_module_duplicate"
        else:
            merge_status = "proposed_new"

        selected = (
            main_by_id[current_ids[0]]
            if current_ids
            else choose_record(records)
        )
        if current_ids:
            proposed_title = selected["title"]
            proposed_type = selected["source_type"]
            proposed_year = selected["year"]
            proposed_evidence = selected["evidence_level"]
        else:
            chosen = choose_record(records)
            proposed_title = chosen["title"]
            proposed_type = chosen["source_type"]
            proposed_year = chosen["year"]
            proposed_evidence = max(
                (row["evidence_level"] for row in records),
                key=lambda value: {"E2": 2, "E3": 3, "E4": 4}.get(value, 0),
            )

        conflicts: list[str] = []
        module_types = unique([row["source_type"] for row in records])
        module_years = unique([row["year"] for row in records])
        module_levels = unique([row["evidence_level"] for row in records])
        if len(module_types) > 1:
            conflicts.append("source_type=" + "/".join(module_types))
        if len(module_years) > 1:
            conflicts.append("year=" + "/".join(module_years))
        if len(module_levels) > 1:
            conflicts.append("evidence=" + "/".join(module_levels))
        declared_url_mismatches = [
            declared
            for declared in valid_declared
            if normalize_url(main_by_id[declared]["url"]) != normalized_url
        ]
        if declared_url_mismatches:
            conflicts.append("declared_existing_id_url_mismatch=" + "/".join(sorted(declared_url_mismatches)))
        if len(current_ids) > 1:
            conflicts.append("multiple_main_matches=" + "/".join(current_ids))

        archive_statuses = unique(
            [manifest_by_id[source_id]["archive_status"] for source_id in current_ids if source_id in manifest_by_id]
        )
        if current_ids:
            main_archive_status = joined(archive_statuses) or "manifest_missing"
            if archive_statuses and all(status in {"archived", "manual_archived"} for status in archive_statuses):
                archive_prerequisite = "none_current_main_archive_available"
            else:
                archive_prerequisite = "current_main_registered_but_archive_retry_or_check_needed"
        else:
            main_archive_status = "not_applicable_new_candidate"
            archive_prerequisite = "archive_before_main_source_log_merge"

        human_reasons = unique([row["metadata_review_hint"] for row in records])
        if not current_ids:
            human_reasons.insert(0, "approve_new_source_metadata_and_scope")
        if merge_status == "cross_module_duplicate":
            human_reasons.append("confirm_cross_module_collapse_to_one_source")
        if conflicts:
            human_reasons.append("resolve_metadata_or_URL_conflict")
        human_reasons = unique(human_reasons)

        if merge_status == "current_main_match":
            action = "reuse current main source ID; do not add a duplicate"
        elif merge_status == "cross_module_duplicate":
            action = "after archive and review, add one source row and map all module refs to it"
        else:
            action = "after archive and review, add proposed source row"

        provisional.append(
            {
                "merge_status": merge_status,
                "current_main_match": "yes" if current_ids else "no",
                "cross_module_duplicate": "yes" if len(modules) > 1 else "no",
                "proposed_new": "yes" if not current_ids else "no",
                "normalized_url": normalized_url,
                "original_urls": joined([row["url"] for row in records]),
                "current_main_source_ids": ";".join(current_ids),
                "declared_existing_source_ids": ";".join(sorted(declared_ids)),
                "proposed_source_id": "",
                "module_source_refs": ";".join(
                    f"{row['module']}:{row['module_id']}" for row in sorted(
                        records, key=lambda item: (MODULE_PRIORITY[item["module"]], item["module_id"])
                    )
                ),
                "support_modules": ";".join(modules),
                "module_record_count": str(len(records)),
                "proposed_title": proposed_title,
                "proposed_source_type": proposed_type,
                "proposed_year_or_period": proposed_year,
                "proposed_evidence_level": proposed_evidence,
                "module_dispositions": joined(
                    [f"{row['module']}:{row['disposition']}" for row in records]
                ),
                "what_it_supports": joined([row["supports"] for row in records], " | "),
                "review_boundary": joined([row["boundary"] for row in records], " | "),
                "main_archive_status": main_archive_status,
                "archive_prerequisite": archive_prerequisite,
                "human_review_required": "yes" if human_reasons else "no",
                "human_review_prerequisite": ";".join(human_reasons) if human_reasons else "none",
                "metadata_conflicts": ";".join(conflicts),
                "recommended_action": action,
            }
        )

    proposed_rows = [row for row in provisional if row["merge_status"] != "current_main_match"]
    existing_source_ids = set(main_by_id) - integrated_source_ids
    for offset, row in enumerate(proposed_rows):
        proposed_id = f"S{160 + offset:03d}"
        if proposed_id in existing_source_ids:
            raise ValueError(f"proposed source ID already exists: {proposed_id}")
        row["proposed_source_id"] = proposed_id

    rows: list[dict[str, str]] = []
    for index, row in enumerate(provisional, start=1):
        rows.append({"proposal_row_id": f"SMC{index:03d}", **row})

    selected_counts = {module: len(ids) for module, ids in selected_ids.items()}
    selected_counts["input_records"] = len(module_records)
    return rows, selected_counts


def validate(rows: list[dict[str, str]], selected_counts: dict[str, int]) -> None:
    if selected_counts != {"R4": 19, "R9": 30, "R10": 8, "input_records": 57}:
        raise ValueError(f"module-source coverage changed: {selected_counts}")
    module_refs = [
        ref
        for row in rows
        for ref in row["module_source_refs"].split(";")
        if ref
    ]
    if len(module_refs) != 57 or len(set(module_refs)) != 57:
        raise ValueError("module record coverage is incomplete or duplicated")
    expected_refs = (
        {f"R4:{row['corpus_source_id']}" for row in read_csv(R4)}
        | {
            f"R9:{row['source_id']}"
            for row in read_csv(R9)
            if row["disposition"] in R9_ALLOWED
        }
        | {
            f"R10:{row['source_ref']}"
            for row in read_csv(R10)
            if row["status"] in R10_ALLOWED
        }
    )
    if set(module_refs) != expected_refs:
        raise ValueError("proposal does not exactly cover all allowed module sources")
    rejected_refs = {
        f"R9:{row['source_id']}"
        for row in read_csv(R9)
        if row["disposition"] not in R9_ALLOWED
    }
    r4_reject_path = ROOT / "outputs" / "R04_sakishima_frame_corpus_v0" / "source_reject_log_v0.csv"
    rejected_refs |= {
        f"R4:{row['corpus_source_id']}" for row in read_csv(r4_reject_path)
    }
    if set(module_refs) & rejected_refs:
        raise ValueError("rejected module source leaked into proposal")
    if len({row["normalized_url"] for row in rows}) != len(rows):
        raise ValueError("normalized URL deduplication failed")
    proposed = [row for row in rows if row["merge_status"] != "current_main_match"]
    if len({row["normalized_url"] for row in proposed}) != len(proposed):
        raise ValueError("duplicate proposed URL")
    expected_ids = [f"S{160 + index:03d}" for index in range(len(proposed))]
    if [row["proposed_source_id"] for row in proposed] != expected_ids:
        raise ValueError("proposed IDs are not deterministic from S160")
    if any(row["proposed_source_id"] for row in rows if row["merge_status"] == "current_main_match"):
        raise ValueError("current main matches must not receive proposed IDs")
    allowed_statuses = {"current_main_match", "cross_module_duplicate", "proposed_new"}
    if {row["merge_status"] for row in rows} - allowed_statuses:
        raise ValueError("invalid merge status")
    if any("rejected" in row["module_dispositions"] for row in rows):
        raise ValueError("rejected source leaked into proposal")
    for row in rows:
        if (row["current_main_match"] == "yes") != bool(row["current_main_source_ids"]):
            raise ValueError(f"main-match flag mismatch: {row['proposal_row_id']}")
        if (row["cross_module_duplicate"] == "yes") != (len(row["support_modules"].split(";")) > 1):
            raise ValueError(f"cross-module flag mismatch: {row['proposal_row_id']}")
        if (row["proposed_new"] == "yes") != bool(row["proposed_source_id"]):
            raise ValueError(f"proposed-new flag mismatch: {row['proposal_row_id']}")
        required_metadata = [
            "proposed_title", "proposed_source_type", "proposed_year_or_period",
            "proposed_evidence_level", "what_it_supports", "review_boundary",
            "archive_prerequisite", "human_review_prerequisite", "recommended_action",
        ]
        if any(not row[field].strip() for field in required_metadata):
            raise ValueError(f"incomplete proposal metadata: {row['proposal_row_id']}")
    for row in proposed:
        if row["archive_prerequisite"] != "archive_before_main_source_log_merge":
            raise ValueError(f"new candidate lacks archive prerequisite: {row['proposal_row_id']}")
        if row["human_review_required"] != "yes":
            raise ValueError(f"new candidate lacks human approval prerequisite: {row['proposal_row_id']}")


def render_readme(rows: list[dict[str, str]], counts: dict[str, int]) -> str:
    status_counts = Counter(row["merge_status"] for row in rows)
    proposed = [row for row in rows if row["merge_status"] != "current_main_match"]
    archive_retry = [
        row for row in rows
        if row["archive_prerequisite"] == "current_main_registered_but_archive_retry_or_check_needed"
    ]
    human_review = [row for row in rows if row["human_review_required"] == "yes"]
    conflicts = [row for row in rows if row["metadata_conflicts"]]
    cross_module = [row for row in rows if row["cross_module_duplicate"] == "yes"]
    proposed_lines = [
        f"- `{row['proposed_source_id']}` · `{row['merge_status']}` · {row['proposed_title']} · {row['support_modules']}"
        for row in proposed
    ] or ["- 无"]
    conflict_lines = [
        f"- `{row['proposal_row_id']}`：{row['metadata_conflicts']}"
        for row in conflicts
    ] or ["- 无"]
    cross_module_lines = [
        f"- `{row['proposal_row_id']}` · {row['module_source_refs']} · main={row['current_main_source_ids'] or 'none'} · proposed={row['proposed_source_id'] or 'none'}"
        for row in cross_module
    ] or ["- 无"]
    archive_retry_lines = [
        f"- `{row['proposal_row_id']}` · main={row['current_main_source_ids']} · manifest={row['main_archive_status']}"
        for row in archive_retry
    ] or ["- 无"]
    return "\n".join(
        [
            "# Phase-1 cross-module source merge proposal v1",
            "",
            "本包是来源主表合并建议，不是合并结果。脚本不修改 `05_source_log_initial_v0.csv`，也不下载或归档任何 URL。",
            "",
            "## 输入与覆盖",
            "",
            f"- R4 QA-safe sources：{counts['R4']} 条。",
            f"- R9 `accepted` / `usable_with_limit`：{counts['R9']} 条；2 条 rejected 未纳入。",
            f"- R10 `module_candidate_not_in_main_log`：{counts['R10']} 条。",
            f"- 模块记录合计：{counts['input_records']} 条；规范化 URL 后：{len(rows)} 条唯一候选。",
            "",
            "## 合并状态",
            "",
            f"- `current_main_match`：{status_counts['current_main_match']} 条，复用已有 S 编号。",
            f"- `cross_module_duplicate` 主状态：{status_counts['cross_module_duplicate']} 条；独立重复标记共 {len(cross_module)} 条。当前重复 URL 若已在主表，主状态仍优先记为 `current_main_match`。",
            f"- `proposed_new`：{status_counts['proposed_new']} 条。",
            f"- 待新增唯一 URL：{len(proposed)} 条，按规范化 URL 排序后从 S160 连续编号。",
            "",
            "## 跨模块重复 URL",
            "",
            *cross_module_lines,
            "",
            "## 待新增编号",
            "",
            *proposed_lines,
            "",
            "## 归档与人工复核边界",
            "",
            "- 所有待新增来源必须先归档，再由人工确认 title、type、year/period、evidence level 与支持范围；本包不授权直接写入主表。",
            "- R9 `usable_with_limit` 必须把原 interpretation limit 原样带入，不能因来源进入主表而升级结论。",
            "- R10 的 type/year/evidence 是 proposal 层推定，必须在人审和归档后才能落主表。",
            f"- 已在主表但归档 manifest 仍失败或缺失、建议重试/检查：{len(archive_retry)} 条。",
            f"- `human_review_required=yes`：{len(human_review)} 条；逐行原因见 CSV 的 `human_review_prerequisite`。",
            "- `current_main_match` 只表示 URL 或声明的 existing ID 已对应主表，不代表该来源支持模块的全部解释。",
            "",
            "### 主表已有但需重试／检查归档",
            "",
            *archive_retry_lines,
            "",
            "## 元数据或 URL 冲突",
            "",
            *conflict_lines,
            "",
            "## URL 规范化口径",
            "",
            "scheme/host 小写；移除 fragment、默认端口、尾斜杠和常见 tracking query；保留并排序其余 query。该口径保守，不合并不同 path 的主页与子页。",
            "",
            "## 复现与验证",
            "",
            "运行 `python scripts/make_phase1_source_merge_proposal.py`。脚本验证 57 条可用模块记录全部覆盖、rejected 不进入、每个规范化 URL 仅一行、待新增 URL 不重复、S160 起编号稳定。",
            "为保留合并前审计基线，脚本会识别 notes 中带 `Phase-1 module source integration` 的本包既有落表行，并在 proposal 比对时排除这些行；不会排除其他主来源。",
            "",
        ]
    )


def main() -> None:
    rows, counts = build_rows()
    validate(rows, counts)
    write_csv(OUT_CSV, rows)
    README.write_text(render_readme(rows, counts), encoding="utf-8")
    if read_csv(OUT_CSV) != rows:
        raise ValueError("proposal CSV roundtrip mismatch")
    print(
        f"Source proposal OK: 57 module records -> {len(rows)} normalized URLs; "
        f"{sum(row['merge_status'] == 'current_main_match' for row in rows)} main matches; "
        f"{sum(row['merge_status'] != 'current_main_match' for row in rows)} proposed IDs from S160."
    )


if __name__ == "__main__":
    main()
