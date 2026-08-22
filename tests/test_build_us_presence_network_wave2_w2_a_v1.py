import csv
import hashlib
import json
import unittest
from pathlib import Path

from scripts.build_us_presence_network_wave2_w2_a_v1 import DEFAULT_OUT, ROOT, build


def rows(name: str) -> list[dict[str, str]]:
    with (DEFAULT_OUT / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class W2ABuilderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build(DEFAULT_OUT)

    def test_validation_and_expected_counts(self) -> None:
        self.assertEqual(self.report["status"], "PASS_RESEARCH_ONLY_W2_A")
        self.assertEqual(self.report["counts"]["core_five_official_xml"], 14)
        self.assertEqual(self.report["counts"]["mts_official_xml"], 2)
        self.assertEqual(self.report["counts"]["metric_rows"], 72)
        self.assertEqual(self.report["counts"]["person_rows"], 104)
        self.assertEqual(self.report["counts"]["resource_rows"], 55)
        self.assertEqual(self.report["counts"]["w2d_endpoint_handoff_rows"], 132)
        self.assertTrue(all(self.report["checks"].values()))

    def test_sensitive_filing_semantics_stay_gated(self) -> None:
        metric_rows = rows("filing_metric_long_v1.csv")
        mosco = [
            r for r in metric_rows
            if r["case_id"] == "MOSCO"
            and r["period_end"] == "2025-05-31"
            and r["metric"] == "grants_and_similar_paid_usd"
        ]
        self.assertEqual(len(mosco), 1)
        self.assertEqual(mosco[0]["value"], "")
        self.assertEqual(mosco[0]["field_semantics"], "xml_element_absent_not_zero")

        flow_rows = rows("resource_flow_ledger_v1.csv")
        held = [r for r in flow_rows if r["target_id"] == "HELD_KOSC_2580"]
        self.assertEqual(len(held), 1)
        self.assertEqual(held[0]["included_as_relation_candidate"], "no_defer")
        self.assertEqual(held[0]["transaction_closure"], "defer_not_flow")
        self.assertEqual(held[0]["review_status"], "needs_human_semantic_review")

    def test_awwa_inputs_and_recipient_coverage(self) -> None:
        flow_rows = rows("resource_flow_ledger_v1.csv")
        oesc = [
            r for r in flow_rows
            if r["source_actor_id"] == "X007"
            and r["target_id"] == "X004"
            and r["transaction_closure"] == "provider_filing_named_recipient"
        ]
        mts = [
            r for r in flow_rows
            if r["source_actor_id"] == "X018"
            and r["target_id"] == "X004"
            and r["transaction_closure"] == "provider_filing_named_recipient"
        ]
        self.assertEqual([r["amount"] for r in oesc], ["16308", "14371", "8479"])
        self.assertTrue(all(r["review_status"] == "human_checked" for r in oesc))
        self.assertEqual([r["amount"] for r in mts], ["41183", "19669"])
        self.assertTrue(all(r["review_status"] == "ai_seeded" for r in mts))

        combined = [
            r for r in rows("recipient_coverage_v1.csv")
            if r["coverage_scope"] == "combined_two_tax_periods"
        ][0]
        self.assertEqual(combined["named_descriptor_amount_usd"], "84016")
        self.assertEqual(combined["named_share_of_japanese_bucket_pct"], "53.89")
        self.assertEqual(combined["named_share_of_total_grants_pct"], "38.18")
        fy2023 = next(row for row in rows("recipient_coverage_v1.csv") if row["coverage_scope"] == "2023-05-31")
        self.assertEqual(fy2023["named_share_of_japanese_bucket_pct"], "48.07")
        readme = (DEFAULT_OUT / "README.md").read_text(encoding="utf-8")
        self.assertIn("FY ending 2023，48.07%／35.27%", readme)
        self.assertNotIn("48.06%", readme)
        self.assertEqual(combined["recipient_side_awwa_acknowledgment_count"], "3")
        self.assertEqual(combined["exact_amount_and_period_closed_count"], "0")

    def test_dedup_and_legitimacy_boundaries(self) -> None:
        summaries = rows("resource_flow_dedup_summary_v1.csv")
        self.assertTrue(
            all(
                r["closure_status"]
                in {"components_reconcile_to_grant_line", "grant_field_absent_not_zero"}
                for r in summaries
            )
        )
        flow_rows = rows("resource_flow_ledger_v1.csv")
        tracer_rows = rows("marine_thrift_shop_tracer_v1.csv")
        self.assertFalse(any(r.get("leg_layer", "").upper() == "LEG3" for r in flow_rows + tracer_rows))

    def test_person_and_w2d_endpoint_candidates_are_not_bridges(self) -> None:
        people = rows("person_actor_role_time_v1.csv")
        cross = [r for r in people if r["cross_actor_candidate"] == "yes"]
        self.assertEqual(len(cross), 5)
        self.assertEqual({r["name_as_filed"].casefold() for r in cross}, {"trinicia kloepper", "amber tracy"})

        handoff = rows("w2d_endpoint_handoff_v1.csv")
        family_counts = {}
        for row in handoff:
            family_counts[row["endpoint_family"]] = family_counts.get(row["endpoint_family"], 0) + 1
        self.assertEqual(
            family_counts,
            {
                "person_role_observation": 104,
                "person_identity_pair_candidate": 5,
                "recipient_candidate": 6,
                "organization_flow_observation": 17,
            },
        )
        self.assertFalse(any(r["bridge_status"] in {"confirmed_bridge", "audited_public_record_zero"} for r in handoff))
        pair_rows = [r for r in handoff if r["endpoint_family"] == "person_identity_pair_candidate"]
        self.assertTrue(all(r["adjudication_status"] == "awaiting_principal" for r in pair_rows))

    def test_all_receipt_hashes_and_protected_hashes_are_stable(self) -> None:
        for receipt in rows("source_receipts_v1.csv"):
            if not receipt["artifact_path"]:
                continue
            artifact = ROOT / receipt["artifact_path"]
            self.assertTrue(artifact.exists(), receipt["receipt_id"])
            self.assertEqual(digest(artifact), receipt["sha256"], receipt["receipt_id"])

        validation = json.loads((DEFAULT_OUT / "validation_report_v1.json").read_text(encoding="utf-8"))
        for rel, expected in validation["protected_hashes"].items():
            self.assertEqual(digest(ROOT / rel), expected, rel)

    def test_rebuild_is_byte_deterministic(self) -> None:
        before = digest(DEFAULT_OUT / "manifest.json")
        build(DEFAULT_OUT)
        after = digest(DEFAULT_OUT / "manifest.json")
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
