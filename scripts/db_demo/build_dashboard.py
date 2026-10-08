"""Build two standalone, offline HTML views from sanitized migration evidence.

No ODC/Oracle connection, approval, execution, or runtime acceptance is performed.
Optional --refresh-github reads PR/workflow/artifact metadata with the local gh CLI.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
DASHBOARD = ROOT / "demo/dashboard"
DEFAULT_EVIDENCE = ROOT / "evidence/visual-migration-poc-20261008/inputs"
ORDER = ("DEV", "SIT", "UAT", "MOCKPROD")
CHECKS = ("Table", "Sequence", "Index", "Function", "View", "USER_ERRORS", "Seed data", "Function test")
REPO = "devsecopslonghn/DB-Research"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def gh(*args):
    return json.loads(subprocess.check_output(["gh", *args], text=True))


def refresh_github(directory):
    """Refresh the implementation PR's evidence, not arbitrary newest runs."""
    pr = gh("api", f"repos/{REPO}/pulls/1")
    workflows = {}
    for key, commit, name in (("db_validate", pr["head"]["sha"], "DB migration validation"),
                              ("db_report", pr["head"]["sha"], "DB migration report"),
                              ("codeql", pr["merge_commit_sha"], "CodeQL")):
        runs = gh("api", f"repos/{REPO}/actions/runs?head_sha={commit}&per_page=100")["workflow_runs"]
        matches = [r for r in runs if r["name"] == name or (key == "codeql" and "codeql" in r.get("path", "").lower())]
        if not matches:
            workflows[key] = {"conclusion": "NOT_AVAILABLE"}
            continue
        run = matches[0]
        workflows[key] = {k: run.get(k) for k in ("id", "conclusion", "status", "head_sha", "html_url", "created_at")}
        workflows[key]["artifacts"] = [{k: a.get(k) for k in ("id", "name", "expired", "digest")}
                                       for a in gh("api", f"repos/{REPO}/actions/runs/{run['id']}/artifacts")["artifacts"]]
        if key == "db_validate" and run["conclusion"] == "success":
            log = subprocess.check_output(["gh", "run", "view", str(run["id"]), "--repo", REPO, "--log"], text=True)
            counts = re.findall(r"Ran (\d+) tests in", log)
            workflows[key]["test_count"] = int(counts[-1]) if counts else None
    state = {"evidence_source": "LIVE", "observed_at": datetime.now(timezone.utc).isoformat(),
             "main_sha": gh("api", f"repos/{REPO}/commits/main")["sha"], "latest_workflows": workflows,
             "pr": {"number": pr["number"], "html_url": pr["html_url"], "merged": pr["merged"],
                    "merged_at": pr["merged_at"], "state": pr["state"], "head_sha": pr["head"]["sha"],
                    "merge_commit": pr["merge_commit_sha"]}}
    write(directory / "github-current-state.json", state)


def oracle_checks(record, target, contract):
    """Never infer Oracle acceptance from an ODC success status alone."""
    oracle = record.get("oracle") or {}
    native = record.get("native_status")
    if native in ("WAIT_FOR_EXECUTION", "CREATED", "APPROVING", "WAIT_FOR_APPROVAL"):
        return dict.fromkeys(CHECKS, "NOT RUN")
    if (native != "EXECUTION_SUCCEEDED" or oracle.get("query_status") != "SUCCESS"
            or oracle.get("environment") != target["environment"]
            or oracle.get("database_id") != target["odc_target_id"]
            or oracle.get("schema") != target["schema"] or not oracle.get("observed_at")):
        return dict.fromkeys(CHECKS, "NOT AVAILABLE")
    objects = {(o.get("name"), o.get("type")): o.get("status") for o in oracle.get("objects", [])}
    checks = {}
    for name, kind in zip(CHECKS[:5], ("TABLE", "SEQUENCE", "INDEX", "FUNCTION", "VIEW")):
        expected = [o for o in contract["objects"] if o["type"] == kind]
        checks[name] = ("NOT AVAILABLE" if "objects" not in oracle else
                        "PASS" if expected and all(objects.get((o["name"], kind)) == "VALID" for o in expected) else "FAIL")
    checks["USER_ERRORS"] = "NOT AVAILABLE" if "errors" not in oracle else "PASS" if oracle["errors"] == [] else "FAIL"
    checks["Seed data"] = ("NOT AVAILABLE" if not all(k in oracle.get("data", {}) for k in ("row_count", "active_count")) else
                           "PASS" if all(oracle["data"][k] == contract["data"][k] for k in ("row_count", "active_count")) else "FAIL")
    checks["Function test"] = ("NOT AVAILABLE" if "result" not in oracle.get("function", {}) else
                               "PASS" if oracle["function"]["result"] == contract["function"]["expected"] else "FAIL")
    return checks


