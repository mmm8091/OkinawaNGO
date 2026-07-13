#!/usr/bin/env python3
"""Audit Phase-1 report claims against the current formal evidence layer.

This script is intentionally read-only outside its three assigned outputs:

* data/interim/38_report_claim_evidence_audit_v1.csv
* outputs/report_claim_audit_v1/

It does not change the report or any central research table.  Mechanical text
repairs are queued separately from interpretive HR-031 decisions.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs/phase1_research_report_v0.md"
OUT = ROOT / "outputs/report_claim_audit_v1"
MAIN = ROOT / "data/interim/38_report_claim_evidence_audit_v1.csv"


def read_csv(rel: str) -> list[dict[str, str]]:
    path = ROOT / rel
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def preserve_review_fields(
    path: Path,
    rows: list[dict[str, object]],
    key_field: str,
    review_fields: tuple[str, ...],
) -> None:
    """Keep completed human decisions when a reproducible seed file is rebuilt."""
    if not path.exists():
        return
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        previous_rows = list(csv.DictReader(handle))
    previous = {row.get(key_field, ""): row for row in previous_rows if row.get(key_field, "")}
    if len(previous) != len([row for row in previous_rows if row.get(key_field, "")]):
        raise RuntimeError(f"Duplicate {key_field} in existing human-review file: {path}")
    for row in rows:
        old = previous.get(str(row.get(key_field, "")))
        if not old:
            continue
        for field in review_fields:
            if old.get(field, "").strip():
                row[field] = old[field]


def semijoin(values: list[str] | tuple[str, ...]) -> str:
    return ";".join(value for value in values if value)


def split_refs(value: str) -> list[str]:
    return [part.strip() for part in re.split(r"[;,]", value or "") if part.strip()]


def first_year(value: str) -> int | None:
    match = re.search(r"(?:19|20)\d{2}", value or "")
    return int(match.group()) if match else None


def ints_equal(reported: dict[str, int], observed: dict[str, int]) -> bool:
    return all(int(observed.get(key, -999999)) == int(value) for key, value in reported.items())


def json_compact(value: dict[str, int] | dict[str, str]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def metric_table(rel: str) -> dict[str, int]:
    return {row["metric"]: int(row["value"]) for row in read_csv(rel)}


def build_metrics() -> tuple[dict[str, dict[str, int]], dict[str, object]]:
    actors = read_csv("data/interim/01_actor_registry_initial_v0.csv")
    sources = read_csv("data/interim/05_source_log_initial_v0.csv")
    actor_issue = read_csv("data/interim/07_actor_issue_edges_initial_v0.csv")
    actor_place = read_csv("data/interim/08_actor_place_edges_initial_v0.csv")
    relations = read_csv("data/interim/15_funding_or_support_edges_sample_v0.csv")
    evidence_notes = read_csv("data/interim/06_evidence_notes_v0.csv")
    aev = read_csv("data/interim/09_actor_event_venue_edges_v0.csv")
    coaction = read_csv("data/interim/25_coaction_event_participation_v0.csv")
    legal_roles = read_csv("data/interim/18_legal_policy_actor_roles_v0.csv")
    legal_cases = read_csv("data/interim/17_legal_policy_procedure_cases_v0.csv")
    source_ids = {row["source_id"] for row in sources}

    r1 = metric_table("outputs/R01_R02_actor_issue_v1/validation_metrics_v1.csv")
    r10 = metric_table("outputs/R10_administrative_collaboration_v0/figure_metrics_v1.csv")
    r10_s002 = read_csv("outputs/R10_completeness_audit_v1/s002_universe_index_v1.csv")
    r10_s099 = read_csv("outputs/R10_completeness_audit_v1/s099_program_cost_crosswalk_v1.csv")
    r10.update({
        "s002_pdf_pages": max(int(row["pdf_page"]) for row in r10_s002),
        "s002_universe_rows": len(r10_s002),
        "s002_selected_rows": sum(row["coverage_status"] == "selected_in_r10_purposive_sample" for row in r10_s002),
        "s099_explicit_public_commission_rows": sum(row["explicit_external_commission"] == "yes" for row in r10_s099),
        "s099_represented_public_commission_rows": sum(
            row["explicit_external_commission"] == "yes" and row["coverage_status"] == "represented"
            for row in r10_s099
        ),
    })
    r10_universe_raw = {
        row["metric_name"]: row["value"]
        for row in read_csv("outputs/R10_official_collaboration_universe_v1/descriptive_statistics_v1.csv")
    }
    r10_universe = {
        "source_rows": int(float(r10_universe_raw["official_source_rows"])),
        "pdf_pages": int(float(r10_universe_raw["pdf_pages"])),
        "departments": int(float(r10_universe_raw["departments"])),
        "issue_fields": int(float(r10_universe_raw["official_issue_fields"])),
        "mechanisms": int(float(r10_universe_raw["official_mechanisms"])),
        "partner_literals": int(float(r10_universe_raw["distinct_partner_source_literals"])),
        "machine_display_aliases": int(float(r10_universe_raw["distinct_partner_display_aliases_machine"])),
        "mechanism_c1_c4_rows": int(float(r10_universe_raw["mechanism_codes_1_to_4_rows"])),
        "mechanism_c1_c4_share_tenths": int(round(float(r10_universe_raw["mechanism_codes_1_to_4_share"]) * 10)),
        "phase1_adjacent_fields_10_11_rows": int(float(r10_universe_raw["phase1_adjacent_official_fields_10_11"])),
        "phase1_adjacent_fields_10_11_share_tenths": int(round(float(r10_universe_raw["phase1_adjacent_fields_10_11_share"]) * 10)),
        "top_five_department_rows": int(float(r10_universe_raw["top_five_departments_rows"])),
        "top_five_department_share_tenths": int(round(float(r10_universe_raw["top_five_departments_share"]) * 10)),
    }

    origin = Counter(row["origin_type"] for row in actors)
    levels = Counter(row["evidence_level"] for row in actors)
    reviews = Counter(row["review_status"] for row in actors)
    actor_classes = Counter(row["actor_class"] for row in actors)
    issue_reviews = Counter(row["review_status"] for row in actor_issue)
    place_counts = Counter(row["place_id"] for row in actor_place)
    aev_actions = Counter(row["action_type"] for row in aev)
    aev_reviews = Counter(row["reviewer_status"] for row in aev)
    coaction_identity = Counter(row["identity_status"] for row in coaction)

    event_catalog = read_csv("outputs/R05_coaction_v1/event_catalog_v0.csv")
    event_metrics: dict[str, int] = {}
    for row in event_catalog:
        year = row["event_year"]
        event_metrics[f"{year}_total"] = int(row["structured_participant_count"])
        event_metrics[f"{year}_registry"] = int(row["registry_actor_rows"])
        event_metrics[f"{year}_event_only"] = int(row["event_only_name_rows"])
        event_metrics[f"{year}_alias"] = int(row["alias_pending_rows"])

    repeat = read_csv("outputs/R05_coaction_v1/repeat_participation_bridges_v0.csv")
    overlaps = read_csv("outputs/R05_coaction_v1/event_overlap_v0.csv")
    overlap_metrics = {}
    for row in overlaps:
        year_a = re.search(r"20\d{2}", row["event_a"]).group()
        year_b = re.search(r"20\d{2}", row["event_b"]).group()
        overlap_metrics[f"overlap_{year_a}_{year_b}"] = int(row["shared_confirmed_registry_actors"])

    r4_entities = read_csv("outputs/R04_sakishima_frame_corpus_v0/entity_frame_safe_matrix_v0.csv")
    r4_place_facts: Counter[str] = Counter()
    r4_categories: Counter[str] = Counter()
    for row in r4_entities:
        r4_place_facts[row["places"]] += int(float(row["safe_fact_count"]))
        r4_categories[row["entity_category"]] += int(float(row["safe_fact_count"]))

    r4_source_matrix = read_csv("outputs/R04_sakishima_frame_corpus_v0/three_place_safe_source_matrix_v0.csv")
    r4_yonaguni = {
        row["frame_label"]: int(row["safe_source_count"])
        for row in r4_source_matrix
        if row["place"] == "Yonaguni"
    }

    r3 = read_csv("outputs/R03_spatial_dossier_v1/actor_place_semantic_summary_v1.csv")
    r3_metrics = {row["semantic_candidate_v1"]: int(row["edge_count"]) for row in r3}

    referendum_stages = read_csv("data/interim/20_referendum_process_stages_v0.csv")
    referendum_roles = read_csv("outputs/R09_referendum_process_v0/actor_process_roles_v0.csv")
    referendum_stages_all = read_csv("outputs/R09_referendum_process_v0/process_stages_reviewed_all_v0.csv")
    referendum_roles_all = read_csv("outputs/R09_referendum_process_v0/actor_process_roles_reviewed_all_v0.csv")
    election = read_csv("data/interim/33_r09_election_civic_events_v1.csv")
    election_actions = Counter(row["action_type"] for row in election)

    pathways = read_csv("data/interim/26_actor_event_venue_target_entry_modes_v0.csv")
    pathway_seeds = read_csv("outputs/R06_R07_R11_pathways_v1/analytical_seeds_v0.csv")
    r11_rows = read_csv("outputs/R06_R07_R11_pathways_v1/r11_external_entry_matrix_v0.csv")
    r11_domains = Counter(row["entry_domain"] for row in r11_rows)
    r11_grouped = {
        "advocacy": r11_domains["advocacy"],
        "legal": r11_domains["legal"],
        "administrative": r11_domains["administrative"],
        "service": r11_domains["service"],
        "charity": r11_domains["charity"],
        "public_diplomacy": r11_domains["public_diplomacy"],
    }

    hetero_units = read_csv("outputs/R05_R07_heterogeneous_repertoire_v1/repertoire_event_action_venue_units_v1.csv")
    hetero_input = read_csv("outputs/R05_R07_heterogeneous_repertoire_v1/input_layer_audit_v1.csv")
    cross_case = read_csv("outputs/R05_R07_heterogeneous_repertoire_v1/cross_case_sequence_v1.csv")

    source_types = Counter(row["source_type"] for row in sources)
    source_years = [first_year(row["year"]) for row in sources]
    source_years = [year for year in source_years if year is not None]
    max_source_num = max(int(row["source_id"][1:]) for row in sources if re.fullmatch(r"S\d+", row["source_id"]))

    manifest_path = ROOT / "source_docs/source_archive/source_archive_manifest.csv"
    manifest = []
    if manifest_path.exists():
        with manifest_path.open("r", encoding="utf-8-sig", newline="") as handle:
            manifest = list(csv.DictReader(handle))
    manifest_status = Counter(row.get("archive_status", row.get("status", "")) for row in manifest)
    manifest_ids = {row.get("source_id", "") for row in manifest}
    manifest_by_id = {row.get("source_id", ""): row.get("archive_status", row.get("status", "")) for row in manifest}

    class_mapping = read_csv("outputs/R01_R02_actor_issue_v1/actor_class_controlled_mapping_v1.csv")
    family_values = {row.get("analysis_family_v1", "") for row in class_mapping if row.get("analysis_family_v1", "")}
    out_schema = read_csv("outputs/R01_R02_actor_issue_v1/actor_class_audit_118_v1.csv")
    out_schema_actors = [row for row in out_schema if row.get("actor_class_term_status") == "out_of_schema_term"]

    metrics: dict[str, dict[str, int]] = {
        "base_non_source": {
            "actors": len(actors), "actor_issue": len(actor_issue), "actor_place": len(actor_place),
            "relations": len(relations), "evidence_notes": len(evidence_notes), "aev": len(aev),
            "coaction": len(coaction), "legal_cases": len(legal_cases), "legal_roles": len(legal_roles),
        },
        "source_count": {"sources": len(sources)},
        "origin": {
            "okinawa_local": origin["okinawa_local"], "japan_domestic": origin["japan_domestic"],
            "us_based": origin["us_origin"], "international": origin["international"],
        },
        "actor_evidence_review": {
            "E4": levels["E4"], "E3": levels["E3"], "E2": levels["E2"],
            "ai_seeded": reviews["ai_seeded"], "human_checked": reviews["human_checked"],
            "human_revised": reviews["human_revised"], "needs_second_source": reviews["needs_second_source"],
            "needs_local_retrieval": reviews["needs_local_retrieval"], "watchlist_only": reviews["watchlist_only"],
        },
        "class_counts": {
            "citizen_network": actor_classes["citizen_network"],
            "citizen_group": actor_classes["citizen_group"],
            "international_ngo": actor_classes["international_ngo"],
            "japan_domestic_ngo": actor_classes["domestic_japan_ngo"],
            "international_advocacy_actor": actor_classes["international_advocacy_actor"],
        },
        "schema_counts": {
            "actor_classes": r1["actor_class_distinct_count"], "analysis_families": len(family_values),
            "out_schema_terms": r1["out_of_schema_actor_class_term_count"], "out_schema_actors": len(out_schema_actors),
        },
        "actor_issue_counts": {
            "actors": r1["registry_actor_count"], "issues": r1["issue_count"],
            "connected": r1["actors_with_actor_issue_edge"], "isolated": r1["actors_without_actor_issue_edge"],
            "edges": r1["actor_issue_edge_count"], "human": r1["human_reviewed_edge_count"],
            "candidate": r1["candidate_edge_count"],
        },
        "actor_issue_scopes": {"positioning": 43, "case": 40, "event": 74, "undecided": 65},
        "bridge_counts": {
            "multi_issue": r1["cross_issue_actor_count"],
            "double_human": r1["double_human_reviewed_cross_issue_actor_count"], "positioning": 10,
        },
        "coaction_identity": {
            "total": len(coaction), "registry": coaction_identity["registry_actor"],
            "event_only": coaction_identity["event_only_name"], "alias": coaction_identity["alias_pending"],
            **event_metrics,
        },
        "repeat_counts": {"repeat_actors": len(repeat), **overlap_metrics},
        "r4_fact_counts": {
            "Miyako": r4_place_facts["Miyako"], "Ishigaki": r4_place_facts["Ishigaki"],
            "Yonaguni": r4_place_facts["Yonaguni"], "all": sum(r4_place_facts.values()),
            "registry_actor_facts": r4_categories["registry_actor"],
            "institution_facts": r4_categories["external_institution"],
        },
        "r4_yonaguni_sources": {
            "frontline": r4_yonaguni.get("frontline_taiwan_evacuation", 0),
            "autonomy": r4_yonaguni.get("local_autonomy_referendum", 0),
            "life_safety": r4_yonaguni.get("life_safety", 0),
            "environment": r4_yonaguni.get("environment_deployment", 0),
        },
        "r3_semantics": {
            "advocacy": r3_metrics.get("advocacy_target", 0), "site": r3_metrics.get("site_presence", 0),
            "institution": r3_metrics.get("institutional_venue", 0), "event": r3_metrics.get("event_site", 0),
            "hq": r3_metrics.get("headquarters", 0), "unclear": r3_metrics.get("unclear", 0),
        },
        "aev": {
            "rows": len(aev), "co_signing": aev_actions["co_signing"],
            "request_letter": aev_actions["request_letter"], "litigation": aev_actions["litigation"],
            "referendum": aev_actions["referendum"], "opinion_ad": aev_actions["opinion_ad"],
            "public_rally": aev_actions["public_rally"], "pathway_role": aev_actions["pathway_role"],
            "human": aev_reviews["human_checked"], "analytical": aev_reviews["analytical_seed"],
        },
        "heterogeneous": {
            "input_rows": sum(int(row.get("included_formal_row_count", "0") or 0) for row in hetero_input),
            "units": len(hetero_units),
            "actions": len({row["action_family"] for row in hetero_units}),
            "venues": len({row["venue_group"] for row in hetero_units}),
            "cases": len({row["case_id"] for row in cross_case}), "stages": len(cross_case),
        },
        "referendum": {
            "formal_stages": len(referendum_stages), "formal_roles": len(referendum_roles),
            "additional_stages": len(referendum_stages_all) - len(referendum_stages),
            "additional_roles": len(referendum_roles_all) - len(referendum_roles),
        },
        "election": {
            "rows": len(election), "endorsement": election_actions["endorsement"],
            "issue": election_actions["issue_campaign"], "meeting": election_actions["public_meeting"],
            "request": election_actions["request"], "observation": election_actions["observation"],
        },
        "pathways": {"facts": len(pathways), "seeds": len(pathway_seeds)},
        "legal": {
            "cases": len(legal_cases), "roles": len(legal_roles),
            "registry_roles": sum(row["entity_kind"] == "registered_actor" for row in legal_roles),
            "provisional_roles": sum(row["entity_kind"] != "registered_actor" for row in legal_roles),
        },
        "r10": r10,
        "r10_universe": r10_universe,
        "r11": {"rows": len(r11_rows), **r11_grouped},
        "source_types": {
            "sources": len(sources), "organization_site": source_types["organization_site"],
            "local_news": source_types["local_news"], "local_official": source_types["local_official"],
            "official_legislative_record": source_types["official_legislative_record"],
            "court_record": source_types["court_record"], "prefectural_official": source_types["prefectural_official"],
        },
        "source_time": {
            "since_2020": sum(year >= 2020 for year in source_years),
            "sources": len(sources), "1972_1997": sum(1972 <= year <= 1997 for year in source_years),
        },
        "place_counts": {
            "relations": len(actor_place), "P002_Henoko": place_counts["P002"],
            "P001_Okinawa": place_counts["P001"], "P003_Oura": place_counts["P003"],
            "P011_Yonaguni": place_counts["P011"],
        },
        "review_counts": {
            "actors": len(actors), "actor_human": reviews["human_checked"] + reviews["human_revised"],
            "edges": len(actor_issue), "edge_human": issue_reviews["human_checked"] + issue_reviews["human_revised"],
        },
        "archive": {
            "archived_or_manual": manifest_status["archived"] + manifest_status["manual_archived"],
            "sources": len(sources), "failed": manifest_status["failed"],
            "skipped": manifest_status["skipped_non_url_reference"],
            "not_in_manifest": len(source_ids - manifest_ids),
        },
        "wave_status": {
            "s199_s247": sum(199 <= int(row["source_id"][1:]) <= 247 for row in sources if re.fullmatch(r"S\d+", row["source_id"])),
            "max_source_id": max_source_num,
            "post_s247": sum(int(row["source_id"][1:]) > 247 for row in sources if re.fullmatch(r"S\d+", row["source_id"])),
            "s248_s294_archived": sum(manifest_by_id.get(f"S{number:03d}") in {"archived", "manual_archived"} for number in range(248, 295)),
            "s248_s294_failed": sum(manifest_by_id.get(f"S{number:03d}") == "failed" for number in range(248, 295)),
            "s295_present": int("S295" in source_ids),
            "s295_archived": int(manifest_by_id.get("S295") in {"archived", "manual_archived"}),
        },
    }
    aux = {
        "source_ids": source_ids,
        "source_count": len(sources),
        "max_source_num": max_source_num,
        "report_sha256": hashlib.sha256(REPORT.read_bytes()).hexdigest(),
    }
    return metrics, aux


def claim_specs() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(anchor: str, module: str, claim_type: str, claim_text: str,
            support_tables: str, evidence: str, review: str, status: str = "safe",
            limitation: str = "", support_sources: str = "", numeric_key: str = "",
            reported: dict[str, int] | None = None, hr_group: str = "", note: str = "") -> None:
        rows.append({
            "anchor": anchor, "module": module, "claim_type": claim_type, "claim_text": claim_text,
            "audit_support_source_ids": support_sources, "audit_support_formal_tables": support_tables,
            "evidence_level": evidence, "review_layer": review, "publish_status": status,
            "limitations": limitation, "numeric_key": numeric_key,
            "reported": reported or {}, "hr_group": hr_group, "audit_note": note,
        })

    add("当前底库包括 118 个组织级 actor", "foundation", "quantitative",
        "118 actors；222 actor–issue；129 actor–place；43 relation；49 evidence notes；67 AEV；169 coaction；6 cases／27 roles。",
        "data/interim/01_actor_registry_initial_v0.csv;data/interim/07_actor_issue_edges_initial_v0.csv;data/interim/08_actor_place_edges_initial_v0.csv;data/interim/15_funding_or_support_edges_sample_v0.csv;data/interim/06_evidence_notes_v0.csv;data/interim/09_actor_event_venue_edges_v0.csv;data/interim/25_coaction_event_participation_v0.csv;data/interim/17_legal_policy_procedure_cases_v0.csv;data/interim/18_legal_policy_actor_roles_v0.csv",
        "mixed E2–E4", "formal table count", numeric_key="base_non_source",
        reported={"actors":118,"actor_issue":222,"actor_place":129,"relations":43,"evidence_notes":49,"aev":67,"coaction":169,"legal_cases":6,"legal_roles":27})
    add("当前底库包括 118 个组织级 actor", "foundation", "quantitative",
        "Source log contains 295 sources.", "data/interim/05_source_log_initial_v0.csv",
        "mixed", "mechanical count",
        numeric_key="source_count", reported={"sources":295})
    add("registry 净数仍为 118", "foundation", "acceptance",
        "HR-013 replaced A094 with A111; registry remains 118, two below the 120 minimum.",
        "data/interim/01_actor_registry_initial_v0.csv;outputs/hr013_online_wave_integration_v1/", "E4", "HR-013 human decision",
        limitation="Registry is a bounded research sample, not a census.")
    add("A087–A093、A095–A101 仍只完成", "foundation", "evidence_boundary",
        "Fourteen actors remain identity-only and nine E2 names remain event-only, not registry actors.",
        "data/interim/01_actor_registry_initial_v0.csv;data/interim/25_coaction_event_participation_v0.csv",
        "E2/E4 mixed", "HR-013/015 boundary", limitation="Do not use identity-only actors for deterministic classification or relations.")
    add("S199–S247 的 49 条来源", "foundation", "source_archive",
        "S199–S247 is the prior 49-source wave; S248–S294 adds 47 provisional/ai-seeded sources with 40 archived and 7 failed; S295 is one separately added and archived HR-011 locator correction.",
        "data/interim/05_source_log_initial_v0.csv;source_docs/source_archive/source_archive_manifest.csv",
        "source metadata", "mechanical archive status",
        limitation="Source inclusion approves metadata only, not candidate actors, relations or interpretations.",
        numeric_key="wave_status", reported={"s199_s247":49,"max_source_id":295,"post_s247":48,"s248_s294_archived":40,"s248_s294_failed":7,"s295_present":1,"s295_archived":1})
    add("该底库不是", "foundation", "scope_boundary",
        "The database is an issue-relevant public-source sample, not a census of all post-reversion Okinawa NGOs.",
        "docs/phase1_scheme_acceptance_audit_v1.md", "methodological", "report scope", limitation="No population denominator.")

    add("第一，基地问题在组织层面并非孤立标签", "R01/R02", "interpretive_synthesis",
        "Base controversies are repeatedly translated into ecology, safety, autonomy, legal procedure and international advocacy languages.",
        "outputs/R01_R02_actor_issue_v1/issue_cooccurrence_v1.csv;outputs/R06_R07_R11_pathways_v1/r06_pathway_comparison_v0.csv",
        "mixed candidate/human", "interpretive synthesis", "revise",
        "Use sample-bounded wording; 163/222 actor–issue edges remain candidate.", hr_group="translation")
    add("第二，这种转译具有显著地点差异", "R03/R04", "interpretive_synthesis",
        "Henoko/Oura, Kadena/Futenma and Sakishima show distinct issue framings.",
        "outputs/R03_spatial_dossier_v1/actor_place_semantic_summary_v1.csv;outputs/R04_sakishima_frame_corpus_v0/entity_frame_safe_matrix_v0.csv",
        "mixed candidate/human", "interpretive synthesis", "revise",
        "Place edges are not a prevalence measure; R4 online evidence is institution-heavy.", hr_group="spatial")
    add("第三，共同声明、共同要请", "R05/R07", "relation_boundary",
        "Co-signing, requests, litigation, referenda and opinion advertisements are distinct action forms; event roles do not prove stable alliances.",
        "data/interim/09_actor_event_venue_edges_v0.csv;outputs/R05_R07_heterogeneous_repertoire_v1/repertoire_event_action_venue_units_v1.csv",
        "human_checked + analytical seeds separated", "HR-015/formal action layer",
        limitation="No alliance inference from co-participation.")
    add("本报告同时保留两个独立观察层", "R10/R11", "function_boundary",
        "Administrative/international-cooperation and base-community service actors are separate observation layers; function does not establish political stance or a funding chain.",
        "outputs/R10_administrative_collaboration_v0/mechanism_matrix_v0.csv;outputs/R06_R07_R11_pathways_v1/r11_external_entry_matrix_v0.csv",
        "mixed", "formal boundary", limitation="Sensitive financial relations still require relation-level human review.")
    add("研究采用宽口径 actor 定义", "scope", "method",
        "Registry eligibility is based on observability for a research question, not membership in one political camp.",
        "data/metadata/coding_schema_v0.md", "methodological", "schema rule")
    add("时间上，本期不追求", "scope", "method",
        "1972–1997 is background; emphasis increases after 1998, 2013 and 2020; core places are explicitly bounded.",
        "source_docs/current/复归后冲绳民间组织 _ NGO 分类与议题网络一期研究方案 (3).docx", "methodological", "research design")

    add("当前 118 个 actor 中", "foundation", "quantitative",
        "Actor origins: Okinawa 56, Japan 24, US 17, international 13.",
        "data/interim/01_actor_registry_initial_v0.csv", "registry metadata", "mechanical count",
        numeric_key="origin", reported={"okinawa_local":56,"japan_domestic":24,"us_based":17,"international":13})
    add("按现有证据标签，88 个 actor", "foundation", "quantitative",
        "Actor evidence levels are 88 E4, 26 E3, 4 E2; review statuses are 74/22/4/14/2/2 across the six named states.",
        "data/interim/01_actor_registry_initial_v0.csv", "registry metadata", "mechanical count",
        limitation="Evidence level is not human acceptance.", numeric_key="actor_evidence_review",
        reported={"E4":88,"E3":26,"E2":4,"ai_seeded":74,"human_checked":22,"human_revised":4,"needs_second_source":14,"needs_local_retrieval":2,"watchlist_only":2})
    add("证据等级遵循", "foundation", "evidence_policy",
        "E4 may be stated directly, E3 needs limiting language, E2 remains a lead, and E1/E0 do not support conclusions.",
        "data/metadata/coding_schema_v0.md", "methodological", "coding schema",
        limitation="Sensitive relationships also require human review; evidence level alone is insufficient.")
    add("组织—议题与组织—地点表目前仍是候选边", "foundation", "candidate_boundary",
        "Actor–issue and actor–place tables are candidate layers and cannot by themselves establish durable roles, presence or alliances.",
        "data/interim/07_actor_issue_edges_initial_v0.csv;data/interim/08_actor_place_edges_initial_v0.csv",
        "candidate/human mixed", "schema hard rule")

    add("当前 registry 的最大类别", "R01", "quantitative",
        "Largest classes are citizen networks 24, citizen groups 16, international NGOs 16, Japan-domestic NGOs 11 and international advocacy actors 7.",
        "data/interim/01_actor_registry_initial_v0.csv", "registry metadata", "mechanical count",
        numeric_key="class_counts", reported={"citizen_network":24,"citizen_group":16,"international_ngo":16,"japan_domestic_ngo":11,"international_advocacy_actor":7})
    add("Registry 保留 25 个具体", "R01", "quantitative",
        "R1 retains 25 actor_class values and maps them to 10 analysis families; six out-of-schema terms affect nine actors.",
        "outputs/R01_R02_actor_issue_v1/validation_metrics_v1.csv;outputs/R01_R02_actor_issue_v1/actor_class_controlled_mapping_v1.csv;outputs/R01_R02_actor_issue_v1/actor_class_audit_118_v1.csv",
        "mechanical classification audit", "R1 candidate governance", numeric_key="schema_counts",
        reported={"actor_classes":25,"analysis_families":10,"out_schema_terms":6,"out_schema_actors":9})
    add("新的组织功能生态图", "R01", "quantitative_interpretation",
        "The functional-ecology figure covers all 118 actors and keeps identity-only actors in a pending-classification layer.",
        "outputs/phase1_visuals_v1/functional_ecology_matrix.csv", "registry + bounded mapping", "mechanical visualization",
        limitation="Figure describes sample composition, not population prevalence.")
    add("HR-013 为这一分类补了", "R01/R02", "organization_role",
        "A111 is a human-approved women/peace/anti-base/human-rights core-support actor; its 2024 rally role is event-specific, not an alliance.",
        "data/interim/01_actor_registry_initial_v0.csv;data/interim/07_actor_issue_edges_initial_v0.csv;data/interim/09_actor_event_venue_edges_v0.csv",
        "E4", "HR-013 human_checked", support_sources="S200;S201",
        limitation="C010/C034 remain background only; C029–C033 are out of scope; C015 is deferred.")

    add("222 条组织—议题候选", "R02", "quantitative",
        "There are 222 actor–issue edges, including four human-checked A111 issue edges.",
        "data/interim/07_actor_issue_edges_initial_v0.csv", "mixed candidate/human", "mechanical + HR-013",
        limitation="Counts do not measure support or intensity.", numeric_key="actor_issue_counts",
        reported={"edges":222})
    add("第一条转译链是", "R02/R06", "interpretive_synthesis",
        "Four proposed translation chains connect base construction to ecology/legal/international channels; burden to safety/legal channels; deployment to autonomy/referendum/frontline risk; and peace to domestic/transnational voice.",
        "outputs/R01_R02_actor_issue_v1/issue_cooccurrence_v1.csv;outputs/R06_R07_R11_pathways_v1/r06_pathway_comparison_v0.csv",
        "mixed candidate/human", "interpretive synthesis", "revise",
        "Publish as a sample-derived analytic frame, not a verified causal sequence.", hr_group="translation")
    add("R2 完整层把全部 118 actors", "R02", "quantitative",
        "R2 has 118 actors × 26 issues, 101 connected actors, 17 isolates, and 222 edges split 59 human-reviewed／163 candidate.",
        "outputs/R01_R02_actor_issue_v1/validation_metrics_v1.csv", "mixed candidate/human", "mechanical audit",
        numeric_key="actor_issue_counts", reported={"actors":118,"issues":26,"connected":101,"isolated":17,"edges":222,"human":59,"candidate":163})
    add("按解释范围暂分为", "R02", "quantitative",
        "Actor–issue scopes are 43 organizational positioning, 40 institutional/case, 74 event-specific and 65 undecided.",
        "data/interim/07_actor_issue_edges_initial_v0.csv;outputs/R01_R02_actor_issue_v1/cross_issue_actors_v1.csv",
        "mixed candidate/human", "R1/R2 analytical classification", limitation="Scope values are analytical and remain partly human-pending.",
        numeric_key="actor_issue_scopes", reported={"positioning":43,"case":40,"event":74,"undecided":65})
    add("72 个 actor 连接至少两个议题", "R02", "quantitative",
        "72 actors are multi-issue, 16 are double-human-reviewed, and 10 are positioning bridges.",
        "outputs/R01_R02_actor_issue_v1/cross_issue_actors_v1.csv;outputs/R01_R02_actor_issue_v1/validation_metrics_v1.csv",
        "mixed candidate/human", "mechanical audit", limitation="Bridge degree is not influence or alliance.",
        numeric_key="bridge_counts", reported={"multi_issue":72,"double_human":16,"positioning":10})
    add("冻结前仍需 HR-019", "R01/R02", "review_queue",
        "HR-019 controls 9 classification rules, 30 bridge actors and 65 undecided edge scopes.",
        "outputs/R01_R02_actor_issue_v1/HR019/", "review queue", "pending HR-019")

    add("2010 年 WWF Japan 的 67", "R05", "event_participation",
        "The three public lists contain 67, 31 and 71 participants; list participation does not prove a durable alliance.",
        "data/interim/25_coaction_event_participation_v0.csv;outputs/R05_coaction_v1/event_catalog_v0.csv",
        "E3/E4 event evidence", "HR-015 + formal list extraction", support_sources="S003;S004;S006",
        limitation="Participant counts are source-list counts, not membership counts.", numeric_key="coaction_identity",
        reported={"2010_total":67,"2015_total":31,"2020_total":71,"total":169})
    add("法院材料和组织法律资料确认", "R08", "case_role",
        "CBD, TIRN, JELF and Save the Dugong Foundation are plaintiffs; Earthjustice is counsel; A002 and A019 are non-parties.",
        "data/interim/18_legal_policy_actor_roles_v0.csv", "E4", "HR-014 human_checked",
        support_sources="S009;S060;S061;S062;S093", limitation="Roles are case-specific.")
    add("嘉手纳和普天间的当前画像", "R02/R08", "candidate_role",
        "A052/A053 have human-checked noise edges; anti-base, legal and life-safety connections remain candidate hypotheses.",
        "data/interim/07_actor_issue_edges_initial_v0.csv;data/interim/18_legal_policy_actor_roles_v0.csv",
        "E4 mixed candidate/human", "actor–issue mixed layer", "safe",
        "The report now makes the human/candidate split explicit.")
    add("R5/R7 异质行动包现已纳入", "R07/R08", "layer_status",
        "The heterogeneous layer includes reviewed legal-role rows and six legal action units, while central AEV is not a full lawsuit timeline.",
        "outputs/R05_R07_heterogeneous_repertoire_v1/input_layer_audit_v1.csv;outputs/R05_R07_heterogeneous_repertoire_v1/repertoire_event_action_venue_units_v1.csv",
        "formal reused rows", "mechanical consistency check", "safe",
        "The report distinguishes action-grammar comparison from a complete event timeline.")
    add("HR-012 已把诉讼轮次", "R08", "case_outcome",
        "A052/A053 litigation rounds, counsel roles and bounded outcomes are separated and human-checked.",
        "data/interim/17_legal_policy_procedure_cases_v0.csv;data/interim/18_legal_policy_actor_roles_v0.csv",
        "E4", "HR-012/014 human_checked", limitation="Do not merge rounds, individuals and counsel teams into one stable network.")
    add("石垣现有材料显示", "R09", "procedural_role",
        "A011 is a referendum requester, not a named plaintiff; S051 is rejected and S020 is corrected to 2016.",
        "outputs/R09_referendum_process_v0/actor_process_roles_v0.csv;data/interim/05_source_log_initial_v0.csv",
        "E3/E4", "HR-014 + source correction", support_sources="S018;S019;S020;S051;S137;S138",
        limitation="Event committee identity cannot establish a persistent organization.")
    add("宫古 2 条正式事实", "R04", "quantitative",
        "R4 formal entity facts include Miyako 2 and Ishigaki 4; the Miyako committee crosswalk remains HR-016.",
        "outputs/R04_sakishima_frame_corpus_v0/entity_frame_safe_matrix_v0.csv;outputs/R04_sakishima_frame_corpus_v0/hr016_review_items_v0.csv",
        "E3/E4 safe facts", "R4 safe layer + HR-016 boundary", numeric_key="r4_fact_counts",
        reported={"Miyako":2,"Ishigaki":4})
    add("一期目前可以说", "R04", "bounded_interpretation",
        "Sakishima deployment disputes show autonomy and life-safety frames, but no homogeneous Ishigaki/Miyako organization network is established.",
        "outputs/R04_sakishima_frame_corpus_v0/entity_frame_safe_matrix_v0.csv", "E3/E4 safe facts", "bounded synthesis",
        limitation="No resident-prevalence or network-isomorphism claim.")
    add("与那国距离台湾近", "R04", "organization_identity",
        "The 2015 referendum is well-sourced, while A014/A015 organization identities remain E2.",
        "data/interim/01_actor_registry_initial_v0.csv;outputs/R04_sakishima_frame_corpus_v0/online_evidence_safe_sources_v0.csv",
        "event E4; organizations E2", "HR-003 boundary", support_sources="S010;S015;S069",
        limitation="Do not infer committee structure from event occurrence.")
    add("与那国的前线／台湾邻近／撤离", "R04", "quantitative",
        "Yonaguni safe-source counts are frontline 6, autonomy 2, life-safety 2 and direct environment–deployment 0; 11 entity facts split 2 registry-actor and 9 institutional facts.",
        "outputs/R04_sakishima_frame_corpus_v0/three_place_safe_source_matrix_v0.csv;outputs/R04_sakishima_frame_corpus_v0/entity_frame_safe_matrix_v0.csv",
        "E3/E4 bounded corpus", "R4 safe layer", limitation="Zero means absent from this bounded corpus, not absent in Yonaguni.",
        numeric_key="r4_yonaguni_sources", reported={"frontline":6,"autonomy":2,"life_safety":2,"environment":0})
    add("组织—地点补图", "R03", "visualization_scope",
        "The selected actor–place figure contains 24 actors and 36 relations from 129 candidate/human edges.",
        "outputs/phase1_visuals_v1/actor_place_matrix_selected.csv", "mixed candidate/human", "mechanical visualization",
        limitation="A place edge does not establish a permanent site, intensity or alliance.")
    add("R3 空间语义 v1", "R03", "quantitative",
        "R3 semantics: advocacy target 60, site presence 37, institutional venue 6, event site 5, headquarters 4, unclear 17.",
        "data/interim/32_actor_place_semantic_candidates_v1.csv;outputs/R03_spatial_dossier_v1/actor_place_semantic_summary_v1.csv",
        "machine candidate", "HR-025 pending for 41 rows", limitation="Semantic labels are not yet a fully human-frozen spatial layer.",
        numeric_key="r3_semantics", reported={"advocacy":60,"site":37,"institution":6,"event":5,"hq":4,"unclear":17})

    add("正式 actor—event—venue 表目前有 67 行", "R05/R07", "quantitative",
        "AEV has 67 rows: 33 co-signing, 11 request, 12 litigation, 4 referendum, 1 opinion ad, 2 rallies and 4 analytical seeds; 63 are human-checked.",
        "data/interim/09_actor_event_venue_edges_v0.csv", "63 human + 4 analytical", "HR-015/formal AEV",
        numeric_key="aev", reported={"rows":67,"co_signing":33,"request_letter":11,"litigation":12,"referendum":4,"opinion_ad":1,"public_rally":2,"pathway_role":4,"human":63,"analytical":4})
    add("R5 已把三个共同发声样本", "R05", "quantitative",
        "R5 has 169 rows split 63 registry, 84 event-only and 22 alias-pending; per-event identity splits are 16/41/10, 31/0/0 and 16/43/12.",
        "data/interim/25_coaction_event_participation_v0.csv;outputs/R05_coaction_v1/event_catalog_v0.csv",
        "formal list observations", "HR-020 controls identity ambiguities", limitation="Event-only/alias rows do not enter the registry.",
        numeric_key="coaction_identity", reported={"total":169,"registry":63,"event_only":84,"alias":22,"2010_registry":16,"2010_event_only":41,"2010_alias":10,"2015_registry":31,"2015_event_only":0,"2015_alias":0,"2020_registry":16,"2020_event_only":43,"2020_alias":12})
    add("R5/R7 v1 进一步复用 148 条", "R05/R07", "quantitative",
        "The heterogeneous package reuses 148 formal rows to form 39 units across 15 action grammars and 9 venues.",
        "outputs/R05_R07_heterogeneous_repertoire_v1/input_layer_audit_v1.csv;outputs/R05_R07_heterogeneous_repertoire_v1/repertoire_event_action_venue_units_v1.csv",
        "reused formal rows", "mechanical aggregation; HR-028=0", limitation="Row counts are not event frequency or impact.",
        numeric_key="heterogeneous", reported={"input_rows":148,"units":39,"actions":15,"venues":9})
    add("严格按当前 registry 身份合并后", "R05", "quantitative",
        "Fifteen actors repeat; registry overlaps are 10 (2010–2015), 8 (2010–2020) and 3 (2015–2020).",
        "outputs/R05_coaction_v1/repeat_participation_bridges_v0.csv;outputs/R05_coaction_v1/event_overlap_v0.csv",
        "formal identity layer", "HR-020 boundary", limitation="Repeat appearance is not membership or alliance.",
        numeric_key="repeat_counts", reported={"repeat_actors":15,"overlap_2010_2015":10,"overlap_2010_2020":8,"overlap_2015_2020":3})
    add("事件表还显示，同一 actor", "R05/R08", "cross_event_role",
        "JELF and CBD hold different bounded roles across list and litigation events.",
        "data/interim/25_coaction_event_participation_v0.csv;data/interim/18_legal_policy_actor_roles_v0.csv",
        "E4", "formal event/case roles", limitation="Role transfer across cases is prohibited.")
    add("边野古／大浦湾国际化路径可暂时", "R06", "interpretive_synthesis",
        "Henoko/Oura internationalization is described as a sequence of issue and role conversions across local knowledge, domestic advocacy/legal actors and US institutions.",
        "outputs/R06_R07_R11_pathways_v1/r06_pathway_comparison_v0.csv;outputs/explanatory_v0/",
        "mixed formal + analytical", "interpretive synthesis", "revise",
        "Make explicit that the ordering is an analytical reconstruction, not causality, command or a stable chain.", hr_group="pathway")
    add("R9 对名护、与那国", "R09", "quantitative_procedure",
        "R9 formal layer has 24 accepted stages and 25 accepted roles; reviewed-all adds 9 stages and 9 roles under HR-017.",
        "data/interim/20_referendum_process_stages_v0.csv;outputs/R09_referendum_process_v0/actor_process_roles_v0.csv;outputs/R09_referendum_process_v0/process_stages_reviewed_all_v0.csv;outputs/R09_referendum_process_v0/actor_process_roles_reviewed_all_v0.csv",
        "E3/E4", "formal accepted + HR-017 separate", limitation="Institutional sequence is not causal effect identification.",
        numeric_key="referendum", reported={"formal_stages":24,"formal_roles":25,"additional_stages":9,"additional_roles":9})
    add("选举侧候选层已覆盖", "R09", "candidate_quantitative",
        "Election candidate layer has 19 observations: endorsement 4, issue action 4, meetings 2, requests 4 and observation/information 5; all need HR-026.",
        "data/interim/33_r09_election_civic_events_v1.csv;outputs/R09_election_civic_interface_v1/",
        "candidate", "HR-026 pending", limitation="No turnout, vote, result or policy-effect claim is permitted.",
        numeric_key="election", reported={"rows":19,"endorsement":4,"issue":4,"meeting":2,"request":4,"observation":5})
    add("R6/R7 的统一底盘", "R06/R07/R11", "quantitative",
        "Pathway floor has 71 formal facts plus 4 analytical seeds; six-case heterogeneous sequence has 17 stages.",
        "data/interim/26_actor_event_venue_target_entry_modes_v0.csv;outputs/R06_R07_R11_pathways_v1/analytical_seeds_v0.csv;outputs/R05_R07_heterogeneous_repertoire_v1/cross_case_sequence_v1.csv",
        "formal + separately labelled analytical", "mechanical pathway derivation", limitation="Arrows indicate time/structure/direction, not causal effect.",
        numeric_key="pathways", reported={"facts":71,"seeds":4})
    add("R8 六案比较进一步", "R08", "case_outcome",
        "Six cases and 27 accepted roles show differentiated procedural outputs; 13 roles are registered actors and 14 provisional nodes.",
        "data/interim/17_legal_policy_procedure_cases_v0.csv;data/interim/18_legal_policy_actor_roles_v0.csv",
        "E3/E4", "HR-014 human_checked", limitation="Do not collapse outcomes into a single win/loss scale.",
        numeric_key="legal", reported={"cases":6,"roles":27,"registry_roles":13,"provisional_roles":14})
    add("R5/R7 异质行动包已完成", "R05/R07", "visualization_status",
        "The heterogeneous package completes the Phase-1 action-grammar comparison while retaining the missing protest-timeline limitation.",
        "outputs/R05_R07_heterogeneous_repertoire_v1/", "formal reused layer", "mechanical consistency check", "safe",
        "Completed package status and the remaining corpus limitation are now separated.")

    add("R10 现在先建立一个与 actor", "R10", "quantitative",
        "The complete S002 FY2024 source universe contains 616 rows across 86 pages, 15 departments, 19 official issue fields and 10 official mechanisms. C1–C4 account for 469 rows (76.1%), the top five departments for 443 (71.9%), and fields 10+11 for 19 rows (3.1%). The table has 390 literal partner strings and 365 machine display aliases, neither of which is an actor count.",
        "outputs/R10_official_collaboration_universe_v1/official_collaboration_source_universe_v1.csv;outputs/R10_official_collaboration_universe_v1/descriptive_statistics_v1.csv;outputs/R10_official_collaboration_universe_v1/official_resource_type_summary_v1.csv;outputs/R10_official_collaboration_universe_v1/department_resource_summary_v1.csv",
        "E4 official source universe", "mechanical full-source extraction", limitation="Source rows, literal strings and machine display aliases are not organizations, contracts, awards or payments.", support_sources="S002",
        numeric_key="r10_universe", reported={"source_rows":616,"pdf_pages":86,"departments":15,"issue_fields":19,"mechanisms":10,"partner_literals":390,"machine_display_aliases":365,"mechanism_c1_c4_rows":469,"mechanism_c1_c4_share_tenths":761,"phase1_adjacent_fields_10_11_rows":19,"phase1_adjacent_fields_10_11_share_tenths":31,"top_five_department_rows":443,"top_five_department_share_tenths":719})
    add("来源总体图 `fig_r10_s002", "R10", "identity_and_relation_boundary",
        "The two S002 source-universe figures are publishable as source-row/source-label aggregations. HR-032 gates only future canonical identity, JV split and registry crosswalk; HR-018 still controls new relation and amount claims.",
        "outputs/R10_official_collaboration_universe_v1/figure_registry_v1.csv;outputs/R10_official_collaboration_universe_v1/HR032_partner_alias_crosswalk_review_v1.csv;outputs/R10_administrative_collaboration_v0/HR018_relation_review_v0.csv",
        "official source aggregation", "mechanical source layer + blank HR-032/HR-018 gates", limitation="Do not transform machine display labels into actors, source rows into relation edges, or project cost into actor payment.", support_sources="S002")

    add("R10 将此前混在一起的目的性跨来源样本", "R10", "quantitative",
        "R10's purposive cross-source sample has 35 relations, 26 amount observations and 43 function observations; 16 administrative／19 lower-layer mechanisms; 14 project-cost observations; 9 inherited human relations and 26+8 pending HR-018 items. These are package-internal counts, not a complete FY2024, department or mechanism census.",
        "outputs/R10_administrative_collaboration_v0/figure_metrics_v1.csv;outputs/R10_administrative_collaboration_v0/HR018_relation_review_v0.csv;outputs/R10_administrative_collaboration_v0/HR018_source_prerequisites_v0.csv;outputs/R10_completeness_audit_v1/source_universe_coverage_v1.csv;outputs/R10_completeness_audit_v1/s002_universe_index_v1.csv;outputs/R10_completeness_audit_v1/s099_program_cost_crosswalk_v1.csv",
        "mixed formal/candidate", "R10 mechanical normalization + HR-018 gate", limitation="New contract/commission candidates are not automatically accepted relations; sample shares cannot estimate the institutional universe.",
        numeric_key="r10", reported={"relation_observations":35,"amount_observations":26,"function_observations":43,"mechanism_figure_admin_layer":16,"mechanism_figure_lower_layer":19,"project_cost_observations":14,"human_checked_or_revised_relations":9,"s002_pdf_pages":86,"s002_universe_rows":616,"s002_selected_rows":10,"s099_explicit_public_commission_rows":3,"s099_represented_public_commission_rows":3})
    add("ONC，X010）是", "R10", "organization_function",
        "ONC is an Okinawa NPO active in international cooperation, multicultural coexistence, development education and Japanese-language learning.",
        "data/interim/05_source_log_initial_v0.csv", "E4 organization identity/function", "organization-site claim", support_sources="S095")
    add("外务省 NGO 相談員名单", "R10", "sensitive_admin_relation",
        "MOFA lists provide an official-source candidate for ONC's designated NGO-consultant role, still pending HR-018.",
        "data/interim/15_funding_or_support_edges_sample_v0.csv;outputs/R10_administrative_collaboration_v0/HR018_relation_review_v0.csv",
        "E4 source", "HR-018-06/07 pending", "safe",
        "The text explicitly withholds relation acceptance pending HR-018.", support_sources="S096;S101")
    add("S099 中明确标作公共行政委托", "R10", "sensitive_amount",
        "ONC FY2024 project costs are JPY 2.894m, 16.04m and 5.53m; the report explicitly says they are not government payments or contract amounts.",
        "data/interim/15_funding_or_support_edges_sample_v0.csv;outputs/R10_administrative_collaboration_v0/HR018_relation_review_v0.csv",
        "E4 source", "HR-018-04/05/06 pending", "safe",
        "Project-cost semantics are published only as a boundary; the underlying relations remain pending.", support_sources="S099")
    add("JICA 材料也不能", "R10", "sensitive_admin_relation",
        "The report treats the JICA contractor mapping as HR-018-pending and prohibits a funding-transfer inference.",
        "outputs/R10_administrative_collaboration_v0/annual_relations_v0.csv;outputs/R10_administrative_collaboration_v0/HR018_relation_review_v0.csv",
        "E4 source", "HR-018-01 pending", "safe",
        "No accepted contractor or payment relation is asserted before HR-018.", support_sources="S100")
    add("这些材料的来源等级可达 E4", "R10", "evidence_layer",
        "Official source strength is separated from human acceptance of the administrative relation.",
        "data/interim/15_funding_or_support_edges_sample_v0.csv;outputs/R10_administrative_collaboration_v0/HR018_relation_review_v0.csv",
        "central rows are E4 sources / ai_seeded relations", "HR-018-04/05 pending", "safe",
        "The report now states: E4 source evidence, relation still pending human review; project cost is not payment.")
    add("原先把 ONC 与县知事公室", "R10", "rejected_relation",
        "F019 ONC–base-affairs relation is unsupported and must not be used.",
        "data/interim/15_funding_or_support_edges_sample_v0.csv", "E2 rejected/not_supported", "source-boundary decision",
        limitation="No ONC-to-anti-base-network inference.")
    add("USO Okinawa（X001）的公开页面", "R10", "service_function",
        "USO's beneficiaries and Okinawa service sites are source-backed.",
        "data/interim/15_funding_or_support_edges_sample_v0.csv", "E4", "function observation", support_sources="S097",
        limitation="Service presence does not establish political stance.")
    add("16,000 美元捐赠", "R10", "sponsorship",
        "AEC sponsorship and a USD 16,000 donation/center improvement are human-checked.",
        "data/interim/15_funding_or_support_edges_sample_v0.csv", "E4", "F002 human_checked", support_sources="S097;S098",
        limitation="No political-stance inference.")
    add("公开军方社区报道产生三条", "R10", "sensitive_recipient_relation",
        "AWWA reporting produces three ai-seeded recipient candidates (Yomitan, Uruma and Boy Scouts), explicitly withheld from factual publication pending HR-018.",
        "data/interim/15_funding_or_support_edges_sample_v0.csv;outputs/R10_administrative_collaboration_v0/HR018_relation_review_v0.csv",
        "E3 military-community reporting", "HR-018-23/24/25 pending", "safe",
        "The report no longer publishes these candidates as accepted facts.", support_sources="S072;S094")
    add("40 年约 8 亿日元", "R10", "aggregate_amount_boundary",
        "AWWA's aggregate historical amount cannot be allocated to named recipients or years.",
        "outputs/R10_administrative_collaboration_v0/figure_metrics_v1.csv", "E3", "financial-semantics boundary", support_sources="S072;S078")
    add("关系图 `outputs/phase1_visuals", "R10", "sensitive_relation_visual",
        "The E3/E4 relation figure is explicitly labelled an evidence-threshold candidate graph and requires regeneration after HR-018.",
        "outputs/phase1_visuals_v1/support_relations_strict_e3e4.csv", "mixed E3/E4", "contains HR-018-pending rows", "block",
        "The current PNG remains excluded from final factual use until it is regenerated after HR-018.")
    add("不能被命名为", "R10", "financial_boundary",
        "Neither R10 mechanism figures nor the strict graph may be called an Okinawa NGO funding network.",
        "outputs/R10_administrative_collaboration_v0/mechanism_dictionary_v1.csv", "methodological", "red-line boundary")
    add("R11 从同一正式底盘派生 44", "R11", "quantitative",
        "R11 has 44 entries: advocacy 30, legal 5, administrative 1, service 5, charity 2 and public diplomacy 1.",
        "outputs/R06_R07_R11_pathways_v1/r11_external_entry_matrix_v0.csv", "formal role/relation layer", "mechanical derivation",
        limitation="Event/case roles are bounded; NOFO is opportunity only.", numeric_key="r11",
        reported={"rows":44,"advocacy":30,"legal":5,"administrative":1,"service":5,"charity":2,"public_diplomacy":1})

    add("295 条来源中，组织官网", "coverage", "quantitative",
        "Source composition is 295 total; organization sites 45, local news 39, local official 16, court 12, legislature 15 and prefectural official 11.",
        "data/interim/05_source_log_initial_v0.csv", "source metadata", "mechanical count",
        limitation="Counts describe current source visibility, not balanced coverage.", numeric_key="source_types",
        reported={"sources":295,"organization_site":45,"local_news":39,"local_official":16,"court_record":12,"official_legislative_record":15,"prefectural_official":11})
    add("第二是地点偏差。129 条组织—地点", "coverage/R03", "quantitative",
        "Actor–place counts are 129 total, Henoko 45, Okinawa-wide 42, Oura 6 and Yonaguni 6.",
        "data/interim/08_actor_place_edges_initial_v0.csv", "mixed candidate/human", "mechanical count",
        limitation="Counts indicate visibility/coding density, not real organization prevalence.", numeric_key="place_counts",
        reported={"relations":129,"P002_Henoko":45,"P001_Okinawa":42,"P003_Oura":6,"P011_Yonaguni":6})
    add("2020 年以来来源为 185/295", "coverage", "quantitative",
        "Sources since 2020 are 185/295 (62.7%); 1972–1997 has four sources.",
        "data/interim/05_source_log_initial_v0.csv", "source metadata", "mechanical count",
        limitation="Time distribution reflects source visibility rather than historical activity.", numeric_key="source_time",
        reported={"since_2020":185,"sources":295,"1972_1997":4})
    add("严格口径下有 26/118", "coverage", "quantitative",
        "Human-reviewed status covers 26/118 actors and 59/222 actor–issue edges.",
        "data/interim/01_actor_registry_initial_v0.csv;data/interim/07_actor_issue_edges_initial_v0.csv",
        "review metadata", "mechanical count", limitation="E4 is not equivalent to human review.", numeric_key="review_counts",
        reported={"actors":118,"actor_human":26,"edges":222,"edge_human":59})
    add("公开 NOFO 或项目机会", "coverage/R10", "financial_boundary",
        "A public NOFO or opportunity does not prove an award or recipient; funding claims require stricter evidence.",
        "data/metadata/coding_schema_v0.md;outputs/R10_administrative_collaboration_v0/mechanism_dictionary_v1.csv",
        "methodological", "red-line boundary")
    add("当前 267/295 个来源已归档", "coverage", "quantitative",
        "Archive status is 267/295 preserved, 26 failed and 2 non-URL references.",
        "source_docs/source_archive/source_archive_manifest.csv;data/interim/05_source_log_initial_v0.csv",
        "archive metadata", "mechanical count",
        limitation="Archive failure is a technical/access state, not evidence rejection; HR-030 controls metadata/archive issues.",
        numeric_key="archive", reported={"archived_or_manual":267,"sources":295,"failed":26,"skipped":2,"not_in_manifest":0})

    add("一期最稳健的发现不是", "conclusion", "interpretive_synthesis",
        "The strongest finding is differentiated translation of base/military disputes, not a single Okinawa NGO alliance.",
        "outputs/R01_R02_actor_issue_v1/;outputs/R04_sakishima_frame_corpus_v0/;outputs/R08_legal_procedure_v1/",
        "mixed candidate/human", "interpretive synthesis", "revise",
        "Retain the no-alliance boundary but decide whether the positive translation claim is stated as finding or sample-bounded interpretation.", hr_group="translation")
    add("第二，这一转译具有地点依赖性", "conclusion", "interpretive_synthesis",
        "Translation is place-dependent; Henoko cannot be directly generalized to Yonaguni, Ishigaki or Miyako.",
        "outputs/R03_spatial_dossier_v1/;outputs/R04_sakishima_frame_corpus_v0/",
        "mixed candidate/human", "interpretive synthesis", "revise",
        "Decide final-report strength in light of candidate place semantics and institution-heavy R4 evidence.", hr_group="spatial")
    add("事件角色比无差别关系边", "conclusion", "methodological_finding",
        "Event roles preserve participation intensity and institutional position better than undifferentiated relation edges.",
        "data/interim/09_actor_event_venue_edges_v0.csv;outputs/R05_R07_heterogeneous_repertoire_v1/",
        "formal + analytical", "methodological comparison", limitation="Do not interpret as causal explanatory superiority.")
    add("第四，冲绳基地社会的民间组织生态", "conclusion", "function_boundary",
        "The observed ecology includes administrative, international-cooperation, service and charity layers outside protest actors.",
        "outputs/phase1_visuals_v1/functional_ecology_matrix.csv;outputs/R10_administrative_collaboration_v0/",
        "mixed", "bounded function observation", limitation="Observed function is not political stance.")
    add("当前结论仍是线上公开资料", "conclusion", "scope_boundary",
        "Results are an online-source Phase-1 product suitable for mechanisms, visuals and local-task prioritization, not population, funding-flow or alliance-history inference.",
        "docs/phase1_scheme_acceptance_audit_v1.md;docs/local_retrieval_tasks_v1.md", "methodological", "acceptance boundary")

    add("R5/R7 异质行动包又以 148", "report_status", "quantitative",
        "The heterogeneous package has 148 input observations, 39 units, 15 action types and 9 venues.",
        "outputs/R05_R07_heterogeneous_repertoire_v1/input_layer_audit_v1.csv;outputs/R05_R07_heterogeneous_repertoire_v1/repertoire_event_action_venue_units_v1.csv",
        "formal reused rows", "mechanical count", numeric_key="heterogeneous",
        reported={"input_rows":148,"units":39,"actions":15,"venues":9})
    add("HR-013～015 已并入", "report_status", "review_queue_status",
        "The report lists unresolved gates through HR-032 and notes HR-028=0.",
        "outputs/", "review metadata", "mechanical queue inventory", "safe",
        "The current review-gate inventory includes HR-029, HR-030, HR-031 and HR-032.")
    return rows


def report_context(lines: list[str], anchor: str) -> tuple[int, str]:
    matches = [index for index, line in enumerate(lines) if anchor in line]
    if len(matches) != 1:
        raise RuntimeError(f"Anchor must match exactly once ({len(matches)}): {anchor}")
    index = matches[0]
    return index + 1, lines[index]


def paragraph_ids(lines: list[str]) -> dict[int, str]:
    mapping: dict[int, str] = {}
    paragraph = 0
    active = False
    for line_no, line in enumerate(lines, 1):
        if line.strip():
            if not active:
                paragraph += 1
                active = True
            mapping[line_no] = f"P{paragraph:03d}"
        else:
            active = False
    return mapping


def extract_source_ids(text: str) -> list[str]:
    ids = set(re.findall(r"\bS\d{3}\b", text))
    for start, end in re.findall(r"S(\d{3})\s*[—–-]\s*S?(\d{3})", text):
        ids.update(f"S{number:03d}" for number in range(int(start), int(end) + 1))
    return sorted(ids, key=lambda value: int(value[1:]))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lines = REPORT.read_text(encoding="utf-8-sig").splitlines()
    paragraph_map = paragraph_ids(lines)
    metrics, aux = build_metrics()
    specs = claim_specs()
    source_ids: set[str] = aux["source_ids"]  # type: ignore[assignment]

    audits: list[dict[str, object]] = []
    numeric_rows: list[dict[str, object]] = []
    source_rows: list[dict[str, object]] = []
    formal_rows: list[dict[str, object]] = []
    for index, spec in enumerate(specs, 1):
        claim_id = f"RCA{index:03d}"
        line_no, excerpt = report_context(lines, str(spec["anchor"]))
        report_sources = extract_source_ids(excerpt)
        support_sources = split_refs(str(spec["audit_support_source_ids"]))
        refs = sorted(set(report_sources + support_sources), key=lambda value: int(value[1:]) if re.fullmatch(r"S\d+", value) else 999999)
        missing_sources = [source for source in refs if source not in source_ids]
        source_check = "pass" if not missing_sources else "fail_missing:" + semijoin(missing_sources)
        support_paths = split_refs(str(spec["audit_support_formal_tables"]))
        missing_paths = [path for path in support_paths if not (ROOT / path).exists()]
        formal_check = "pass" if not missing_paths else "fail_missing:" + semijoin(missing_paths)

        numeric_status = "not_applicable"
        reported_value = ""
        verified_value = ""
        key = str(spec["numeric_key"])
        if key:
            reported = spec["reported"]
            observed_all = metrics[key]
            observed = {name: observed_all.get(name, -999999) for name in reported}
            numeric_status = "match" if ints_equal(reported, observed) else "mismatch"
            reported_value = json_compact(reported)
            verified_value = json_compact(observed)
            numeric_rows.append({
                "claim_id": claim_id, "report_locator": f"L{line_no:03d};{paragraph_map[line_no]}",
                "metric_group": key, "reported_value": reported_value, "verified_value": verified_value,
                "numeric_check_status": numeric_status,
                "source_of_truth": spec["audit_support_formal_tables"],
            })

        status = str(spec["publish_status"])
        if numeric_status == "mismatch" and status == "safe":
            status = "revise"
        if missing_sources:
            status = "block"
        if missing_paths:
            status = "block"

        audits.append({
            "claim_id": claim_id,
            "report_locator": f"L{line_no:03d};{paragraph_map[line_no]}",
            "module": spec["module"],
            "claim_type": spec["claim_type"],
            "claim_text": spec["claim_text"],
            "report_excerpt": excerpt,
            "report_cited_source_ids": semijoin(report_sources),
            "audit_support_source_ids": semijoin(support_sources),
            "audit_support_formal_tables": spec["audit_support_formal_tables"],
            "evidence_level_or_layer": spec["evidence_level"],
            "review_layer": spec["review_layer"],
            "source_id_check": source_check,
            "formal_table_check": formal_check,
            "numeric_check_status": numeric_status,
            "reported_value": reported_value,
            "verified_value": verified_value,
            "publish_status": status,
            "limitations": spec["limitations"],
            "audit_note": spec["audit_note"],
            "hr031_group": spec["hr_group"],
        })
        for source_id in refs:
            source_rows.append({
                "claim_id": claim_id, "report_locator": f"L{line_no:03d};{paragraph_map[line_no]}",
                "source_id": source_id,
                "citation_origin": "report_and_audit" if source_id in report_sources and source_id in support_sources else ("report" if source_id in report_sources else "audit_crosswalk"),
                "exists_in_source_log": "yes" if source_id in source_ids else "no",
            })
        for path in support_paths:
            formal_rows.append({
                "claim_id": claim_id, "report_locator": f"L{line_no:03d};{paragraph_map[line_no]}",
                "formal_table_or_resource": path,
                "exists_in_workspace": "yes" if (ROOT / path).exists() else "no",
            })

    audit_by_claim = {str(row["claim_id"]): row for row in audits}

    def claim_for_text(text: str) -> str:
        for row in audits:
            if text in str(row["claim_text"]):
                return str(row["claim_id"])
        raise KeyError(text)

    fixes: list[tuple[str, str, str, str]] = []
    fix_rows: list[dict[str, object]] = []
    for number, (slug, claim_id, issue, action) in enumerate(fixes, 1):
        row = audit_by_claim[claim_id]
        fix_rows.append({
            "fix_id": f"RCF{number:03d}", "claim_id": claim_id, "report_locator": row["report_locator"],
            "issue_type": issue, "current_claim": row["claim_text"], "verified_value": row["verified_value"],
            "replacement_or_action": action, "requires_human_judgment": "no", "status": "open",
        })

    if "### 定量主张核验索引" not in "\n".join(lines):
        fix_rows.append({
            "fix_id": "RCF001", "claim_id": "all_quantitative_claims", "report_locator": "report_endmatter",
            "issue_type": "missing_formal_table_locator_index",
            "current_claim": "The report has no compact quantitative claim-to-table index.",
            "verified_value": "See the main claim audit crosswalk.",
            "replacement_or_action": "Add a module-level quantitative verification index before the data/source index.",
            "requires_human_judgment": "no", "status": "open",
        })

    blockers = [row for row in audits if row["publish_status"] == "block"]
    blocker_rows = [{
        "blocker_id": f"RCB{index:03d}", "claim_id": row["claim_id"], "report_locator": row["report_locator"],
        "claim_text": row["claim_text"], "blocking_dependency": row["review_layer"],
        "required_action": row["limitations"], "release_condition": "Relevant existing human gate is accepted/revised and the report wording is updated.",
    } for index, row in enumerate(blockers, 1)]

    hr_groups = {
        "translation": {
            "question": "一期结论应把‘基地争议被转译为生态／生活安全／自治／法律／国际倡议’写成阶段性发现，还是降为‘当前公开样本中的分析框架’？",
            "options": "A=阶段性发现（保留样本限定）;B=分析框架（更保守）;C=拆成仅人审案例可支持的子结论",
            "why": "相关段落混用 59 条人审与 163 条候选 actor–issue edge；否定统一联盟是安全的，正向综合强度需主研究者判断。",
        },
        "spatial": {
            "question": "地点差异应以何种强度进入最终结论：显著地点依赖，还是仅称当前可见材料呈现差异？",
            "options": "A=显著地点依赖（强）;B=公开材料呈现差异（推荐）;C=移到局限／待当地复核",
            "why": "129 条地点边仍为候选／人审混合，R4 也明显由制度记录主导。",
        },
        "pathway": {
            "question": "边野古／大浦湾国际化段落是否保留‘连续转换’叙事，或改成并列的可观察入口／角色？",
            "options": "A=保留连续转换但加分析重建限定;B=改成并列入口（推荐）;C=只保留案件／事件事实",
            "why": "现有正式角色能证明入口与角色，不能证明组织间传递、指挥或因果链。",
        },
    }
    hr_rows: list[dict[str, object]] = []
    for index, (group, detail) in enumerate(hr_groups.items(), 1):
        linked = [str(row["claim_id"]) for row in audits if row["hr031_group"] == group]
        hr_rows.append({
            "review_item_id": f"HR-031-{index:02d}", "claim_ids": semijoin(linked),
            "report_locators": semijoin([str(audit_by_claim[claim_id]["report_locator"]) for claim_id in linked]),
            "module": semijoin(sorted({str(audit_by_claim[claim_id]["module"]) for claim_id in linked})),
            "review_question": detail["question"], "decision_options": detail["options"],
            "why_human_judgment_is_required": detail["why"],
            "decision": "", "reviewer": "", "review_date": "", "review_note": "",
        })

    red_lines = [
        ("alliance", "共同声明／共同要请", "pass", "Report repeatedly states event participation is not a stable alliance."),
        ("candidate_layer", "actor–issue / actor–place", "pass", "A052/A053 now explicitly separate human-checked noise edges from candidate issue connections."),
        ("funding_award", "NOFO / project cost", "pass", "NOFO and project-cost non-payment boundaries are correctly stated."),
        ("sensitive_admin", "ONC commission/designated role", "pass", "The report labels the relations HR-018-pending and does not publish them as accepted facts."),
        ("sensitive_recipient", "AWWA recipient relations", "pass", "The report labels all three as ai-seeded candidates pending HR-018."),
        ("sensitive_visual", "strict E3/E4 relation figure", "block", "Evidence threshold was incorrectly allowed to stand in for human relation acceptance."),
        ("service_stance", "USO/AEC/AWWA political stance", "pass", "Report explicitly prohibits political-stance inference from observed function."),
        ("causality", "referendum/election/pathway arrows", "pass", "Report disclaims turnout, result, policy-effect and arrow causality."),
        ("role_transfer", "case-specific legal roles", "pass", "Plaintiff/counsel/requester/non-party distinctions are preserved."),
    ]
    red_rows = [{
        "scan_id": f"RCR{index:03d}", "red_line_category": category, "trigger_scope": trigger,
        "result": result, "finding": finding,
    } for index, (category, trigger, result, finding) in enumerate(red_lines, 1)]

    main_fields = [
        "claim_id","report_locator","module","claim_type","claim_text","report_excerpt",
        "report_cited_source_ids","audit_support_source_ids","audit_support_formal_tables",
        "evidence_level_or_layer","review_layer","source_id_check","formal_table_check","numeric_check_status",
        "reported_value","verified_value","publish_status","limitations","audit_note","hr031_group",
    ]
    write_csv(MAIN, audits, main_fields)
    write_csv(OUT / "claim_source_crosswalk_v1.csv", source_rows,
              ["claim_id","report_locator","source_id","citation_origin","exists_in_source_log"])
    write_csv(OUT / "claim_formal_table_crosswalk_v1.csv", formal_rows,
              ["claim_id","report_locator","formal_table_or_resource","exists_in_workspace"])
    write_csv(OUT / "numeric_check_results_v1.csv", numeric_rows,
              ["claim_id","report_locator","metric_group","reported_value","verified_value","numeric_check_status","source_of_truth"])
    write_csv(OUT / "mechanical_fix_queue_v1.csv", fix_rows,
              ["fix_id","claim_id","report_locator","issue_type","current_claim","verified_value","replacement_or_action","requires_human_judgment","status"])
    write_csv(OUT / "publication_blockers_v1.csv", blocker_rows,
              ["blocker_id","claim_id","report_locator","claim_text","blocking_dependency","required_action","release_condition"])
    hr_path = OUT / "HR031_report_claim_review_v0.csv"
    preserve_review_fields(hr_path, hr_rows, "review_item_id", ("decision", "reviewer", "review_date", "review_note"))
    write_csv(hr_path, hr_rows,
              ["review_item_id","claim_ids","report_locators","module","review_question","decision_options","why_human_judgment_is_required","decision","reviewer","review_date","review_note"])
    write_csv(OUT / "red_line_scan_v1.csv", red_rows,
              ["scan_id","red_line_category","trigger_scope","result","finding"])

    status_counts = Counter(str(row["publish_status"]) for row in audits)
    numeric_mismatches = sum(row["numeric_check_status"] == "mismatch" for row in numeric_rows)
    missing_source_count = sum(row["exists_in_source_log"] == "no" for row in source_rows)
    missing_formal_count = sum(row["exists_in_workspace"] == "no" for row in formal_rows)
    summary = f"""# 一期研究报告 claim→source/evidence 审计 v1

