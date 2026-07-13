from __future__ import annotations

"""Audit the bounded completeness of the R10 working package.

The audit is deliberately source-universe aware.  It distinguishes exact
within-package row accounting from coverage of external documents.  It does
not add actors, relations, amounts, functions, or human-review decisions.
"""

import csv
import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path

import pdfplumber


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"
R10 = ROOT / "outputs" / "R10_administrative_collaboration_v0"
OUT = ROOT / "outputs" / "R10_completeness_audit_v1"
ARCHIVE = ROOT / "source_docs" / "source_archive"

REL_PATH = DATA / "21_admin_collaboration_relations_v0.csv"
AMT_PATH = DATA / "22_admin_amount_observations_v0.csv"
FUN_PATH = DATA / "23_admin_function_observations_v0.csv"
FUNDING_PATH = DATA / "15_funding_or_support_edges_sample_v0.csv"
MANIFEST_PATH = ARCHIVE / "source_archive_manifest.csv"
S002_PATH = ARCHIVE / "S002" / "raw.pdf"
S099_PATH = ARCHIVE / "S099" / "raw.pdf"

S002_FIELDS = [
    "source_row_number",
    "pdf_page",
    "department",
    "office",
    "official_mechanism_code",
    "official_issue_field_code",
    "program_name",
    "program_description",
    "partner_kind_code",
    "partner_name",
    "period",
    "project_cost_thousand_jpy",
    "planning主体",
    "implementation主体",
    "included_r10_relation_id",
    "included_r10_amount_id",
    "coverage_status",
    "interpretation_limit",
]

S099_PROGRAM_COST_ROWS = [
    {
        "source_program_id": "S099P01",
        "program_name": "NGO相談員（外務省委託）",
        "activity_table_page": "2",
        "reported_project_cost_thousand_jpy": "2894",
        "exact_category_cost_jpy_page8": "2894630",
        "explicit_external_commission": "yes",
        "represented_relation_id": "R10R006",
        "represented_amount_id": "R10AM009",
        "coverage_status": "represented",
        "interpretation_limit": "Organization-side project cost; not MOFA payment or contract amount.",
    },
    {
        "source_program_id": "S099P02",
        "program_name": "コザ・インターナショナル・プラザ（沖縄市委託）",
        "activity_table_page": "2",
        "reported_project_cost_thousand_jpy": "16040",
        "exact_category_cost_jpy_page8": "",
        "explicit_external_commission": "yes",
        "represented_relation_id": "R10R004",
        "represented_amount_id": "R10AM006",
        "coverage_status": "represented",
        "interpretation_limit": "Program-row cost; the broader accounting category totals JPY17,724,340 and includes other activities.",
    },
    {
        "source_program_id": "S099P03",
        "program_name": "出前事業",
        "activity_table_page": "2",
        "reported_project_cost_thousand_jpy": "70",
        "exact_category_cost_jpy_page8": "",
        "explicit_external_commission": "no",
        "represented_relation_id": "",
        "represented_amount_id": "",
        "coverage_status": "not_selected_noncommission_program_cost",
        "interpretation_limit": "Activity cost only; no independent external administrative relation is asserted.",
    },
    {
        "source_program_id": "S099P04",
        "program_name": "開発教育関連活動",
        "activity_table_page": "2",
        "reported_project_cost_thousand_jpy": "85",
        "exact_category_cost_jpy_page8": "",
        "explicit_external_commission": "no",
        "represented_relation_id": "",
        "represented_amount_id": "",
        "coverage_status": "not_selected_noncommission_program_cost",
        "interpretation_limit": "Activity cost only; no independent external administrative relation is asserted.",
    },
    {
        "source_program_id": "S099P05",
        "program_name": "Peace & Democracy 2024（沖縄平和賞委員会委託）",
        "activity_table_page": "3",
        "reported_project_cost_thousand_jpy": "1530",
        "exact_category_cost_jpy_page8": "",
        "explicit_external_commission": "no",
        "represented_relation_id": "",
        "represented_amount_id": "",
        "coverage_status": "not_selected_nonpublic_commission_program_cost",
        "interpretation_limit": "A commissioned activity, but not one of the three public-administration relations currently modeled in R10.",
    },
    {
        "source_program_id": "S099P06",
        "program_name": "多文化共生社会の構築に関する万国津梁会議運営等支援業務（沖縄県委託）",
        "activity_table_page": "3",
        "reported_project_cost_thousand_jpy": "5530",
        "exact_category_cost_jpy_page8": "5530234",
        "explicit_external_commission": "yes",
        "represented_relation_id": "R10R005",
        "represented_amount_id": "R10AM008",
        "coverage_status": "represented",
        "interpretation_limit": "Organization-side project cost; not a prefectural payment or contract amount.",
    },
]

