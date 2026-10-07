# ODC retention experiment — final practical-adoption decision

**ODC practical POC = GO for the governed internal pilot. Retention configuration experiment = PASS.** The prepared supported configuration closes both demonstrated retention failures for fresh tickets: result retrieval no longer depends on a retired pod IP, and task logs survive on the existing data PVC and remain accessible through ODC. No bounded correction round, product patch, direct MetaDB write, additional controller or storage redesign was needed.

This is the final bounded experiment for the mission dated 7 October 2026. Evidence retains actual UTC capture timestamps; ODC's own log timestamps use CST. The experiment repeats only retention, using two new harmless tickets. A/B/C/E and Bytebase were not rerun. [Earlier practical results](odc-practical-poc-results.md), [historical product comparison](odc-bytebase-practical-comparison.md), [historical lab snapshot](odc-current-lab-state.md) and [original 45-case results](../ODC-ORACLE-POC-RESULTS.md) retain their distinct evidence scopes.

**The lab was restored to its original configuration and Argo CD reconciliation is active, Synced/Healthy.** GO applies to the demonstrated configuration. The restored baseline still lacks that retention configuration; apply the separately authorized minimal GitOps change before operating the pilot. Older stale-host records and previously lost logs were not rewritten or repaired.

## Established baseline and authorization

The unchanged baseline [before/after evidence](../evidence/odc-practical-poc-20261007/d-after.json) remains FAIL: successful/failed tickets 2000005/2000007 retain metadata/SQL/audit and physical ASYNC files, but result APIs forward to retired `10.244.1.98:8989`, and the `emptyDir` task-log mount loses files. These were established facts, not rerun tests.

The user's explicit mission authorized application-only Argo pause, the prepared patch, ODC rollouts/replacement, minimum fresh tickets and harmless isolated SQL, read-only diagnosis, at most one supported reversible correction, and rollback. Production, PVC recreation, destructive Oracle/MetaDB operations, historical-ticket edits, source patches, new platforms and permanent GitOps pushes remained outside scope. None occurred.

[Pre-experiment cluster evidence](../evidence/odc-retention-experiment-20261007/cluster-before.json), [ticket inventory](../evidence/odc-retention-experiment-20261007/inventory-before.json), [readiness](../evidence/odc-retention-experiment-20261007/readiness-before.json) and [file preservation baseline](../evidence/odc-retention-experiment-20261007/preservation-before.json) capture the original state. All 26 historical and 12 prior practical tickets were terminal; four actors authenticate, project 1 and five exact datasource mappings remain readable, and Oracle DEV identifies the intended POC schema/service/PDB over TCPS. Only read-only Oracle readiness SQL was used outside R1/R2.

ODC remains the pinned `4.4.1-20260116` image, digest `ee8ee48edea2907b1b2c11eac54c8603e554bdcc570eb11b0b1f9cef2ead040d`. MetaDB remains the existing pinned OceanBase CE deployment; its pod UID `c4c97f43-3230-42ca-8814-e2077db930cd` and both PVC UIDs are unchanged throughout. No image/source equivalence or reproducible TCPS-plugin byte build is newly claimed.

## Configuration and runtime proof

[Application reconciliation pause](../evidence/odc-retention-experiment-20261007/reconciliation-paused.json) uses only `argocd.argoproj.io/skip-reconcile=true` on `oceanbase-odc`. Its parent-managed automated sync policy, including `selfHeal=true`, is unchanged. The [configuration action](../evidence/odc-retention-experiment-20261007/configuration-applied.json) applies the historical prepared patch. [Runtime capture](../evidence/odc-retention-experiment-20261007/cluster-configured.json) verifies actual hostname `odc`, effective `ODC_HOST=odc.oceanbase-odc.svc.cluster.local`, `ODC_MAPPING_PORT=8989`, and `/proc/self/mountinfo` shows `/task-logs` from the same Longhorn data volume mounted at `/opt/odc/log`. This is verified inside the running pod, not inferred from desired YAML.

The [pinned source review](../evidence/odc-retention-experiment-20261007/source-review.json) explains why all three executor identity fields matter: host, port and hostname participate in matching; PID/JVM start time do not. Runtime proof is independent: [read-only MetaDB captures](../evidence/odc-retention-experiment-20261007/executors-before.json) show the fresh persisted executor fields, and working post-replacement APIs establish the actual binary behavior. Only SELECTs against the exact new task rows were used. No internal records were updated.

## Fresh pair and ordinary replacement

| Ticket | Target / operation | Expected and observed result | Execute audit |
| --- | --- | --- | --- |
| R1, 2000013 | Existing DEV 1000069; SELECT marker from DUAL | EXECUTION_SUCCEEDED; successCount=1; marker returned | 3000137, DBA actor 10002 |
| R2, 2000014 | Same DEV; SELECT 1/0 from DUAL | EXECUTION_FAILED; failCount=1; ORA-01476 / SQLState 22012 | 3000139, DBA actor 10002 |

