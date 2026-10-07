# ODC practical adoption POC — 7 October 2026

**ODC practical POC = GO for the internal native-workflow pilot using the demonstrated retention configuration and accepting approved requester dispatch.** The role-separated approval journey, native four-environment batch and its manual failure boundary, intended Oracle/TCPS path, explicit DBA validity check, correction tickets and API provenance were demonstrated. The baseline ordinary replacement test **FAILS on the unchanged deployment**: metadata/SQL/audit survive, but new logs/results/downloads are unavailable. The separately authorized [final retention experiment](odc-retention-experiment.md) proves the supported storage/executor-identity configuration with fresh successful/failed tickets after another ordinary replacement. Results, statement output, logs, ZIPs and audit are preserved. The lab and Argo CD were restored afterward; apply the supplied minimal GitOps settings before pilot operation.

The original A–E runtime created **12 new tickets, 2000001–2000012**, in existing isolated project 1. The final retention experiment adds exactly **two**, 2000013/2000014, without rerunning A/B/C/E. All are terminal: successful, intentionally failed or cancelled. The 26 historical tickets, 1000003–1000028, retain their statuses and SQL hashes. No historical results were rewritten. No production targets, external runner, Flyway/Jenkins executor, controller or Bytebase rerun were used. The baseline replacement remains its original result. The final experiment temporarily paused only the ODC Argo application, patched/rolled/replaced only ODC, then restored the exact original configuration and reconciliation. MetaDB, PVCs and Service remain unchanged. The [plan](odc-practical-poc-plan.md), [case records](../evidence/odc-practical-poc-20261007/cases.json) and [dated evidence](../evidence/odc-practical-poc-20261007/) provide the full scope and records.

## Readiness and exact runtime

The [readiness capture](../evidence/odc-practical-poc-20261007/readiness.json) confirms four legitimate role authentications, five exact existing datasource/schema mappings, 26 preserved historical tickets, restricted writer grants and a live read-only observer. ODC and MetaDB are ready with bound existing PVCs; see [cluster capture](../evidence/odc-practical-poc-20261007/cluster-before.json). Current metadata reads and successful new task creation/execution substantiate MetaDB availability without querying or restarting it directly.

| Item | Observation |
| --- | --- |
| ODC | 4.4.1-20260116; image digest `ee8ee48edea2907b1b2c11eac54c8603e554bdcc570eb11b0b1f9cef2ead040d` |
| MetaDB | Existing OceanBase CE 4.3.5.6 lab; pinned image digest `31086a6900c21c479c2bcd942b6a28c53b17a51f4e9b9eb8eafcc596adfcd2e3` |
| Oracle, live | Oracle AI Database 26ai Enterprise Edition 23.26.4.1.0; confirmed independently through each writer's ODC session |
| Oracle service / PDB | `GAF051B0A6547F3_LABDB_tp.adb.oraclecloud.com` / `GAF051B0A6547F3_LABDB` |
| Protocol | `SYS_CONTEXT('USERENV','NETWORK_PROTOCOL')=tcps` for all four writer sessions and the observer; valid-function postcheck uses the same ODC path |
| Connector during A–E | Existing mounted `connect-plugin-oracle-4.4.1-20260116.jar`, SHA-256 `873d828075d83e65967d8cede82b282f23e4e313c10861d4b7a16ed12ab21f33`; deployment-specific TCPS extension remains a custom adapter |
| Writers | Only CREATE SESSION/TABLE/VIEW/SEQUENCE/PROCEDURE/TRIGGER; no SESSION_ROLES or ANY/DBA/unlimited-tablespace privilege observed |
| Observer | Existing Oracle observer authenticated over TCPS, CREATE SESSION only, reads its previously granted DEV.POC_ORDERS; ODC PARTICIPANT also reads the new A1 ticket |
| Target isolation | DEV/SIT/UAT/MOCKPROD are four existing owner schemas on one Oracle service; MOCKPROD is not production |
| Actors | 10000 DEVELOPER requester; 10001 OWNER approver; 10002 DBA executor; 10003 PARTICIPANT observer; existing admin used only for audit readback |

[Final pre-replacement review](../evidence/odc-practical-poc-20261007/runtime-before-replacement-review.json) confirms actual current membership roles, no active new ticket, and historical ticket preservation. Source pins remain distinct from the running image; no new image-to-source mapping is claimed. This run certifies neither Oracle 19c/21c, independent instances, the actual estate, capacity nor a clean upstream TCPS connector without the existing extension.

