#!/usr/bin/env python3
"""Build the client-facing data and evidence attachment for progress sync 3.

The bundle is deliberately narrower than the repository. It exports public-safe
columns, the immutable client-preview publication payload, figure assets, source
metadata, limited evidence notes, and locally archived official primary records.
News/media archives and internal review-task fields remain outside the ZIP.
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import zipfile
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = ROOT / "outputs" / "formal_comm_v3"
STAGE = OUT_ROOT / "附件_研究数据与证据_v1"
ZIP_PATH = OUT_ROOT / "复归后冲绳民间组织_NGO_第三次同步_研究数据与证据附件_v1.zip"
OUT_README = OUT_ROOT / "附件_研究数据与证据_v1_README.md"

TODAY = date(2026, 7, 21)
ZIP_TIMESTAMP = (2026, 7, 21, 0, 0, 0)

INTERNAL_COLUMNS = {
    "notes",
    "human_reviewer",
    "review_task_id",
    "decision_source_report",
    "scope_decision_source_report",
    "identity_decision_id",
    "hr018_relation_observation_ids",
}

OFFICIAL_ARCHIVE_TYPES = {
    "official_legislative_record",
    "local_official",
    "court_record",
    "official_data",
    "official_portal",
    "prefectural_official",
    "official_project_report",
    "government_webpage",
    "official_npo_portal",
    "official_gazette",
    "official_defense",
    "government_report",
    "national_official",
    "official_contract_record",
    "official_referendum",
    "official_government_record",
    "official_jica_partner_page",
    "official_jica_project_record",
    "official_meeting_minutes",
    "official_npo_report",
    "government_corporate_record",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], columns: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        if columns:
            with path.open("w", encoding="utf-8-sig", newline="") as handle:
                csv.DictWriter(handle, fieldnames=columns).writeheader()
        return
    if columns is None:
        columns = [key for key in rows[0] if key not in INTERNAL_COLUMNS]
    missing = [column for column in columns if column not in rows[0]]
    if missing:
        raise ValueError(f"{path.name}: missing columns {missing}")
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def safe_copy(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_value(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def source_worktree_dirty() -> bool:
    """Ignore only this builder's generated attachment outputs."""
    ignored_prefixes = {
        ZIP_PATH.relative_to(ROOT).as_posix(),
        OUT_README.relative_to(ROOT).as_posix(),
        STAGE.relative_to(ROOT).as_posix(),
    }
    status = git_value("-c", "core.quotepath=false", "status", "--porcelain=v1")
    for line in status.splitlines():
        path_text = line[3:].strip().strip('"').replace("\\", "/")
        if not any(path_text.startswith(prefix) for prefix in ignored_prefixes):
            return True
    return False


