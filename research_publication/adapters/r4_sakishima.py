from __future__ import annotations

"""Build the bounded R4 Sakishima framing exhibit.

This adapter reads only the post-HR-016 formal observation and safe-excerpt
tables.  It does not infer actors from speakers, aggregate anonymous comments
into a resident actor, or turn document frequency into a claim about local
attitudes.
"""

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


CATALOG_ID = "PUB-MR-004"
SCHEMA_VERSION = "r4_sakishima_exhibit_v1"
FORMAL_FACT_PATH = Path("data/interim/19_sakishima_frame_corpus_v0.csv")
SAFE_EXCERPT_PATH = Path(
    "outputs/R04_sakishima_frame_corpus_v0/"
    "online_evidence_safe_sources_v0.csv"
)

EXPECTED_FORMAL_OBSERVATIONS = 19
EXPECTED_SAFE_EXCERPTS = 24
EXPECTED_BOUNDED_SUBJECT_DISPLAY_UNITS = 14
EXPECTED_UNIQUE_ENTITY_IDS = 13

COMPARISON_PLACES = ("Miyako", "Ishigaki", "Yonaguni")
REGIONAL_CONTEXT_PLACES = ("Sakishima",)
PLACE_ORDER = COMPARISON_PLACES + REGIONAL_CONTEXT_PLACES

PLACE_DISPLAY = {
    "Miyako": {
        "display_label_zh": "宫古",
        "display_label_ja": "宮古",
        "display_label_en": "Miyako",
    },
    "Ishigaki": {
        "display_label_zh": "石垣",
        "display_label_ja": "石垣",
        "display_label_en": "Ishigaki",
    },
    "Yonaguni": {
        "display_label_zh": "与那国",
        "display_label_ja": "与那国",
        "display_label_en": "Yonaguni",
    },
    "Sakishima": {
        "display_label_zh": "先岛",
        "display_label_ja": "先島",
        "display_label_en": "Sakishima",
    },
}

FRAME_DISPLAY = {
    "groundwater_life_safety": {
        "display_label_zh": "地下水／饮用水",
        "display_label_ja": "地下水／飲料水",
        "display_label_en": "Groundwater / drinking water",
    },
    "local_autonomy_referendum": {
        "display_label_zh": "地方自治／公投",
        "display_label_ja": "地方自治／住民投票",
        "display_label_en": "Local autonomy / referendum",
    },
    "frontline_taiwan_evacuation": {
        "display_label_zh": "前线化／台湾邻近／撤离",
        "display_label_ja": "前線化／台湾近接／避難",
        "display_label_en": "Frontline / Taiwan proximity / evacuation",
    },
    "life_safety": {
        "display_label_zh": "生活安全",
        "display_label_ja": "生活安全",
        "display_label_en": "Life safety",
    },
    "environment_deployment": {
        "display_label_zh": "环境—部署连接",
        "display_label_ja": "環境―配備の接続",
        "display_label_en": "Environment–deployment link",
    },
    "procedural_fairness": {
        "display_label_zh": "程序进入／说明",
        "display_label_ja": "手続参加／説明",
        "display_label_en": "Procedural entry / explanation",
    },
    "environment_background_not_deployment": {
        "display_label_zh": "一般环境背景（非部署主张）",
        "display_label_ja": "一般環境背景（配備主張ではない）",
        "display_label_en": (
            "General environmental context (not a deployment claim)"
        ),
    },
}

ALLOWED_FACT_SCOPES = {
    "human_reviewed_frame_observation",
    "online_frame_observation",
}
ALLOWED_FACT_REVIEW_STATUSES = {
    "ai_seeded",
    "human_checked",
    "human_revised",
}
ALLOWED_ENTITY_STATUSES = {
    "existing_actor",
    "external_institution",
    "named_individual_non_registry",
    "non_actor_event_evidence",
    "provisional_event_committee",
}
ALLOWED_SOURCE_REVIEW_STATUSES = {
    "human_checked",
    "human_revised",
    "qa_safe_online_source",
}
ALLOWED_SOURCE_DISPOSITIONS = {
    "human_checked",
    "human_revised",
    "safe_merge",
    "safe_with_correction",
}
HUMAN_REVIEW_STATUSES = {"human_checked", "human_revised"}

