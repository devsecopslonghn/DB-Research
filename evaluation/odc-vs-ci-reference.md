# Recovered ODC lab versus the implemented CI/Flyway reference

Independent reassessment, **7 October 2026**. This round follows the user's comparison mission, with no preference inferred from historical `HOLD` or from implemented CI code. No SQL, runtime test, cluster change or historical-result edit was performed.

## 1. Executive conclusion

**FINAL COMPARISON: CI WINS under the specified responsibility/architecture threshold; neither path is accepted for production. ODC_RUNTIME_NOT_JUSTIFIED.** This is a selection of the current OSS reference for further acceptance, not a claim that its blocked Oracle/Jenkins runtime has passed.

The actual ODC lab is available and preserves its POC projects, project roles, five exact Oracle target registry IDs and historical tickets. It has the better integrated daily interface. Recovering it also establishes an important limit: four sampled historical tickets have unreadable logs and unavailable results/attachments despite preserved metadata and PVCs. Current Oracle effects and organization audit retention remain UNKNOWN.

ODC supplies substantial native inventory, approval, SQL review and history presentation. It does **not demonstrably retire any entire C1–C5 safety responsibility** under the full requirements. At least **four functional additions remain necessary**: immutable artifact/target binding, independent authorized dispatch/promotion, durable admission/replay/HOLD, and Oracle verification/reconciliation. Retained complete evidence is a **fifth unresolved responsibility**, potentially closable by supported storage configuration or bounded export. Even granting full native/configured C5 closure leaves four additions and an independent admission/recovery controller, which fails the user's simplicity threshold.

This count differs from a feature count: native project and approval screens are credited, but they do not eliminate the remaining invariant inside the same responsibility. A single implementation containing C1–C4 still owns four responsibilities. In particular, replay and partial/unknown recovery cannot be hidden inside a verifier or called a small script. No supported native contract was established that would safely remove those responsibilities without a replacement executor, workflow controller or deep authorization change.

CI already implements these boundaries for **one target on one restricted persistent agent**, with retained 30-test local evidence. Its Oracle T1–T7, authenticated Jenkins controls, operator acceptance, restore and promotion are still BLOCKED/NOT_RUN. Therefore **live correctness has no proved winner**; CI is the stronger implemented correctness/recovery reference, while ODC is the current UX winner. Evidence: [recovered lab](odc-current-lab-state.md), [retained CI results](../poc/results.md), [historical ODC results](../ODC-ORACLE-POC-RESULTS.md).

## 2. Current ODC lab state

The [current-state record](odc-current-lab-state.md) and [sanitized read-only capture](odc-current-lab-evidence-20261007.json) provide resource IDs, images/digests, ConfigMap key hashes, Secret names, registry records, actor roles, workflow and ticket readbacks.

| Question | Established current answer |
| --- | --- |
| Running where? | `k8s-admin-public`, Kubernetes API `api.k8s.drgdevlab.com:6443`, namespace `oceanbase-odc`; nginx Ingress → `odc:8989` |
| Healthy? | Endpoint HTTPS 200; ODC Deployment and MetaDB StatefulSet each 1/1 Ready; current pods Running, restart counts 0 |
| Product/build? | ODC **4.4.1-20260116**, image `4.4.1_bp1`, digest `ee8ee48…ead040d`; MetaDB tag `4.3.5-lts`, digest `31086a69…cdfcd2e3`; version-only binary read **OceanBase_CE 4.3.5.6** |
| Same lifetime? | No. Current MetaDB/ODC pods were created at 06:20/06:21 UTC today. Zero restarts on these pods do not erase earlier replacements |
| Persistent storage? | Same historical 5 GiB ODC and 10 GiB MetaDB PVC UIDs, both Bound. ODC `/opt/odc/log` is `emptyDir` |
| Oracle targets? | Five exact historical schema/database/datasource ID mappings preserved on one Oracle service; connection tests and live SQL intentionally not run |
| Current Oracle version? | UNKNOWN. Historical **26ai EE 23.26.4.1.0** is not a new observation or 19c/21c acceptance |
| Reusable? | **YES, conditional** for inspection/future focused testing. Oracle access/effects, evidence retention and full audit visibility still require confirmation |
| Previous artifacts? | 26 project tickets, 21 product-success/5 product-failure statuses; 14 detailed readbacks and 9 matched published SQL hashes |
| Retained execution evidence? | For 1000011/12/23/28: 4 log readbacks contain “read log failed”; 4 result and 4 attachment GETs return 500 |
| Organization audit/users? | Organization audit 403; organization users/roles/source administration visibility incomplete for the existing OWNER account. Historical 97 audit records do not prove current retention |

Inspection reused a local application credential; it did not read Kubernetes Secret payloads. Login/logout changed sessions only. Metadata GETs did not create database sessions or execute SQL. The initial wrong API paths were corrected from controllers; 404s from those probes are not capability gaps. Empty permission-scoped listings were not classified as deleted inventory.

## 3. Historical/current correlation

`PRESERVED` means a matching accessible record, pin or identifier, not re-executed acceptance. `CHANGED` means an observed difference. `MISSING` means a requested evidence retrieval is unavailable; it does not prove physical deletion. `UNKNOWN` means insufficient visibility/measurement.

