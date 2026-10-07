"""Render management/audit Markdown and JSON; retain native and derived states separately."""
import argparse
import json
from pathlib import Path
import re

from .common import DemoError, ENVIRONMENTS, STATES, fail_cli, sanitize, summary, table_cell, write_json
from .verify_oracle import assess


def environment_state(record, parent_status=None):
    native = record["native_status"]
    if native == "EXECUTION_FAILED":
        return "EXECUTION_FAILED"
    if native == "EXECUTION_SUCCEEDED":
        if record["verification"] == "VERIFIED":
            return "VERIFIED"
        return "INVALID" if record["verification"] == "INVALID" else "VERIFYING"
    if native in ("APPROVING", "WAIT_FOR_APPROVAL", "CREATED"):
        return "WAITING_APPROVAL"
    if native in ("EXECUTING", "RUNNING"):
        return "EXECUTING"
    if native in ("WAIT_FOR_EXECUTION", "APPROVED"):
        # Native child tasks already wait for execution while the parent is
        # still in precheck/approval. That does not prove human approval.
        if parent_status in ("APPROVING", "WAIT_FOR_APPROVAL", "CREATED"):
            return "WAITING_APPROVAL"
        if parent_status == "PRE_CHECK_EXECUTING":
            return "PARTIAL"
        return "APPROVED"
    return "PARTIAL"


def make_report(evidence):
    if evidence.get("schema_version") != 1 or evidence.get("evidence_source") not in ("LIVE", "FIXTURE", "NOT_AVAILABLE"):
        raise DemoError("Unsupported evidence schema/source")
    if set(evidence.get("environments", {})) != set(ENVIRONMENTS):
        raise DemoError("Report requires all four environments")
    report = sanitize(evidence)
    for record in report["environments"].values():
        if record.get("oracle", {}).get("query_status") is not None:
            record.update(assess(report["envelope"]["verification"], record["oracle"], record["native_status"]))
        else:
            record["verification"] = "NOT_AVAILABLE"
        record["demo_status"] = environment_state(record, report.get("native_parent_status"))
    states = [r["demo_status"] for r in report["environments"].values()]
    if "EXECUTION_FAILED" in states:
        result = "EXECUTION_FAILED"
    elif "INVALID" in states:
        result = "INVALID"
    elif all(s == "VERIFIED" for s in states):
        result = "VERIFIED"
    elif report.get("native_parent_status") in ("APPROVING", "WAIT_FOR_APPROVAL", "CREATED"):
        result = "WAITING_APPROVAL"
    elif "EXECUTING" in states:
        result = "EXECUTING"
    elif "VERIFYING" in states:
        result = "VERIFYING"
    else:
        result = "PARTIAL"
    report["status"] = result
    owners, dbas = set(), set()
    for approval in report.get("approvals", []):
        actor = approval.get("actor_id") or approval.get("actor")
        roles = approval.get("actor_roles") or []
        if approval.get("native_status") != "COMPLETED" or not actor or actor == report.get("requester_id"):
            continue
        if "OWNER" in roles:
            owners.add(actor)
        if "DBA" in roles:
            dbas.add(actor)
    report["approval_evidence_complete"] = any(owner != dba for owner in owners for dba in dbas)
    if result == "VERIFIED" and not report["approval_evidence_complete"]:
        report["status"] = result = "PARTIAL"
    report["runtime_proven"] = report["evidence_source"] == "LIVE" and result == "VERIFIED" and report["approval_evidence_complete"]
    report["runtime_result"] = result if report["evidence_source"] == "LIVE" else "NOT_AVAILABLE"
    report["decision"] = "GO" if report["runtime_proven"] and report.get("retention_status") == "VERIFIED" else "CONDITIONAL GO"
    report["next_action"] = "CORRECTION_REQUIRED" if result in ("EXECUTION_FAILED", "INVALID") else "REVIEW_EVIDENCE"
    report["result_scope"] = "SAMPLE / DEMO — fixture simulation" if report["evidence_source"] == "FIXTURE" else report["evidence_source"]
    return report


