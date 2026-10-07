import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch

import yaml

from scripts.db_demo.build_release import build_release, verify_bundle
from scripts.db_demo.collect_evidence import collect
from scripts.db_demo.common import DemoError, ENVIRONMENTS, ROOT, app_root, environments, file_hash, load_yaml, sanitize, sha256
from scripts.db_demo.generate_report import make_report, render
from scripts.db_demo.odc_client import ODCClient
from scripts.db_demo.validate_manifest import changed_releases, validate_release
from scripts.db_demo.validate_sql import analyze
from scripts.db_demo.verify_oracle import assess, queries, verify_live

HAPPY = "REL-2026.10-DEMO01"
FAIL = "REL-2026.10-DEMO02-FAIL"
FIX = "REL-2026.10-DEMO02-FIX"


def sample_metadata():
    return {"git_repository": "devsecopslonghn/DB-Research", "git_commit": "0" * 40,
            "git_branch": "SAMPLE", "github_actor": "SAMPLE_ACTOR", "github_run_id": "NOT_AVAILABLE",
            "created_at": "2026-10-08T00:00:00+00:00", "evidence_source": "FIXTURE"}


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "demo", self.root / "demo")
        self.manifest = self.root / "demo/customer-profile/migrations" / HAPPY / "manifest.yaml"

    def tearDown(self):
        self.temp.cleanup()

    def mutate(self, change):
        value = load_yaml(self.manifest)
        change(value)
        self.manifest.write_text(yaml.safe_dump(value, sort_keys=False))

    def test_all_three_release_contracts(self):
        for rid in (HAPPY, FAIL, FIX):
            result, _ = validate_release(rid, self.root)
            self.assertEqual(result["status"], "VALIDATED")

    def test_duplicate_missing_reordered_and_traversal_files(self):
        original = self.manifest.read_text()
        changes = [lambda v: v["migrations"].append(v["migrations"][0]),
                   lambda v: v["migrations"].reverse(),
                   lambda v: v["migrations"].__setitem__(0, "001_missing.sql"),
                   lambda v: v["migrations"].__setitem__(0, "../001_escape.sql")]
        for change in changes:
            self.manifest.write_text(original)
            self.mutate(change)
            with self.assertRaises(DemoError):
                validate_release(HAPPY, self.root)

    def test_unique_order_prefix_even_when_names_differ(self):
        path = self.manifest.parent
        (path / "002_create_customer_sequence.sql").rename(path / "001_other_sequence.sql")
        self.mutate(lambda v: v["migrations"].__setitem__(1, "001_other_sequence.sql"))
        with self.assertRaises(DemoError):
            validate_release(HAPPY, self.root)

    def test_secrets_and_disabled_verification_rejected(self):
        original = self.manifest.read_text()
        for change in [lambda v: v.update(password="not-a-real-secret"),
                       lambda v: v["verification"].update(compile_errors=False),
                       lambda v: v["rollout"].update(mode="auto")]:
            self.manifest.write_text(original)
            self.mutate(change)
            with self.assertRaises(DemoError):
                validate_release(HAPPY, self.root)

    def test_duplicate_yaml_keys_rejected(self):
        self.manifest.write_text(self.manifest.read_text() + "release_id: duplicate\n")
        with self.assertRaises(DemoError):
            load_yaml(self.manifest)

    def test_schema_target_change_and_symlink_rejected(self):
        config = self.root / "demo/customer-profile/environments/dev.yaml"
        original = config.read_text()
        config.write_text(original.replace("ODC_POC_20261004_DEV", "PRODUCTION"))
        with self.assertRaises(DemoError):
            validate_release(HAPPY, self.root)
        config.write_text(original)
        file = self.manifest.parent / "001_create_customer_table.sql"
        original_sql = file.read_text()
        outside = self.root / "outside.sql"
        outside.write_text(original_sql)
        file.unlink()
        file.symlink_to(outside)
        with self.assertRaises(DemoError):
            validate_release(HAPPY, self.root)

    def test_hashes_exact_bytes_and_envelope_targets(self):
        output = self.root / "artifact"
        envelope = build_release(HAPPY, output, self.root, sample_metadata(), committed=False)
        for migration in envelope["migrations"]:
            self.assertEqual(migration["sha256"], file_hash(self.manifest.parent / migration["file"]))
        self.assertEqual([t["environment"] for t in envelope["targets"]], list(ENVIRONMENTS))
        self.assertEqual(envelope["sql_sha256"], file_hash(output / "release-bundle/migration.sql"))
        self.assertEqual(verify_bundle(output, self.root), envelope)

    def test_bundle_tampering_and_overwrite_rejected(self):
        output = self.root / "artifact"
        build_release(HAPPY, output, self.root, sample_metadata(), committed=False)
        (output / "release-bundle/migration.sql").write_text("ALTER SYSTEM SHUTDOWN;")
        with self.assertRaises(DemoError):
            verify_bundle(output, self.root)
        with self.assertRaises(DemoError):
            build_release(HAPPY, output, self.root, sample_metadata(), committed=False)

    def test_manifest_and_envelope_target_tamper_rejected(self):
        for key in ("targets", "verification"):
            output = self.root / key
            env = build_release(HAPPY, output, self.root, sample_metadata(), committed=False)
            if key == "targets":
                env["targets"][0]["schema"] = "PRODUCTION"
            else:
                env["verification"]["compile_errors"] = False
            (output / "release-envelope.json").write_text(json.dumps(env))
            with self.assertRaises(DemoError):
                verify_bundle(output, self.root)

    def test_committed_source_required_and_reproducible(self):
        def git(*args):
            return subprocess.check_output(["git", "-C", str(self.root), *args], stderr=subprocess.DEVNULL).decode().strip()
        git("init", "-b", "main")
        git("config", "user.email", "fixture@example.invalid")
        git("config", "user.name", "Fixture")
        git("add", "demo")
        git("commit", "-qm", "Fixture release")
        first = build_release(HAPPY, self.root / "artifact1", self.root)
        second = build_release(HAPPY, self.root / "artifact2", self.root)
        self.assertEqual(first, second)
        self.assertEqual(first["git_commit"], git("rev-parse", "HEAD"))
        file = self.manifest.parent / "001_create_customer_table.sql"
        file.write_text(file.read_text() + "-- changed after commit\n")
        with self.assertRaises(DemoError):
            build_release(HAPPY, self.root / "artifact3", self.root)

    def test_existing_release_immutable_against_pr_base(self):
        def git(*args):
            return subprocess.check_output(["git", "-C", str(self.root), *args], stderr=subprocess.DEVNULL).decode().strip()
        git("init", "-b", "main")
        git("config", "user.email", "fixture@example.invalid")
        git("config", "user.name", "Fixture")
        git("add", "demo")
        git("commit", "-qm", "Base")
        base = git("rev-parse", "HEAD")
        self.manifest.write_text(self.manifest.read_text().replace("synthetic customer", "edited customer"))
        git("add", "demo")
        git("commit", "-qm", "Edit old manifest")
        changed, errors = changed_releases(self.root, base, git("rev-parse", "HEAD"))
        self.assertIn(HAPPY, changed)
        self.assertEqual(len(errors), 1)


