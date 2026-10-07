# ODC versus Bytebase: practical product and workflow comparison

Re-evaluated **7 October 2026** for approximately **50 Oracle instances and 20 users**. This round compares everyday database change management with Bytebase's evidenced product, rather than the earlier custom release-control contract. It adds no runtime observations and changes no historical verdicts.

[O1]: ../ODC-ORACLE-POC-RESULTS.md
[O2]: odc-current-lab-state.md
[O3]: research-round-2/coordinator/odc-source-survey-20261006.md
[O4]: ../evidence/product-model/sources/oceanbase__odc-doc/en-US/700.database-change-management/650.multiple-database-change.md
[O5]: ../evidence/product-model/sources/oceanbase__odc-doc/en-US/700.database-change-management/600.database-change.md
[O6]: ../evidence/product-model/sources/oceanbase__odc-doc/en-US/700.database-change-management/100.user-permission-and-management/100.odc-users-and-roles.md
[O7]: ../evidence/product-model/sources/oceanbase__odc-doc/en-US/700.database-change-management/300.risk-level-risk-identification-rules-and-approval-process.md
[O8]: ../evidence/product-model/sources/oceanbase__odc-doc/en-US/900.data-security-and-compliance/200.operating-records.md
[O9]: ../evidence/product-model/sources/oceanbase__odc-doc/en-US/1000.system-integration/100.login-integration.md
[O10]: ../evidence/product-model/sources/oceanbase__odc-client/src/component/Task/component/ApprovalModal/index.tsx
[O11]: ../evidence/product-model/sources/oceanbase__odc/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/FlowPermissionHelper.java
[B1]: ../BYTEBASE-ORACLE-POC-RESULTS.md
[B2]: https://docs.bytebase.com/change-database/review
[B3]: https://docs.bytebase.com/change-database/approval
[B4]: https://www.bytebase.com/pricing/
[B5]: https://docs.bytebase.com/change-database/plan
[B6]: https://docs.bytebase.com/change-database/batch-change
[B7]: https://docs.bytebase.com/change-database/scheduled-rollout
[B8]: https://docs.bytebase.com/change-database/change-history
[B9]: https://docs.bytebase.com/gitops/migration-based-workflow/overview
[B10]: https://docs.bytebase.com/security/audit-log
[B11]: https://docs.bytebase.com/get-started/self-host/production-setup
[C1]: ../poc/results.md
[C2]: ../poc/architecture.md

## 1. Executive conclusion

**ODC is a credible practical adoption candidate: 80/100 product parity, a MODERATE GAP to Bytebase, and a MAJOR IMPROVEMENT over DBeaver plus manually operated SQL/Flyway CLI. A focused adoption POC is justified. Production hardening risk remains HIGH for the observed deployment.**

ODC already centralizes inventory, projects, SQL tickets, visible SQL/targets, multi-step approval, Oracle execution, results and basic audit. Those capabilities include historical UI/API runtime, not just feature claims. Bytebase's strongest demonstrated advantages are reusable native releases, version/revision history and ordinary replay handling. ODC's native batch feature deserves DOC/SOURCE credit even though its Oracle end-to-end journey has not been demonstrated in the preserved run.

Neither product has demonstrated a perfect Oracle deployment outcome. Both reported success for an INVALID procedure. Bytebase FREE allowed premature MOCKPROD rollout and SQL Review ERROR execution; its approval and audit tests were edition-blocked. Enterprise documentation is useful product evidence, not a passed Enterprise regression. These shared or unproved controls cannot justify building a replacement platform around ODC.

**If Bytebase did not exist, ODC would already be a major practical improvement.** This is a workflow judgment, not measured time savings or permission to retire all Flyway guarantees. A native ODC ticket workflow can replace much manual coordination; complete replacement of Flyway's versioned migration behavior still has an ordinary migration-history/replay gap. Start with the five bounded adoption items in section 16, not a new controller.

## 2. Why Bytebase is the benchmark

Bytebase matches the desired product shape: one UI ties databases, proposed SQL, review, approval, rollout and recorded results together. Its historical run demonstrates native release/version/revision links. This makes it an appropriate reference for what users actually need to do each day. It does not make its execution or recovery semantics the ideal specification.

The baseline is:

```text
Login → database inventory → create SQL change → review SQL → approval
→ execute → inspect result → DEV/SIT/UAT/PROD rollout → history/audit
```

The comparison separates **Bytebase product capability in the applicable edition** from **observed Bytebase FREE behavior**. Current pricing documents Community as 10 instances/20 users, custom instance counts and approval as Enterprise, and audit as Pro/Enterprise. A roughly 50-instance estate therefore cannot assume Community or Pro fits; actual Oracle registration/licensing units need confirmation. ODC's reviewed Apache-2.0 application source has no paid count gate established in the inspected paths; this does not certify every shipped image, MetaDB, plugin or Oracle driver dependency. [Bytebase pricing][B4]; [pinned license reviews](candidates/bytebase/source-review.md), [ODC source/license review](candidates/odc/source-review.md).

| Evidence label | Meaning used in every product capability cell |
| --- | --- |
| DOC | Official documentation describes the feature. Later docs do not prove the historical binary implements it. |
| SOURCE | A bounded, pinned source path demonstrates implementation structure; no binary/runtime equivalence assumed. |
| RUNTIME | Preserved observation on the exact historical build/topology, including failures and blocked features. |
| UNKNOWN | No sufficient evidence for the claim, or the needed runtime/estate qualification is missing. |

Each Bytebase/ODC matrix cell states its label and scope. Gap and impact cells are **assessments derived from those cells**, not extra runtime observations. Every identified gap is classified CORE, IMPORTANT or ADVANCED HARDENING. An evidence gap is distinguished from a missing feature. **BYTEBASE ALSO UNPROVEN** is used where the matching Bytebase capability lacks positive evidence; a witnessed failure is stated explicitly as stronger negative evidence. Runtime unproved is also stated where DOC/SOURCE exists.

| Evidence record | Scope and boundary |
| --- | --- |
| [ODC historical results][O1] | 4 October; 4.4.1-20260116, Oracle 26ai EE 23.26.4.1.0, local TCPS extension; 12 PASS / 20 PARTIAL / 5 FAIL / 8 NOT_RUN. |
| [Bytebase historical results][B1] | 4 October; 3.22.1/FREE, commit `a85f6cb4195299995e8554303550d672d5093e1d`; 17 PASS / 14 PARTIAL / 4 FAIL / 3 BLOCKED / 7 NOT_RUN; extra P04 FAIL outside the 45 totals. |
| [ODC retained lab readback][O2] | 7 October read-only capture already performed: inventory, actors, approvals and ticket SQL preserved; sampled old logs/results/attachments unavailable. No live Oracle check. |
| [ODC source survey][O3] | Backend `d517c0f27971642fb0cd7565fd61ab2309875ec3`; frontend `273fa3c4cc7d87f942ade231ce9220b98fa595e2`. Image-to-source mapping remains unproved. |
| [ODC official documentation snapshot][O4] | `oceanbase/odc-doc@40dc7c03522fef1968bd11b2b051bc216091e60d`; batch, ticket, approval, audit and SSO descriptions are DOC. |
| Bytebase public docs | Relevant official pricing, plan, review, approval, scheduling, batch, history, GitOps, audit and production-setup pages inspected this round. All remain DOC. |
| [Implemented CI results][C1], [architecture][C2] | One-target Jenkins/Flyway/SQLite reference; 30 retained local checks. Oracle/Jenkins acceptance blocked; multi-environment promotion not implemented. |

