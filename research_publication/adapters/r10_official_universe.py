from __future__ import annotations

"""Publication adapter for the FY2024 Okinawa official collaboration universe.

This adapter deliberately publishes a *source-row universe*, not an actor or
funding network.  It reads and cross-validates the authoritative 616-row S002
table and its official aggregation tables, then emits only bounded summaries
and compact source-row/page references.
"""

import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


PACKAGE = Path("outputs/R10_official_collaboration_universe_v1")
UNIVERSE_FILE = "official_collaboration_source_universe_v1.csv"
RESOURCE_FILE = "official_resource_type_summary_v1.csv"
DEPARTMENT_FILE = "department_resource_summary_v1.csv"
FUNCTION_MATRIX_FILE = "issue_mechanism_matrix_v1.csv"
DEPARTMENT_MATRIX_FILE = "department_mechanism_matrix_v1.csv"
STATISTICS_FILE = "descriptive_statistics_v1.csv"
EXPECTED_SOURCE_ROWS = 616


class R10OfficialUniverseError(ValueError):
    """Raised when the formal R10 source-universe package is inconsistent."""


def _read_csv(path: Path) -> list[dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    except FileNotFoundError as exc:
        raise R10OfficialUniverseError(f"Missing formal R10 input: {path}") from exc


def _required_columns(
    rows: list[dict[str, str]],
    columns: set[str],
    *,
    table: str,
) -> None:
    if not rows:
        raise R10OfficialUniverseError(f"{table} is empty")
    missing = sorted(columns - set(rows[0]))
    if missing:
        raise R10OfficialUniverseError(f"{table} is missing columns: {missing}")


def _as_int(value: str, *, field: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise R10OfficialUniverseError(
            f"Expected integer in {field}, received {value!r}"
        ) from exc


def _as_float(value: str, *, field: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise R10OfficialUniverseError(
            f"Expected number in {field}, received {value!r}"
        ) from exc


def _parse_row_numbers(value: str) -> list[int]:
    if not value.strip():
        return []
    return [_as_int(item, field="source_row_numbers") for item in value.split(";")]


def _compress_numbers(values: Iterable[int]) -> str:
    """Return a deterministic compact range expression such as ``1-3;7;9-11``."""

    ordered = sorted(set(values))
    if not ordered:
        return ""
    groups: list[str] = []
    start = previous = ordered[0]
    for value in ordered[1:]:
        if value == previous + 1:
            previous = value
            continue
        groups.append(str(start) if start == previous else f"{start}-{previous}")
        start = previous = value
    groups.append(str(start) if start == previous else f"{start}-{previous}")
    return ";".join(groups)


def _share(count: int) -> float:
    return round(count * 100 / EXPECTED_SOURCE_ROWS, 1)


def _validate_universe(rows: list[dict[str, str]]) -> dict[str, Any]:
    _required_columns(
        rows,
        {
            "source_row_uid",
            "source_id",
            "source_title",
            "fiscal_year",
            "source_row_number",
            "pdf_page",
            "department_display_machine",
            "official_mechanism_code",
            "official_mechanism_label",
            "official_mechanism_definition",
            "mechanism_analytical_family",
            "official_issue_field_code",
            "official_issue_field_label",
        },
        table=UNIVERSE_FILE,
    )
    if len(rows) != EXPECTED_SOURCE_ROWS:
        raise R10OfficialUniverseError(
            f"R10 source universe must contain exactly {EXPECTED_SOURCE_ROWS} rows; "
            f"found {len(rows)}"
        )

    row_numbers = [_as_int(row["source_row_number"], field="source_row_number") for row in rows]
    if row_numbers != list(range(1, EXPECTED_SOURCE_ROWS + 1)):
        raise R10OfficialUniverseError(
            "R10 source_row_number must be sequential 1-616 in source order"
        )
    expected_uids = [f"S002-R{number:04d}" for number in row_numbers]
    actual_uids = [row["source_row_uid"] for row in rows]
    if actual_uids != expected_uids or len(set(actual_uids)) != EXPECTED_SOURCE_ROWS:
        raise R10OfficialUniverseError(
            "R10 source_row_uid must be unique and match S002-R0001 through S002-R0616"
        )
    if {row["source_id"] for row in rows} != {"S002"}:
        raise R10OfficialUniverseError("R10 source universe must contain only S002")
    if {row["fiscal_year"] for row in rows} != {"2024"}:
        raise R10OfficialUniverseError("R10 source universe must contain only FY2024")

    pages = [_as_int(row["pdf_page"], field="pdf_page") for row in rows]
    if set(pages) != set(range(1, 87)):
        raise R10OfficialUniverseError(
            "R10 source universe must preserve references to every PDF page 1-86"
        )
    for field in (
        "department_display_machine",
        "official_mechanism_code",
        "official_mechanism_label",
        "official_issue_field_code",
        "official_issue_field_label",
    ):
        if any(not row[field].strip() for row in rows):
            raise R10OfficialUniverseError(
                f"R10 source universe has blank required values in {field}"
            )

    return {
        "row_numbers": row_numbers,
        "page_by_row": {
            number: page for number, page in zip(row_numbers, pages, strict=True)
        },
        "department_counts": Counter(
            row["department_display_machine"] for row in rows
        ),
        "function_counts": Counter(row["official_issue_field_code"] for row in rows),
        "mechanism_counts": Counter(row["official_mechanism_code"] for row in rows),
    }


def _validate_resource_summary(
    rows: list[dict[str, str]],
    mechanism_counts: Counter[str],
) -> list[dict[str, Any]]:
    _required_columns(
        rows,
        {
            "official_mechanism_code",
            "official_mechanism_label",
            "official_mechanism_definition",
            "mechanism_analytical_family",
            "source_row_count",
            "share_of_616_percent",
            "department_count",
            "issue_field_count",
            "cash_transfer_inference_allowed_from_s002_alone",
            "interpretation_limit",
        },
        table=RESOURCE_FILE,
    )
    codes = [row["official_mechanism_code"] for row in rows]
    if codes != [str(value) for value in range(1, 11)]:
        raise R10OfficialUniverseError(
            "Official resource summary must contain mechanism codes 1-10 in order"
        )

    result: list[dict[str, Any]] = []
    for row in rows:
        code = row["official_mechanism_code"]
        count = _as_int(row["source_row_count"], field="resource source_row_count")
        if count != mechanism_counts[code]:
            raise R10OfficialUniverseError(
                f"Resource mechanism {code} count disagrees with the 616-row universe"
            )
        reported_share = _as_float(
            row["share_of_616_percent"], field="resource share_of_616_percent"
        )
        if reported_share != _share(count):
            raise R10OfficialUniverseError(
                f"Resource mechanism {code} share disagrees with its row count"
            )
        if row["cash_transfer_inference_allowed_from_s002_alone"].lower() != "no":
            raise R10OfficialUniverseError(
                f"Resource mechanism {code} must prohibit cash-transfer inference"
            )
        result.append(
            {
                "code": code,
                "label": row["official_mechanism_label"],
                "definition": row["official_mechanism_definition"],
                "analytical_family": row["mechanism_analytical_family"],
                "source_row_count": count,
                "share_of_denominator_percent": reported_share,
                "department_count": _as_int(
                    row["department_count"], field="resource department_count"
                ),
                "function_count": _as_int(
                    row["issue_field_count"], field="resource issue_field_count"
                ),
                "cash_transfer_inference_allowed": False,
                "interpretation_limit": row["interpretation_limit"],
            }
        )
    if sum(item["source_row_count"] for item in result) != EXPECTED_SOURCE_ROWS:
        raise R10OfficialUniverseError(
            "Official resource-type summary does not sum to 616"
        )
    return result


def _validate_department_summary(
    rows: list[dict[str, str]],
    department_counts: Counter[str],
) -> list[dict[str, Any]]:
    _required_columns(
        rows,
        {
            "department_display_machine",
            "source_row_count",
            "share_of_616_percent",
            "office_count",
            "mechanism_count",
            "issue_field_count",
            "interpretation_limit",
        },
        table=DEPARTMENT_FILE,
    )
    labels = [row["department_display_machine"] for row in rows]
    if len(rows) != 15 or len(set(labels)) != 15 or set(labels) != set(department_counts):
        raise R10OfficialUniverseError(
            "Department summary must cover the 15 source-universe departments exactly"
        )

    result: list[dict[str, Any]] = []
    for row in rows:
        label = row["department_display_machine"]
        count = _as_int(row["source_row_count"], field="department source_row_count")
        if count != department_counts[label]:
            raise R10OfficialUniverseError(
                f"Department {label} count disagrees with the 616-row universe"
            )
        reported_share = _as_float(
            row["share_of_616_percent"], field="department share_of_616_percent"
        )
        if reported_share != _share(count):
            raise R10OfficialUniverseError(
                f"Department {label} share disagrees with its row count"
            )
        result.append(
            {
                "label": label,
                "source_row_count": count,
                "share_of_denominator_percent": reported_share,
                "office_source_label_count": _as_int(
                    row["office_count"], field="department office_count"
                ),
                "resource_type_count": _as_int(
                    row["mechanism_count"], field="department mechanism_count"
                ),
                "function_count": _as_int(
                    row["issue_field_count"], field="department issue_field_count"
                ),
                "interpretation_limit": row["interpretation_limit"],
            }
        )
    if sum(item["source_row_count"] for item in result) != EXPECTED_SOURCE_ROWS:
        raise R10OfficialUniverseError("Department summary does not sum to 616")
    return result


def _validate_matrix(
    rows: list[dict[str, str]],
    *,
    table: str,
    dimension_field: str,
    expected_dimension_values: set[str],
    expected_dimension_type: str,
    universe_rows: list[dict[str, str]],
    universe_dimension_field: str,
    page_by_row: dict[int, int],
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    _required_columns(
        rows,
        {
            "dimension_type",
            dimension_field,
            "dimension_label",
            "official_mechanism_code",
            "official_mechanism_label",
            "source_row_count",
            "source_row_numbers",
            "fact_layer",
            "human_gate",
            "interpretation_limit",
        },
        table=table,
    )
    mechanism_codes = {str(value) for value in range(1, 11)}
    keys = {
        (row[dimension_field], row["official_mechanism_code"]) for row in rows
    }
    expected_keys = {
        (dimension, mechanism)
        for dimension in expected_dimension_values
        for mechanism in mechanism_codes
    }
    if keys != expected_keys or len(rows) != len(expected_keys):
        raise R10OfficialUniverseError(
            f"{table} must be a complete "
            f"{len(expected_dimension_values)}x10 matrix"
        )
    if {row["dimension_type"] for row in rows} != {expected_dimension_type}:
        raise R10OfficialUniverseError(f"{table} has an unexpected dimension_type")

    expected_refs: dict[tuple[str, str], list[int]] = defaultdict(list)
    for source_row in universe_rows:
        expected_refs[
            (
                source_row[universe_dimension_field],
                source_row["official_mechanism_code"],
            )
        ].append(_as_int(source_row["source_row_number"], field="source_row_number"))

    labels: dict[str, str] = {}
    result: list[dict[str, Any]] = []
    for row in rows:
        dimension = row[dimension_field]
        mechanism = row["official_mechanism_code"]
        labels.setdefault(dimension, row["dimension_label"])
        if labels[dimension] != row["dimension_label"]:
            raise R10OfficialUniverseError(
                f"{table} has inconsistent labels for {dimension}"
            )
        refs = _parse_row_numbers(row["source_row_numbers"])
        expected = expected_refs[(dimension, mechanism)]
        count = _as_int(row["source_row_count"], field=f"{table} source_row_count")
        if refs != expected or count != len(expected):
            raise R10OfficialUniverseError(
                f"{table} cell {dimension} x {mechanism} disagrees with source rows"
            )
        if not count:
            continue
        pages = [page_by_row[number] for number in refs]
        result.append(
            {
                "dimension_code_or_label": dimension,
                "dimension_label": row["dimension_label"],
                "resource_type_code": mechanism,
                "resource_type_label": row["official_mechanism_label"],
                "source_row_count": count,
                "share_of_denominator_percent": _share(count),
                "source_row_refs": {
                    "count": count,
                    "row_numbers_compact": _compress_numbers(refs),
                    "pdf_pages_compact": _compress_numbers(pages),
                },
                "fact_layer": row["fact_layer"],
                "review_gate": row["human_gate"],
                "interpretation_limit": row["interpretation_limit"],
            }
        )
    if sum(item["source_row_count"] for item in result) != EXPECTED_SOURCE_ROWS:
        raise R10OfficialUniverseError(f"{table} non-zero cells do not sum to 616")
    return result, labels


def _statistics(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    _required_columns(
        rows,
        {
            "metric_id",
            "metric_name",
            "value",
            "unit",
            "claim_scope",
            "fact_layer",
            "human_gate",
            "interpretation_limit",
        },
        table=STATISTICS_FILE,
    )
    by_id = {row["metric_id"]: row for row in rows}
    if len(by_id) != len(rows):
        raise R10OfficialUniverseError("Descriptive statistics contain duplicate IDs")
    required = {"M01", "M02", "M08", "M11", "M12", "M13", "M14", "M18", "M19"}
    missing = sorted(required - set(by_id))
    if missing:
        raise R10OfficialUniverseError(
            f"Descriptive statistics are missing required metrics: {missing}"
        )
    expected = {
        "M01": 616.0,
        "M02": 86.0,
        "M08": 365.0,
        "M11": 469.0,
        "M12": 76.1,
        "M13": 19.0,
        "M14": 3.1,
        "M18": 443.0,
        "M19": 71.9,
    }
    for metric_id, expected_value in expected.items():
        value = _as_float(by_id[metric_id]["value"], field=f"{metric_id} value")
        if value != expected_value:
            raise R10OfficialUniverseError(
                f"Descriptive statistic {metric_id} must equal {expected_value}"
            )
    return by_id


def _metric(
    metric_id: str,
    stats: dict[str, dict[str, str]],
    *,
    label_zh: str,
) -> dict[str, Any]:
    row = stats[metric_id]
    raw_value = _as_float(row["value"], field=f"{metric_id} value")
    value: int | float = int(raw_value) if raw_value.is_integer() else raw_value
    return {
        "id": metric_id,
        "label_zh": label_zh,
        "value": value,
        "unit": row["unit"],
        "claim_scope": row["claim_scope"],
        "interpretation_limit": row["interpretation_limit"],
    }


def build_r10_official_universe_exhibit(project_root: Path | str) -> dict[str, Any]:
    """Build the bounded, frontend-safe PUB-MR-012 exhibit.

    The returned dictionary contains no partner-name, actor-identity, program,
    amount, award, or payment rows.  Complete cell provenance is retained only
    as compact S002 row-number and PDF-page ranges.
    """

    root = Path(project_root).resolve()
    package = root / PACKAGE
    universe = _read_csv(package / UNIVERSE_FILE)
    universe_meta = _validate_universe(universe)

    resources = _validate_resource_summary(
        _read_csv(package / RESOURCE_FILE),
        universe_meta["mechanism_counts"],
    )
    departments = _validate_department_summary(
        _read_csv(package / DEPARTMENT_FILE),
        universe_meta["department_counts"],
    )
    stats = _statistics(_read_csv(package / STATISTICS_FILE))

    function_codes = set(universe_meta["function_counts"])
    function_cells, function_labels = _validate_matrix(
        _read_csv(package / FUNCTION_MATRIX_FILE),
        table=FUNCTION_MATRIX_FILE,
        dimension_field="dimension_code_or_name",
        expected_dimension_values=function_codes,
        expected_dimension_type="official_issue_field",
        universe_rows=universe,
        universe_dimension_field="official_issue_field_code",
        page_by_row=universe_meta["page_by_row"],
    )
    department_cells, _ = _validate_matrix(
        _read_csv(package / DEPARTMENT_MATRIX_FILE),
        table=DEPARTMENT_MATRIX_FILE,
        dimension_field="dimension_code_or_name",
        expected_dimension_values=set(universe_meta["department_counts"]),
        expected_dimension_type="department_source_label",
        universe_rows=universe,
        universe_dimension_field="department_display_machine",
        page_by_row=universe_meta["page_by_row"],
    )

    function_resource_counts: dict[str, int] = Counter()
    function_department_sets: dict[str, set[str]] = defaultdict(set)
    for row in universe:
        function = row["official_issue_field_code"]
        function_resource_counts[function] += 1
        function_department_sets[function].add(row["department_display_machine"])

    functions = [
        {
            "code": code,
            "label": function_labels[code],
            "source_row_count": function_resource_counts[code],
            "share_of_denominator_percent": _share(function_resource_counts[code]),
            "department_count": len(function_department_sets[code]),
            "resource_type_count": len(
                {
                    cell["resource_type_code"]
                    for cell in function_cells
                    if cell["dimension_code_or_label"] == code
                }
            ),
            "interpretation_limit": (
                "Official issue-field source-row visibility; not actor purpose, "
                "organizational identity, or political position."
            ),
        }
        for code in sorted(function_codes, key=int)
    ]
    if sum(item["source_row_count"] for item in functions) != EXPECTED_SOURCE_ROWS:
        raise R10OfficialUniverseError("Function summary does not sum to 616")

    department_rank = {
        item["label"]: rank
        for rank, item in enumerate(
            sorted(
                departments,
                key=lambda item: (-item["source_row_count"], item["label"]),
            ),
            start=1,
        )
    }
    function_rank = {
        item["code"]: rank
        for rank, item in enumerate(
            sorted(
                functions,
                key=lambda item: (-item["source_row_count"], int(item["code"])),
            ),
            start=1,
        )
    }
    for item in departments:
        item["rank_by_source_rows"] = department_rank[item["label"]]
    for item in functions:
        item["rank_by_source_rows"] = function_rank[item["code"]]

    departments.sort(key=lambda item: item["rank_by_source_rows"])
    functions.sort(key=lambda item: item["rank_by_source_rows"])
    department_cells.sort(
        key=lambda item: (
            department_rank[item["dimension_code_or_label"]],
            int(item["resource_type_code"]),
        )
    )
    function_cells.sort(
        key=lambda item: (
            function_rank[item["dimension_code_or_label"]],
            int(item["resource_type_code"]),
        )
    )

    headline_metrics = [
        _metric("M18", stats, label_zh="前五个部门的来源记录"),
        _metric("M19", stats, label_zh="前五个部门占全部来源记录"),
        _metric("M11", stats, label_zh="官方机制代码 1–4 的来源记录"),
        _metric("M12", stats, label_zh="官方机制代码 1–4 占全部来源记录"),
        _metric("M13", stats, label_zh="人权／和平与国际协力／交流分野记录"),
        _metric("M14", stats, label_zh="上述两个一期相邻分野占全部来源记录"),
    ]

    return {
        "schema_version": "publication_exhibit_v1",
        "id": "PUB-MR-012",
        "exhibit_type": "official_source_universe",
        "status": "method_ready_bounded",
        "display": {
            "title": {
                "zh": "县政府日常协作：616 条记录",
                "ja": "県の日常的な協働：616件の記録",
                "en": "Everyday Prefectural Collaboration: 616 Records",
            },
            "subtitle": {
                "zh": "查看这些协作集中在哪些部门、事業分野与协作机制。",
                "ja": "協働がどの部局・事業分野・協働形態に集中しているかを見ます。",
                "en": (
                    "Explore which departments, official functions and collaboration "
                    "mechanisms account for these records."
                ),
            },
            "interpretation_limit": {
                "zh": (
                    "这里的单位始终是官方表中的记录行。协作机制不等于付款，"
                    "重复出现不等于组织关系，机器排版标签不作为组织展示。"
                ),
                "ja": (
                    "単位は常に公式表の記録行です。協働形態は支払いを意味せず、"
                    "反復掲載は組織関係を意味しません。機械整形した名称を団体として表示しません。"
                ),
                "en": (
                    "The unit is always an official table row. A mechanism is "
                    "not a payment, repeated appearance is not an organizational "
                    "relation, and machine-formatted labels are not presented as organizations."
                ),
            },
        },
        "denominator": {
            "value": EXPECTED_SOURCE_ROWS,
            "unit": "official_source_rows",
            "source_id": "S002",
            "source_title": universe[0]["source_title"],
            "fiscal_year": 2024,
            "pdf_pages": 86,
            "source_row_range": "S002-R0001–S002-R0616",
            "denominator_is_not": [
                "organizations",
                "contracts",
                "awards",
                "payments",
            ],
        },
        "selection_boundary": {
            "population": (
                "All 616 numbered rows in the archived 86-page FY2024 Okinawa "
                "Prefecture survey of collaboration with NPOs and related bodies."
            ),
            "selection_rule": "complete_source_universe_no_row_sampling",
            "analysis_unit": "one_official_table_source_row",
            "included_dimensions": [
                "department_source_label",
                "official_issue_field",
                "official_collaboration_mechanism",
            ],
            "excluded_from_public_exhibit": [
                "partner_names_and_machine_display_aliases",
                "actor_identity_crosswalks",
                "program_names_and_descriptions",
                "project_cost_cells",
                "purposive_sample_relation_and_amount_ids",
            ],
            "identity_boundary": (
                "The package's 365 normalized machine display labels are omitted "
                "and must not be counted or rendered as actors."
            ),
        },
        "method": {
            "fact_layer": "S002_616_row_source_universe_mechanical_aggregation",
            "method_status": "method_ready_bounded",
            "claim_strength": "descriptive_source_universe_only",
            "review_gate": "none_ready_now",
            "aggregation": (
                "Exact mechanical counts cross-validated against the complete "
                "official resource, department and 19x10 / 15x10 matrix tables."
            ),
            "row_reference_policy": (
                "Every non-zero cell retains complete source-row and PDF-page "
                "references as compact ranges; no underlying partner or amount "
                "record is republished."
            ),
        },
        "headline_metrics": headline_metrics,
        "summaries": {
            "departments": departments,
            "functions": functions,
            "resource_types": resources,
        },
        "drilldown": {
            "department_by_resource_type_nonzero_cells": department_cells,
            "function_by_resource_type_nonzero_cells": function_cells,
            "zero_cell_policy": (
                "Zero cells from the formal complete matrices are omitted from "
                "the publication payload; completeness is declared in dimensions."
            ),
            "dimensions": {
                "departments": 15,
                "functions": 19,
                "resource_types": 10,
                "department_matrix_cells_total": 150,
                "department_matrix_cells_nonzero": len(department_cells),
                "function_matrix_cells_total": 190,
                "function_matrix_cells_nonzero": len(function_cells),
            },
        },
        "interpretation_limits": [
            (
                "Counts describe official source rows, not numbers of organizations, "
                "contracts, awards, payments, alliances or political positions."
            ),
            (
                "The 365 normalized partner display labels are machine layout "
                "aliases, not actor identities or a registry."
            ),
            (
                "Official resource mechanism 4 combines subsidies, assistance and "
                "in-kind support; it is not a cash-grant count."
            ),
            (
                "A whole-program project-cost cell is not an amount paid or awarded "
                "to a named partner; project-cost fields are not published here."
            ),
            (
                "Repeated appearance or department co-occurrence is not stable "
                "partnership, dependence, network centrality or political stance."
            ),
        ],
    }