ENTITY_KIND = {
    "existing_actor": "registry_actor",
    "external_institution": "institution",
    "named_individual_non_registry": "named_person",
    "non_actor_event_evidence": "anonymous_event_utterance",
    "provisional_event_committee": "provisional_event_collective",
}

FACT_REQUIRED_FIELDS = {
    "fact_id",
    "fact_scope",
    "place",
    "entity_id_or_provisional",
    "entity_name",
    "entity_status",
    "event_or_document",
    "event_year",
    "frame_code",
    "frame_label",
    "relation_basis",
    "source_ref",
    "existing_source_ids",
    "source_urls",
    "source_locator_summary",
    "evidence_level",
    "review_status",
    "human_review_required",
    "interpretation_limit",
    "relationship_limit",
}

EXCERPT_REQUIRED_FIELDS = {
    "corpus_source_id",
    "existing_source_id",
    "place",
    "title",
    "url",
    "source_type",
    "speaker_or_owner",
    "date_or_period",
    "locator",
    "excerpt_short",
    "paraphrase_zh",
    "frame_candidates",
    "evidence_level",
    "coding_status",
    "qa_disposition",
    "review_status",
    "interpretation_limit",
}

ANALYSIS_UNIT = (
    "A formal frame observation with an explicit entity or speaker layer, "
    "place, frame, and source locator; safe source excerpts form a separate "
    "visibility denominator."
)
SELECTION_BOUNDARY = (
    "All 19 post-HR-016 formal frame observations and all 24 QA-safe online "
    "source excerpts in the current R4 tables. Miyako, Ishigaki, and Yonaguni "
    "are comparison places; the Sakishima-wide row remains regional context."
)
INTERPRETATION_LIMIT = (
    "Counts describe visibility in this bounded online corpus. They are not "
    "organization counts, resident attitudes, prevalence, mobilization "
    "intensity, or evidence of political agreement. Administrative responses, "
    "named individuals, provisional committees, and anonymous event utterances "
    "remain distinct from registry actors."
)
EXHIBIT_DISPLAY = {
    "title": {
        "zh": "先岛三地：公开材料中的问题框架",
        "ja": "先島三地域：公開資料に現れる問題フレーム",
        "en": "Three Sakishima localities: frames visible in public records",
    },
    "subtitle": {
        "zh": "在宫古、石垣、与那国之间切换，并下钻到逐条观察、原始摘录与定位信息。",
        "ja": "宮古・石垣・与那国を切り替え、観察行、原文抜粋、所在情報まで確認できます。",
        "en": (
            "Switch between Miyako, Ishigaki, and Yonaguni, then inspect "
            "each observation, excerpt, and source locator."
        ),
    },
    "interpretation_limit": {
        "zh": (
            "19条正式观察中，18条进入宫古／石垣／与那国三地比较，另1条"
            "先岛整体观察只作区域语境，单岛比较采用18条对应材料。计数呈现限定"
            "线上语料中各框架的可见度；组织数量、居民态度、现实普遍程度、动员强度与政治共识"
            "分别需要名录、调查和事件数据衡量。行政答复、具名个人、临时委员会"
            "和匿名事件话语采用独立类别呈现。"
        ),
        "ja": (
            "正式観察19件のうち18件を宮古・石垣・与那国の比較に用い、"
            "先島全域の1件は地域文脈としてのみ扱い、各島の分母には加えません。"
            "件数は限定オンライン資料での可視性であり、団体数、住民意識、"
            "現実の普及度、動員強度、政治的合意を示しません。行政回答、実名個人、"
            "暫定委員会、匿名のイベント発話は登録団体と区別します。"
        ),
        "en": (
            "Of 19 formal observations, 18 enter the Miyako/Ishigaki/Yonaguni "
            "comparison and one Sakishima-wide observation remains regional "
            "context outside every island denominator. "
            + INTERPRETATION_LIMIT
        ),
    },
}