def export_tables() -> dict[str, int]:
    out = STAGE / "01_当前数据"
    counts: dict[str, int] = {}

    specs: list[tuple[str, str, list[str] | None, object]] = [
        (
            "data/interim/01_actor_registry_initial_v0.csv",
            "组织登记表_历史122.csv",
            [
                "actor_id", "canonical_name", "actor_class", "origin_type",
                "legal_status_guess", "primary_places", "issue_tags", "source_refs",
                "evidence_level", "review_status", "needs_local_retrieval",
                "scope_status", "merged_duplicate_of", "human_decision", "reviewed_fields",
            ],
            None,
        ),
        (
            "data/interim/03_issue_taxonomy_v0.csv",
            "议题分类_26.csv",
            ["issue_id", "issue_label", "issue_group", "definition", "include_in_phase1"],
            None,
        ),
        (
            "data/interim/04_place_registry_v0.csv",
            "地点与场域_21.csv",
            [
                "place_id", "place_name", "place_type", "region", "why_relevant",
                "phase1_priority", "parent_place_id", "aliases",
            ],
            None,
        ),
        (
            "outputs/R01_R02_actor_issue_v1/active_actor_issue_edges_v1.csv",
            "组织议题关系_当前283.csv",
            None,
            None,
        ),
        (
            "data/interim/08_actor_place_edges_initial_v0.csv",
            "组织地点关系_当前130.csv",
            [
                "edge_id", "actor_id", "place_id", "place_name", "relation_basis",
                "source_ref", "evidence_level", "review_status", "scope_status",
                "place_semantic", "interpretation_limit", "approved_formulation",
                "review_scope", "claim_status", "confirmed_scope", "missing_scope",
                "graph_eligibility",
            ],
            lambda row: not row.get("scope_status", "").startswith("retired_"),
        ),
        (
            "data/interim/09_actor_event_venue_edges_v0.csv",
            "组织事件场域_67.csv",
            [
                "record_id", "record_scope", "event_id", "event_name", "event_year",
                "actor_or_counterpart_id", "legacy_candidate_id", "actor_or_counterpart_name",
                "entity_type", "action_type", "venue_id", "target_type", "target_id_or_name",
                "role", "pathway_stage", "evidence_level", "source_id", "reviewer_status",
                "interpretation_limit", "review_decision",
            ],
            None,
        ),
        (
            "data/interim/15_funding_or_support_edges_sample_v0.csv",
            "类型化关系样本_43.csv",
            None,
            None,
        ),
        (
            "data/interim/17_legal_policy_procedure_cases_v0.csv",
            "法律政策案件_6.csv",
            None,
            None,
        ),
        (
            "data/interim/18_legal_policy_actor_roles_v0.csv",
            "法律政策角色_27.csv",
            None,
            None,
        ),
        (
            "outputs/R03_strict_place_issue_v1/same_source_actor_place_issue_triples_v1.csv",
            "同源组织地点议题三元组_306.csv",
            None,
            None,
        ),
        (
            "outputs/R05_coaction_v1/actor_event_bipartite_edges_v0.csv",
            "三份公开行动名单_参与观察169.csv",
            None,
            None,
        ),
        (
            "outputs/R05_coaction_v1/repeat_participation_bridges_v0.csv",
            "三份公开行动名单_重复身份21.csv",
            None,
            None,
        ),
        (
            "outputs/R09_referendum_process_v0/process_stages_reviewed_all_v0.csv",
            "公投案例_已接受阶段29.csv",
            None,
            lambda row: row.get("review_status") == "accepted",
        ),
        (
            "outputs/R09_referendum_process_v0/actor_process_roles_reviewed_all_v0.csv",
            "公投案例_已接受角色29.csv",
            None,
            lambda row: row.get("review_status") == "accepted",
        ),
        (
            "outputs/translation_episode_comparison_v1/translation_episode_candidates_v1.csv",
            "制度转译比较_13案例.csv",
            None,
            None,
        ),
        (
            "outputs/R10_official_collaboration_universe_v1/official_collaboration_source_universe_v1.csv",
            "县政府NPO日常协作_官方616记录.csv",
            None,
            None,
        ),
        (
            "outputs/formal_comm_v3/data/current_metrics_v3.csv",
            "第三次同步_数字口径索引.csv",
            None,
            None,
        ),
    ]

    for source_name, output_name, columns, predicate in specs:
        rows = read_csv(ROOT / source_name)
        if predicate:
            rows = [row for row in rows if predicate(row)]
        write_csv(out / output_name, rows, columns)
        counts[output_name] = len(rows)

    if counts["组织地点关系_当前130.csv"] != 130:
        raise AssertionError("current actor-place export must contain 130 rows")
    return counts


def copy_publication_payload() -> dict[str, object]:
    source = ROOT / "prototypes" / "nr3_explorer" / "dist"
    target = STAGE / "02_前端冻结数据"
    for name in ["core", "research", "exhibits", "views"]:
        shutil.copytree(source / name, target / name)
    for name in ["manifest.json", "checksums.json", "release.json"]:
        safe_copy(source / name, target / name)
    return json.loads((source / "release.json").read_text(encoding="utf-8"))


def copy_figures() -> None:
    target = STAGE / "03_图表与底表"
    shutil.copytree(OUT_ROOT / "fig", target / "第三次同步截图")
    safe_copy(
        ROOT / "outputs" / "coverage_audit_v1" / "coverage_bias_implications_v1.csv",
        target / "资料覆盖偏差_含义表.csv",
    )
    safe_copy(
        ROOT / "outputs" / "R10_official_collaboration_universe_v1" / "descriptive_statistics_v1.csv",
        target / "县政府协作记录_描述统计.csv",
    )