Both historical Oracle labs used environment schemas on **one physical database/service**, not four isolated instances. Neither proves Oracle 19c/21c, RAC, real estate topology, or 50-instance/20-user capacity. No SQL, connection test, Oracle regression or cluster change was performed for this report.

## 3. Core workflow comparison

| Capability | Bytebase | ODC | Gap | Practical impact |
| --- | --- | --- | --- | --- |
| Login → inventory | RUNTIME: login, projects and five Oracle target registrations. [B1] | RUNTIME: login, project and five POC connections; registry retained. [O1], [O2] | No core feature gap established. | Both replace personal connection lists with shared inventory. |
| Create → review | RUNTIME: stored release/plan/issue SQL and targets visible. [B1] | RUNTIME: stored ticket SQL/target visible before OWNER/DBA review. [O1] | CORE: ODC lacks demonstrated native versioned release identity; ordinary ticket review exists. | Shared SQL review is already practical; Flyway-style migration tracking needs separate treatment. |
| Approval → execute | DOC: Enterprise approval; RUNTIME: FREE skipped approval, authorized rollout executed. [B3], [B1] | RUNTIME: OWNER→DBA approval followed by manual execution. [O1] | IMPORTANT: ODC creator can execute after approval; independent execution policy differs. | Normal approved-ticket flow works; stricter DBA-only execution is conditional on team policy. |
| Inspect → rollout | RUNTIME: task results and four native environment stages; premature stage execution observed. [B1] | RUNTIME: single-ticket results and four externally sequenced tickets; DOC/SOURCE: native ordered batch. [O1], [O4][O3] | CORE evidence gap: ODC native Oracle batch journey not demonstrated. Bytebase enforced predecessor success also unproven/failed in FREE. | Validate native batch usability; do not mandate an external rollout controller. |
| History/audit | RUNTIME: release/revision/task history; FREE audit blocked. [B1] | RUNTIME: ticket history and 97 audit records; some retained execution files unreadable. [O1], [O2] | IMPORTANT: ODC evidence retention; both paid/full audit export acceptance unresolved. | ODC already improves traceability, but old incident evidence must remain accessible. |

## 4. Inventory

| Capability | Bytebase | ODC | Gap | Practical impact |
| --- | --- | --- | --- | --- |
| Instances/datasources | RUNTIME: five project-owned instance/database resources. [B1] | RUNTIME: five project POC datasource records. [O1], [O2] | No core inventory gap; neither lab is a 50-instance demonstration. | Shared target registry is available in both. |
| Databases/schemas | RUNTIME: schema-owner targets and stable resource names. [B1] | RUNTIME: stable database IDs, schema owners and datasource mapping. [O1], [O2] | No gap established for registered Oracle schemas. | Reviewers can identify the intended schema before execution. |
| Environments | RUNTIME: DEV/SIT/UAT/MOCKPROD represented. [B1] | RUNTIME: environment assignments and retained POCUAT/POCPROD. [O1], [O2] | No inventory gap; isolated environments remain UNKNOWN in both. | Environment labels help prevent routine wrong-target selection. |
| Projects | RUNTIME: project groups inventory and changes. [B1] | RUNTIME: project 1 groups members, databases and tickets. [O1], [O2] | No core project gap established. | Team/application grouping already exists. |
| Ownership | RUNTIME: project roles/resource ownership. [B1] | RUNTIME: OWNER/DBA/DEVELOPER/PARTICIPANT membership. [O1], [O2] | IMPORTANT: map actual business owners and estate routes during onboarding, for both. | Fifty instances need an agreed registry; this is configuration work, not a new product. |

An Oracle instance, service, PDB and schema are different inventory units. Use the existing products' target identifiers and record environment/schema/owner explicitly; this round does not require canonical alias serialization. Actual estate discovery remains UNKNOWN for both.

## 5. SQL/review/approval

| Capability | Bytebase | ODC | Gap | Practical impact |
| --- | --- | --- | --- | --- |
| SQL editor/upload | RUNTIME: UI SQL and API release sheets; DOC: local SQL-file revision import. [B1], [B8] | RUNTIME: SQL Window and ticket creation; DOC: SQL entry and `.sql` upload. [O1], [O5] | No normal authoring gap. Exact upload ergonomics not compared in runtime. | Users can prepare changes in the product rather than distribute execution instructions. |
| Target selection | RUNTIME: plan targets resolve to environment/schema. [B1] | RUNTIME: ticket targets use database IDs; DOC: ordered batch target selector/templates. [O1], [O4] | No single-target gap; native multi-target UX remains an evidence gap. | Inventory replaces copying connection details for each request. |
| SQL preview | RUNTIME: API SQL matched artifact; UI review exposed SQL/target. [B1] | RUNTIME: CREATE SQL and MOCKPROD visible before approvals. [O1] | No basic preview gap. | Reviewers see the proposed operation and destination. |
| Stored change/ticket | RUNTIME: release → plan → issue → task/revision links. [B1] | RUNTIME: ticket ID, SQL and approval nodes; SOURCE/UNKNOWN: no native versioned migration identity established. [O1], [O3] | CORE: ordinary release/version parity with Bytebase/Flyway is incomplete. | A ticket is sufficient for a reviewed ad hoc change; less convenient for repeatable versioned releases. |
| Change history | RUNTIME: linked version/SHA/revision and applied-version replay skip. [B1] | RUNTIME: ticket history; repeated new ticket executes again. [O1] | CORE: automatic applied-version awareness missing in observed ODC path. | A complete Flyway replacement needs an explicit normal release-history/replay policy. |
| SQL visible to reviewer | RUNTIME: MODEL-05 PASS. [B1] | RUNTIME: MODEL-05 PASS with OWNER/DBA UI. [O1] | No core review gap. | ODC is already usable for human SQL review. |
| Comments/findings | DOC: inline SQL threads/current Plan review; RUNTIME: SQL Review ERROR finding displayed, enforcement FAIL. [B5], [B1] | SOURCE: approval/rejection comments, required and limited to 200 characters; DOC: SQL check. [O10], [O5] | IMPORTANT: richer inline discussion parity not established for ODC; Oracle review-rule/enforcement parity UNKNOWN. | Basic review feedback exists. Do not claim automated rules substitute for DBA review in either product. |
| Change visibility | RUNTIME: plan/issue and linked deployment records. [B1] | RUNTIME: project tickets and current SQL readbacks. [O1], [O2] | No core visibility gap established. | Requester, reviewer and DBA share the same work item. |
| Target visibility | RUNTIME: SQL and selected target visible. [B1] | RUNTIME: selected MOCKPROD target visible before approval. [O1] | No core visibility gap established. | Reduces ambiguity over where SQL will run. |
| Approval workflow | DOC: custom approval; RUNTIME: FREE approval SKIPPED/BLOCKED. [B3], [B1] | RUNTIME: approval before manual execute, requester denied while APPROVING. [O1] | No ODC approval-existence gap. Bytebase paid approval runtime unproved. | ODC demonstrated a central approval benefit unavailable in the tested FREE edition. |
| Multi-step approval | DOC: sequential approval nodes; RUNTIME: FREE unavailable. [B3], [B1] | RUNTIME: OWNER then DBA actors on ticket 1000023. [O1], [O2] | No ODC feature gap against documented Bytebase behavior. | Two-step production review does not require custom orchestration. |
| Requester/reviewer distinction | DOC: role-based approvals; RUNTIME: no actual approver in FREE. [B3], [B1] | RUNTIME: distinct requester and two approvers; SOURCE/UNKNOWN: exhaustive self-approval prevention not established here. [O1], [O11] | IMPORTANT evidence gap: all role combinations/self-approval paths; Bytebase equivalent runtime also unproved. | Distinct actors are workable; policy enforcement needs a focused configuration check. |
| Environment-specific approval | DOC: conditions include environment; RUNTIME: FREE not tested with active approval. [B3], [B1] | DOC: risk-rule routing; RUNTIME: POCPROD high-risk OWNER→DBA workflow. [O7], [O1] | No basic routing gap; every intended environment rule not accepted in either lab. | DEV and PROD can follow different policies without new software. |

