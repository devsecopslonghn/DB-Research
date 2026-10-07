# ODC focused practical-adoption POC — 7 October 2026

This mission evaluates whether the existing ODC lab can support an internal Oracle change-management pilot through native product workflows and bounded DBA procedures. The [practical comparison](odc-bytebase-practical-comparison.md), approximately 80/100 parity with Bytebase, supplies the starting hypothesis. The older HOLD conclusion and 45-case acceptance contract do not decide this experiment. Historical evidence remains unchanged.

## Boundaries and readiness

Use only project 1, `odc-oracle-poc`, at the existing [ODC endpoint](https://oceanbase.apps.drgdevlab.com/#/datasource). Create new ticket IDs greater than 1000028. Preserve the 26 historical tickets and their SQL hashes. Use new `P7_` objects without editing historical objects. API probes call ODC's native executor; they are disposable experiment tools, not an external rollout controller or alternative SQL executor.

Before change execution, confirm ODC/MetaDB health, all four role authentications, exact registry mappings, live Oracle schema/service/protocol/version, restricted writer grants, observer access and historical ticket preservation. Close console sessions after each query. The [dated evidence folder](../evidence/odc-practical-poc-20261007/) holds sanitized records and the preservation baseline; credentials and login responses remain outside it.

| Environment | Schema | Database ID | Datasource ID |
| --- | --- | --- | --- |
| DEV | ODC_POC_20261004_DEV | 1000069 | 1000001 |
| SIT | ODC_POC_20261004_SIT | 1000122 | 1000002 |
| UAT | ODC_POC_20261004_UAT | 1000184 | 1000003 |
| MOCKPROD | ODC_POC_20261004_MOCKPROD | 1000218 | 1000004 |
| Observer | ODC_POC_20261004_OBSERVER | 1000345 | 1000005 |

MOCKPROD is an isolated lab schema on the same Oracle service as the other schemas, not a production target. Existing actors: requester 10000/DEVELOPER, approver 10001/OWNER, executor 10002/DBA, observer 10003/PARTICIPANT. Do not substitute accounts if authentication fails. A legitimately available administrative account may read audit records; it does not create, approve or execute these changes.

The proposed pilot policy requires independent OWNER/DBA approval and permits requester dispatch after approval. Enforced DBA-only execution remains a material policy choice presented to the owner; classify the actual permission as unacceptable if that stricter policy is required.

## Five bounded experiments

| Case | Native action | Acceptance observation |
| --- | --- | --- |
| A1 | Requester creates one harmless change in MOCKPROD; reviewers read SQL/target; requester attempts self-approval; OWNER then DBA approve; DBA executes | Actual role denials/approvals, Execute caller, final object and result/history recorded |
| A2 | Separate harmless SELECT ticket after independent approval; requester attempts Execute | Record actual permission and policy classification; permission alone does not fail adoption |
| B1 | One MULTIPLE_ASYNC definition, one CREATE TABLE artifact, four singleton groups DEV→SIT→UAT→MOCKPROD, MANUAL boundaries, ABORT, zero retries | Full target set visible before execution; each group waits for native Execute; per-target results and Oracle effects recorded |
| B2 | One new native batch with safe conditional failure in SIT before CREATE; same four groups | DEV succeeds; SIT fails visibly; UAT/MOCKPROD wait or stop; do not authorize later groups after failure |
| C1 | New EDITIONABLE function with END and slash, through the existing ODC Oracle plugin/path | Task succeeds, exact owner/type, VALID and no compile ERROR, callable result, TCPS identity/version captured |
| C2 | Separate deliberately invalid EDITIONABLE function in DEV | Compare task outcome to USER_OBJECTS and USER_ERRORS; demonstrate explicit DBA postcheck through ODC; record misleading success as a product gap |
| D1/D2 | Capture one new successful and one new failed ticket before ordinary replacement | Metadata, SQL, result, task log, attachment/log download and audit record retrievable; content/hash baseline retained |
| D3 | Separately approved ordinary replacement of ODC pod only, then retrieve the same new evidence | Each item PRESERVED/MISSING/CORRUPT/PERMISSION_BLOCKED; unchanged MetaDB/PVCs; no recovery or exactly-once claim |
| E1 | Submit the same harmless naturally idempotent SELECT artifact as two new tickets | Warning/acceptance, prior-ticket discoverability and repeated execution behavior observed |
| E2 | New harmless failing ticket, then normal corrected ticket referencing the original | Original SQL/history remains readable; correction/retry model documented |
| E3 | Add application/release/reference in supported description and retrieve through API | Release reference→ticket→SQL→target→approvals→result usable without custom platform code |

Pod replacement and any storage fix need the mission's separate authorization. First prepare the complete before-replacement capture, identify the exact action and evidence checks, then request approval. Do not restart MetaDB, change Kubernetes configuration, push, merge, deploy or rewrite old tickets. A refused/unavailable authorization produces BLOCKED retention acceptance, not an invented result. If a supported storage fix is identified, make it reviewable and seek authorization before applying it; repeat only retention afterward.

## Evidence and decision

Each case record includes case ID, timestamp, exact ODC/Oracle versions, datasource/database IDs, new ticket ID(s), requester/reviewer/executor, SQL reference, expected/observed behavior, PASS/PARTIAL/FAIL/BLOCKED/NOT_RUN and evidence links. A controlled SQL failure can PASS its test expectation. Distinguish task status from test status and Oracle validity. HTTP 200 with `read log failed` is missing evidence.

Use only existing Bytebase results/docs/source as the benchmark; do not rerun it. State BYTEBASE ALSO FAILED for its INVALID/premature-stage observations and BYTEBASE ALSO UNPROVEN for paid approval or replacement retention. Link each area comparison in the results document.

GO requires usable daily workflow, native rollout, intended-path Oracle/TCPS, reliable DBA validity checks, durable new execution evidence or an accepted supported fix, understandable duplicate/correction handling and no external control plane. CONDITIONAL GO requires demonstrated daily usability and only one or two bounded operational/process gaps. NO-GO applies to material native rollout/connector/role-policy failures, unsupported evidence retention or a required custom release-control platform. A missing required runtime proof is an acceptance blocker, not proof the product cannot implement the feature.

Exclude the previous 45-case rerun, lost ACK/commit ambiguity, distributed exactly-once, fencing, metadata restore, alias locks, multi-controller failover, capacity and concurrency testing. Retain those as advanced hardening risks. The [results](odc-practical-poc-results.md) will state the practical pilot decision and its limits.
