# Bounded single-target architecture

```text
Exact Git commit: SQL + verification JSON
    -> existing protected Jenkins job and authenticated requester
    -> freeze exact bytes/envelope in private SQLite
    -> show exact SQL/target/hash/requester from protected state
    -> independent authenticated reviewer approves envelope hash
    -> independent authenticated executor confirms dispatch
    -> restricted persistent runner / Flyway Community
    -> existing Oracle lab owner schema
    -> separate Oracle observer checks validity/errors/effects
    -> durable state + escaped HTML/JSON/SQL/audit report
```

## Trust and approval

The CI owner must protect the **pipeline definition independently of submitted SQL**. Do not load a PR's Jenkinsfile or allow source authors to edit this job, credentials, installed runner, environment or protected configuration. Use an operator-controlled pipeline definition or separate protected pipeline source. A malicious Jenkinsfile can bypass all shell-level controls; the file's comment cannot enforce server RBAC. Job/agent setup and real UI/RBAC acceptance remain runtime gates, not claims of a deployed capability.

Jenkins captures `UserIdCause` for the requester and actual `input` submitter IDs for reviewer/executor. Scheduled/upstream triggers without a named human are rejected. One reviewer serves as both `reviewed_by` and `approved_by`. Requester, reviewer and executor must be distinct and remain in the protected role policy at dispatch. An administrator's ability to override input does not override the runner's policy check; administrators with state/secret/OS access remain trusted operators. Jenkins documents these input controls in its [input-step reference](https://www.jenkins.io/doc/pipeline/steps/pipeline-input-step/).

The runner reads SQL and expectation JSON from the exact commit and rejects dirty working files. SQL bytes are stored in SQLite, never rerendered or reread from a user-writable file at dispatch. The envelope includes release ID, commit, SQL SHA-256, numeric version, resolved target including identity/route/schema/credential references, requester, engine/driver versions and checksums, execution options, and expected verification. Its canonical SHA-256 is the approval token. Reusing the release ID with any changed field rejects before Oracle access. The review step obtains SQL and metadata together from integrity-checked protected state; workspace report projections cannot alter the approval content.

Operator policy may revoke actors, disable/change targets, change engine pins or disable instrumentation; dispatch then fails closed. No release parameter supplies a JDBC URL, password or schema. The only target selector is an allowlisted stable ID. Engine username is the schema owner; schema namespace and object grants restrict writes. Cross-schema/administrative migrations are outside this first phase.

## Owned responsibilities

| Package | Boundary |
| --- | --- |
| `inventory/`, `runner/artifact.py` | Single-target resolution, Git bytes, expectations and frozen binding |
| `state/store.py` | Transactional registration/admission, roles, durable state and audit |
| `runner/engine.py`, `runner/java/` | Fixed OSS Flyway invocation, no general CLI/SQL parser implementation |
| `verifier/oracle.py` | Identity preflight, exact owner/name/type/status/errors, approved data/call checks |
| `reports/`, `ci/Jenkinsfile` | Existing CI gates and static projections/evidence; no portal or service |

These are five bounded functional responsibilities, co-located on one restricted agent. Short code does not remove their security/correctness maintenance cost. No plugin/controller, queue, web API, scheduler, general workflow engine or application database was added.

## Durable admission and state

SQLite is built into Python, avoiding another service/dependency. WAL + synchronous FULL, `BEGIN IMMEDIATE`, permanent primary release ID, unique canonical-schema/version and unique schema guard prove atomic admission and duplicate exclusion. The canonical scope is DB_NAME/DB_UNIQUE_NAME/CON_NAME + schema; service aliases cannot open a second stream. A local nonblocking `flock` spans the complete execution and makes stranded RUNNING detection safe after process death. SQLite plus one local lock is intentionally limited to one persistent POSIX agent; it is not a distributed lock design.

```text
NOT_STARTED -> APPROVED -> RUNNING -> VERIFIED
                                -> FAILED
                                -> INVALID
                                -> PARTIAL
                                -> UNKNOWN_OUTCOME
                                -> HOLD
FAILED / INVALID / PARTIAL / UNKNOWN_OUTCOME -> HOLD after recorded DBA closure
```

VERIFIED clears the schema guard. Every other execution outcome retains it. RUNNING is committed **before** invoking Flyway; process death leaves retained admission and is recovered as UNKNOWN_OUTCOME only after reacquiring the execution lock. No status except APPROVED is dispatchable. HOLD is terminal for that release; a new identity is required after DBA closure. The system makes no exactly-once or rollback promise for Oracle DDL.

The full set of previous started migrations is rebuilt from retained exact SQL when a new release runs. Flyway validates its own target history against those files. Missing central state after restore is dangerous: keep inventory disabled, inspect Oracle history/effects/sessions, reconcile the restored store before reopening. Store restoration and disaster recovery are operator duties; no automated repair or state reconstruction was implemented.

## Verification and uncertain results

Writer/observer preflight checks DB_NAME, DB_UNIQUE_NAME, CON_NAME, service, exact Oracle version and principal/current schema using TCPS with hostname verification. The Java data source also checks those fields on **every actual Flyway connection before returning it**, including VERSION_FULL from PRODUCT_COMPONENT_VERSION; a separate earlier preflight cannot protect against route drift between connections. Missing diagnostic access or a changed identity fails before schema-history or migration writes. Successful engine migration must report exactly one new migration; a skip or unexpected migration count is not verified success.

The observer filters ALL_OBJECTS by exact owner/name/type, requires one VALID object, and checks ALL_ERRORS for relevant ERROR diagnostics. Package bodies are distinct objects. Missing visibility fails verification. DML assertions are integer-key row counts on approved tables; no free-form verification query is accepted. Optional CLOB function calls are explicitly included in approval and use the deterministic fixture. They are safe only if the reviewed body is side-effect-free; reconciliation normally uses dictionary/effect reads, and may include only those expressly approved calls. [Oracle ALL_OBJECTS](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/ALL_OBJECTS.html), [Oracle ALL_ERRORS](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/ALL_ERRORS.html), [Oracle PRODUCT_COMPONENT_VERSION](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/PRODUCT_COMPONENT_VERSION.html).

Object errors yield INVALID even if Flyway succeeded. Missing objects/effect mismatches yield FAILED and hold the schema. SQL failure after engine start is conservatively PARTIAL because earlier Oracle DDL may have committed. Transport loss, process loss, timeout or failed verification communication yields UNKNOWN_OUTCOME. Additional read-only observations never overrule a failed/uncertain engine outcome. Diagnostic positions/codes are retained without raw error text that can expose SQL literals. [Oracle transaction/DDL semantics](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/COMMIT.html).

`reconcile` records observations without redispatch or promotion. `close-hold` binds the reconciliation hash and an authorized DBA's session/history/effect attestation; it never rewrites UNKNOWN to VERIFIED. Failed engine history may still require a separately approved manual forward fix/repair. This operational gate deliberately avoids implementing a general recovery controller.

## Evidence and credentials

SQLite stores frozen SQL/envelopes, actors, times, status, verification and append-only audit events. Generated `index.html`, `result.json`, `events.json` and `artifact.sql` are projections archived by Jenkins. HTML is escaped with no JavaScript; CLI diagnostics are fixed/JSON escaped. Engine stdout/stderr and driver exception text are captured privately and discarded, never copied into retained logs/reports. Separate injected password environment variables feed the writer and observer; inventory contains references only.

All state files must be private and owned by the restricted service. Protect backups, reports, CI retention and configuration together. A generated report after a crash may be stale until orphan recovery/regeneration; protected SQLite is the state authority. Expiring Jenkins build artifacts is not an acceptable backup for admission. Measured UX, owner acceptance and restore proof remain incomplete; users must still work across Git and CI and read linked reports on held releases.