class PolicyTests(unittest.TestCase):
    def test_all_required_policy_classes(self):
        for sql, level in [("ALTER SYSTEM FLUSH SHARED_POOL;", "BLOCKED"), ("CREATE USER U IDENTIFIED BY X;", "BLOCKED"),
                           ("DROP USER U;", "BLOCKED"), ("GRANT DBA TO U;", "BLOCKED"), ("DROP TABLE X;", "REQUIRES_DBA_REVIEW"),
                           ("TRUNCATE TABLE X;", "REQUIRES_DBA_REVIEW"), ("COMMIT;", "WARNING"), ("ROLLBACK;", "WARNING"),
                           ("WHENEVER SQLERROR EXIT", "REQUIRES_DBA_REVIEW"), ("SPOOL file", "REQUIRES_DBA_REVIEW"),
                           ("@script.sql", "REQUIRES_DBA_REVIEW"), ("@@script.sql", "REQUIRES_DBA_REVIEW"),
                           ("SELECT '&value', '&&value' FROM DUAL;", "REQUIRES_DBA_REVIEW")]:
            result = analyze(sql)
            self.assertTrue(any(f["level"] == level for f in result["findings"]), sql)
            self.assertEqual(bool(result["errors"]), level == "BLOCKED", sql)

    def test_comments_literals_and_split_keyword(self):
        result = analyze("-- DROP TABLE foo\nSELECT 'GRANT DBA', q'[ALTER SYSTEM]', 'a@b' FROM DUAL;")
        self.assertEqual(result["findings"], [])
        self.assertTrue(analyze("ALTER /*comment*/ SYSTEM FLUSH SHARED_POOL;")["errors"])

    def test_plsql_recognized_slash_required(self):
        sql = "CREATE OR REPLACE EDITIONABLE FUNCTION DM_CP_TEST RETURN NUMBER AS BEGIN RETURN 1; END;\n/\n"
        self.assertEqual(analyze(sql)["sql_types"], ["FUNCTION"])
        self.assertTrue(analyze(sql)["plsql"])
        self.assertTrue(analyze(sql.replace("\n/\n", "\n"))["errors"])

    def test_dynamic_sql_always_requires_dba_review(self):
        result = analyze("BEGIN EXECUTE IMMEDIATE 'DROP TABLE DM_CP_CUSTOMER'; END;\n/\n")
        self.assertIn({"rule": "DYNAMIC_SQL", "level": "REQUIRES_DBA_REVIEW", "line": 1}, result["findings"])
        self.assertTrue(analyze("ALTER USER U IDENTIFIED BY X;")["errors"])
        self.assertTrue(analyze("GRANT CREATE ANY TABLE TO U;")["errors"])

    def test_empty_sql_and_policy_weakening_rejected(self):
        self.assertTrue(analyze("/*only comments*/")["errors"])
        policy = load_yaml(app_root() / "policies/sql-policy.yaml")
        policy["rules"]["GRANT_DBA"] = "WARNING"
        with self.assertRaises(DemoError):
            analyze("GRANT DBA TO USER;", policy)


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.output = Path(self.temp.name)
        self.envelope = build_release(HAPPY, self.output / "artifact", metadata=sample_metadata(), committed=False)
        self.fixture = json.loads((app_root() / "reports/fixtures/happy.json").read_text())

    def tearDown(self):
        self.temp.cleanup()

    def test_fixture_report_cannot_claim_runtime(self):
        evidence = collect(self.envelope, "FIXTURE", fixture=self.fixture)
        report = make_report(evidence)
        self.assertEqual(report["status"], "VERIFIED")
        self.assertFalse(report["runtime_proven"])
        self.assertEqual(report["runtime_result"], "NOT_AVAILABLE")
        text = render(report)
        for heading in ("Executive Summary", "Source Provenance", "Migration Files", "Static Validation", "Target Environments", "Review and Approval", "Execution Timeline", "Oracle Verification", "Environment Results", "Failure / Correction", "Audit Evidence", "Artifacts", "Final Decision"):
            self.assertIn("## " + heading, text)
        self.assertIn("SAMPLE / DEMO", text)

    def test_task_success_and_missing_errors_not_verified(self):
        actual = copy.deepcopy(self.fixture["environments"]["DEV"]["oracle"])
        actual["objects"][3]["status"] = "INVALID"
        self.assertEqual(assess(self.envelope["verification"], actual, "EXECUTION_SUCCEEDED")["verification"], "INVALID")
        actual = copy.deepcopy(self.fixture["environments"]["DEV"]["oracle"])
        actual.pop("errors")
        self.assertEqual(assess(self.envelope["verification"], actual, "EXECUTION_SUCCEEDED")["verification"], "INVALID")
        actual["errors"] = [{"attribute": "ERROR", "text": "PLS-00201"}]
        self.assertEqual(assess(self.envelope["verification"], actual, "EXECUTION_SUCCEEDED")["verification"], "INVALID")

    def test_wrong_rows_and_function_not_verified(self):
        for key, change in [("data", {"row_count": 2, "active_count": 2}), ("function", {"result": "wrong"})]:
            actual = copy.deepcopy(self.fixture["environments"]["DEV"]["oracle"])
            actual[key] = change
            self.assertEqual(assess(self.envelope["verification"], actual, "EXECUTION_SUCCEEDED")["verification"], "INVALID")

    def test_fixture_cannot_be_relabelled_live(self):
        with self.assertRaises(DemoError):
            collect(self.envelope, "LIVE", receipt=self.fixture)

    def test_unrelated_roles_and_requester_cannot_prove_approval(self):
        evidence = collect(self.envelope, "FIXTURE", fixture=self.fixture)
        for approval in evidence["approvals"]:
            approval["actor_roles"] = ["PARTICIPANT"]
        report = make_report(evidence)
        self.assertFalse(report["approval_evidence_complete"])
        self.assertEqual(report["status"], "PARTIAL")
        evidence = collect(self.envelope, "FIXTURE", fixture=self.fixture)
        evidence["requester_id"] = evidence["approvals"][0]["actor_id"]
        self.assertFalse(make_report(evidence)["approval_evidence_complete"])

    def test_forged_verified_flag_is_recomputed_from_oracle(self):
        evidence = collect(self.envelope, "FIXTURE", fixture=self.fixture)
        evidence["environments"]["DEV"]["oracle"]["objects"][0]["status"] = "INVALID"
        evidence["environments"]["DEV"]["verification"] = "VERIFIED"
        self.assertEqual(make_report(evidence)["status"], "INVALID")

    def test_not_available_does_not_imply_execution(self):
        report = make_report(collect(self.envelope, "NOT_AVAILABLE"))
        self.assertEqual(report["status"], "PARTIAL")
        self.assertFalse(report["runtime_proven"])

    def test_failure_stops_and_correction_has_new_hashes(self):
        failed = build_release(FAIL, self.output / "failed", metadata=sample_metadata(), committed=False)
        fixed = build_release(FIX, self.output / "fixed", metadata=sample_metadata(), committed=False)
        self.assertNotEqual(failed["sql_sha256"], fixed["sql_sha256"])
        self.assertEqual(fixed["corrects"], FAIL)
        fixture = json.loads((app_root() / "reports/fixtures/failure.json").read_text())
        report = make_report(collect(failed, "FIXTURE", fixture=fixture))
        self.assertEqual(report["status"], "EXECUTION_FAILED")
        self.assertEqual(report["environments"]["DEV"]["demo_status"], "VERIFIED")
        self.assertEqual(report["environments"]["SIT"]["demo_status"], "EXECUTION_FAILED")
        self.assertEqual(report["environments"]["UAT"]["native_status"], "WAIT_FOR_EXECUTION")
        self.assertEqual(report["environments"]["MOCKPROD"]["native_status"], "WAIT_FOR_EXECUTION")

    def test_secret_redaction_drops_fields_and_masks_embedded_values(self):
        with patch.dict(os.environ, {"ODC_PASSWORD": "synthetic-secret-value"}):
            cleaned = sanitize({"password": "synthetic-secret-value", "cookies": ["cookie"],
                                "Authorization": "Bearer abcdefghijklmnopqrstuvwxyz", "nested": {"access_token": "abc", "actor": "reviewer"},
                                "message": "synthetic-secret-value https://alice:pass@host/ token=abc"})
        serialized = json.dumps(cleaned)
        self.assertNotIn("synthetic-secret-value", serialized)
        self.assertNotIn("alice:pass", serialized)
        self.assertNotIn("access_token", serialized)
        self.assertNotIn("Authorization", serialized)
        self.assertEqual(cleaned["nested"]["actor"], "reviewer")