def export_evidence() -> tuple[dict[str, int], list[dict[str, str]]]:
    evidence_dir = STAGE / "04_证据索引"
    archive_dir = STAGE / "05_官方一手证据归档"
    sources = read_csv(ROOT / "data" / "interim" / "05_source_log_initial_v0.csv")
    evidence_notes = read_csv(ROOT / "data" / "interim" / "06_evidence_notes_v0.csv")
    archive_rows = read_csv(ROOT / "source_docs" / "source_archive" / "source_archive_manifest.csv")
    source_by_id = {row["source_id"]: row for row in sources}

    public_source_columns = [
        "source_id", "source_type", "title", "year", "url", "what_it_supports",
        "evidence_level", "bias_note", "review_status", "locator", "support_scope",
        "archive_resolution", "relation_or_claim_approved",
    ]
    write_csv(evidence_dir / "来源索引_295.csv", sources, public_source_columns)
    write_csv(
        evidence_dir / "证据笔记_49.csv",
        evidence_notes,
        [
            "evidence_id", "object_type", "object_id", "claim", "source_id",
            "evidence_summary_or_short_quote", "source_locator", "evidence_level",
            "reviewer_status", "review_decision", "locator_status", "interpretation_limit",
        ],
    )

    joined: list[dict[str, str]] = []
    embedded: list[dict[str, str]] = []
    excluded: list[dict[str, str]] = []
    for archive in archive_rows:
        source = source_by_id.get(archive["source_id"], {})
        source_type = source.get("source_type", "")
        status = archive.get("archive_status", "")
        include = source_type in OFFICIAL_ARCHIVE_TYPES and status in {"archived", "manual_archived"}
        embedded_path = ""
        reason = ""
        if include:
            raw = ROOT / Path(archive["local_path"])
            meta = ROOT / Path(archive["metadata_path"])
            source_target = archive_dir / archive["source_id"]
            safe_copy(raw, source_target / raw.name)
            safe_copy(meta, source_target / "metadata.json")
            embedded_path = str((Path("05_官方一手证据归档") / archive["source_id"] / raw.name).as_posix())
            reason = "官方／法院／议会等一手材料，随包供项目核验"
        elif status in {"failed", "skipped_non_url_reference"}:
            reason = "归档未成功或非URL来源；保留网址、定位与状态"
        else:
            reason = "非官方网页、新闻、研究或组织材料；为控制版权与传播边界，仅提供索引、定位与哈希"

        row = {
            "source_id": archive["source_id"],
            "source_type": source_type,
            "title": archive.get("title", ""),
            "year": source.get("year", ""),
            "url": archive.get("url", ""),
            "archive_status": status,
            "content_type": archive.get("content_type", ""),
            "http_status": archive.get("http_status", ""),
            "sha256": archive.get("sha256", ""),
            "embedded": "yes" if include else "no",
            "embedded_path": embedded_path,
            "handling_note": reason,
        }
        joined.append(row)
        (embedded if include else excluded).append(row)

    write_csv(evidence_dir / "归档总清单_295.csv", joined)
    write_csv(evidence_dir / "随包嵌入的一手证据清单.csv", embedded)
    write_csv(evidence_dir / "未随包嵌入的来源清单.csv", excluded)

    if len(sources) != 295 or len(evidence_notes) != 49 or len(joined) != 295:
        raise AssertionError("source/evidence archive counts do not match the current freeze")
    if any(row["source_type"] not in OFFICIAL_ARCHIVE_TYPES for row in embedded):
        raise AssertionError("non-official archive leaked into embedded evidence")

    return {
        "sources": len(sources),
        "evidence_notes": len(evidence_notes),
        "archive_manifest_rows": len(joined),
        "embedded_official_archives": len(embedded),
        "not_embedded_sources": len(excluded),
    }, embedded


def copy_methods() -> None:
    target = STAGE / "06_方法与口径"
    safe_copy(ROOT / "data" / "metadata" / "coding_schema_v1.md", target / "编码与展示状态规则_v1.md")
    safe_copy(ROOT / "data" / "metadata" / "coding_schema_v0.md", target / "基础编码方案_v0.md")
    safe_copy(
        ROOT / "docs" / "research_publication_architecture_v1.md",
        target / "研究发布架构_v1.md",
    )


