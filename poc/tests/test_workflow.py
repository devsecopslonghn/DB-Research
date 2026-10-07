import copy
import json
import multiprocessing
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from poc.common import Rejected, binding, digest
from poc.inventory.targets import resolve
from poc.reports.render import write_report
from poc.runner.artifact import envelope, git_artifact
from poc.runner.workflow import execute, reconcile
from poc.state.store import Store

ROOT = Path(__file__).resolve().parents[1]


def settings():
    target = json.loads((ROOT / 'inventory/targets.example.json').read_text())["targets"]["oracle-lab"]
    target["enabled"] = True
    target["database_identity"] = {"db_name": "LAB", "db_unique_name": "LAB1", "con_name": "LABPDB"}
    target["oracle_version"] = "19.25.0.0.0"
    policy = {"requesters": ["alice"], "reviewers": ["bob", "alice"], "executors": ["exec", "bob", "alice"],
              "recovery_owners": ["dba"], "engine": "Flyway Community", "engine_version": "13.9.0",
              "engine_sha256": "a" * 64, "allow_failure_instrumentation": True,
              "oracle_driver": {"approved": False, "sha256": "b" * 64, "license": "FUTC fixture"}}
    return target, policy


class EngineFake:
    def __init__(self, outcome="SUCCESS"):
        self.calls = 0
        self.outcome = outcome

    def run(self, target, directory):
        self.calls += 1
        self.scripts = {p.name: p.read_bytes() for p in directory.glob('*.sql')}
        return {"outcome": self.outcome}


class ObserverFake:
    def __init__(self, verdict="VERIFIED"):
        self.verdict = verdict
        self.calls = 0

    def preflight(self, target):
        self.calls += 1
        return {"observed": "test fixture only"}

    def check(self, target, expected):
        self.calls += 1
        return {"verification_status": self.verdict}


def admit_process(directory, value, sql, output):
    try:
        store = Store(directory)
        output.put(store.register(value, sql))
    except Exception as error:
        output.put(type(error).__name__)