| Item | Historical | Current | Same? | Evidence |
| --- | --- | --- | --- | --- |
| ODC version | 4.4.1-20260116 | Same `/api/v2/info` version | PRESERVED | [Historical results](../ODC-ORACLE-POC-RESULTS.md); current capture `successful_metadata` |
| ODC image | 4.4.1_bp1 at `ee8ee48…ead040d` in 3 October deployment capture | Same desired and running digest | PRESERVED | [Initial runtime](../evidence/product-model/odc-runtime-20261003.json); current capture `cluster` |
| MetaDB | CE 4.3.5 family, pinned `31086a69…cdfcd2e3` | Same digest; binary version now resolved as 4.3.5.6 | PRESERVED | Initial runtime; current binary/version capture. Exact historical binary suffix was not recorded; no upgrade inferred |
| ODC/MetaDB pods | Earlier recorded pods and operational replacements | Both current pods created 7 October | CHANGED | Initial runtime; current `cluster.pods` |
| PVCs | ODC UID `4f42837c…acad3`; MetaDB UID `669aee81…ccad` | Same UIDs, 5/10 GiB Bound | PRESERVED | [Historical PVC verification](../evidence/odc-oracle-portal-verification-20261004.json); current PVC capture |
| Oracle connection plugin | TCPS extension used during 4 October execution | Mounted plugin hash recorded; exact historical built hash unavailable | UNKNOWN | Historical result/wrapper account; current hash is discovery, not a proved extension byte match |
| Oracle target registry | One Autonomous host/service, five POC connections | Same service route, schema owners and exact IDs | PRESERVED | [Historical schemas](../evidence/oracle-poc-api.json); five current database detail responses |
| Oracle live identity/effects | 26ai EE 23.26.4.1.0 and historical postchecks | No SQL/connection test permitted this round | UNKNOWN | Historical postchecks retained; registry is not live target truth |
| Schemas | DEV/SIT/UAT/MOCKPROD/OBSERVER | Five exact registry records still exist | PRESERVED | Database IDs 1000069/1000122/1000184/1000218/1000345; actual objects/grants UNKNOWN |
| Projects | `odc-oracle-poc` 1; bootstrap 2 | Both in basic project list; project 1 detailed readback | PRESERVED | Current `successful_metadata`; bootstrap detail 403, detailed state UNKNOWN |
| Users/project roles | Requester 10000 DEVELOPER; approver 10001 OWNER; executor 10002 DBA; observer 10003 PARTICIPANT; admin OWNER | Same project membership and roles | PRESERVED | Current project detail. Organization role definitions and outsider account UNKNOWN |
| Approval workflow | High-risk OWNER→DBA; ticket 1000023 approved by 10001 then 10002 | Flow 4/risk level 4 and completed approval actors retained | PRESERVED | [Historical manual approval](../evidence/oracle-poc-manual-approval.json); current risk/flow/ticket readbacks |
| Test tickets | Historical SQL/governance/recovery tickets | IDs 1000003–1000028 listed; 14 selected details readable | PRESERVED | Current `ticket_inventory` and `ticket_readbacks` |
| Ticket SQL | Published artifact SHA-256 and client-side comparison | Nine selected comparable current SQL digests match | PRESERVED | Historical API/manual records; current hash comparisons. This does not prove a native immutability gate |
| Logs | Historical post-restart “read log failed” | Same symptom on four sampled tickets | MISSING | Current `evidence_retrieval`; both reports describe unreadable evidence |
| Results/attachments | Historical old-ticket downloads returned 500 | Four result and four download endpoints return 500 | MISSING | Same current retrieval sample; not an inferred successful retention repair |
| Audit records | 97 POC audit entries published | Current search denied, HTTP 403 | UNKNOWN | [Historical audit sample](../evidence/oracle-poc-review.json); current restricted-visibility capture |

The [source survey](research-round-2/coordinator/odc-source-survey-20261006.md), [baseline requirements](current-baseline.md) and [rejection register](rejection-register.md) identify earlier hypotheses and failures; their labels did not decide this round. Current public repository HEAD was separately read as `d517c0f27971642fb0cd7565fd61ab2309875ec3`, matching the inspected local source. That commit still lacks an exact mapping to the deployed binary and TCPS extension. Historical PASS cases remain retained evidence for this build/topology; failure cases remain evidence too. Neither was rescored.

## 4. CI reference responsibilities

The reference is the implemented [README](../poc/OSS-POC-README.md), [architecture](../poc/architecture.md), [test plan](../poc/test-plan.md) and [results](../poc/results.md), with Flyway Community **13.9.0** and existing Jenkins **2.568.3-jdk21**. The following grouping normalizes implementation packages to the mission's five functional responsibilities; package count is not the burden measure.

