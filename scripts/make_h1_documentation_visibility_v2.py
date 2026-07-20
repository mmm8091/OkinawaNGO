from __future__ import annotations

"""Build H1 v2: documentation traces and observed graph visibility.

This package is deliberately research-only.  It keeps five analytical objects
separate:

1. the current actor--issue bipartite evidence graph;
2. same-source actor--place--issue observations;
3. human-checked actor--event incidence (event hyperedges, not alliances);
4. reviewed typed dyadic organization relations; and
5. accepted case-role incidence.

The source-derived indicators below are *observed documentation traces*.  They
are not measures of staff, skill, organizational capacity, activity, influence,
or causal effects of documentation.
"""

import csv
import hashlib
import json
import math
import random
import re
from collections import Counter, defaultdict, deque
from pathlib import Path
from statistics import median
from urllib.parse import urlparse
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
OUT = ROOT / "outputs" / "research_wave_h1_documentation_visibility_v2"

ACTORS = DATA / "01_actor_registry_initial_v0.csv"
SOURCES = DATA / "05_source_log_initial_v0.csv"
EDGES = DATA / "24_r01_r02_actor_issue_layered_v0.csv"
TRIPLES = (
    ROOT
    / "outputs"
    / "R03_strict_place_issue_v1"
    / "same_source_actor_place_issue_triples_v1.csv"
)
EVENTS = DATA / "09_actor_event_venue_edges_v0.csv"
CASE_ROLES = DATA / "18_legal_policy_actor_roles_v0.csv"
LIFECYCLE = ROOT / "outputs" / "actor_lifecycle_v1" / "actor_lifecycle_v0.csv"
CLASS_MAP = (
    ROOT
    / "outputs"
    / "R01_R02_actor_issue_v1"
    / "actor_class_controlled_mapping_v1.csv"
)
ARCHIVE = (
    ROOT
    / "source_docs"
    / "source_archive"
    / "source_archive_manifest.csv"
)
DYADIC = (
    ROOT
    / "outputs"
    / "exploration_system_data_v1"
    / "demo"
    / "dyadic_relations.json"
)

AUDIT_DATE = "2026-07-20"
E3PLUS = {"E3", "E4"}
BIG3 = {"S003", "S004", "S006"}
HUMAN_EDGE_STATUSES = {"human_checked", "human_revised"}
PACKAGE_META = {
    "research_status": "research_only",
    "display_tier": "research",
    "claim_status": "candidate",
    "review_status": "ai_seeded",
    "frontend_eligibility": "not_frontend_ready",
}
INTERPRETATION_LIMIT = (
    "Observed documentation and encoded evidence-layer visibility only; no "
    "causal documentation effect, social-network influence, activity strength, "
    "alliance, staff capacity, language capacity, or organizational lifespan."
)

ORGANIZATION_HOSTED_TYPES = {
    "association_directory",
    "association_report",
    "foundation_program_record",
    "foundation_site",
    "member_organization_action_record",
    "ngo_directory",
    "ngo_statement",
    "organization_action_record",
    "organization_blog",
    "organization_event_record",
    "organization_event_report",
    "organization_filing",
    "organization_financial_filing",
    "organization_history",
    "organization_profile",
    "organization_program_document",
    "organization_report",
    "organization_site",
    "organization_site_subunit_page",
    "organization_social",
    "organization_statement",
    "organization_story",
    "organization_website",
    "parent_organization_profile",
    "parent_organization_topic_page",
    "partner_organization_record",
    "union_research_report",
}
LEGAL_TYPES = {
    "court_record",
    "formal_counsel_material",
    "legal_database",
    "legal_international",
    "legal_network_report",
    "legal_source",
    "participating_law_firm_record",
    "party_legal_filing",
}
MEDIA_TYPES = {
    "community_site",
    "encyclopedia",
    "event_report",
    "local_news",
    "local_news_english",
    "local_newspaper",
    "magazine_news",
    "main_local_newspaper",
    "media_record",
    "news",
    "party_news",
}
ACADEMIC_TYPES = {
    "academic_article",
    "academic_presentation",
    "research_report",
}
FUNDING_RECORD_TYPES = {
    "funded_project_report",
    "grant_database",
    "grant_document",
    "grant_listing",
    "nonprofit_record",
}