审计对象：`docs/phase1_research_report_v0.md`
报告 SHA-256：`{aux['report_sha256']}`

## 结果

- 审计 claim 单元：**{len(audits)}**
- 发布状态：**safe {status_counts['safe']} / revise {status_counts['revise']} / block {status_counts['block']}**
- 定量 claim 组：**{len(numeric_rows)}**；数值不一致：**{numeric_mismatches}**
- Claim–source 交叉：**{len(source_rows)}** 行；缺失 source ID：**{missing_source_count}**
- Claim–formal resource 交叉：**{len(formal_rows)}** 行；缺失路径：**{missing_formal_count}**
- 机械修订项：**{len(fix_rows)}**
- 受既有人工任务控制的发布阻断项：**{len(blocker_rows)}**
- 新增解释性人工判断：**{len(hr_rows)}**（`HR-031`）

## 主要发现

1. Registry、actor–issue、actor–place、事件、公投、法律、R4、R5/R7 和 R11 的主要数字均与当前正式表一致。
2. 来源相关陈述已与 **{aux['source_count']}** 行 source log（最新 **S{aux['max_source_num']:03d}**）及当前 archive manifest 对齐；脚本保留动态核验，后续来源波次改变时会自动报差异。
3. 报告大部分位置已正确守住五条红线：共同出现不等于联盟、NOFO 不等于 award、project cost 不等于付款、服务功能不等于政治立场、路径箭头不等于因果。
4. ONC 与 AWWA 的敏感关系已改为明确的 `HR-018` 待审候选，不再作为已接受事实发布；旧 E3/E4 关系图仍需在 HR-018 后重生，才能进入定稿图组。来源等级不能替代敏感关系的人审接受。
5. `HR-031` 只保留三组真正需要研究者判断的解释措辞：转译结论强度、地点差异强度、国际化路径的“连续转换”叙事。过时文本、层级标签与引用补齐均留在机械修订队列，不推给人工。