Requester/reviewer distinction is separate from requester/executor distinction. ODC's GOV-03 FAIL proves the requester could execute **after real approval**; it does not prove the requester bypassed review or self-approved. Bytebase's automated ERROR finding is real, but the historical executor still deployed it. Current documentation describing stronger behavior does not rewrite that failure.

## 6. Oracle execution

| Capability | Bytebase | ODC | Gap | Practical impact |
| --- | --- | --- | --- | --- |
| Manual execution | RUNTIME: authorized executor resumes waiting tasks; requester rollout 403. [B1] | RUNTIME: MANUAL waits, then UI/API Execute runs; creator also permitted after approval. [O1] | IMPORTANT: weaker independent-executor separation in ODC. | Both support deliberate execution after review; DBA-only dispatch is a policy question. |
| Scheduled execution | DOC: choose a later task execution time. [B7] | DOC: scheduled execution in task settings. [O5] | No documented feature gap. Scheduled Oracle runtime UNKNOWN for both. | Maintenance-window capability deserves DOC credit, not RUNTIME. |
| Batch execution | RUNTIME: four target tasks in a rollout; DOC: same-stage batch deployment. [B1], [B6] | DOC/SOURCE: native serial/parallel multi-database task, 2–100 databases within one project. [O4], [O3] | CORE evidence gap: native ODC Oracle batch not exercised historically. | Potentially covers the estate size per batch; limits do not prove estate capacity or usability. |
| Oracle execution | RUNTIME: DDL/DML, procedure/function/package/trigger/blocks/slash/literals execute. [B1] | RUNTIME: corresponding syntax cases execute, using local TCPS extension. [O1] | IMPORTANT: ODC connector/TCPS support and upgrade burden; actual estate compatibility UNKNOWN for both. | ODC is not disqualified as an Oracle executor. Qualify the deployed connector and real SQL corpus. |
| Stop on error | RUNTIME: missing-table task FAILED; later statement did not execute; later stage waited automatically. [B1] | RUNTIME: ABORT stopped later INSERT; DOC: batch stop/continue option. [O1], [O4] | CORE evidence gap: ODC batch failure behavior; Bytebase explicit later-stage dispatch after failure was still allowed. | Use stop-on-error and deliberate stage continuation; neither has proved universal promotion enforcement. |
| Oracle compile success | RUNTIME: SQL-11 FAIL, INVALID procedure shown DONE/Deployed. [B1] | RUNTIME: SQL-11 FAIL, INVALID procedure shown EXECUTION_SUCCEEDED. [O1] | CORE shared outcome gap. BYTEBASE ALSO UNPROVEN for reliable INVALID detection; both actually failed. | Require visible object-status/error inspection for affected PL/SQL before declaring the change successful. |

The lack of a target-side migration ledger does not by itself make CREATE/ALTER execution unusable: Bytebase also held its revision history centrally and SQL-01/02 were PARTIAL under the old contract. ODC SQL-01/02 remain PARTIAL, but normal DDL execution was observed. Both SQLPlus directive bundles failed; directive-heavy scripts need qualification or conversion, not a claim that either is a universal SQLPlus replacement.

## 7. Result/history

| Capability | Bytebase | ODC | Gap | Practical impact |
| --- | --- | --- | --- | --- |
| Statement result | RUNTIME: task output, Oracle errors and statement ranges. [B1] | RUNTIME: statement success/error counts and SQL Window result sets. [O1] | No basic result-display gap; INVALID interpretation failed in both. | Users can inspect routine outcomes centrally. |
| Execution logs | RUNTIME: retained API/UI task error/log details; restart retention not tested. [B1] | RUNTIME: logs existed, but old logs became unreadable; same symptom in later retained capture. [O1], [O2] | IMPORTANT: concrete ODC retention failure; Bytebase restart retention UNKNOWN, BYTEBASE ALSO UNPROVEN. | Incident investigation needs accessible logs after normal pod replacement. |
| Failure status | RUNTIME: FAILED on missing table and partial DDL. [B1] | RUNTIME: EXECUTION_FAILED on missing table and partial DDL. [O1] | No ordinary error-status gap; compile failure remains shared CORE issue. | A failed ticket is visible; earlier Oracle DDL may still have committed. |
| History | RUNTIME: release/revision/version/task links; DOC: database changelog. [B1], [B8] | RUNTIME: ticket SQL, approval history and status survived; results not all retrievable. [O1], [O2] | CORE: version-aware applied-change parity; IMPORTANT: complete retained evidence. | History exists in ODC, but it is less effective as the sole Flyway-style migration record. |
| Downloadable evidence | DOC: audit API/streaming; RUNTIME: API logs retrieved. UNKNOWN: complete one-click deployment evidence bundle. [B10], [B1] | DOC: task log download and audit Excel/CSV export; RUNTIME: sampled old results/attachments returned 500. [O5], [O8][O2] | IMPORTANT: fix ODC download durability. Complete cross-restart bundle is UNKNOWN in both; BYTEBASE ALSO UNPROVEN. | An export button or retained ticket alone does not demonstrate an incident-ready evidence package. |