class R4SakishimaAdapterError(ValueError):
    """Raised when the formal R4 input no longer satisfies its publication gate."""


def _read_csv(path: Path, required_fields: set[str]) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fields = set(reader.fieldnames or [])
            missing = sorted(required_fields - fields)
            if missing:
                raise R4SakishimaAdapterError(
                    f"{path} is missing required fields: {missing}"
                )
            return [
                {key: (value or "").strip() for key, value in row.items()}
                for row in reader
            ]
    except FileNotFoundError as exc:
        raise R4SakishimaAdapterError(f"Required R4 table is missing: {path}") from exc


def _tokens(value: str) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for token in value.split(";"):
        token = token.strip()
        if token and token not in seen:
            seen.add(token)
            result.append(token)
    return result


def _require_unique(rows: Iterable[dict[str, str]], field: str, label: str) -> None:
    values = [row[field] for row in rows]
    blank_count = sum(not value for value in values)
    duplicates = sorted(
        value for value, count in Counter(values).items() if value and count > 1
    )
    if blank_count or duplicates:
        raise R4SakishimaAdapterError(
            f"{label} requires unique non-blank {field}; "
            f"blank={blank_count}, duplicates={duplicates}"
        )


def _validate_rows(
    facts: list[dict[str, str]],
    excerpts: list[dict[str, str]],
) -> None:
    if len(facts) != EXPECTED_FORMAL_OBSERVATIONS:
        raise R4SakishimaAdapterError(
            "R4 formal observation denominator changed: "
            f"expected {EXPECTED_FORMAL_OBSERVATIONS}, found {len(facts)}"
        )
    if len(excerpts) != EXPECTED_SAFE_EXCERPTS:
        raise R4SakishimaAdapterError(
            "R4 safe excerpt denominator changed: "
            f"expected {EXPECTED_SAFE_EXCERPTS}, found {len(excerpts)}"
        )
    _require_unique(facts, "fact_id", "R4 formal facts")
    _require_unique(excerpts, "corpus_source_id", "R4 safe excerpts")

    excerpt_ids = {row["corpus_source_id"] for row in excerpts}
    for row in facts:
        fact_id = row["fact_id"]
        if row["fact_scope"] not in ALLOWED_FACT_SCOPES:
            raise R4SakishimaAdapterError(
                f"{fact_id} has an ineligible fact_scope: {row['fact_scope']}"
            )
        if row["review_status"] not in ALLOWED_FACT_REVIEW_STATUSES:
            raise R4SakishimaAdapterError(
                f"{fact_id} has an ineligible review_status: {row['review_status']}"
            )
        if row["human_review_required"].lower() != "no":
            raise R4SakishimaAdapterError(
                f"{fact_id} still requires human review"
            )
        if row["entity_status"] not in ALLOWED_ENTITY_STATUSES:
            raise R4SakishimaAdapterError(
                f"{fact_id} has an unknown entity_status: {row['entity_status']}"
            )
        if row["place"] not in PLACE_ORDER:
            raise R4SakishimaAdapterError(
                f"{fact_id} has an out-of-bound place: {row['place']}"
            )
        if not row["frame_code"] or not row["frame_label"]:
            raise R4SakishimaAdapterError(f"{fact_id} has a blank frame")
        if row["frame_label"] not in FRAME_DISPLAY:
            raise R4SakishimaAdapterError(
                f"{fact_id} has an unregistered frame display key: "
                f"{row['frame_label']}"
            )
        if not row["source_locator_summary"]:
            raise R4SakishimaAdapterError(f"{fact_id} has no source locator")

        entity_id = row["entity_id_or_provisional"]
        if row["entity_status"] == "existing_actor":
            if not re.fullmatch(r"A\d{3}", entity_id):
                raise R4SakishimaAdapterError(
                    f"{fact_id} marks a non-registry id as existing_actor: {entity_id}"
                )
        elif re.fullmatch(r"A\d{3}", entity_id):
            raise R4SakishimaAdapterError(
                f"{fact_id} hides registry actor id {entity_id} behind "
                f"entity_status={row['entity_status']}"
            )

        source_ids = _tokens(row["source_ref"])
        if not source_ids:
            raise R4SakishimaAdapterError(f"{fact_id} has no corpus source reference")
        missing_sources = sorted(set(source_ids) - excerpt_ids)
        if missing_sources:
            raise R4SakishimaAdapterError(
                f"{fact_id} references sources outside the safe excerpt table: "
                f"{missing_sources}"
            )

    for row in excerpts:
        source_id = row["corpus_source_id"]
        if row["review_status"] not in ALLOWED_SOURCE_REVIEW_STATUSES:
            raise R4SakishimaAdapterError(
                f"{source_id} has an ineligible review_status: "
                f"{row['review_status']}"
            )
        if row["qa_disposition"] not in ALLOWED_SOURCE_DISPOSITIONS:
            raise R4SakishimaAdapterError(
                f"{source_id} has an ineligible qa_disposition: "
                f"{row['qa_disposition']}"
            )
        if row["place"] not in PLACE_ORDER:
            raise R4SakishimaAdapterError(
                f"{source_id} has an out-of-bound place: {row['place']}"
            )
        for field in ("url", "locator", "speaker_or_owner", "interpretation_limit"):
            if not row[field]:
                raise R4SakishimaAdapterError(
                    f"{source_id} has a blank required evidence field: {field}"
                )
        unknown_frames = sorted(
            set(_tokens(row["frame_candidates"])) - set(FRAME_DISPLAY)
        )
        if unknown_frames:
            raise R4SakishimaAdapterError(
                f"{source_id} has unregistered frame display keys: "
                f"{unknown_frames}"
            )

    unique_entity_ids = {
        row["entity_id_or_provisional"]
        for row in facts
        if row["entity_id_or_provisional"]
    }
    bounded_subject_display_units = {
        (row["entity_id_or_provisional"], row["entity_name"])
        for row in facts
        if row["entity_id_or_provisional"]
    }
    if len(unique_entity_ids) != EXPECTED_UNIQUE_ENTITY_IDS:
        raise R4SakishimaAdapterError(
            "R4 unique entity-id denominator changed: "
            f"expected {EXPECTED_UNIQUE_ENTITY_IDS}, found {len(unique_entity_ids)}"
        )
    if (
        len(bounded_subject_display_units)
        != EXPECTED_BOUNDED_SUBJECT_DISPLAY_UNITS
    ):
        raise R4SakishimaAdapterError(
            "R4 bounded subject display-unit denominator changed: "
            f"expected {EXPECTED_BOUNDED_SUBJECT_DISPLAY_UNITS}, "
            f"found {len(bounded_subject_display_units)}"
        )