## A — role-separated journey

| Case | Result | Ticket and observation |
| --- | --- | --- |
| A1 | PASS | 2000001: requester creates CREATE TABLE `P7_ROLE_JOURNEY` in MOCKPROD; OWNER/DBA can read exact SQL and database before approval; requester self-approval returns 404/NotFound and failed audit; OWNER then DBA approve; DBA Execute succeeds; Oracle object/result/log/history visible |
| A2 | PASS | 2000002: independent OWNER/DBA approval followed by requester Execute is allowed and succeeds; harmless SELECT only |

Evidence: [A1](../evidence/odc-practical-poc-20261007/a1.json), [A2](../evidence/odc-practical-poc-20261007/a2.json), [audit records](../evidence/odc-practical-poc-20261007/audit-before.json). A1's task node labels requester 10000 as operator even though audit 3000029 records Execute by DBA 10002. A2 audit 3000036 records requester 10000. The actual caller is therefore retrievable, but task-node operator alone is misleading.

**Requester execution = ACCEPTABLE_BY_POLICY under the stated provisional internal-pilot model:** independent review/approval is mandatory; approved requester dispatch is permitted. If the owner requires product-enforced DBA-only dispatch, classify this permission **NOT_ACCEPTABLE_BY_POLICY** and block adoption under that policy. Distinct actors in this test do not establish DBA-only enforcement or exhaustive self-approval protection.

## B — native ordered rollout

**Native batch = PASS.** Ticket 2000003 is one `MULTIPLE_ASYNC` definition containing the shared CREATE TABLE artifact, all four targets and ordered singleton groups `[[1000069],[1000122],[1000184],[1000218]]`. It uses MANUAL execution, ABORT and zero retry configuration. OWNER→DBA approval covers the batch. ODC maintains the per-target state; the probe invokes the native parent Execute at each operator boundary. It neither creates four external tickets nor sequences an alternative executor.

| Case | DEV | SIT | UAT | MOCKPROD | Result |
| --- | --- | --- | --- | --- | --- |
| B1, 2000003 | EXECUTION_SUCCEEDED | EXECUTION_SUCCEEDED | EXECUTION_SUCCEEDED | EXECUTION_SUCCEEDED | PASS |
| B2, 2000008, before cancellation | EXECUTION_SUCCEEDED | EXECUTION_FAILED | WAIT_FOR_EXECUTION | WAIT_FOR_EXECUTION | PASS |

In B1, waiting without Execute leaves the next environment waiting; its object is absent until continuation. `P7_BATCH_HAPPY` is created in each target, in the requested order. In B2, the same artifact conditionally raises `ORA-20007` in SIT before CREATE; `P7_BATCH_FAIL` exists only in DEV. UAT/MOCKPROD remain waiting, and the operator explicitly cancels this new batch instead of continuing. MANUAL boundaries permit an operator decision after failure; ABORT does not terminally fail the entire manual parent or prohibit a later explicit continuation. This satisfies the requested practical wait/stop behavior and does not claim a stronger enforced promotion policy.

Evidence: [B1 with boundaries and object checks](../evidence/odc-practical-poc-20261007/b1.json), [B2 failure and cancellation](../evidence/odc-practical-poc-20261007/b2.json), [happy artifact](../evidence/odc-practical-poc-20261007/b1-native-batch.sql), [failure artifact](../evidence/odc-practical-poc-20261007/b2-controlled-failure.sql).

The initial probe incorrectly expected the separate child-ticket listing shape from the reviewed source and timed out after DEV had succeeded. It was corrected to use this binary's native per-target result records; the same batch resumed at SIT, with no replay or extra batch. The actual API records reference the parent ticket ID and expose per-target status. This is recorded as a probe correction, not an ODC execution failure. AUTO+ABORT and within-group parallel behavior were not additional runtime goals and were not tested.

## C — Oracle function validity and TCPS

| Case | Task result | Oracle observation | POC result |
| --- | --- | --- | --- |
| C1, 2000004 | EXECUTION_SUCCEEDED | DEV.P7_VALID_FN, FUNCTION, VALID; USER_ERRORS empty; P7_VALID_FN(35)=42; `EDITIONABLE`, END and slash accepted | PASS |
| C2, 2000006 | EXECUTION_SUCCEEDED | DEV.P7_INVALID_FN, FUNCTION, INVALID; PLS-00201 for undeclared identifier and Statement ignored | PARTIAL |