def environment(record, target, contract, source):
    checks = oracle_checks(record, target, contract)
    native = record.get("native_status", "NOT_AVAILABLE")
    if native == "EXECUTION_FAILED":
        status = "FAILED"
    elif native == "EXECUTION_SUCCEEDED":
        status = "VERIFIED" if all(v == "PASS" for v in checks.values()) else "INVALID" if "FAIL" in checks.values() else "PARTIAL"
    elif native in ("EXECUTING", "RUNNING"):
        status = "EXECUTING"
    else:
        status = "WAITING"
    return {"name": target["environment"], "target": target["odc_target_id"], "schema": target["schema"],
            "status": status, "native_status": native, "source": source,
            "verification": "PASS" if status == "VERIFIED" else "FAIL" if "FAIL" in checks.values() else "NOT_AVAILABLE",
            "verification_source": source if any(v in ("PASS", "FAIL") for v in checks.values()) else "NOT_AVAILABLE",
            "start": record.get("execution_start", record.get("start")), "end": record.get("execution_end", record.get("end")),
            "actor": record.get("execution_actor", "NOT_AVAILABLE"), "checks": checks}


def build_data(directory):
    report = read(directory / "REL-2026.10-DEMO01/migration-report.json")
    receipt = read(directory / "happy-odc-receipt.json")
    envelope = report["envelope"]
    if report.get("sample") or report["evidence_source"] == "FIXTURE" or receipt["evidence_source"] != "LIVE":
        raise ValueError("Current release must use a real ODC receipt and a non-fixture report")
    if receipt["odc_batch_id"] != report["odc_batch_id"]:
        raise ValueError("Report and ODC receipt batch identities differ")
    if (receipt["release_id"] != envelope["release_id"] or receipt["git_commit"] != envelope["git_commit"]
            or receipt["sql_sha256"] != envelope["sql_sha256"]):
        raise ValueError("Report and live receipt source provenance differ")
    if report.get("native_parent_status") != receipt["native_status"]:
        raise ValueError("Refresh report and receipt together; native batch states differ")
    for name in ORDER:
        if (report["environments"][name]["native_status"] != receipt["environments"][name]["native_status"]
                or receipt["environments"][name].get("ticket_id") != report["odc_batch_id"]):
            raise ValueError(f"Report and receipt stage observations differ: {name}")
    # Ensure the displayed reviewed migrations still match the repository.
    files = []
    for item in envelope["migrations"]:
        path = ROOT / f"demo/customer-profile/migrations/{envelope['release_id']}/{item['file']}"
        if sha(path) != item["sha256"]:
            raise ValueError(f"Reviewed SQL hash mismatch: {item['file']}")
        files.append({"file": item["file"], "type": ", ".join(item["sql_types"]), "sha256": item["sha256"],
                      "policy": "PASS" if not item["errors"] else "FAIL", "path": path.relative_to(ROOT).as_posix()})
    manifest = ROOT / f"demo/customer-profile/migrations/{envelope['release_id']}/manifest.yaml"
    if sha(manifest) != envelope["manifest_sha256"]:
        raise ValueError("Reviewed manifest hash mismatch")
    targets = {t["environment"]: t for t in envelope["targets"]}
    stages = [environment(report["environments"][n], targets[n], envelope["verification"], "LIVE") for n in ORDER]
    states = [s["status"] for s in stages]
    native = report.get("native_parent_status", receipt["native_status"])
    status = ("CORRECTION_REQUIRED" if "FAILED" in states else "FAILED" if "INVALID" in states
              else "WAITING_APPROVAL" if native in ("APPROVING", "WAIT_FOR_APPROVAL", "CREATED")
              else "VERIFIED" if all(s == "VERIFIED" for s in states) and report.get("runtime_proven")
              else "IN_PROGRESS" if "EXECUTING" in states else "PARTIAL")
    approval_state = read(directory / "happy-batch-approval-state.json")
    if (approval_state.get("evidence_source") != "LIVE" or approval_state.get("batch_id") != report["odc_batch_id"]
            or approval_state.get("native_status") != native):
        raise ValueError("Native approval snapshot must match the live batch receipt")
    nodes = [n for n in approval_state["nodes"] if n["node_type"] == "APPROVAL_TASK"]
    requester = next((n.get("operator", {}).get("accountName") for n in approval_state["nodes"]
                      if n.get("operator", {}).get("id") == report["requester_id"]), "Actor name not available")
    approvals = [{"role": "Requester", "actor": requester, "status": "SUBMITTED", "source": "LIVE",
                  "detail": f"ODC requester ID {report['requester_id']}"}]
    for index, role in enumerate(("OWNER review", "DBA approval")):
        node = nodes[index] if index < len(nodes) else {}
        # Candidate/operator fields do not prove a completed independent approval.
        approval = next((a for a in report.get("approvals", []) if a.get("node_id") == node.get("node_id")
                         and role.split()[0] in a.get("actor_roles", [])), {})
        complete = (node.get("native_status") == "COMPLETED" and node.get("complete_time")
                    and approval.get("timestamp") and approval.get("actor_id") != report["requester_id"]
                    and report.get("approval_evidence_complete"))
        approvals.append({"role": role, "actor": approval.get("actor") if complete else "Pending",
                          "status": "APPROVED" if complete else "PENDING", "source": "LIVE" if node else "NOT_AVAILABLE",
                          "detail": f"Node {node.get('node_id', 'unavailable')} · native {node.get('native_status', 'NOT_AVAILABLE')}; role assignment not proven" if not complete else "Completed independent approval"})
    approvals.append({"role": "Execution", "actor": "Authorized operator", "status": "WAITING" if all(s == "WAITING" for s in states) else status,
                      "source": "LIVE", "detail": "Manual continuation in ODC after approval and stage verification"})
    approval_complete = all(a["status"] == "APPROVED" for a in approvals[1:3])
    if status == "VERIFIED" and not approval_complete:
        status = "PARTIAL"
    runtime_proven = status == "VERIFIED" and bool(report.get("runtime_proven"))
    github = read(directory / "github-current-state.json")
    verified = read(directory / "github-artifacts-verified.json")
    workflows = []
    for key, name, scope in (("db_validate", "db-validate", "Static validation, tests and release packages"),
                             ("db_report", "db-report", "Fixture report rendering; no live execution"),
                             ("codeql", "CodeQL", "Code scanning on the merge commit")):
        run = github["latest_workflows"][key]
        workflows.append({"name": name, "status": "PASS" if run["conclusion"] == "success" else run["conclusion"].upper(),
                          "run": run.get("id"), "commit": run.get("head_sha"), "url": run.get("html_url"), "scope": scope,
                          "source": "LIVE", "artifacts": run.get("artifacts", [])})
    retention = read(directory / "retention-conclusion.json")
    current_retention = read(directory / "retention-current-state.json")
    retained = {label: retention[key] for label, key in (("Result", "result_retention"), ("Log", "log_retention"),
                ("Attachment", "attachment_retention"), ("Metadata", "metadata_sql_approvals_audit_retention"),
                ("Audit", "metadata_sql_approvals_audit_retention"))}
    fixtures = {}
    for name, release in (("expected", "REL-2026.10-DEMO01"), ("failure", "REL-2026.10-DEMO02-FAIL"), ("correction", "REL-2026.10-DEMO02-FIX")):
        fixture = read(ROOT / f"demo/customer-profile/reports/fixtures/{'happy' if name == 'expected' else name}.json")
        contract = envelope["verification"] if name == "expected" else read(directory / release / "migration-report.json")["envelope"]["verification"]
        fixtures[name] = {"release": release, "source": "FIXTURE", "batch": fixture["odc_batch_id"],
                          "environments": [environment(fixture["environments"][n], targets[n], contract, "FIXTURE") for n in ORDER]}
    fail_envelope = read(directory / "REL-2026.10-DEMO02-FAIL/migration-report.json")["envelope"]
    fix_envelope = read(directory / "REL-2026.10-DEMO02-FIX/migration-report.json")["envelope"]
    if fix_envelope["corrects"] != fail_envelope["release_id"] or fix_envelope["sql_sha256"] == fail_envelope["sql_sha256"]:
        raise ValueError("Correction must reference the preserved failure and have new SQL hashes")
    chain = [{"title": title, "source": source, "detail": detail} for title, source, detail in (
        ("Git commit", "LIVE", envelope["git_commit"][:12]), ("Release manifest", "LIVE", envelope["manifest_sha256"][:12]),
        ("Migration SHA-256", "LIVE", envelope["sql_sha256"][:12]), ("ODC batch", "LIVE", str(report["odc_batch_id"])),
        ("Approval", "LIVE", "Incomplete approval nodes observed" if not report["approval_evidence_complete"] else "Independent approval evidence"),
        ("Execution", "NOT_AVAILABLE" if all(s == "WAITING" for s in states) else "LIVE", "No execution yet" if all(s == "WAITING" for s in states) else status),
        ("Oracle verification", "NOT_AVAILABLE" if all(s["verification_source"] == "NOT_AVAILABLE" for s in stages) else "LIVE", "Post-migration acceptance required"),
        ("Report", "LIVE", "Generated snapshot; runtime result unavailable" if not runtime_proven else "Generated verified result"))]
    if not directory.is_relative_to(ROOT):
        raise ValueError("Store sanitized evidence inside this repository so offline source links remain portable")
    sources = [{"file": p.relative_to(ROOT).as_posix(), "sha256": sha(p)}
               for p in sorted(directory.rglob("*.json"))]
    return {"schema_version": 1, "generated_at": datetime.now(timezone.utc).isoformat(), "observed_at": report["collected_at"],
            "application": envelope["application"], "release": envelope["release_id"], "repository": REPO, "source": "GitHub",
            "odc_batch": str(report["odc_batch_id"]), "native_status": native, "overall_status": status,
            "happy_path": "LIVE" if runtime_proven else "PARTIAL", "runtime_proven": runtime_proven,
            "active_environment": next((s["name"] for s in stages if s["status"] == "EXECUTING"), None),
            "approval_complete": approval_complete,
            "evidence_directory": directory.relative_to(ROOT).as_posix(),
            "environments": stages, "approvals": approvals, "files": files, "fixtures": fixtures, "chain": chain,
            "provenance": {"source_commit": envelope["git_commit"], "pr_head": github["pr"]["head_sha"],
                           "merge_commit": github["pr"]["merge_commit"], "manifest_sha256": envelope["manifest_sha256"],
                           "sql_sha256": envelope["sql_sha256"], "github_run": envelope["github_run_id"], "package_origin": "LOCAL_OPERATOR"},
            "github": {"pr": github["pr"], "observed_at": github["observed_at"], "workflows": workflows,
                       "tests": github["latest_workflows"]["db_validate"].get("test_count"),
                       "package_status": "PASS" if verified["all_bundles_verified_against_committed_source"] else "FAIL",
                       "artifact_id": verified["artifact_id"], "artifact_run": verified["workflow_run_id"]},
            "retention": {"status": "PASS" if all(v == "PASS" for v in retained.values()) else "FAIL", "source": "LIVE",
                          "tickets": retention["tickets"], "observed_at": retention["timestamp"], "checks": retained,
                          "configuration": current_retention["retention_configuration"], "configuration_observed_at": current_retention["observed_at"],
                          "hostname": current_retention["hostname"], "mount": "/opt/odc/log", "identity": "Stable ODC service identity"},
            "correction": {"failed_release": fail_envelope["release_id"], "release": fix_envelope["release_id"],
                           "failed_sha256": fail_envelope["sql_sha256"], "sha256": fix_envelope["sql_sha256"], "source": "FIXTURE",
                           "policy": "Dynamic SQL requires DBA review", "live_status": "NOT_AVAILABLE — neither runtime ticket created"},
            "sources": sources,
            "limitations": [("OWNER/DBA approval and migration execution remain pending; Oracle preflight is not migration acceptance." if status == "WAITING_APPROVAL" else
                              "Oracle preflight is not migration acceptance; final verification requires complete independent approval, execution and Oracle evidence."),
                            "db-report Actions success proves fixture rendering. Authenticated Actions-to-ODC handoff still needs runner, environment, secrets and original handoff artifact.",
                            "DEV, SIT, UAT and MOCKPROD are four isolated schemas on one Oracle service. MOCKPROD is a simulation environment.",
                            "Failure and correction runtime have not been executed. Their visual demonstrations use repository fixtures.",
                            "ODC manual continuation requires an authorized operator; ABORT/retry 0 is not an automatic approval or Oracle verification gate.",
                            "Static SQL policy is lexical. ODC does not provide Flyway-style migration version ledger/replay, DDL rollback, backup or production readiness."]}


def safe_json(value):
    # Script data cannot close its containing tag or introduce executable markup.
    return json.dumps(value, ensure_ascii=True).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-dir", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--refresh-github", action="store_true")
    args = parser.parse_args()
    directory = args.evidence_dir.resolve()
    if args.refresh_github:
        refresh_github(directory)
    data = build_data(directory)
    write(DASHBOARD / "data/demo-status.json", data)
    css = (DASHBOARD / "assets/dashboard.css").read_text()
    js = (DASHBOARD / "assets/dashboard.js").read_text()
    for mode, filename in (("dashboard", "index.html"), ("report", "migration-report.html")):
        template = (DASHBOARD / "assets/page.template.html").read_text()
        html = template.replace("@@MODE@@", mode).replace("@@TITLE@@", "Database Migration POC" if mode == "dashboard" else "Database Migration Report")
        html = html.replace("@@CSS@@", css).replace("@@DATA@@", safe_json(data)).replace("@@JS@@", js)
        (DASHBOARD / filename).write_text(html, encoding="utf-8")
    print(f"Dashboard + report built: {data['release']} / {data['overall_status']} / ODC {data['odc_batch']}; happy {data['happy_path']}")


if __name__ == "__main__":
    main()