[SQL artifacts](../evidence/odc-retention-experiment-20261007/r1.sql), [failure SQL](../evidence/odc-retention-experiment-20261007/r2.sql), [before capture](../evidence/odc-retention-experiment-20261007/pair-before.json) and [audit](../evidence/odc-retention-experiment-20261007/audit-before.json) retain exact SQL/target, terminal status, summary, statement results, log content, log download, ZIP and meaningful HTTP response bodies. The existing DEV rule uses system auto-approval; its completed approval node is preserved. This pair does not claim new human approvals. Earlier independent OWNER/DBA approval acceptance remains the A/B evidence. Audit SUCCESS means dispatch accepted; R2's SQL correctly failed.

The [ordinary replacement action](../evidence/odc-retention-experiment-20261007/ordinary-replacement-action.json) deletes only the configured ODC pod after confirming no active unfinished ticket. MetaDB, Service, PVCs and Deployment template are unchanged during this replacement.

| Identity | Before ordinary replacement | After ordinary replacement |
| --- | --- | --- |
| Pod | `odc-6cd8c7d459-pmw9v` | `odc-6cd8c7d459-7hqjn` |
| Pod UID | `f6bec88e-26a0-4f3e-810d-4277cee4b031` | `6e9d8a20-7e5b-43db-b4b5-829e82d44600` |
| Pod IP | `10.244.1.114` | `10.244.1.105` |
| Runtime hostname | odc | odc |
| Advertised executor endpoint | odc.oceanbase-odc.svc.cluster.local:8989 | odc.oceanbase-odc.svc.cluster.local:8989 |

[After-replacement cluster](../evidence/odc-retention-experiment-20261007/cluster-after-replacement.json) and [readiness](../evidence/odc-retention-experiment-20261007/readiness-after-replacement.json) establish new-pod readiness, unchanged dependent resources, working login/datasource mappings and continued Oracle TCPS.

## Artifact classification and routing

[After capture](../evidence/odc-retention-experiment-20261007/pair-after.json) compares the exact same ticket IDs against their clean pre-replacement snapshots. Every retrieval endpoint returns meaningful HTTP 200 content; logs contain execution lines, not `read log failed` fallback text.

| Artifact, both R1/R2 | Classification | Evidence |
| --- | --- | --- |
| Ticket metadata, SQL and target | PRESERVED | Full selected detail and SQL match |
| Approval/workflow nodes | PRESERVED | Completed system-approval node matches |
| Execute audit actor/action/time | PRESERVED | Both audit records match exactly |
| Result summary | PRESERVED | Same success/failure counts and error/result file references |
| Per-statement result | PRESERVED | R1 marker and R2 Oracle error match |
| ZIP attachment | PRESERVED | API download SHA-256 matches baseline |
| Task log content | PRESERVED | Same meaningful execution text |
| Downloadable log | PRESERVED | API download SHA-256 matches baseline |
| Physical JSON/ZIP/task-log files | PRESERVED | Relevant hashes match; all 101 ASYNC files match |

[File hashes before](../evidence/odc-retention-experiment-20261007/files-before.json) and [after](../evidence/odc-retention-experiment-20261007/files-after.json) prove physical retention. R1's log is `/opt/odc/log/async/10000/2000026/asynctask.all`; R2's is `/opt/odc/log/async/10000/2000028/asynctask.all`. Downloaded log hashes match those exact files. [Retained downloads](../evidence/odc-retention-experiment-20261007/retained-downloads.json) provide local ZIP/log artifacts for review after rollback.

**RETIRED-POD FORWARDING = NO for the fresh configured tickets.** [Routing verification](../evidence/odc-retention-experiment-20261007/routing-verification.json) combines retired-pod NotFound, changed physical IP, current Service endpoints, persisted executor host/port/hostname without the retired IP, exact successful retrieval, and actual local task-log lookup lines with `exist=true`. The stored executor JSON remains unchanged, as expected; the replacement advertises matching logical fields. This claim is scoped to R1/R2, not unrepaired historical task identities.

The first file comparison had an integer-versus-string JSON ticket-key mismatch in the disposable probe. Comparison of saved JSON and individual hashes confirmed unchanged artifacts; the probe comparison was corrected without configuration changes or SQL replay. No evidence-driven configuration correction was necessary: **prepared experiment PASS; retention blocker CLOSED under the demonstrated configuration**.

## Rollback and preservation

The original saved Deployment template was restored exactly with JSON Patch; [template verification](../evidence/odc-retention-experiment-20261007/rollback-template-verification.json) confirms full Deployment spec equality. An initial merge left the added hostname field in place; this was caught and removed with exact template replacement before acceptance. This was a rollback implementation correction, not a retention configuration experiment round.