def render(report):
    envelope = report["envelope"]
    lines = ["# Database Migration Report", "", "## Executive Summary", "",
             f"Evidence source: **{report['evidence_source']}**. Scope: **{report['result_scope']}**.", "",
             f"Derived result: **{report['status']}**. Runtime result: **{report['runtime_result']}**. Runtime-proven complete migration: **{report['runtime_proven']}**.", "",
             "ODC execution success alone is insufficient; every environment also needs valid objects, no compilation errors, expected rows and function result.", "",
             "## Application / Release", "", f"Application: `{envelope['application']}`  ", f"Release: `{envelope['release_id']}`  ",
             f"Collected: {report['collected_at']}", "", "## Source Provenance", "",
             f"Repository: `{envelope['git_repository']}`  ", f"Branch: `{envelope['git_branch']}`  ",
             f"Git commit: `{envelope['git_commit']}`  ", f"GitHub actor: `{envelope['github_actor']}`  ",
             f"GitHub run: `{envelope['github_run_id']}`  ", f"Manifest SHA-256: `{envelope['manifest_sha256']}`  ",
             f"Ordered SQL SHA-256: `{envelope['sql_sha256']}`", "", "## Migration Files", "",
             "| File | SHA-256 | Type | Static status |", "| --- | --- | --- | --- |"]
    for migration in envelope["migrations"]:
        lines.append("| " + " | ".join(table_cell(v) for v in [migration["file"], migration["sha256"], ", ".join(migration["sql_types"]), "INVALID" if migration["errors"] else "VALIDATED"]) + " |")
    lines += ["", "## Static Validation", "", "| File | Level | Pattern | Line |", "| --- | --- | --- | --- |"]
    findings = [(m["file"], f) for m in envelope["migrations"] for f in m["findings"]]
    for name, finding in findings:
        lines.append(f"| {table_cell(name)} | {finding['level']} | {finding['rule']} | {finding['line']} |")
    if not findings:
        lines.append("| All migration files | INFO | No listed dangerous pattern | — |")
    lines += ["", "Lexical analysis is not a complete Oracle parser. Dynamic SQL and dependencies require DBA review.", "",
              "## Target Environments", "", "| Environment | ODC database | Datasource | Owner schema |", "| --- | --- | --- | --- |"]
    for target in envelope["targets"]:
        lines.append(f"| {target['environment']} | {target['odc_target_id']} | {target['odc_datasource_id']} | {target['schema']} |")
    lines += ["", "All four owner schemas are isolated logical environments on one Oracle service; MOCKPROD is a lab schema.", "",
              "## Review and Approval", "", "| Node | Actor | Native status | Timestamp |", "| --- | --- | --- | --- |"]
    for approval in report["approvals"]:
        lines.append("| " + " | ".join(table_cell(approval.get(k)) for k in ("node_id", "actor", "native_status", "timestamp")) + " |")
    if not report["approvals"]:
        lines.append("| NOT_AVAILABLE | NOT_AVAILABLE | NOT_AVAILABLE | NOT_AVAILABLE |")
    lines += ["", "OWNER and DBA approve in ODC. Automation has no approval or Execute operation. Native manual continuation remains an operator decision.", "",
              "## Execution Timeline", "", "| Environment | Flow created | Execution start | Flow complete | Execution actor |", "| --- | --- | --- | --- | --- |"]
    for name in ENVIRONMENTS:
        record = report["environments"][name]
        lines.append("| " + " | ".join(table_cell(v) for v in [name, record.get("flow_created_at"), record.get("execution_start"), record.get("execution_end"), record.get("execution_actor")]) + " |")
    lines += ["", "Task-node operator may identify the requester; the Execute audit is the authority for the caller. Uncollected timestamps/actors remain NOT_AVAILABLE.", "",
              "## Oracle Verification", "", "| Environment | Object | Type | Status | Errors |", "| --- | --- | --- | --- | --- |"]
    for name in ENVIRONMENTS:
        record = report["environments"][name]
        oracle = record["oracle"]
        for obj in oracle.get("objects", []):
            errors = [e for e in oracle.get("errors", []) if e.get("name") == obj["name"]]
            lines.append("| " + " | ".join(table_cell(v) for v in [name, obj["name"], obj["type"], obj["status"], "; ".join(e.get("text", "ERROR") for e in errors) or "0"]) + " |")
        if not oracle.get("objects"):
            lines.append(f"| {name} | NOT_AVAILABLE | NOT_AVAILABLE | NOT_AVAILABLE | NOT_AVAILABLE |")
    lines += ["", "| Environment | Rows: expected / actual | Active: expected / actual | Function: expected / actual |", "| --- | --- | --- | --- |"]
    for name in ENVIRONMENTS:
        record = report["environments"][name]
        actual = record["oracle"]
        lines.append("| " + " | ".join(table_cell(v) for v in [name, f"3 / {actual.get('data', {}).get('row_count', 'NOT_AVAILABLE')}", f"2 / {actual.get('data', {}).get('active_count', 'NOT_AVAILABLE')}", f"{envelope['verification']['function']['expected']} / {actual.get('function', {}).get('result', 'NOT_AVAILABLE')}"]) + " |")
    lines += ["", "## Environment Results", "", "| Environment | ODC Ticket/Task | Native execution | Oracle verify | Demo result |", "| --- | --- | --- | --- | --- |"]
    for name in ENVIRONMENTS:
        record = report["environments"][name]
        lines.append("| " + " | ".join(table_cell(v) for v in [name, record["ticket_id"], record["native_status"], record["verification"], record["demo_status"]]) + " |")
    lines += ["", "## Failure / Correction", "", f"Corrects: `{envelope.get('corrects') or 'NOT_APPLICABLE'}`. Depends on: `{envelope.get('depends_on') or 'NOT_APPLICABLE'}`.", "",
              "The failure release raises ORA-20042 in SIT before index creation. UAT/MOCKPROD wait. Review/cancel the failed batch, then approve a new correction release; preserve old SQL, hashes, approvals and failure history. Already committed DDL is not automatically rolled back.", "",
              "## Audit Evidence", "", f"Native batch: `{report.get('odc_batch_id') or 'NOT_AVAILABLE'}`. Audit collection: {report['audit_collection']}.", ""]
    lines += [f"- `{table_cell(ref)}`" for ref in report["audit_references"]] or ["No audit references collected."]
    lines += ["", "## Artifacts", "", "Release artifact: `release-envelope.json`, `release-bundle/`. Evidence: `evidence.json`. Reports: `migration-report.md`, `migration-report.json`.", "",
              "GitHub workflow run/artifact links are available when the envelope contains a real workflow run ID. Fixtures are never runtime proof.", "",
              "## Final Decision", "", f"**{report['decision']}** for the recorded scope. Live approval, rollout, verification and the proven retention GitOps settings are required before claiming a working internal application pilot.", "",
              "Operational effort is NOT_MEASURED unless captured by an operator. No custom execution platform, direct Oracle migration executor or automatic promotion controller is introduced.", ""]
    repo = envelope.get("git_repository", "")
    if re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        commit = envelope.get("git_commit", "")
        if re.fullmatch(r"[0-9a-f]{40}", commit) and commit != "0" * 40:
            lines += [f"Source: [Git commit](https://github.com/{repo}/commit/{commit}).", ""]
        run = str(envelope.get("github_run_id", ""))
        if run.isdigit():
            lines += [f"Artifacts and logs: [GitHub Actions run](https://github.com/{repo}/actions/runs/{run}).", ""]
    return "\n".join(line.rstrip() + (chr(92) if line.endswith("  ") else "") for line in lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = make_report(json.loads(args.evidence.read_text()))
        write_json(args.output / "migration-report.json", report)
        text = render(report)
        (args.output / "migration-report.md").write_text(text, encoding="utf-8")
        summary(text)
        print(f"Report: {report['status']}; evidence={report['evidence_source']}; runtime_proven={report['runtime_proven']}")
    except (DemoError, OSError, ValueError, KeyError) as exc:
        fail_cli(exc)


if __name__ == "__main__":
    main()