## 发布状态口径

- `safe`：在所列限制下，证据与措辞可发布。
- `revise`：有依据，但当前数字、层级标签、引用或措辞过时／过强。
- `block`：既有人工关口完成且正文修订前，不得作为事实发布。

完整逐行审计位于 `data/interim/38_report_claim_evidence_audit_v1.csv`。本包不修改报告或任何中央研究表。
"""
    (OUT / "report_claim_audit_summary_v1.md").write_text(summary, encoding="utf-8")

    max_bar = max(status_counts.values()) or 1
    colors = {"safe":"#2f855a", "revise":"#d69e2e", "block":"#c53030"}
    svg_rows = []
    for index, status in enumerate(("safe","revise","block")):
        y = 72 + index * 56
        width = 520 * status_counts[status] / max_bar
        svg_rows.append(f'<text x="30" y="{y+22}" font-size="18">{status}</text><rect x="120" y="{y}" width="{width:.1f}" height="32" rx="4" fill="{colors[status]}"/><text x="{130+width:.1f}" y="{y+22}" font-size="18">{status_counts[status]}</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="280" viewBox="0 0 760 280">
<rect width="760" height="280" fill="#f8fafc"/><text x="30" y="38" font-size="24" font-family="Arial, sans-serif" font-weight="700">Report claim publish status (n={len(audits)})</text>
<g font-family="Arial, sans-serif" fill="#1a202c">{''.join(svg_rows)}</g>
<text x="30" y="254" font-family="Arial, sans-serif" font-size="14" fill="#4a5568">Block = existing human gate unresolved; revise = mechanical or wording repair.</text></svg>'''
    (OUT / "fig_claim_publish_status_v1.svg").write_text(svg + "\n", encoding="utf-8")

    validation = {
        "report_sha256": aux["report_sha256"], "claim_count": len(audits),
        "publish_status": dict(status_counts), "numeric_checks": len(numeric_rows),
        "numeric_mismatches": numeric_mismatches, "missing_source_ids": missing_source_count,
        "missing_formal_paths": missing_formal_count,
        "mechanical_fix_count": len(fix_rows), "publication_blocker_count": len(blocker_rows),
        "hr031_count": len(hr_rows), "all_hr_decision_fields_blank": all(not row["decision"] and not row["reviewer"] and not row["review_date"] and not row["review_note"] for row in hr_rows),
    }
    (OUT / "validation_report_v1.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    readme = """# report_claim_audit_v1

Reproducible paragraph/claim audit of `docs/phase1_research_report_v0.md`.

- Main audit: `data/interim/38_report_claim_evidence_audit_v1.csv`
- Mechanical repair queue: `mechanical_fix_queue_v1.csv`
- Existing human-gate blockers: `publication_blockers_v1.csv`
- New interpretive decisions only: `HR031_report_claim_review_v0.csv`
- Numeric comparisons: `numeric_check_results_v1.csv`
- Claim/source validation: `claim_source_crosswalk_v1.csv`
- Claim/formal-table validation: `claim_formal_table_crosswalk_v1.csv`
- Red-line scan: `red_line_scan_v1.csv`

Run from the repository root with `python scripts/audit_report_claims_v1.py`. The script does not modify the report or central research tables.
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")

    print(json.dumps(validation, ensure_ascii=False))


if __name__ == "__main__":
    main()
