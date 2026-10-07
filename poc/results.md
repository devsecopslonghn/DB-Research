# OSS POC results — 7 October 2026

**Latest runtime-prerequisite follow-up:** [7 October 09:51 UTC evidence](reports/runtime-prerequisites-20261007T095109Z/README.md), [current T1–T7 records](reports/runtime-prerequisites-20261007T095109Z/cases.json). The user authorized the existing single-target T1–T7 run. The unchanged runner and `oracledb==3.4.0` are now prepared in an isolated local venv; 30 local tests, installed entry point, dependency/version checks and four parser inputs PASS. Runtime entry remains **NO-GO / BLOCKED**: approved target/credential references, actor/recovery-owner assignments, protected CI/agent/Git source and the JDBC exception are still required. Jenkins discovery found the full-control-for-logged-in-users strategy, shared non-exclusive agents and no existing reference job/template. No Oracle connection/SQL or Jenkins configuration change occurred. Earlier implementation/acceptance evidence below is preserved.

**Implementation and local safety/parser checks pass. Oracle T1–T7 and authenticated Jenkins acceptance are BLOCKED. Adoption decision: NO-GO until those runtime gates pass; the feasibility question remains open.** No Oracle SQL was executed, no CI job/controller was deployed, no credential was extracted, and no historical ODC/Bytebase result was changed.

## Evidence observed in this round

| Check | Result | Scope / retained evidence |
| --- | --- | --- |
| Python safety tests | PASS, 30 tests | [Latest local record](reports/local-20261007T090057.153281_0000/checks.json), [test log](reports/local-20261007T090057.153281_0000/tests.log); synthetic actors/Oracle adapters, real SQLite and process exit |
| OSS Java build/version | PASS | Maven package succeeds; actual readback `OSS_POC_VERSION=13.9.0`; checksum in latest local record |
| Actual Flyway Oracle parser | PASS, five inputs | [Parser log](reports/local-20261007T090057.153281_0000/parser.log); T1=2, T2=2, T6=3, T7=2, retained release-small=11 statements; no DB connection |
| Default engine dependency boundary | PASS | Default build contains Flyway core/Oracle libraries plus Jackson annotations; Oracle JDBC is excluded and explicit approval is required for the external FUTC driver |
| Installed isolated Python entry point | PASS | [Isolation evidence](reports/local-20261007T090057.153281_0000/installed-isolation.json); hostile workspace module/PYTHONPATH ignored |
| Packaged CLI and static preview | PASS, LOCAL ONLY | [CLI smoke](reports/local-20261007T090057.153281_0000/cli-smoke.json), [preview disclaimer](reports/preview-local-only/README.md), [HTML example](reports/preview-local-only/LOCAL_PREVIEW_ONLY/index.html); synthetic actors, disabled target, no Oracle connection; driver gate rejects execution before start |
| Existing research document check / final review | PASS | [Final review record](reports/local-20261007T090057.153281_0000/final-review.json); zero errors; 815 research links, 242 tables, 38 source snapshots, 183 source references and 11 screenshot hashes; POC links and engine checksum checked; only the two existing indexes changed |
| Existing orchestrator discovery | ESTABLISHED | Read-only metadata identifies ready Jenkins 2.568.3-jdk21, installed pipeline/input/credentials plugins and bound controller PVC; [topology](lab-topology.md) |
| Code safety review | Completed | Independent read-only review; fixes cover approval source integrity, Python import isolation, private state files and driver binding; effective CI configuration still unproved |
| Oracle cases T1–T7 | BLOCKED, 7 cases | [New structured records](reports/oracle-attempt-20261007/cases.json); no Oracle cases executed, no runtime PASS claimed |
| Actual Jenkins review/execute UI | BLOCKED | Restricted agent, named actors, protected job/RBAC and source repository not confirmed |
| 19c/21c correctness | NOT_RUN | Current lab version unconfirmed; historical Oracle 26ai 23.26.4.1.0 is not transferred into new engine acceptance |
| Promotion, scale, backup/restore and owner acceptance | NOT_RUN | Deferred until the single-target gates pass; no adoption/maintainer assignment inferred |

The [earlier local checkpoint](reports/local-20261007T085916.429048_0000/checks.json) is retained separately. It predates the additional same-session JDBC identity guard; the latest record describes the final guarded build. New local runs append timestamped evidence, rather than overwrite previous attempts.

Local process-loss instrumentation exits a subprocess with code 86 after a **fake** engine call and before outcome recording, then reopens the actual SQLite state and proves UNKNOWN/no replay. It is evidence of durable admission mechanics only. Live T7 must execute the real engine, commit effects, lose central recording, and perform read-only reconciliation. Valid-object mocks and parser acceptance do not certify Oracle compilation or verification visibility.

