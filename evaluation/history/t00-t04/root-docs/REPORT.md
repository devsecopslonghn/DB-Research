# Open-source Oracle database change platform research

## Cập nhật T00–T04, 04/10/2026

[Kết luận mở rộng](evaluation/report.md) và [shortlist mới](evaluation/shortlist.md) bổ sung CloudDM và phạm vi governance của Archery.
ODC/AccessFlow vẫn là POC platform có điều kiện. Bytebase là đối chứng riêng có edition gates.
Các bảng phía dưới giữ phạm vi source/POC trước lượt T00–T04.
Chúng không xếp hạng hiệu năng hoặc xác nhận ứng viên mới đạt runtime.
[Register](evaluation/candidates.csv) ghi rõ phần được tái kiểm và phần kế thừa hồ sơ cũ.

Runtime update, 2026-10-04: ODC completed Oracle API/UI SQL and permission POC through a local TCPS wrapper.
See [connection POC](ODC-CONNECTION-POC.md). The 45 original criteria now have per-case results. See [API/UI results](ODC-ORACLE-POC-RESULTS.md).; earlier inspection statements retain their dated scope.

Research date: 2026-10-03.
The supplied [brief](brief.md) defines execution requirements.
The [product-model constraint](product-model-constraint.md) defines the primary search and shortlist rules.

## 1. Executive summary

