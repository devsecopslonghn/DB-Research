# Current Oracle change-management research baseline

Consolidated **7 October 2026**. This is the authority for the research goal, requirements, architecture classes, candidate status and next decision. Dated reports remain authoritative for their observations; their older recommendations are not parallel current backlogs. Consolidation adds no product, runtime result or execution authorization.

## A. Business and operational problem

The user-reported current operating model is:

```text
DBeaver → manually choose database → manually execute SQL
```

The previous improvement attempt was:

```text
Git → Flyway CLI → Oracle
```

Standalone Flyway improved migration execution/history, but estate management remained difficult. Source organization, distributed logs, traceability, credentials, database/schema inventory, release state, target selection, failure/retry/recovery, session/lock investigation, audit, multi-database coordination and human review/approval still need a coherent operating model. Process details beyond manual execution are incompletely documented; these pain categories are research inputs, not measured incident rates or savings. See the [operational account](report.md#lợi-ích-với-dba-trên-một-release) and [original brief](../brief.md).

The desired solution is centralized database change management. A migration CLI alone does not supply it.

## B. Target operating model

```text
Change request → SQL/schema change → review → approval
→ select DB/schema/environment → controlled execution → verification
→ history/audit → failure/recovery

DEV → SIT → UAT → PROD
```

Target selection can be proposed or finalized after initial review, but execution approval must bind exact SQL, options and resolved targets. Changes require renewed approval before dispatch. Promotion requires verified predecessor results and applicable stage authorization; showing environments in a UI is insufficient.

Plan for approximately **50 Oracle instances and 20 users**, subject to inventory and identity discovery:

| Unit | Meaning for the decision |
| --- | --- |
| Instance | Running Oracle instance; RAC can have several instances associated with one database |
| Service | Named routing/connection service; several services or aliases can reach the same database/PDB |
| PDB | Pluggable database in a container database, where applicable |
| Schema | Object namespace owned by an Oracle user; several schemas can share a database/PDB |
| Deployment target | Approved database/PDB, service route, schema and migration stream in an environment, with owner and credential reference |

These are not 1:1. Fifty instances do not mean fifty schemas, license units or targets per release. Locks must account for aliases and cross-schema changes. Start serial; concurrency/live scale are separate decisions. Historical environment labs used four schemas on one Oracle database/service, not four isolated instances.

## Actual goal

> Find the simplest maintainable centralized database change-management solution for Oracle that materially improves DBeaver/manual SQL and standalone Flyway CLI, preferably free/open-source and self-hosted.

Secondary requirements are centralized UI, inventory, review, approval, RBAC, audit, controlled execution, multi-environment rollout, Git/CI/CD compatibility, credential integration, failure visibility and recovery ownership. **CI/CD is an integration requirement, not necessarily the central user interface.** Jenkins is optional; Flyway need not remain if a native executor or another engine meets the requirements more simply.

The [original brief](../brief.md) and [product-model constraint](../product-model-constraint.md) required a free OSS self-hosted platform first. Later composition studies and [reassessment](architecture-reassessment.md#1-executive-conclusion) opened separate composed and commercial branches. A paid option never becomes an OSS match. Self-hosting and safe Oracle execution remain mandatory across branches; commercial purchase acceptance is unresolved.

## Evidence rules and completed tests

| Label | Meaning; never substitute one for another |
| --- | --- |
| DOC | Documentation describes a capability at its recorded date/version |
| SOURCE | Selected code/license inspected at a pin; not whole-image or runtime proof |
| RUNTIME | Observed behavior at the exact product/build/edition/Oracle topology/case recorded |
| DESIGN | Proposed architecture, policy, adapter or state contract; not implemented capability |
| UNKNOWN | Required fact/conclusion is not established |
| NOT_RUN | Relevant execution/test has not been performed |

`PASS`, `PARTIAL`, `FAIL`, `BLOCKED` and `NOT_RUN` are historical **case results**, separate from candidate status. Keep original records/spelling, including older `NOT RUN`. Source incompatibility can stop a POC without turning its runtime NOT_RUN into FAIL.

| Historical run, 4 October 2026 | Exact product/build and edition | Oracle version/topology | Cases and retained results |
| --- | --- | --- | --- |
| ODC API/UI | ODC **4.4.1-20260116**; application edition not separately identified in the result report. OceanBase **CE 4.3.5** was MetaDB, not Oracle target; local TCPS wrapper was part of deployment | Oracle **26ai Enterprise Edition 23.26.4.1.0**; DEV/SIT/UAT/MOCKPROD plus observer schemas on one database/service | Original 45 cases: **12 PASS / 20 PARTIAL / 5 FAIL / 8 NOT_RUN**. [Results](../ODC-ORACLE-POC-RESULTS.md), [case evidence](../evidence/oracle-poc-cases.json) |
| Bytebase API/UI | Bytebase **3.22.1/FREE**, commit `a85f6cb4195299995e8554303550d672d5093e1d`; central PostgreSQL metadata | Same Oracle **26ai Enterprise Edition 23.26.4.1.0** lab; four environment schemas plus observer on one service | Original 45 cases: **17 PASS / 14 PARTIAL / 4 FAIL / 3 BLOCKED / 7 NOT_RUN**. [Results](../BYTEBASE-ORACLE-POC-RESULTS.md), [case evidence](../evidence/bytebase-poc-cases.json) |

- **ODC:** SQL-11 FAIL (success while procedure INVALID); REC-02/08/10 FAIL (replay, changed content and duplicate requests); GOV-03 FAIL (requester executed after approval). Ordinary procedure/function/package/trigger/block cases have PASS evidence. MODEL-07/GOV-04 remain PARTIAL: an external runner ordered tickets; native promotion was not proved. Logs/attachments had restart durability failures.
- **Bytebase FREE:** REC-02 PASS shows normal version replay skip. REC-08 remains FAIL despite WARNING/skip. SQL-11 FAIL hid INVALID; MODEL-07/GOV-04 FAIL describe premature MOCKPROD. Extra P04 SQL Review ERROR enforcement is FAIL **outside** the 45-case totals. Approval/audit cases were BLOCKED by edition. Console and rollout permissions are separate.
- Earlier Bytebase P03/P04 records stay in the [original contract](../poc/ORACLE-POC.md) and [comparison](../BYTEBASE-ODC-COMPARISON.md). Do not fill missing old build/edition/topology values from the later 3.22.1 run.
- SQL-01/02 PARTIAL includes successful SQL with incomplete migration-state acceptance. MODEL-12 PASS means gaps were identified, not implemented. Operational restarts are not controlled recovery PASS evidence.

The [45-case Oracle contract](../poc/ORACLE-POC.md), [criteria](criteria.csv), [14 workload hashes](workloads/manifest.json) and [engine evidence](../EVIDENCE.md) remain intact. AccessFlow, Archery and CloudDM have no new Oracle RUNTIME acceptance; Bytebase EE and proposed compositions are NOT_RUN. There are no [benchmark samples](benchmarks/README.md) or verified 50-instance/20-user load results. Oracle 19c/21c, RAC and the real estate are not certified by the 26ai lab.

A central immutable applied-state ledger can be a future design if admission, durability and Oracle reconciliation are proved. That refinement does not rescore historical target-ledger cases or rewrite expected results; alternative future acceptance mapping must be explicit before its POC. Oracle DDL can commit before success recording regardless of ledger location.

## Exactly three architecture classes

| Class | Shape | Existing examples and boundary |
| --- | --- | --- |
| **A — Integrated database platform** | Users → database platform owning inventory, review, approval, execution, rollout, audit and recovery state → Oracle | Bytebase, ODC native, Archery, CloudDM native, SQLE/DMS, AccessFlow native. Product shape does not establish completeness/acceptance |
| **B — Database governance platform + execution engine** | Users → governance platform → **supported handoff** → restricted migration engine → Oracle | AccessFlow deployment-gate API + engine. A bridge requiring task-engine/scheduler/native-status or direct metadata surgery is excluded |
| **C — CI/CD composition** | Git → CI/orchestration → migration engine → Oracle, with owned inventory, authorization, results and recovery | Jenkins/Flyway, entitled GitLab CI/Flyway, AWX/engine, Rundeck/engine. Fallback class; host/node inventory needs DB/schema mapping |

Historical product `Category A/B/C` and validation `POC A/B` names are not these classes. Validation POC B (Git/Jenkins/Flyway) maps to **Architecture C**; Archery's old governance Category B maps to native **Architecture A**. Rejected ODC/CloudDM bridges remain history, not eligible B options.

## Canonical hard requirements

| Priority / ID | Requirement and acceptance boundary |
| --- | --- |
| MUST M1 | Actual Oracle estate versions/topologies; required DDL/DML/PLSQL parse and execute correctly, including package body and diagnostics |
| MUST M2 | Self-hosting possible for normal operation; selected edition/artifact/plugins/drivers/dependencies usable at actual counts. OSS branch must remain usable free OSS |
| MUST M3 | Central UI/inventory with stable target ID, environment, schema, owner, stream and credential reference; targets visible before execution |
| MUST M4 | No plaintext Oracle passwords in Git or published logs/evidence; restricted deploy/observer principals, protected secret access and accountable rotation |
| MUST M5 | Traceable requester, human reviewer/approver, initiating service/human and executor; approval bound to exact artifact/options/targets; independent actors enforced across UI/API/scheduler/console |
| MUST M6 | One executor per managed stream; durable duplicate/replay prevention, canonical schema serialization and pre-write rejection of altered applied content |
| MUST M7 | Per-target result/failure state; no misleading SUCCESS on INVALID, partial or unknown outcome; verification vetoes promotion |
| MUST M8 | Enforced DEV→SIT→UAT→PROD boundaries; stop new dispatch on failure/uncertainty and retain already-started outcomes |
| MUST M9 | Durable central history/audit linking actor, SQL/hash, target, trigger, time, result and recovery; retained through restart/restore |
| MUST M10 | Named recovery owner and held state after uncertain commit/session loss; inspect effects/history/session before approved recovery; cancel/retry/repair does not imply rollback |
| SHOULD S1 | Native Git integration, convenient release promotion and configurable approval routing/quorum beyond the mandatory bound-approval policy |
| SHOULD S2 | SSO, API/CI integration, useful dashboard, notifications and existing secret-manager integration; protected basic credentials remain M4 |
| SHOULD S3 | Supported onboarding/export/restore procedures with small component/upgrade burden |
| NICE TO HAVE N1 | Schema diff, drift, lineage, SQL AI review, MCP, Terraform provider; none compensates for a MUST failure |

## Operational pain → desired capability → responsible solution

Capability references below do **not** mean a complete candidate passes. EE DOC describes an edition; DESIGN identifies owned work still required.

| Current pain | Desired capability | Candidate/component addressing it |
| --- | --- | --- |
| Disorganized SQL/source | Retained reviewed artifact and release ID | Bytebase release historical RUNTIME; optional Git for A; Git bundle for B/C DESIGN |
| Manual DB selection | Inventory + approved target selector | ODC inventory historical RUNTIME; Bytebase EE DOC; AccessFlow datasource SOURCE; C registry/view DESIGN |
| Unclear service/PDB/schema inventory | Stable physical/logical target mapping | Platform inventory plus DBA mapping; B/C frozen export/registry DESIGN |
| Credential files/sharing | Restricted centralized credential references | Selected platform provider or runner store; actual provider/rotation UNKNOWN |
| Logs scattered | Central retained execution history | ODC/Bytebase historical task history with retention gaps; B/C attempt records DESIGN |
| Release state assembled manually | Release × environment × target results | Bytebase revision/rollout historical RUNTIME; ODC batch DOC/SOURCE; B/C matrix DESIGN |
| Weak traceability/audit | Query who/what/where/when/how/result | Platform request/actor records; EE audit DOC; B/C correlated exports DESIGN |
| Manual review/PROD approval | Independent bound workflow approval | ODC human approval RUNTIME with requester gap; EE approval DOC; AccessFlow API SOURCE; C gates DESIGN |
| Multi-DB coordination | Ordered waves, stage authorization, stop policy | ODC batch DOC/SOURCE; EE rollout DOC; B/C dispatch DESIGN; verified enforcement open |
| Flyway failure/retry investigation | Target state + recovery workflow | Native recovery must be proved; B/C durable admission/verifier/reconciler DESIGN; DBA recovery owner |
| Session/lock investigation | Attempt/session/principal/lock correlation | DBA observer/runbook plus platform/runner evidence; exact grants and safe inspection UNKNOWN |
| Unknown execution outcome | Per-target verified release result | Oracle validity/effect/history verification feeding an enforced gate for every architecture |

This mapping keeps research tied to user value. No time savings or annual maintenance cost has been measured.

## Architectural principles

1. Prefer one authoritative workflow over loosely synchronized tools. Each state has one owner; projections are not independently editable.
2. Do not build a database platform in Jenkins unless integrated options fail license, correctness or maintainability gates.
3. A migration engine is not a governance platform; history is execution evidence, not the whole approval/audit workflow.
4. A nice UI does not compensate for unsafe execution/recovery.
5. Judge native execution by total operating model, not whether it behaves exactly like Flyway.
6. Avoid two executors for the same migration stream; every ordinary managed write path must obey authorization/admission.
7. Every SUCCESS must be distinguishable from `PARTIAL`, `INVALID`, `UNKNOWN_OUTCOME`, `FAILED`. Product task status, engine history and verified Oracle effects are separate facts.
8. Custom correctness/recovery code costs significantly more to own than presentation/reporting. Count concurrency, restore, upgrades and incident responsibility even for short scripts.

## Tool roles

| Role | Existing tools and limits |
| --- | --- |
| Full / near-full platforms | Bytebase, ODC, CloudDM, NineData; DBmaestro and OEM change plans are commercial comparators; shape is not acceptance |
| Governance platforms | AccessFlow, Archery, SQLE/DMS; native execution belongs to A, supported AccessFlow external API can participate in B |
| Migration engines / authoring toolchains | Flyway, Liquibase, Sqitch, Atlas, Oracle SQLcl Project, dbpm; SQLcl/dbpm emphasize artifacts/packages. Atlas Oracle is paid; Liquibase 4.33 Apache and 5.x FSL differ |
| CI/orchestration | Jenkins, GitLab CI, AWX/Ansible, Rundeck, Octopus; Harness Database DevOps is a commercial DB-aware pipeline/module comparator |
| Workbenches | DBeaver, CloudBeaver, DbGate; connections/query access do not supply immutable release/recovery |
| Supporting components | Git, existing identity/secrets/evidence storage, Oracle clients/drivers, verifier/reporting; DBHub query/MCP and Flyway UI/Play wrappers are components |

[Catalog profiles](tool-feature-catalog.md) and [engine evidence](../EVIDENCE.md) retain the details. “Flyway vs Bytebase” requires explaining engine versus platform responsibility. Components are not additional final candidates.

## Canonical candidate status

This is the **only current status table**. `ACTIVE` = eligible for next bounded work after stated entry conditions; `HOLD` = material prerequisite unresolved; `RESERVE` = retained alternative, no scheduled work; `STOP` = reviewed proposal rejected/deprioritized until its reopening condition; `COMMERCIAL_CHECK` = rights/counting/quote/build decision before technical POC; `FALLBACK` = reference if preferred branches fail. None authorizes runtime.

| Candidate | Architecture | Current status | Main blocker | Reopen / advance condition |
| --- | --- | --- | --- | --- |
| ODC native | A | HOLD | Historical INVALID/replay/checksum/dedup/requester failures; admission/recovery closure unestablished | Supported bounded safety delta, mapped build and enforceable verified continuation; focused regression afterward |
| AccessFlow deployment API + restricted engine | B | RESERVE | Generic gate not Oracle uniqueness/per-target recovery/verified promotion; five owned modules | No integrated option qualifies; bounded contract/ownership comparison justifies extra UI/services over C |
| Bytebase EE self-host | A | COMMERCIAL_CHECK | No suitable actual quote/entitlement/counting or licensed-build regression | Resolve commercial/build gate; separately authorize native regression, not FREE substitution |
| Git/Jenkins/Flyway S6; entitled GitLab CI substitution | C | FALLBACK | Five owned inventory/actor/admission/verifier/reporting packages; stack NOT_RUN | Integrated paths fail, existing CI/entitlement and ownership confirmed; pass contract then Oracle gates |
| Archery native SQL-ticket portal | A | RESERVE | Full release/promotion/admission/recovery absent; transaction/parser/package-body NOT_RUN | Owner confirms narrower ticket use case or supported bounded release-control delta |
| AccessFlow native schema changes | A | STOP | Reviewed gate rejects required DML/ordinary PL/SQL | Supported workload-compatible native delta plus safety gates; do not remove required SQL |
| CloudDM v4.3.0 native release executor | A | STOP | Ticket compile default off; target release admission/locking/recovery unestablished | Supported validity and native state/recovery delta; renewed caps research is insufficient |
| ODC + external engine, old S2 | B, rejected proposal | STOP | Gate A unclosed; native external-completion/replacement contract unestablished | Six Gate A proofs with accepted link-only lifecycle/value, or supported completion contract; no deep fork |
| CloudDM + external engine, old S3 | B, rejected proposal | STOP | Inbound HttpCall/native-finish callback not approved engine handoff | Supported versioned post-approval authorization/result contract and native-write suppression |
| Bytebase Community/FREE or Pro/TEAM estate proposal | A | STOP | Recorded 10-instance cap and governance gates; FREE correctness failures | Suitable new free entitlement/features plus safety delta; Pro not assumed to supply EE approval/capacity |
| SQLE/DMS Community Oracle | A | STOP | Recorded Oracle edition boundary; plugin rights/current artifact mapping unresolved | Usable OSS Oracle package/license/compatibility and release-safety evidence |
| SQLE/DMS licensed Oracle bundle | A | HOLD | Exact Oracle SKU ambiguity, package rights/support and recovery unknown | Suitable entitlement and supported mapping justify bounded commercial comparison |
| NineData Community for estate | A | STOP | Recorded 10-datasource cap; OSS implementation not established | Suitable free OSS distribution/capacity, not Enterprise label |
| NineData EE, DBmaestro, OEM with Lifecycle Pack | A | RESERVE | No selected entitlement/quote or exact Oracle safety proof; OEM footprint | Existing entitlement or specific commercial hypothesis materially changes comparison |
| AWX/engine or Rundeck/engine | C | RESERVE | No simplicity gain shown; DB mapping/safety owned; release/CE approval constraints | Already operated platform and bound approval/target controls reduce total burden |
| Octopus/engine or Harness DB DevOps | C | RESERVE | Commercial/hosting constraints; exact Oracle recovery NOT_RUN | Existing suitable entitlement/self-host model with concrete advantage |

The [rejection register](rejection-register.md) preserves dates, pins and original verdict vocabulary. NO-GO/RED map to STOP for a reviewed blocker; YELLOW/conditional are not eligibility (S2 STOP because Gate A remains open). Older pause becomes RESERVE for Archery but STOP for incompatible AccessFlow native. Bytebase EE's old HOLD becomes COMMERCIAL_CHECK. Source STOP never changes a NOT_RUN case to FAIL.

## Preferred architecture and four retained decision options

**Prefer A: one integrated platform, native executor and bounded enforced verification/recovery. No qualifying integrated OSS adoption winner is demonstrated.** This follows operating-model evidence and critical custom-code burden, not file age or score alone.

| Decision role | Retained option | Reason and evidence boundary |
| --- | --- | --- |
| Best conditional integrated OSS candidate | ODC native | Strongest relevant OSS inventory/approval/PLSQL historical evidence; known safety gaps keep HOLD |
| Best composed OSS reserve | AccessFlow deployment API + engine | Supported submit/gate/confirm/outcome avoids internal task replacement; not a shipped Oracle/Flyway adapter or proved simpler stack |
| Best commercial integrated comparison | Bytebase EE | Documented chance to remove owned governance/dispatch/UI; actual rights/budget/licensed Oracle regression unresolved |
| Fallback CI composition | Git/Jenkins/Flyway reference | Supported CLI/CI interfaces and explicit ownership; another existing CI may substitute with equivalent controls |

ODC safety closure is provisionally five functional packages; AccessFlow composition and S6 also need five. Bytebase EE is estimated at one bounded Oracle verification package, possibly a second export package **if native admission/recovery passes**. These are DESIGN estimates, not implementations or measured effort. Count sources, authorities, storage and upgrade obligations; see [custom-code](architecture-reassessment.md#12-custom-code-comparison) and [operations](architecture-reassessment.md#13-operational-simplicity-comparison).

AccessFlow's API `EXECUTED` means confirmation accepted, not completed Oracle SQL. Outcome fields do not supply per-target PARTIAL/UNKNOWN truth. The restricted runner still owns binding, admission, verification/promotion and recovery evidence. This supported API earns RESERVE; old ODC/CloudDM bridges do not become eligible B options.

## One canonical decision model

Hard gates first: **actual Oracle workload correctness; usable self-hosted rights/capacity; immutable artifact/target/actor authorization; single-writer duplicate/concurrency control; truthful validity/partial/unknown reporting and promotion; durable audit/restore and owned recovery; supported bounded maintenance.** FAIL rejects adoption; missing proof holds it. Scores override neither.

Use the reassessment's existing 100-weight model for qualified comparisons. Execution and self-hosting are explicit included dimensions/gates, not extra points:

| Dimension | Weight / treatment | Evidence needed |
| --- | --- | --- |
| Oracle correctness | 18, includes execution | Required parser/PLSQL validity/effects at actual version/driver/topology |
| License / 50-target viability | 15 plus gate | Real instance/service/PDB/schema/human/service-account counting and artifact rights |
| Central inventory | 8 | Stable owner/env/schema IDs and safe selection |
| Review / approval | 10 | Independent authenticated actors and bound authorization |
| Execution | Gate; included in Oracle 18 | Sole executor, release admission, serialization, accurate results |
| Multi-environment rollout | 8 | Immutable artifact, verified predecessors, stage authorization |
| Audit / traceability | 8 | Durable centrally retrievable actor/artifact/target/attempt chain |
| Failure / recovery | 10 | Partial/unknown HOLD, session/effect reconciliation and approved recovery |
| Operational simplicity | 10 | Interfaces/components/authorities, backup/upgrade/on-call |
| Custom correctness code | 8 | Owned critical packages, supported boundaries and maintainers |
| Self-hosting | Gate; license/operations impact above | Supported normal operation on own infrastructure |
| API / Git integration | 3 | Supported interfaces, exact artifact/service identity |
| UI usability | 2 | Representative selection/review/result workflow; fixtures are not load |

Score 0–5; weighted total = `sum(weight × score / 5)`. Higher simplicity/custom-code score means less owned burden. [Dated scores/rationale](architecture-reassessment.md#14-revised-decision-matrix) remain judgment, not acceptance/performance. Do not mix them with older weights or create new scores in consolidation. NICE TO HAVE features receive no primary weight.

## Funnel and current phase

```text
Market/catalog → capability fit → license fit → Oracle fit
→ architecture simplicity → shortlist → POC → adoption decision
```

Current phase: **shortlist/POC-entry decision after architecture reassessment**. Historical POCs inform Oracle fit; license/recovery gates remain open. No adoption, new eligible runtime POC, benchmark phase or implementation backlog is authorized here.

Next establish whether self-hosted Bytebase EE is commercially acceptable and available for the real estate: actual counting, budget/existing entitlement and exact licensed-build facts through responsible owners. [Open questions](open-questions.md) specifies how. This consolidation does not contact vendors or start trials.

If that gate passes, select a separately authorized **Bytebase EE native Oracle regression**: original SQL/INVALID/package body, strict checksum/replay/dedup, real actor/console/API/SQL-review enforcement, early-PROD negatives, audit and instrumented partial/unknown recovery. Payment is not a correctness fix. See [C0–C4](architecture-reassessment.md#16-recommended-next-poc).

If commercial is ruled out, record it. Reopen ODC only for a supported bounded safety delta; absent one, record “no integrated OSS solution demonstrated.” Then compare AccessFlow API/engine ownership with existing CI fallback and choose one bounded probe. Do not resume all old plans.

## Decision timeline and reconciliation

| Phase / date | Change and reason for priority |
| --- | --- |
| Initial research, 3 October | CLI pain led to platform-first [report](../REPORT.md)/[product model](../PRODUCT-MODEL.md): ODC/AccessFlow workflows first, engines/workbenches as components |
| Runtime/T00–T04, 4 October | [ODC](../ODC-ORACLE-POC-RESULTS.md)/[Bytebase FREE](../BYTEBASE-ORACLE-POC-RESULTS.md) showed useful Oracle/UI behavior and concrete failures; [frozen shortlist](history/t00-t04/shortlist.md) retained four conditional tools, without treating untested tools as better |
| Deep source/license, 4–6 October | [Source trace](research-round-2/coordinator/oracle-governance-source.md) found incompatible AccessFlow gate and Archery body risk; [ODC survey](research-round-2/coordinator/odc-source-survey-20261006.md) found creator execution/scoped state gaps; image mapping unresolved |
| CloudDM artifact decision, 7 October | [v4.3.0 review](research-round-2/coordinator/clouddm-v430-artifact-review-20261007.md) resolved selected license/cap paths but found compile/state/recovery gaps; native STOP is safety-based, not stale cap |
| Catalog/composition, 7 October | [Catalog](tool-feature-catalog.md), [solutions](solution-shortlist.md), [architectures](reference-architecture.md), [POC plan](poc-plan.md) compared native/engine/CI; S2/S3 handoff was a hypothesis |
| Validation/gates, 7 October | [Validation](poc-design-validation.md) separated MANUAL wait from external completion; [gates](decision-gates.md) stopped S2/S3 and favored bounded S6. GREEN meant design/interface feasibility, not runtime acceptance |
| Reassessment, 7 October | [Reassessment](architecture-reassessment.md) counted S6's five critical modules, removed Jenkins/Flyway assumptions and preferred integrated simplicity; ODC HOLD, supported AccessFlow API reserve, conditional EE next, S6 fallback |
| Consolidation, 7 October | One goal/model/status table replaces competing next-step summaries. Runtime/source/license history unchanged; no winner or newly passed gate inferred |

Chronology explains proposals, not truth by itself. Current priority follows runtime failures, scoped source/artifact findings and ownership comparison. A new report cannot erase an old failure; an old native rejection need not exclude a distinct supported API/licensed branch.

## Do not repeat without new evidence

- Unchanged historical POCs or operational restarts as recovery proof. New runs need exact build/edition/configuration deltas and separate records.
- Disproven source assumptions: ODC MANUAL cannot wait; approval integration replaces an executor; AccessFlow native accepts required DML/ordinary PL/SQL; internal Flyway manages customer Oracle state.
- Obsolete license claims: cached CloudDM 10/5 is not its reviewed-path blocker; Liquibase 4.33 Apache does not license 5.x FSL; public dbpm Core Apache evidence resolved the old source-license unknown. These do not prove artifact/runtime readiness.
- Rejected executor bridges, direct status/metadata writes and deep task-engine/product forks. Engine substitution does not close handoff gaps.
- Workbenches/wrappers presented as full platforms, unchanged unlicensed Oracle plugins, sampled Bytebase forks as license bypasses.
- Broad discovery with no new hypothesis. Consult the [rejection register](rejection-register.md); keep catalog reserves outside the active four-option comparison unless their condition changes.

## Maintaining the baseline

[Open questions](open-questions.md) groups estate, identity, infrastructure, process, commercial and technical uncertainty. Highest-impact inputs: actual Oracle/service/PDB/schema/stream counts and mandatory scripts; EE budget/entitlement/build; independent approval/SSO; existing operated components; recovery/maintenance owners. Do not infer these from the lab.

Read this baseline first. Change its status/requirements only with cited new evidence or explicit owner decision. Append separately dated run evidence; never edit historical verdicts/expected outcomes/workloads/pins/frozen history. Keep rejection/unknown registers linked to this authority. [Evaluation index](README.md) locates supporting material; old plans do not grant implementation permission.

```text
CURRENT GOAL = Choose the simplest maintainable self-hosted Oracle change-management workflow improving manual DBeaver and standalone Flyway CLI, preferably free OSS.
CURRENT PHASE = Shortlist/POC-entry decision after architecture reassessment; no adoption or new runtime POC eligible.
ACTIVE CANDIDATES = None in ACTIVE status; four retained options are ODC native, AccessFlow API + engine, Bytebase EE and CI/Flyway fallback.
HOLD = ODC native until supported bounded safety delta; SQLE/DMS licensed Oracle until exact rights/package; Bytebase EE is COMMERCIAL_CHECK pending estate, budget/entitlement and build.
STOP = AccessFlow native full workload, CloudDM v4.3.0 native, old ODC/CloudDM engine bridges, Bytebase FREE/Pro estate proposal, SQLE/DMS CE Oracle and NineData CE; component exclusions in rejection-register.md.
FALLBACK = Git/Jenkins/Flyway S6 with five owned safety/operational packages; substitute existing entitled CI only with equivalent proven controls.
TOP UNKNOWNS = Real Oracle versions/topology/target counts and mandatory scripts; EE budget/entitlement/build; approval/SSO; existing CI/secrets/storage; maintenance/recovery owners.
NEXT RESEARCH QUESTION = Is suitable self-hosted Bytebase EE commercially acceptable and available for the actual target/user model, with an exact licensed build for regression?
NEXT POC DECISION = Select Bytebase EE native Oracle regression after commercial/build gate; otherwise choose one bounded OSS probe under ODC delta or AccessFlow-versus-CI ownership gates.
```