## What is implemented

The modular package freezes SQL/expectation JSON from exact Git bytes, resolves one protected allowlisted target, binds the entire envelope to approval, enforces independent actors, admits execution transactionally, retains canonical schema guards through failure/unknown results, invokes only fixed Flyway migration, verifies Oracle object status/diagnostics/effects, and generates escaped HTML/JSON/SQL/audit projections. A protected Jenkinsfile supplies the target choice and authenticated human gates. No promotion controller or web service was built.

The engine checks the approved DB identity/version/schema on every actual JDBC session before passing the connection to Flyway, including before schema-history writes. The Python preflight provides an independent diagnostic check. Target resolution cannot take an arbitrary URL/schema/password. Ambiguous engine/verification outcomes cannot become VERIFIED. This is implemented behavior; its real Oracle acceptance remains blocked.

## Blockers, responsible roles and decision

1. **DBA / credential owner:** supply approved separate writer and observer references and the existing schema this POC may modify; confirm live DB/PDB/service/version, least privilege, observer visibility and TCPS requirements. No injected POC variables exist in this session, and Bytebase secrets are explicitly excluded.
2. **User / software-policy owner:** decide whether the no-fee Oracle JDBC connectivity dependency is allowed. `ojdbc11:21.18.0.0` is FUTC, not OSS; it is absent from the default build and the example policy rejects it. Under a literal all-dependencies-OSS rule, this selected JDBC composition cannot be executed without changing the requirement/approved available engine path.
3. **CI / platform owner:** identify real requester/reviewer/executor IDs, protect the pipeline definition/runner/config outside source-author control, assign a persistent restricted agent and two credential bindings, confirm artifact retention/backup and an approved Git source. The research workspace has no Git metadata. Controller availability does not prove these controls.
4. **Application owner / DBA:** provide the complete sanitized function/body and confirm the actual corpus's required client directives/edition semantics. The supplied ellipsis cannot be compiled; T1 remains a derived fixture. Record 19c/21c runtime evidence separately.

No approval answer, credential reference or real human identity was invented. These inputs are required to complete the user's Definition of Done, so this round cannot determine whether the team can operate the workflow or maintain it safely. NO-GO here blocks adoption; it is not a claimed Oracle compatibility failure. Runtime completion remains outstanding.

## Operating cost and user experience

Users must use Git and Jenkins, with report links for SQL/hash/target/results. The CI provides one target choice and captures independent submitters, but its usability and approval text rendering need an actual operator session. The restricted agent may wait during human gates. HTML can be downloaded from archived Jenkins artifacts; no HTML-publisher plugin is assumed. No timings, screenshots, 50-target performance or maintainer acceptance were manufactured.

The main cost is owning five safety responsibilities, pinned engine/observer upgrades, protected CI/agent/state/config, evidence backup and DBA hold recovery. Successful parser tests do not make these free. The main safety risk is Oracle DDL committing before outcome recording, especially if stale state is restored or another write path bypasses the managed stream. UNKNOWN/HOLD + session/history/effect reconciliation mitigates this; no automatic retry/repair is provided.

```text
SELECTED ENGINE = Flyway Community 13.9.0 (OSS Maven libraries)
SELECTED CI/ORCHESTRATOR = Existing Jenkins 2.568.3-jdk21

ORACLE VERSION = Current UNCONFIRMED; historical lab 26ai 23.26.4.1.0; 19c/21c NOT_RUN
TARGET MODEL = One existing database/PDB/service and one allowlisted owner schema

POC RESULT = Local implementation/tests PASS; Oracle T1–T7 and CI runtime BLOCKED
GO / NO-GO = NO-GO for adoption pending runtime evidence; feasibility undecided

CUSTOM COMPONENTS OWNED =
1. Inventory and frozen artifact/envelope validation
2. SQLite admission/guard/state/audit and bounded hold reconciliation
3. Fixed Flyway invocation and same-session JDBC identity guard
4. Oracle identity/object/error/effect verifier
5. Jenkins gates and static HTML/JSON evidence reporting

WHAT THIS REPLACES = Intended controlled replacement for manual DBeaver writes and standalone Flyway launches after runtime acceptance
WHAT IT DOES NOT REPLACE = Oracle administration, Git/CI/credential operations, DBA recovery, estate compatibility testing or a full governance platform

MAIN OPERATIONAL COST = Maintaining protected CI/runner/state and five safety responsibilities plus DBA hold recovery
MAIN SAFETY RISK = Committed Oracle DDL with lost/stale outcome state or bypass writes

NEXT STEP = Supply approved lab/CI/source references and resolve JDBC dependency policy; run one-target T1–T7, then classify feasibility from actual evidence
```
