"""Evidence integrity regressions for the human-facing offline report."""
import copy
import json
import unittest
from unittest.mock import patch

from scripts.db_demo.build_dashboard import (CHECKS, DEFAULT_EVIDENCE, ROOT,
                                            build_data, oracle_checks, read, safe_json)


class DashboardEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.report = read(DEFAULT_EVIDENCE / "REL-2026.10-DEMO01/migration-report.json")
        self.target = self.report["envelope"]["targets"][0]
        self.contract = self.report["envelope"]["verification"]
        self.fixture = read(ROOT / "demo/customer-profile/reports/fixtures/happy.json")["environments"]["DEV"]

    def test_odc_success_without_oracle_evidence_is_not_pass(self):
        checks = oracle_checks({"native_status": "EXECUTION_SUCCEEDED"}, self.target, self.contract)
        self.assertEqual(set(checks.values()), {"NOT AVAILABLE"})

    def test_oracle_results_must_match_target_identity(self):
        record = copy.deepcopy(self.fixture)
        record["oracle"]["schema"] = "ANOTHER_SCHEMA"
        self.assertNotIn("PASS", oracle_checks(record, self.target, self.contract).values())

    def test_function_and_compile_failures_override_successful_execution(self):
        record = copy.deepcopy(self.fixture)
        record["oracle"]["function"]["result"] = "WRONG"
        record["oracle"]["errors"] = [{"name": "DM_CP_LABEL", "text": "invalid"}]
        checks = oracle_checks(record, self.target, self.contract)
        self.assertEqual(checks["Function test"], "FAIL")
        self.assertEqual(checks["USER_ERRORS"], "FAIL")

    def test_pending_stage_cannot_accept_successful_fixture_oracle_data(self):
        record = copy.deepcopy(self.fixture)
        record["native_status"] = "WAIT_FOR_EXECUTION"
        self.assertEqual(oracle_checks(record, self.target, self.contract), dict.fromkeys(CHECKS, "NOT RUN"))

    def test_missing_query_components_are_unavailable_not_failures(self):
        record = copy.deepcopy(self.fixture)
        for field in ("objects", "errors", "data", "function"):
            record["oracle"].pop(field)
        self.assertEqual(set(oracle_checks(record, self.target, self.contract).values()), {"NOT AVAILABLE"})

    def test_current_snapshot_does_not_promote_pending_approvals_or_fixtures(self):
        data = build_data(DEFAULT_EVIDENCE)
        self.assertEqual(data["overall_status"], "WAITING_APPROVAL")
        self.assertFalse(data["runtime_proven"])
        self.assertEqual([a["status"] for a in data["approvals"][1:3]], ["PENDING", "PENDING"])
        self.assertTrue(all(s["verification_source"] == "NOT_AVAILABLE" for s in data["environments"]))
        self.assertTrue(all(f["source"] == "FIXTURE" for f in data["fixtures"].values()))
        self.assertNotEqual(data["provenance"]["source_commit"], data["provenance"]["merge_commit"])

    def test_embedded_data_cannot_close_script_tag(self):
        value = {"value": '</script><script>alert("demo")</script>&'}
        encoded = safe_json(value)
        self.assertNotIn("<", encoded)
        self.assertEqual(json.loads(encoded), value)

    def test_report_flag_cannot_promote_pending_runtime_to_verified(self):
        report = copy.deepcopy(self.report)
        report["runtime_proven"] = True
        def altered_read(path):
            return report if path == DEFAULT_EVIDENCE / "REL-2026.10-DEMO01/migration-report.json" else read(path)
        with patch("scripts.db_demo.build_dashboard.read", side_effect=altered_read):
            data = build_data(DEFAULT_EVIDENCE)
        self.assertEqual(data["happy_path"], "PARTIAL")
        self.assertFalse(data["runtime_proven"])


if __name__ == "__main__":
    unittest.main()