Evidence: [C1](../evidence/odc-practical-poc-20261007/c1.json), [C2](../evidence/odc-practical-poc-20261007/c2.json), [valid SQL](../evidence/odc-practical-poc-20261007/c1-function.sql), [invalid SQL](../evidence/odc-practical-poc-20261007/c2-function.sql). Owner, type, status, line/position/attribute/text, intended service/PDB and TCPS are captured. The new functions use the requested representative EDITIONABLE/slash syntax; they are small synthetic fixtures, not a claim that every application script is qualified.

**Explicit validity check = PASS as a DBA pilot procedure.** The executor uses ODC SQL Console API to query USER_OBJECTS and USER_ERRORS after execution. The invalid function's diagnostics are reliably visible in the same practical tool. Require VALID and no ERROR for every changed PL/SQL object before accepting a release or continuing the next batch environment. Check relevant package specs/bodies and dependent objects as appropriate. ODC task success alone remains insufficient. Automatic INVALID detection remains a product gap; Bytebase's historical run also failed it.

## D — baseline replacement FAIL; supported configuration experiment PASS

New successful ticket **2000005** and failed ticket **2000007** both have their metadata, SQL, result summary, per-statement result, task log, ZIP attachment, log download and Execute audit recorded before replacement. All retrieval endpoints return meaningful HTTP 200 content. The same records were then retrieved after the approved ordinary application-pod replacement; the comparison demonstrates a fresh retention failure rather than relying on the historical sample.

Evidence: [before capture](../evidence/odc-practical-poc-20261007/d-before.json), [after capture](../evidence/odc-practical-poc-20261007/d-after.json), [replacement action](../evidence/odc-practical-poc-20261007/replacement-action.json), [file hashes before](../evidence/odc-practical-poc-20261007/replacement-baseline.json), [after workload/PVC/file checks](../evidence/odc-practical-poc-20261007/cluster-after.json).

| Item, both new tickets | Before replacement | After replacement |
| --- | --- | --- |
| Ticket metadata and SQL | Retrievable | PRESERVED |
| Result and per-statement result | Retrievable | MISSING — HTTP 500, forwarding to retired pod |
| Task log and log download | Retrievable | MISSING — HTTP 200 diagnostic, not log content |
| ZIP attachment | Retrievable, hashes captured | MISSING — HTTP 500 |
| Audit/operation record | Retrievable by existing admin | PRESERVED — all baseline IDs present |

D1/D2 are PASS for capture; **D3 is FAIL on the baseline configuration**. User continuation authorized the previously requested replacement of `odc-5b74c68b74-bzcp7`; new pod `odc-5b74c68b74-v2cbd` is Running/Ready with the same image. MetaDB pod and both PVC UIDs are unchanged. The TCPS initContainer rebuilds the plugin on replacement; its new JAR SHA-256 is `ad9902712e30907f513c750c90ee35522e19f0f13be0476466990b93552b4a31`, different from the pre-replacement JAR. Image and build configuration are unchanged, but byte identity and the cause of this hash difference are not established; Oracle function results above apply to the pre-replacement connector. The retention readback does not execute new Oracle SQL. All **96 ASYNC files retain identical hashes**, including the new ticket results. The result/per-statement APIs explicitly time out forwarding to old pod IP **10.244.1.98:8989**, while the replacement runs at **10.244.1.212**. This directly establishes the retired-host retrieval failure; merely adding a results PVC would not fix it. Task log endpoints return `read log failed, may be log file not exist`, consistent with the lost `emptyDir` log mount. HTTP 200 diagnostic downloads are classified MISSING, not a preserved log or ZIP.

### Supported configuration investigation

The [existing retained lab readback](odc-current-lab-state.md) already demonstrates old result/log/download failures. The baseline round's bounded primary-source review established two configuration hypotheses. They were unproved at that capture; the separate final experiment below now demonstrates both:

