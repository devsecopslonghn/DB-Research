# Final decision: self-hosted Oracle database change management

Decision closed **7 October 2026** against [current-baseline.md](current-baseline.md). The baseline remains the factual requirements, evidence and candidate-status authority. This document closes the research recommendation; it does not record adoption or authorize runtime, purchase, trial, deployment or vendor contact.

## 1. Executive decision

**Prefer a gated Bytebase Enterprise native evaluation if commercial software is allowed. If OSS-only, select the existing CI + Oracle migration-engine fallback for the next bounded contract POC. Stop spending research time on unchanged ODC and on the premise that AccessFlow needs only a small Oracle runner.**

No retained product has passed the complete adoption contract. The decision is nevertheless actionable: Bytebase has the best documented chance to remove owned governance, dispatch and presentation code; CI is the defensible OSS fallback when integrated options do not qualify. AccessFlow does not currently remove the difficult correctness responsibilities, and ODC has no publicly established supported safety delta.

The Bytebase branch has a **commercial and supported-control feasibility gate before Oracle regression**. A suitable quote alone is insufficient. Public 3.23.0 evidence does not establish fixes for the historical INVALID, altered-content or early-promotion failures. Reject its simplicity claim if safe operation needs a separate admission/promotion/recovery controller. Do not turn this gate into indefinite product research: establish the selected build, legitimate access and supported configuration, then perform one bounded regression or choose CI.

| Option | Canonical status retained | Final allocation decision |
| --- | --- | --- |
| ODC native | HOLD | No unchanged POC or continuing source survey; reopen only on concrete supported safety evidence. |
| AccessFlow deployment API + engine | RESERVE | No next POC by default; consider only a demonstrated reuse/ownership advantage over CI. |
| Bytebase EE self-hosted | COMMERCIAL_CHECK | Preferred commercial branch, conditional on entitlement and bounded native control feasibility. |
| Existing CI + one Oracle engine | FALLBACK | Selected OSS-only branch; use the existing reference without further architecture design. |

## 2. Goal

Choose the simplest maintainable self-hosted Oracle change-management workflow for approximately **50 Oracle instances and 20 human users**, preferably free OSS, that materially improves DBeaver/manual SQL and standalone Flyway CLI:

```text
Login → inventory → change request → exact SQL/target review → approval
→ controlled execution → verification → DEV → SIT → UAT → PROD
→ retained history/audit → held, accountable recovery
```

Minimize manual DBA work, systems, custom correctness code and operational ownership while retaining Oracle correctness, approval, traceability, controlled rollout and recovery safety. CI/CD integration is required; CI need not be the daily platform UI. Fifty Oracle instances are not necessarily fifty endpoints, schemas, PDBs, license units or targets per release.

## 3. Evidence boundary

Public checks use official documentation, release metadata and pinned source. **DOC/SOURCE establishes product descriptions or code paths; RUNTIME establishes observed behavior at one exact artifact and topology; DESIGN is proposed behavior.** Public absence findings are scoped to the inspected contracts and releases, not claims about every possible binary implementation.

| Retained historical observation | Exact scope | Result boundary |
| --- | --- | --- |
| [ODC POC](../ODC-ORACLE-POC-RESULTS.md) | 4.4.1-20260116; Oracle 26ai EE 23.26.4.1.0; four environment schemas on one service; OceanBase CE 4.3.5 MetaDB | 12 PASS / 20 PARTIAL / 5 FAIL / 8 NOT_RUN. No rescore. |
| [Bytebase POC](../BYTEBASE-ORACLE-POC-RESULTS.md) | 3.22.1/FREE, `a85f6cb4195299995e8554303550d672d5093e1d`; same Oracle lab | 17 PASS / 14 PARTIAL / 4 FAIL / 3 BLOCKED / 7 NOT_RUN; extra SQL-review FAIL outside the original 45. EE NOT_RUN. |

No new Oracle, product, recovery or scale test was run. The real estate, Oracle 19c/21c, RAC and 50-instance/20-user execution are uncertified. Public work closes questions; it cannot establish private rights, actual budget or runtime acceptance. The [question register](open-questions.md) classifies all 32 original questions and the newly closed public facts.

## 4. ODC final research status

**ODC remains HOLD. No supported public delta reduces its five provisional safety responsibilities to at most two bounded additions. This branch is closed for current research.**

Official vendor documentation now lists V4.5.0 and V4.4.3. GitHub's latest published release remains `v4.3.4_bp2`, and current public HEAD remains the previously reviewed `d517c0f27971642fb0cd7565fd61ab2309875ec3`. Later documentation identifies product versions but does not map the historical 4.4.1 image to source or establish a safety fix. [Pinned public delta review](decision-closing/odc-public-delta.md), [official V4.5.0 notes](https://www.oceanbase.com/docs/common-odc-1000000006663615), [GitHub release](https://github.com/oceanbase/odc/releases/tag/v4.3.4_bp2).