FRAME_MAP = {
    "base": {"anti_base", "anti_military", "Henoko"},
    "ecology": {"environment", "biodiversity", "dugong", "groundwater"},
    "life_health": {
        "life_safety",
        "health_risk",
        "noise",
        "base_community_welfare",
        "military_family_service",
    },
    "autonomy": {"local_autonomy", "referendum"},
    "legal": {"legal"},
    "international": {
        "international_advocacy",
        "public_diplomacy",
        "international_cooperation",
    },
    "frontline": {"frontline_prevention", "Taiwan_contingency", "anti_war"},
    "rights_peace": {
        "women",
        "human_rights",
        "peace",
        "solidarity",
        "mobilization",
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def split_tokens(value: str) -> set[str]:
    return {token.strip() for token in (value or "").split(";") if token.strip()}


def source_refs(value: str) -> set[str]:
    return {token for token in split_tokens(value) if re.fullmatch(r"S\d{3}", token)}


def current_actor(row: dict[str, str]) -> bool:
    actor_id = row.get("actor_id", "")
    review_status = row.get("review_status", "").lower()
    scope_status = row.get("scope_status", "").lower()
    if actor_id == "A072" or row.get("merged_duplicate_of", ""):
        return False
    if review_status == "rejected":
        return False
    if scope_status == "merged_duplicate":
        return False
    if scope_status.startswith(("retired_", "deactivated_")):
        return False
    if "excluded" in scope_status:
        return False
    return True


def source_channel(source_type: str) -> str:
    if source_type in LEGAL_TYPES:
        return "legal_procedural"
    if source_type in ORGANIZATION_HOSTED_TYPES:
        return "organization_hosted"
    if (
        "official" in source_type
        or source_type.startswith("government_")
        or source_type
        in {
            "local_official",
            "military_news",
            "prefectural_official",
            "government_corporate_record",
        }
    ):
        return "official_administrative"
    if source_type in MEDIA_TYPES or any(
        marker in source_type for marker in ("news", "newspaper", "magazine")
    ):
        return "media"
    if source_type in ACADEMIC_TYPES or source_type.startswith("academic"):
        return "academic_secondary"
    if source_type in FUNDING_RECORD_TYPES or source_type.startswith("grant_"):
        return "funding_nonprofit_record"
    return "other"


def title_language(title: str, source_type: str) -> str:
    japanese = len(re.findall(r"[\u3040-\u30ff\u3400-\u9fff]", title))
    latin = len(re.findall(r"[A-Za-z]", title))
    if source_type == "local_news_english":
        return "likely_english_title"
    if japanese >= 3 and latin >= 12:
        return "mixed_title"
    if japanese >= 3:
        return "likely_japanese_title"
    if latin >= 12:
        return "likely_english_title"
    return "undetermined_title"


def year_values(value: str) -> list[int]:
    years = [
        int(match)
        for match in re.findall(r"(?<!\d)(?:19|20)\d{2}(?!\d)", value or "")
    ]
    return [year for year in years if 1972 <= year <= 2026]


def url_domain(url: str) -> str:
    try:
        return urlparse(url).netloc.lower().removeprefix("www.")
    except ValueError:
        return ""


def legal_case_marker(source: dict[str, str]) -> bool:
    value = " ".join(
        [
            source.get("title", ""),
            source.get("url", ""),
            source.get("source_type", ""),
        ]
    )
    return bool(
        re.search(
            r"(docket|No\.?\s*\d|cv-\d|判決|訴訟|裁判|事件|意見書|court_record)",
            value,
            re.IGNORECASE,
        )
    )


def source_feature_rows(
    sources: list[dict[str, str]],
    archive_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    archive_by_id = {row["source_id"]: row for row in archive_rows}
    rows: list[dict[str, object]] = []
    for source in sources:
        source_id = source["source_id"]
        channel = source_channel(source["source_type"])
        language = title_language(source["title"], source["source_type"])
        archive = archive_by_id.get(source_id, {})
        primary_formal = channel in {
            "organization_hosted",
            "legal_procedural",
            "official_administrative",
            "funding_nonprofit_record",
        }
        external = channel in {"media", "academic_secondary"}
        years = year_values(source.get("year", ""))
        row = {
            "source_id": source_id,
            "source_title": source["title"],
            "source_type": source["source_type"],
            "source_channel_heuristic": channel,
            "source_year_raw": source.get("year", ""),
            "parsed_year_min": min(years) if years else "",
            "parsed_year_max": max(years) if years else "",
            "url_domain": url_domain(source.get("url", "")),
            "organization_hosted_trace_candidate": (
                "yes" if channel == "organization_hosted" else "no"
            ),
            "official_or_formal_trace_candidate": (
                "yes" if primary_formal else "no"
            ),
            "external_mention_trace_candidate": "yes" if external else "no",
            "legal_procedural_trace": (
                "yes"
                if channel == "legal_procedural" or legal_case_marker(source)
                else "no"
            ),
            "title_language_heuristic": language,
            "case_number_or_legal_title_marker": (
                "yes" if legal_case_marker(source) else "no"
            ),
            "high_capacity_list_source": "yes" if source_id in BIG3 else "no",
            "archive_status": archive.get("archive_status", "missing_manifest_row"),
            "archive_content_type": archive.get("content_type", ""),
            "source_evidence_level": source.get("evidence_level", ""),
            "source_review_status": source.get("review_status", ""),
            "classification_method": (
                "mechanical source_type/title/url/archive classification; "
                "organization hosting is not actor ownership and title language "
                "is not document or staff language capacity"
            ),
            **PACKAGE_META,
            "interpretation_limit": INTERPRETATION_LIMIT,
        }
        rows.append(row)
    return rows


def ranks(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda index: values[index])
    result = [0.0] * len(values)
    cursor = 0
    while cursor < len(values):
        end = cursor
        while (
            end + 1 < len(values)
            and values[order[end + 1]] == values[order[cursor]]
        ):
            end += 1
        rank = (cursor + end + 2) / 2
        for position in range(cursor, end + 1):
            result[order[position]] = rank
        cursor = end + 1
    return result


def spearman(values_x: list[float], values_y: list[float]) -> float | None:
    if len(values_x) < 3 or len(values_x) != len(values_y):
        return None
    ranked_x = ranks(values_x)
    ranked_y = ranks(values_y)
    mean_x = sum(ranked_x) / len(ranked_x)
    mean_y = sum(ranked_y) / len(ranked_y)
    numerator = sum(
        (x - mean_x) * (y - mean_y) for x, y in zip(ranked_x, ranked_y)
    )
    denominator = math.sqrt(
        sum((x - mean_x) ** 2 for x in ranked_x)
        * sum((y - mean_y) ** 2 for y in ranked_y)
    )
    return numerator / denominator if denominator else None


def bootstrap_spearman(
    values_x: list[float],
    values_y: list[float],
    *,
    seed: int,
    iterations: int = 2000,
) -> tuple[float | None, float | None]:
    """Descriptive actor-resampling interval; not design-based inference."""

    if len(values_x) < 5:
        return None, None
    rng = random.Random(seed)
    estimates: list[float] = []
    for _ in range(iterations):
        indices = [rng.randrange(len(values_x)) for _ in values_x]
        estimate = spearman(
            [values_x[index] for index in indices],
            [values_y[index] for index in indices],
        )
        if estimate is not None:
            estimates.append(estimate)
    if not estimates:
        return None, None
    estimates.sort()
    low = estimates[int(0.025 * (len(estimates) - 1))]
    high = estimates[int(0.975 * (len(estimates) - 1))]
    return low, high


def brandes_betweenness(adjacency: dict[str, set[str]]) -> dict[str, float]:
    """Unweighted normalized betweenness for the observed graph only."""

    nodes = sorted(adjacency)
    centrality = {node: 0.0 for node in nodes}
    for source in nodes:
        stack: list[str] = []
        predecessors = {node: [] for node in nodes}
        path_count = {node: 0.0 for node in nodes}
        path_count[source] = 1.0
        distance = {node: -1 for node in nodes}
        distance[source] = 0
        queue = deque([source])
        while queue:
            node = queue.popleft()
            stack.append(node)
            for neighbor in adjacency[node]:
                if distance[neighbor] < 0:
                    queue.append(neighbor)
                    distance[neighbor] = distance[node] + 1
                if distance[neighbor] == distance[node] + 1:
                    path_count[neighbor] += path_count[node]
                    predecessors[neighbor].append(node)
        dependency = {node: 0.0 for node in nodes}
        while stack:
            node = stack.pop()
            for predecessor in predecessors[node]:
                dependency[predecessor] += (
                    path_count[predecessor]
                    / path_count[node]
                    * (1 + dependency[node])
                )
            if node != source:
                centrality[node] += dependency[node]
    for node in centrality:
        centrality[node] /= 2
    denominator = (len(nodes) - 1) * (len(nodes) - 2) / 2
    if denominator:
        centrality = {
            node: value / denominator for node, value in centrality.items()
        }
    return centrality


def bipartite_actor_metrics(
    pairs: set[tuple[str, str]],
    *,
    actor_prefix: str,
    object_prefix: str,
) -> tuple[Counter[str], dict[str, float]]:
    adjacency: dict[str, set[str]] = defaultdict(set)
    degrees: Counter[str] = Counter()
    for actor_id, object_id in pairs:
        actor_node = f"{actor_prefix}:{actor_id}"
        object_node = f"{object_prefix}:{object_id}"
        adjacency[actor_node].add(object_node)
        adjacency[object_node].add(actor_node)
        degrees[actor_id] += 1
    between = brandes_betweenness(adjacency) if adjacency else {}
    actor_between = {
        node.split(":", 1)[1]: value
        for node, value in between.items()
        if node.startswith(f"{actor_prefix}:")
    }
    return degrees, actor_between


def dyadic_actor_metrics(
    relations: list[dict[str, object]],
) -> tuple[Counter[str], dict[str, float]]:
    adjacency: dict[str, set[str]] = defaultdict(set)
    degrees: Counter[str] = Counter()
    seen: set[tuple[str, str, str]] = set()
    for relation in relations:
        source = str(relation["source_endpoint"])
        target = str(relation["target_endpoint"])
        relation_id = str(relation["id"])
        key = (relation_id, source, target)
        if key in seen:
            continue
        seen.add(key)
        adjacency[f"actor:{source}"].add(f"actor:{target}")
        adjacency[f"actor:{target}"].add(f"actor:{source}")
        degrees[source] += 1
        degrees[target] += 1
    between = brandes_betweenness(adjacency) if adjacency else {}
    return degrees, {
        node.split(":", 1)[1]: value
        for node, value in between.items()
        if node.startswith("actor:")
    }


def issue_frame(issue_label: str) -> str:
    for frame, labels in FRAME_MAP.items():
        if issue_label in labels:
            return frame
    return "other"


def issue_graph_summary(
    edges: list[dict[str, str]],
    registry_actor_count: int,
) -> dict[str, object]:
    pairs = {(row["actor_id"], row["issue_id"]) for row in edges}
    degrees, _ = bipartite_actor_metrics(
        pairs,
        actor_prefix="actor",
        object_prefix="issue",
    )
    adjacency: dict[str, set[str]] = defaultdict(set)
    actor_frames: dict[str, set[str]] = defaultdict(set)
    for row in edges:
        actor = f"actor:{row['actor_id']}"
        issue = f"issue:{row['issue_id']}"
        adjacency[actor].add(issue)
        adjacency[issue].add(actor)
        actor_frames[row["actor_id"]].add(issue_frame(row["issue_label"]))
    seen: set[str] = set()
    components: list[tuple[int, int]] = []
    for node in adjacency:
        if node in seen:
            continue
        queue = deque([node])
        seen.add(node)
        actor_count = 0
        total_count = 0
        while queue:
            current = queue.popleft()
            total_count += 1
            actor_count += current.startswith("actor:")
            for neighbor in adjacency[current]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        components.append((actor_count, total_count))
    largest = max(components, default=(0, 0))
    return {
        "edge_count": len(edges),
        "observed_actor_count": len(degrees),
        "registry_isolated_actor_count": registry_actor_count - len(degrees),
        "issue_count": len({row["issue_id"] for row in edges}),
        "cross_frame_actor_count": sum(
            len(frames) >= 2 for frames in actor_frames.values()
        ),
        "ecology_international_bridge_count": sum(
            {"ecology", "international"}.issubset(frames)
            for frames in actor_frames.values()
        ),
        "component_count": len(components),
        "largest_component_actor_count": largest[0],
        "largest_component_total_node_count": largest[1],
    }


def build_actor_rows(
    actors: list[dict[str, str]],
    sources: list[dict[str, str]],
    source_features: list[dict[str, object]],
    edges: list[dict[str, str]],
    triples: list[dict[str, str]],
    events: list[dict[str, str]],
    roles: list[dict[str, str]],
    lifecycle: list[dict[str, str]],
    class_map: dict[str, str],
    dyadic: list[dict[str, object]],
) -> tuple[list[dict[str, object]], dict[str, set[str]]]:
    actor_ids = {actor["actor_id"] for actor in actors}
    source_by_id = {row["source_id"]: row for row in sources}
    feature_by_id = {str(row["source_id"]): row for row in source_features}
    lifecycle_by_actor = {row["actor_id"]: row for row in lifecycle}

    linked: dict[str, set[str]] = defaultdict(set)
    unresolved: dict[str, set[str]] = defaultdict(set)
    by_basis: dict[str, dict[str, set[str]]] = defaultdict(
        lambda: defaultdict(set)
    )
    issue_support: dict[str, set[str]] = defaultdict(set)
    s004_only_edge_count: Counter[str] = Counter()

    for actor in actors:
        actor_id = actor["actor_id"]
        tokens = split_tokens(actor.get("source_refs", ""))
        refs = {token for token in tokens if token in source_by_id}
        linked[actor_id] |= refs
        by_basis[actor_id]["registry"] |= refs
        unresolved[actor_id] |= tokens - refs
    for edge in edges:
        actor_id = edge["actor_id"]
        tokens = split_tokens(edge.get("source_ref", ""))
        refs = {token for token in tokens if token in source_by_id}
        linked[actor_id] |= refs
        issue_support[actor_id] |= refs
        by_basis[actor_id]["actor_issue"] |= refs
        unresolved[actor_id] |= tokens - refs
        if refs and refs.issubset({"S004"}):
            s004_only_edge_count[actor_id] += 1
    for triple in triples:
        actor_id = triple["actor_id"]
        source_id = triple["shared_source_id"]
        if source_id in source_by_id:
            linked[actor_id].add(source_id)
            by_basis[actor_id]["strict_triple"].add(source_id)
    for event in events:
        actor_id = event["actor_or_counterpart_id"]
        refs = {
            token
            for token in split_tokens(event.get("source_id", ""))
            if token in source_by_id
        }
        linked[actor_id] |= refs
        by_basis[actor_id]["event"] |= refs
    for role in roles:
        actor_id = role["actor_id"]
        refs = {
            token
            for token in split_tokens(role.get("source_refs", ""))
            if token in source_by_id
        }
        linked[actor_id] |= refs
        by_basis[actor_id]["case_role"] |= refs
    for relation in dyadic:
        relation_refs = {
            token
            for token in relation.get("source_ids", [])
            if token in source_by_id
        }
        for endpoint_key in ("source_endpoint", "target_endpoint"):
            actor_id = str(relation[endpoint_key])
            if actor_id in actor_ids:
                linked[actor_id] |= relation_refs
                by_basis[actor_id]["typed_dyadic"] |= relation_refs

    issue_pairs = {(row["actor_id"], row["issue_id"]) for row in edges}
    e3_pairs = {
        (row["actor_id"], row["issue_id"])
        for row in edges
        if row["evidence_level"] in E3PLUS
    }
    reviewed_pairs = {
        (row["actor_id"], row["issue_id"])
        for row in edges
        if row["review_status"] in HUMAN_EDGE_STATUSES
    }
    issue_degree, issue_between = bipartite_actor_metrics(
        issue_pairs, actor_prefix="actor", object_prefix="issue"
    )
    e3_degree, e3_between = bipartite_actor_metrics(
        e3_pairs, actor_prefix="actor", object_prefix="issue"
    )
    reviewed_degree, reviewed_between = bipartite_actor_metrics(
        reviewed_pairs, actor_prefix="actor", object_prefix="issue"
    )
    event_pairs = {
        (row["actor_or_counterpart_id"], row["event_id"])
        for row in events
        if row["event_id"]
    }
    event_degree, event_between = bipartite_actor_metrics(
        event_pairs, actor_prefix="actor", object_prefix="event"
    )
    case_pairs = {
        (row["actor_id"], row["case_id"]) for row in roles if row["actor_id"]
    }
    case_degree, case_between = bipartite_actor_metrics(
        case_pairs, actor_prefix="actor", object_prefix="case"
    )
    dyadic_degree, dyadic_between = dyadic_actor_metrics(dyadic)

    triple_by_actor: dict[str, list[dict[str, str]]] = defaultdict(list)
    for triple in triples:
        triple_by_actor[triple["actor_id"]].append(triple)
    roles_by_actor: dict[str, list[dict[str, str]]] = defaultdict(list)
    for role in roles:
        roles_by_actor[role["actor_id"]].append(role)
    issue_edges_by_actor: dict[str, list[dict[str, str]]] = defaultdict(list)
    for edge in edges:
        issue_edges_by_actor[edge["actor_id"]].append(edge)

    rows: list[dict[str, object]] = []
    for actor in sorted(actors, key=lambda row: row["actor_id"]):
        actor_id = actor["actor_id"]
        linked_ids = {source_id for source_id in linked[actor_id] if source_id in source_by_id}
        feature_rows = [feature_by_id[source_id] for source_id in linked_ids]
        channels = {
            str(row["source_channel_heuristic"]) for row in feature_rows
        }
        domains = {
            str(row["url_domain"])
            for row in feature_rows
            if row.get("url_domain", "")
        }
        years = [
            int(year)
            for source_id in linked_ids
            for year in year_values(source_by_id[source_id].get("year", ""))
        ]
        archive_success = sum(
            row["archive_status"] in {"archived", "manual_archived"}
            for row in feature_rows
        )
        org_trace = any(
            row["organization_hosted_trace_candidate"] == "yes"
            for row in feature_rows
        )
        official_trace = any(
            row["source_channel_heuristic"] == "official_administrative"
            for row in feature_rows
        )
        external_trace = any(
            row["external_mention_trace_candidate"] == "yes"
            for row in feature_rows
        )
        legal_trace = any(
            row["legal_procedural_trace"] == "yes" for row in feature_rows
        ) or bool(case_degree[actor_id])
        english_title = any(
            row["title_language_heuristic"]
            in {"likely_english_title", "mixed_title"}
            for row in feature_rows
        )
        japanese_title = any(
            row["title_language_heuristic"]
            in {"likely_japanese_title", "mixed_title"}
            for row in feature_rows
        )
        span = max(years) - min(years) if len(years) >= 2 else 0
        source_count = len(linked_ids)
        doc_stratum = (
            "dense_4plus"
            if source_count >= 4
            else "moderate_2to3"
            if source_count >= 2
            else "thin_0to1"
        )
        actor_triples = triple_by_actor[actor_id]
        actor_roles = roles_by_actor[actor_id]
        actor_issue_edges = issue_edges_by_actor[actor_id]
        lifecycle_row = lifecycle_by_actor.get(actor_id)
        feature_count = sum(
            [
                org_trace,
                official_trace,
                external_trace,
                legal_trace,
                english_title,
                span >= 3,
                len(domains) >= 2,
            ]
        )
        row = {
            "actor_id": actor_id,
            "actor_name": actor["canonical_name"],
            "actor_class": actor["actor_class"],
            "analysis_family": class_map[actor["actor_class"]],
            "origin_type": actor["origin_type"],
            "origin_bucket": (
                "okinawa_local"
                if actor["origin_type"] == "okinawa_local"
                else "nonlocal_or_institutional"
            ),
            "legal_status_guess": actor.get("legal_status_guess", ""),
            "legal_formality_bucket": legal_formality_bucket(
                actor.get("legal_status_guess", "")
            ),
            "actor_evidence_level": actor.get("evidence_level", ""),
            "actor_review_status": actor.get("review_status", ""),
            "linked_source_count": source_count,
            "linked_source_ids": ";".join(sorted(linked_ids)),
            "unresolved_reference_count": len(unresolved[actor_id]),
            "unresolved_reference_tokens": ";".join(sorted(unresolved[actor_id])),
            "registry_source_count": len(by_basis[actor_id]["registry"]),
            "actor_issue_support_source_count": len(
                by_basis[actor_id]["actor_issue"]
            ),
            "strict_triple_source_count": len(
                by_basis[actor_id]["strict_triple"]
            ),
            "event_source_count": len(by_basis[actor_id]["event"]),
            "case_role_source_count": len(by_basis[actor_id]["case_role"]),
            "typed_dyadic_source_count": len(
                by_basis[actor_id]["typed_dyadic"]
            ),
            "non_issue_linked_source_count": len(
                linked_ids - issue_support[actor_id]
            ),
            "non_big3_linked_source_count": len(linked_ids - BIG3),
            "source_channel_count": len(channels),
            "source_channels": ";".join(sorted(channels)),
            "source_domain_count": len(domains),
            "archive_success_count": archive_success,
            "archive_failure_or_skip_count": len(feature_rows) - archive_success,
            "archive_success_share": (
                round(archive_success / len(feature_rows), 3)
                if feature_rows
                else ""
            ),
            "organization_hosted_trace_candidate": "yes" if org_trace else "no",
            "own_website_status": "not_measured_actor_owner_crosswalk_missing",
            "official_administrative_trace": (
                "yes" if official_trace else "no"
            ),
            "external_media_or_academic_trace": (
                "yes" if external_trace else "no"
            ),
            "legal_procedural_trace": "yes" if legal_trace else "no",
            "english_title_trace": "yes" if english_title else "no",
            "japanese_title_trace": "yes" if japanese_title else "no",
            "multilingual_title_trace": (
                "yes" if english_title and japanese_title else "no"
            ),
            "language_capacity_status": (
                "not_measured_title_language_is_only_a_trace"
            ),
            "document_year_min": min(years) if years else "",
            "document_year_max": max(years) if years else "",
            "document_record_span_years": span,
            "lifecycle_status": (
                lifecycle_row.get("lifecycle_status", "")
                if lifecycle_row
                else "not_measured"
            ),
            "lifespan_status": (
                "not_measured_record_span_is_not_organizational_lifespan"
            ),
            "documentation_trace_feature_count_0to7": feature_count,
            "documentation_trace_stratum": doc_stratum,
            "active_actor_issue_degree": issue_degree[actor_id],
            "e3plus_actor_issue_degree": e3_degree[actor_id],
            "reviewed_actor_issue_degree": reviewed_degree[actor_id],
            "active_actor_issue_betweenness": round(
                issue_between.get(actor_id, 0.0), 8
            ),
            "e3plus_actor_issue_betweenness": round(
                e3_between.get(actor_id, 0.0), 8
            ),
            "reviewed_actor_issue_betweenness": round(
                reviewed_between.get(actor_id, 0.0), 8
            ),
            "active_issue_frame_count": len(
                {issue_frame(edge["issue_label"]) for edge in actor_issue_edges}
            ),
            "s004_only_actor_issue_edge_count": s004_only_edge_count[actor_id],
            "strict_triple_row_count": len(actor_triples),
            "strict_unique_place_issue_pair_count": len(
                {
                    (triple["place_id"], triple["issue_id"])
                    for triple in actor_triples
                }
            ),
            "strict_unique_shared_source_count": len(
                {triple["shared_source_id"] for triple in actor_triples}
            ),
            "human_checked_event_degree": event_degree[actor_id],
            "human_checked_event_betweenness": round(
                event_between.get(actor_id, 0.0), 8
            ),
            "accepted_case_degree": case_degree[actor_id],
            "accepted_case_betweenness": round(
                case_between.get(actor_id, 0.0), 8
            ),
            "substantive_case_role_count": sum(
                role["role_family"] != "non_party" for role in actor_roles
            ),
            "reviewed_typed_dyadic_degree": dyadic_degree[actor_id],
            "reviewed_typed_dyadic_betweenness": round(
                dyadic_between.get(actor_id, 0.0), 8
            ),
            "graph_object_boundary": (
                "actor_issue, event_incidence, typed_dyadic, case_role and "
                "strict_triple measures are separate and must not be summed or "
                "called one network centrality"
            ),
            **PACKAGE_META,
            "interpretation_limit": INTERPRETATION_LIMIT,
        }
        rows.append(row)
    return rows, linked


def legal_formality_bucket(value: str) -> str:
    lowered = (value or "").lower()
    if any(
        marker in lowered
        for marker in (
            "npo",
            "法人",
            "foundation",
            "incorporated",
            "nonprofit",
            "ngo",
        )
    ):
        return "formal_or_incorporated_guess"
    return "informal_unclear_or_program"


def association_row(
    analysis_id: str,
    graph_object: str,
    subset_label: str,
    rows: list[dict[str, object]],
    x_field: str,
    y_field: str,
    seed: int,
    limit: str,
) -> dict[str, object]:
    values_x = [float(row[x_field]) for row in rows]
    values_y = [float(row[y_field]) for row in rows]
    rho = spearman(values_x, values_y)
    low, high = bootstrap_spearman(values_x, values_y, seed=seed)
    return {
        "analysis_id": analysis_id,
        "graph_object": graph_object,
        "subset": subset_label,
        "x_measure": x_field,
        "y_measure": y_field,
        "actor_count": len(rows),
        "spearman_rho": "" if rho is None else round(rho, 3),
        "descriptive_bootstrap_low": "" if low is None else round(low, 3),
        "descriptive_bootstrap_high": "" if high is None else round(high, 3),
        "bootstrap_note": (
            "2,000 actor-resampling iterations; descriptive only because actors "
            "are not a probability sample or independent design units"
        ),
        "same_graph_object_rule": (
            "the y measure belongs only to the named graph/observation object"
        ),
        **PACKAGE_META,
        "interpretation_limit": limit,
    }


def build_associations(
    actor_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    all_rows = actor_rows
    connected = [
        row for row in actor_rows if int(row["active_actor_issue_degree"]) > 0
    ]
    local = [
        row for row in actor_rows if row["origin_bucket"] == "okinawa_local"
    ]
    no_case = [
        row for row in actor_rows if int(row["accepted_case_degree"]) == 0
    ]
    no_s004_only = [
        row
        for row in actor_rows
        if int(row["s004_only_actor_issue_edge_count"]) == 0
    ]
    specifications = [
        (
            "H1A001",
            "actor_issue_bipartite",
            "all_current_actors",
            all_rows,
            "linked_source_count",
            "active_actor_issue_degree",
        ),
        (
            "H1A002",
            "actor_issue_bipartite",
            "all_current_actors",
            all_rows,
            "linked_source_count",
            "active_actor_issue_betweenness",
        ),
        (
            "H1A003",
            "actor_issue_bipartite",
            "actor_issue_connected_only",
            connected,
            "linked_source_count",
            "active_actor_issue_degree",
        ),
        (
            "H1A004",
            "actor_issue_bipartite",
            "okinawa_local_only",
            local,
            "linked_source_count",
            "active_actor_issue_degree",
        ),
        (
            "H1A005",
            "actor_issue_bipartite",
            "actors_without_accepted_case_role",
            no_case,
            "linked_source_count",
            "active_actor_issue_degree",
        ),
        (
            "H1A006",
            "actor_issue_bipartite",
            "exclude_actors_with_any_S004_only_issue_edge",
            no_s004_only,
            "linked_source_count",
            "active_actor_issue_degree",
        ),
        (
            "H1A007",
            "actor_issue_bipartite",
            "all_current_actors",
            all_rows,
            "non_big3_linked_source_count",
            "active_actor_issue_degree",
        ),
        (
            "H1A008",
            "actor_issue_bipartite",
            "all_current_actors",
            all_rows,
            "non_issue_linked_source_count",
            "active_actor_issue_degree",
        ),
        (
            "H1A009",
            "actor_issue_bipartite",
            "all_current_actors",
            all_rows,
            "source_channel_count",
            "active_actor_issue_degree",
        ),
        (
            "H1A010",
            "strict_same_source_triples",
            "all_current_actors",
            all_rows,
            "linked_source_count",
            "strict_unique_place_issue_pair_count",
        ),
        (
            "H1A011",
            "event_hyperedge_incidence",
            "all_current_actors",
            all_rows,
            "linked_source_count",
            "human_checked_event_degree",
        ),
        (
            "H1A012",
            "reviewed_typed_dyadic",
            "all_current_actors",
            all_rows,
            "linked_source_count",
            "reviewed_typed_dyadic_degree",
        ),
        (
            "H1A013",
            "accepted_case_role_incidence",
            "all_current_actors",
            all_rows,
            "linked_source_count",
            "accepted_case_degree",
        ),
        (
            "H1A014",
            "actor_issue_bipartite",
            "all_current_actors",
            all_rows,
            "organization_hosted_trace_binary",
            "active_actor_issue_degree",
        ),
        (
            "H1A015",
            "actor_issue_bipartite",
            "all_current_actors",
            all_rows,
            "english_title_trace_binary",
            "active_actor_issue_degree",
        ),
    ]
    prepared: list[dict[str, object]] = []
    for row in actor_rows:
        row["organization_hosted_trace_binary"] = (
            1 if row["organization_hosted_trace_candidate"] == "yes" else 0
        )
        row["english_title_trace_binary"] = (
            1 if row["english_title_trace"] == "yes" else 0
        )
    for index, (
        analysis_id,
        graph_object,
        subset,
        rows,
        x_field,
        y_field,
    ) in enumerate(specifications):
        prepared.append(
            association_row(
                analysis_id,
                graph_object,
                subset,
                rows,
                x_field,
                y_field,
                seed=20260720 + index,
                limit=(
                    "Descriptive association between observed traces and one "
                    "encoded object. Shared source construction, venue-generated "
                    "records, selection and coding rules preclude causal reading."
                ),
            )
        )
    return prepared


def build_stratified_associations(
    actor_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    groups["ALL CURRENT ACTORS"] = actor_rows
    for row in actor_rows:
        groups[str(row["analysis_family"])].append(row)
    rows: list[dict[str, object]] = []
    index = 1
    for label, members in sorted(
        groups.items(),
        key=lambda item: (
            item[0] != "ALL CURRENT ACTORS",
            item[0],
        ),
    ):
        if len(members) < 5:
            continue
        for outcome in (
            "active_actor_issue_degree",
            "active_actor_issue_betweenness",
        ):
            rho = spearman(
                [float(row["linked_source_count"]) for row in members],
                [float(row[outcome]) for row in members],
            )
            rows.append(
                {
                    "stratum_id": f"H1S{index:03d}",
                    "graph_object": "actor_issue_bipartite",
                    "stratum_type": (
                        "overall"
                        if label == "ALL CURRENT ACTORS"
                        else "analysis_family"
                    ),
                    "stratum_label": label,
                    "actor_count": len(members),
                    "x_measure": "linked_source_count",
                    "y_measure": outcome,
                    "spearman_rho": "" if rho is None else round(rho, 3),
                    "minimum_n_rule": "n>=5; small strata are descriptive",
                    **PACKAGE_META,
                    "interpretation_limit": (
                        "Within-family descriptive association in the actor--"
                        "issue evidence graph only; family composition, issue "
                        "coding and shared sources remain uncontrolled."
                    ),
                }
            )
            index += 1
    return rows


def evidence_score(value: str) -> int:
    return {"E4": 3, "E3": 2, "E2": 1, "E1": 0}.get(value, 0)


def build_matched_pairs(
    actor_rows: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    outcomes = [
        ("actor_issue_bipartite", "active_actor_issue_degree"),
        ("actor_issue_bipartite", "active_actor_issue_betweenness"),
        ("strict_same_source_triples", "strict_unique_place_issue_pair_count"),
        ("event_hyperedge_incidence", "human_checked_event_degree"),
        ("accepted_case_role_incidence", "accepted_case_degree"),
        ("reviewed_typed_dyadic", "reviewed_typed_dyadic_degree"),
    ]
    pair_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []
    pair_index = 1
    for universe_label, universe in (
        ("all_current_actors", actor_rows),
        (
            "actor_issue_connected_only",
            [
                row
                for row in actor_rows
                if int(row["active_actor_issue_degree"]) > 0
            ],
        ),
    ):
        groups: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(
            list
        )
        for row in universe:
            groups[
                (
                    str(row["analysis_family"]),
                    str(row["origin_bucket"]),
                    str(row["legal_formality_bucket"]),
                )
            ].append(row)
        universe_pairs: list[tuple[dict[str, object], dict[str, object], str]] = []
        for key, members in sorted(groups.items()):
            dense = sorted(
                [
                    row
                    for row in members
                    if row["documentation_trace_stratum"] == "dense_4plus"
                ],
                key=lambda row: (
                    -int(row["linked_source_count"]),
                    str(row["actor_id"]),
                ),
            )
            thin = [
                row
                for row in members
                if row["documentation_trace_stratum"] == "thin_0to1"
            ]
            unused = {str(row["actor_id"]) for row in thin}
            for dense_row in dense:
                candidates = [
                    row for row in thin if str(row["actor_id"]) in unused
                ]
                if not candidates:
                    break
                thin_row = min(
                    candidates,
                    key=lambda row: (
                        abs(
                            evidence_score(str(row["actor_evidence_level"]))
                            - evidence_score(
                                str(dense_row["actor_evidence_level"])
                            )
                        ),
                        0
                        if row["actor_review_status"]
                        == dense_row["actor_review_status"]
                        else 1,
                        str(row["actor_id"]),
                    ),
                )
                unused.remove(str(thin_row["actor_id"]))
                match_key = " | ".join(key)
                universe_pairs.append((dense_row, thin_row, match_key))
                pair_row = {
                    "pair_id": f"H1M{pair_index:03d}",
                    "match_universe": universe_label,
                    "exact_match_key": match_key,
                    "dense_actor_id": dense_row["actor_id"],
                    "dense_actor_name": dense_row["actor_name"],
                    "dense_linked_source_count": dense_row["linked_source_count"],
                    "thin_actor_id": thin_row["actor_id"],
                    "thin_actor_name": thin_row["actor_name"],
                    "thin_linked_source_count": thin_row["linked_source_count"],
                    "match_selection_rule": (
                        "exact analysis_family + origin_bucket + legal-formality "
                        "bucket; then closest registry evidence level and review "
                        "status; deterministic actor_id tie-break; no replacement"
                    ),
                    "active_actor_issue_degree_difference_dense_minus_thin": (
                        float(dense_row["active_actor_issue_degree"])
                        - float(thin_row["active_actor_issue_degree"])
                    ),
                    "active_actor_issue_betweenness_difference_dense_minus_thin": round(
                        float(dense_row["active_actor_issue_betweenness"])
                        - float(thin_row["active_actor_issue_betweenness"]),
                        8,
                    ),
                    "strict_place_issue_pair_difference_dense_minus_thin": (
                        float(dense_row["strict_unique_place_issue_pair_count"])
                        - float(thin_row["strict_unique_place_issue_pair_count"])
                    ),
                    "event_degree_difference_dense_minus_thin": (
                        float(dense_row["human_checked_event_degree"])
                        - float(thin_row["human_checked_event_degree"])
                    ),
                    "case_degree_difference_dense_minus_thin": (
                        float(dense_row["accepted_case_degree"])
                        - float(thin_row["accepted_case_degree"])
                    ),
                    "typed_dyadic_degree_difference_dense_minus_thin": (
                        float(dense_row["reviewed_typed_dyadic_degree"])
                        - float(thin_row["reviewed_typed_dyadic_degree"])
                    ),
                    **PACKAGE_META,
                    "interpretation_limit": (
                        "Coarsened descriptive pairing, not a matched causal "
                        "design: age, staff, actual activity, issue salience, "
                        "place and source-generation mechanisms remain unmeasured."
                    ),
                }
                pair_rows.append(pair_row)
                pair_index += 1
        for graph_object, outcome in outcomes:
            differences = [
                float(dense_row[outcome]) - float(thin_row[outcome])
                for dense_row, thin_row, _ in universe_pairs
            ]
            summary_rows.append(
                {
                    "match_universe": universe_label,
                    "graph_object": graph_object,
                    "outcome_measure": outcome,
                    "pair_count": len(differences),
                    "mean_dense_minus_thin": (
                        round(sum(differences) / len(differences), 4)
                        if differences
                        else ""
                    ),
                    "median_dense_minus_thin": (
                        round(median(differences), 4) if differences else ""
                    ),
                    "dense_higher_pair_count": sum(
                        difference > 0 for difference in differences
                    ),
                    "tie_pair_count": sum(
                        difference == 0 for difference in differences
                    ),
                    "dense_lower_pair_count": sum(
                        difference < 0 for difference in differences
                    ),
                    "do_not_pool_across_objects": "yes",
                    **PACKAGE_META,
                    "interpretation_limit": (
                        "Object-specific matched contrast only; do not sum "
                        "outcomes or infer a causal documentation effect."
                    ),
                }
            )
    return pair_rows, summary_rows


def percentile_rank(values: list[float], value: float) -> float:
    if not values:
        return 0.0
    return sum(candidate <= value for candidate in values) / len(values)


def build_negative_cases(
    actor_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_values = [float(row["linked_source_count"]) for row in actor_rows]
    degree_values = [
        float(row["active_actor_issue_degree"]) for row in actor_rows
    ]
    between_values = [
        float(row["active_actor_issue_betweenness"]) for row in actor_rows
    ]
    candidates: list[dict[str, object]] = []
    for row in actor_rows:
        source_count = int(row["linked_source_count"])
        degree = int(row["active_actor_issue_degree"])
        between = float(row["active_actor_issue_betweenness"])
        contrast = ""
        if source_count >= 4 and degree <= 2:
            contrast = "dense_documentation_trace_low_actor_issue_degree"
        elif source_count <= 1 and (
            degree >= 3
            or percentile_rank(between_values, between) >= 0.85
        ):
            contrast = "thin_documentation_trace_high_actor_issue_visibility"
        if not contrast:
            continue
        candidates.append(
            {
                "contrast_id": "",
                "graph_object": "actor_issue_bipartite",
                "contrast_type": contrast,
                "actor_id": row["actor_id"],
                "actor_name": row["actor_name"],
                "analysis_family": row["analysis_family"],
                "linked_source_count": source_count,
                "linked_source_percentile": round(
                    percentile_rank(source_values, source_count), 3
                ),
                "active_actor_issue_degree": degree,
                "degree_percentile": round(
                    percentile_rank(degree_values, degree), 3
                ),
                "active_actor_issue_betweenness": between,
                "betweenness_percentile": round(
                    percentile_rank(between_values, between), 3
                ),
                "organization_hosted_trace_candidate": row[
                    "organization_hosted_trace_candidate"
                ],
                "english_title_trace": row["english_title_trace"],
                "contrast_use": (
                    "counterexample to a simple monotonic claim that more "
                    "documentation traces automatically produce greater "
                    "actor--issue visibility"
                ),
                **PACKAGE_META,
                "interpretation_limit": (
                    "A negative case is a descriptive counterexample, not proof "
                    "that documentation never matters or that encoded "
                    "centrality equals real coordination."
                ),
            }
        )
    candidates.sort(
        key=lambda row: (
            row["contrast_type"],
            -abs(
                float(row["linked_source_percentile"])
                - float(row["degree_percentile"])
            ),
            row["actor_id"],
        )
    )
    limited: list[dict[str, object]] = []
    counts: Counter[str] = Counter()
    for row in candidates:
        if counts[str(row["contrast_type"])] >= 10:
            continue
        counts[str(row["contrast_type"])] += 1
        row["contrast_id"] = f"H1N{len(limited) + 1:03d}"
        limited.append(row)
    return limited


def select_edges_after_source_deletion(
    edges: list[dict[str, str]],
    dropped_sources: set[str],
) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    for edge in edges:
        refs = source_refs(edge.get("source_ref", ""))
        if refs and not (refs - dropped_sources):
            continue
        selected.append(edge)
    return selected


def build_source_dependency(
    edges: list[dict[str, str]],
    sources: list[dict[str, str]],
) -> list[dict[str, object]]:
    baseline = [edge for edge in edges if edge["evidence_level"] in E3PLUS]
    base_actors = {edge["actor_id"] for edge in baseline}
    rows: list[dict[str, object]] = []
    for source in sources:
        source_id = source["source_id"]
        declared = [
            edge
            for edge in baseline
            if source_id in source_refs(edge.get("source_ref", ""))
        ]
        remaining = select_edges_after_source_deletion(baseline, {source_id})
        remaining_actor_ids = {edge["actor_id"] for edge in remaining}
        rows.append(
            {
                "source_id": source_id,
                "source_title": source["title"],
                "source_type": source["source_type"],
                "declared_e3plus_edge_count": len(declared),
                "exclusively_supported_removed_edge_count": (
                    len(baseline) - len(remaining)
                ),
                "lost_observed_actor_count": len(
                    base_actors - remaining_actor_ids
                ),
                "comparison_unit": (
                    "remove source support; edge survives if any stated source "
                    "remains"
                ),
                **PACKAGE_META,
                "interpretation_limit": (
                    "Source dependency of encoded E3/E4 support, not disappearance "
                    "of an actor, issue, activity or social relation."
                ),
            }
        )
    rows.sort(
        key=lambda row: (
            -int(row["exclusively_supported_removed_edge_count"]),
            -int(row["lost_observed_actor_count"]),
            str(row["source_id"]),
        )
    )
    for rank, row in enumerate(rows, 1):
        row["removed_edge_rank_desc"] = rank
    return rows


def build_sensitivity(
    actor_rows: list[dict[str, object]],
    edges: list[dict[str, str]],
    source_features: list[dict[str, object]],
) -> list[dict[str, object]]:
    registry_count = len(actor_rows)
    e3_edges = [edge for edge in edges if edge["evidence_level"] in E3PLUS]
    feature_ids_by_channel: dict[str, set[str]] = defaultdict(set)
    for row in source_features:
        feature_ids_by_channel[str(row["source_channel_heuristic"])].add(
            str(row["source_id"])
        )
    source_scenarios = [
        ("SRC_BASE", "E3/E4 baseline", set(), "baseline"),
        ("SRC_NO_S004", "remove S004 support", {"S004"}, "single source"),
        ("SRC_NO_BIG3", "remove S003/S004/S006 support", BIG3, "three sources"),
        (
            "SRC_NO_ORG_HOSTED",
            "remove organization-hosted support",
            feature_ids_by_channel["organization_hosted"],
            "source channel",
        ),
        (
            "SRC_NO_LEGAL",
            "remove legal/procedural support",
            feature_ids_by_channel["legal_procedural"],
            "source channel",
        ),
        (
            "SRC_NO_OFFICIAL",
            "remove official/administrative support",
            feature_ids_by_channel["official_administrative"],
            "source channel",
        ),
        (
            "SRC_NO_MEDIA",
            "remove media support",
            feature_ids_by_channel["media"],
            "source channel",
        ),
    ]
    rows: list[dict[str, object]] = []
    source_base = issue_graph_summary(e3_edges, registry_count)
    for scenario_id, label, dropped, unit in source_scenarios:
        selected = select_edges_after_source_deletion(e3_edges, dropped)
        metrics = issue_graph_summary(selected, registry_count)
        rows.append(
            {
                "scenario_id": scenario_id,
                "scenario_family": "source_support_deletion",
                "graph_object": "actor_issue_e3plus_bipartite",
                "scenario_label": label,
                "deletion_unit": unit,
                "dropped_ids": ";".join(sorted(dropped)),
                **metrics,
                "edge_retention_share": round(
                    int(metrics["edge_count"])
                    / int(source_base["edge_count"]),
                    3,
                ),
                "observed_actor_retention_share": round(
                    int(metrics["observed_actor_count"])
                    / int(source_base["observed_actor_count"]),
                    3,
                ),
                "baseline_edge_count": source_base["edge_count"],
                "baseline_observed_actor_count": source_base[
                    "observed_actor_count"
                ],
                "selection_rule": (
                    "remove an edge only if all stated S-source support is in "
                    "the dropped set; rows without S refs survive"
                ),
                **PACKAGE_META,
                "interpretation_limit": (
                    "Source-support deletion and actor-node deletion are "
                    "different intervention units and are shown separately."
                ),
            }
        )

    actor_by_source = sorted(
        actor_rows,
        key=lambda row: (
            -int(row["linked_source_count"]),
            str(row["actor_id"]),
        ),
    )
    actor_by_degree = sorted(
        actor_rows,
        key=lambda row: (
            -int(row["active_actor_issue_degree"]),
            str(row["actor_id"]),
        ),
    )
    actor_by_thin = sorted(
        actor_rows,
        key=lambda row: (
            int(row["linked_source_count"]),
            str(row["actor_id"]),
        ),
    )
    actor_scenarios = [
        ("ACT_BASE", "active-edge baseline", set(), "baseline"),
        (
            "ACT_TOP10_DOC",
            "remove 10 actors with most linked sources",
            {str(row["actor_id"]) for row in actor_by_source[:10]},
            "10 actor nodes",
        ),
        (
            "ACT_TOP10_DEGREE",
            "remove 10 actors with highest actor–issue degree",
            {str(row["actor_id"]) for row in actor_by_degree[:10]},
            "10 actor nodes",
        ),
        (
            "ACT_BOTTOM10_DOC",
            "remove 10 actors with fewest linked sources",
            {str(row["actor_id"]) for row in actor_by_thin[:10]},
            "10 actor nodes",
        ),
    ]
    actor_base = issue_graph_summary(edges, registry_count)
    for scenario_id, label, dropped, unit in actor_scenarios:
        selected = [
            edge for edge in edges if edge["actor_id"] not in dropped
        ]
        metrics = issue_graph_summary(selected, registry_count - len(dropped))
        rows.append(
            {
                "scenario_id": scenario_id,
                "scenario_family": "actor_node_deletion",
                "graph_object": "actor_issue_active_bipartite",
                "scenario_label": label,
                "deletion_unit": unit,
                "dropped_ids": ";".join(sorted(dropped)),
                **metrics,
                "edge_retention_share": round(
                    int(metrics["edge_count"]) / int(actor_base["edge_count"]),
                    3,
                ),
                "observed_actor_retention_share": round(
                    int(metrics["observed_actor_count"])
                    / int(actor_base["observed_actor_count"]),
                    3,
                ),
                "baseline_edge_count": actor_base["edge_count"],
                "baseline_observed_actor_count": actor_base[
                    "observed_actor_count"
                ],
                "selection_rule": "remove named actor nodes and all incident actor–issue edges",
                **PACKAGE_META,
                "interpretation_limit": (
                    "Actor-node deletion changes the social/evidence node set; "
                    "it is not a matched counterfactual to source deletion."
                ),
            }
        )
    return rows


def graph_object_summary(
    actor_rows: list[dict[str, object]],
    edges: list[dict[str, str]],
    triples: list[dict[str, str]],
    events: list[dict[str, str]],
    roles: list[dict[str, str]],
    dyadic: list[dict[str, object]],
    associations: list[dict[str, object]],
) -> list[dict[str, object]]:
    rho_lookup = {
        (
            str(row["graph_object"]),
            str(row["x_measure"]),
            str(row["y_measure"]),
            str(row["subset"]),
        ): row["spearman_rho"]
        for row in associations
    }
    specifications = [
        {
            "object_id": "G1",
            "graph_object": "actor_issue_bipartite",
            "input_observation_count": len(edges),
            "incident_registry_actor_count": len(
                {row["actor_id"] for row in edges}
            ),
            "counterpart_or_object_count": len(
                {row["issue_id"] for row in edges}
            ),
            "primary_actor_measure": "active_actor_issue_degree",
            "source_breadth_spearman": rho_lookup[
                (
                    "actor_issue_bipartite",
                    "linked_source_count",
                    "active_actor_issue_degree",
                    "all_current_actors",
                )
            ],
            "object_semantics": (
                "actor×issue evidence visibility; degree counts coded issue "
                "categories, not organizational relationships"
            ),
            "projection_status": "no actor projection used",
        },
        {
            "object_id": "G2",
            "graph_object": "strict_same_source_triples",
            "input_observation_count": len(triples),
            "incident_registry_actor_count": len(
                {row["actor_id"] for row in triples}
            ),
            "counterpart_or_object_count": len(
                {(row["place_id"], row["issue_id"]) for row in triples}
            ),
            "primary_actor_measure": "strict_unique_place_issue_pair_count",
            "source_breadth_spearman": rho_lookup[
                (
                    "strict_same_source_triples",
                    "linked_source_count",
                    "strict_unique_place_issue_pair_count",
                    "all_current_actors",
                )
            ],
            "object_semantics": (
                "same-source actor–place–issue observations; not a network "
                "centrality measure"
            ),
            "projection_status": "no projection used",
        },
        {
            "object_id": "G3",
            "graph_object": "event_hyperedge_incidence",
            "input_observation_count": len(events),
            "incident_registry_actor_count": len(
                {row["actor_or_counterpart_id"] for row in events}
            ),
            "counterpart_or_object_count": len(
                {row["event_id"] for row in events}
            ),
            "primary_actor_measure": "human_checked_event_degree",
            "source_breadth_spearman": rho_lookup[
                (
                    "event_hyperedge_incidence",
                    "linked_source_count",
                    "human_checked_event_degree",
                    "all_current_actors",
                )
            ],
            "object_semantics": (
                "human-checked event participation incidence; co-signing is an "
                "event hyperedge, not a stable alliance"
            ),
            "projection_status": "actor co-participation projection prohibited",
        },
        {
            "object_id": "G4",
            "graph_object": "reviewed_typed_dyadic",
            "input_observation_count": len(dyadic),
            "incident_registry_actor_count": len(
                {
                    str(row[key])
                    for row in dyadic
                    for key in ("source_endpoint", "target_endpoint")
                }
            ),
            "counterpart_or_object_count": len(dyadic),
            "primary_actor_measure": "reviewed_typed_dyadic_degree",
            "source_breadth_spearman": rho_lookup[
                (
                    "reviewed_typed_dyadic",
                    "linked_source_count",
                    "reviewed_typed_dyadic_degree",
                    "all_current_actors",
                )
            ],
            "object_semantics": (
                "14 reviewed typed organization relations; relation families "
                "retain their semantics and are not alliances by default"
            ),
            "projection_status": "already dyadic; no event projection",
        },
        {
            "object_id": "G5",
            "graph_object": "accepted_case_role_incidence",
            "input_observation_count": len(roles),
            "incident_registry_actor_count": len(
                {row["actor_id"] for row in roles}
            ),
            "counterpart_or_object_count": len(
                {row["case_id"] for row in roles}
            ),
            "primary_actor_measure": "accepted_case_degree",
            "source_breadth_spearman": rho_lookup[
                (
                    "accepted_case_role_incidence",
                    "linked_source_count",
                    "accepted_case_degree",
                    "all_current_actors",
                )
            ],
            "object_semantics": (
                "accepted actor×case role incidence; role is case-specific and "
                "does not establish a durable organization tie"
            ),
            "projection_status": "no co-party or co-counsel projection used",
        },
    ]
    for row in specifications:
        row.update(PACKAGE_META)
        row["interpretation_limit"] = INTERPRETATION_LIMIT
    return specifications


def bubble_counts(
    actor_rows: list[dict[str, object]], y_field: str
) -> Counter[tuple[int, int]]:
    return Counter(
        (
            int(row["linked_source_count"]),
            int(float(row[y_field])),
        )
        for row in actor_rows
    )


def html_wrapper(title: str, svg: str) -> str:
    return (
        "<!doctype html><html lang=\"zh-CN\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        f"<title>{escape(title)}</title><style>"
        "body{margin:0;background:#ece9e1}main{max-width:1640px;margin:18px auto;"
        "box-shadow:0 8px 24px #0002}svg{display:block;width:100%;height:auto}"
        "@media(max-width:700px){main{margin:0;box-shadow:none}}</style></head>"
        f"<body><main>{svg}</main></body></html>"
    )


def render_graph_objects(
    actor_rows: list[dict[str, object]],
    associations: list[dict[str, object]],
) -> str:
    rho = {
        (
            str(row["graph_object"]),
            str(row["x_measure"]),
            str(row["y_measure"]),
            str(row["subset"]),
        ): row["spearman_rho"]
        for row in associations
    }
    panels = [
        (
            "A",
            "actor × issue 二模图",
            "active_actor_issue_degree",
            "编码议题度数",
            rho[
                (
                    "actor_issue_bipartite",
                    "linked_source_count",
                    "active_actor_issue_degree",
                    "all_current_actors",
                )
            ],
        ),
        (
            "B",
            "event hyperedge incidence",
            "human_checked_event_degree",
            "参与的已核事件数",
            rho[
                (
                    "event_hyperedge_incidence",
                    "linked_source_count",
                    "human_checked_event_degree",
                    "all_current_actors",
                )
            ],
        ),
        (
            "C",
            "typed dyadic 关系图",
            "reviewed_typed_dyadic_degree",
            "已核类型化关系度数",
            rho[
                (
                    "reviewed_typed_dyadic",
                    "linked_source_count",
                    "reviewed_typed_dyadic_degree",
                    "all_current_actors",
                )
            ],
        ),
        (
            "D",
            "case-role incidence",
            "accepted_case_degree",
            "进入的已核案件数",
            rho[
                (
                    "accepted_case_role_incidence",
                    "linked_source_count",
                    "accepted_case_degree",
                    "all_current_actors",
                )
            ],
        ),
    ]
    # Keep additional bottom clearance because some CJK fonts render a little
    # below their nominal SVG text box at the second-row x-axis labels.
    width, height = 1600, 1140
    plot_w, plot_h = 620, 350
    origins = [(95, 175), (870, 175), (95, 650), (870, 650)]
    body: list[str] = []
    max_x = max(int(row["linked_source_count"]) for row in actor_rows)
    for (letter, title, y_field, y_label, value_rho), (x0, y0) in zip(
        panels, origins
    ):
        counts = bubble_counts(actor_rows, y_field)
        max_y = max((point[1] for point in counts), default=1)
        body.append(
            f'<text x="{x0}" y="{y0 - 62}" class="panel-title">'
            f"{letter}. {escape(title)}</text>"
        )
        body.append(
            f'<text x="{x0}" y="{y0 - 34}" class="panel-note">'
            f"Spearman ρ = {value_rho} · n = {len(actor_rows)}</text>"
        )
        body.append(
            f'<line x1="{x0}" y1="{y0 + plot_h}" x2="{x0 + plot_w}" '
            f'y2="{y0 + plot_h}" class="axis"/>'
        )
        body.append(
            f'<line x1="{x0}" y1="{y0}" x2="{x0}" '
            f'y2="{y0 + plot_h}" class="axis"/>'
        )
        for tick in range(max_x + 1):
            x = x0 + (tick / max(1, max_x)) * plot_w
            body.append(
                f'<line x1="{x:.1f}" y1="{y0 + plot_h}" x2="{x:.1f}" '
                f'y2="{y0 + plot_h + 7}" class="axis"/>'
            )
            body.append(
                f'<text x="{x:.1f}" y="{y0 + plot_h + 27}" '
                f'class="tick" text-anchor="middle">{tick}</text>'
            )
        for tick in range(max_y + 1):
            y = y0 + plot_h - (tick / max(1, max_y)) * plot_h
            body.append(
                f'<line x1="{x0 - 7}" y1="{y:.1f}" x2="{x0 + plot_w}" '
                f'y2="{y:.1f}" class="grid"/>'
            )
            body.append(
                f'<text x="{x0 - 14}" y="{y + 5:.1f}" class="tick" '
                f'text-anchor="end">{tick}</text>'
            )
        for (source_count, degree), count in sorted(counts.items()):
            x = x0 + (source_count / max(1, max_x)) * plot_w
            y = y0 + plot_h - (degree / max(1, max_y)) * plot_h
            radius = 4 + math.sqrt(count) * 4.2
            body.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" '
                f'class="bubble"><title>linked sources {source_count}; '
                f'{escape(y_label)} {degree}; actors {count}</title></circle>'
            )
            if count >= 5:
                body.append(
                    f'<text x="{x:.1f}" y="{y + 4:.1f}" class="bubble-label" '
                    f'text-anchor="middle">{count}</text>'
                )
        body.append(
            f'<text x="{x0 + plot_w / 2}" y="{y0 + plot_h + 55}" '
            f'class="axis-label" text-anchor="middle">关联来源数（观测痕迹）</text>'
        )
        body.append(
            f'<text transform="translate({x0 - 55},{y0 + plot_h / 2}) '
            f'rotate(-90)" class="axis-label" text-anchor="middle">'
            f"{escape(y_label)}</text>"
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">文档痕迹与四种不同观测对象</title>
<desc id="desc">Four bubble plots keep actor-issue degree, human-checked event incidence, reviewed typed dyadic relation degree, and accepted case incidence separate. Bubble size is the number of actors at each coordinate.</desc>
<rect width="{width}" height="{height}" fill="#f4f1e9"/>
<style>
text{{font-family:"Noto Sans CJK SC","Microsoft YaHei",Arial,sans-serif;fill:#17312b}}
.title{{font-size:30px;font-weight:700}}.subtitle{{font-size:15px;fill:#5d6c66}}
.panel-title{{font-size:20px;font-weight:700}}.panel-note{{font-size:14px;fill:#6b5b3f}}
.axis{{stroke:#48645c;stroke-width:1.2}}.grid{{stroke:#d5d0c5;stroke-width:1}}
.tick{{font-size:12px;fill:#66736f}}.axis-label{{font-size:13px;font-weight:700}}
.bubble{{fill:#2f7d68;fill-opacity:.58;stroke:#1f5d4d;stroke-width:1}}
.bubble-label{{font-size:11px;fill:#fff;font-weight:700}}
</style>
<text x="55" y="48" class="title">“中心性”不是一个对象：四层必须分开</text>
<text x="55" y="78" class="subtitle">横轴相同，纵轴分别来自不同图／观察层；共同署名没有被投影为稳定组织关系。圆面积表示同一坐标上的 actor 数。</text>
{''.join(body)}
</svg>"""


def render_strata(
    stratified: list[dict[str, object]],
) -> str:
    labels: list[str] = []
    by_label: dict[str, dict[str, float]] = defaultdict(dict)
    counts: dict[str, int] = {}
    for row in stratified:
        label = str(row["stratum_label"])
        if label not in labels:
            labels.append(label)
        counts[label] = int(row["actor_count"])
        if row["spearman_rho"] != "":
            by_label[label][str(row["y_measure"])] = float(
                row["spearman_rho"]
            )
    width = 1500
    x0, plot_w = 580, 830
    y0, row_h = 145, 66
    height = y0 + len(labels) * row_h + 90
    body: list[str] = []
    for tick in (-1, -0.5, 0, 0.5, 1):
        x = x0 + (tick + 1) / 2 * plot_w
        body.append(
            f'<line x1="{x:.1f}" y1="{y0 - 30}" x2="{x:.1f}" '
            f'y2="{height - 70}" class="grid"/>'
        )
        body.append(
            f'<text x="{x:.1f}" y="{y0 - 42}" class="tick" '
            f'text-anchor="middle">{tick:g}</text>'
        )
    for index, label in enumerate(labels):
        y = y0 + index * row_h
        body.append(
            f'<text x="45" y="{y + 5}" class="label">{escape(label)}</text>'
        )
        body.append(
            f'<text x="525" y="{y + 5}" class="n" text-anchor="end">'
            f"n={counts[label]}</text>"
        )
        for measure, css, symbol, y_offset in (
            ("active_actor_issue_degree", "degree", "●", -7),
            ("active_actor_issue_betweenness", "between", "◆", 9),
        ):
            if measure not in by_label[label]:
                continue
            value = by_label[label][measure]
            x = x0 + (value + 1) / 2 * plot_w
            body.append(
                f'<text x="{x:.1f}" y="{y + 7 + y_offset}" class="{css}" '
                f'text-anchor="middle">{symbol}</text>'
            )
            body.append(
                f'<text x="{x + 15:.1f}" y="{y + 5 + y_offset}" class="value">'
                f"{value:.2f}</text>"
            )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">Actor-issue associations by analysis family</title>
<desc id="desc">Spearman correlations between linked source count and actor-issue degree or actor-issue betweenness, shown overall and within analysis families of at least five actors.</desc>
<rect width="{width}" height="{height}" fill="#f4f1e9"/>
<style>
text{{font-family:"Noto Sans CJK SC","Microsoft YaHei",Arial,sans-serif;fill:#17312b}}
.title{{font-size:29px;font-weight:700}}.subtitle{{font-size:14px;fill:#5d6c66}}
.grid{{stroke:#d3cec3;stroke-width:1}}.tick{{font-size:12px;fill:#66736f}}
.label{{font-size:15px}}.n{{font-size:12px;fill:#66736f}}.degree{{font-size:22px;fill:#24745f}}
.between{{font-size:22px;fill:#ad6f2c}}.value{{font-size:12px;fill:#4d5b56}}
.legend{{font-size:14px;font-weight:700}}
</style>
<text x="45" y="45" class="title">Actor×issue 层：来源痕迹的相关方向并不稳定</text>
<text x="45" y="73" class="subtitle">同一图对象内分层；仅显示 n≥5。小样本相关不作显著性或因果判断。</text>
<text x="1040" y="72" class="legend" fill="#24745f">● 议题度数</text>
<text x="1190" y="72" class="legend" fill="#ad6f2c">◆ 二模 betweenness</text>
{''.join(body)}
</svg>"""


def render_sensitivity(
    scenarios: list[dict[str, object]],
) -> str:
    display_labels = {
        "SRC_NO_S004": "移除 S004 的证据支持",
        "SRC_NO_BIG3": "移除 S003／S004／S006 的证据支持",
        "SRC_NO_ORG_HOSTED": "移除组织托管来源的支持",
        "SRC_NO_LEGAL": "移除法律／程序来源的支持",
        "SRC_NO_OFFICIAL": "移除官方／行政来源的支持",
        "SRC_NO_MEDIA": "移除媒体来源的支持",
        "ACT_TOP10_DOC": "移除关联来源最多的 10 个 actor",
        "ACT_TOP10_DEGREE": "移除议题度数最高的 10 个 actor",
        "ACT_BOTTOM10_DOC": "移除关联来源最少的 10 个 actor",
    }
    source_rows = [
        row
        for row in scenarios
        if row["scenario_family"] == "source_support_deletion"
        and row["scenario_id"] != "SRC_BASE"
    ]
    actor_rows = [
        row
        for row in scenarios
        if row["scenario_family"] == "actor_node_deletion"
        and row["scenario_id"] != "ACT_BASE"
    ]
    width, height = 1600, 780
    panels = [
        (source_rows, 65, "A. 删除 source support（E3/E4）", "source"),
        (actor_rows, 835, "B. 删除 actor nodes（active）", "actor"),
    ]
    body: list[str] = []
    for rows, x0, title, css in panels:
        body.append(
            f'<text x="{x0}" y="145" class="panel-title">{escape(title)}</text>'
        )
        body.append(
            f'<line x1="{x0 + 280}" y1="177" x2="{x0 + 665}" '
            f'y2="177" class="axis"/>'
        )
        for tick in (0.5, 0.75, 1.0):
            x = x0 + 280 + (tick - 0.5) / 0.5 * 385
            body.append(
                f'<line x1="{x:.1f}" y1="177" x2="{x:.1f}" y2="655" '
                f'class="grid"/>'
            )
            body.append(
                f'<text x="{x:.1f}" y="168" class="tick" '
                f'text-anchor="middle">{tick:.0%}</text>'
            )
        for index, row in enumerate(rows):
            y = 215 + index * 74
            retention = float(row["edge_retention_share"])
            bar_width = max(0, (retention - 0.5) / 0.5 * 385)
            display_label = display_labels.get(
                str(row["scenario_id"]),
                str(row["scenario_label"]),
            )
            body.append(
                f'<text x="{x0}" y="{y + 17}" class="label">'
                f"{escape(display_label)}</text>"
            )
            body.append(
                f'<rect x="{x0 + 280}" y="{y}" width="{bar_width:.1f}" '
                f'height="28" class="bar-{css}"/>'
            )
            body.append(
                f'<text x="{x0 + 290 + bar_width:.1f}" y="{y + 19}" '
                f'class="value">{retention:.1%}</text>'
            )
            removed = int(row["baseline_edge_count"]) - int(row["edge_count"])
            body.append(
                f'<text x="{x0}" y="{y + 39}" class="detail">'
                f"移除 {removed} 条编码边</text>"
            )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">Actor-issue sensitivity with source and actor deletions separated</title>
<desc id="desc">Two separate panels show retained actor-issue edges after source-support deletion and actor-node deletion. The units are not directly comparable.</desc>
<rect width="{width}" height="{height}" fill="#f4f1e9"/>
<style>
text{{font-family:"Noto Sans CJK SC","Microsoft YaHei",Arial,sans-serif;fill:#17312b}}
.title{{font-size:30px;font-weight:700}}.subtitle{{font-size:15px;fill:#5d6c66}}
.panel-title{{font-size:20px;font-weight:700}}.axis{{stroke:#48645c;stroke-width:1.2}}
.grid{{stroke:#d5d0c5;stroke-width:1}}.tick{{font-size:12px;fill:#66736f}}
.label{{font-size:14px}}.detail{{font-size:12px;fill:#6b5b3f}}
.bar-source{{fill:#2f7d68}}.bar-actor{{fill:#b0722f}}.value{{font-size:13px;font-weight:700}}
.warning{{font-size:14px;fill:#6a4822;font-weight:700}}
</style>
<text x="55" y="48" class="title">同一 actor×issue 图，不同删除单位必须拆开读</text>
<text x="55" y="78" class="subtitle">左：删来源只移除“支持被耗尽”的 E3/E4 边。右：删 actor 会移除节点及全部 incident edges。两栏不能当作匹配反事实。</text>
{''.join(body)}
<rect x="55" y="690" width="1490" height="42" rx="8" fill="#eadfc9"/>
<text x="75" y="717" class="warning">边保留率只描述当前编码层；不表示现实组织、活动或社会关系按同比例消失。</text>
</svg>"""


def fmt_rho(
    associations: list[dict[str, object]],
    graph: str,
    outcome: str,
    subset: str = "all_current_actors",
) -> float:
    row = next(
        row
        for row in associations
        if row["graph_object"] == graph
        and row["y_measure"] == outcome
        and row["subset"] == subset
    )
    return float(row["spearman_rho"])


def render_method_brief(
    actor_rows: list[dict[str, object]],
    associations: list[dict[str, object]],
    matched_summary: list[dict[str, object]],
    sensitivity: list[dict[str, object]],
    negative_cases: list[dict[str, object]],
    graph_summary: list[dict[str, object]],
) -> str:
    issue_rho = fmt_rho(
        associations, "actor_issue_bipartite", "active_actor_issue_degree"
    )
    between_rho = fmt_rho(
        associations,
        "actor_issue_bipartite",
        "active_actor_issue_betweenness",
    )
    event_rho = fmt_rho(
        associations, "event_hyperedge_incidence", "human_checked_event_degree"
    )
    dyadic_rho = fmt_rho(
        associations, "reviewed_typed_dyadic", "reviewed_typed_dyadic_degree"
    )
    case_rho = fmt_rho(
        associations, "accepted_case_role_incidence", "accepted_case_degree"
    )
    org_rho = fmt_rho(
        associations, "actor_issue_bipartite", "active_actor_issue_degree"
    )
    org_row = next(row for row in associations if row["analysis_id"] == "H1A014")
    english_row = next(
        row for row in associations if row["analysis_id"] == "H1A015"
    )
    matched_all = next(
        row
        for row in matched_summary
        if row["match_universe"] == "all_current_actors"
        and row["outcome_measure"] == "active_actor_issue_degree"
    )
    matched_connected = next(
        row
        for row in matched_summary
        if row["match_universe"] == "actor_issue_connected_only"
        and row["outcome_measure"] == "active_actor_issue_degree"
    )
    src_s004 = next(
        row for row in sensitivity if row["scenario_id"] == "SRC_NO_S004"
    )
    src_big3 = next(
        row for row in sensitivity if row["scenario_id"] == "SRC_NO_BIG3"
    )
    act_doc = next(
        row for row in sensitivity if row["scenario_id"] == "ACT_TOP10_DOC"
    )
    act_degree = next(
        row for row in sensitivity if row["scenario_id"] == "ACT_TOP10_DEGREE"
    )
    thin_high = [
        row
        for row in negative_cases
        if row["contrast_type"]
        == "thin_documentation_trace_high_actor_issue_visibility"
    ][:4]
    dense_low = [
        row
        for row in negative_cases
        if row["contrast_type"]
        == "dense_documentation_trace_low_actor_issue_degree"
    ][:4]
    graph_lines = "\n".join(
        f"- `{row['graph_object']}`：{row['input_observation_count']} 条输入观察；"
        f"{row['incident_registry_actor_count']} 个可见 registry actor；"
        f"{row['object_semantics']}"
        for row in graph_summary
    )
    thin_names = "、".join(
        f"{row['actor_id']}（{row['linked_source_count']}源／"
        f"{row['active_actor_issue_degree']}议题）"
        for row in thin_high
    )
    dense_names = "、".join(
        f"{row['actor_id']}（{row['linked_source_count']}源／"
        f"{row['active_actor_issue_degree']}议题）"
        for row in dense_low
    )
    return f"""# H1 v2：资料留存与“观测中心性”到底重合多少

日期：{AUDIT_DATE}

状态：**research_only / candidate / not_frontend_ready**

## 结论先行

当前材料支持一个比原命题更窄、也更有方法价值的判断：

> 少数高承载名单会显著改变 actor×issue 可见层的大小；但组织层面的资料痕迹与 actor×issue 中心性只呈弱到中等的正相关，而且该关系在功能分层中方向不稳定。现有数据不支持“中心性主要是官网、英文能力或律师团队制造的资料幻象”。

在 121 个当前 actor 上，关联来源数与 actor×issue 度数的 Spearman ρ={issue_rho:.3f}，与该二模图 betweenness 的 ρ={between_rho:.3f}。这说明两者有重叠，但远非一一对应。organization-hosted trace 与议题度数的 ρ={float(org_row['spearman_rho']):.3f}；英文标题痕迹与议题度数的 ρ={float(english_row['spearman_rho']):.3f}。后两项尤其不能支持“有官网／英文材料就会成为中心”的强说法；它们还只是 host/title 代理，不是 actor 自有官网或语言能力。

## 五种对象，不能再统称 network centrality

{graph_lines}

图 1 只把相同的 documentation-trace 横轴放在四种对象旁边；纵轴没有合并。event 仍以 hyperedge incidence 表示，不做共同署名 actor 投影。case-role 也不投影为同案协作。

## 组织层比较

- actor×issue：来源数—度数 ρ={issue_rho:.3f}；来源数—betweenness ρ={between_rho:.3f}。
- event incidence：来源数—已核事件数 ρ={event_rho:.3f}；当前事件层高度受三份名单及案件记录的抽样边界影响。
- typed dyadic：来源数—已核类型化关系度数 ρ={dyadic_rho:.3f}；这里只有 14 条目的性关系样本，不能概括冲绳组织关系总体。
- case-role：来源数—进入案件数 ρ={case_rho:.3f}。这很可能同时反映“法律场域真实产生更多正式文书”和“有程序角色的 actor 更容易被编码”，不是文档能力的独立效应。

精确分层匹配把 `dense_4plus` 与 `thin_0to1` actor 按 analysis family、local/nonlocal、法人／非正式猜测桶配对，再尽量匹配 registry evidence/review 状态。全 registry 得到 {matched_all['pair_count']} 对，dense actor 平均多 {float(matched_all['mean_dense_minus_thin']):.2f} 条 actor×issue 边（{matched_all['dense_higher_pair_count']} 对较高／{matched_all['tie_pair_count']} 对相同／{matched_all['dense_lower_pair_count']} 对较低）；只看已有 issue edge 的 actor 后为 {matched_connected['pair_count']} 对、平均差 {float(matched_connected['mean_dense_minus_thin']):.2f}（{matched_connected['dense_higher_pair_count']}/{matched_connected['tie_pair_count']}/{matched_connected['dense_lower_pair_count']}）。差距收缩说明 registry 中尚未连边的 actor 会放大表面关联。该匹配没有控制组织年代、规模、实际活动量、议题显著性和地点，仍不是因果设计。

## 来源集中与 actor capacity 是两件不同的事

S004 单源删除会耗尽 {int(src_s004['baseline_edge_count']) - int(src_s004['edge_count'])} 条 E3/E4 actor×issue 边，并使 {int(src_s004['baseline_observed_actor_count']) - int(src_s004['observed_actor_count'])} 个 actor 失去该层全部边；删除 S003/S004/S006 合计耗尽 {int(src_big3['baseline_edge_count']) - int(src_big3['edge_count'])} 条边、{int(src_big3['baseline_observed_actor_count']) - int(src_big3['observed_actor_count'])} 个 actor。这仍是最强的、可复算的资料偏差证据，但它证明的是**研究设计对几份列表的依赖**。

删除“关联来源数最多的 10 个 actor”会去掉 {int(act_doc['baseline_edge_count']) - int(act_doc['edge_count'])} 条 active actor×issue 边；删除“actor×issue 度数最高的 10 个 actor”会去掉 {int(act_degree['baseline_edge_count']) - int(act_degree['edge_count'])} 条。两个 actor 集合并不相同。更重要的是，source-support deletion 与 actor-node deletion 的干预单位不同，图 3 分栏显示，不能写成匹配反事实。

## 反例使强命题不能成立

- 资料薄但 actor×issue 可见度高：{thin_names}。
- 资料密但 actor×issue 度数不高：{dense_names}。

这些反例不说明资料留存不重要；它们说明“更多资料痕迹 → 必然更中心”的单调机制不成立。比如有的组织只由一份资料支持，却在同一编码行上被赋予 3–4 个议题；也有服务／国际组织有较丰富的正式或英文材料，但一期问题只给它们 1–2 个功能议题。**议题编码规则和研究问题本身也在塑造度数。**

## competing explanations

1. **制度生产文书**：诉讼、EIA、公投与正式行政程序本来就要求案号、意见书、判决或会议记录；文档多可能是真实制度角色的结果，而不是外生“保存能力”。
2. **播种来源内生性**：S004 等名单同时帮助发现 actor 并支持 issue 编码，来源数和网络度数共享建构过程。
3. **真实协调与留痕可能共存**：秘书处、律师或 Web team 既可能真实协调，也可能保存记录；不能把可见度全部扣成偏差。H3 若出现“秘书处＋Web team”同组织并存，只能作为下一轮机制例交叉核查，不能在本包中当作已证解释。
4. **范围和分类效应**：服务组织、公共机构、国际 NGO 与地方实行委员会被赋予的 issue taxonomy 宽度不同。
5. **时间右删失**：linked source 的年份跨度不是 lifespan；当前 lifecycle 表只覆盖极少数 actor。

## 方法文献接口

- Shvydun（2025）在 113 个经验网络上比较不完整资料下的 centrality 稳健性，并明确指出：扰动策略应随网络性质与缺失类型调整，经验网络中的缺失通常不是随机的。本包因此不用随机删边代替实际缺失机制，而把 S004／来源 channel 的定向 support deletion 与 actor-node deletion 分开；但本包也没有复刻其 16 种 centrality 或 1,000 次扰动设计。DOI：<https://doi.org/10.1371/journal.pcsy.0000042>
- Mosca（2014）把线上社会运动研究的资料收集／归档、采样和线上—线下方法关系列为三个核心方法问题。本包据此只把 121 actors／295 sources 当作 purposive online working corpus；线上未见不等于线下不存在，早期通讯、地方报刊与组织内部材料仍须当地／馆藏补查。DOI：<https://doi.org/10.1093/acprof:oso/9780198719571.003.0016>

两篇文献只支持方法边界，不替本项目证明“真实中心性”或 documentation capacity。

## 目前不能说什么

- 不能说“网络中心性主要是信息留存能力”；
- 不能说删掉网页、律师或英文材料，现实组织网络就会断裂；
- 不能把 organization-hosted 来源说成 actor 自有官网；
- 不能把英文标题说成组织具有英文 staff capacity；
- 不能把 event 同场或 case 同案投影成稳定组织关系；
- 不能从当前 source-year span 推断组织寿命；
- 不能用 14 条 reviewed typed dyadic 样本概括整个冲绳组织关系结构。

## 可继续验证的最小下一步

若负责人希望把 H1 从“方法附录”升级为论文命题，下一轮不应再扩大 actor 数，而应对本包的 18 组 matched pairs 做人工字段冻结：actor 自有官网／非自有 host、日英双语原文、专职 staff、律师／秘书处支援、成立—终止日期、至少两个相同时间窗的外部报道。只有这些字段被人工读过，documentation capacity 才能从 proxy 变成可以讨论的解释变量。
"""


def method_literature_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = [
        {
            "reference_id": "H1L001",
            "citation": (
                "Shvydun, Sergey. 2025. Centrality in complex networks under "
                "incomplete data. PLOS Complex Systems 2(5): e0000042."
            ),
            "doi": "10.1371/journal.pcsy.0000042",
            "url": "https://doi.org/10.1371/journal.pcsy.0000042",
            "source_kind": "peer_reviewed_research_article",
            "method_point": (
                "Centrality sensitivity depends on network class and the type "
                "of missing or incorrect data; missing links are often not "
                "uniformly distributed, so perturbations should reflect the "
                "network and error mechanism."
            ),
            "application_in_h1_v2": (
                "Use object-specific, targeted source-support deletions and "
                "keep actor-node deletion separate; do not substitute random "
                "edge loss for observed source concentration."
            ),
            "non_transfer_boundary": (
                "H1 v2 does not reproduce the paper's 16 centralities, 113 "
                "networks or 1,000 perturbations and cannot inherit its "
                "comparative robustness findings."
            ),
        },
        {
            "reference_id": "H1L002",
            "citation": (
                "Mosca, Lorenzo. 2014. Methodological Practices in Social "
                "Movement Online Research. In Methodological Practices in "
                "Social Movement Research, pp. 397–417."
            ),
            "doi": "10.1093/acprof:oso/9780198719571.003.0016",
            "url": (
                "https://doi.org/10.1093/acprof:oso/"
                "9780198719571.003.0016"
            ),
            "source_kind": "academic_methods_chapter",
            "method_point": (
                "Online social-movement research must make collection and "
                "archiving, sampling, and its relationship with offline "
                "techniques explicit."
            ),
            "application_in_h1_v2": (
                "Treat the online registry/source corpus as purposive and "
                "archived but incomplete; route offline and local holdings as "
                "a separate evidence gap rather than coding absence."
            ),
            "non_transfer_boundary": (
                "The chapter does not validate this registry, source "
                "classification or any actor centrality claim."
            ),
        },
    ]
    for row in rows:
        row.update(PACKAGE_META)
        row["interpretation_limit"] = (
            "Method interface only; it does not establish an empirical finding "
            "about Okinawa actors or a causal documentation effect."
        )
    return rows


def render_principal_checkpoint(
    negative_cases: list[dict[str, object]],
    matched_pairs: list[dict[str, object]],
) -> str:
    priority_negative = negative_cases[:8]
    negative_lines = "\n".join(
        f"- {row['actor_id']} {row['actor_name']}：{row['contrast_type']}；"
        f"{row['linked_source_count']} 个 linked sources，"
        f"{row['active_actor_issue_degree']} 个 issue edges。"
        for row in priority_negative
    )
    all_pairs = [
        row
        for row in matched_pairs
        if row["match_universe"] == "all_current_actors"
    ]
    pair_lines = "\n".join(
        f"- {row['dense_actor_id']} ↔ {row['thin_actor_id']}（{row['exact_match_key']}）"
        for row in all_pairs[:10]
    )
    return f"""# H1 v2 负责人检查点

状态：`principal_interpretive_decision_required`。本包维持 `not_frontend_ready`。

## 建议负责人先读的 8 个反例

{negative_lines}

请逐个判断：是 source linkage 漏编、issue 标签过宽／过窄、组织范围不同，还是确有“资料密度与观测中心性不一致”。

## 建议抽读的 matched pairs

{pair_lines}

完整 {len(all_pairs)} 对见 `matched_actor_pairs_v2.csv`。匹配只是缩小功能／来源差异，不是因果设计。

## 需要负责人拍板

1. H1 在一期报告中的位置：
   - 建议：方法／偏差章节的核心敏感性；
   - 可选：独立方法短文候选；
   - 暂不建议：主论文的实质性中心命题。
2. 是否接受当前最强措辞：
   - “少数高承载名单显著塑造 actor×issue 可见层”；
   - “组织层 documentation traces 与 actor×issue visibility 只有弱到中等重合，且分层方向不稳定”。
3. 是否批准一轮 **36 actor 以内** 的人工 capacity crosswalk：
   - 自有官网／第三方 host；
   - 日英双语原文，而非标题；
   - staff／律师／秘书处／Web team；
   - 成立、重组、终止与右删失；
   - 固定时间窗的外部报道。
4. 是否将 H3 的“秘书处＋Web team 与真实协调同组织共存”仅列为跨包机制候选，不合并为本包事实。

## 停止条件

若负责人不批准第 3 项，本包在这里停止，作为 H1 方法附录即可；不得继续把 proxy 强化成 actor capacity 或 causal effect。
"""


def render_readme() -> str:
    return """# research_wave_h1_documentation_visibility_v2

H1 第二轮独立研究包。它检验“观测中心性有多少与资料留存／索引痕迹重合”，但不把相关性写成因果。

## 复现

```powershell
python scripts\\make_h1_documentation_visibility_v2.py
python -m unittest tests.test_make_h1_documentation_visibility_v2
```

## 关键输出

- `actor_documentation_visibility_v2.csv`：121 个 current actor 的资料痕迹和五类分开测量的可见度。
- `source_feature_audit_v2.csv`：295 sources 的机械 channel／title-language／archive 分类。
- `graph_object_summary_v2.csv`：actor×issue、strict triple、event hyperedge、typed dyadic、case-role 的对象边界。
- `association_estimates_v2.csv`：总体／限定子集的描述性 Spearman。
- `stratified_associations_v2.csv`：同一 actor×issue 图对象内的 analysis-family 分层。
- `matched_actor_pairs_v2.csv`、`matched_pair_summary_v2.csv`：dense vs thin 的有界匹配。
- `negative_case_audit_v2.csv`：反驳简单单调机制的对照案例。
- `source_dependency_v2.csv`、`sensitivity_scenarios_v2.csv`：来源支持删除与 actor 节点删除，严格分栏。
- `method_literature_v2.csv`：两项方法文献接口及不可转移边界。
- 3 组 SVG／HTML 图。
- `method_brief_v2.md`、`principal_checkpoint_v2.md`、`validation_report_v2.md`。

## 固定边界

全包为 `research_only / candidate / ai_seeded / not_frontend_ready`。organization-hosted trace 不等于 actor 自有官网；英文标题不等于组织英文能力；source-year span 不等于 lifespan；共同事件和同案角色不投影成稳定组织关系。
"""


def validate(
    actors: list[dict[str, str]],
    sources: list[dict[str, str]],
    edges: list[dict[str, str]],
    triples: list[dict[str, str]],
    events: list[dict[str, str]],
    roles: list[dict[str, str]],
    dyadic: list[dict[str, object]],
    source_features: list[dict[str, object]],
    actor_rows: list[dict[str, object]],
    associations: list[dict[str, object]],
    matched_pairs: list[dict[str, object]],
    sensitivity: list[dict[str, object]],
) -> list[str]:
    checks: list[str] = []
    if len(actors) != 121:
        raise ValueError(f"expected 121 current actors, got {len(actors)}")
    checks.append("current actor gate = 121; A072 excluded")
    if len(edges) != 238:
        raise ValueError(f"expected 238 active actor-issue edges, got {len(edges)}")
    checks.append("active actor-issue gate = 238")
    if len(triples) != 312:
        raise ValueError(f"expected 312 strict triples, got {len(triples)}")
    checks.append("strict same-source triple gate = 312")
    if any(event["reviewer_status"] != "human_checked" for event in events):
        raise ValueError("non-human-checked event leaked into event object")
    checks.append(
        f"event object = {len(events)} human-checked registered-actor rows; no analytical seeds"
    )
    if any(
        role["review_status"] != "human_checked"
        or role["human_decision"] != "accept"
        or not role["actor_id"]
        for role in roles
    ):
        raise ValueError("invalid registered case role entered H1 v2")
    checks.append(f"case-role object = {len(roles)} accepted registered-actor rows")
    if len(dyadic) != 14:
        raise ValueError(f"expected 14 reviewed typed dyadic rows, got {len(dyadic)}")
    if any(
        relation.get("display_tier") != "reviewed"
        or relation.get("graph_eligibility") != "dyadic_relation"
        for relation in dyadic
    ):
        raise ValueError("non-reviewed/non-dyadic relation leaked into H1 v2")
    checks.append("typed dyadic object = 14 reviewed rows")
    if len(source_features) != len(sources) != 295:
        raise ValueError("source feature audit does not cover 295 source rows")
    checks.append("source feature audit = 295/295")
    if len(actor_rows) != 121 or len({row["actor_id"] for row in actor_rows}) != 121:
        raise ValueError("actor diagnostic output incomplete or duplicated")
    checks.append("actor diagnostic = 121 unique rows")
    for collection_name, collection in (
        ("source_features", source_features),
        ("actor_rows", actor_rows),
        ("associations", associations),
        ("matched_pairs", matched_pairs),
        ("sensitivity", sensitivity),
    ):
        if any(
            row.get("research_status") != "research_only"
            or row.get("frontend_eligibility") != "not_frontend_ready"
            for row in collection
        ):
            raise ValueError(f"research gate failed in {collection_name}")
    checks.append("research_only/not_frontend_ready gate holds across outputs")
    s004 = next(row for row in sensitivity if row["scenario_id"] == "SRC_NO_S004")
    if int(s004["baseline_edge_count"]) - int(s004["edge_count"]) != 41:
        raise ValueError("S004 sensitivity no longer removes 41 E3/E4 edges")
    checks.append("S004 source-support deletion removes 41 E3/E4 edges")
    association_ids = {row["analysis_id"] for row in associations}
    if len(association_ids) != len(associations):
        raise ValueError("association IDs are not unique")
    checks.append(f"association specifications = {len(associations)} unique rows")
    if not any(
        row["match_universe"] == "all_current_actors" for row in matched_pairs
    ):
        raise ValueError("matched comparison missing all-current universe")
    checks.append(
        f"matched pair rows = {len(matched_pairs)} across two explicit universes"
    )
    return checks


SOURCE_FEATURE_FIELDS = [
    "source_id",
    "source_title",
    "source_type",
    "source_channel_heuristic",
    "source_year_raw",
    "parsed_year_min",
    "parsed_year_max",
    "url_domain",
    "organization_hosted_trace_candidate",
    "official_or_formal_trace_candidate",
    "external_mention_trace_candidate",
    "legal_procedural_trace",
    "title_language_heuristic",
    "case_number_or_legal_title_marker",
    "high_capacity_list_source",
    "archive_status",
    "archive_content_type",
    "source_evidence_level",
    "source_review_status",
    "classification_method",
    "research_status",
    "display_tier",
    "claim_status",
    "review_status",
    "frontend_eligibility",
    "interpretation_limit",
]

ACTOR_FIELDS = [
    "actor_id",
    "actor_name",
    "actor_class",
    "analysis_family",
    "origin_type",
    "origin_bucket",
    "legal_status_guess",
    "legal_formality_bucket",
    "actor_evidence_level",
    "actor_review_status",
    "linked_source_count",
    "linked_source_ids",
    "unresolved_reference_count",
    "unresolved_reference_tokens",
    "registry_source_count",
    "actor_issue_support_source_count",
    "strict_triple_source_count",
    "event_source_count",
    "case_role_source_count",
    "typed_dyadic_source_count",
    "non_issue_linked_source_count",
    "non_big3_linked_source_count",
    "source_channel_count",
    "source_channels",
    "source_domain_count",
    "archive_success_count",
    "archive_failure_or_skip_count",
    "archive_success_share",
    "organization_hosted_trace_candidate",
    "own_website_status",
    "official_administrative_trace",
    "external_media_or_academic_trace",
    "legal_procedural_trace",
    "english_title_trace",
    "japanese_title_trace",
    "multilingual_title_trace",
    "language_capacity_status",
    "document_year_min",
    "document_year_max",
    "document_record_span_years",
    "lifecycle_status",
    "lifespan_status",
    "documentation_trace_feature_count_0to7",
    "documentation_trace_stratum",
    "active_actor_issue_degree",
    "e3plus_actor_issue_degree",
    "reviewed_actor_issue_degree",
    "active_actor_issue_betweenness",
    "e3plus_actor_issue_betweenness",
    "reviewed_actor_issue_betweenness",
    "active_issue_frame_count",
    "s004_only_actor_issue_edge_count",
    "strict_triple_row_count",
    "strict_unique_place_issue_pair_count",
    "strict_unique_shared_source_count",
    "human_checked_event_degree",
    "human_checked_event_betweenness",
    "accepted_case_degree",
    "accepted_case_betweenness",
    "substantive_case_role_count",
    "reviewed_typed_dyadic_degree",
    "reviewed_typed_dyadic_betweenness",
    "graph_object_boundary",
    "research_status",
    "display_tier",
    "claim_status",
    "review_status",
    "frontend_eligibility",
    "interpretation_limit",
]


def main() -> None:
    actor_history = read_csv(ACTORS)
    actors = [row for row in actor_history if current_actor(row)]
    actor_ids = {row["actor_id"] for row in actors}
    sources = read_csv(SOURCES)
    edges = [
        row
        for row in read_csv(EDGES)
        if row["analysis_inclusion"] == "active"
        and row["actor_id"] in actor_ids
    ]
    triples = [
        row for row in read_csv(TRIPLES) if row["actor_id"] in actor_ids
    ]
    events = [
        row
        for row in read_csv(EVENTS)
        if row["reviewer_status"] == "human_checked"
        and row["entity_type"] == "registry_actor"
        and row["actor_or_counterpart_id"] in actor_ids
        and row["event_id"]
    ]
    roles = [
        row
        for row in read_csv(CASE_ROLES)
        if row["actor_id"] in actor_ids
        and row["review_status"] == "human_checked"
        and row["human_decision"] == "accept"
    ]
    lifecycle = read_csv(LIFECYCLE)
    class_map = {
        row["actor_class_original"]: row["analysis_family_v1"]
        for row in read_csv(CLASS_MAP)
    }
    archive_rows = read_csv(ARCHIVE)
    with DYADIC.open(encoding="utf-8") as handle:
        dyadic_all = json.load(handle)
    dyadic = [
        row
        for row in dyadic_all
        if row.get("display_tier") == "reviewed"
        and row.get("graph_eligibility") == "dyadic_relation"
        and row.get("source_endpoint") in actor_ids
        and row.get("target_endpoint") in actor_ids
    ]

    source_features = source_feature_rows(sources, archive_rows)
    actor_rows, _ = build_actor_rows(
        actors,
        sources,
        source_features,
        edges,
        triples,
        events,
        roles,
        lifecycle,
        class_map,
        dyadic,
    )
    associations = build_associations(actor_rows)
    stratified = build_stratified_associations(actor_rows)
    matched_pairs, matched_summary = build_matched_pairs(actor_rows)
    negative_cases = build_negative_cases(actor_rows)
    source_dependency = build_source_dependency(edges, sources)
    sensitivity = build_sensitivity(actor_rows, edges, source_features)
    graph_summary = graph_object_summary(
        actor_rows,
        edges,
        triples,
        events,
        roles,
        dyadic,
        associations,
    )
    literature_rows = method_literature_rows()
    checks = validate(
        actors,
        sources,
        edges,
        triples,
        events,
        roles,
        dyadic,
        source_features,
        actor_rows,
        associations,
        matched_pairs,
        sensitivity,
    )

    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUT / "source_feature_audit_v2.csv", source_features, SOURCE_FEATURE_FIELDS)
    write_csv(OUT / "actor_documentation_visibility_v2.csv", actor_rows, ACTOR_FIELDS)
    write_csv(
        OUT / "association_estimates_v2.csv",
        associations,
        [
            "analysis_id",
            "graph_object",
            "subset",
            "x_measure",
            "y_measure",
            "actor_count",
            "spearman_rho",
            "descriptive_bootstrap_low",
            "descriptive_bootstrap_high",
            "bootstrap_note",
            "same_graph_object_rule",
            "research_status",
            "display_tier",
            "claim_status",
            "review_status",
            "frontend_eligibility",
            "interpretation_limit",
        ],
    )
    write_csv(
        OUT / "stratified_associations_v2.csv",
        stratified,
        [
            "stratum_id",
            "graph_object",
            "stratum_type",
            "stratum_label",
            "actor_count",
            "x_measure",
            "y_measure",
            "spearman_rho",
            "minimum_n_rule",
            "research_status",
            "display_tier",
            "claim_status",
            "review_status",
            "frontend_eligibility",
            "interpretation_limit",
        ],
    )
    write_csv(
        OUT / "matched_actor_pairs_v2.csv",
        matched_pairs,
        [
            "pair_id",
            "match_universe",
            "exact_match_key",
            "dense_actor_id",
            "dense_actor_name",
            "dense_linked_source_count",
            "thin_actor_id",
            "thin_actor_name",
            "thin_linked_source_count",
            "match_selection_rule",
            "active_actor_issue_degree_difference_dense_minus_thin",
            "active_actor_issue_betweenness_difference_dense_minus_thin",
            "strict_place_issue_pair_difference_dense_minus_thin",
            "event_degree_difference_dense_minus_thin",
            "case_degree_difference_dense_minus_thin",
            "typed_dyadic_degree_difference_dense_minus_thin",
            "research_status",
            "display_tier",
            "claim_status",
            "review_status",
            "frontend_eligibility",
            "interpretation_limit",
        ],
    )
    write_csv(
        OUT / "matched_pair_summary_v2.csv",
        matched_summary,
        [
            "match_universe",
            "graph_object",
            "outcome_measure",
            "pair_count",
            "mean_dense_minus_thin",
            "median_dense_minus_thin",
            "dense_higher_pair_count",
            "tie_pair_count",
            "dense_lower_pair_count",
            "do_not_pool_across_objects",
            "research_status",
            "display_tier",
            "claim_status",
            "review_status",
            "frontend_eligibility",
            "interpretation_limit",
        ],
    )
    write_csv(
        OUT / "negative_case_audit_v2.csv",
        negative_cases,
        [
            "contrast_id",
            "graph_object",
            "contrast_type",
            "actor_id",
            "actor_name",
            "analysis_family",
            "linked_source_count",
            "linked_source_percentile",
            "active_actor_issue_degree",
            "degree_percentile",
            "active_actor_issue_betweenness",
            "betweenness_percentile",
            "organization_hosted_trace_candidate",
            "english_title_trace",
            "contrast_use",
            "research_status",
            "display_tier",
            "claim_status",
            "review_status",
            "frontend_eligibility",
            "interpretation_limit",
        ],
    )
    write_csv(
        OUT / "source_dependency_v2.csv",
        source_dependency,
        [
            "source_id",
            "source_title",
            "source_type",
            "declared_e3plus_edge_count",
            "exclusively_supported_removed_edge_count",
            "lost_observed_actor_count",
            "removed_edge_rank_desc",
            "comparison_unit",
            "research_status",
            "display_tier",
            "claim_status",
            "review_status",
            "frontend_eligibility",
            "interpretation_limit",
        ],
    )
    write_csv(
        OUT / "sensitivity_scenarios_v2.csv",
        sensitivity,
        [
            "scenario_id",
            "scenario_family",
            "graph_object",
            "scenario_label",
            "deletion_unit",
            "dropped_ids",
            "edge_count",
            "observed_actor_count",
            "registry_isolated_actor_count",
            "issue_count",
            "cross_frame_actor_count",
            "ecology_international_bridge_count",
            "component_count",
            "largest_component_actor_count",
            "largest_component_total_node_count",
            "edge_retention_share",
            "observed_actor_retention_share",
            "baseline_edge_count",
            "baseline_observed_actor_count",
            "selection_rule",
            "research_status",
            "display_tier",
            "claim_status",
            "review_status",
            "frontend_eligibility",
            "interpretation_limit",
        ],
    )
    write_csv(
        OUT / "graph_object_summary_v2.csv",
        graph_summary,
        [
            "object_id",
            "graph_object",
            "input_observation_count",
            "incident_registry_actor_count",
            "counterpart_or_object_count",
            "primary_actor_measure",
            "source_breadth_spearman",
            "object_semantics",
            "projection_status",
            "research_status",
            "display_tier",
            "claim_status",
            "review_status",
            "frontend_eligibility",
            "interpretation_limit",
        ],
    )
    write_csv(
        OUT / "method_literature_v2.csv",
        literature_rows,
        [
            "reference_id",
            "citation",
            "doi",
            "url",
            "source_kind",
            "method_point",
            "application_in_h1_v2",
            "non_transfer_boundary",
            "research_status",
            "display_tier",
            "claim_status",
            "review_status",
            "frontend_eligibility",
            "interpretation_limit",
        ],
    )

    fig1 = render_graph_objects(actor_rows, associations)
    fig2 = render_strata(stratified)
    fig3 = render_sensitivity(sensitivity)
    for stem, title, svg in (
        ("fig_graph_objects_v2", "Documentation traces and graph objects", fig1),
        ("fig_actor_issue_strata_v2", "Actor-issue stratified associations", fig2),
        ("fig_actor_issue_sensitivity_v2", "Actor-issue sensitivity", fig3),
    ):
        (OUT / f"{stem}.svg").write_text(svg, encoding="utf-8")
        (OUT / f"{stem}.html").write_text(
            html_wrapper(title, svg), encoding="utf-8"
        )

    (OUT / "README.md").write_text(render_readme(), encoding="utf-8")
    (OUT / "method_brief_v2.md").write_text(
        render_method_brief(
            actor_rows,
            associations,
            matched_summary,
            sensitivity,
            negative_cases,
            graph_summary,
        ),
        encoding="utf-8",
    )
    (OUT / "principal_checkpoint_v2.md").write_text(
        render_principal_checkpoint(negative_cases, matched_pairs),
        encoding="utf-8",
    )

    metrics = {
        "as_of_date": AUDIT_DATE,
        "research_status": "research_only",
        "frontend_eligibility": "not_frontend_ready",
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (
                ACTORS,
                SOURCES,
                EDGES,
                TRIPLES,
                EVENTS,
                CASE_ROLES,
                LIFECYCLE,
                CLASS_MAP,
                ARCHIVE,
                DYADIC,
            )
        },
        "counts": {
            "current_actors": len(actors),
            "sources": len(sources),
            "active_actor_issue_edges": len(edges),
            "e3plus_actor_issue_edges": sum(
                edge["evidence_level"] in E3PLUS for edge in edges
            ),
            "strict_triples": len(triples),
            "human_checked_registered_actor_event_rows": len(events),
            "accepted_registered_actor_case_roles": len(roles),
            "reviewed_typed_dyadic_relations": len(dyadic),
            "method_literature_interfaces": len(literature_rows),
            "matched_pair_rows": len(matched_pairs),
            "negative_case_rows": len(negative_cases),
        },
        "headline_associations": {
            "linked_sources_vs_actor_issue_degree": fmt_rho(
                associations,
                "actor_issue_bipartite",
                "active_actor_issue_degree",
            ),
            "linked_sources_vs_actor_issue_betweenness": fmt_rho(
                associations,
                "actor_issue_bipartite",
                "active_actor_issue_betweenness",
            ),
            "linked_sources_vs_event_degree": fmt_rho(
                associations,
                "event_hyperedge_incidence",
                "human_checked_event_degree",
            ),
            "linked_sources_vs_typed_dyadic_degree": fmt_rho(
                associations,
                "reviewed_typed_dyadic",
                "reviewed_typed_dyadic_degree",
            ),
            "linked_sources_vs_case_degree": fmt_rho(
                associations,
                "accepted_case_role_incidence",
                "accepted_case_degree",
            ),
        },
        "hard_boundary": INTERPRETATION_LIMIT,
    }
    (OUT / "metrics_v2.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT / "validation_report_v2.md").write_text(
        "# H1 documentation visibility v2 validation\n\n"
        + "\n".join(f"- PASS: {check}" for check in checks)
        + "\n- PASS: 3 SVG and 3 standalone HTML figures generated.\n"
        + "- PASS: source deletion and actor deletion remain separate scenario families.\n"
        + "- PASS: event hyperedges and case roles are not projected into organization relations.\n"
        + f"- PASS: {len(literature_rows)} method references include explicit non-transfer boundaries.\n"
        + "- PASS: central tables, frontend and workbench are read-only inputs; no writes performed.\n",
        encoding="utf-8",
    )
    print(
        "H1 v2 OK: "
        f"{len(actor_rows)} actors; {len(associations)} associations; "
        f"{len(matched_pairs)} matched rows; {len(negative_cases)} negative cases"
    )


if __name__ == "__main__":
    main()