1. **Persist task logs.** The live `/opt/odc/log` mount is `emptyDir`. Pinned `TaskService` and `log4j2.xml` use `odc.log.directory` (default `./log`). Put that path on persistent storage. The existing data PVC already contains `/opt/odc/data/ASYNC` result JSON/ZIP files; changing `file.storage.dir` alone is insufficient because the reviewed ASYNC path uses relative `data/ASYNC` directly. Ordinary age expiry is 336 hours, not an explanation for same-day replacement loss.
2. **Stabilize ordinary app-executor identity.** Supported `ODC_HOST` and `ODC_MAPPING_PORT` configure advertised host/port. Pinned in-process task matching also compares hostname; PID/JVM start time are excluded. The new runtime errors confirm retrieval forwards to the retired pod IP despite surviving JSON files. Stable service DNS plus a stable workload hostname is a bounded single-replica configuration hypothesis. Task-framework job branches differ, so this must be qualified against the running image.

Primary paths: [HostProperties](../evidence/product-model/sources/oceanbase__odc/server/odc-service/src/main/java/com/oceanbase/odc/service/common/model/HostProperties.java), [ExecutorInfo](../evidence/product-model/sources/oceanbase__odc/server/odc-service/src/main/java/com/oceanbase/odc/service/task/model/ExecutorInfo.java), [WebTaskDispatchChecker](../evidence/product-model/sources/oceanbase__odc/server/starters/web-starter/src/main/java/com/oceanbase/odc/service/dispatch/WebTaskDispatchChecker.java), [FlowTaskInstanceService](../evidence/product-model/sources/oceanbase__odc/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/FlowTaskInstanceService.java), [TaskService](../evidence/product-model/sources/oceanbase__odc/server/odc-service/src/main/java/com/oceanbase/odc/service/task/TaskService.java), [DatabaseChangeThread](../evidence/product-model/sources/oceanbase__odc/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/task/DatabaseChangeThread.java).

The [historical prepared strategic merge patch](../evidence/odc-practical-poc-20261007/retention-storage-proposal.yaml) was a hypothesis at this baseline capture. The [final retention experiment](odc-retention-experiment.md), under subsequent explicit authorization, proves it for fresh tickets 2000013/2000014. The running pod uses hostname `odc`, advertised Service DNS/port and a persistent `data/task-logs` mount. After an ordinary ODC-only replacement, exact metadata/SQL/approval/audit, results/statements, task logs and ZIP/log downloads remain PRESERVED with matching hashes. Persisted executor identity and actual local log lookup establish **RETIRED-POD FORWARDING = NO** for this pair. No configuration correction round or product/MetaDB patch was required.

The original baseline D3 FAIL and all prior evidence remain unchanged. Final lab checks prove exact Deployment restoration, Argo active/Synced/Healthy, healthy ODC/MetaDB and unchanged historical ticket/PVC/Service identities. The tested settings are supplied as a [minimal permanent GitOps recommendation](../evidence/odc-retention-experiment-20261007/permanent-gitops-recommendation.yaml); they were not pushed permanently. GO applies to a pilot using those settings, rather than the deliberately restored baseline. Earlier stale-host records and lost logs are not repaired.

## E — duplicate, correction and API provenance

| Case | Result | Observation |
| --- | --- | --- |
| E1 | PASS | 2000009/2000010 accept identical SQL and identical release reference as two tickets; both API submissions accepted without rejection; GUI-specific duplicate prompts were not tested; OWNER/DBA independently approve both; safe SELECT executes twice; both prior tickets visible together in project listing |
| E2 | PASS | 2000011 fails from deliberate harmless bad column; new corrected ticket 2000012 references original and succeeds; original failed SQL/status/results remain available |
| E3 | PASS | Ticket 2000009 description round-trips application, release version and illustrative Git-reference label; API exposes SQL, exact target, approval actors and task result, with Execute caller supplied by audit |

Evidence: [duplicates](../evidence/odc-practical-poc-20261007/e1.json), [correction](../evidence/odc-practical-poc-20261007/e2.json), [provenance](../evidence/odc-practical-poc-20261007/e3.json). The Git label exercises metadata retention; it is not a real verified branch/commit or native SCM binding. Description is limited to 200 characters in the reviewed normal authoring interface.

**Operational model:** search prior tickets by release reference and target before dispatch; do not blindly resubmit non-idempotent SQL. The supported, demonstrated correction model is a new reviewed ticket carrying `corrects-ticket=<original>` and a new version/reference. This does not claim an immutable native migration-version graph or rule out every product edit path. The historical ODC duplicate DML already proved repeated effects; this new test deliberately uses idempotent SELECT so both submissions can be observed safely. Full automatic versioned replay/checksum parity with Flyway remains absent in the demonstrated path.

## Bytebase benchmark, without a new run