def write_readme(table_counts: dict[str, int], evidence_counts: dict[str, int], release: dict[str, object]) -> None:
    readme = f"""# 第三次进度同步：研究数据与证据附件 v1

生成日期：{TODAY.isoformat()}  
数据状态：2026-07-20 人工复核合并层；前端发布为 `{release['publication_profile']}` / `{release['publication_release_id']}`  
仓库提交：`{git_value('rev-parse', 'HEAD')}`

## 这个附件包含什么

1. `01_当前数据`：当前组织、议题、地点、关系、事件、案件、公投、制度转译和县政府协作表；
2. `02_前端冻结数据`：网站本轮实际读取的不可变 JSON 发布包，已核层与研究层物理分开；
3. `03_图表与底表`：第三次同步使用的截图和相关统计底表；
4. `04_证据索引`：295 条来源、49 条证据笔记，以及全部归档状态、网址、哈希和嵌入情况；
5. `05_官方一手证据归档`：{evidence_counts['embedded_official_archives']} 份已成功归档的官方、法院、议会等一手材料；
6. `06_方法与口径`：证据等级、人工复核、展示层和关系语法。

## 主要数据边界

- 组织登记表为 122 条历史记录；当前有效组织为 121 个，A072 是并入 A071 的 provenance tombstone。
- 当前组织—议题关系 283 条：141 条人工复核，142 条候选。
- 当前组织—地点关系 130 条：53 条人工复核，77 条候选。
- 306 条组织—地点—议题三元组要求三者来自同一份材料；其中 81 条两侧关系都已人工复核。
- 共同署名、共同声明或同场出现是事件参与，不自动构成稳定联盟。
- 资助机会、项目总成本、赞助层级与实际拨款分开编码。
- `review_status`、`claim_status` 与 `graph_eligibility` 的含义见 `06_方法与口径/编码与展示状态规则_v1.md`。

## 怎样核验证据

1. 从数据表的 `source_ref` / `source_id` 找到 `04_证据索引/来源索引_295.csv`；
2. 查看网址、证据等级、偏差说明和 locator；
3. 在 `归档总清单_295.csv` 查看归档状态与 SHA-256；
4. `embedded=yes` 的记录可在 `05_官方一手证据归档/Sxxx/` 直接打开；
5. 其他材料请按原始网址访问。未嵌入不代表证据无效，只表示本附件不再分发其网页全文。

## 使用与版权

本附件用于项目阶段核验和研究沟通。项目整理的数据表、编码说明和有限证据摘录可以随同步文档使用；原始材料的权利仍属于原发布机构。包内只嵌入官方、法院、议会等一手公开记录，新闻全文、学术文章全文、组织网页镜像和内部人工任务字段没有随包分发。引用时应优先引用原始网址和发布机构。

## 当前表数量

"""
    for name, count in table_counts.items():
        readme += f"- `{name}`：{count} 行\n"
    readme += f"""

## 完整性

- 文件清单：`manifest.csv`
- 内容校验：`checksums.sha256`
- ZIP 内所有文件使用固定时间戳生成，便于重复构建比对。
"""
    (STAGE / "README_使用说明.md").write_text(readme, encoding="utf-8")


def write_version(table_counts: dict[str, int], evidence_counts: dict[str, int], release: dict[str, object]) -> None:
    version = {
        "schema_version": "third_sync_data_evidence_bundle_v1",
        "generated_on": TODAY.isoformat(),
        "repository_commit": git_value("rev-parse", "HEAD"),
        "repository_dirty_before_manifest": source_worktree_dirty(),
        "frontend_release": release,
        "table_counts": table_counts,
        "evidence_counts": evidence_counts,
        "publication_boundary": {
            "embedded_archive_policy": "official_primary_public_records_only",
            "news_fulltext_embedded": False,
            "academic_fulltext_embedded": False,
            "organization_web_mirrors_embedded": False,
            "internal_review_task_fields_exported": False,
        },
    }
    (STAGE / "版本与计数.json").write_text(
        json.dumps(version, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def write_manifests() -> None:
    files = sorted(path for path in STAGE.rglob("*") if path.is_file())
    rows: list[dict[str, str]] = []
    for path in files:
        rel = path.relative_to(STAGE).as_posix()
        rows.append(
            {
                "relative_path": rel,
                "bytes": str(path.stat().st_size),
                "sha256": sha256(path),
                "category": rel.split("/", 1)[0] if "/" in rel else "root",
            }
        )
    write_csv(STAGE / "manifest.csv", rows)

    checksum_lines = [f"{row['sha256']}  {row['relative_path']}" for row in rows]
    (STAGE / "checksums.sha256").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")


def build_zip() -> tuple[int, int]:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    files = sorted(path for path in STAGE.rglob("*") if path.is_file())
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            arcname = (Path(STAGE.name) / path.relative_to(STAGE)).as_posix()
            info = zipfile.ZipInfo(arcname, ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(ZIP_PATH, "r") as archive:
        bad = archive.testzip()
        if bad:
            raise AssertionError(f"corrupt ZIP member: {bad}")
        return len(archive.infolist()), ZIP_PATH.stat().st_size


def main() -> None:
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)

    table_counts = export_tables()
    release = copy_publication_payload()
    copy_figures()
    evidence_counts, _ = export_evidence()
    copy_methods()
    write_readme(table_counts, evidence_counts, release)
    write_version(table_counts, evidence_counts, release)
    write_manifests()
    member_count, zip_size = build_zip()
    safe_copy(STAGE / "README_使用说明.md", OUT_README)
    shutil.rmtree(STAGE)

    summary = {
        "zip": str(ZIP_PATH.relative_to(ROOT)),
        "zip_bytes": zip_size,
        "zip_mib": round(zip_size / 1024 / 1024, 2),
        "zip_members": member_count,
        "embedded_official_archives": evidence_counts["embedded_official_archives"],
        "status": "PASS",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