[Reconciliation restoration](../evidence/odc-retention-experiment-20261007/reconciliation-restored.json), [restored cluster](../evidence/odc-retention-experiment-20261007/cluster-restored.json) and [final lab verification](../evidence/odc-retention-experiment-20261007/final-lab-verification.json) verify Argo active/Synced/Healthy, ODC and MetaDB healthy, original application/Deployment specs, unchanged MetaDB UID/images/readiness and PVC/Service identities. Final ODC pod is `odc-5b74c68b74-g5vxw`. All 26 historical and 12 prior practical ticket metadata/SQL/status hashes match; R1/R2 remain terminal and are not deleted. All 101 ASYNC files and the persistent task-log hashes survive rollback; the latter are accessible physically through `/opt/odc/data/task-logs/` after the log mount is restored to `emptyDir`.

Rollback intentionally removes the configuration that enabled product retrieval. Captured R1/R2 ZIP/logs remain local evidence, and their backing PVC files remain intact. The restored lab is healthy but is not claimed to provide the proven retention behavior until the settings enter desired state. No permanent change, push or merge occurred.

[Preservation verification](../evidence/odc-retention-experiment-20261007/preservation-after.json) and [document/evidence checks](../evidence/odc-retention-experiment-20261007/document-checks.json) retain final validation. Historical 45-case ODC evidence, Bytebase evidence, CI/Flyway evidence, prior practical evidence and baseline FAIL are unchanged. Only the requested practical results/index are updated among existing files; the retention report/evidence are new. DB-Research has no Git metadata; review uses saved originals, targeted diffs and hashes.

## Permanent recommendation and operating procedure

[Minimal GitOps recommendation](../evidence/odc-retention-experiment-20261007/permanent-gitops-recommendation.yaml) contains only demonstrated settings: `hostname: odc`, `ODC_HOST` service FQDN, `ODC_MAPPING_PORT: "8989"`, and `/opt/odc/log` mounted from the existing `data` PVC with `subPath: task-logs`. The existing single-replica deployment, Service and data PVC are prerequisites. No image, MetaDB, Service or cluster-security change is proposed. This does not certify multi-replica routing or retroactively restore old logs.

1. Requester creates a native ticket/batch with a release reference.
2. OWNER/DBA review exact SQL and target.
3. Required environment approvals complete.
4. An authorized actor starts the current environment; approved requester dispatch is permitted by the pilot policy.
5. DBA inspects the ODC task and statement results.
6. For changed PL/SQL, DBA checks USER_OBJECTS/USER_ERRORS and requires VALID with no compile ERROR.
7. Continue the next environment only after acceptance.
8. Corrections use a new reviewed ticket referencing the original.
9. Search release/target history and inspect partial effects before retry/resubmission; use one execution window per target.
10. ODC retains ticket/result/log/audit evidence with the demonstrated settings; platform owner maintains retention/backup policy.

## Separate adoption dimensions and parity

| Dimension | Final assessment |
| --- | --- |
| PRODUCT WORKFLOW | PASS for role-separated approval, manual native batch and normal correction/provenance; requester dispatch policy explicit |
| ORACLE COMPATIBILITY | PASS for observed Oracle 26ai and existing TCPS adapter; explicit DBA validity acceptance required |
| OPERATIONAL RETENTION | PASS for new success/failure evidence after ordinary replacement with demonstrated settings; baseline FAIL preserved |
| MIGRATION-VERSION SEMANTICS | PARTIAL replacement of Flyway; automatic version/history/replay behavior is not natively equivalent |
| PRODUCTION HARDENING | NOT_PROVED; actual estate, long-term expiry/backups, crash/restore/HA and distributed guarantees remain outside scope |

**Bytebase practical parity = 86/100, moderate gap.** Only result/history changes, 6→9 out of 10, from the previous 83. Native versioned history remains weaker. Other weights/scores stay as already established: inventory 10, SQL UX 9, review 8, approval 9, Oracle 13, multi-environment 9, audit/RBAC 8, API/integration 4, simplicity 7. The total is a comparative feature judgment, not test accounting or production readiness. Earlier 80/100 comparison and 10 PASS / 1 PARTIAL / 1 FAIL practical case records retain their original meanings and are not rewritten. Bytebase replacement durability remains unproved; no new Bytebase superiority or failure is invented.

ODC is a major improvement over DBeaver/manual SQL for central inventory, review, approvals and traceable execution. It can replace governed execution/orchestration portions of Flyway, while Flyway's automatic migration-version/history/replay semantics remain distinct. No new custom platform code is required; the already existing deployment-specific TCPS adapter remains an owned component and upgrade qualification gap.

## Final executive decision

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