**OceanBase ODC is an existing free, self-hosted Oracle platform with open-source software (OSS) and substantial Bytebase-like structure.**
ODC has projects, registered datasources, database records, environments, approvals, and ordered database deployment batches.
These capabilities exist in inspected backend and frontend source.
Its immutable release model and reliable target migration state remain incomplete or unverified.
It is a platform evaluation candidate. It is not a verified replacement for every Bytebase capability.
[P-ODC-PROJECT, P-ODC-QUEUE, P-ODC-BATCH-EXEC, P-ODC-ORACLE-UI](PRODUCT-EVIDENCE.md#source-references)

The [new product constraint](product-model-constraint.md) controls shortlist selection.
It permits a strong platform to remain despite missing target migration state.
The original [brief](brief.md) still defines execution and recovery requirements.
The review therefore separates Platform Fit from Migration Engine Fit.

| Existing platform shortlist | Category | Platform Fit | Migration Engine Fit | Material limits |
|---|---|---|---|---|
| OceanBase ODC | A | HIGH | LOW | Ticket-based SQL and ordered batches. Immutable version releases and target applied detection not established. Public source snapshot is from 2025. ODC 4.4.1 is deployed. Oracle POC has results; invalid compilation and request dedup failed. |
| AccessFlow | A | MEDIUM | LOW | Existing schema change sets and environment promotion. Project/estate model is partial. Oracle script gate and target state gaps remain. |

Missing target state no longer makes this platform shortlist empty.
No inspected candidate satisfies every original execution, recovery, scale, and license requirement without additional verification or work.
The [product comparison](PRODUCT-MODEL.md) gives ten complete 18-capability comparisons and classifies every reviewed candidate.
The [frontend record](UI-EVIDENCE.md) provides actual routes, navigation, ten page checks per shortlisted platform, and official screenshots.

Archery and SQLE Community are Category B SQL governance systems.
Their SQL workflow controls do not establish a free immutable release promotion model.
Flyway, Liquibase, Sqitch, migration wrappers, and file migration UIs are Category C.
They remain secondary execution components.

Bytebase is the full product reference.
Community remains limited to 10 instances and 20 users.
Configurable approval workflows, audit, enterprise identity, and external secrets have paid boundaries.
Rollout execution permissions differ from configurable approval workflows.
The inspected Oracle runner records revisions centrally.
The root license restricts enterprise directories and excludes enablement code from its MIT grant.
[P-BB-LICENSE](PRODUCT-EVIDENCE.md#source-references), [BB-PLAN, BB-GATES, BB-STATE](EVIDENCE.md#source-references)

The historical and fork search inspected seven Bytebase repositories.
Recent and renamed samples retain upstream commits. Historical divergence did not establish a new unrestricted Oracle product.
Exact fork creation commits remain UNKNOWN.
The [fork record](FORK-SEARCH.md) records licenses, commit relationships, source limits, and the Gitee access limitation.

The existing platform evaluation must precede engine composition.
Evaluate ODC's project estate and multi-environment batch workflow first.
Evaluate AccessFlow's existing schema change-set promotion second.
Consider a Flyway composition only if those workflows fail the accepted platform or recovery requirements.

Current Liquibase Community uses FSL-1.1-ALv2. Liquibase 4.33.0 source retains Apache-2.0.
SchemaPilot has a restricted custom license. DRM has unresolved complete payload license coverage.
The [license audit](LICENSE-AUDIT.md) preserves these distinctions.

ODC is deployed at [oceanbase.apps.drgdevlab.com](https://oceanbase.apps.drgdevlab.com).
Version, volume sizes, Oracle driver presence, administrator login, and selected authenticated GET routes were inspected.
The [ODC evaluation](ODC-EVALUATION.md) records architecture, Oracle onboarding, inherited permissions, API integration, language, and licensing.
No application tests or Oracle proof of concept ran during the initial source review. Later runtime results have separate dated sections.
The 45 original criteria now have per-case results. See [API/UI results](ODC-ORACLE-POC-RESULTS.md).

### Decision boundary

A migration ledger is necessary for this request. A ledger alone does not guarantee exactly-once DDL execution.
Oracle commits around DDL statements. A process can fail after DDL commits but before a history insert completes.
Flyway, Liquibase, and Sqitch each execute before recording final success in their inspected paths.
Recovery must detect uncertain results and stop automatic replay. [FW-EXEC, LB4-EXEC, SQ-EXEC](EVIDENCE.md#source-references)
Oracle documents the [DDL commit behavior](https://docs.oracle.com/en/database/oracle/oracle-database/19/tdddg/committing-transactions.html).

## 2. Product selection and execution matrices

`YES` means the inspected source or official documentation establishes the capability.
It does not mean that this research tested the capability.
`PARTIAL` means limited scope, a paid boundary, or required integration work.
`NO` means an identified gap. `UNKNOWN` means insufficient evidence.

The matrices describe the free edition, unless a row explicitly identifies another edition.
These execution matrices do not replace the product shortlist criteria.
Category and independent fit scores are in [PRODUCT-MODEL.md](PRODUCT-MODEL.md).
“Audit” means central accountability beyond a target ledger or temporary command output.
“GitLab” and “Jenkins” distinguish native integration from generic command invocation.
Maturity is a judgment supported by [the separate maturity register](MATURITY.md).
The [feature matrix](FEATURE-MATRIX.md) evaluates each desired and optional feature.
The [Oracle coverage table](ORACLE-COMPATIBILITY.md) separates procedural constructs and execution mechanisms.

### Original requirement matrix

| Platform | OSS License | Fully Free? | Self-hosted | Oracle | Target Ledger | Central Server | Web UI | History | Audit | RBAC | Approval | GitLab | Jenkins | Maturity |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Bytebase Community | MIT subset / restricted enterprise and enablement | PARTIAL | YES | YES | NO | YES | YES | YES | NO | YES | NO | PARTIAL | PARTIAL | Established |
| OceanBase ODC | Apache-2.0 backend and frontend | YES | YES | YES | NO | YES | YES | YES | YES | YES | YES | PARTIAL | PARTIAL | Established. Deployed 4.4.1. Public snapshot older |
| SQLE + DMS Community | MPL-2.0 core. Oracle plugin coverage UNKNOWN | PARTIAL | YES | PARTIAL | UNKNOWN | YES | YES | YES | PARTIAL | YES | YES | UNKNOWN | PARTIAL | Active SQL governance |
| AccessFlow | Apache-2.0 | YES | YES | PARTIAL | NO | YES | YES | YES | YES | YES | YES | YES | PARTIAL | Young, active |
| D-Band DRM | ISC declaration, coverage UNKNOWN | PARTIAL | YES | YES | PARTIAL | NO | NO | PARTIAL | NO | NO | NO | PARTIAL | PARTIAL | Small CLI |
| Open Migration | MIT | YES | YES | NO | PARTIAL | PARTIAL | YES | PARTIAL | NO | NO | NO | YES | PARTIAL | Small prototype |
| SchemaPilot | Custom restricted license | NO | YES | NO | PARTIAL | PARTIAL | YES | PARTIAL | NO | NO | NO | UNKNOWN | UNKNOWN | Small prototype |
| Flyway UI (`binout`) | Apache-2.0 | YES | YES | UNKNOWN | PARTIAL | NO | YES | PARTIAL | NO | NO | NO | PARTIAL | PARTIAL | Stale component |
| Flyway Play | Apache-2.0 | YES | YES | PARTIAL | YES | NO | PARTIAL | PARTIAL | NO | NO | NO | PARTIAL | PARTIAL | Application module |
| Liquibase Community 5.x | FSL, future Apache-2.0 | NO | YES | YES | YES | NO | NO | PARTIAL | NO | NO | NO | PARTIAL | PARTIAL | Established engine |
| Liquibase 4.33.0 source | Apache-2.0 | YES | YES | YES | YES | NO | NO | PARTIAL | NO | NO | NO | PARTIAL | PARTIAL | Older OSS engine |
| Flyway Community source | Apache-2.0 | YES | YES | YES | YES | NO | NO | PARTIAL | NO | NO | NO | PARTIAL | PARTIAL | Established engine |
| Sqitch | MIT | YES | YES | YES | YES | NO | NO | PARTIAL | NO | NO | NO | PARTIAL | PARTIAL | Established engine |
| Atlas public OSS | Apache-2.0 | PARTIAL | YES | NO | YES | NO | NO | PARTIAL | NO | NO | NO | PARTIAL | PARTIAL | Active engine |
| Yearning | AGPL-3.0 | YES | YES | NO | NO | YES | YES | YES | YES | YES | YES | UNKNOWN | UNKNOWN | Established, MySQL |
| Archery | Apache-2.0 | YES | YES | YES | NO | YES | YES | YES | YES | YES | YES | UNKNOWN | PARTIAL | Established SQL workflow |
| Tareya Archery derivative | Apache-2.0 | YES | YES | YES | NO | YES | YES | YES | PARTIAL | YES | YES | UNKNOWN | PARTIAL | Fork, support UNKNOWN |
| .NET dbdeploy (`gigi81`) | MIT | YES | YES | YES | YES | NO | NO | PARTIAL | NO | NO | NO | PARTIAL | PARTIAL | Engine, support UNKNOWN |
| DbMaintain | Apache-2.0 | YES | YES | YES | YES | NO | NO | PARTIAL | NO | NO | NO | PARTIAL | PARTIAL | Deprecated |
| dbpm | Apache-2.0 CLI, Core coverage UNKNOWN | PARTIAL | YES | YES | PARTIAL | NO | NO | PARTIAL | NO | NO | NO | PARTIAL | PARTIAL | Young Oracle tool |
| dbward core | Apache-2.0 / commercial extensions | PARTIAL | YES | NO | PARTIAL | YES | UNKNOWN | YES | YES | PARTIAL | YES | UNKNOWN | UNKNOWN | Young, open-core |
| CloudBeaver Community | Apache-2.0 / commercial editions | YES | YES | YES | NO | YES | YES | PARTIAL | UNKNOWN | PARTIAL | NO | UNKNOWN | UNKNOWN | Established SQL editor |

Atlas has target revision tracking for its supported engines.
Its Oracle driver requires Pro. That Oracle functionality is not established by the public Apache source.
The [official compatibility page](https://atlasgo.io/features) identifies this boundary. [AT-L, AT-DRIVERS](EVIDENCE.md#source-references)

History in a CLI row means target history or local records.
It does not satisfy the central history requirement.
`PARTIAL` CI integration often means that a pipeline can invoke the CLI.
It does not establish approval, promotion, or central inventory.

Source references by candidate:

| Candidate | Evidence IDs |
|---|---|
| Bytebase | BB-L, BB-ENT, BB-PLAN, BB-GATES, BB-STATE, BB-ORA, BB-DRIVER |
| OceanBase ODC | P-ODC-LICENSE, P-ODC-PROJECT, P-ODC-ORACLE, P-ODC-GIT-API, P-ODC-DATASOURCE-API, P-ODC-FLOW-API, P-ODC-ROLE-INHERITANCE. Live evidence: ODC-EVALUATION.md |
| AccessFlow | AF-L, AF-PROM, AF-GATE, AF-SCAN, AF-GROUP, AF-JDBC, AF-ORA, AF-SSO, AF-VAULT, AF-DR, AF-CI |
| DRM | DRM-L, DRM-LOCAL, DRM-FW, DRM-LB, DRM-SQLPLUS, DRM-EXEC, DRM-RETRY |
| Open Migration | OM-L, OM-ENG, OM-STATE, OM-RUN, OM-META, OM-AUTH |
| SchemaPilot | SP-L, SP-EXEC, SP-DRIVERS |
| Flyway UI / Play | UI-L, UI-DEPS, UI-SERVLET, PLAY-L, PLAY-SCOPE, PLAY-DEPS |
| Migration engines | FW-L, FW-ORA, FW-PARSER, FW-EXEC, FW-FAIL, LB4-L, LB5-L, LB4-STATE, LB4-EXEC, SQ-L, SQ-STATE, SQ-EVENTS, SQ-EXEC |
| Yearning / Archery / derivative | YE-L, YE-SCOPE, AR-L, AR-ORA, AR-EXEC, AR-PARSER, AR-STATE, AR-SQLPLUS, FORK-L, FORK-EXEC |
| Additional candidates | DEP-L, DEP-ORA, MAINT-L, MAINT-SCOPE, PM-L, PM-SCOPE, PM-LIMITS, WARD-L, WARD-SCOPE, WARD-BOUNDARY, CB-L, CB-ORA |

Original IDs resolve in [EVIDENCE.md](EVIDENCE.md#source-references).
ODC IDs resolve in [PRODUCT-EVIDENCE.md](PRODUCT-EVIDENCE.md#source-references).

### Execution and edition gap matrix

| Platform | Free OSS | Oracle | Reliable Migration State | Central Control Plane | Result |
|---|---|---|---|---|---|
| Bytebase Community | PARTIAL | YES | NO | YES | NO TARGET MIGRATION STATE. COMMUNITY LIMIT TOO RESTRICTIVE. |
| OceanBase ODC | YES | YES | NO | YES | RETAIN CATEGORY A SHORTLIST. TARGET STATE AND RELEASE ARTIFACT GAPS. |
| SQLE + DMS Community | PARTIAL | PARTIAL | UNKNOWN | YES | CATEGORY B. FREE SQL VERSION RELEASES BLOCKED. ORACLE PLUGIN LICENSE UNKNOWN. |
| AccessFlow | YES | PARTIAL | NO | YES | RETAIN CATEGORY A SHORTLIST. TARGET STATE AND SCRIPT GATE GAPS. |
| D-Band DRM | UNKNOWN | YES | PARTIAL | NO | NO CENTRAL SERVER. LICENSE COVERAGE UNKNOWN. PAID FLYWAY OPTION. |
| Open Migration | YES | NO | PARTIAL | PARTIAL | NO ORACLE. NO CHECKSUM VALIDATION. |
| SchemaPilot | NO | NO | PARTIAL | PARTIAL | SOURCE AVAILABLE. NO ORACLE. |
| Flyway UI | YES | UNKNOWN | UNKNOWN | NO | NO CENTRAL CONTROL PLANE. STALE DEPENDENCIES. |
| Flyway Play | YES | PARTIAL | PARTIAL | NO | NO CENTRAL CONTROL PLANE. |
| Liquibase 5.x | NO | YES | PARTIAL | NO | SOURCE AVAILABLE. NO CENTRAL SERVER. |
| Liquibase 4.33.0 | YES | YES | PARTIAL | NO | NO CENTRAL SERVER. RECOVERY REQUIRES VERIFICATION. |
| Flyway Community | YES | YES | PARTIAL | NO | NO CENTRAL SERVER. RECOVERY REQUIRES VERIFICATION. |
| Sqitch | YES | YES | PARTIAL | NO | NO CENTRAL SERVER. RECOVERY REQUIRES VERIFICATION. |
| Atlas OSS | YES | NO | PARTIAL | NO | ORACLE REQUIRES PRO. NO OSS CONTROL PLANE. |
| Yearning | YES | NO | NO | YES | NO ORACLE. NO TARGET MIGRATION STATE. |
| Archery / sampled derivative | YES | YES | NO | YES | NO TARGET MIGRATION STATE. |
| .NET dbdeploy | YES | YES | PARTIAL | NO | NO CENTRAL SERVER. |
| DbMaintain | YES | YES | PARTIAL | NO | NO CENTRAL SERVER. DEPRECATED. |
| dbpm | PARTIAL | YES | PARTIAL | NO | NO CENTRAL SERVER. REQUIRED CORE REVIEW INCOMPLETE. |
| dbward core | PARTIAL | NO | PARTIAL | YES | NO ORACLE. NO TARGET CHECKSUM VALIDATION. FREE DISTRIBUTION LIMITS. |
| CloudBeaver Community | YES | YES | NO | YES | NO TARGET MIGRATION STATE. NO RELEASE WORKFLOW. |
| Jenkins + Flyway proposal | YES | YES | PARTIAL | PARTIAL | COMPOSITION. IMPLEMENTATION AND VERIFICATION REQUIRED. |
| Rundeck + Flyway proposal | YES | YES | PARTIAL | PARTIAL | COMPOSITION. APPROVAL AND INVENTORY WORK REQUIRED. |

`PARTIAL` engine state reflects real target ledgers with an Oracle DDL recovery gap.
It does not mean that those engines lack normal applied detection.
No row becomes a complete match merely because several components could be connected.
ODC and AccessFlow remain platform candidates under the revised selection rule.

## 3. Detailed candidate analysis

### OceanBase ODC: existing project estate and ordered Oracle deployment batches

Category: A. Platform Fit: HIGH. Migration Engine Fit: LOW.
Repository: `oceanbase/odc`. Snapshot: `d517c0f27971642fb0cd7565fd61ab2309875ec3`.
The public main commit is dated 2025-06-19.
The pinned frontend submodule is `273fa3c4cc7d87f942ade231ce9220b98fa595e2`, dated 2025-05-07.
The review does not establish active public main development in 2026.

The backend and frontend have Apache-2.0 licenses.
No paid instance or user gate was identified in the inspected project and batch-change path.
The web deployment runs locally with central metadata services.
The documented container example uses an OceanBase MySQL metadata tenant.
This differs from the Oracle target databases.
The deployed image contains separate Oracle plugins and `ojdbc8-21.1.0.0.jar`.
This inspection establishes packaging presence. Complete image dependency licensing and Oracle execution remain unverified.
[P-ODC-LICENSE, P-ODC-CLIENT-L, P-ODC-DEPLOY](PRODUCT-EVIDENCE.md#source-references)

```text
Projects -> database estate -> environment-labelled targets
                       |
          reviewed batch database change ticket
                       |
           ordered groups of database targets
              |                    |
      automatic/manual       central metadata
      continuation           parent/child status, logs
              |
         Oracle JDBC -> Oracle
                          |
                no migration ledger in reviewed path
```

ODC has separate project, environment, and database entities.
Its frontend exposes Projects, project Databases, Tickets, Data Sources, Users, Security, and Integrations.
A batch change selects databases from one project and arranges them into ordered execution groups.
Targets within a group execute concurrently. Groups execute in order.
The frontend displays environment labels and permits manual or automatic continuation.
The official batch guide describes development, testing, prerelease, and production use.
[P-ODC-PROJECT, P-ODC-ENV, P-ODC-DATABASE, P-ODC-QUEUE, P-ODC-BATCH-DOC](PRODUCT-EVIDENCE.md#source-references)

This is an existing estate deployment workflow.
It is broader than an isolated SQL approval ticket.
It still differs from Bytebase's release model:

- A ticket and its SQL files do not establish an immutable application release with a stable version and target checksum.
- Ordered target batches do not establish an enforced named environment ladder or a prerequisite release policy.
- Parent approval applies before batch execution. The inspected worker creates child tickets without a new approval node.
- `CONTINUE` error policy can permit later execution after failure. The accepted policy must be verified explicitly.
- The documented batch limit is 2–100 databases. This is a task limit, not a licensed total estate limit.
- Running batches cannot be aborted through the documented batch control. Manual batches can stop while awaiting the next group.

[P-ODC-BATCH-MODEL, P-ODC-BATCH-EXEC, P-ODC-STRATEGY, P-ODC-BATCH-DOC](PRODUCT-EVIDENCE.md#source-references)

Actual Oracle support is distinct from OceanBase Oracle compatibility mode.
The Oracle connection plugin builds `jdbc:oracle:thin` URLs for SID or service name.
The Oracle frontend configuration explicitly enables single and multiple database change tasks.
The embedded OceanBase Cloud Platform (OCP) deployment removes the Oracle frontend option. Evaluate standalone ODC Web for this shortlist.
It also enables PL editing and anonymous blocks, while its compile action is disabled.
That configuration does not prove invalid-compilation detection during deployment.
Oracle packages, triggers, q-quoted literals, slash delimiters, and failure recovery remain runtime verification cases.
No SQLPlus interpreter was established in the reviewed JDBC execution path.
[P-ODC-ORACLE, P-ODC-ORACLE-UI](PRODUCT-EVIDENCE.md#source-references)

The executor runs statements through JDBC and then stores results.
Its configured retry loop can repeat a failed statement. The default retry count is zero.
No target version/checksum lookup or target migration ledger write was found in this reviewed path.
A new ticket can therefore require external verification to prevent repeated committed DDL.
Central task recovery does not establish target applied detection after an uncertain Oracle result.
[P-ODC-EXEC, P-ODC-PARAMS](PRODUCT-EVIDENCE.md#source-references)

The [frontend evidence](UI-EVIDENCE.md) includes official project and batch-change screenshots.
The screenshots show OceanBase MySQL examples. Oracle support is established separately by source.
The [product comparison](PRODUCT-MODEL.md) records Git and CI/CD limits without treating roadmap promises as implementations.

#### Deployed topology, permissions, and API integration

ODC 4.4.1 runs as one Java/web Deployment in namespace `oceanbase-odc`.
Its application PVC is 5 GiB. A separate OceanBase CE StatefulSet provides a 10 GiB MetaDB PVC.
The MetaDB uses OceanBase's MySQL tenant `test` and schema `odc_metadb`.
It stores ODC application state. Managed Oracle data stays in the external Oracle target.
Single application and database replicas do not provide high availability.
Kubernetes is optional. The official repository also documents Docker deployment with a MetaDB.

Project administrators, DBAs, and Developers inherit access to every project database.
Participants need explicit grants and suit evaluation of access limited to selected database/schema records.
ODC grants support QUERY, CHANGE, EXPORT, ACCESS, and expiry.
They are application metadata. Oracle permissions still depend on the datasource account's native privileges.
Actual cross-schema isolation, expiry, and approval duties remain NOT RUN.
[P-ODC-ROLE-INHERITANCE, P-ODC-DB-PERMISSION-SERVICE](PRODUCT-EVIDENCE.md#source-references)

The datasource API can register Oracle connections and synchronize schema records. It does not provision an Oracle instance.
Flow APIs expose ticket creation, approval, execution, status, and logs.
Project repository registration exists, so Git integration is PARTIAL rather than UNKNOWN.
Native merge-to-deploy automation was not established.
The current login uses encrypted credentials, session cookies, organization context, and CSRF protection.
Authenticated list GET requests succeeded. CI write requests and Oracle task execution remain unverified.
[P-ODC-DATASOURCE-API, P-ODC-FLOW-API, P-ODC-GIT-API](PRODUCT-EVIDENCE.md#source-references)

The inspected deployment does not expose a working Swagger API catalog.
The latest HTML route returned 200, but its resource endpoint returned 404 and its documentation route returned configuration-shaped JSON.
Select English through the UI language selector. The setting is stored per browser.
ODC's Apache-2.0 source rights remain separate from OceanBase commercial database trials and hosted-service charges.

The [detailed ODC evaluation](ODC-EVALUATION.md) contains the architecture diagram, Bytebase mappings, Oracle procedure, API routes, and evidence limits.
The [runtime record](evidence/product-model/odc-runtime-20261003.json) records sanitized deployment observations.

### SQLE + DMS Community: project SQL governance with paid version releases

Category: B. Platform Fit: LOW. Migration Engine Fit: LOW.
SQLE snapshot: `44e88c45f9cd55edb2d826795770001e019dda81`.
DMS snapshot: `d63b4ea798e811881107d193b25d2c33f6d8685c`.
Their inspected root licenses are MPL-2.0.

The commercial project model and central SQL workflow justify serious comparison.
Community blocks project creation and modification in the inspected DMS implementation.
It also blocks global datasource inventory endpoints.
Per-project connection metadata and environment tags do not remove those restrictions.
[P-DMS-PROJECT-CE, P-DMS-INVENTORY-CE, P-DMS-ENV](PRODUCT-EVIDENCE.md#source-references)
Community's SQL-version controller returns an Enterprise feature error.
The blocked endpoints include version creation, version dependencies, batch release, and batch execution.
A product-wide release description therefore cannot be assigned to the free edition.
[P-SQLE-L, P-DMS-L, P-SQLE-CE, P-SQLE-VERSION](PRODUCT-EVIDENCE.md#source-references)

The public Oracle audit plugin also contains direct SQL execution through `go-ora`.
Its source snapshot has no root license file.
A free, fully licensed Oracle distribution was therefore not established.
Oracle execution must not be dismissed merely because the plugin calls itself an audit plugin.
The missing free version-release workflow independently prevents Category A selection.
[P-SQLE-ORACLE, P-SQLE-ORACLE-DOC](PRODUCT-EVIDENCE.md#source-references)

DMS builds against a separate `dms-ui` output.
That public frontend location was inaccessible during this review.
The [comparison](PRODUCT-MODEL.md) retains frontend and edition uncertainties explicitly.
[P-DMS-FRONTEND](PRODUCT-EVIDENCE.md#source-references)

### AccessFlow: existing schema promotion, partial project estate

Category: A. Platform Fit: MEDIUM. Migration Engine Fit: LOW.
Repository: `bablsoft/accessflow`. Source snapshot: `55c209a4d9e4ba09a6c089f90e68a8b16b3f2133`.
Latest recorded release: `v2.7.0`, 2026-10-01.
The review used the default-branch snapshot. It did not verify the matching container build.

The repository license is Apache-2.0.
No paid feature boundary or licensed instance limit was identified in the inspected workflow.
Modification and internal forks are permitted under the license conditions.
Deployment uses Spring Boot, React, PostgreSQL, and Redis.
Docker Compose and a Helm chart exist. Normal execution can occur on local infrastructure. [AF-L, AF-DR](EVIDENCE.md#source-references)

```text
React UI / REST / CI request
        |
Spring Boot: review, permission checks, promotion
        |                         |
        |                  central PostgreSQL
        |                  sets, checksums, results, audit
        v
Ordered request group -> JDBC prepared statements
        |
Oracle Thin JDBC -> Oracle
                         |
                    no target migration ledger
```

Flyway in the backend dependencies migrates AccessFlow's own PostgreSQL schema.
That dependency does not prove target-side Flyway execution.
The inspected Oracle path uses JDBC directly. [AF-GROUP, AF-JDBC, AF-ORA, AF-DOC](EVIDENCE.md#source-references)

The new schema workflow has immutable statement content after promotion.
It calculates a SHA-256 checksum and checks that central statement content still matches.
Lower bound environments must have a successful central promotion before higher environments proceed.
Permissions, freeze windows, and review rules restrict promotion. [AF-PROM](EVIDENCE.md#source-references)

This improves release governance. It does not close the migration-state gap:

- Target checksum validation: `NO` in the inspected path.
- Target migration ID and applied detection: `NO` in the inspected path.
- Central result recording: `YES`, after the target operation.
- Partial execution: central group results identify failed or partially executed groups.
- Safe retry after an uncertain Oracle result: `UNKNOWN`.
- Automatic skip after a previous successful promotion: not established by the promotion guard.

The open-promotion guard covers `PENDING`, `IN_REVIEW`, and `APPROVED`.
It excludes `APPLIED`. It therefore does not prove exactly-once promotion.
The executor saves each member result after target execution. [AF-PROM, AF-GROUP](EVIDENCE.md#source-references)

The schema workflow documentation identifies another recovery gap.
A lost asynchronous status update can leave a promotion pending after its DDL has run.
The module has no repair path for that condition.
Partially applied promotions also require a new change set.
Freeze windows are checked at submission rather than execution. [AF-RECOVERY](EVIDENCE.md#source-references)

Oracle SQL, DDL, and DML have a connector and direct execution path.
The schema change-set path refuses `SELECT`, `INSERT`, `UPDATE`, and `DELETE`.
The scanner also refuses a leading `BEGIN` and internal statement separators.
Common procedures, packages, triggers, and anonymous PL/SQL therefore cannot be assumed to pass that gate.
Oracle q-quoted literals and complex procedural syntax need separate parser verification.
No SQLPlus script interpreter was found in this path. [AF-GATE, AF-SCAN](EVIDENCE.md#source-references)

AccessFlow documents OIDC, SAML, RBAC, service accounts, audit records, notifications, Vault, backup, and recovery.
Its deployment guide supports multiple replicas and shared services.
These source and documentation features do not prove safe concurrent Oracle migration execution.
LDAP authentication was not established in this review. [AF-SSO, AF-VAULT, AF-DR, AF-CI](EVIDENCE.md#source-references)

### Archery: Oracle-aware SQL workflow, target ledger absent

Category: B. Platform Fit: LOW. Migration Engine Fit: LOW.
Repository: `hhyo/Archery`. Source snapshot: `ccc7134f48d0e261f9e3ffa0d445dcec48adb790`.
Latest recorded release: `v1.14.0`, 2026-03-07.
License: Apache-2.0. No paid user or instance limit was identified in the inspected source.

```text
Web UI / API -> Django review and execution workflow
                      |                   |
                      |             central metadata DB
                      |             SQL, actor, review, result
                      v
OracleEngine -> python-oracledb -> Oracle
                                      |
                                 no migration ledger

Optional Oracle backup material -> separate MySQL backup DB
```

The current connector uses `python-oracledb`.
Thin or OCI-backed thick mode depends on the installed driver configuration.
The source reviewed here does not invoke SQLPlus. [AR-ORA](EVIDENCE.md#source-references)

Its parser explicitly identifies procedures, functions, triggers, packages, package bodies, and anonymous blocks.
Its execution loop commits each statement.
It then checks the compilation status of named PL/SQL objects.
The failed-statement path cannot undo previous committed statements. [AR-PARSER, AR-EXEC](EVIDENCE.md#source-references)

Central workflow models store the requester, database instance, schema, time, SQL, review, and execution result.
This meets much of the accountability requirement.
It does not establish immutable release artifacts, target checksums, or applied detection across repeated tickets.
Oracle backup rows are recovery material. They are not a target migration ledger. [AR-STATE, AR-EXEC](EVIDENCE.md#source-references)

Archery refuses some SQLPlus commands, including `SET`, `ROLLBACK`, and `EXIT`.
Its procedural parser uses text normalization and delimiter handling.
Complex literals, wrapped code, nested blocks, slash placement, and invalid compilation need Oracle verification.
The [official Oracle review documentation](https://archerydms.com/modules/sql_check/) describes only a subset of SQL review rules. [AR-SQLPLUS](EVIDENCE.md#source-references)

The sampled `Tareya/devops-archery` derivative retains direct Oracle workflow execution.
No target migration ledger was identified in that path.
This result cannot be generalized to every Archery fork. [FORK-L, FORK-EXEC](EVIDENCE.md#source-references)

### Bytebase: reference architecture with multiple knockout reasons

Repository: `bytebase/bytebase`. Source snapshot: `80524fc54601bcc5545575e02f83b23ee6bb0a70`.
Latest recorded release: `3.23.0`, 2026-09-24.

The root license distinguishes MIT code from directories containing `enterprise`.
Those enterprise directories use a proprietary license.
The root license also excludes feature, permission, role, and plan enablement code from the MIT grant.
A separate unrestricted grant for that line was not established.
Public source availability does not grant production rights to the enterprise code.
MIT portions permit modification and internal forks under their conditions.
The report proposes no removal or bypass of license enforcement. [BB-L, BB-ENT](EVIDENCE.md#source-references)

The Free plan has 10 instances and 20 seats.
It permits projects, environments, database changes, basic IAM, query history, and SQL review.
It excludes enterprise approval workflows and the audit-log feature.
OIDC, LDAP, custom roles, and external secrets also have paid boundaries.
No separate free environment count was identified. [BB-PLAN, BB-GATES](EVIDENCE.md#source-references)

```text
Web UI / API -> Bytebase backend -> release task runner
                       |                     |
                central PostgreSQL       Go SQL driver
                revision/changelog       go-ora + Oracle splitter
                                             |
                                           Oracle
                                             |
                                     no target migration ledger
```

Oracle execution uses `go-ora`, not Flyway or JDBC.
The driver has transaction and autocommit paths.
The release runner reads applied versions from central records.
It executes a file before creating the central revision with the version and sheet SHA-256.
An Oracle commit followed by a central-record failure can therefore leave an uncertain result.
That is an inference from the execution order. [BB-DRIVER, BB-ORA, BB-STATE](EVIDENCE.md#source-references)

The repository has Oracle splitting and PL/SQL parser code.
A complete SQLPlus client environment was not established.
Packages, anonymous blocks, q-quoted text, slash delimiters, and compile errors remain runtime verification cases.
Bytebase's central changelog must not be described as an Oracle `flyway_schema_history` equivalent.

### D-Band DRM: still local, with an important Flyway dependency

Repository: `dband-drm/drm-cli`. Source snapshot: `d6b049d79b07a461949ec89e15dfe2c1eecf81ed`.
Package version: `1.2.1`. Latest recorded GitHub release: `Release1.2.0`, 2026-04-25.
The package and GitHub release versions differ.

Installation selects SQLite or JSON metadata.
The repository has a command interface and an MCP process for AI tools.
That MCP process does not establish a shared multi-user database change server.
No web inventory, shared metadata service, or approval server was identified. [DRM-LOCAL](EVIDENCE.md#source-references)

```text
CLI / CI / MCP process -> local SQLite or JSON
                 |
        Flyway dry-run generation OR Liquibase updateSql
                 |
             generated SQL
                 |
              SQLPlus -> Oracle
```

The Flyway adapter passes `-dryRunOutput`.
The current [Flyway setting reference](https://documentation.red-gate.com/fd/flyway-namespace-277578913.html) places this feature in Teams.
The inspected adapter therefore does not establish a usable Flyway Community-only path. [DRM-FW](EVIDENCE.md#source-references)

The Liquibase path generates SQL with `updateSql`, then uses native execution.
Generated history inserts may produce target state.
This path is not equivalent to running the migration engine directly under its normal locking and validation path.
Target locking, checksum validation before execution, and retry behavior need separate verification. [DRM-LB, DRM-SQLPLUS](EVIDENCE.md#source-references)

The Oracle parser accepts narrow IPv4 and service-name patterns.
The runner appends `EXIT` and relies on the process exit code.
It does not add its own `WHENEVER SQLERROR` or `WHENEVER OSERROR` in the inspected method.
An SQLPlus script can therefore need explicit error directives to return reliable failure status.
The release layer also retries failures. Safe replay after partial DDL was not established. [DRM-EXEC, DRM-SQLPLUS, DRM-RETRY](EVIDENCE.md#source-references)

The current package declares ISC, while earlier public descriptions claimed MIT.
No complete license file covers the inspected repository snapshot.
Internal modification rights across the Python payload therefore remain `UNKNOWN` in this report.
DRM fails the central-server requirement independently of this license uncertainty. [DRM-L](EVIDENCE.md#source-references)

### Open Migration: central UI prototype, no Oracle

Repository: `minuth/open-migration`. Source snapshot: `5dc73cc3ee98e3951d7436bfccb12063c0d6441e`.
License: MIT. Docker deployment exists.
The Nuxt server has central SQLite metadata and an administrator session.
SQLite does not prevent central management. The missing multi-user model and operational controls limit this implementation. [OM-L, OM-META, OM-AUTH](EVIDENCE.md#source-references)

```text
Nuxt UI / API -> migration service -> engine factory
        |                                  |
central SQLite              PostgreSQL / SQLite / MySQL / MariaDB
                                            |
                                _migrations_tracking in target

Oracle: no implemented engine
```

The tracking table stores a filename and applied time.
It has no checksum, actor, or failed-state fields.
Applied detection uses filenames.
The PostgreSQL implementation executes SQL and inserts history in one transaction.
This does not establish equivalent Oracle DDL behavior.
The migration service catches an individual failure and continues its outer loop. [OM-ENG, OM-STATE, OM-RUN](EVIDENCE.md#source-references)

GitHub and GitLab source retrieval exists.
An Oracle adapter alone would not close the checksum, locking, approval, identity, and audit gaps.
This is a larger implementation base than its UI initially suggests.

### SchemaPilot: restricted license and custom history writes

The name is ambiguous. The migration UI in this report is `apegeek/schema-pilot`.
Other search results use “SchemaPilot” for data platforms, CSV migration, or schema.org editing.
Those results are not treated as the same product.

Source snapshot: `67b2cc2864df1ce0d1f1f87dfd9d14ded792fe88`.
Its custom license permits internal use and modifications within its defined scope.
It restricts commercial redistribution and paid services.
It therefore fails the genuine OSS requirement. [SP-L](EVIDENCE.md#source-references)

The server implements MySQL and PostgreSQL clients.
It creates and writes a table named `flyway_schema_history` itself.
This table name does not establish that Flyway executes or validates the migration.
Execution responses can show successful SQL with separate history errors.
No Oracle implementation was found in the reviewed server. [SP-DRIVERS, SP-EXEC](EVIDENCE.md#source-references)

### Flyway UI and Flyway Play: application components

`binout/flyway-ui` is an Apache-2.0 servlet component.
It obtains one supplied Flyway object and displays its information.
Its dependency is Flyway 2.2.1, with a Java 6 build target.
The inspected servlet provides no central estate model, approval service, or durable multi-user audit.
Current Oracle suitability remains unverified. [UI-L, UI-DEPS, UI-SERVLET](EVIDENCE.md#source-references)

`playframework/flyway-play` is an Apache-2.0 Play application module.
It has Flyway history and a migration page within an application.
The default dependency remains Flyway 9.16.0.
It is not an independent central control plane for many applications and databases.
Oracle capability comes from the configured Flyway version and driver. [PLAY-L, PLAY-SCOPE, PLAY-DEPS](EVIDENCE.md#source-references)

### Migration engines: necessary components, not complete platforms

| Engine | Target state and identity | Checksum and applied behavior | Oracle execution | Failure and retry boundary |
|---|---|---|---|---|
| Flyway Community | `flyway_schema_history`. Version, rank, actor, time, result. | SQL checksums. Normal successful versioned migrations are skipped. Changed repeatable migrations can run again. | Oracle Thin JDBC and Oracle parser. PL/SQL uses slash delimiters. | Nontransactional failures can leave DDL applied. Recovery and repair require inspection. |
| Liquibase 4.33.0 | `DATABASECHANGELOG` and `DATABASECHANGELOGLOCK`. Identity uses ID, author, and filename. | Stored checksum and normal applied filtering. `runAlways` and `runOnChange` alter skip behavior. | Oracle JDBC. SQL or changeset configuration must preserve procedural bodies. | Failed DDL can remain applied without a successful changelog row. Lock and target inspection are required. |
| Sqitch | Target Oracle registry with `changes`, `tags`, dependencies, and events. | Change IDs and script hashes. Verification and integrity checks differ from Flyway validation. | Native SQLPlus for scripts. Oracle client setup is required. | Deploy occurs before verification and final registry recording. Revert scripts cannot guarantee undo of committed DDL. |

Evidence: [FW-ORA, FW-PARSER, FW-EXEC, FW-FAIL, LB4-STATE, LB4-SKIP, LB4-EXEC, SQ-STATE, SQ-EVENTS, SQ-EXEC, SQ-SQLPLUS](EVIDENCE.md#source-references).

Liquibase 5.x has similar migration concepts but a different current license.
Its FSL permits specified internal uses and provides an Apache license after two years.
That future grant does not make newly released code open source today. [LB5-L](EVIDENCE.md#source-references)

The 4.33 source license must be distinguished from bundled commercial binaries or extensions.
A strict OSS composition must use the inspected OSS source and separately check every bundled component.
The [official 4.33 FAQ](https://docs.liquibase.com/oss/user-guide-4-33/faq) notes commercial code in some distributions.

Flyway Community supports normal Oracle SQL and procedural migrations.
Full SQLPlus commands are a separate feature boundary.
The [Oracle settings reference](https://documentation.red-gate.com/flyway/reference/configuration/flyway-namespace/flyway-oracle-namespace) assigns SQLPlus support to Teams.
The native Oracle connector is also a Redgate preview feature.
A free design must not assume that `PROMPT`, `SET`, `SPOOL`, `@`, or `@@` work through Community JDBC.

### Other candidates and forks

Yearning documents MySQL auditing. Oracle is absent from the reviewed product scope.
Its central SQL workflow cannot satisfy the Oracle requirement. [YE-L, YE-SCOPE](EVIDENCE.md#source-references)

The additional search examined .NET dbdeploy, legacy DbMaintain, dbpm, dbward, and CloudBeaver.
The engine projects lack a central service.
The server projects lack Oracle migration state or Oracle execution.
See [the corrected additional analysis](additional-candidates.md).

GitHub fork metadata was collected for the first twelve repositories.
The original sample includes the newest twenty forks where the repository has more forks.
The [supplemental fork search](FORK-SEARCH.md) adds seven direct Bytebase fork checks and historical Apache license review.
The Tareya Archery derivative received direct source review.
No inspected derivative closed every hard gap.
This is a sampled result. It is not a claim that no suitable fork exists anywhere.

## 4. Existing OSS platform shortlist

The revised shortlist contains existing products. Missing target migration state is an execution gap, not an automatic platform rejection.

| Project | Category | Platform Fit | Migration Engine Fit | Next decision |
|---|---|---|---|---|
| OceanBase ODC | A | HIGH | LOW | Verify the existing project estate, Oracle batch workflow, approval scope, and recovery behavior. |
| AccessFlow | A | MEDIUM | LOW | Verify the existing schema promotion. Decide whether pipeline and datasource abstractions meet the required estate model. |

ODC is the strongest product-model candidate in the documented search.
AccessFlow is more recently active and has explicit central change-set checksums and promotion prerequisites.
Neither has verified reliable Oracle target migration state in the reviewed execution path.
Neither needs an engine integration proposal to explain why its existing platform belongs in this evaluation.

Archery and SQLE Community remain Category B alternatives.
Open Migration and SchemaPilot remain Category C migration UIs.
The engines remain Category C execution references.
The [18-capability comparison](PRODUCT-MODEL.md) gives the precise differences.
The [frontend evidence](UI-EVIDENCE.md) supports the shortlist with actual pages and official screenshots.

## 5. Rejected candidates

The execution gap matrix records state and edition limits.
The product comparison records Category B and C exclusions from the primary platform shortlist.
ODC and AccessFlow remain shortlisted despite their target-state gaps.
Commercial reference products have a separate status:

| Reference | Status for this request | Basis |
|---|---|---|
| Bytebase Enterprise | COMMERCIAL GOVERNANCE FEATURES | BB-ENT and BB-GATES establish the paid boundary. |
| Liquibase Secure server | COMMERCIAL PRODUCT | Current vendor documentation distinguishes Secure from Community and OSS 4.33. |
| Atlas Pro / Atlas Cloud | ORACLE REQUIRES PRO. OSS CONTROL PLANE NOT ESTABLISHED. | Official compatibility and public CLI source. |
| Harness Database DevOps | FREE OSS SELF-HOSTED PRODUCT NOT ESTABLISHED | Its self-managed platform documentation requires enterprise licensing. |
| Oracle SQLcl by itself | NO CENTRAL SERVER. PLATFORM OSS NOT ESTABLISHED. | It is an execution client, not the requested central governance platform. |

Harness Open Source repository licensing does not establish licensing for the Database DevOps module.
This review does not claim that the relevant self-managed module is fully available under Apache-2.0.
The [self-managed architecture](https://developer.harness.io/docs/self-managed-enterprise-edition/reference-architecture) is the relevant deployment reference.

## 6. Best proof-of-concept candidates

The first target is OceanBase ODC's existing platform workflow.
Verify project ownership, Oracle inventory, environments, requester identity, approval, ordered batches, history, and logs.
Verify manual continuation and failure policy across DEV, SIT, UAT, and PROD.
Then evaluate immutable release binding, duplicate execution, target state, and uncertain-result recovery.

The second target is AccessFlow's existing schema change-set workflow.
Verify datasource-bound environments, immutable central content, lower-environment prerequisites, review, promotion, and history.
Determine whether its project and database abstractions meet the accepted estate model.
Verify required DML and PL/SQL before accepting its schema gate.

Evaluate the existing products before implementing adapters.
Only if a selected platform fails execution acceptance should an engine integration become the next design task.
Flyway Community against the required Oracle version is then a secondary engine verification target.
Archery remains a secondary SQL governance option for teams that already operate it.
Bytebase Community remains a limited reference installation, not the large-estate free recommendation.

## 7. Required Oracle proof of concept

[poc/ORACLE-POC.md](poc/ORACLE-POC.md) includes every required SQL and failure case.
It also includes checksum changes, duplicate submissions, concurrent runners, approval binding, and invalid PL/SQL compilation.

The process-crash case has two distinct checkpoints:

1. Stop the worker after Oracle commits and before the target ledger records success.
2. Stop the worker after the target ledger records success and before central success is recorded.

The first checkpoint requires uncertain-state handling and operator reconciliation.
The second checkpoint should recover success from the target ledger without replaying SQL.
A UI status change alone cannot prove that either checkpoint is safe.

## 8. Evidence pack and maturity

The original evidence pack contains twenty source snapshots and commit-pinned references.
The product-model revision adds a separate source register, frontend review, screenshots, and fork comparisons.
See [PRODUCT-EVIDENCE.md](PRODUCT-EVIDENCE.md) and its [supplemental manifest](evidence/product-model/source-manifest.json).
Each reference records a repository, SHA, file, line range, and local file hash.
See [EVIDENCE.md](EVIDENCE.md), [source-references.csv](evidence/source-references.csv), and [source-manifest.json](evidence/source-manifest.json).

[MATURITY.md](MATURITY.md) reports available releases, activity, stars, forks, contributors, issues, deployment assets, documentation, and security evidence.
Missing or incomplete statistics remain explicit.
Repository popularity is not proof of production readiness.
ODC images were deployed, and Oracle plugin/driver presence was inspected.
No image vulnerability scan or complete binary dependency audit ran.
The other candidates retain their original source-only verification scope.

## 9. Remaining gaps and engineering scope

### Secondary composition options

These options apply only after the existing platform evaluation.
They are engineering proposals, not discovered complete products.

| Proposal | Potential value | Required work |
|---|---|---|
| ODC + migration engine | Preserve project estate and batch workflow | Immutable releases, engine jobs, target reconciliation, approval binding, recovery. |
| AccessFlow + Flyway Community | Preserve schema promotion and governance | Dedicated migration authoring path, engine worker, target reconciliation, recovery. |
| Archery + Flyway Community | Preserve an existing SQL governance deployment | Add a project release model and environment promotion. |
| Existing Jenkins + Flyway Community | Reuse existing CI/CD operations | Database estate inventory, release approval binding, structured records, recovery. |
| Rundeck Community + Flyway Community | Reuse job inventory and execution controls | Database release model, approval records, environment promotion, recovery. |

Rundeck job access control does not establish complete change approval.
Jenkins build logs do not establish a complete database audit database.

### Proposed execution architecture

```text
Existing UI / API / reviewed Git release
                 |
Central inventory + immutable release record
                 |
Approval bound to release hash, target, and environment
                 |
Durable job + target/schema lock
                 |
Worker -> Flyway Community -> Oracle
                               |
                       flyway_schema_history
                 |
Central result + logs + reconciliation
```

For a Flyway proposal, the worker must not execute SQL independently and then write a Flyway-shaped table.
It must invoke the actual migration engine with validation enabled.
The central service must retain the human requester and approver separately from the database service account.

### Estimated scope

These are engineering estimates, not vendor commitments.
One engineer-week means five working days by an experienced engineer.
The estimates assume an existing identity provider, Git service, secret manager, and deployment infrastructure.
They cover an initial Oracle release workflow. They exclude full commercial-product parity.

| Option | Bounded proof of concept | Initial operational version | Main work |
|---|---|---|---|
| AccessFlow + Flyway adapter | 2–4 engineer-weeks | 8–14 engineer-weeks | Immutable artifacts, engine jobs, dedicated migration authoring path, target reconciliation, permissions. |
| Archery + Flyway adapter | 3–5 engineer-weeks | 10–16 engineer-weeks | Release and environment model, artifact approval, engine worker, target history, recovery. |
| Existing Jenkins + Flyway | 1–2 engineer-weeks | 4–8 engineer-weeks | Inventory manifest, approved artifact pinning, structured central records, locking, recovery. |
| Rundeck Community + Flyway | 2–3 engineer-weeks | 6–10 engineer-weeks | Job wrapper, approval records, promotion, inventory, target reconciliation. |
| Open Migration extension | 4–6 engineer-weeks | 14–24 engineer-weeks | Oracle engine or engine adapter, checksum model, multi-user identity, RBAC, approval, audit, operations. |

Do not add the two columns. The operational estimate includes the proof of concept.
Two engineers may reduce elapsed time. Independent reviews and failure experiments still constrain the schedule.

### Minimum implementation checklist

1. Define stable application, instance, service, schema, and environment identities.
2. Create immutable release artifacts with Git commit and SHA-256 references.
3. Bind approval to the exact artifact and target set.
4. Preserve requester, approver, service account, trigger, and timestamps separately.
5. Serialize migrations by target schema and ledger.
6. Invoke a pinned, licensed OSS engine with validation enabled.
7. Store complete SQL references, redacted logs, engine results, and target versions centrally.
8. Reconcile central state against target history after restart.
9. Mark uncertain target results for operator review.
10. Require reviewed recovery after partial DDL.
11. Back up central metadata, artifacts, configuration, and necessary encryption keys.
12. Verify restore against target ledgers before enabling execution.

A target ledger does not solve cross-database atomic deployment.
It does not provide automatic rollback, SQL review, drift detection, or immutable central audit.
Those gaps remain separate acceptance items.

Advanced HA, broad schema diff, deep Oracle drift analysis, SIEM delivery, and complete policy tooling need additional scope.
The source review does not establish measured availability, recovery time, or production scale for any proposed composition.

## Bytebase API/UI POC, 04/10/2026

[Bytebase mới: 45 kết quả](BYTEBASE-ORACLE-POC-RESULTS.md) và [đối chiếu ODC](BYTEBASE-ODC-COMPARISON.md).
Kết quả: 17 PASS, 14 PARTIAL, 4 FAIL, 3 BLOCKED, 7 NOT_RUN. Runtime 3.22.1/FREE, Oracle 26ai.
Native version/replay và execution-role separation có bằng chứng tốt hơn ODC.
Procedure INVALID, SQL Review ERROR và early mockPROD vẫn là các lỗi cần xử lý.
Approval/audit bị giới hạn FREE; chưa đánh giá Enterprise hoặc controlled recovery.
Có 11 ảnh Selenium thật, API evidence và Oracle Thin hậu kiểm tại [portal](https://db-poc.apps.drgdevlab.com/).
Bằng chứng mới dùng `evidence/bytebase-poc-*.json`. Lịch sử P03/P04 vẫn FAIL, được giữ riêng.