The recheck covers immutable SQL/options/targets; cross-request duplicate/replay and altered-content rejection; canonical schema serialization; requester/executor separation; approval; verified native stage progression; INVALID diagnostics; completion hooks; HOLD/recovery; logs/audit; restart/restore. Native tickets, batch order, approval and audit remain useful, but none establishes the missing end-to-end control contract. The inspected permission helper still allows creator execution; statement success is not an Oracle validity check. No completion extension was established that retires admission, verified continuation and recovery ownership. [Reviewed permission helper](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/FlowPermissionHelper.java), [area-by-area evidence](decision-closing/odc-public-delta.md#public-capability-check).

**Product conclusion:** strong integrated OSS inventory/ticket/PLSQL workflow, currently unsuitable for adoption under the complete safety contract. A verifier alone cannot repair replay, actor or uncertain-outcome control.

**Estate conclusion:** required versions, TCPS, RAC aliases, grants, corpus and storage can further disqualify it. Favorable estate answers cannot remove its public safety gate.

**POC conclusion:** no ODC POC now. A future supported mapped artifact must first demonstrate closure within two bounded additions, then regress SQL-11, REC-02/04/08/09/10, GOV-02/03/04, native promotion, log/attachment retention and instrumented unknown-outcome recovery. Do not repeat historical failures without that delta.

## 5. AccessFlow final research status

**AccessFlow + engine is a supported composition, but no demonstrated smaller solution than existing CI + engine. Retain RESERVE; do not select it as the default next POC.**

Current main remains `c8bb247637df76ce36e52f47b45899823409495e`; latest published release is v2.7.0, tag `2ba5d322e7e1b4c750b5b0af85935e9ae814bd6a`. The supported lifecycle is submit → review → gate → confirm → report outcome. Native schema-change execution remains STOP; it must not substitute for this external branch. [Currentness and source review](decision-closing/accessflow-public-contract.md), [supported API guide](https://github.com/bablsoft/accessflow/blob/c8bb247637df76ce36e52f47b45899823409495e/docs/18-deployment-governance.md).

| Required invariant | Public API/source conclusion | Remaining external responsibility |
| --- | --- | --- |
| Immutable SQL/options and exact targets | Artifact/commit references and metadata are optional strings; no required digest or resolved Oracle target envelope. | Bind immutable bytes/options and canonical service/PDB/schema targets to approval. |
| Human/service identity and approval | API-key owner, optional initiating-human attribution, review plans and self-approval guard exist. | Trusted attribution and required independent requester/reviewer/executor policy. |
| Exclusive claim and duplicate prevention | Run-tuple submission uniqueness and optimistic status locking exist. Already-EXECUTED confirmation returns success again; no runner claim/lease is supplied. | Durable Oracle release admission and one writer per canonical stream, across different run IDs and aliases. |
| Per-target PARTIAL/UNKNOWN truth | Outcomes are caller-reported SUCCEEDED/FAILED/ROLLED_BACK, without per-target partial/unknown states. | Retained target attempts, uncertainty HOLD and reconciliation. |
| Verified promotion | Version projections reflect confirmed/reported deployment state. | Oracle effects/validity/history verification must veto later dispatch. |

`EXECUTED` means execution confirmation was accepted. **It does not mean Oracle execution succeeded.** The [confirmation source](https://github.com/bablsoft/accessflow/blob/c8bb247637df76ce36e52f47b45899823409495e/backend/src/main/java/com/bablsoft/accessflow/deploygov/internal/DefaultDeploymentGateService.java) and [outcome source](https://github.com/bablsoft/accessflow/blob/c8bb247637df76ce36e52f47b45899823409495e/backend/src/main/java/com/bablsoft/accessflow/deploygov/internal/DefaultDeploymentOutcomeService.java) establish those boundaries.

**Product conclusion:** suitable as an approval/control-plane component; not a shipped Oracle release controller. All five baseline safety/operational responsibilities remain, even if implemented in one runner process.

**Estate conclusion:** if CI is already maintained, adding AccessFlow usually adds a platform and lifecycle to reconcile. If AccessFlow already has owners while CI does not, reuse can reverse marginal infrastructure burden. That exception requires evidence and does not erase runner correctness work. A general-purpose CI system is optional in the AccessFlow branch.

**POC conclusion:** select only if that reuse comparison favors it. First test changed artifact/target under the same run tuple, different run IDs, two confirm callers, repeated EXECUTED confirmation, service/on-behalf attribution, post-commit restart/lost outcome, per-target HOLD and premature PROD. Reject if AccessFlow status can overrule unverified Oracle outcomes or if five responsibilities are presented as a small API adapter.

## 6. Bytebase EE final public assessment

**Bytebase EE is the best documented integrated commercial branch, with a conditional simplicity advantage. It is not a proved Oracle winner.** The public plan boundary is resolved; the quote and exact-build acceptance are separate gates. [Detailed public evidence](decision-closing/bytebase-public.md).

| Current edition fact | Community | Pro | Enterprise |
| --- | --- | --- | --- |
| Published user allowance | 20 | Custom | Custom contracted |
| Published database-instance allowance | 10 | 10 | Custom contracted |
| Approval workflow | Unavailable | Unavailable | Available |
| Audit log | Unavailable | 7-day retention | Unlimited retention advertised |
| External secret manager | Unavailable | Unavailable | Available |
| Custom roles / environment tiers | Unavailable | Unavailable | Available |
| SSO | Unavailable | Google/GitHub | Enterprise identity options |
| HA | Unavailable | Unavailable | Add-on |

These are **PUBLICLY VERIFIED DOC** from the [current edition matrix](https://www.bytebase.com/pricing/). Its Pro summary wording does not override the feature table's Enterprise-only approval boundary. Neither Community nor Pro qualifies for approximately 50 Bytebase-counted instance records. EE capacity is contracted, not publicly unlimited. No suitable estate price is published or invented here.

Other public facts are closed as follows:

| Subject | PUBLICLY VERIFIED DOC/SOURCE | Boundary still requiring input/proof |
| --- | --- | --- |
| Self-host architecture | Bytebase application plus PostgreSQL metadata; production sizing guidance covers 50 users/50 instances; air-gapped operation described. Embedded or external metadata deployment is documented. | Choose actual artifact/storage/backup policy; sizing is not a load benchmark. [Production setup](https://docs.bytebase.com/get-started/self-host/production-setup). |
| Upgrade/restore | Metadata backup and restoration procedures; in-place downgrade unsupported. | Restored metadata must be reconciled against Oracle commits before dispatch. [Upgrade/restore](https://docs.bytebase.com/get-started/self-host/upgrade). |
| Oracle | Vendor matrix lists 11g+; service/SID connection and schema inventory. 3.23.0 source uses go-ora v2.9.0, not JDBC/Flyway. | Actual versions/RUs, RAC/TCPS/grants and mandatory scripts need exact-build proof. [Database matrix](https://docs.bytebase.com/introduction/supported-databases), [pinned driver dependency](https://github.com/bytebase/bytebase/blob/c8188c635465321ff930c97200742a96ef653144/go.mod). |
| Counting terms | A Bytebase Oracle Instance is a configured server/service endpoint; a Bytebase Database represents an Oracle schema. | Contractual RAC/PDB/alias/standby/duplicate-registration and service-identity billing rules require written confirmation. [Instance concept](https://docs.bytebase.com/concepts/instance). |
| Approval/audit | Custom routing/sequential approval; 3.23.0 can forbid the last plan editor approving. That setting differs for existing versus new projects. Audit actor now distinguishes users/service accounts/workload identities. | Configure actor separation explicitly and prove exact SQL/target mutation invalidation, refused-call retention and every write path. [Approval](https://docs.bytebase.com/change-database/approval), [audit](https://docs.bytebase.com/security/audit-log), [release notes](https://github.com/bytebase/bytebase/releases/tag/3.23.0). |
| API/service identity | Scoped service accounts/API keys and short-lived OIDC workload identities are documented; release/plan/rollout APIs exist. | Prove initiating-human attribution, actual permissions/key lifecycle and UI/API/console consistency. [Service accounts](https://docs.bytebase.com/administration/service-account), [workload identities](https://docs.bytebase.com/administration/workload-identity/overview). |
| Secrets | Enterprise supports Vault KV v2, AWS Secrets Manager, Google Cloud Secret Manager and Azure Key Vault. Vault uses token/AppRole; cloud providers use their SDK credential chains. | Actual identity/network path, rotation, grants and redacted evidence require estate/configuration proof. [Pinned provider/source assessment](decision-closing/bytebase-public.md#external-secret-managers-source-bytebase-3230). |
| Release/rollout semantics | Retained release SQL/digests, plans, environment stages, per-database tasks and attempts. UI Plan checks are pre-execution; GitOps Release plans do not run those UI checks. | Native per-target task success is not Oracle verified success. Prove predecessor enforcement through UI/API, not just an intended sequence. [Release](https://docs.bytebase.com/concepts/release), [rollout](https://docs.bytebase.com/concepts/rollout), [rollout policy](https://docs.bytebase.com/change-database/environment-policy/rollout-policy). |

**Current public release is 3.23.0**, `c8188c635465321ff930c97200742a96ef653144`, published 24 September 2026. Its Oracle additions concern database-link access and object-definition viewing. The inspected migration executor is byte-identical to historical 3.22.1; other driver/API changes are scoped in the evidence note. This neither proves every old failure persists nor supplies a demonstrated fix. [Release](https://github.com/bytebase/bytebase/releases/tag/3.23.0), [bounded source comparison](decision-closing/bytebase-public.md#publicly-verified-post-3221-sourcerelease-delta-source--release-notes).

The source has an MIT-covered subset and explicit commercial exclusions for Enterprise and feature/permission/role/plan-control code. Enterprise production use requires applicable subscription/agreement rights; the license permits development/testing without a subscription, which does not grant feature activation or authorize a trial here. Public source visibility is not unrestricted OSS Enterprise entitlement. [Pinned root license](https://github.com/bytebase/bytebase/blob/c8188c635465321ff930c97200742a96ef653144/LICENSE), [Enterprise license](https://github.com/bytebase/bytebase/blob/c8188c635465321ff930c97200742a96ef653144/LICENSE.enterprise).

No first-class post-execution Oracle verifier/advancement contract was established in the inspected public interfaces. A final, approved anonymous PL/SQL verification block that raises an application error is a **plausible DESIGN inference** from native PL/SQL support. It could veto one task if errors propagate correctly. It does not itself solve strict changed-content admission, cross-stage bypass, partial commits or unknown outcomes. The bounded task-run handler inspection does not prove whole-product absence of ordering, but does not establish the required predecessor predicate either. [Pinned task-run API](https://github.com/bytebase/bytebase/blob/c8188c635465321ff930c97200742a96ef653144/backend/api/v1/rollout_service.go), [Oracle object status](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/ALL_OBJECTS.html).

**Product conclusion:** best integrated workflow fit, conditional on native enforcement and recovery passing. The baseline's **one verifier, possibly a second evidence-export addition** is an optimistic DESIGN ceiling to test, not a publicly proved implementation path.

**Estate conclusion:** commercial prohibition/unacceptable quote, unsupported required Oracle/client semantics, unsuitable credential/identity integration or insufficient operator ownership can disqualify it. Mandatory SQLPlus behavior is a material case, not a reason to silently reduce scope.

**POC conclusion:** require legitimate exact EE artifact and supported configuration, then test the historical FREE negatives first. If success requires an external admission/promotion/recovery state service, reject the assumed simplicity advantage instead of expanding the POC into a new platform.

**REQUIRES COMMERCIAL QUOTE / PRIVATE ENTITLEMENT:** actual self-hosted rights and counts, service/workload-account billing, selected paid features/providers/add-ons, price, support/renewal and lawful licensed-artifact access. Current plan features, public release, architecture, API availability and advertised Oracle support do not require a sales conversation to resolve.

## 7. CI fallback status

Keep the existing [S6 reference](decision-gates.md#3-jenkinsflyway-feasibility) and [five-package boundary](architecture-reassessment.md#12-custom-code-comparison). No new public evidence in this round retires or materially expands that boundary; **no further fallback architecture is designed here**.

**Product conclusion:** existing Git/CI plus one Oracle-capable migration engine is a viable composition reference, not a turnkey database platform. It still owns immutable inventory/artifact binding, actor/approval/promotion policy, durable admission/serialization/HOLD, Oracle verification/reconciliation and central retained results.

**Estate conclusion:** existing maintained CI, protected-environment entitlement, secrets/storage and qualified owners determine marginal burden. Jenkins is not assumed to exist or mandatory; substitute an already operated CI only with equivalent controls. Flyway Community is the familiar engine reference, not an irrevocable choice.

**POC conclusion:** select the existing contract probe before its Oracle acceptance probe. Require all five responsibilities to have owners and explicit pass criteria. Do not present a passing migration CLI as completion of inventory, governance, verified rollout or recovery.

## 8. Workload scenario compatibility

These classifications concern the workload archetype, not adoption eligibility. All full workflows need runtime acceptance; ODC remains HOLD irrespective of syntax fit. AccessFlow and CI columns use the existing Oracle/Flyway Community reference engine.

| Workload | ODC native | AccessFlow + engine | Bytebase EE | CI + engine |
| --- | --- | --- | --- | --- |
| W1 Simple DDL | LIKELY_SUPPORTED | LIKELY_SUPPORTED | LIKELY_SUPPORTED | LIKELY_SUPPORTED |
| W2 DML data migration | NEEDS_RUNTIME_PROOF | LIKELY_SUPPORTED | LIKELY_SUPPORTED | LIKELY_SUPPORTED |
| W3 Package/procedure/trigger release | NEEDS_RUNTIME_PROOF | NEEDS_RUNTIME_PROOF | NEEDS_RUNTIME_PROOF | NEEDS_RUNTIME_PROOF |
| W4 Cross-schema / privilege change | SUPPORTED_WITH_ADAPTATION | SUPPORTED_WITH_ADAPTATION | SUPPORTED_WITH_ADAPTATION | SUPPORTED_WITH_ADAPTATION |
| W5 Mandatory SQLPlus-heavy legacy behavior | LIKELY_BLOCKER | LIKELY_BLOCKER | LIKELY_BLOCKER | LIKELY_BLOCKER |

W1 has useful historical native DDL evidence and documented engine support. W2's ordinary SQL syntax is plausible elsewhere, but ODC's recorded repeat-DML effects prevent assuming safe migration behavior; all candidates need explicit transaction/effect/replay tests. W3 must check package spec **and body**, procedure/function/trigger validity, diagnostics, dependency effects and invocation. A PL/SQL compilation warning or successful driver return does not complete the release.

W4 requires approved privilege scopes, exact touched-schema sets, dependency checks and serialization across service aliases. Changing current schema does not grant privileges. `ALL_OBJECTS`/`ALL_ERRORS` visibility follows the executing observer's access; owner/name/type filtering and pre-existing invalid objects must be handled deliberately. [Oracle object catalog](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/ALL_OBJECTS.html), [compilation diagnostics](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/ALL_ERRORS.html).

W5 is a blocker **for the default native/JDBC path when native client semantics are mandatory**. Convert it to SUPPORTED_WITH_ADAPTATION only after owners approve equivalent conversion or an entitled supported native-client component passes the corpus. Flyway's built-in SQLPlus emulation is paid Teams functionality and is not full client parity; unsupported commands can be ignored with warnings. Do not strip @/@@, substitutions, WHENEVER or SPOOL and call the script unchanged. [Current Flyway Oracle reference](https://documentation.red-gate.com/flyway/reference/database-driver-reference/oracle-database).

| Estate scenario | Decision consequence |
| --- | --- |
| Mostly 19c/21c with ordinary supported SQL/PLSQL, normal reviewed forward-fix recovery | Bytebase EE remains preferred commercial evaluation; CI is selected OSS fallback. Corpus/driver regression decides adoption. |
| Mandatory native SQLPlus/SQLcl semantics that cannot be converted | Establish an approved supported client-capable engine/component first; default Bytebase/ODC native execution is not presumed viable. Keep the central workflow and safety contract. |
| Many RAC/service aliases, PDBs or shared-schema streams | Canonical target/lock identity and quote mapping become entry-critical; physical instance count alone cannot decide fit. |
| Required whole-file rollback for mixed DDL/DML | No candidate can promise general Oracle DDL atomicity. Owners must accept explicit forward-fix/compensation semantics or the requirement is incompatible. |
| Neither reusable infrastructure nor ownership for custom correctness code | Do not choose greenfield CI/AccessFlow merely for zero platform license cost. Resolve commercial/support or staffing capacity before implementation. |

Oracle commits around DDL and can lose the client acknowledgement after a durable commit. A failed task, cancelled job or restored metadata does not prove effects were undone or permit automatic replay. [Oracle COMMIT semantics](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/COMMIT.html).

## 9. UX/operational comparison

Counts are distinct routine interfaces, not containers or measured clicks. Git is optional for integrated native workflows. Oracle incident inspection is additional whenever needed.

| Candidate | Developer journey / systems | Reviewer journey / systems | DBA journey / systems |
| --- | --- | --- | --- |
| ODC | Login → project/databases → target → SQL ticket → submit. **1** platform. | Ticket exact SQL/target → approve/reject. **1** platform; actor/envelope gaps remain. | PROD approval → native Execute → task/logs → Oracle verify/recover. **2 today**; native verified status/retention unaccepted. |
| AccessFlow composition | Git SQL/PR + AccessFlow datasource/pipeline/environment/request. **2**. Runner submits the deployment record. | Git exact SQL/artifact + AccessFlow target reference/approval. **2**; frozen Oracle targets must be supplied by integration. | AccessFlow approval → runner execution/evidence → per-target verification/HOLD → Oracle recovery. **2–3**; runner can expose linked evidence without a separate product UI. |
| Bytebase EE | Login → project/inventory → Plan targets/SQL → Ready for Review. **1**, or 2 with Git authoring. | Plan SQL/checks/resolved targets → required review/approve/reject. **1** UI workflow. | PROD approval → authorized Rollout stage → tasks/logs/revisions → verification → held recovery. **1 routinely only if gating passes; 2 during Oracle incidents**. |
| CI fallback | Git SQL/PR → CI inventory/target preview → request job. **2**. | Git exact SQL + authenticated CI deployment approval/target preview. **2**. | CI approval/run/results → retained verifier/HOLD evidence → Oracle recovery; Git forward-fix if required. **2–3**. |

These journeys reconstruct DOC/SOURCE and historical UI observations; they are not new usability acceptance. [Existing UI evidence](goal-aligned-final-assessment.md#6-uiworkflow-comparison), [Bytebase first change tutorial](https://docs.bytebase.com/tutorials/first-schema-change), [AccessFlow detail source](https://github.com/bablsoft/accessflow/blob/c8bb247637df76ce36e52f47b45899823409495e/frontend/src/pages/deployments/DeploymentDetailPage.tsx).

During a failed release, a DBA must understand these moving parts:

| Candidate | Logical moving parts to reconcile | Distinct state authorities / owners |
| --- | --- | --- |
| ODC | ODC → Oracle; adding a guard/verifier may add an incident state surface. | **2 native**: ODC workflow/results and Oracle effects. **At least 3** if a separate admission/HOLD ledger is required. Unsafe native simplicity is not a saving. |
| AccessFlow | Git → AccessFlow → runner/state → engine → Oracle. | **4 authority domains**, **5 writers/owners** counting engine history: artifact, approval/version projection, durable attempt state, Oracle history/effects. |
| Bytebase EE | Bytebase → Oracle; inline verifier can remain within one approved task. | **2**: platform release/task/revision state and Oracle effects. Optional Git adds artifact authority; independent guard state invalidates the assumed minimum. |
| CI fallback | Git → CI → durable state/guard → engine → Oracle. | **4 authority domains**, **5 writers/owners** counting engine history: artifact, approval/run, durable attempts, Oracle history/effects. |

Engine history and Oracle effects share a database but can disagree after committed DDL. Counts describe logical incident responsibilities, not automatically separate servers. Bytebase wins this simplicity test only if native state/authorization/recovery passes. AccessFlow swaps the governance UI; it does not remove an incident authority. [Existing authority comparison](architecture-reassessment.md#11-state-authority-comparison).

## 10. Cost/ownership comparison

Qualitative **DESIGN judgment**, not currency, person-days or measured savings. LOW/MEDIUM/HIGH/VERY HIGH compare the full safe operating model. Bytebase license HIGH means greatest commercial cost exposure here; actual magnitude needs a quote. Its low custom burden is conditional.

| Dimension | ODC native made safe | AccessFlow + engine | Bytebase EE | Existing CI + engine |
| --- | --- | --- | --- | --- |
| License cost exposure | LOW | LOW, engine edition caveat | HIGH, unquoted | LOW, existing CI/engine rights caveat |
| Implementation burden | HIGH | HIGH | MEDIUM, conditional | HIGH |
| Custom correctness burden | VERY HIGH / unsupported extension risk | HIGH | LOW if native gates pass; otherwise HIGH and reconsider | HIGH |
| Upgrade burden | HIGH | HIGH | MEDIUM | HIGH |
| DBA burden | HIGH | HIGH | MEDIUM; recovery ownership remains | HIGH |
| DevOps burden | HIGH | HIGH; VERY HIGH greenfield | MEDIUM | HIGH; lower marginal setup if already operated |
| Owned functional responsibilities | 5 provisional | 5 | 1–2 optimistic ceiling, not established | 5 |
| Core deployed units outside Oracle | 2 minimum app + MetaDB; more if guarded | 4 platform units + restricted runner/state host = 5 minimum | 2 chosen app + external PostgreSQL shape; embedding reduces deployment units, not metadata responsibility | 2 reference controller + runner/state host; reuse may reduce new units |
| Persistent lifecycle locations outside Oracle | Metadata + SQL/log files = 2; guard adds state | Platform PostgreSQL/Redis + attempt/evidence lifecycles = 4 | Metadata + retained evidence lifecycles = 2; may share protected storage | CI home + attempt state + immutable evidence = 3; may share protected storage |
| Incident authority domains | 2 unsafe native / at least 3 guarded | 4, plus engine as writer | 2 conditional | 4, plus engine as writer |

Existing Git, IdP, secrets and backup services are excluded from deployed-unit totals but remain owned integrations. Logical storage locations can share infrastructure. The reviewed [AccessFlow compose](https://github.com/bablsoft/accessflow/blob/c8bb247637df76ce36e52f47b45899823409495e/docker-compose.yml) and [baseline operations comparison](architecture-reassessment.md#13-operational-simplicity-comparison) support these minimum/reference shapes.

Zero platform license price does not demonstrate lowest total ownership. Conversely, paid EE rights do not establish safety. The comparison favors buying a native workflow **only if it deletes critical custom state/policy services in practice**.

## 11. Decision tree

```text
Is commercial software allowed and the mandatory Oracle/client workload plausible?
│
├─ YES → Bytebase EE commercial + supported-control feasibility gate
│        ├─ suitable rights/counts/budget + exact licensed build/configuration
│        │  + bounded verification path → one EE native regression POC
│        │      ├─ native admission/actors/promotion/recovery pass,
│        │      │  with ≤2 bounded additions → select staged adoption
│        │      └─ fail or require separate safety controller → OSS fallback
│        └─ quote/build/control path not viable → OSS fallback
│
└─ NO / OSS-only / native workload incompatible → OSS branch
         ├─ qualifying supported ODC safety delta? CURRENTLY NO → ODC HOLD
         ├─ AccessFlow reuse demonstrably removes more ownership than CI?
         │      ├─ YES (internal exception, not established) → one AF contract POC
         │      └─ NO → existing CI + engine contract POC, then Oracle acceptance
         └─ no owners/infrastructure for safe fallback → adoption blocked;
                resolve staffing/approved platform constraint, not more catalogs
```

This tree uses today's negative public results to skip ODC/AccessFlow by default. A future supported delta is a reopening rule, not a request to keep searching. A mandatory client-semantic mismatch changes the engine/native branch before spend or Oracle execution.

## 12. Recommended branch

**Commercial allowed:** take Bytebase EE through the written entitlement/counting and exact-build/control gate, then run one native Oracle/governance/recovery regression. Stop at the first failed hard gate. This is the most credible route to one ordinary user interface and two incident authority domains.

**OSS-only or commercial/native gates fail:** select the existing CI + engine reference and its bounded contract POC. Accept explicitly that five safety responsibilities are an owned software investment. Do not insert AccessFlow unless already-operated reuse makes the total burden demonstrably smaller; do not fund an ODC fork.

**Budget or estate details still unknown:** the recommendation above remains valid as a conditional branch decision. Gather the seven facts below; do not delay on release-volume measurements, full live inventory, all policies or more candidate discovery.

## 13. Exact POC entry conditions

Select **one** branch. This document does not authorize the following runtime work.

| Gate | Concrete entry evidence |
| --- | --- |
| EE commercial/build | Commercial allowed; acceptable self-hosted rights for real endpoint/user/service counts; exact version/image digest/edition/driver; legitimate access. No FREE substitution or paid feature bypass. |
| Supported bounded controls | Identify supported configuration and native SQL/task path for validity/effect veto and actor/stage restrictions. A generic webhook or manual reminder is insufficient. Start with the plausible inline failing PL/SQL path only as a hypothesis. No separate admission/promotion/recovery controller or metadata edits. |
| Estate scope | Sanitized representative W1–W4 scripts and W5 decision; target/alias/PDB/schema/stream map; writer/observer privilege and TCPS requirements. Full enterprise inventory is unnecessary for entry. |
| Owners and evidence | Named platform/DBA/recovery owners; protected secrets; retained artifacts/logs/audit; defined restore reconciliation and recovery authorization. |
| Execution authorization | Separate approval for an isolated lab, real distinct human/service actors and failure instrumentation. No production target. |

The first EE regression is a **fail-fast feasibility POC**, not a 50-instance trial:

| Exact acceptance group | Prove / reject criterion |
| --- | --- |
| Historical negatives first | SQL-11 invalid procedure **and new invalid package body** must not become verified success; REC-08 altered applied content must hard-reject before writes, not warning/skip; MODEL-07/GOV-04 early PROD must reject through UI/API. Regress extra SQL-review ERROR enforcement. Reject native simplicity if any needs a parallel controller. |
| Approval/identity | Real requester/reviewer/PROD approver/executor/service identities; changed bytes/options/targets invalidate authorization; requester/self-approval/console/scheduler bypass negatives; selected last-editor policy explicitly configured. |
| Replay/concurrency | Same release and different request IDs produce one effect; two concurrent starts and target aliases cannot create two writers; engine/platform history agrees with effects. |
| Partial/unknown/recovery | First DDL commits, later statement fails → per-target PARTIAL/HOLD, no new dispatch. Instrument commit-before-result/acknowledgement loss; retain UNKNOWN_OUTCOME and require effect/session/history inspection plus recorded recovery authorization. No automatic replay/repair. |
| Workload correctness | Ordinary DDL/DML and procedure/function/package spec/body/trigger/block invoke correctly; expected transaction behavior; cross-schema diagnostics/effects accessible to restricted observers. |
| Native stages and durability | Same artifact DEV→SIT→UAT→MOCKPROD with verified predecessors and fresh stage authorization; restart/restore retains SQL/audit/logs and cannot replay already committed work. |
| Deletion and UX | Developer/reviewer ordinarily use one platform; DBA sees exact target/result/HOLD. No added CI/engine/guard/state portal for native EE. ≤2 bounded additions and named maintainers. |

Start with one disposable instance and four environment schemas, clearly labeled as one service rather than four instances; use real role identities. A second isolated endpoint can be added for per-target partial behavior after single-target gates pass. Reuse the [original 45-case contract](../poc/ORACLE-POC.md) and [workload manifest](workloads/manifest.json); append new results without editing historical outcomes. Do not count uninstrumented uncertainty as PASS. Only afterward load 50 inventory/20-user fixtures; fixtures are not live scale acceptance.

For **CI**, reuse the existing S6 contract and acceptance gates: approved immutable envelope, actor policy, durable admission/locks/HOLD, verifier/reconciler and retained readable results all have owners before Oracle execution. For the **AccessFlow exception**, add the API-specific negatives in section 5 to that same responsibility boundary. For **ODC**, entry remains closed until section 4's supported delta appears.

## 14. Minimal internal decision dataset

Seven grouped facts; owners can answer from existing records and a small sanitized sample. These are not requests for credentials or a live production scan.

| # / question | Why it changes the decision | Who can answer |
| --- | --- | --- |
| 1. Is commercial software permitted, what budget/contract envelope is acceptable, and is any suitable EE entitlement already held? | Opens or closes the Bytebase branch. Exact new quote remains procurement work, not public research. | Sponsor / team lead / procurement. |
| 2. What representative Oracle versions/RUs/editions and database→RAC/service/PDB/schema/stream/alias map describe the estate? | Determines native compatibility, canonical locks and real registered/contracted count; 50 physical instances is insufficient. | Lead DBA with existing CMDB/application records. |
| 3. Which sanitized mandatory scripts cover W1–W5, substitutions, cross-schema effects and required DML transaction/DDL recovery semantics? | Mandatory client-only behavior can rule out native executors; ordinary corpus supports the preferred regression. | Application release owners + DBA. |
| 4. What independent requester/reviewer/PROD approver/executor policy, IdP and human/service identity counts are mandatory? | Determines approval/API/console acceptance and seat/SSO entitlement; fixture roles do not prove policy. | Security / identity / DBA / release owner. |
| 5. Which Git/CI versions/editions, protected gates, secrets and evidence/backup services already have operational owners? Is AccessFlow already operated? | Reuse selects the lowest marginal OSS burden and approved credential/storage integration; no new tool is assumed. | DevOps / platform / secrets owners. |
| 6. Who owns upgrades, critical custom modules and Oracle HOLD/recovery, with what capacity and required retention/restore obligations? | A no-owner branch is not maintainable; willingness to own five packages versus a bounded verifier changes buy/build feasibility. | Team lead + platform lead + lead DBA. |
| 7. Is a disposable isolated Oracle lab available with approved restricted writer/observer grants, required TLS access and failure-instrumentation permission? | Defines executable POC entry and diagnostic visibility; missing access delays the test, not the public recommendation. | DBA / platform / security approver. |

Change frequency, precise time savings, every production window, full-scale resource budgets and auxiliary tool inventories belong to selected POC/adoption work. They are not prerequisites to this branch decision.

## 15. What is no longer worth researching

- Unchanged ODC failure reruns, version-label surveys or historical image mapping without a qualifying supported safety delta.
- AccessFlow EXECUTED/version projection as Oracle success, or line-count arguments that rename five responsibilities a small runner.
- Bytebase current public edition facts as UNKNOWN; Community/Pro estate workarounds; EE entitlement as a correctness fix; unrelated Oracle feature releases as regression proof.
- Old ODC/CloudDM completion bridges, native AccessFlow's incompatible workload, CloudDM's already-reviewed executor, stale/unlicensed Oracle plugins or unchanged sampled forks.
- Generic catalogs, workbenches, migration CLIs or CI systems as newly discovered integrated platforms. No credible new integrated OSS candidate emerged in the bounded retained-branch research; discovery is not reopened.
- More fallback design, parallel POCs, live-scale benchmarking before ordinary safety passes, or invented prices/effort savings.

The [rejection register](rejection-register.md) retains actual reopening conditions. Selected build support and runtime acceptance are next-phase gates; they are not a renewed broad public-research backlog.

## 16. Final recommendation

**Given the current public evidence, choose the Bytebase EE gated native POC when commercial terms and the mandatory workload permit it; otherwise choose the existing CI + engine contract POC. ODC remains HOLD. AccessFlow remains a reuse-dependent reserve without a demonstrated simplicity advantage.**

Confidence is **HIGH in the branch ordering and public product boundaries; MEDIUM in Bytebase's potential ownership advantage; runtime adoption confidence remains unestablished**. The only facts that can change the next branch are the seven grouped internal inputs, actual commercial rights and exact-build hard-gate results.

Local documentation checks are reported in the completion message. Baseline statuses, historical evidence, expected criteria and source working files remain unchanged.

```text
RECOMMENDED PATH = Bytebase EE commercial/build/control gate, then one native regression; otherwise existing CI + Oracle engine.
WHY = Best documented chance to remove custom governance/state/UI; no integrated OSS winner or smaller AccessFlow runner is demonstrated.

IF OSS-ONLY = Existing CI + one Oracle-capable engine; explicitly own all five safety responsibilities.
IF COMMERCIAL ALLOWED = Bytebase EE only with suitable rights/counting and supported bounded controls; payment does not fix Oracle behavior.

NEXT POC = Conditional Bytebase EE native safety regression; if its entry fails, existing CI contract POC then Oracle acceptance.
ENTRY CONDITIONS = Exact legitimate build; representative corpus/targets; supported control hypothesis; independent actors; named owners; protected evidence/secrets; separate isolated-runtime authorization.

FALLBACK = Existing CI + engine reference; AccessFlow only if actual reuse proves lower total ownership.

NEED FROM INTERNAL TEAM =
1. Commercial allowance/budget/existing entitlement.
2. Sanitized Oracle versions and target/alias/stream map.
3. Mandatory W1–W5 script corpus and transaction/client semantics.
4. Independent actors/IdP and human/service identity counts.
5. Already operated CI/Git/AccessFlow/secrets/evidence/backup services.
6. Named maintenance and Oracle recovery owners/capacity.
7. Isolated lab/access/grants and failure-instrumentation scope.

STOP RESEARCHING = Unchanged ODC, small-runner assumptions, public edition unknowns, rejected bridges/forks, broad catalogs and more CI design.

CONFIDENCE = HIGH for branch decision; MEDIUM for conditional EE ownership benefit; adoption awaits exact-build runtime proof.
```