| Area | Bytebase reference | ODC observed | Practical difference |
| --- | --- | --- | --- |
| A, roles | Historical FREE rollout roles deny requester; paid approval DOC, actual OWNER/DBA approval BYTEBASE ALSO UNPROVEN | New independent OWNER→DBA approvals; requester self-approval denied; approved requester dispatch allowed; audit identifies actual Execute caller | ODC daily approval is usable; stricter DBA-only dispatch is a policy-dependent gap; task-node operator needs audit correlation |
| B, rollout | Historical native four-stage release; premature MOCKPROD dispatch allowed — BYTEBASE ALSO FAILED enforced ordering | One new native four-target batch; manual pauses; SIT failure leaves later groups waiting | Native ODC replaces the prior external four-ticket sequencing journey for this operating model; no universal predecessor enforcement claim for either product |
| C, Oracle | Historical required PL/SQL families/TCPS run; INVALID marked DONE/Deployed — BYTEBASE ALSO FAILED | New EDITIONABLE function/slash over TCPS; valid and invalid states retrievable through explicit ODC DBA checks | Both need explicit compile acceptance; ODC still owns its existing deployment TCPS adapter |
| D, retention | Historical results retrievable; replacement durability BYTEBASE ALSO UNPROVEN | Baseline fails while metadata/SQL/audit and ASYNC files survive; fresh configured success/failure pair preserves all retrieval after replacement | Bytebase restart durability remains unproved; ODC's supported single-replica retention configuration is now demonstrated |
| E, normal workflow | Historical versioned release/revision links and applied-version replay skip; changed-content behavior also failed REC-08 | Ordinary new tickets accept duplicate references; safe correction preserves original; description/API/audit trace usable | ODC supports the human workflow but does not replace automatic versioned migration history or native Git/release packaging |

Sources: [Bytebase preserved results](../BYTEBASE-ORACLE-POC-RESULTS.md), [practical comparison and pinned docs/source references](odc-bytebase-practical-comparison.md). Bytebase Enterprise behavior remains DOC where no applicable runtime evidence exists. Its historical FREE audit was edition-blocked, and SQL Review ERROR execution also failed; neither product is assumed perfect.

## Verification

The existing `python3 tools/verify_research_documents.py` check passes with no errors: source snapshots/hashes, document links/tables and historical 45-case identities remain intact. Its `oracle_execution_run=false` describes the verifier itself, not this separately evidenced runtime POC. Local evidence checks pass for all required case fields, statuses, JSON and links. The preservation comparison confirms 54 existing files unchanged and only the requested evaluation index modified among its 55-file baseline. DB-Research has no Git metadata; review used baseline hashes, the saved index diff and inspection of the new files. The approved ordinary replacement was checked separately: all 26 historical ticket SQL/status records remain unchanged afterward, all 12 new tickets are terminal, MetaDB/PVC UIDs are unchanged and ODC is healthy. [Post-replacement review](../evidence/odc-practical-poc-20261007/runtime-after-replacement-review.json) and [secret-value scan](../evidence/odc-practical-poc-20261007/secret-scan.json) retain these checks. No unrelated application unit suite was needed for these evidence/document additions. The separate final retention run has [current preservation](../evidence/odc-retention-experiment-20261007/preservation-after.json), [document checks](../evidence/odc-retention-experiment-20261007/document-checks.json), [same-ticket comparison](../evidence/odc-retention-experiment-20261007/pair-after.json) and [final lab verification](../evidence/odc-retention-experiment-20261007/final-lab-verification.json).

## Practical acceptance and operating model

| Required criterion | Assessment |
| --- | --- |
| Usable normal request→review→approval→execution | Demonstrated under proposed pilot dispatch policy |
| Native batch replaces external four-ticket sequencing | Demonstrated with manual singleton environment groups |
| Intended Oracle PL/SQL/TCPS path | Demonstrated on this 26ai lab and existing extension |
| DBA detects INVALID before accepting release | Demonstrated through explicit ODC postcheck; automatic task status remains misleading |
| New execution evidence durable after replacement, or supported fix proved | PASS with demonstrated settings; baseline FAIL remains historical |
| Manageable duplicate/correction workflow | Demonstrated with deliberate prior-ticket checks and new corrective tickets |
| No new external control plane | None required for the demonstrated workflow; none built |

