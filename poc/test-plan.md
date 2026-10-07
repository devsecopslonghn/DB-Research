# Single-target staged test plan

New acceptance records only; preserve the historical [45-case contract](ORACLE-POC.md) and [14 workload hashes](../evaluation/workloads/manifest.json). Statuses are PASS, PARTIAL, FAIL, BLOCKED or NOT_RUN. Unit/SQLite/engine-parser evidence never becomes an Oracle case PASS.

## Gate L: local safety

Run the existing document verifier plus `python3 -m unittest discover -s poc/tests -v` and the Maven/parser commands in the [README](OSS-POC-README.md). Tests cover hash/target/expectation/requester changes, duplicate/atomic concurrent admission, illegal transitions, independent actors, role revocation, unsupported/free-form targets, Git dirty files, HTML/log escaping, tampered/private state, previous exact migrations, INVALID/compile diagnostics/effect veto, conservative partial handling, process-exit persistence, UNKNOWN/HOLD replay rejection and authorized reconciliation. Oracle adapters here are fakes. Real Oracle execution remains gated separately.

## Gate O: existing lab and real UI

Before any write: approved separate references/principals; confirmed live version/database/PDB/service/schema; restricted grants and TLS; a protected Jenkins definition and installed isolated runner; actual distinct actors; persistent local state/retention; explicit no-fee JDBC exception if permitted. The DBA must verify no previous unknown work/session for this migration stream. Capture actual target preview, approval submitters, execution and evidence links using the existing Jenkins UI. No new portal or controller is deployed by this repository.

The owner writer needs only own-schema create privileges for approved objects and grant authority for its objects. The observer needs dictionary visibility plus explicit SELECT/EXECUTE grants on these test objects; the fixtures carry approved grants to the proposed observer. No shared ADMIN credential. Runtime fixture names must match the reviewed existing schema before Git freezing. No credentials in SQL, screenshots, logs, envelope or HTML.

## Oracle cases

| Case | Frozen input / action | Required observed result |
| --- | --- | --- |
| T1 | [Function SQL](fixtures/T1_function.sql), [expectations](fixtures/T1_expected.json); one independent review/execution | Flyway executes one migration; correct owner FUNCTION exists; VALID; no relevant ALL_ERRORS; approved CLOB call returns 3; state VERIFIED |
| T2 | [Invalid SQL](fixtures/T2_invalid.sql), [expectations](fixtures/T2_expected.json); a fresh increasing version/release | Oracle may accept CREATE; diagnostics/object INVALID must veto success; retained state INVALID (or PARTIAL if engine reports SQL failure), never VERIFIED; schema held |
| T3 | Resubmit/reapprove/execute exact T1 identity/SQL/target | No second Oracle execution/effect/history increment; permanent release record remains VERIFIED |
| T4 | Change T1 SQL or expectation JSON at a new commit, reuse T1 release ID | Hard reject before any Oracle connection/write; original binding/history unchanged |
| T5 | Supply unknown target or mutate protected target/schema after approval in an authorized negative-test copy | Reject before connection/write; do not mutate the actual approved allowlist to redirect a live run |
| T6 | [Partial SQL](fixtures/T6_partial.sql), [expectations](fixtures/T6_expected.json); fresh version | First table/grant persist and later ALTER fails; result PARTIAL with evidence, schema held, no retry or promotion |
| T7 | [Loss SQL](fixtures/T7_lost_result.sql), [expectations](fixtures/T7_expected.json); fresh version, explicit approved loss option | Real engine success then runner exit 86 before result persistence; RUNNING survives; recovery records UNKNOWN_OUTCOME; replay rejected; read-only reconciliation records Oracle effects/history and required DBA closure |

The full original business function is unavailable. T1 is a derived syntax fixture; testing it does not certify the unseen business body or entire corpus. Package/body parser evidence is local; add real package/body regression before estate adoption. Record exact 19c and 21c versions/drivers separately; the existing 26ai lab alone is insufficient.

Suggested order: T1, T3, T4, T5, T7, authorized reconciliation/closure, T2, authorized reconciliation/closure, T6 last. T2/T6/T7 hold the single schema, so blindly running T1–T7 sequentially would be unsafe. Closing a hold is a new authenticated DBA decision, not an automatic test cleanup. After T2, a new reviewed forward-fix release may be needed; after T6, failed Flyway history needs explicit DBA recovery and no further case is automatically dispatched. Never create extra targets to hide holds or clear the ledger to rerun a case.

T7 requires `allow_failure_instrumentation=true` in protected policy and `freeze --loss-after-engine-success`, which is included in the approval envelope. A fake process exit in unit tests proves SQLite persistence only. If real instrumentation/approval is unavailable, T7 is NOT_RUN/BLOCKED, not PASS. Do not infer rollback from exit 86, cancellation or timeout.

## Evidence protocol

Every runtime record must include `case_id`, timestamp, engine/version + jar/driver pins, exact Oracle version, target and identity, artifact SHA-256, expected, observed, status and evidence references. Retain approval binding/actors and engine/dictionary/history/effect observations. New runs get timestamped record paths; do not overwrite historical files or the current BLOCKED attempt to fake continuity. Include failed/blocked attempts.

Evidence should prove the number of engine invocations, target history rows and object/data effects for replay cases. Screenshots supplement structured records. All raw secrets/cookies/driver traces remain private. The static HTML/JSON artifacts must be retrievable after a job/process restart, and SQLite backup/restore must be tested with inventory held disabled until reconciliation.

## Promotion and adoption gate

No promotion code exists in this phase. Only after all T1–T7 runtime cases pass and actors/UX/retention/owners are accepted may a separate requested phase add DEV/SIT/UAT/MOCKPROD. It must use the same artifact, verified predecessors and fresh MOCKPROD approval; FAILED/INVALID/PARTIAL/UNKNOWN_OUTCOME/HOLD can never authorize a next stage. Inventory fixtures do not prove live estate scale.