class IntegrationBoundaryTests(unittest.TestCase):
    def test_client_exposes_no_approval_or_executor(self):
        for name in ("approve", "execute", "continue_batch", "rollback"):
            self.assertFalse(hasattr(ODCClient, name))

    def test_query_api_refuses_non_allowlisted_or_write_sql(self):
        client = ODCClient("https://odc.example.invalid", "demo", "synthetic-secret")
        for db, sql in [(999, "SELECT 1 FROM DUAL"), (1000069, "DROP TABLE DM_CP_CUSTOMER"), (1000069, "SELECT 1 FROM DUAL; DELETE FROM X")]:
            with self.assertRaises(DemoError):
                client.read_only_sql(db, sql)

    def test_live_fixture_change_and_wrong_inventory_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            envelope = build_release(HAPPY, Path(temp) / "artifact", metadata=sample_metadata(), committed=False)
            client = ODCClient("https://odc.example.invalid", "demo", "synthetic-secret")
            client.inventory = Mock()
            with self.assertRaises(DemoError):
                client.create_change(envelope, (Path(temp) / "artifact/release-bundle/migration.sql").read_text())
            client.inventory = ODCClient.inventory.__get__(client)
            client.request = Mock(return_value={"id": 1000069, "name": "PRODUCTION", "dataSource": {"id": 1000001}, "project": {"id": 1}})
            with self.assertRaises(DemoError):
                client.inventory(envelope["targets"])

    def test_native_create_is_manual_ordered_and_never_executes(self):
        with tempfile.TemporaryDirectory() as temp:
            env = build_release(HAPPY, Path(temp) / "artifact", metadata=sample_metadata(), committed=False)
            env["evidence_source"] = "GIT"
            client = ODCClient("https://odc.example.invalid", "demo", "synthetic-secret")
            client.inventory = Mock()
            client.request = Mock(return_value={"contents": [{"id": 42}]})
            sql = (Path(temp) / "artifact/release-bundle/migration.sql").read_text()
            self.assertEqual(client.create_change(env, sql), 42)
            payload = client.request.call_args.kwargs["payload"]
            self.assertEqual(payload["executionStrategy"], "MANUAL")
            self.assertEqual(payload["parameters"]["orderedDatabaseIds"], [[1000069], [1000122], [1000184], [1000218]])
            self.assertEqual(payload["parameters"]["retryTimes"], 0)
            self.assertEqual(payload["parameters"]["errorStrategy"], "ABORT")
            self.assertEqual(client.request.call_count, 1)
            self.assertNotIn("execute", client.request.call_args.args[1])

    def test_changed_sql_fails_before_any_request(self):
        with tempfile.TemporaryDirectory() as temp:
            env = build_release(HAPPY, Path(temp) / "artifact", metadata=sample_metadata(), committed=False)
            env["evidence_source"] = "GIT"
            client = ODCClient("https://odc.example.invalid", "demo", "synthetic-secret")
            client.inventory = Mock()
            client.request = Mock()
            with self.assertRaises(DemoError):
                client.create_change(env, "ALTER SYSTEM SHUTDOWN;")
            client.inventory.assert_not_called()
            client.request.assert_not_called()

    def test_wrong_native_environment_rejected(self):
        target = environments()["DEV"]
        client = ODCClient("https://odc.example.invalid", "demo", "synthetic-secret")
        client.request = Mock(return_value={"id": target["odc_target_id"], "name": target["schema"],
                                           "dataSource": {"id": target["odc_datasource_id"]}, "project": {"id": 1},
                                           "environment": {"id": 2, "name": "sit"}})
        with self.assertRaises(DemoError):
            client.inventory([target])

    def test_receipt_run_binding_and_string_audit_task_id(self):
        with tempfile.TemporaryDirectory() as temp:
            envelope = build_release(HAPPY, Path(temp) / "artifact", metadata=sample_metadata(), committed=False)
            sql = (Path(temp) / "artifact/release-bundle/migration.sql").read_text()
            description = f"app={envelope['application']};release={HAPPY};git={envelope['git_commit']};github_run={envelope['github_run_id']};sql_sha256={envelope['sql_sha256']}"
            detail = {"type": "MULTIPLE_ASYNC", "parameters": {"orderedDatabaseIds": [[t["odc_target_id"]] for t in envelope["targets"]], "sqlContent": sql}, "description": description,
                      "nodeList": [], "status": "APPROVING", "creator": {"id": 1}}
            client = ODCClient("https://odc.example.invalid", "demo", "synthetic-secret")
            client.ticket = Mock(return_value=detail)
            client.request = Mock(side_effect=[{"contents": []}, {"contents": [{"id": 7, "taskId": "42", "action": "EXECUTE_MULTIPLE_ASYNC_TASK"}]}])
            receipt = client.collect(42, envelope)
            self.assertEqual(receipt["audit_events"][0]["id"], 7)
            detail["description"] = description.replace("github_run=NOT_AVAILABLE", "github_run=OTHER_RUN")
            client.request.reset_mock()
            with self.assertRaises(DemoError):
                client.collect(42, envelope)
            client.request.assert_not_called()

    def test_waiting_native_targets_skip_oracle_queries(self):
        with tempfile.TemporaryDirectory() as temp:
            env = build_release(HAPPY, Path(temp) / "artifact", metadata=sample_metadata(), committed=False)
            client = Mock()
            receipt = {"evidence_source": "LIVE", "git_commit": env["git_commit"], "sql_sha256": env["sql_sha256"],
                       "environments": {name: {"native_status": "WAIT_FOR_EXECUTION"} for name in ENVIRONMENTS}}
            result = verify_live(client, env, receipt)
            client.read_only_sql.assert_not_called()
            self.assertTrue(all(r["verification"] == "NOT_AVAILABLE" for r in result["environments"].values()))


if __name__ == "__main__":
    unittest.main()