Use ODC as the shared inventory, SQL request/review/approval, manual native rollout and evidence interface. For each stage, the DBA inspects task output, changed object validity and compile errors before the next native continuation. Use one release reference across tickets and explicit correction links; inspect existing application state before retrying failed or partial Oracle DDL. Retain existing migration files and version discipline where Flyway guarantees are required. Approved requester execution is permitted in the proposed pilot; strict DBA-only dispatch changes the acceptance decision.

**Parity estimate: 86/100, practical feature judgment; moderate gap.** Keep the earlier comparison's explicit weights. The previous POC reached 83 after native rollout 7→9 and API integration 3→4. Final retention closure changes only result/history 6→9, adding three points; all other scores remain unchanged. This is not a percentage of test passes, production readiness or a claim that Bytebase earned perfect correctness.

The final answer is **GO for the governed internal pilot using the demonstrated configuration**. Retention is closed through supported settings; no new controller, custom executor or product patch is needed. The exact original lab state and Argo reconciliation were restored. Apply the supplied minimal GitOps change before operating the pilot. Full Flyway migration-version equivalence and estate-wide production hardening remain outside this acceptance. The [final experiment report](odc-retention-experiment.md) separates product workflow, Oracle compatibility, retention, migration semantics and production hardening, and contains the minimum ten-step DBA procedure.

```text
ODC FINAL PRACTICAL ADOPTION DECISION
=====================================

ODC PRACTICAL POC =
GO — internal pilot using the demonstrated configuration

ROLE-SEPARATED WORKFLOW =
PASS — independent approval; approved requester dispatch accepted by policy

NATIVE MULTI-ENV BATCH =
PASS

ORACLE PL/SQL/TCPS =
PASS — observed 26ai lab with existing TCPS adapter

PL/SQL VALIDITY ACCEPTANCE =
PASS WITH DBA CHECK

RETENTION BASELINE =
FAIL

RETENTION CONFIGURATION EXPERIMENT =
PASS

RESULT RETENTION =
PASS

LOG RETENTION =
PASS

ATTACHMENT RETENTION =
PASS

RETIRED-POD FORWARDING =
NO — fresh configured tickets

METADATA/SQL/AUDIT RETENTION =
PASS

DUPLICATE/CORRECTION WORKFLOW =
PASS — prior-ticket checks and new reviewed corrections

API/PROVENANCE =
PASS — description/API/Execute audit trace

ARGO CD RESTORED =
YES

LAB HEALTH AFTER EXPERIMENT =
HEALTHY

HISTORICAL EVIDENCE PRESERVED =
YES

BYTEBASE PRACTICAL PARITY =
86/100
moderate gap

ODC VS DBEAVER/MANUAL SQL =
MAJOR IMPROVEMENT

ODC VS FLYWAY =
PARTIAL REPLACEMENT

CUSTOM PLATFORM CODE REQUIRED =
NO — no new controller, executor or product patch; existing TCPS adapter remains

PERMANENT GITOPS CHANGES RECOMMENDED =
Deployment hostname: odc
ODC_HOST: odc.oceanbase-odc.svc.cluster.local
ODC_MAPPING_PORT: "8989"
/opt/odc/log: existing data PVC, subPath task-logs

PILOT OPERATING MODEL =
Native tickets/batches, release references, OWNER/DBA review and approval,
authorized manual dispatch, DBA result/validity acceptance per environment,
prior-ticket lookup and new reviewed correction tickets.

KNOWN NON-BLOCKING GAPS =
1. Automatic INVALID detection; explicit DBA acceptance remains mandatory.
2. Native migration-version/replay and Git binding are not Flyway-equivalent.
3. Existing TCPS adapter ownership; approved requester dispatch and audit correlation.

PRODUCTION HARDENING NOT PROVED =
1. Actual 50-instance/20-user estate, Oracle 19c/21c and capacity.
2. Lost-ACK/commit ambiguity, restore reconciliation and multi-replica failover.
3. Distributed serialization/fencing, backups and full audit/long-term retention.

FINAL RECOMMENDATION =
Adopt ODC for the governed internal pilot after the proven minimal settings enter
GitOps desired state. The bounded retention blocker is closed without product or
MetaDB patches. Keep DBA PL/SQL checks and existing migration-version discipline;
this does not approve production estate-wide rollout or retire all Flyway semantics.

NEXT STEP =
Approve and apply the supplied minimal GitOps retention change for the pilot;
the lab was deliberately restored to its original baseline.
```
