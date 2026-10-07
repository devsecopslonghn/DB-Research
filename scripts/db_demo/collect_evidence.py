"""Project available provenance and ODC/Oracle evidence without retaining raw responses."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

from .build_release import verify_bundle
from .common import DemoError, ENVIRONMENTS, ROOT, app_root, fail_cli, sanitize, write_json
from .verify_oracle import assess

FIXTURES = {"REL-2026.10-DEMO01": "happy.json", "REL-2026.10-DEMO02-FAIL": "failure.json",
            "REL-2026.10-DEMO02-FIX": "correction.json"}


def collect(envelope, source, receipt=None, verification=None, fixture=None):
    if source not in ("LIVE", "FIXTURE", "NOT_AVAILABLE"):
        raise DemoError("Evidence source must be explicit")
    if source == "FIXTURE":
        if fixture is None or fixture.get("evidence_source") != "FIXTURE" or fixture.get("release_id") != envelope["release_id"]:
            raise DemoError("Fixture source/release does not match")
        receipt = fixture
    elif source == "LIVE":
        if receipt is None or receipt.get("evidence_source") != "LIVE" or receipt.get("release_id") != envelope["release_id"] or receipt.get("git_commit") != envelope["git_commit"] or receipt.get("sql_sha256") != envelope["sql_sha256"]:
            raise DemoError("Live receipt release/commit/SQL hash does not match")
        if verification is not None and (verification.get("evidence_source") != "LIVE" or verification.get("release_id") != envelope["release_id"] or verification.get("git_commit") != envelope["git_commit"] or verification.get("sql_sha256") != envelope["sql_sha256"]):
            raise DemoError("Live verification provenance does not match")
    receipt = receipt or {}
    targets = {t["environment"]: t for t in envelope["targets"]}
    values = {}
    for name in ENVIRONMENTS:
        record = receipt.get("environments", {}).get(name, {})
        actual = (record.get("oracle") or {}) if source == "FIXTURE" else (verification or {}).get("environments", {}).get(name, {})
        native = record.get("native_status", "NOT_AVAILABLE")
        if source == "LIVE" and actual.get("query_status") is not None:
            target = targets[name]
            if actual.get("environment") != name or actual.get("database_id") != target["odc_target_id"] or actual.get("schema") != target["schema"]:
                raise DemoError("Oracle verification is not bound to the approved environment/database/schema")
        assessment = assess(envelope["verification"], actual, native) if actual.get("query_status") is not None else {"verification": "NOT_AVAILABLE", "problems": ["Oracle verification evidence has not been collected"]}
        values[name] = {"target": targets[name], "native_status": native, "ticket_id": record.get("ticket_id", receipt.get("odc_batch_id")),
                       "execution_start": record.get("start"), "execution_end": record.get("end"),
                       "flow_created_at": record.get("flow_created_at"),
                       "execution_actor": record.get("execution_actor", "NOT_AVAILABLE"),
                       "oracle": {k: actual[k] for k in ("environment", "database_id", "schema", "query_status", "observed_at", "objects", "errors", "data", "function") if k in actual},
                       **assessment}
    evidence = {"schema_version": 1, "evidence_source": source, "sample": source == "FIXTURE",
                "collected_at": datetime.now(timezone.utc).isoformat(), "envelope": envelope,
                "odc_batch_id": receipt.get("odc_batch_id"), "native_parent_status": receipt.get("native_status", "NOT_AVAILABLE"),
                "approvals": receipt.get("approvals", []), "environments": values,
                "requester_id": receipt.get("requester_id"),
                "audit_references": receipt.get("audit_references", []), "audit_collection": receipt.get("audit_collection", "NOT_AVAILABLE"),
                "audit_events": receipt.get("audit_events", []), "retention_status": "NOT_CHECKED",
                "collection_errors": receipt.get("collection_errors", []),
                "operational_effort": {"manual_actions": "NOT_MEASURED", "approvals": "NOT_MEASURED", "time_per_environment": "NOT_MEASURED",
                                       "total_release_time": "NOT_MEASURED", "credentials_handled": "NOT_MEASURED", "systems_used": "NOT_MEASURED"}}
    return sanitize(evidence)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--source", choices=("LIVE", "FIXTURE", "NOT_AVAILABLE"), required=True)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--verification", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        envelope = verify_bundle(args.bundle)
        receipt = json.loads(args.receipt.read_text()) if args.receipt else None
        verification = json.loads(args.verification.read_text()) if args.verification else None
        fixture = None
        if args.source == "FIXTURE":
            name = FIXTURES.get(envelope["release_id"])
            if not name:
                raise DemoError("No checked-in fixture exists for this release")
            fixture = json.loads((app_root() / "reports" / "fixtures" / name).read_text())
        write_json(args.output, collect(envelope, args.source, receipt, verification, fixture))
        print(f"Evidence collected: {args.source}")
    except (DemoError, OSError, ValueError) as exc:
        fail_cli(exc)


if __name__ == "__main__":
    main()
