import tempfile
from pathlib import Path

from poc.common import Rejected, binding, canonical


def execute(store, release_id, actor, target, policy, engine, observer, checkpoint=None):
    with store.execution_lock():
        store.recover_orphans()
        row = store.get(release_id)
        if row["status"] != "APPROVED":
            raise Rejected("release is not dispatchable; no replay is allowed")
        if canonical(row["envelope"]["target"]) != canonical(target):
            raise Rejected("resolved target changed after approval")
        for field in ("engine", "engine_version", "engine_sha256", "oracle_driver"):
            if row["envelope"][field] != policy[field]:
                raise Rejected("engine configuration changed after approval")
        from poc.common import require_actor
        require_actor(policy, "executors", actor)
        require_actor(policy, "requesters", row["envelope"]["requested_by"])
        require_actor(policy, "reviewers", row["approved_by"])
        if actor in {row["envelope"]["requested_by"], row["approved_by"]}:
            raise Rejected("executor must be independent")
        # Reject existing holds before making any Oracle connection.
        if store.db.execute("SELECT 1 FROM guards WHERE scope=?", (row["scope"],)).fetchone():
            raise Rejected("schema is held for reconciliation")
        history = store.history(row["scope"])
        if history and int(row["version"]) <= max(int(r["version"]) for r in history):
            raise Rejected("migration version must increase within this schema")
        preflight = observer.preflight(target)
        with tempfile.TemporaryDirectory(prefix="migrations-", dir=store.directory) as folder:
            directory = Path(folder)
            for previous in history + [row]:
                name = "V" + previous["version"] + "__" + previous["release_id"] + ".sql"
                path = directory / name
                path.write_bytes(previous["sql"])
                path.chmod(0o400)
            store.claim(release_id, actor, target, policy)
            try:
                outcome = engine.run(target, directory)
                if checkpoint and outcome["outcome"] == "SUCCESS":
                    checkpoint()  # Test-only injectable loss after execution, before result recording.
                evidence = {"preflight": preflight, "engine": outcome}
                if outcome["outcome"] == "SUCCESS":
                    verification = observer.check(target, row["envelope"]["expected"])
                    verdict = verification["verification_status"]
                    evidence["verification"] = verification
                    store.finish(release_id, verdict, verdict, evidence)
                else:
                    # Read-only postchecks can establish partial effects, but never override failure.
                    try:
                        evidence["verification"] = observer.check(target, row["envelope"]["expected"])
                    except Exception:
                        evidence["verification"] = {"verification_status": "NOT_RUN"}
                    store.finish(release_id, outcome["outcome"], evidence["verification"]["verification_status"], evidence)
            except Exception:
                store.finish(release_id, "UNKNOWN_OUTCOME", "NOT_RUN",
                             {"reason": "execution or verification result could not be retained"})
                # Do not surface raw driver/engine exceptions in CI logs.
            return store.get(release_id)


def reconcile(store, release_id, actor, policy, observer):
    with store.execution_lock():
        store.recover_orphans()
        row = store.get(release_id)
        from poc.common import require_actor
        require_actor(policy, "recovery_owners", actor)
        if row["status"] not in {"FAILED", "INVALID", "PARTIAL", "UNKNOWN_OUTCOME", "HOLD"}:
            raise Rejected("only held outcomes can be reconciled")
        evidence = observer.check(row["envelope"]["target"], row["envelope"]["expected"])
        store.reconcile(release_id, actor, evidence, policy)
        return binding(store.get(release_id)["evidence"]["reconciliation"])