Keep ticket metadata, SQL attachments/results, task logs and organization audit distinct. Missing attachments do not prove the inventory or all audit metadata disappeared. ODC's 14-day configured file expiry does not explain the sampled files disappearing while younger than that limit. A supported storage/retention fix or bounded export can be sufficient; a new audit service is not required by this comparison. [Retained configuration and retrieval evidence][O2].

## 8. Rollout

| Capability | Bytebase | ODC | Gap | Practical impact |
| --- | --- | --- | --- | --- |
| DEV→SIT→UAT→PROD | RUNTIME: native four-stage rollout and shared artifact; MODEL-07/GOV-04 FAIL for premature MOCKPROD. [B1] | DOC/SOURCE: ordered batch across environments; RUNTIME: four tickets ordered by external runner, MODEL-07/GOV-04 PARTIAL. [O4], [O3][O1] | CORE evidence gap: ODC native journey; no demonstrated Bytebase advantage in mandatory predecessor enforcement. | Prefer a tested native batch/manual stage process; do not treat environment labels as proof of safe automatic promotion. |
| Multiple targets | RUNTIME: one release/plan with four schema targets. [B1] | DOC/SOURCE: 2–100 same-project databases and reusable target templates. [O4], [O3] | CORE evidence gap, not proven feature absence. | A reusable template can reduce repeated selection substantially if the UI matches the docs. |
| Ordering | RUNTIME: lower stages can wait; explicit API dispatch can run higher stage first. [B1] | DOC/SOURCE: serial nodes, parallel databases within a node; RUNTIME: runner-only order. [O4], [O3][O1] | CORE practical acceptance: native order/pause/failure behavior. Stronger universal stage veto: BYTEBASE ALSO UNPROVEN and failed in FREE. | Human continuation after checking the predecessor is acceptable for the practical POC in either product. |
| Stage visibility | RUNTIME: target/stage status in native rollout. [B1] | DOC: batch process and per-database execution records; RUNTIME: separate ticket statuses. [O4], [O1] | CORE evidence gap: inspect native batch progress and failed-target location. | ODC should remove the runner/individual-ticket navigation burden before claiming full rollout parity. |

