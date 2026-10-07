import fcntl
import json
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from poc.common import Rejected, binding, canonical, digest, now, require_actor
from poc.inventory.targets import lock_key

TRANSITIONS = {
    "NOT_STARTED": {"APPROVED"}, "APPROVED": {"RUNNING"},
    "RUNNING": {"VERIFIED", "FAILED", "INVALID", "PARTIAL", "UNKNOWN_OUTCOME", "HOLD"},
    "FAILED": {"HOLD"}, "INVALID": {"HOLD"}, "PARTIAL": {"HOLD"},
    "UNKNOWN_OUTCOME": {"HOLD"}, "HOLD": set(), "VERIFIED": set(),
}


class Store:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.directory.mkdir(mode=0o700, parents=True, exist_ok=True)
        if self.directory.is_symlink() or self.directory.stat().st_uid != os.geteuid() or self.directory.stat().st_mode & 0o077:
            raise Rejected("state directory must be private to the restricted service")
        for path in self.directory.iterdir():
            if path.name in {"state.sqlite3", "state.sqlite3-wal", "state.sqlite3-shm", "runner.lock"}:
                if path.is_symlink() or path.stat().st_uid != os.geteuid() or path.stat().st_mode & 0o077:
                    raise Rejected("state files must be private and owned by the restricted service")
        previous_umask = os.umask(0o077)
        try:
            self.db = sqlite3.connect(str(self.directory / "state.sqlite3"), timeout=30)
            self.db.execute("PRAGMA journal_mode=WAL")
        finally:
            os.umask(previous_umask)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS releases (
              release_id TEXT PRIMARY KEY, envelope TEXT NOT NULL, binding TEXT NOT NULL,
              sql BLOB NOT NULL, scope TEXT NOT NULL, version TEXT NOT NULL,
              status TEXT NOT NULL, verification_status TEXT NOT NULL DEFAULT 'NOT_RUN',
              reviewed_by TEXT, approved_by TEXT, executor TEXT,
              start_time TEXT, end_time TEXT, evidence TEXT NOT NULL DEFAULT '{}',
              UNIQUE(scope, version));
            CREATE TABLE IF NOT EXISTS guards (scope TEXT PRIMARY KEY, release_id TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS events (
              sequence INTEGER PRIMARY KEY AUTOINCREMENT, release_id TEXT NOT NULL,
              timestamp TEXT NOT NULL, action TEXT NOT NULL, actor TEXT, details TEXT NOT NULL);
        """)

    @contextmanager
    def transaction(self):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            yield
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise

    @contextmanager
    def execution_lock(self):
        descriptor = os.open(self.directory / "runner.lock", os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        with os.fdopen(descriptor, "a") as stream:
            try:
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise Rejected("another restricted execution is active") from None
            try:
                yield
            finally:
                fcntl.flock(stream, fcntl.LOCK_UN)

    def event(self, release_id, action, actor=None, details=None):
        self.db.execute("INSERT INTO events(release_id,timestamp,action,actor,details) VALUES(?,?,?,?,?)",
                        (release_id, now(), action, actor, canonical(details or {})))

    def get(self, release_id):
        row = self.db.execute("SELECT * FROM releases WHERE release_id=?", (release_id,)).fetchone()
        if row is None:
            raise Rejected("unknown release")
        result = dict(row)
        result["envelope"] = json.loads(result["envelope"])
        result["evidence"] = json.loads(result["evidence"])
        if digest(result["sql"]) != result["envelope"]["artifact_sha256"] or binding(result["envelope"]) != result["binding"]:
            raise Rejected("frozen artifact or envelope integrity failed")
        return result

    def register(self, envelope, sql):
        if digest(sql) != envelope["artifact_sha256"]:
            raise Rejected("artifact hash mismatch")
        release_id = envelope["release_id"]
        with self.transaction():
            exists = self.db.execute("SELECT binding FROM releases WHERE release_id=?", (release_id,)).fetchone()
            if exists:
                if exists["binding"] != binding(envelope):
                    raise Rejected("release identity already binds different content or target")
                return False
            try:
                self.db.execute("INSERT INTO releases(release_id,envelope,binding,sql,scope,version,status) VALUES(?,?,?,?,?,?,?)",
                                (release_id, canonical(envelope), binding(envelope), sql,
                                 lock_key(envelope["target"]), envelope["migration_version"], "NOT_STARTED"))
            except sqlite3.IntegrityError:
                raise Rejected("migration version already reserved in this schema") from None
            self.event(release_id, "NOT_STARTED", envelope["requested_by"], {"binding": binding(envelope)})
        return True

    def transition(self, release_id, status, actor=None, details=None):
        old = self.get(release_id)["status"]
        if status not in TRANSITIONS[old]:
            raise Rejected("illegal state transition")
        self.db.execute("UPDATE releases SET status=? WHERE release_id=?", (status, release_id))
        self.event(release_id, status, actor, details)

    def approve(self, release_id, actor, expected_binding, policy):
        require_actor(policy, "reviewers", actor)
        with self.transaction():
            row = self.get(release_id)
            if row["binding"] != expected_binding:
                raise Rejected("approval binding mismatch")
            if actor == row["envelope"]["requested_by"]:
                raise Rejected("requester cannot approve their own release")
            self.transition(release_id, "APPROVED", actor, {"binding": expected_binding})
            self.db.execute("UPDATE releases SET reviewed_by=?,approved_by=? WHERE release_id=?", (actor, actor, release_id))

    def claim(self, release_id, actor, target, policy):
        require_actor(policy, "executors", actor)
        with self.transaction():
            row = self.get(release_id)
            if canonical(target) != canonical(row["envelope"]["target"]):
                raise Rejected("allowlisted target changed after submission")
            if actor in {row["envelope"]["requested_by"], row["approved_by"]}:
                raise Rejected("executor must be independent of requester and reviewer")
            if row["status"] != "APPROVED":
                raise Rejected("release is not dispatchable; no replay is allowed")
            try:
                self.db.execute("INSERT INTO guards(scope,release_id) VALUES(?,?)", (row["scope"], release_id))
            except sqlite3.IntegrityError:
                raise Rejected("schema is running or held for reconciliation") from None
            self.transition(release_id, "RUNNING", actor)
            self.db.execute("UPDATE releases SET executor=?,start_time=? WHERE release_id=?", (actor, now(), release_id))

    def finish(self, release_id, status, verification_status, evidence):
        with self.transaction():
            self.transition(release_id, status, details=evidence)
            self.db.execute("UPDATE releases SET verification_status=?,end_time=?,evidence=? WHERE release_id=?",
                            (verification_status, now(), canonical(evidence), release_id))
            if status == "VERIFIED":
                self.db.execute("DELETE FROM guards WHERE release_id=?", (release_id,))

    def recover_orphans(self):
        # Caller holds execution_lock: no live runner is being timed out.
        ids = [r[0] for r in self.db.execute("SELECT release_id FROM releases WHERE status='RUNNING'")]
        for release_id in ids:
            self.finish(release_id, "UNKNOWN_OUTCOME", "NOT_RUN", {"reason": "runner ended before durable outcome"})
        return ids

    def history(self, scope):
        return [self.get(r[0]) for r in self.db.execute(
            "SELECT release_id FROM releases WHERE scope=? AND start_time IS NOT NULL ORDER BY start_time", (scope,))]

    def reconcile(self, release_id, actor, evidence, policy):
        require_actor(policy, "recovery_owners", actor)
        with self.transaction():
            row = self.get(release_id)
            if row["status"] not in {"FAILED", "INVALID", "PARTIAL", "UNKNOWN_OUTCOME", "HOLD"}:
                raise Rejected("release is not held")
            retained = row["evidence"]
            retained["reconciliation"] = {"actor": actor, "timestamp": now(), "observed": evidence}
            self.db.execute("UPDATE releases SET evidence=? WHERE release_id=?", (canonical(retained), release_id))
            self.event(release_id, "READ_ONLY_RECONCILIATION", actor, evidence)

    def close_hold(self, release_id, actor, reconciliation_hash, attestation, policy):
        require_actor(policy, "recovery_owners", actor)
        if attestation != {"sessions_clear": True, "engine_history_checked": True, "effects_inspected": True}:
            raise Rejected("DBA closure attestation is incomplete")
        with self.transaction():
            row = self.get(release_id)
            rec = row["evidence"].get("reconciliation")
            if not rec or binding(rec) != reconciliation_hash:
                raise Rejected("closure must bind retained read-only reconciliation")
            if row["status"] == "HOLD":
                raise Rejected("hold already closed; release remains non-dispatchable")
            self.transition(release_id, "HOLD", actor, {"reconciliation_sha256": reconciliation_hash, **attestation})
            self.db.execute("DELETE FROM guards WHERE release_id=?", (release_id,))
        # New release identities may now proceed. This identity can never run again.