def _source_record(row: dict[str, str]) -> dict[str, Any]:
    return {
        "corpus_source_id": row["corpus_source_id"],
        "existing_source_ids": _tokens(row["existing_source_id"]),
        "place": row["place"],
        "title": row["title"],
        "url": row["url"],
        "source_type": row["source_type"],
        "speaker_or_owner": row["speaker_or_owner"],
        "date_or_period": row["date_or_period"],
        "locator": row["locator"],
        "excerpt_short": row["excerpt_short"],
        "paraphrase_zh": row["paraphrase_zh"],
        "frame_labels": _tokens(row["frame_candidates"]),
        "evidence_level": row["evidence_level"],
        "coding_status": row["coding_status"],
        "qa_disposition": row["qa_disposition"],
        "review_status": row["review_status"],
        "display_tier": (
            "reviewed"
            if row["review_status"] in HUMAN_REVIEW_STATUSES
            else "research"
        ),
        "interpretation_limit": row["interpretation_limit"],
    }


def _observation_record(
    row: dict[str, str],
    excerpts_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    source_ref_ids = _tokens(row["source_ref"])
    entity_status = row["entity_status"]
    entity_id = row["entity_id_or_provisional"]
    return {
        "observation_id": row["fact_id"],
        "display_tier": (
            "reviewed"
            if row["review_status"] in HUMAN_REVIEW_STATUSES
            else "research"
        ),
        "fact_scope": row["fact_scope"],
        "place": row["place"],
        "subject": {
            "entity_id": entity_id,
            "entity_name": row["entity_name"],
            "entity_kind": ENTITY_KIND[entity_status],
            "source_entity_status": entity_status,
            "actor_id": entity_id if entity_status == "existing_actor" else None,
        },
        "event_or_document": row["event_or_document"],
        "event_year": row["event_year"],
        "frame": {
            "code": row["frame_code"],
            "label": row["frame_label"],
        },
        "relation_basis": row["relation_basis"],
        "evidence": {
            "evidence_level": row["evidence_level"],
            "review_status": row["review_status"],
            "human_review_required": False,
            "source_ref_ids": source_ref_ids,
            "existing_source_ids": _tokens(row["existing_source_ids"]),
            "source_urls": _tokens(row["source_urls"]),
            "source_locator_summary": row["source_locator_summary"],
            "source_records": [excerpts_by_id[source_id] for source_id in source_ref_ids],
        },
        "interpretation_limit": row["interpretation_limit"],
        "relationship_limit": row["relationship_limit"],
    }


def _count_rows_by_key(
    rows: Iterable[dict[str, Any]],
    key: str,
) -> dict[str, int]:
    return dict(sorted(Counter(str(row[key]) for row in rows).items()))


def _place_aggregate(
    place: str,
    observations: list[dict[str, Any]],
    excerpts: list[dict[str, Any]],
) -> dict[str, Any]:
    place_observations = [
        row for row in observations if row["place"] == place
    ]
    place_excerpts = [row for row in excerpts if row["place"] == place]

    observation_frames: dict[str, list[str]] = defaultdict(list)
    for row in place_observations:
        observation_frames[row["frame"]["label"]].append(row["observation_id"])

    excerpt_frames: dict[str, list[str]] = defaultdict(list)
    for row in place_excerpts:
        for frame_label in row["frame_labels"]:
            excerpt_frames[frame_label].append(row["corpus_source_id"])

    return {
        "place": place,
        "place_scope": "comparison_place"
        if place in COMPARISON_PLACES
        else "regional_context",
        "formal_observation_denominator": len(place_observations),
        "safe_excerpt_denominator": len(place_excerpts),
        "unique_bounded_entity_count": len(
            {row["subject"]["entity_id"] for row in place_observations}
        ),
        "bounded_subject_display_unit_count": len(
            {
                (
                    row["subject"]["entity_id"],
                    row["subject"]["entity_name"],
                )
                for row in place_observations
            }
        ),
        "registry_actor_observation_count": sum(
            row["subject"]["actor_id"] is not None
            for row in place_observations
        ),
        "entity_kind_counts": _count_rows_by_key(
            (row["subject"] for row in place_observations),
            "entity_kind",
        ),
        "observation_frame_visibility": [
            {
                "frame_label": frame_label,
                "observation_count": len(observation_ids),
                "observation_ids": sorted(observation_ids),
            }
            for frame_label, observation_ids in sorted(observation_frames.items())
        ],
        "excerpt_frame_visibility": [
            {
                "frame_label": frame_label,
                "safe_excerpt_count": len(source_ids),
                "corpus_source_ids": sorted(source_ids),
            }
            for frame_label, source_ids in sorted(excerpt_frames.items())
        ],
        "measurement_scope": (
            "Counts are bounded formal observations and QA-safe online excerpts "
            "in this exhibit; not local prevalence or resident attitudes."
        ),
    }


def build_r4_sakishima_exhibit(project_root: Path) -> dict[str, Any]:
    """Return a deterministic, read-only PUB-MR-004 exhibit payload."""

    project_root = Path(project_root).resolve()
    facts = _read_csv(project_root / FORMAL_FACT_PATH, FACT_REQUIRED_FIELDS)
    raw_excerpts = _read_csv(
        project_root / SAFE_EXCERPT_PATH,
        EXCERPT_REQUIRED_FIELDS,
    )
    _validate_rows(facts, raw_excerpts)

    excerpts = [
        _source_record(row)
        for row in sorted(raw_excerpts, key=lambda row: row["corpus_source_id"])
    ]
    excerpts_by_id = {row["corpus_source_id"]: row for row in excerpts}
    observations = [
        _observation_record(row, excerpts_by_id)
        for row in sorted(facts, key=lambda row: row["fact_id"])
    ]

    entity_status_counts = _count_rows_by_key(facts, "entity_status")
    fact_review_counts = _count_rows_by_key(facts, "review_status")
    excerpt_review_counts = _count_rows_by_key(raw_excerpts, "review_status")
    unique_entity_ids = sorted(
        {row["entity_id_or_provisional"] for row in facts}
    )
    bounded_subject_display_units = sorted(
        {
            (row["entity_id_or_provisional"], row["entity_name"])
            for row in facts
        }
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "catalog_id": CATALOG_ID,
        "exhibit_id": "r4_sakishima_frame_corpus_v1",
        "method_status": "method_ready_bounded",
        "claim_status": "descriptive_ready",
        "display": EXHIBIT_DISPLAY,
        "analysis_unit": ANALYSIS_UNIT,
        "selection_boundary": SELECTION_BOUNDARY,
        "interpretation_limit": INTERPRETATION_LIMIT,
        "comparison_places": list(COMPARISON_PLACES),
        "regional_context_places": list(REGIONAL_CONTEXT_PLACES),
        "place_vocabulary": [
            {
                "id": place,
                "place_scope": "comparison_place"
                if place in COMPARISON_PLACES
                else "regional_context",
                **PLACE_DISPLAY[place],
            }
            for place in PLACE_ORDER
        ],
        "frame_vocabulary": [
            {"id": frame_label, **FRAME_DISPLAY[frame_label]}
            for frame_label in sorted(FRAME_DISPLAY)
        ],
        "declared_denominators": {
            "formal_frame_observations": EXPECTED_FORMAL_OBSERVATIONS,
            "safe_source_excerpts": EXPECTED_SAFE_EXCERPTS,
            "bounded_subject_display_units": (
                EXPECTED_BOUNDED_SUBJECT_DISPLAY_UNITS
            ),
            "unique_entity_identifiers": EXPECTED_UNIQUE_ENTITY_IDS,
            "registry_actor_observations": entity_status_counts.get(
                "existing_actor", 0
            ),
            "non_registry_or_institution_observations": (
                EXPECTED_FORMAL_OBSERVATIONS
                - entity_status_counts.get("existing_actor", 0)
            ),
            "reviewed_formal_frame_observations": sum(
                row["display_tier"] == "reviewed" for row in observations
            ),
            "reviewed_safe_source_excerpts": sum(
                row["display_tier"] == "reviewed" for row in excerpts
            ),
            "research_layer_formal_frame_observations": sum(
                row["display_tier"] == "research" for row in observations
            ),
            "research_layer_safe_source_excerpts": sum(
                row["display_tier"] == "research" for row in excerpts
            ),
        },
        "review_gate": {
            "hr_batch": "HR-016",
            "open_fact_or_locator_items": 0,
            "formal_fact_review_status_counts": fact_review_counts,
            "safe_excerpt_review_status_counts": excerpt_review_counts,
            "formal_entity_status_counts": entity_status_counts,
            "note": (
                "Module-level semantic and locator decisions are closed. "
                "Raw ai_seeded row status is preserved where the row entered "
                "through the QA-safe online gate."
            ),
        },
        "place_aggregates": [
            _place_aggregate(place, observations, excerpts)
            for place in PLACE_ORDER
        ],
        "observations": observations,
        "excerpts": excerpts,
        "provenance": {
            "formal_observation_table": FORMAL_FACT_PATH.as_posix(),
            "safe_excerpt_table": SAFE_EXCERPT_PATH.as_posix(),
            "formal_fact_ids": [row["observation_id"] for row in observations],
            "safe_excerpt_ids": [row["corpus_source_id"] for row in excerpts],
            "bounded_entity_ids": unique_entity_ids,
            "bounded_subject_display_units": [
                {
                    "entity_id": entity_id,
                    "entity_name": entity_name,
                }
                for entity_id, entity_name in bounded_subject_display_units
            ],
        },
    }
