import argparse
import json
import os
import sys
from pathlib import Path

from poc.common import Rejected, canonical
from poc.inventory.targets import resolve
from poc.reports.render import write_report
from poc.runner.artifact import envelope, git_artifact
from poc.runner.engine import Engine
from poc.runner.workflow import execute, reconcile
from poc.state.store import Store
from poc.verifier.oracle import Observer


def main(argv=None):
    os.umask(0o077)
    parser = argparse.ArgumentParser(description="Trusted single-target POC runner; connection configuration is operator-owned.")
    commands = parser.add_subparsers(dest="command", required=True)
    freeze = commands.add_parser("freeze")
    for name in ("release-id", "git-commit", "version", "target-id", "actor", "sql", "expected"):
        freeze.add_argument("--" + name, required=True)
    freeze.add_argument("--repo", default=".")
    freeze.add_argument("--loss-after-engine-success", action="store_true")
    approve = commands.add_parser("approve")
    approve.add_argument("--release-id", required=True)
    approve.add_argument("--actor", required=True)
    approve.add_argument("--binding", required=True)
    for name in ("execute", "reconcile", "close-hold"):
        cmd = commands.add_parser(name)
        cmd.add_argument("--release-id", required=True)
        cmd.add_argument("--actor", required=True)
        if name == "close-hold":
            cmd.add_argument("--reconciliation-sha256", required=True)
            cmd.add_argument("--attestation", required=True, help="Operator-owned nonsecret JSON attestation")
    report = commands.add_parser("report")
    report.add_argument("--release-id", required=True)
    review = commands.add_parser("review")
    review.add_argument("--release-id", required=True)
    commands.add_parser("recover-orphans")
    probe = commands.add_parser("probe")
    probe.add_argument("--target-id", required=True)
    args = parser.parse_args(argv)
    try:
        inventory = os.environ["OSS_POC_INVENTORY"]
        policy = json.loads(Path(os.environ["OSS_POC_POLICY"]).read_text())
        if args.command == "probe":
            # Read-only; operator compares this with approved nonsecret lab records.
            print(canonical(Observer().probe(resolve(inventory, args.target_id))))
            return 0
        store = Store(os.environ["OSS_POC_STATE_DIR"])
        if args.command == "review":
            row = store.get(args.release_id)
            print(canonical({"envelope": row["envelope"], "approval_binding_sha256": row["binding"],
                             "sql_utf8": row["sql"].decode("utf-8")}))
            return 0
        if args.command == "freeze":
            sql = git_artifact(args.repo, args.git_commit, args.sql)
            target = resolve(inventory, args.target_id)
            expected = json.loads(git_artifact(args.repo, args.git_commit, args.expected, suffix=".json"))
            value = envelope(args.release_id, args.git_commit, args.version, args.target_id,
                             target, args.actor, sql, expected, policy, args.loss_after_engine_success)
            store.register(value, sql)
        elif args.command == "approve":
            store.approve(args.release_id, args.actor, args.binding, policy)
        elif args.command == "execute":
            row = store.get(args.release_id)
            target = resolve(inventory, row["envelope"]["target_id"])
            engine = Engine(os.environ["OSS_POC_ENGINE_JAR"], policy["engine_sha256"], policy["engine_version"],
                            os.environ.get("OSS_POC_ORACLE_DRIVER_JAR", ""), policy["oracle_driver"])
            simulate = row["envelope"]["execution_options"]["loss_after_engine_success"]
            if simulate and policy.get("allow_failure_instrumentation") is not True:
                raise Rejected("failure instrumentation is no longer authorized")
            result = execute(store, args.release_id, args.actor, target, policy, engine, Observer(),
                             (lambda: os._exit(86)) if simulate else None)
            write_report(store, args.release_id, os.environ["OSS_POC_REPORT_DIR"])
            print(canonical({"release_id": args.release_id, "status": result["status"]}))
            return 0 if result["status"] == "VERIFIED" else 1
        elif args.command == "reconcile":
            print(canonical({"reconciliation_sha256": reconcile(store, args.release_id, args.actor, policy, Observer())}))
        elif args.command == "close-hold":
            with store.execution_lock():
                store.recover_orphans()
                store.close_hold(args.release_id, args.actor, args.reconciliation_sha256,
                                 json.loads(Path(args.attestation).read_text()), policy)
        elif args.command == "recover-orphans":
            with store.execution_lock():
                print(canonical({"unknown_outcomes": store.recover_orphans()}))
            return 0
        value = write_report(store, args.release_id, os.environ["OSS_POC_REPORT_DIR"])
        # Structured summary: no terminal control chars, secret values, or raw SQL in logs.
        print(canonical({k: value[k] for k in ("release_id", "status", "artifact_sha256", "approval_binding_sha256")}))
        return 0
    except Rejected as error:
        print(canonical({"status": "REJECTED", "reason": str(error)}), file=sys.stderr)
        return 2
    except Exception:
        print('{"status":"BLOCKED","reason":"required protected configuration or dependency unavailable"}', file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