| Responsibility | Implemented ownership | Evidence/remaining boundary |
| --- | --- | --- |
| C1 Inventory and immutable artifact/target binding | Protected stable target inventory; exact Git SQL/expectation bytes; canonical envelope includes resolved identity/schema/route, requester, engine/driver pins/options; approval hash; revalidation before dispatch | [targets.py](../poc/inventory/targets.py), [artifact.py](../poc/runner/artifact.py), [store.py](../poc/state/store.py). One disabled example target; operator configuration/live identity still unconfirmed |
| C2 Actor/approval/promotion policy | Jenkins named requester and actual input submitters; reviewer/requester/executor separation; protected policy checked again at dispatch | [Jenkinsfile](../poc/ci/Jenkinsfile), [workflow.py](../poc/runner/workflow.py). One reviewer also serves as approver. Real server RBAC/actors are BLOCKED; **promotion is DESIGN, not implemented** |
| C3 Durable admission/serialization/HOLD | Permanent release ID, unique canonical schema/version; SQLite transaction and schema guard; local nonblocking execution lock; RUNNING before engine start; orphan UNKNOWN; non-success guard retention; authorized closure, no automatic replay | [store.py](../poc/state/store.py), workflow. Real SQLite/process-loss local evidence; one POSIX agent/state authority, not a distributed service or proved restore protocol |
| C4 Oracle verification/reconciliation | Fixed Flyway invocation; actual-connection identity guard; separate observer checks exact object owner/name/type including PACKAGE BODY, status/errors and approved effects; uncertainty remains held; readback reconciliation plus DBA session/history/effect attestation | [engine.py](../poc/runner/engine.py), [GuardedDataSource.java](../poc/runner/java/src/main/java/org/example/poc/GuardedDataSource.java), [oracle.py](../poc/verifier/oracle.py), workflow. Oracle adapters in safety tests are fakes; session/history closure remains DBA-owned |
| C5 Central retained result/audit presentation | Protected SQLite exact SQL/envelope/actors/status/audit; escaped HTML/JSON/SQL projections and Jenkins archives | [render.py](../poc/reports/render.py), Jenkinsfile. Local report evidence only; protected agent, archive retention/backup/restore acceptance still incomplete |

**CI reference owned critical responsibilities = 5.** Flyway contributes parser/executor/schema history; Jenkins contributes UI and authenticated input primitives. The team owns the five glue/correctness boundaries, engine wrapper upgrades, configuration and operations. No report or SQLite mechanism makes these costs disappear. Local tests prove specific mechanics, not all Oracle behavior or enforceability on an unconfigured server.

## 5. ODC responsibility mapping

Classification applies to the complete requirement; component capabilities are credited separately. `EXTERNAL CUSTOM` means custom ownership is required to supply the missing behavior, **not** that a safe supported integration has been demonstrated. `UNSUPPORTED` below is limited to the reviewed control path, not every possible later ODC edition.

| Responsibility | Whole-requirement classification | Native/configured contribution | Addition and retirement verdict |
| --- | --- | --- | --- |
| C1 | EXTERNAL CUSTOM; final immutability contract UNKNOWN | NATIVE datasource/project/database inventory and SQL/target-bearing tickets; CONFIGURATION environments/owners | Approved SQL/options/target bytes must be frozen and checked against dispatch and live identity. No native content digest/version enforcement proved. **Retires inventory UI, not the entire inventory/envelope layer** |
| C2 | EXTERNAL CUSTOM; creator exclusion UNSUPPORTED in reviewed native execution policy | NATIVE actors, project roles, approval nodes and MANUAL wait; CONFIGURATION OWNER→DBA routing | Independent requester/reviewer/executor dispatch and verified stage policy remain owned. No supported narrow policy hook was established across native write paths. **Does not retire actor/promotion policy** |
| C3 | EXTERNAL CUSTOM; partial/unknown stream HOLD contract UNKNOWN | NATIVE durable ticket/task state, rejection of Execute on a completed ticket, configurable retry count, ordered batch scheduling | Cross-ticket release identity/checksum/replay exclusion, canonical schema admission and durable failure/uncertainty barrier need an independent ledger/controller absent a new native contract. **Cannot retire SQLite admission/state/lock** |
| C4 | BOUNDED EXTENSION for object verifier; EXTERNAL CUSTOM for authoritative completion/reconciliation | NATIVE Oracle execution and separate PL compile/development tools | A dictionary/effect verifier can be small; making its result veto native completion/promotion and drive recovery is a separate integration/control obligation. **Cannot retire most verifier/reconciliation ownership yet** |
| C5 | CONFIGURATION candidate for retention; BOUNDED EXTENSION candidate for export; full closure UNKNOWN | NATIVE ticket SQL/target/actor/time/history, results/log/attachment endpoints, audit search/export surfaces | Durable complete evidence and reliable retrieval across replacement/restore remain unresolved. **Can replace report UI; cannot presently retire retained audit/evidence responsibility** |

### C1: inventory and final binding

Current exact IDs, environment mapping and matching ticket SQL hashes are positive native evidence. Reviewers have SQL and target in one ticket. Historical MODEL-05 passed visible target/SQL review; MODEL-06 only showed an unsupported direct PUT route, not that all mutation paths were sealed. Client-calculated SHA-256 in a description and matching SQL today are not server-enforced binding, upload immutability or route/schema drift protection. Release options, file bytes, credential/route/schema references and final target sets need immutable approval binding. Wrong-target live-session validation remains UNKNOWN. Thus the custom **inventory screen** could disappear, but the correctness envelope cannot. [Historical API/manual evidence](../evidence/oracle-poc-api.json), [MODEL-03/06](../ODC-ORACLE-POC-RESULTS.md).

### C2: separation across execution paths