def crash_process(directory, value, policy):
    store = Store(directory)
    execute(store, value["release_id"], "exec", value["target"], policy, EngineFake(), ObserverFake(),
            checkpoint=lambda: os._exit(86))


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.store = Store(self.root / 'state')
        self.target, self.policy = settings()
        self.sql = (ROOT / 'fixtures/T1_function.sql').read_bytes()
        self.expected = json.loads((ROOT / 'fixtures/T1_expected.json').read_text())
        self.value = envelope("r1", "f" * 40, "1", "oracle-lab", self.target, "alice", self.sql, self.expected, self.policy)

    def tearDown(self):
        self.store.db.close()
        self.temp.cleanup()

    def approved(self, value=None, sql=None):
        value = value or self.value
        self.store.register(value, sql or self.sql)
        self.store.approve(value["release_id"], "bob", binding(value), self.policy)

    def dispatch(self, engine=None, observer=None, target=None):
        return execute(self.store, "r1", "exec", target or self.target, self.policy,
                       engine or EngineFake(), observer or ObserverFake())

    def test_hash_mismatch(self):
        with self.assertRaises(Rejected):
            self.store.register(self.value, self.sql + b'-- changed')
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM releases').fetchone()[0], 0)

    def test_changed_content_and_verification_under_same_identity(self):
        self.approved()
        for mutation in ("sql", "expected", "requester", "target"):
            value = copy.deepcopy(self.value)
            sql = self.sql
            if mutation == "sql":
                sql += b'-- changed\n'
                value["artifact_sha256"] = digest(sql)
            elif mutation == "expected":
                value["expected"]["invocations"][0]["expected_number"] = 999
            elif mutation == "requester":
                value["requested_by"] = "another"
            else:
                value["target"]["schema"] = "OTHER"
            with self.subTest(mutation=mutation), self.assertRaises(Rejected):
                self.store.register(value, sql)

    def test_approval_hash_and_self_approval(self):
        self.store.register(self.value, self.sql)
        for actor, expected in (("bob", "wrong"), ("alice", binding(self.value)), ("outsider", binding(self.value))):
            with self.assertRaises(Rejected):
                self.store.approve("r1", actor, expected, self.policy)
        self.assertEqual(self.store.get("r1")["status"], "NOT_STARTED")

    def test_changed_target_rejects_before_oracle(self):
        self.approved()
        target = copy.deepcopy(self.target)
        target["schema"] = 'EVIL'
        engine, observer = EngineFake(), ObserverFake()
        with self.assertRaises(Rejected):
            self.dispatch(engine, observer, target)
        self.assertEqual((engine.calls, observer.calls), (0, 0))

    def test_duplicate_never_executes_twice(self):
        self.approved()
        engine = EngineFake()
        self.assertEqual(self.dispatch(engine)["status"], 'VERIFIED')
        self.assertFalse(self.store.register(self.value, self.sql))
        with self.assertRaises(Rejected):
            self.dispatch(engine)
        self.assertEqual(engine.calls, 1)
        self.assertEqual(next(iter(engine.scripts.values())), self.sql)

    def test_no_requester_or_reviewer_execution(self):
        self.approved()
        for actor in ("alice", "bob", "outsider"):
            with self.assertRaises(Rejected):
                execute(self.store, "r1", actor, self.target, self.policy, EngineFake(), ObserverFake())

    def test_invalid_object_vetoes_engine_success_and_holds_schema(self):
        self.approved()
        self.assertEqual(self.dispatch(observer=ObserverFake('INVALID'))["status"], 'INVALID')
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM guards').fetchone()[0], 1)
        next_value = copy.deepcopy(self.value)
        next_value.update(release_id='r2', migration_version='2')
        self.approved(next_value)
        engine, observer = EngineFake(), ObserverFake()
        with self.assertRaises(Rejected):
            execute(self.store, "r2", "exec", self.target, self.policy, engine, observer)
        self.assertEqual((engine.calls, observer.calls), (0, 0))

    def test_partial_cannot_be_overridden_by_valid_objects(self):
        self.approved()
        row = self.dispatch(EngineFake('PARTIAL'))
        self.assertEqual(row['status'], 'PARTIAL')
        with self.assertRaises(Rejected):
            self.dispatch()

    def test_illegal_transitions(self):
        self.store.register(self.value, self.sql)
        with self.assertRaises(Rejected):
            with self.store.transaction():
                self.store.transition('r1', 'VERIFIED')
        self.approved_after_registration()
        self.dispatch()
        with self.assertRaises(Rejected):
            with self.store.transaction():
                self.store.transition('r1', 'RUNNING')

    def approved_after_registration(self):
        self.store.approve('r1', 'bob', binding(self.value), self.policy)

    def test_process_loss_persists_unknown_and_no_replay(self):
        self.approved()
        process = multiprocessing.Process(target=crash_process, args=(str(self.root / 'state'), self.value, self.policy))
        process.start(); process.join(10)
        self.assertEqual(process.exitcode, 86)
        self.assertEqual(self.store.get('r1')['status'], 'RUNNING')
        # A new process/connection after restart acquires the exclusive lock before orphan recovery.
        restarted = Store(self.root / 'state')
        with restarted.execution_lock():
            self.assertEqual(restarted.recover_orphans(), ['r1'])
        self.assertEqual(restarted.get('r1')['status'], 'UNKNOWN_OUTCOME')
        engine = EngineFake()
        with self.assertRaises(Rejected):
            execute(restarted, 'r1', 'exec', self.target, self.policy, engine, ObserverFake())
        self.assertEqual(engine.calls, 0)
        restarted.db.close()

    def test_read_only_reconciliation_never_dispatches_or_changes_unknown_to_success(self):
        self.approved()
        self.dispatch(EngineFake('UNKNOWN_OUTCOME'))
        result_hash = reconcile(self.store, 'r1', 'dba', self.policy, ObserverFake())
        self.assertEqual(self.store.get('r1')['status'], 'UNKNOWN_OUTCOME')
        attestation = {"sessions_clear": True, "engine_history_checked": True, "effects_inspected": True}
        with self.assertRaises(Rejected):
            self.store.close_hold('r1', 'dba', 'wrong', attestation, self.policy)
        with self.store.execution_lock():
            self.store.close_hold('r1', 'dba', result_hash, attestation, self.policy)
        self.assertEqual(self.store.get('r1')['status'], 'HOLD')
        with self.assertRaises(Rejected):
            self.dispatch()

    def test_concurrent_admission(self):
        output = multiprocessing.Queue()
        processes = [multiprocessing.Process(target=admit_process,
                     args=(str(self.root / 'state'), self.value, self.sql, output)) for _ in range(2)]
        for process in processes: process.start()
        for process in processes:
            process.join(10)
            self.assertEqual(process.exitcode, 0)
        self.assertCountEqual([output.get(timeout=2), output.get(timeout=2)], [True, False])

    def test_unknown_target_and_free_form_inputs(self):
        path = self.root / 'targets.json'
        path.write_text(json.dumps({'targets': {'oracle-lab': self.target}}))
        self.assertEqual(resolve(path, 'oracle-lab'), self.target)
        for target_id in ('other', 'jdbc:oracle:evil', '../../foo', 'oracle-lab\nINJECT'):
            with self.subTest(target_id=target_id), self.assertRaises(Rejected):
                resolve(path, target_id)

    def test_html_escaping_and_no_raw_sql_in_events(self):
        sql = b"-- <script>alert('x')</script> & \x1b[31m\nCREATE TABLE EXAMPLE(ID NUMBER);\n"
        value = envelope('r1', 'f'*40, '1', 'oracle-lab', self.target, 'alice', sql, self.expected, self.policy)
        self.store.register(value, sql)
        report = self.root / 'reports'
        write_report(self.store, 'r1', report)
        html = (report / 'r1/index.html').read_text()
        self.assertNotIn('<script>', html)
        self.assertIn('&lt;script&gt;', html)
        events = (report / 'r1/events.json').read_text()
        self.assertNotIn('alert', events)
        self.assertNotIn('\x1b', events)

    def test_sqlplus_not_silently_stripped(self):
        for sql in (b'@other.sql\n', b'WHENEVER SQLERROR EXIT\n', b'SPOOL foo\n', b'BEGIN :x:=&VAR; END;\n/'):
            with self.assertRaises(Rejected):
                envelope('r1', 'f'*40, '1', 'oracle-lab', self.target, 'alice', sql, self.expected, self.policy)

    def test_sqlite_tampering_detected(self):
        self.approved()
        with self.store.transaction():
            self.store.db.execute("UPDATE releases SET sql=? WHERE release_id='r1'", (b'modified',))
        with self.assertRaises(Rejected):
            self.dispatch()

    def test_git_bytes_and_dirty_working_tree(self):
        repo = self.root / 'source'
        repo.mkdir()
        subprocess.run(['git', 'init', '-q', str(repo)], check=True)
        (repo / 'change.sql').write_bytes(self.sql)
        subprocess.run(['git', '-C', str(repo), 'add', 'change.sql'], check=True)
        subprocess.run(['git', '-C', str(repo), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@invalid',
                        'commit', '-qm', 'test fixture'], check=True)
        commit = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
        self.assertEqual(git_artifact(repo, commit, 'change.sql'), self.sql)
        (repo / 'change.sql').write_bytes(self.sql + b'-- changed')
        with self.assertRaises(Rejected):
            git_artifact(repo, commit, 'change.sql')
        with self.assertRaises(Rejected):
            git_artifact(repo, commit, '../change.sql')

    def test_previous_exact_migrations_are_retained_for_flyway_validation(self):
        self.approved(); self.dispatch()
        other = copy.deepcopy(self.value)
        other.update(release_id='r2', migration_version='2')
        sql = self.sql + b'-- next release\n'
        other['artifact_sha256'] = digest(sql)
        self.approved(other, sql)
        engine = EngineFake()
        execute(self.store, 'r2', 'exec', self.target, self.policy, engine, ObserverFake())
        self.assertEqual(engine.scripts, {'V1__r1.sql': self.sql, 'V2__r2.sql': sql})

    def test_revoked_review_actor_rejects_before_oracle(self):
        self.approved()
        self.policy['reviewers'].remove('bob')
        engine, observer = EngineFake(), ObserverFake()
        with self.assertRaises(Rejected):
            self.dispatch(engine, observer)
        self.assertEqual((engine.calls, observer.calls), (0, 0))

    def test_permissive_state_file_rejected(self):
        self.store.db.close()
        (self.root / 'state/state.sqlite3').chmod(0o644)
        with self.assertRaises(Rejected):
            Store(self.root / 'state')

    def test_failure_instrumentation_requires_explicit_policy(self):
        self.policy['allow_failure_instrumentation'] = False
        with self.assertRaises(Rejected):
            envelope('r1', 'f'*40, '1', 'oracle-lab', self.target, 'alice', self.sql, self.expected,
                     self.policy, loss_after_success=True)


if __name__ == '__main__':
    unittest.main()