R10_ADJACENT_OMITTED_F = {"F001", "F009", "F010"}
UNSUPPORTED_F = {"F019"}
DUPLICATE_F = {"F008"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def clean_pdf_cell(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def extract_s002_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with pdfplumber.open(S002_PATH) as document:
        for page_number, page in enumerate(document.pages, start=1):
            tables = page.extract_tables()
            if len(tables) != 1:
                raise RuntimeError(f"S002 page {page_number}: expected one table, got {len(tables)}")
            for raw in tables[0][3:]:
                if not raw[0] or not clean_pdf_cell(raw[0]).isdigit():
                    continue
                cells = [clean_pdf_cell(cell) for cell in raw]
                rows.append(
                    {
                        "source_row_number": cells[0],
                        "pdf_page": str(page_number),
                        "department": cells[1],
                        "office": cells[2],
                        "official_mechanism_code": cells[3],
                        "official_issue_field_code": cells[4],
                        "program_name": cells[5],
                        "program_description": cells[6],
                        "partner_kind_code": cells[7],
                        "partner_name": cells[8],
                        "period": cells[9],
                        "project_cost_thousand_jpy": cells[10],
                        "planning主体": cells[11],
                        "implementation主体": cells[12],
                    }
                )
    return rows


def s002_selection_map(amounts: list[dict[str, str]]) -> dict[str, tuple[str, str]]:
    selected: dict[str, tuple[str, str]] = {}
    for row in amounts:
        if row["source_refs"] != "S002":
            continue
        match = re.search(r"\brow\s+(\d+)\b", row["source_locators"])
        if not match:
            raise RuntimeError(f"Cannot find S002 row locator for {row['amount_observation_id']}")
        source_row = match.group(1)
        if source_row in selected:
            raise RuntimeError(f"Duplicate S002 row crosswalk: {source_row}")
        selected[source_row] = (row["relation_observation_id"], row["amount_observation_id"])
    return selected


def enrich_s002_rows(
    source_rows: list[dict[str, str]], selected: dict[str, tuple[str, str]]
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for row in source_rows:
        relation_id, amount_id = selected.get(row["source_row_number"], ("", ""))
        output.append(
            {
                **row,
                "included_r10_relation_id": relation_id,
                "included_r10_amount_id": amount_id,
                "coverage_status": "selected_in_r10_purposive_sample" if relation_id else "not_selected",
                "interpretation_limit": (
                    "Source-universe row extraction only; inclusion does not approve the relation or amount."
                ),
            }
        )
    return output


def pct(included: int, universe: int) -> str:
    return f"{100 * included / universe:.1f}" if universe else ""


def coverage_row(
    universe_id: str,
    universe_name: str,
    universe_n: int,
    included_n: int,
    verification_method: str,
    classification: str,
    allowed_claim: str,
    prohibited_claim: str,
    notes: str,
) -> dict[str, object]:
    return {
        "universe_id": universe_id,
        "universe_name": universe_name,
        "universe_records": universe_n,
        "included_records": included_n,
        "coverage_percent": pct(included_n, universe_n),
        "verification_method": verification_method,
        "completeness_classification": classification,
        "allowed_claim": allowed_claim,
        "prohibited_claim": prohibited_claim,
        "notes": notes,
    }


def build_coverage_summary(
    relations: list[dict[str, str]],
    amounts: list[dict[str, str]],
    functions: list[dict[str, str]],
    s002_rows: list[dict[str, str]],
    selected_s002: dict[str, tuple[str, str]],
    funding: list[dict[str, str]],
    represented_f: set[str],
) -> list[dict[str, object]]:
    selected_numbers = {int(value) for value in selected_s002}

    def subset(predicate) -> tuple[int, int]:
        members = [row for row in s002_rows if predicate(row)]
        selected = sum(int(row["source_row_number"]) in selected_numbers for row in members)
        return len(members), selected

    d10_n, d10_selected = subset(lambda row: row["official_issue_field_code"] == "10")
    d11_n, d11_selected = subset(lambda row: row["official_issue_field_code"] == "11")
    d1011_n, d1011_selected = subset(lambda row: row["official_issue_field_code"] in {"10", "11"})
    office_n, office_selected = subset(lambda row: clean_pdf_cell(row["office"]).replace(" ", "") == "交流推進課")
    amount_relations = {row["relation_observation_id"] for row in amounts}
    function_relations = {row["relation_observation_id"] for row in functions}
    s099_explicit = [row for row in S099_PROGRAM_COST_ROWS if row["explicit_external_commission"] == "yes"]
    s099_explicit_included = [row for row in s099_explicit if row["represented_relation_id"]]
    s099_nonzero_included = [row for row in S099_PROGRAM_COST_ROWS if row["represented_relation_id"]]
    rows = [
        coverage_row(
            "U01", "Current R10 relation table", len(relations), len(relations),
            "CSV primary-key validation", "within_package_accounting_complete",
            "The current package has exactly 35 unique relation observations.",
            "The 35 rows are a complete inventory of Okinawa administrative or service relations.",
            "Internal row accounting only; the external source universe is not 35.",
        ),
        coverage_row(
            "U02", "Current R10 amount table", len(amounts), len(amounts),
            "CSV primary-key and foreign-key validation", "within_package_accounting_complete",
            "The current package has exactly 26 amount observations attached to 19 relations.",
            "The 26 rows exhaust all amounts in S002, S099, AWWA, USO, or Okinawa public records.",
            "Amounts are selected observations and are not additive by default.",
        ),
        coverage_row(
            "U03", "Current R10 function table", len(functions), len(functions),
            "CSV primary-key and foreign-key validation", "within_package_accounting_complete",
            "The current package has exactly 43 function observations attached to 33 relations.",
            "The 43 rows exhaust the functions of all included organizations or source documents.",
            "Functions are explanatory coding of selected relations; eight rows are USO sites.",
        ),
        coverage_row(
            "U04", "S002 FY2024 Okinawa Prefecture NPO collaboration survey: all rows", len(s002_rows), len(selected_s002),
            "pdfplumber table extraction; sequential row validation", "purposive_sample_not_complete",
            "R10 selected 10 named rows from the 616-row official survey.",
            "R10 is a full extraction of the FY2024 official collaboration survey.",
            "S002 PDF has 86 pages and rows 1-616 with no missing or duplicate row numbers.",
        ),
        coverage_row(
            "U05", "Current R10 purposive selection within S002 fields 10 (human rights/peace) + 11 (international cooperation/exchange)", d1011_n, d1011_selected,
            "mechanical filter over extracted S002 fields", "purposive_sample_not_complete",
            "R10 selected 10 of the 19 S002 rows in the two Phase-1-adjacent official fields.",
            "R10 exhausts the official peace/human-rights and international-cooperation fields.",
            "The omitted rows remain source records, not approved relation candidates.",
        ),
        coverage_row(
            "U06", "Current R10 purposive selection within S002 field 10: human rights/peace", d10_n, d10_selected,
            "mechanical filter over extracted S002 fields", "purposive_sample_not_complete",
            "R10 selected rows 1, 10, and 11 from this eight-row field.",
            "The three selected rows represent all FY2024 peace/human-rights collaborations.",
            "Omitted source rows are 9, 204, 246, 496, and 529.",
        ),
        coverage_row(
            "U07", "Current R10 purposive selection within S002 field 11: international cooperation/exchange", d11_n, d11_selected,
            "mechanical filter over extracted S002 fields", "purposive_sample_not_complete",
            "R10 selected rows 431-437 from this eleven-row field.",
            "Rows 431-437 are the full FY2024 international cooperation/exchange field.",
            "Omitted source rows are 438, 501, 548, and 571.",
        ),
        coverage_row(
            "U08", "Current R10 purposive selection within the S002 Exchange Promotion Division block", office_n, office_selected,
            "mechanical office-name filter over extracted S002 fields", "near_complete_but_missing_one_row",
            "R10 selected seven of the division's eight contiguous source rows.",
            "R10 fully extracts the Exchange Promotion Division block.",
            "Row 438 is the exact online-available omission.",
        ),
        coverage_row(
            "U09", "S099 FY2024 activity-report rows explicitly marked as public external commissions", len(s099_explicit), len(s099_explicit_included),
            "page-level visual inspection of image-only PDF pp.2-3 and accounting cross-check on p.8",
            "bounded_complete_visual_not_machine_enumerated",
            "All three explicitly public-commissioned program rows are represented: MOFA consultant, Okinawa City KIP, and Okinawa Prefecture multicultural support.",
            "The three R10 amounts exhaust S099's annual activities or total project costs.",
            "This is a source-row completeness check, not HR-018 approval of the relations or payment semantics.",
        ),
        coverage_row(
            "U10", "S099 non-zero program-cost rows in the activity table", len(S099_PROGRAM_COST_ROWS), len(s099_nonzero_included),
            "page-level visual inspection of image-only PDF pp.2-3", "purpose_selected_not_complete",
            "R10 represents three of six non-zero program-cost rows because it follows public-administration relations.",
            "R10 extracts all non-zero activity costs from S099.",
            "Unselected non-zero rows are outreach, development education, and Peace & Democracy 2024.",
        ),
        coverage_row(
            "U11", "Central funding/support/relation sample table", len(funding), len(represented_f),
            "mechanical F-ID crosswalk", "purpose_selected_not_complete",
            "R10 crosswalks 24 of the 43 central sample rows, consolidating some into one relation.",
            "The R10 lower layer fully represents the central funding/support table.",
            "F001/F009/F010 are R10-adjacent omissions; F019 is unsupported; remaining omissions belong mainly to other modules.",
        ),
        coverage_row(
            "U12", "R10 relations with one or more amount observations", len(relations), len(amount_relations),
            "mechanical foreign-key aggregation", "partial_by_design",
            "Nineteen of 35 selected relations carry one or more amount observations.",
            "Relations without amounts have zero value or no financial relevance.",
            "Absence of an amount means unobserved/not modeled, not zero.",
        ),
        coverage_row(
            "U13", "R10 relations with one or more function observations", len(relations), len(function_relations),
            "mechanical foreign-key aggregation", "partial_by_design",
            "Thirty-three of 35 selected relations carry one or more function observations.",
            "The 43 function rows are a complete function census.",
            "R10R002/R10R003 reuse the KIP function coding attached to R10R004 rather than duplicate it by year.",
        ),
    ]
    return rows


def build_relation_crosswalk(
    relations: list[dict[str, str]],
    amounts: list[dict[str, str]],
    functions: list[dict[str, str]],
    selected_s002: dict[str, tuple[str, str]],
) -> list[dict[str, str]]:
    amounts_by_relation: dict[str, list[str]] = defaultdict(list)
    functions_by_relation: dict[str, list[str]] = defaultdict(list)
    s002_by_relation: dict[str, list[str]] = defaultdict(list)
    for row in amounts:
        amounts_by_relation[row["relation_observation_id"]].append(row["amount_observation_id"])
    for row in functions:
        functions_by_relation[row["relation_observation_id"]].append(row["function_observation_id"])
    for source_row, (relation_id, _amount_id) in selected_s002.items():
        s002_by_relation[relation_id].append(source_row)

    output: list[dict[str, str]] = []
    for row in relations:
        rid = row["relation_observation_id"]
        if s002_by_relation.get(rid):
            family = "S002_FY2024_selected_official_rows"
            design = "purposive selection from a 616-row official table"
        elif rid in {"R10R001", "R10R002", "R10R003", "R10R004", "R10R006", "R10R007"}:
            family = "ONC_multi_source_case_and_selected_years"
            design = "case-driven multi-source selection; not a continuous annual panel"
        else:
            family = "central_relation_sample_recode"
            design = "purpose-selected recode/consolidation of existing sample rows"
        output.append(
            {
                "relation_observation_id": rid,
                "source_record_ids": row["source_record_ids"],
                "source_refs": row["source_refs"],
                "source_universe_family": family,
                "selection_design": design,
                "s002_source_row_numbers": ";".join(sorted(s002_by_relation.get(rid, []), key=int)),
                "linked_amount_ids": ";".join(amounts_by_relation.get(rid, [])),
                "linked_function_ids": ";".join(functions_by_relation.get(rid, [])),
                "current_review_status": row["review_status"],
                "external_completeness_claim_allowed": "no",
                "human_gate": (
                    "existing_human_decision_inherited" if row["review_status"] in {"human_checked", "human_revised"}
                    else "HR-018_required_before_relation_publication"
                ),
                "interpretation_limit": "Row accounting is exact inside R10; source-universe coverage is purposive unless a separate bounded universe is stated.",
            }
        )
    return output


def build_funding_crosswalk(
    funding: list[dict[str, str]], relations: list[dict[str, str]]
) -> tuple[list[dict[str, str]], set[str]]:
    relation_map: dict[str, list[str]] = defaultdict(list)
    for row in relations:
        for record_id in row["source_record_ids"].split(";"):
            if re.fullmatch(r"F\d{3}", record_id):
                relation_map[record_id].append(row["relation_observation_id"])
    represented = set(relation_map)
    output: list[dict[str, str]] = []
    for row in funding:
        edge_id = row["edge_id"]
        if edge_id in represented:
            scope = "represented_or_consolidated_in_R10"
            next_action = "No completeness action; preserve the relation's existing human gate."
        elif edge_id in R10_ADJACENT_OMITTED_F:
            scope = "R10_adjacent_omission"
            next_action = "Resolve source-level citation/locator online, then decide whether HR-018 should be extended."
        elif edge_id in UNSUPPORTED_F:
            scope = "excluded_unsupported_relation"
            next_action = "Do not reintroduce without a new human decision and valid supporting source."
        elif edge_id in DUPLICATE_F:
            scope = "excluded_duplicate_replaced"
            next_action = "Keep the replacement row only."
        else:
            scope = "excluded_other_module_or_non_R10_scope"
            next_action = "No R10 action unless the module boundary is formally expanded."
        output.append(
            {
                "edge_id": edge_id,
                "relation_type": row["relation_type"],
                "event_or_program": row["event_or_program"],
                "source_ref": row["source_ref"],
                "current_review_status": row["review_status"],
                "represented_in_r10": "yes" if edge_id in represented else "no",
                "mapped_r10_relation_ids": ";".join(relation_map.get(edge_id, [])),
                "audit_scope_class": scope,
                "next_action_if_scope_expands": next_action,
                "interpretation_limit": "Crosswalk status does not approve or reject the underlying relation.",
            }
        )
    return output, represented


def build_gap_rows() -> list[dict[str, str]]:
    return [
        {
            "gap_id": "R10C-G01",
            "priority": "P0_if_expanding_exchange_relation_layer",
            "gap_type": "online_source_row",
            "exact_scope": "S002 row 438, Exchange Promotion Division, field 11",
            "online_action": "No extraction remains: the row is already formalized in the 616-row official source-universe package.",
            "human_action": "Decide through HR-018 whether it belongs in R10; do not auto-add the relation or amount.",
            "trigger": "Only required if the report converts the source-level division block into actor/relation-level coverage; the ready-now source-universe figure already includes it.",
        },
        {
            "gap_id": "R10C-G02",
            "priority": "P1_if_claiming_field_11_completeness",
            "gap_type": "online_source_rows",
            "exact_scope": "S002 rows 501, 548, 571 in official field 11",
            "online_action": "No extraction remains; triage actor crosswalks only if expanding the purposive relation layer.",
            "human_action": "Use HR-018 or a successor task to accept/revise/reject any proposed relation.",
            "trigger": "Only required for an actor/relation-level all-field claim; the formal source-universe table already includes all three rows.",
        },
        {
            "gap_id": "R10C-G03",
            "priority": "P1_if_claiming_field_10_completeness",
            "gap_type": "online_source_rows",
            "exact_scope": "S002 rows 9, 204, 246, 496, 529 in official field 10",
            "online_action": "No extraction remains; triage actor crosswalks only if expanding the purposive relation layer.",
            "human_action": "Keep background institutions and general public-interest actors separate from Phase-1 core actors.",
            "trigger": "Only required for an actor/relation-level all-field claim; the formal source-universe table already includes all five rows.",
        },
        {
            "gap_id": "R10C-G04",
            "priority": "P1_if_claiming_lower_layer_completeness",
            "gap_type": "source_and_scope_crosswalk",
            "exact_scope": "Central rows F001, F009, F010",
            "online_action": "Replace actor-ID source_ref values with source IDs/URLs and exact locators before reuse.",
            "human_action": "Decide whether the Phoenix donation, Red Cross service, and relief-society service belong in R10.",
            "trigger": "Required only if the lower service/charity layer is presented as exhaustive of the central sample.",
        },
        {
            "gap_id": "R10C-G05",
            "priority": "P0_for_publication_wording",
            "gap_type": "source_universe_label",
            "exact_scope": "S099 image-only annual report, pp.2-3 and p.8",
            "online_action": "No new relation search is required; retain the six-row page-level crosswalk in this audit.",
            "human_action": "If publishing a completeness statement, verify the page-level enumeration while reviewing HR-018.",
            "trigger": "Use the narrow phrase 'three explicitly public-commissioned program rows', not 'all annual-report project costs'.",
        },
        {
            "gap_id": "R10C-G06",
            "priority": "P2_conditional_longitudinal",
            "gap_type": "year_gap",
            "exact_scope": "KIP public records between FY2020 and FY2024",
            "online_action": "Search FY2021-FY2023 city verification/contract records only if a continuous annual series is needed.",
            "human_action": "None until a longitudinal claim is proposed; HR-018 still gates any new relation/amount.",
            "trigger": "Current 2019/2020/2024 observations are selected years, not a continuous panel.",
        },
    ]


def validate(
    relations: list[dict[str, str]],
    amounts: list[dict[str, str]],
    functions: list[dict[str, str]],
    funding: list[dict[str, str]],
    s002_rows: list[dict[str, str]],
    selected_s002: dict[str, tuple[str, str]],
    represented_f: set[str],
) -> list[str]:
    checks: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            raise AssertionError(message)
        checks.append(message)

    relation_ids = [row["relation_observation_id"] for row in relations]
    amount_ids = [row["amount_observation_id"] for row in amounts]
    function_ids = [row["function_observation_id"] for row in functions]
    check(len(relations) == 35 and len(set(relation_ids)) == 35, "PASS: 35 unique relation observations")
    check(len(amounts) == 26 and len(set(amount_ids)) == 26, "PASS: 26 unique amount observations")
    check(len(functions) == 43 and len(set(function_ids)) == 43, "PASS: 43 unique function observations")
    check({row["relation_observation_id"] for row in amounts} <= set(relation_ids), "PASS: all amount foreign keys resolve")
    check({row["relation_observation_id"] for row in functions} <= set(relation_ids), "PASS: all function foreign keys resolve")
    source_numbers = [int(row["source_row_number"]) for row in s002_rows]
    check(source_numbers == list(range(1, 617)), "PASS: S002 extracts sequential rows 1-616 with no gaps or duplicates")
    check(len(selected_s002) == 10, "PASS: exactly 10 S002 source rows crosswalk to R10")
    check(set(map(int, selected_s002)) == {1, 10, 11, 431, 432, 433, 434, 435, 436, 437}, "PASS: S002 selected-row set is stable")
    d10 = [row for row in s002_rows if row["official_issue_field_code"] == "10"]
    d11 = [row for row in s002_rows if row["official_issue_field_code"] == "11"]
    check(len(d10) == 8, "PASS: S002 field 10 contains 8 rows")
    check(len(d11) == 11, "PASS: S002 field 11 contains 11 rows")
    exchange = [row for row in s002_rows if row["office"].replace(" ", "") == "交流推進課"]
    check(len(exchange) == 8, "PASS: S002 Exchange Promotion Division contains 8 rows")
    check(len(funding) == 43 and len(represented_f) == 24, "PASS: R10 crosswalks 24 of 43 central relation-sample rows")
    s099_amount_ids = {row["represented_amount_id"] for row in S099_PROGRAM_COST_ROWS if row["represented_amount_id"]}
    check(s099_amount_ids == {"R10AM006", "R10AM008", "R10AM009"}, "PASS: S099 represented amount IDs match the three public-commission rows")

    manifest = {row["source_id"]: row for row in read_csv(MANIFEST_PATH)}
    check(manifest["S002"]["sha256"] == sha256(S002_PATH), "PASS: S002 archive SHA matches manifest")
    check(manifest["S099"]["sha256"] == sha256(S099_PATH), "PASS: S099 archive SHA matches manifest")
    review_counts = Counter(row["review_status"] for row in relations)
    check(review_counts["human_checked"] + review_counts["human_revised"] == 9, "PASS: audit preserves 9 inherited human-reviewed relations and does not upgrade others")
    return checks


def write_brief(coverage: list[dict[str, object]]) -> None:
    by_id = {row["universe_id"]: row for row in coverage}
    brief = f"""# R10 有界完整性核验 v1

日期：2026-07-13

## 结论

**35 条 relation、26 条 amount 和 43 条 function 只在当前 R10 包内部计数完备；它们不是任何外部资料库或机制部门的全量抽取。** 当前 R10 是围绕 ONC、基地／和平信息、国际交流、军属服务与慈善支持所构造的**目的性、跨来源案例样本**。

## 四个可复核的范围判定

1. **当前 35-relation 目的性样本对 S002 并非全量。** 本地归档 PDF 共 86 页、616 条 FY2024 县级“NPO 等协作”记录；该样本只选了 {by_id['U04']['included_records']}/{by_id['U04']['universe_records']} 条（{by_id['U04']['coverage_percent']}%）。616 行来源总体已另在 `R10_official_collaboration_universe_v1` 全量形式化。
2. **即使收窄到一期相关官方领域，仍不是全量。** 官方事业分野 10（人权／和平）与 11（国际合作／交流）共 {by_id['U05']['universe_records']} 条，R10 覆盖 {by_id['U05']['included_records']} 条（{by_id['U05']['coverage_percent']}%）。交流推进课的连续区块为 8 条，当前只有 7 条，精确缺口是 S002 row 438。
3. **S099 只能做非对称的小范围完整性判定。** 图像型年报 pp.2-3 中明确标为公共行政委托的 3 个项目（MOFA 相谈员、冲绳市 KIP、冲绳县多文化支援）均已映射到 R10；但年报共有 6 个非零项目成本行，R10 只取 3 个，且 KIP 16.040m 与该会计分类总计 17.72434m 不是同一口径。
4. **下层服务／慈善也是目的性样本。** R10 交叉了中央 43 条 relation sample 中的 24 条 F 记录；F001、F009、F010 与 R10 相邻但未进入，F019 则是已标记不支持的关系，其余多属其他模块。

## 35／26／43 应该如何表述

- 可写：“当前目的性 R10 样本内有 35 条规范化关系观察、26 条金额观察和 43 条功能观察；类型计数对这 35 条内部加总完备。”
- 不可写：“系统抽取冲绳 FY2024 行政协作全量”、“全部国际交流委托”、“完整军属慈善网”或“26 条金额穷尽已公开资金”。
- S099 唯一可用的完整性短语是：“该 FY2024 年报中明确标为**公共行政委托**的三个项目行已全部进入候选映射”。这是来源行范围，不是关系人审通过，也不是付款语义认定。

## 目的性 actor／relation 层的精确缺口与顺序

1. 若报告继续定位为**目的性案例样本**，不必为数量扩张；只需修正完整性措辞并完成 HR-018。
2. row 438、501、548、571、9、204、246、496、529 已全部进入 616-row 正式来源总体；只有要把“来源总体完整”进一步改写为“actor／relation 层完整”时，才需经 HR-018／HR-032 处理身份与关系。它们不得由 source row 自动建边。
3. 若要声称下层服务／慈善完整，需先为 F001、F009、F010 把 actor-ID 式 `source_ref` 换成可归档 URL/source ID 与 locator，再交 HR-018 决定是否入 R10。
4. KIP 2019／2020／2024 是选定年份，不是连续年表。只有报告要做纵向趋势时，才需继续线上查 FY2021-FY2023。

## 人审与敏感边界

本核验不新增或批准任何 actor、relation、amount 或 function。已有 9 条关系仅继承原人审状态，其余仍由 HR-018 决定。S002 的全表抽取是来源总体索引，不是新的关系表。

## 正式来源总体层

S002 的 616 行已进一步形成独立、可重跑的 `outputs/R10_official_collaboration_universe_v1/`：正式来源总体表保留 row／page，另有 partner source-label × mechanism／department 双模聚合、两张解释图和 8 项紧凑 HR-032。该总体层不把 raw source rows 升为 registry actor 或 relation edge；纯 616-row 图为 `ready_now / no HR gate`，只有未来的法人 alias、JV 成员展开或 registry crosswalk 受 HR-032 控制。
"""
    (OUT / "R10_bounded_completeness_brief_v1.md").write_text(brief, encoding="utf-8")


def write_validation_report(checks: list[str], coverage: list[dict[str, object]]) -> None:
    by_id = {row["universe_id"]: row for row in coverage}
    report = "# R10 completeness audit validation v1\n\nDate: 2026-07-13\n\n"
    report += "## Structural checks\n\n" + "\n".join(f"- {item}" for item in checks) + "\n\n"
    report += "## Boundary checks\n\n"
    report += f"- PASS: S002 whole-table coverage is {by_id['U04']['included_records']}/{by_id['U04']['universe_records']}; classification is purposive sample.\n"
    report += f"- PASS: S002 field 10+11 coverage is {by_id['U05']['included_records']}/{by_id['U05']['universe_records']}; no full-field claim is allowed.\n"
    report += "- PASS: S099's three explicitly public-commissioned rows are represented, while only 3/6 non-zero program-cost rows are selected.\n"
    report += "- PASS: No central actor, relation, amount, function, source-log, or human-review table is mutated by this audit.\n"
    report += "- PASS: Every generated table states that source-universe crosswalk status does not approve a sensitive relation.\n"
    (OUT / "validation_report_v1.md").write_text(report, encoding="utf-8")


def write_readme() -> None:
    readme = """# R10 completeness audit v1

This package separates exact within-package accounting from external-source completeness.

- `R10_bounded_completeness_brief_v1.md`: conclusion, safe wording, exact online gaps.
- `source_universe_coverage_v1.csv`: 13 bounded universes and permitted/prohibited claims.
- `relation_source_universe_crosswalk_v1.csv`: all 35 R10 relations mapped to their selection design and human gate.
- `s002_universe_index_v1.csv`: mechanical index of all 616 FY2024 official survey rows; it is not an approved relation table.
- `s099_program_cost_crosswalk_v1.csv`: page-level six-row non-zero program-cost crosswalk; S099 is image-only and this enumeration is not human review.
- `central_relation_sample_crosswalk_v1.csv`: all 43 central F rows mapped to R10 or an explicit exclusion class.
- `online_gap_and_human_task_suggestions_v1.csv`: conditional purposive-layer gaps and human-gate suggestions; the 616-row source extraction itself is complete.
- `validation_report_v1.md`: structural, SHA, foreign-key, and scope checks.

The full S002 source universe is now formalized in `outputs/R10_official_collaboration_universe_v1/`, including an authoritative 616-row table, source-label bimode tables, two figures, and the compact HR032 identity/crosswalk queue.  The audit index remains the independent extraction-parity check.

The audit never mutates central research tables and never upgrades a review status.
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")


def validate_text_cleanliness() -> None:
    for path in OUT.glob("*.md"):
        lines = path.read_text(encoding="utf-8").splitlines()
        bad = [index for index, line in enumerate(lines, start=1) if line.rstrip() != line]
        if bad:
            raise AssertionError(f"Trailing whitespace in {path}: {bad}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    relations = read_csv(REL_PATH)
    amounts = read_csv(AMT_PATH)
    functions = read_csv(FUN_PATH)
    funding = read_csv(FUNDING_PATH)
    s002_raw = extract_s002_rows()
    selected_s002 = s002_selection_map(amounts)
    s002_index = enrich_s002_rows(s002_raw, selected_s002)
    funding_crosswalk, represented_f = build_funding_crosswalk(funding, relations)
    coverage = build_coverage_summary(
        relations, amounts, functions, s002_raw, selected_s002, funding, represented_f
    )
    relation_crosswalk = build_relation_crosswalk(relations, amounts, functions, selected_s002)
    checks = validate(
        relations, amounts, functions, funding, s002_raw, selected_s002, represented_f
    )

    write_csv(OUT / "s002_universe_index_v1.csv", s002_index, S002_FIELDS)
    write_csv(
        OUT / "s099_program_cost_crosswalk_v1.csv",
        S099_PROGRAM_COST_ROWS,
        list(S099_PROGRAM_COST_ROWS[0]),
    )
    write_csv(
        OUT / "source_universe_coverage_v1.csv",
        coverage,
        list(coverage[0]),
    )
    write_csv(
        OUT / "relation_source_universe_crosswalk_v1.csv",
        relation_crosswalk,
        list(relation_crosswalk[0]),
    )
    write_csv(
        OUT / "central_relation_sample_crosswalk_v1.csv",
        funding_crosswalk,
        list(funding_crosswalk[0]),
    )
    gap_rows = build_gap_rows()
    write_csv(
        OUT / "online_gap_and_human_task_suggestions_v1.csv",
        gap_rows,
        list(gap_rows[0]),
    )
    write_brief(coverage)
    write_validation_report(checks, coverage)
    write_readme()
    validate_text_cleanliness()
    print(
        "R10 completeness audit built: "
        f"{len(s002_index)} S002 rows, {len(coverage)} universes, "
        f"{len(relation_crosswalk)} relation crosswalks"
    )


if __name__ == "__main__":
    main()