ODC docs limit aborting a running batch: manual batches can be aborted while waiting for the next group, not while a database change is running. This is an **IMPORTANT operational limitation**, not lack of rollout. Validate a maintenance-window procedure with manual boundaries; do not equate cancel with rolling back committed Oracle DDL. [Batch documentation][O4]; [current official batch page](https://en.oceanbase.com/docs/common-odc-10000000001510652).

## 9. Governance

| Capability | Bytebase | ODC | Gap | Practical impact |
| --- | --- | --- | --- | --- |
| Users | RUNTIME: named requester/executor/service account. [B1] | RUNTIME: separate requester/approver/executor/participant and outsider. [O1] | No basic user-management gap. Actual 20-user operating acceptance UNKNOWN in both. | Central identities replace sharing database credentials for coordination. |
| Roles | RUNTIME: project roles and separate console/rollout permissions. [B1] | RUNTIME: OWNER/DBA/DEVELOPER/PARTICIPANT; DOC: organization roles. [O1], [O6] | IMPORTANT: ODC creator execution permission; map roles deliberately. | Role labels alone do not enforce the team's desired separation. |
| RBAC | RUNTIME: requester rollout denied; query UPDATE initially allowed, then denied after role adjustment. [B1] | RUNTIME: participant QUERY allowed, CHANGE denied, revoke denied again. [O1] | IMPORTANT: test UI/API/console permission scope in both; exhaustive coverage UNKNOWN. | Both provide useful RBAC; console permissions can bypass a ticket process if misconfigured. |
| Audit | DOC: paid audit search/API/streaming; RUNTIME: FREE audit 403/BLOCKED. [B10], [B1] | RUNTIME: 97 POC actor/action/time records; DOC: searchable/exportable operation records. [O1], [O8] | IMPORTANT: export/completeness/retention acceptance unresolved; Bytebase paid audit runtime unproved. | ODC has real basic audit evidence. Do not describe it as having no audit. |
| SSO | DOC: provider/edition choices in pricing; UNKNOWN: actual IdP runtime. [B4] | DOC: OAuth2/OIDC/LDAP and SAML descriptions; UNKNOWN: actual IdP runtime. [O9] | IMPORTANT only if the team's IdP is required; equivalent runtime unproved. | Native identity integration may avoid another login; no new SSO platform is proposed. |

ODC operation-record documentation describes permanent retention, while task-file expiry and observed retrieval failures have a different scope. Neither DOC statement proves restored/exported audit evidence in the actual deployment. Privileged DBA-only execution becomes a **CORE policy blocker only if the team requires it**; this mission has not required a three-person requester/reviewer/executor contract.

## 10. Integration

| Capability | Bytebase | ODC | Gap | Practical impact |
| --- | --- | --- | --- | --- |
| API | RUNTIME: service account creates release/plan/issue, dispatch/poll/query. [B1] | RUNTIME: application login, inventory, ticket creation, approval, Execute and polling. [O1] | IMPORTANT: supported CI identity/API lifecycle needs qualification in ODC. | Neither is UI-only; existing API capability is useful automation evidence. |
| Git | DOC: migration files, PR checks and release creation through CI/API; RUNTIME: release version/SHA, not a real GitOps job. [B9], [B1] | UNKNOWN: native Git-to-ticket/version binding not established in reviewed scope; RUNTIME: local client hash/job reference. [O1], [O3] | IMPORTANT: Bytebase has a clearer documented Git workflow; ODC needs provenance convention or small integration. | A commit/reference plus frozen SQL may suffice for a pilot; native Git binding is not demonstrated. |
| CI/CD | DOC: official GitOps/CI flow; RUNTIME: local service-account API, real Jenkins/GitLab job unproved. [B9], [B1] | RUNTIME: local API runner only; UNKNOWN: live Jenkins/GitLab integration. [O1] | IMPORTANT acceptance gap in both; ODC has fewer evidenced release-specific integration primitives. | Do not present either lab as an observed end-to-end CI deployment. |
| Automation | DOC: version-sequenced migration revisions; RUNTIME: normal replay skip and bounded dedup observations. [B9], [B1] | DOC: automatic/scheduled/manual tasks and batch; RUNTIME: local API orchestration, duplicate new tickets produced two effects. [O4], [O5][O1] | CORE for ordinary migration replay; ADVANCED HARDENING for global exactly-once/crash semantics. | Avoid blind API resubmission. The practical workflow does not require a distributed admission service. |

Bytebase GitOps also uses Git and CI: it is not always a one-system journey. Its documented GitOps approval occurs in VCS PR/MR review rather than automatically inheriting UI custom approval. ODC may remain a one-UI ticket workflow while API integration is qualified independently. [Approval workflow compatibility][B3].

## 11. ODC historical failures by practical severity

Original results below are unchanged. The category describes **why the observation matters now**, not whether the old expected result was met. CORE directly affects the daily workflow; IMPORTANT matters for production operation; ADVANCED HARDENING concerns exceptional failure-mode control beyond this mission.

| Historical issue / original result | Preserved observation | Current classification / severity | Same-standard Bytebase evidence | Adoption consequence |
| --- | --- | --- | --- | --- |
| INVALID object reported success — SQL-11 FAIL | ODC ticket 1000011 succeeded; procedure INVALID with PLS-00201. | PRODUCT DEFECT / CORE outcome gap. JDBC execution success is insufficient to declare a usable PL/SQL change. | RUNTIME: Bytebase SQL-11 also FAIL, DONE/Deployed with INVALID procedure. | Blocks unattended acceptance/promotion, not the reviewed product POC. Require an explicit validity/error check in both; a DBA checklist can close pilot risk. |
| Ordinary replay — REC-02 FAIL; SQL-03 PARTIAL | A new ODC ticket re-executed DML and hit ORA-00001; no version-based skip. | WORKFLOW GAP / CORE for complete Flyway-style replacement. Not a defect in an ad hoc ticket executor's declared identity model. | RUNTIME: Bytebase REC-02 PASS, applied native version skipped and data unchanged. | Material, everyday difference. Use explicit applied-release review for a pilot; do not claim native versioned migration parity. |
| Duplicate/replay — REC-10 FAIL | Two POSTs with same artifact/job reference created distinct tickets and two marker rows. Re-executing a completed ticket was refused. | PRODUCTION HARDENING GAP / IMPORTANT for automated retries. A demand for arbitrary cross-request exactly-once is TEST TOO STRICT FOR CURRENT GOAL / ADVANCED HARDENING. | RUNTIME: Bytebase REC-10 PARTIAL, same-task double dispatch had one effect; global/crash-safe dedup UNKNOWN. | No blind resubmit after a lost response. Ticket lookup/manual confirmation is acceptable in a UI pilot; automate only with a bounded retry policy. |
| Changed-content ticket — REC-08 FAIL | Reused external case ID with changed SQL still created a new ODC ticket; no native migration-version identity. | WORKFLOW GAP / IMPORTANT for version/content traceability. Requiring an arbitrary external case ID to imply immutability is TEST TOO STRICT FOR CURRENT GOAL. | RUNTIME: Bytebase REC-08 also FAIL under strict rejection; WARNING/two hashes and skip are better detection. | Does not prove an approved ODC ticket was edited. Treat corrections as new reviewed tickets; preserve SQL/version provenance. |
| Requester execution — GOV-03 FAIL | Requester denied before approval, accepted after OWNER→DBA approval. SOURCE intentionally permits creator or OWNER/DBA. | WORKFLOW GAP / IMPORTANT; CORE only if independent DBA-only dispatch is required. | RUNTIME: Bytebase requester rollout 403, but console initially allowed UPDATE until role adjustment; FREE approval unproved. | Approved requester execution may be acceptable. Review separation is already demonstrated; do not silently assume stronger SoD. |
| Partial DDL — REC-04 PARTIAL | CREATE committed, ALTER failed, ticket correctly failed; created object remained. | PRODUCTION HARDENING GAP / IMPORTANT recovery procedure. Requiring general rollback/automatic partial-state fencing is TEST TOO STRICT FOR CURRENT GOAL / ADVANCED HARDENING. | RUNTIME: Bytebase REC-04 also PARTIAL with committed CREATE and FAILED task. | Normal Oracle operational risk in both. Inspect completed statements/effects, then approve a forward correction; failed ticket is not proof of rollback. |
| Concurrent execution — REC-09 PARTIAL | Two tickets on one target succeeded; actual overlap/lock boundary uninstrumented. | PRODUCTION HARDENING GAP / IMPORTANT same-target scheduling; distributed fencing/alias-global locks are ADVANCED HARDENING. | RUNTIME: Bytebase REC-09 PARTIAL, one observed effect for same version; full stream serialization UNKNOWN. | Start with one DBA execution window per target. Evidence does not prove either candidate has a global Oracle serialization guarantee. |
| Logs/attachments retention — MODEL-10, REC-01, GOV-09 PARTIAL plus operational failure | Old log readback failed after restart; attachments returned 500. Later capture repeated 4 log failures and 4 result/4 attachment 500s. | PRODUCT DEFECT in the observed deployment / IMPORTANT operational gap; source/configuration root cause UNKNOWN. | RUNTIME: Bytebase logs retrieved; restart/restore retention UNKNOWN, BYTEBASE ALSO UNPROVEN. | Fix before production. Core metadata remains usable; inaccessible incident evidence is a concrete operational cost, not an exactly-once issue. |
| Promotion — MODEL-07/GOV-04 PARTIAL | Same bytes/hash on four schema tickets; external runner controlled order. | WORKFLOW GAP / CORE evidence gap for native daily rollout. Strong verified-state veto on every API path is a separate hardening demand. | RUNTIME: Bytebase native stages existed but MODEL-07/GOV-04 FAIL for early MOCKPROD. | Test ODC's documented native batch first. Requiring a separate rollout controller before that test is disproportionate. |
| Crash/lost ACK/restore/failover — REC-05/06/07/11/12, GOV-06/07 NOT_RUN | No checkpoint/proxy/restore instrumentation; operational restarts were not controlled recovery experiments. | TEST TOO STRICT FOR CURRENT GOAL / ADVANCED HARDENING at this product-comparison stage. | RUNTIME: corresponding Bytebase acceptance NOT_RUN; BYTEBASE ALSO UNPROVEN. | Keep the unknowns in the risk register. They do not veto a normal-workflow POC or add mandatory controller modules. |

Evidence: [original ODC cases][O1], [original Bytebase cases][B1], [source path review][O3], [later retained file retrieval][O2]. The five historical ODC FAILs remain SQL-11, REC-02, REC-08, REC-10 and GOV-03. No FAIL became PASS; PARTIAL and NOT_RUN cases are not relabeled as failures.

## 12. Daily UX comparison

```text
Bytebase UI → SQL/targets → review → paid approval → rollout → results/history
ODC UI      → SQL/targets → review → approval      → execute/batch → results/history
CI reference: Git → Jenkins → review/approval → Flyway → Jenkins HTML/JSON artifacts
```

Counts below are **UNKNOWN as measured UX; estimates from evidenced workflow steps**, not timed sessions or click telemetry. One manual step means one meaningful human action (select, submit, review, approve, start, inspect), not every field/click. SQL editing time and login are excluded equally. Target selections count selection sessions, not selected database checkboxes. The reference scenario is one new change and one target; four-stage implications follow below. Reports archived in Jenkins count as Jenkins, not another application.

| Role | Bytebase: routine systems; manual steps; target selections; result places; recovery places | ODC: routine systems; manual steps; target selections; result places; recovery places | CI reference: routine systems; manual steps; target selections; result places; recovery places |
| --- | --- | --- | --- |
| Developer | 1 UI; 3 actions (select, author, submit); 1 selection; 1 result page; 1 initial task page then DBA escalation. DOC approval journey, RUNTIME authoring/execution substeps. | 1 UI; 3 actions (select, author, submit); 1 selection; 1 ticket/result page; 1 initial ticket then DBA escalation. RUNTIME single-ticket journey. | 2 (Git/Jenkins); 3–4 actions (commit/submit, choose target/start, inspect); 1 selection; 1 Jenkins report; 1 held report then DBA. SOURCE implementation, live UX UNKNOWN. |
| Reviewer | 1 UI; 2 actions (inspect SQL/target, approve) per approval node; 0 selections; 1 result/history location if needed; 1 issue/task then DBA. DOC paid approval, FREE runtime unavailable. | 1 UI; 2 actions per approval node; 0 selections; 1 ticket; 1 ticket then DBA. RUNTIME OWNER→DBA gives 4 actions across two approvers. | 1–2 (Jenkins plus Git for diff context); 2–3 actions (read diff/frozen preview, approve); 0 selections; 1 report; 1 held report then DBA. SOURCE, runtime UNKNOWN. |
| DBA/executor | 1 UI, or 2 with independent Oracle diagnostics; 2–3 actions (confirm/start, inspect, validity check if needed); 0 fresh selections; 1 result place, 2 with diagnostics; at least 2 recovery places (product/Oracle tool). RUNTIME substeps; full paid path UNKNOWN. | 1 UI, or 2 with independent Oracle diagnostics; 2–3 actions; 0 fresh selections; 1 result place, 2 with diagnostics; at least 2 recovery places (ODC/Oracle tool), more if old evidence is missing. RUNTIME single-target path. | 1 Jenkins routinely; 2–3 actions (confirm/start, inspect, resolve diagnostics); 0 fresh selections; 1 report; at least 3 recovery surfaces (Jenkins, restricted agent/state, Oracle tool). SOURCE, runtime UNKNOWN. |
| Platform owner | 2 routine surfaces (product admin and deployment/config tooling); estimated 3–4 actions per target/role onboarding event; 1 registration; 1 product history/health location plus deployment monitoring; 2–3 incident surfaces including PostgreSQL/backup. DOC/RUNTIME deployment, counts UNKNOWN. | 2 routine surfaces (ODC admin and GitOps/Kubernetes); estimated 3–4 actions per target/role onboarding event; 1 registration; 1 product location plus deployment monitoring; at least 3 incident surfaces including MetaDB/storage/adapter. RUNTIME retained deployment, counts UNKNOWN. | 2 routine surfaces (Git and Jenkins/agent admin); estimated 4–6 actions per target/role onboarding event; 1 inventory registration; 1 report plus runner logs; at least 3 incident surfaces including SQLite/agent/Oracle. SOURCE implementation, counts UNKNOWN. |

Platform-owner actions concern occasional onboarding/maintenance, not extra actions on every release. After onboarding, normal inventory selection does not require entering another JDBC URL or password in either product.

For four environments, Bytebase's native target set is **one selection session** followed by up to four start/inspect pairs when manual. ODC's documented native batch/template could also provide **one selection session**, but that is DOC/SOURCE credit; its historical four-ticket journey involved four target selections and the external runner. Those are different evidence levels. Independent OWNER→DBA approval can double approval actions; neither product eliminates human review by having a central UI.

The CI implementation has only one target and no native promotion. A four-environment CI journey is UNKNOWN, not a fictitious implemented dashboard. Bytebase GitOps and an optional ODC Git review both add Git/CI surfaces. Oracle compile diagnostics and partial-DDL recovery remain DBA work in **both** products because both historical success displays missed INVALID.

## 13. Operational ownership

These are actual retained components and implemented packages, not theoretical future safety services. Shared Oracle, Kubernetes, Git and secret infrastructure is counted as shared operation, not as a new installation charge. Existing Jenkins still needs maintenance; its existence does not make custom code ownership free.

| Maintenance item | Bytebase | ODC | CI reference |
| --- | --- | --- | --- |
| Application | RUNTIME: one Bytebase StatefulSet, UI/API/native engine. [B1] | RUNTIME: one ODC Deployment, UI/API/task workers. [O2] | DOC/RUNTIME record: existing Jenkins controller; SOURCE: protected pipeline and installed runner preparation, live job acceptance blocked. [C1], [C2] |
| Metadata/state DB | RUNTIME: embedded PostgreSQL and 2 GiB PVC in lab; DOC: external PostgreSQL for production/HA. [B1], [B11] | RUNTIME: OceanBase CE MetaDB StatefulSet, 10 GiB PVC; ODC app data 5 GiB. [O2] | SOURCE: persistent local SQLite/WAL, transactional state and backup procedure; live state/restore acceptance UNKNOWN. [C2] |
| Configuration/inventory | RUNTIME: projects, environments, roles, Oracle resource configuration; DOC: rollout/approval policy. [B1], [B3] | RUNTIME: projects, environment risk rules, role mappings, datasource/plugin configuration. [O1], [O2] | SOURCE: protected inventory, policy, engine pins, JDBC policy and Jenkinsfile; sample target remains disabled. [C1], [C2] |
| Oracle connectivity/engine | RUNTIME: native driver/TCPS settings; no local custom Bytebase adapter recorded. [B1] | RUNTIME: mounted Oracle plugin and deployment-specific TCPS extension; upgraded jar/source correspondence UNKNOWN. [O1], [O2] | SOURCE/local checks: Flyway 13.9.0 Java wrapper/parser, Python observer, separate Oracle JDBC entitlement/configuration; Oracle execution blocked. [C1], [C2] |
| Storage/logging/reporting | RUNTIME: product metadata/task logs; DOC: paid audit streaming, app/PG storage. Retention runtime UNKNOWN. [B1], [B10] | RUNTIME: app PVC, MetaDB PVC, ephemeral `/opt/odc/log`, inaccessible old files; operator must fix and monitor retention. [O2] | SOURCE: Jenkins artifacts, generated HTML/JSON/SQL/events, protected state; team maintains reporting code and retention. [C2] |
| Credentials | RUNTIME: user/service-account and Oracle datasource credentials; DOC/SOURCE: edition/provider-dependent secret integration. [B1]; [provider review](decision-closing/bytebase-public.md) | RUNTIME: ODC identities, Oracle principals, MetaDB/bootstrap credentials, TCPS policy. [O2] | SOURCE: Jenkins credentials, writer/observer bindings, restricted agent/OS state access; actual target/actors still blocked. [C1], [C2] |
| Backup | DOC: app/metadata production operation; UNKNOWN: restore acceptance. [B11], [B1] | RUNTIME: persistent stores exist; UNKNOWN: coherent backup/restore/retention acceptance. [O2] | SOURCE: SQLite backup plus Git/config/Jenkins archives and Flyway target history; UNKNOWN: live restore acceptance. [C2] |
| Custom tests/code | RUNTIME: no local product patch recorded; qualifying upgrades remains operator work. [B1] | RUNTIME: one local TCPS adapter/build/mount path; no added controller in this comparison. [O1], [O2] | SOURCE/local checks: inventory/artifact runner, state, Flyway wrapper, verifier, reports, pipeline and custom tests. Five owned functional responsibilities, 30 local tests. [C1], [C2] |

Using the mission's requested groupings, Bytebase has **5 ownership categories** (application, metadata DB, configuration, credentials, backup); ODC has **5** (ODC, MetaDB, Oracle plugin/TCPS extension, storage/logging, credentials); CI has **9** (Jenkins, runner, Flyway wrapper, SQLite state, verifier, reporting, target inventory, custom tests, credentials). These are checklist groupings, not equivalent deployable components. The normalized table includes configuration/backup for all three so category counts do not hide duties.

On infrastructure, both product labs have two main application/database processes; ODC additionally owns the local adapter. CI reuses a controller but needs a restricted persistent agent, state and artifacts. On application behavior, Bytebase/ODC upstream owns most UI/workflow code; the team owns CI's binding, gates, state, verification, reporting and regression tests. CI is consequently **more custom code to maintain**, even if it installs fewer new servers. The earlier five-module ODC estimate was conditional on the stronger safety contract, not something already present or required for this practical pilot.

ODC's current requests are 1 CPU/3 GiB for the app and 2 CPU/8 GiB for MetaDB; limits are 2 CPU/4 GiB and 4 CPU/10 GiB. These observed allocations illustrate a real MetaDB operational footprint, not a 50-instance sizing measurement. Bytebase's production guide supplies sizing guidance but no comparable local benchmark. [ODC retained resources][O2]; [Bytebase production setup][B11].

**Ownership conclusion:** Bytebase has the strongest native release/integration packaging; ODC is operationally simpler than building and owning the complete CI workflow, provided ordinary storage/adapter issues can be bounded. CI has stronger implemented local guard logic, but its live acceptance is still blocked. Neither deployment count nor 30 synthetic/local checks prove Oracle or user acceptance.

## 14. Product parity score

**Bytebase product parity reference = 100; ODC = 80/100.** The 100 is a normalization of the evidenced Bytebase product shape in applicable editions, not 100% correctness or a score earned by FREE on every requirement. The score is a transparent comparative judgment, not a benchmark, probability or sum of historical PASS counts.

Credit ordinary capabilities supported by DOC/SOURCE, identify where only RUNTIME gives adoption confidence, and deduct for practical usability/function/ownership differences. No universal percentage discount is imposed on documentation. Do not deduct for missing exactly-once, lost-ACK fencing or restore controllers; do not invent a Bytebase capability to penalize ODC. Shared INVALID and premature-promotion concerns are stated separately, not used as evidence of a Bytebase superiority.

| Area | Weight / Bytebase reference | ODC score | Deduction rationale and evidence boundary |
| --- | --- | --- | --- |
| DB/schema inventory | 10 | 10 | RUNTIME: both have projects, schemas, environments and target IDs. No demonstrated daily feature shortfall. |
| SQL change UX | 10 | 9 | RUNTIME: useful editor/tickets. One-point comparative deduction for weaker reusable release packaging; not absence of SQL authoring. |
| Review | 10 | 8 | RUNTIME: SQL/target visible; SOURCE: ODC approval comments. DOC: Bytebase richer inline discussion/check workflow; ODC matching experience unproved. No credit for Bytebase ERROR enforcement. |
| Approval | 10 | 9 | RUNTIME: ODC two-step approval. One point for less restrictive post-approval execution separation versus Bytebase's observed rollout roles; paid Bytebase approval itself stays DOC. |
| Oracle execution | 15 | 13 | RUNTIME: both execute the main SQL/PLSQL families. ODC's local TCPS adapter leaves a two-point native-connectivity/support disadvantage. Shared INVALID/SQLPlus limitations do not create a relative penalty. |
| Result/history | 10 | 6 | RUNTIME: ODC ticket history exists, but old result/log/attachment retrieval fails and native applied-version history is weaker. Bytebase ordinary revisions/logs observed; its restart retention not assumed. |
| Multi-env rollout | 10 | 7 | DOC/SOURCE: native ODC batch earns substantial credit. Deduction for less established reusable release/stage journey and no native batch runtime. Bytebase universal stage enforcement not credited. |
| Audit/RBAC | 10 | 8 | RUNTIME: ODC actors, grants/revoke and audit records. Deduction for incomplete full export/actor-query acceptance; actual SSO/restore unknown in both. Log-file durability counted under result/history, not again here. |
| API/CI integration | 5 | 3 | RUNTIME: API works. DOC: Bytebase migration/GitOps flow; native ODC Git/version binding unestablished. Neither has a real Jenkins/GitLab deployment in the retained POC. |
| Operational simplicity | 10 | 7 | RUNTIME: separate ODC/MetaDB plus storage incident ownership and plugin upgrade coupling; upstream still owns ordinary UI/workflow. CI's custom platform burden is not charged to ODC. |
| **Total** | **100** | **80** | **20 points of practical feature/UX/operations difference; no advanced distributed-failure deduction.** |

For this report, CLOSE means 90–100, MODERATE GAP means 70–89, LARGE GAP means below 70. These are declared reporting bands, not vendor standards. Native batch and durable evidence could improve the judgment; the exact 80 is less decisive than its explicit deductions. This is also not a purchase comparison: a free OSS preference may favor ODC even when paid Bytebase has higher product parity.

## 15. Production hardening risks

**ODC PRODUCTION HARDENING RISK = HIGH for the observed deployment.** HIGH means material unclosed production evidence/operating controls, not rejection of its daily workflow. Concrete missing old evidence and misleading compile success justify this rating without asserting that an untested crash scenario failed. Bytebase's corresponding hardening cannot be rated LOW from Enterprise docs; its own observed failures and NOT_RUN cases remain.

| Risk/control | ODC evidence | Bytebase held to the same standard | Practical classification |
| --- | --- | --- | --- |
| Compile outcome | RUNTIME: INVALID reported success. | RUNTIME: same failure; BYTEBASE ALSO UNPROVEN for reliable detection. | CORE shared acceptance check, closable initially by explicit DBA verification. |
| Retained evidence | RUNTIME: logs/results/attachments unavailable after replacements; metadata survives. | RUNTIME: logs retrieved; cross-restart durability UNKNOWN, BYTEBASE ALSO UNPROVEN. | IMPORTANT before production; supported persistence/export may suffice. |
| Roles and routine retries | RUNTIME/SOURCE: creator executes after approval; repeated new tickets can repeat effects. | RUNTIME: rollout denial/replay skip/bounded dedup stronger; full approval and all-path controls unproved. | IMPORTANT; conditional CORE if the team insists on DBA-only dispatch or full versioned-engine replacement. |
| Partial DDL and simultaneous target work | RUNTIME: failed ticket with committed CREATE; concurrency instrumentation incomplete. | RUNTIME: partial CREATE and incomplete concurrency proof too. | IMPORTANT operator procedure; automate only after understanding normal failure handling. |
| Lost ACK after Oracle commit | UNKNOWN; historical NOT_RUN. | UNKNOWN/NOT_RUN; BYTEBASE ALSO UNPROVEN. | ADVANCED HARDENING; no main-score deduction. |
| Stale metadata restore | UNKNOWN; historical controlled restore NOT_RUN. | UNKNOWN/NOT_RUN; BYTEBASE ALSO UNPROVEN. | ADVANCED HARDENING beyond ordinary backup duties. |
| Alias-global serialization/distributed fencing/exactly-once | UNKNOWN; not established by batch order or ticket IDs. | UNKNOWN; bounded dedup does not demonstrate this, BYTEBASE ALSO UNPROVEN. | ADVANCED HARDENING; no mandatory custom UNKNOWN_OUTCOME/admission controller. |

Retain named DBA recovery ownership and ordinary backup/log procedures. Do not transform those duties into a new distributed state architecture for this decision.

## 16. Minimum practical gaps

Five bounded items are sufficient to decide an internal pilot. Items 1–3 should be closed or explicitly demonstrated before a production pilot; items 4–5 define the operating scope and can use a written, reviewable process. None presupposes a new platform.

1. **Demonstrate native multi-target rollout.** Use ODC batch/template, inspect SQL/targets, apply the intended approvals, pause between environment groups, and show per-target results and stop-on-error. Replace the old external sequencing runner with the native journey if it works. This is a CORE evidence gap, not an established missing feature.
2. **Make Oracle PL/SQL acceptance explicit.** Record VALID/object errors for affected procedures/packages/triggers before continuing. A DBA check through supported ODC tooling or an Oracle tool is enough for a controlled pilot; automated completion gating is a later choice. Qualify the intended Oracle version and TCPS connector at the same time. Shared CORE outcome issue; Bytebase needs the same check.
3. **Keep results, SQL attachments and logs retrievable.** Fix supported storage/file paths/retention or use a bounded export, and verify accessibility after normal restart/replacement. Retain actor/target/time with the ticket. IMPORTANT operational closure before production; this does not require a separate audit application.
4. **Agree normal version/replay and correction handling.** Use a release/version/commit reference and exact stored SQL, inspect whether it was already applied, and require a new reviewed correction ticket. Avoid blind retries and concurrent same-target dispatch. A simple applied-change register can support a UI pilot; it is not native automatic replay parity. If automatic versioned replay is mandatory to retire Flyway, this remains a CORE unresolved gap rather than a claimed script fix.
5. **Confirm the actual actor/permission policy.** Demonstrate distinct requester/reviewer and restrict console write access. Explicitly decide whether approved requester execution is acceptable; if DBA-only dispatch is mandatory, do not pretend a checklist enforces it. Validate a narrow API/provenance flow for the existing CI requirement; native Git binding/full audit export can follow the UI pilot. IMPORTANT by default, conditionally CORE for mandatory independent execution.

No inventory, SQL editor, human approval, basic Oracle execution or basic ticket history subsystem needs to be rebuilt. Richer Git binding, audit export and SSO remain IMPORTANT follow-ups, not extra controller modules or automatic blockers for a manual UI pilot.

## 17. Recommendation

**POC ODC for practical adoption: YES.** Prioritize its native journey over further deep release-controller research. The old HOLD was a conclusion under a stronger contract and module-count threshold; it does not decide this new product/workflow mission. Historical acceptance files, candidate statuses and CI results remain preserved; this recommendation is not a new runtime PASS or production authorization.

ODC already delivers the largest missing improvement over the current manual model: a shared database inventory and a reviewable, approved SQL work item connected to execution/history. Bytebase remains better for native versioned releases and documented GitOps packaging, but its FREE run cannot supply production approval/audit or an ideal Oracle success/promotion standard. CI remains a viable integration/fallback with more team-owned code and currently blocked live acceptance; it is not the default UX benchmark.

**Minimum next tests for a future focused POC, not performed here:** one role-separated ticket journey using retained inventory; one native ordered batch with a failing-target/manual-boundary check; one intended-version Oracle PL/SQL/TCPS validity journey; one result/log/attachment retrieval check after ordinary replacement; one normal duplicate/correction/API-provenance check. These are targeted adoption checks, not another 45-case run or crash/restore campaign. This report executed only the existing read-only document verifier and static preservation/structure checks.

```text
BYTEBASE PRODUCT PARITY REFERENCE = 100

ODC PRACTICAL PARITY SCORE = 80/100
ODC PRODUCTION HARDENING RISK = HIGH

ODC CORE GAPS =
1. Native versioned applied-change/replay parity if fully replacing Flyway.
2. Reliable PL/SQL validity acceptance; Bytebase failed the same check.
3. Native Oracle multi-target rollout journey not yet demonstrated at runtime.

ODC IMPORTANT BUT NON-BLOCKING GAPS =
1. Durable log/result/attachment retrieval; close before production use.
2. Independent-executor policy and complete permission-path qualification.
3. Native Git/CI provenance and full audit-export acceptance.

ODC ADVANCED HARDENING GAPS =
1. Lost-ACK/commit-ambiguity handling; BYTEBASE ALSO UNPROVEN.
2. Stale metadata restore reconciliation; BYTEBASE ALSO UNPROVEN.
3. Alias-global serialization, distributed fencing and exactly-once;
   BYTEBASE ALSO UNPROVEN.

ODC VS BYTEBASE = MODERATE GAP

ODC VS DBeaver + Flyway CLI = MAJOR IMPROVEMENT

WOULD I POC ODC FOR PRACTICAL ADOPTION = YES

WHY = Integrated inventory/review/approval/Oracle execution already has
historical runtime evidence. Remaining daily-workflow gaps are bounded;
Bytebase itself has shared failures and edition/runtime limits.

MINIMUM NEXT TESTS = Role-separated ticket journey; native ordered batch;
Oracle validity/TCPS qualification; restart evidence retrieval;
normal duplicate/correction/API provenance. Future POC only; no SQL here.
```