Current OWNER and DBA nodes and MANUAL tickets prove approval routing and a human Execute step. Historical GOV-03 proved requester Execute returned 200 after approval; the record still survives. The reviewed [FlowPermissionHelper](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/FlowPermissionHelper.java#L83-L100) allows the creator, otherwise project OWNER/DBA. [FlowTaskInstanceService](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/FlowTaskInstanceService.java#L174-L199) uses that predicate for native Execute. This is intended authorization behavior, not a bypass exploit.

Removing an Execute button or putting a gate before a caller does not remove creator API rights. Console development, scheduler/AUTO execution, privileged project roles, admin override and inherited/global roles need the same policy coverage. Current native configuration covering all of them is UNKNOWN; historical read-only participant/revoke tests cover only a subset. A supported narrow authorization extension could be bounded if demonstrated. An authorization fork, replacement executor or controller which owns approvals/promotion would fail this mission's threshold. [Historical governance](../evidence/oracle-poc-governance.json), [original results](../ODC-ORACLE-POC-RESULTS.md).

### C3: admission and durable HOLD — decisive gap

Historical REC-02/08/10 separately established SQL replay, changed content submitted under the same client identity, and two duplicate tickets/effects. Native refusal to execute **one completed ticket again** is credited but does not reject **another ticket for the same release**. Byte-identical submissions need a durable identity plus target/version policy; any same-content reuse policy must be explicit, because intentionally new releases can legitimately share bytes. CI enforces release/schema-version uniqueness, not a blanket global SQL-hash uniqueness rule.

The pinned [DatabaseChangeThread](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/task/DatabaseChangeThread.java#L141-L280) iterates SQL and optionally retries statement failures. [DatabaseChangeParameters](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/task/model/DatabaseChangeParameters.java#L34-L55) defaults `retryTimes=0`, also preserved on the sampled POC tickets: disabling retries is ordinary configuration and is credited. It does not provide cross-ticket admission, a permanent failed-release barrier or reconciliation before a new ticket.

Historical concurrent same-target tickets both completed; without lock/commit instrumentation that proves neither overlap nor safe serialization. Batch ordering is distinct from locking all independently submitted work on a canonical database/PDB/schema, including service aliases and console/API/scheduler writes. The scoped execution review does not establish such a lock or a durable unknown-outcome HOLD. ODC's own metadata migration/checksum framework is not Oracle target release admission. Consequently retiring C3 requires a supported native contract that is not currently evidenced; constructing it externally would be the expressly excluded controller.

### C4: verifier versus release controller

Valid procedure/function/package/trigger/block execution has retained historical PASS evidence. SQL-11 has equally concrete historical failure evidence: ticket 1000011 succeeded while Oracle's procedure was INVALID with PLS-00201. Current readback preserves that success record without rechecking the object. The pinned [statement callback](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/session/OdcStatementCallBack.java#L275-L329) creates JDBC-success results; the examined worker does not establish a native `ALL_OBJECTS`/`ALL_ERRORS` completion check. [DBPLService](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/db/DBPLService.java#L196-L245) supplies separate compile operations, not an evidenced authoritative change-ticket veto.

A bounded verifier must check expected exact owner/name/type, PACKAGE BODY separately, function/procedure/trigger validity, ERROR diagnostics and approved data effects. It must report uncertainty rather than success on missing visibility/result loss. Partial DDL additionally requires session/history/effect reconciliation; an object being VALID cannot tell whether every intended DML/DDL effect occurred exactly once. No supported hook has been established that receives the immutable approved input, blocks native success/next-stage execution, durably holds the stream and records verified closure. A standalone postcheck can assist a DBA, but cannot replace that control contract. [Historical SQL-11/REC-04 evidence](../ODC-ORACLE-POC-RESULTS.md), [source survey](research-round-2/coordinator/odc-source-survey-20261006.md).

### C5: native interface, incomplete retained truth

ODC offers the strongest native result/history experience here. Current project/ticket metadata retains SQL, target, creators, approval operators and timestamps. SQL hashes in the capture are calculated locally from readback content; they are not native checksum enforcement. Historical audit recorded 97 POC entries; current audit search/export is permission-blocked and UNKNOWN. The four current failed log/result/download retrievals show a concrete retention gap. A native HTTP-200 fallback string must not be treated as a recovered log.

The reviewed [logger service](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/FlowTaskInstanceLoggerService.java#L82-L147) can forward retrieval to a task's recorded executor host and substitutes fallback text on errors. [ScheduleLogProperties](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/schedule/ScheduleLogProperties.java) makes the log directory configurable. This supports considering a storage/retention configuration remedy rather than assuming a new reporting application is necessary. It does not prove that a mount change repairs old-host routing or missing results. Native storage configuration and a narrow export could close C5; this round neither changes them nor assumes success. Even granting that closure does not change C3 or the final threshold.

## 6. Custom burden comparison

| Responsibility | CI/Flyway reference | ODC native | ODC addition required |
| --- | --- | --- | --- |
| Inventory/binding — C1 | Custom frozen inventory/envelope and dispatch checks | Inventory/project/environment/ticket SQL and target selection | Frozen final artifact/options/target and dispatch integrity contract; owned correctness remains |
| Approval/actors — C2 | Custom policy joining Jenkins identities and stage rules; promotion not implemented | Role/approval workflow and MANUAL wait | Independent execution and all-write-path policy; verified predecessor/promotion policy. Supported narrow enforcement UNKNOWN |
| Admission/replay — C3 | Custom SQLite/OS-lock admission, schema guards and HOLD closure | Workflow/task persistence, per-ticket lifecycle, batch order, retry setting | Durable release/checksum admission, canonical schema serialization, unknown/partial HOLD and recovery authority; **independent controller required absent new native contract** |
| Oracle verification — C4 | Custom guarded engine/observer, diagnostics/effects, bounded reconciliation | Executor and separate development/compile tools | Verifier plus authoritative completion veto/reconciliation. Verifier alone is bounded; missing recovery control is not |
| Audit/results — C5 | Custom retained state/audit and HTML/JSON projections | Ticket/history/result/audit UI and retrieval/export APIs | Retention configuration/retrieval proof, or bounded durable evidence export; current full closure UNKNOWN |

```text
CI/Flyway owned critical responsibilities = 5
ODC owned additions required = 4 confirmed functional responsibilities (C1–C4)
                               + 1 unresolved retention/evidence responsibility (C5)
ODC fully native/configured responsibilities retired with evidence = 0 of 5
ODC best-case count if native/configured C5 is accepted = 4
```

This is a minimum required-ownership assessment, not a count of completed extensions. C2/C4 supported integration feasibility is itself unproved. C3 includes recovery admission; C4 includes observing Oracle truth, so the same uncertainty is not counted as an extra sixth “recovery module.” The existing TCPS adapter adds a connectivity/upgrade obligation but is **not** counted as a sixth C responsibility. Retiring inventory and report screens is valuable UX reduction, yet does not imply retirement of their entire safety contracts.

## 7. Failure-handling comparison

Labels describe the strongest evidence for **handling this scenario**: `NATIVE PROVEN`, `HISTORICAL RUNTIME`, `SOURCE ONLY`, `DESIGN`, `UNKNOWN`. A historical runtime label can describe a failure, not just a pass. Local tests are noted within `SOURCE ONLY` and are never relabeled Oracle runtime. `NATIVE PROVEN` is unused where only historic execution or current metadata is available.

| Scenario | ODC evidence class and observed handling | CI reference evidence class and implemented handling | Remaining acceptance |
| --- | --- | --- | --- |
| F1 Valid PL/SQL | HISTORICAL RUNTIME: procedure/function/package/body/trigger/block/slash passed; corresponding ticket metadata preserved | SOURCE ONLY: real Flyway parser plus mock verification; fixed migration wrapper/observer implemented | CI live T1 and package/body regression BLOCKED/NOT_RUN; exact current Oracle behavior not re-executed |
| F2 INVALID procedure/package body | HISTORICAL RUNTIME: procedure INVALID yet ticket success (SQL-11 FAIL); package-body invalid handling UNKNOWN | SOURCE ONLY: exact-type status/ERROR diagnostics veto success; PACKAGE BODY supported as distinct expected type, local fake tests | CI T2 BLOCKED; ODC later binary/package-body INVALID behavior UNKNOWN |
| F3 Duplicate release | HISTORICAL RUNTIME: REC-02/10 replay/new duplicate tickets caused extra execution/effects; completed-ticket Execute denied | SOURCE ONLY: permanent release ID/schema-version uniqueness and no terminal redispatch, tested with real SQLite | CI T3 BLOCKED; distinguish one completed ticket from another identical release request |
| F4 Changed content/same identity | HISTORICAL RUNTIME: REC-08 submitted changed SQL as new ticket; client ID/hash not enforced | SOURCE ONLY: changed envelope under permanent identity rejected before Oracle, tested locally | CI T4 BLOCKED; ODC immutable release identity missing from observed workflow |
| F5 Wrong schema/target | UNKNOWN for live mismatch rejection: native UI registry/role checks and correct historical target selection exist; deliberate drift not proved | SOURCE ONLY: allowlist/envelope comparison, observer identity preflight and actual Flyway-connection guard | CI T5 BLOCKED; ODC UI target selection alone is not live identity verification |
| F6 Partial DDL | HISTORICAL RUNTIME: earlier CREATE persisted, later ALTER failed, ticket failed; no accepted release barrier/reconciliation | SOURCE ONLY: conservatively PARTIAL after engine SQL failure, retains guard; no retry/rollback promise | CI T6 BLOCKED; real Oracle history/forward-fix operation needs DBA acceptance |
| F7 Lost ACK / UNKNOWN | UNKNOWN: historical fault-instrumented cases NOT_RUN; no evidenced all-stream HOLD contract | SOURCE ONLY: RUNNING-before-start, fake engine subprocess exits before recording, durable orphan UNKNOWN/no replay proved locally | CI real T7 BLOCKED; neither has live lost-ack reconciliation proof |
| F8 Restart / restore | HISTORICAL RUNTIME for retention failure: current replacement preserves metadata/PVCs, old results/logs fail. Controlled running-task restart/backup restore UNKNOWN | DESIGN for restore: disable inventory, restore coherently, inspect history/sessions/effects before reopening. Local process-state persistence is SOURCE ONLY | Both full restore/restart recovery NOT_RUN; current pod replacement is not a crash/restore PASS |
| F9 Concurrent same-target execution | HISTORICAL RUNTIME: two submissions completed, but overlap/lock boundaries uninstrumented; serialization UNKNOWN | SOURCE ONLY: one-agent flock, SQLite unique guard and transactional concurrent-admission tests; Jenkins also disables concurrent builds for that job | No distributed claim; same canonical schema via service aliases must be proved in authorized live scope |
| F10 Requester executes after approval | HISTORICAL RUNTIME: GOV-03 FAIL, requester accepted after OWNER→DBA approval; source intentionally permits creator | SOURCE ONLY: authenticated-input design plus independent actor/role rechecks, local rejection tests | CI actual named identities/server RBAC BLOCKED; ODC all-path separated execution contract unestablished |

Neither architecture can undo Oracle committed DDL by rolling back its control metadata. Both need a DBA to distinguish committed effects, active sessions and stale records before a reviewed forward fix. CI implements a conservative admission barrier; its procedure and observer are still awaiting live acceptance. Historical totals **12 PASS / 20 PARTIAL / 5 FAIL / 8 NOT_RUN** and all CI blocked case records remain unchanged.

## 8. UX comparison

These are system-boundary counts for the recorded journeys, not measured click counts or operator timings. ODC has historical API/UI execution and current metadata evidence; the CI workflow is implemented but its live user journey is **not yet observed**. A report served as a Jenkins build artifact is part of Jenkins for these counts, not an invented third application. Adding Git review to ODC would add another routine system, but Git is not required by its native ticket journey.

```text
ODC: Login → project/database → ticket → review → approval → execute → results/history
CI:  Git → Jenkins → approval → execution → HTML/JSON build artifacts
```

| Role | ODC routine systems / target selections | CI routine systems / target selections | Review and results | Recovery location |
| --- | --- | --- | --- | --- |
| Developer/requester | 1: ODC. One target choice for a single-target ticket; individual multi-environment tickets repeat selection, native batch/template can reduce repetition | 2: Git + Jenkins. One allowlisted target choice in this POC; no environment-promotion implementation | ODC ticket SQL/target and native history; CI Git diff plus exact frozen SQL/envelope at Jenkins gate, then archived HTML/JSON | ODC ticket first, DBA if effects uncertain; CI held report first, DBA/runner for closure |
| Reviewer/approver | 1: ODC; 0 new target choices, reviews submitted target. OWNER and DBA approval nodes may involve two people | 1–2: Jenkins exact artifact gate, Git for change context; 0 new target choices. One reviewer also approves | ODC SQL/task detail; CI protected-state SQL/hash/target/expectation preview. Current ODC result attachments unavailable for sampled old work; CI report UX runtime unproved | Held/missing evidence escalated to DBA; no reviewer clearance of Oracle uncertainty |
| DBA/executor | Routine ticket path 1: ODC; 0 new target choices, checks submitted target. Safe independent role policy unresolved | Routine execution path 1: Jenkins; 0 new target choices, confirms approved target. Policy implemented, actual UI/RBAC acceptance pending | Native ODC results would be easier when retrievable; CI linked structured report names INVALID/PARTIAL/UNKNOWN | ODC + Oracle admin tool at least 2 systems, with extra recovery authority required; CI Jenkins report + restricted runner/state + Oracle admin tool at least 3 surfaces |
| Platform owner | Normally ODC admin + Kubernetes/GitOps (at least 2 surfaces), plus MetaDB/backup tooling during incidents | Git + Jenkins/agent administration (at least 2), plus state/backup/Oracle tooling during incidents | ODC role/workflow/storage administration; CI protected job/installed runner/config and evidence retention | ODC pod/MetaDB/adapter/log routing plus missing controller; CI restricted agent/SQLite/Flyway history/report regeneration |

**UX WINNER: ODC for normal request/review/result navigation.** It avoids the Git-to-CI handoff for native tickets and integrates inventory, SQL and actors. Its present results and recovery journey is incomplete, so this is not a safe-operation endorsement. CI has more explicit held-state evidence semantics but places more work on Git/Jenkins/DBA operators. Neither has measured daily-use acceptance for a 50-instance/20-user estate.

ODC batch serial/parallel ordering is a real native feature; it should be credited as potential workflow reduction. It is not the same as verified predecessor promotion or global target admission. [Official batch documentation](https://en.oceanbase.com/docs/common-odc-10000000001510652).

## 9. Operational complexity

LOW/MEDIUM/HIGH/VERY HIGH are qualitative ownership estimates for this existing lab/reference, not measured incident rates or costs. Shared Oracle/cluster/GitOps infrastructure is not charged twice. An existing service still requires upgrades, backup and incident ownership; a prepared codebase is not a deployed restricted agent.

| Dimension | ODC native today | ODC with required safe-workflow closure | CI reference after necessary operator setup |
| --- | --- | --- | --- |
| Deployed components | MEDIUM: one ODC deployment and one OceanBase MetaDB StatefulSet, plus mounted TCPS adapter | VERY HIGH: native stack plus admission/recovery authority and policy/verification integration; topology not safely specified | MEDIUM: existing Jenkins controller plus one restricted persistent agent/installed runner; no new server/queue/metadata service |
| Persistent stores | MEDIUM: MetaDB 10 GiB + app data 5 GiB; logs currently ephemeral | HIGH: MetaDB/files plus a separate release admission store and retained evidence unless native closure demonstrated | MEDIUM: Git, Jenkins home/archives, protected local SQLite/WAL, Flyway target history; coordinated backup still mandatory |
| Upgrade domains | HIGH: ODC binary/driver/parser, CE MetaDB, TCPS plugin/wrapper and Kubernetes deployment | VERY HIGH: add controller contracts, authorization changes and verifier/export compatibility | HIGH: Jenkins/JDK/plugins, Python package/observer, Flyway API wrapper/parser and external Oracle driver. Internal Flyway APIs require regression |
| Backup and restore | HIGH: both PVCs, logs/files, credentials/config, task routing and Oracle reconciliation; current retention gaps | VERY HIGH: coherent restores across native workflow and added admission/evidence authorities | HIGH: online SQLite backup, Git/config/engine pins, Jenkins artifacts/credentials; disable dispatch after stale restore and reconcile Oracle |
| Credentials | MEDIUM/HIGH: application accounts, datasource writers/observer, MetaDB/bootstrap, TCPS policy; organization controls incompletely visible | HIGH: additional integration identities and restrictions on every bypass write path | HIGH: separated writer/observer bindings, restricted OS agent, actor roles, config/backup confidentiality; actual credentials not assigned |
| Custom code ownership | LOW for existing adapter alone; **incomplete workflow** | VERY HIGH: C1–C4 required, C5 unresolved, possible unsupported policy/completion fork | HIGH: five explicit owned responsibilities, co-located bounded package; no general platform/control-plane build |
| DBA incident surfaces | HIGH: ticket success may mask INVALID; partial effects, missing logs, session pressure and unresolved replay/HOLD | VERY HIGH: must reconcile Oracle plus native tasks and added release controller | HIGH: explicit INVALID/PARTIAL/UNKNOWN guard and forward-fix obligations; live usability/reconciliation unaccepted |
| DevOps ownership | HIGH: ODC/MetaDB provisioning, adapter build/mounts, retention/routing, task integration | VERY HIGH: additionally owns independent control contracts across native workflow/executor/state | HIGH: protected job, restricted agent/config/SQLite, installed Python/Java pins, retention and Jenkins upgrades |
| State authorities | MEDIUM for native metadata presentation; required release/effect authority incomplete | VERY HIGH: Oracle + MetaDB + new admission state + files/audit join, unless product contracts eliminate a store | HIGH: one SQLite release/admission authority + Oracle effects/Flyway history; Jenkins/report/Git are projections/provenance, not competing verdict authorities |

**OPERATIONAL SIMPLICITY WINNER: CI for the complete required operating model, conditionally on single-agent setup.** **ODC wins native interface integration and has less current custom code because its required safety closure is absent.** Comparing the incomplete native lab against complete CI ownership would undercount ODC's cost. The CI reference itself is not LOW complexity; its five responsibilities and operator duties are material. At estate scale CI expansion is DESIGN, so no scale/capacity winner is claimed.

## 10. State-authority comparison

| Question | ODC native / additions | CI reference |
| --- | --- | --- |
| What identifies approved content? | Ticket SQL/files/options/target in MetaDB; immutable release-level envelope contract unproved | Protected SQLite exact SQL and canonical envelope binding; Git supplies provenance |
| Who admits a release? | Native task lifecycle admits tickets; separate release/schema admission authority still required for the goal | SQLite registration/claim + one local execution lock |
| What authorizes next work after a failure? | Native failed/success ticket state does not establish all-stream barrier or reconciliation; added controller must own that decision | Non-success retains schema guard; authorized readback/DBA attestation closes to permanent HOLD; new identity required |
| Who owns Oracle truth? | Oracle owns effects; ticket JDBC success is insufficient for object validity/complete effects | Oracle owns effects/history; observer evidence can verify expected results, but does not rewrite failed/unknown engine outcomes |
| Is history the ledger? | Ticket ID is workflow identity; duplicate new tickets are possible. Native MetaDB migration history is not target release admission | SQLite is release authority; Flyway history is engine fact; both need reconciliation after stale restore |
| Can presentation become authority? | Native result screen cannot become verified release truth without completion/HOLD contract; external report alone cannot veto native dispatch | HTML/JSON/Jenkins status are projections. Stale post-crash report must be regenerated from protected state |
| Restore hazard | Restored native task state/files may disagree with Oracle; added release state creates another disagreement domain | Restored SQLite may forget committed work; inventory must remain disabled pending DBA reconciliation. Restore procedure not yet proved |
| Bypass paths | Native console/API/scheduler/privileged execution require consistent restrictions; an external gate alone does not restrict creator Execute | Restrict agent/credentials/job definition and Oracle writer; raw trusted-operator CLI actor arguments are assertions, not authentication; unmanaged writes still invalidate assumptions |

ODC ticket history is a genuine native durable workflow facility. It must not be conflated with the required idempotent release/admission authority. The team would otherwise own the state joins and failure ordering that CI already makes explicit. Neither architecture supplies an atomic transaction encompassing Oracle DDL and control-state recording.

## 11. ODC simplicity threshold

| User rule | Current finding |
| --- | --- |
| Retire at least three of five responsibilities | No three complete retirements established; C1 inventory and C5 presentation are substantial partial replacements |
| At most two bounded additions | Minimum four remaining responsibilities, plus unresolved C5 evidence retention |
| No separate release controller or durable admission ledger | C3 closure currently requires one absent a new supported native contract; this alone disqualifies the simplicity win |
| No external workflow state machine, replacement executor, deep fork or direct MetaDB mutation | None was built or proposed as an accepted solution. Available evidence does not establish a bounded native policy/completion path avoiding them |
| Small verifier/export can be acceptable | Yes, credit these as possible bounded C4/C5 pieces; they do not fix binding, creator execution or C3 admission/recovery |

**ODC does not win the supplied simplicity test.** This follows current preserved runtime behavior, current source-path review and remaining owned responsibility boundaries; it does not follow from the earlier HOLD label. Even an optimistic grant of native C1 inventory, C2 approval UI and C5 report UI does not retire their complete binding/authorization/retention contracts. Even granting complete C5 closes only one responsibility and leaves the independent controller exclusion.

Current public capability was rechecked as a possible alternative to the historical build. The official **4.5.0** note lists MCP/OpenAPI, package parsing, multi-node scheduling and batch fixes, as well as upgrade cautions. These are relevant improvements; the note does not establish release checksum admission, independent requester execution exclusion or authoritative Oracle UNKNOWN/HOLD closure. The lab remains 4.4.1. No exact later build/control contract was supplied or deployed. This is an unproved closure, not a claim that later binaries cannot contain additional capabilities. [Official ODC 4.5.0 note](https://www.oceanbase.com/docs/common-odc-1000000006663615).

## 12. Runtime-test eligibility

**ODC_RUNTIME_NOT_JUSTIFIED for renewed Oracle safety testing in this round.** The lab's availability is not the disqualifier: it is healthy and conditionally reusable, and its metadata preserved useful historical evidence. The missing responsibility/control closure is decisive.

| Eligibility requirement | Result |
| --- | --- |
| Healthy reusable lab | PARTIAL: application/MetaDB healthy and registry/tickets reusable; live Oracle readiness UNKNOWN and old evidence unavailable |
| At least three full retirements | Not established |
| No more than two bounded additions | Not met: C1–C4 remain, C5 unresolved |
| No fork/controller build | Not established; C3 requires independent admission/recovery without a product delta |

A focused experiment is justified only after a mapped product build/configuration/extension contract appears to own release admission/recovery and separated dispatch, with no more than two bounded residual responsibilities. Better UI or a repaired log mount alone would not make that test eligible. Current unknowns do not justify replaying known failures on unchanged contracts.

## 13. Focused runtime plan if eligible

**Not eligible; no new runtime plan is defined or executed.** If a later mapped native contract meets section 12, define only the requested R1 INVALID object, R2 duplicate/replay, R3 changed content, R4 requester/executor separation, R5 partial DDL, R6 concurrent target, R7 restart/retention and R8 unknown-outcome/recovery cases. Retain historical PASS cases unless a material executor/parser/plugin/build change invalidates their scope. A second controller/ledger or direct MetaDB mutation would stop eligibility before testing. No unchanged 45-case rerun or ODC implementation backlog is proposed here.

## 14. Final OSS recommendation

Keep **the implemented Jenkins/Flyway reference as the current OSS acceptance path**, subject to the existing runtime blockers. Preserve ODC's healthy lab, native UX evidence and historical records for a concrete future product-contract delta; do not build an ODC control-plane fork or attach another migration executor in this round.

Next bounded action is to obtain the required approved CI/Oracle/source/identity references and resolve the external Oracle JDBC dependency policy, then separately authorize and execute existing **single-target T1–T7** and real Jenkins UX/role/retention acceptance. This reassessment grants no runtime permission. Do not silently reuse ODC credentials as CI credentials: a visible inventory record is not authorization to borrow its writer or observer.

Adoption still requires maintainers to accept five owned responsibilities, live failure/recovery and restore evidence, real role enforcement and usable retained results. Multi-environment promotion and the 50-instance/20-user estate remain future acceptance, not completed CI functionality. If CI's actual operator burden is unacceptable, neither current path is accepted; return to a supported native product delta instead of calling unproved CI runtime a win. [CI results and blockers](../poc/results.md), [single-target plan](../poc/test-plan.md).

## 15. Evidence and unknowns

| Evidence | What it supports / limits |
| --- | --- |
| [Current lab state](odc-current-lab-state.md), [new sanitized capture](odc-current-lab-evidence-20261007.json) | Current resources/pins/PVCs, project metadata/roles, approval flows, exact registry IDs, ticket/SQL-hash retention and failed evidence retrieval. No SQL or live Oracle identity proof |
| [Historical ODC results](../ODC-ORACLE-POC-RESULTS.md), [API](../evidence/oracle-poc-api.json), [governance](../evidence/oracle-poc-governance.json), [manual approval](../evidence/oracle-poc-manual-approval.json), [postchecks/audit](../evidence/oracle-poc-review.json) | Exact past Oracle/build cases, including passes and failures. Unchanged totals/observations; historical effects are not current postchecks |
| [Baseline](current-baseline.md), [rejection register](rejection-register.md), [source survey](research-round-2/coordinator/odc-source-survey-20261006.md), [previous public-delta review](decision-closing/odc-public-delta.md) | Requirement/state-authority definitions and previous investigation scope. Older recommendation labels do not determine this result |
| Pinned ODC source links in C2–C5 | Specific creator authorization, statement retry/success, separate PL compile, batch status and log retrieval behavior. Source HEAD independently rechecked; exact image/plugin correspondence UNKNOWN |
| [Official batch docs](https://en.oceanbase.com/docs/common-odc-10000000001510652), [4.5.0 note](https://www.oceanbase.com/docs/common-odc-1000000006663615), [4.4.2 note](https://www.oceanbase.com/docs/common-odc-1000000006663623) | Native ordering and later improvements; upgrade notes identify state/history migration concerns. Docs are not acceptance on the unchanged 4.4.1 lab |
| [CI architecture](../poc/architecture.md), linked actual implementation modules, [test plan](../poc/test-plan.md), [results](../poc/results.md) | Implemented one-target mechanics, retained local evidence, explicit runtime/setup/license/promotion limits |
| [Retained local check record](../poc/reports/local-20261007T090057.153281_0000/checks.json) | 30 local tests and parser/build evidence; real SQLite, fake Oracle adapters. Historical tests were not rerun for this documentation-only round |

Material unknowns: current Oracle identity/version/connectivity/grants/effects; outsider and organization-role state; audit retention/export and actual Execute caller joins; exact TCPS/plugin historical byte identity and binary-source mapping; full post-approval mutation surface; native all-path separation, cross-ticket/schema admission and UNKNOWN recovery; retention failure root cause/configuration closure; protected Jenkins job/agent/actors/credentials; driver-policy decision; real operator UX; full backup/restore; estate/version compatibility and promotion.

Verification for this round is limited to document/link/table integrity, current-evidence consistency, a credential/redaction scan and preservation hashes. Repository root has no Git metadata, so final review uses the saved pre-edit hashes and index diff. The original test/result/source records remain authoritative for their own dates; no new Oracle/Jenkins PASS is manufactured.
