# Product model comparison

**OceanBase ODC is an existing free Oracle platform with open-source software (OSS) and substantial parts of the requested operating model.**
Its projects, estate inventory, environments, approval, and ordered deployment batches justify a Category A shortlist entry.
Its release artifacts and target migration state differ from Bytebase.
The review does not establish a complete replacement for every requested Bytebase workflow.

AccessFlow also remains in the shortlist.
Its schema change-set promotion is an existing database workflow.
Its project and estate models remain less complete.
Missing target state reduces the Migration Engine Fit score. It does not remove either platform from this shortlist.

Research date: 2026-10-03.
ODC is deployed at https://oceanbase.apps.drgdevlab.com with 5 GiB application storage and 10 GiB MetaDB storage.
Deployment and authenticated GET checks succeeded. Oracle API/UI POC has per-case results and migration failures.
See [ODC architecture, permissions, API, and license details](ODC-EVALUATION.md).
The [product-model constraint](product-model-constraint.md) controls selection.
The original [brief](brief.md) still controls execution verification.

## Reference operating model

The review studied Bytebase's public workflow and actual frontend before selecting platform candidates.
The full product reference contains workspace projects, registered instances, databases, environments, plans, issues, releases, and rollouts.
A plan holds proposed changes. An issue records review and approval. A rollout contains environment stages and database tasks.
Execution produces changelog and revision records.
The inspected Oracle runner records revisions centrally. It does not write an Oracle migration ledger.

The full reference includes paid capabilities.
A `YES` reference cell does not grant those capabilities in Community.
Community has instance and user limits. Configurable approval workflows and audit have paid boundaries.
Rollout permission checks must be distinguished from configurable approval workflows.

Sources: [Bytebase API resource model](https://api.bytebase.com/),
[Bytebase environment rollout example](https://www.bytebase.com/blog/database-multi-environment-deployments/),
[P-BB-MODEL, P-BB-ROUTES, P-BB-NAV](PRODUCT-EVIDENCE.md#source-references),
[BB-PLAN, BB-GATES, BB-STATE](EVIDENCE.md#source-references).

## Categories

Category A has an estate and a change lifecycle that includes deployment organization across targets or environments.
Category B primarily reviews and executes SQL tickets or controls interactive SQL access.
Category C primarily applies migration files or displays engine history.
A flat connection list, a web editor, or an approval button alone does not establish Category A.
CloudBeaver uses Category B as the closest SQL-access category. It lacks the approval workflow of a full SQL approval portal.

| Candidate | Category | Model finding |
|---|---|---|
| Bytebase Community / Enterprise reference | A | Complete reference model. Edition and license limits remain separate. |
| OceanBase ODC | A | Projects, estate, environments, approval, ordered database batches, and execution records. Release versioning remains partial. |
| AccessFlow | A | Schema change sets and ordered environment promotion. Project and estate abstractions remain partial. |
| Archery | B | Reviewed SQL tickets. No shared immutable release promotion established. |
| Tareya Archery derivative | B | Sampled Oracle SQL workflow derivative. |
| Yearning | B | MySQL SQL review and approval. |
| SQLE + DMS Community | B | SQL governance with restricted projects and global inventory. Free SQL versions and batch releases are blocked. |
| dbward core | B | Approval and SQL control server with a migration component. Full platform UI not established. |
| CloudBeaver Community | B | Central SQL workspace and connection browser. No release lifecycle. |
| D-Band DRM | C | Local CLI metadata and native execution. |
| Open Migration | C | Central file migration UI. No project/environment/review/rollout model. |
| SchemaPilot | C | Script editor and custom history table. Restricted license. |
| Flyway UI | C | Servlet view of a supplied Flyway instance. |
| Flyway Play | C | Application migration module. |
| Liquibase Community 5.x | C | Migration engine. Current source-available license. |
| Liquibase 4.33.0 source | C | Apache-licensed migration engine snapshot. |
| Flyway Community | C | Migration engine. Strong normal target tracking. |
| Sqitch | C | Script deployment engine and target registry. |
| Atlas public OSS | C | Schema engine. Oracle requires Pro. |
| .NET dbdeploy | C | Migration engine. |
| DbMaintain | C | Deprecated migration engine. |
| dbpm | C | Oracle migration CLI with unresolved Core license coverage. |
| Sampled Bytebase forks, including Dokeeper | A | Inherited platform structure. Independent complete free Oracle platform not verified. |
| NineData Community repository | B | Documented SQL governance distribution. Inspectable platform source absent. |
| Liquibase Secure server | A | Commercial reference. Free OSS server not established. |
| Atlas Pro / Cloud | A | Commercial reference. Public OSS control plane not established. |
| Harness Database DevOps | A | Commercial reference. Required free OSS self-hosted module not established. |
| Oracle SQLcl | C | Execution client. No central platform. |

The last commercial rows describe product class. They do not qualify for the OSS shortlist.
Jenkins and Rundeck compositions are proposed architectures. They are not discovered Category A database products.

## Independent fit scores

Platform Fit measures the estate, project, environment, review, deployment, and history model.
HIGH means most of that model exists. MEDIUM means material abstractions require work. LOW means an engine or SQL ticket model predominates.
Migration Engine Fit measures Oracle script handling, target applied detection, checksums, locking, and recovery controls.
HIGH requires strong normal engine tracking. MEDIUM means an important limitation. LOW means major state or execution gaps.
Scores describe inspected implementation. They do not certify runtime reliability.
No combined score is used.
Role-based access control (RBAC) assigns permissions to roles.

| Shortlisted project | Platform Fit | Migration Engine Fit | Selection status |
|---|---|---|---|
| OceanBase ODC | HIGH | LOW | First platform evaluation. Existing project estate and ordered database batches. |
| AccessFlow | MEDIUM | LOW | Second platform evaluation. Existing schema promotion. Project and estate gaps remain. |

ODC's HIGH score does not imply immutable application releases or an enforced DEV → SIT → UAT → PROD ladder.
Its ordered target batches can contain environment-labelled databases.
Manual or automatic continuation exists. A named environment promotion policy with artifact checksum binding remains unverified.
This distinction keeps ODC above a simple paste/approve/execute portal without claiming full Bytebase equivalence.

| Secondary reference | Platform Fit | Migration Engine Fit | Reason |
|---|---|---|---|
| Bytebase full reference | HIGH | LOW | Strong platform. Oracle state is central. Free limits prevent the requested estate fit. |
| Archery | LOW | LOW | Oracle SQL governance. Release promotion and target tracking absent. |
| SQLE + DMS Community | LOW | LOW | Community blocks project creation, global inventory, and SQL version releases. Oracle plugin license unresolved. |
| Flyway Community | LOW | HIGH | Normal Oracle ledger, checksum validation, and applied filtering. No estate platform. |
| Liquibase 4.33.0 | LOW | HIGH | Normal Oracle ledger and lock. No estate platform. |
| Sqitch | LOW | MEDIUM | Oracle registry and script verification. Integrity semantics differ from checksum validation. |

HIGH engine scores do not remove Oracle's committed-DDL recovery gap.
Those engines remain secondary components. They are not the final platform recommendation.

## Capability comparisons

`YES` requires source or official documentation. `PARTIAL` identifies a limited model or integration work.
`NO` identifies a reviewed gap. `UNKNOWN` identifies insufficient evidence.
Candidate cells describe the inspected free source unless stated otherwise.

### AccessFlow

| Capability | Bytebase reference | Candidate |
|---|---|---|
| Central web console | YES | YES |
| Project/application model | YES | PARTIAL. Pipelines and organizations, no first-class project estate |
| Database instance inventory | YES | PARTIAL. Datasource connections, no separate instance hierarchy |
| Environment model | YES | YES. Ordered pipeline environments |
| Schema/database inventory | YES | PARTIAL. Per-datasource schema browser |
| Change request | YES | YES. Requests and schema change sets |
| Change version/release | YES | YES. Central change-set identity and frozen checksum |
| Review | YES | YES |
| Approval | YES | YES |
| Deployment/rollout | YES | YES. Schema promotion executes database requests |
| Multi-environment promotion | YES | YES. Lower-environment success guard |
| Deployment history | YES | YES. Promotion history and request results |
| Audit | YES | YES |
| RBAC | YES | YES |
| Git integration | YES | YES. SCM connectors and repository references |
| CI/CD integration | YES | YES. Documented CI/API paths |
| Oracle | YES | PARTIAL. Oracle JDBC exists. Schema script gate limits scope |
| Migration state | Central revisions. Target ledger absent in inspected Oracle runner | Central checksum and promotion state. No target ledger in reviewed execution |

Evidence: P-AF-ROUTES, P-AF-NAV, P-AF-SETS, P-AF-PROMOTE, P-AF-ENV, P-AF-INVENTORY. Execution: AF-PROM, AF-GATE, AF-GROUP.

### OceanBase ODC

| Capability | Bytebase reference | Candidate |
|---|---|---|
| Central web console | YES | YES |
| Project/application model | YES | YES. Projects own databases and members |
| Database instance inventory | YES | YES. Registered datasources with connection properties |
| Environment model | YES | YES. Separate environment objects and database labels |
| Schema/database inventory | YES | YES. Physical and logical database records |
| Change request | YES | YES. Project change tickets |
| Change version/release | YES | PARTIAL. Ticket identity and SQL files. Immutable versioned release model not established |
| Review | YES | YES. SQL checks and risk rules |
| Approval | YES | YES. Configurable workflow approval |
| Deployment/rollout | YES | YES. Ordered database batches and child execution records |
| Multi-environment promotion | YES | PARTIAL. Ordered environment-labelled targets with manual or automatic batch continuation |
| Deployment history | YES | YES. Parent and child ticket results |
| Audit | YES | YES. Operation records |
| RBAC | YES | YES. Project admins, DBAs, and Developers inherit all project databases. Participants need explicit grants. Oracle GRANT remains separate |
| Git integration | YES | PARTIAL. Project repository registration API exists. Native commit-to-ticket or merge-to-deploy automation not established |
| CI/CD integration | YES | PARTIAL. Session API can create datasources and flow tickets. CI write and Oracle execution paths remain unverified |
| Oracle | YES | YES by source. Oracle plugin and ojdbc8 driver are present in deployed 4.4.1. No external Oracle target connected. Embedded OCP frontend excludes Oracle |
| Migration state | Central revisions. Target ledger absent in inspected Oracle runner | Central task/batch state. No target migration ledger in reviewed execution |

Evidence: P-ODC-PROJECT, P-ODC-ENV, P-ODC-DATABASE, P-ODC-QUEUE, P-ODC-STRATEGY, P-ODC-BATCH-EXEC, P-ODC-EXEC, P-ODC-ORACLE-UI. P-ODC-GIT-API, P-ODC-DATASOURCE-API, P-ODC-FLOW-API, P-ODC-ROLE-INHERITANCE, P-ODC-DB-PERMISSION-SERVICE. Runtime: [ODC evaluation](ODC-EVALUATION.md).

### Archery

| Capability | Bytebase reference | Candidate |
|---|---|---|
| Central web console | YES | YES |
| Project/application model | YES | PARTIAL. Resource groups, not application release projects |
| Database instance inventory | YES | YES |
| Environment model | YES | PARTIAL. Instance classification, no ordered release environments established |
| Schema/database inventory | YES | YES |
| Change request | YES | YES. SQL workflow tickets |
| Change version/release | YES | NO. Immutable versioned release model not established |
| Review | YES | YES |
| Approval | YES | YES |
| Deployment/rollout | YES | PARTIAL. Ticket execution |
| Multi-environment promotion | YES | NO. Same approved release promotion not established |
| Deployment history | YES | PARTIAL. Central ticket results |
| Audit | YES | YES |
| RBAC | YES | YES |
| Git integration | YES | UNKNOWN |
| CI/CD integration | YES | PARTIAL. API/command integration requires verification |
| Oracle | YES | YES |
| Migration state | Central revisions. Target ledger absent in inspected Oracle runner | Central workflow results. No target migration ledger |

Evidence: P-AR-NAV, P-AR-ROUTES. Execution: AR-STATE, AR-EXEC, AR-ORA.

### SQLE + DMS Community

| Capability | Bytebase reference | Candidate |
|---|---|---|
| Central web console | YES | YES. Separate frontend referenced by deployment build |
| Project/application model | YES | PARTIAL. Default/project metadata. Community blocks project creation and changes |
| Database instance inventory | YES | PARTIAL. Per-project connections. Global inventory endpoints are Enterprise |
| Environment model | YES | PARTIAL. Environment tags, no free release-stage model established |
| Schema/database inventory | YES | PARTIAL. DMS inventory. Oracle coverage not verified |
| Change request | YES | YES |
| Change version/release | YES | NO. Community controller rejects SQL versions |
| Review | YES | YES |
| Approval | YES | YES. SQL workflow |
| Deployment/rollout | YES | PARTIAL. Individual workflows. Batch release is enterprise |
| Multi-environment promotion | YES | NO. Version dependencies and batch releases are enterprise |
| Deployment history | YES | PARTIAL. Workflow execution records |
| Audit | YES | PARTIAL. Edition coverage requires further review |
| RBAC | YES | YES. DMS permissions |
| Git integration | YES | UNKNOWN |
| CI/CD integration | YES | PARTIAL. Workflow APIs. Version release endpoints are enterprise |
| Oracle | YES | PARTIAL. Public Oracle plugin executes SQL. Plugin license coverage UNKNOWN |
| Migration state | Central revisions. Target ledger absent in inspected Oracle runner | Central workflow records. Target ledger not established |

Evidence: P-SQLE-CE, P-SQLE-VERSION, P-DMS-PROJECT-CE, P-DMS-PROJECT-MODEL, P-DMS-INVENTORY-CE, P-DMS-ENV, P-DMS-FRONTEND, P-SQLE-ORACLE.

### Open Migration

| Capability | Bytebase reference | Candidate |
|---|---|---|
| Central web console | YES | YES |
| Project/application model | YES | NO |
| Database instance inventory | YES | PARTIAL. Flat connection inventory |
| Environment model | YES | NO |
| Schema/database inventory | YES | PARTIAL. Registered databases, no estate discovery hierarchy |
| Change request | YES | PARTIAL. Upload and execute files |
| Change version/release | YES | PARTIAL. Filenames, no stored checksum |
| Review | YES | NO |
| Approval | YES | NO |
| Deployment/rollout | YES | PARTIAL. Migration service |
| Multi-environment promotion | YES | NO |
| Deployment history | YES | PARTIAL. Target filenames and UI status |
| Audit | YES | NO |
| RBAC | YES | NO |
| Git integration | YES | YES. GitHub and GitLab retrieval |
| CI/CD integration | YES | PARTIAL. APIs, no governed release pipeline |
| Oracle | YES | NO |
| Migration state | Central revisions. Target ledger absent in inspected Oracle runner | Filename target tracking for supported engines. No Oracle |

Evidence: P-OM-NAV. Execution: OM-ENG, OM-STATE, OM-RUN, OM-AUTH.

### SchemaPilot

| Capability | Bytebase reference | Candidate |
|---|---|---|
| Central web console | YES | YES |
| Project/application model | YES | NO |
| Database instance inventory | YES | PARTIAL. Saved connection configuration |
| Environment model | YES | NO |
| Schema/database inventory | YES | PARTIAL. Current database connection |
| Change request | YES | PARTIAL. Script editor |
| Change version/release | YES | PARTIAL. Custom Flyway-shaped history writes |
| Review | YES | NO |
| Approval | YES | NO |
| Deployment/rollout | YES | PARTIAL. Direct script execution |
| Multi-environment promotion | YES | NO |
| Deployment history | YES | PARTIAL. Script history |
| Audit | YES | NO |
| RBAC | YES | NO |
| Git integration | YES | UNKNOWN |
| CI/CD integration | YES | UNKNOWN |
| Oracle | YES | NO |
| Migration state | Central revisions. Target ledger absent in inspected Oracle runner | Custom target history. No actual Flyway invocation or Oracle |

Evidence: P-SP-UI. Execution and license: SP-L, SP-EXEC, SP-DRIVERS.

### Yearning

| Capability | Bytebase reference | Candidate |
|---|---|---|
| Central web console | YES | YES |
| Project/application model | YES | PARTIAL. Groups and workflow users |
| Database instance inventory | YES | YES. MySQL datasource management |
| Environment model | YES | UNKNOWN. No release ladder established |
| Schema/database inventory | YES | PARTIAL. Query/schema scope |
| Change request | YES | YES |
| Change version/release | YES | NO. Versioned release artifact not established |
| Review | YES | YES |
| Approval | YES | YES |
| Deployment/rollout | YES | PARTIAL. SQL ticket execution |
| Multi-environment promotion | YES | NO. Immutable release promotion not established |
| Deployment history | YES | PARTIAL. SQL ticket results |
| Audit | YES | YES |
| RBAC | YES | YES |
| Git integration | YES | UNKNOWN |
| CI/CD integration | YES | UNKNOWN |
| Oracle | YES | NO |
| Migration state | Central revisions. Target ledger absent in inspected Oracle runner | Central SQL records. No Oracle ledger |

Evidence: YE-L, YE-SCOPE. Unestablished release capabilities remain explicit.

### dbward core

| Capability | Bytebase reference | Candidate |
|---|---|---|
| Central web console | YES | UNKNOWN. Inspected source does not establish a web console |
| Project/application model | YES | PARTIAL. Connection/team configuration |
| Database instance inventory | YES | PARTIAL. Connections |
| Environment model | YES | PARTIAL. Connection configuration |
| Schema/database inventory | YES | PARTIAL. Supported-engine introspection |
| Change request | YES | YES. Server approval requests |
| Change version/release | YES | PARTIAL. Migration files and version identifiers |
| Review | YES | PARTIAL. Policies |
| Approval | YES | YES. Approval path |
| Deployment/rollout | YES | PARTIAL. Server execution and migration component |
| Multi-environment promotion | YES | UNKNOWN |
| Deployment history | YES | YES. Central records |
| Audit | YES | YES |
| RBAC | YES | PARTIAL. Paid identity and policy boundaries |
| Git integration | YES | UNKNOWN |
| CI/CD integration | YES | UNKNOWN |
| Oracle | YES | NO. PostgreSQL/MySQL scope |
| Migration state | Central revisions. Target ledger absent in inspected Oracle runner | Supported-engine version tracking. Target checksum validation not established |

Evidence: WARD-L, WARD-SCOPE, WARD-BOUNDARY. See additional-candidates.md for source limitations.

### CloudBeaver Community

| Capability | Bytebase reference | Candidate |
|---|---|---|
| Central web console | YES | YES |
| Project/application model | YES | NO. SQL workspace is not an application release project |
| Database instance inventory | YES | PARTIAL. Connection inventory |
| Environment model | YES | NO. Ordered release lifecycle not established |
| Schema/database inventory | YES | YES. Database object browser |
| Change request | YES | NO. Governed change request not established |
| Change version/release | YES | NO |
| Review | YES | NO. Change review not established |
| Approval | YES | NO |
| Deployment/rollout | YES | PARTIAL. Interactive SQL execution |
| Multi-environment promotion | YES | NO |
| Deployment history | YES | PARTIAL. Query history |
| Audit | YES | UNKNOWN. Free central accountability coverage |
| RBAC | YES | PARTIAL. Edition boundaries |
| Git integration | YES | UNKNOWN |
| CI/CD integration | YES | UNKNOWN |
| Oracle | YES | YES. Oracle connection support |
| Migration state | Central revisions. Target ledger absent in inspected Oracle runner | No target migration ledger or release state |

Evidence: CB-L, CB-ORA. See additional-candidates.md for source limitations.

### NineData Community repository

| Capability | Bytebase reference | Candidate |
|---|---|---|
| Central web console | YES | UNKNOWN. Public repository supplies documentation only |
| Project/application model | YES | UNKNOWN |
| Database instance inventory | YES | Vendor-described datasource inventory. Source absent |
| Environment model | YES | UNKNOWN |
| Schema/database inventory | YES | Vendor-described inventory. Source absent |
| Change request | YES | Vendor-described SQL workflows. Source absent |
| Change version/release | YES | UNKNOWN |
| Review | YES | Vendor-described. Source absent |
| Approval | YES | Vendor-described. Source absent |
| Deployment/rollout | YES | Vendor-described. Source absent |
| Multi-environment promotion | YES | UNKNOWN |
| Deployment history | YES | UNKNOWN |
| Audit | YES | Vendor-described. Source absent |
| RBAC | YES | UNKNOWN |
| Git integration | YES | UNKNOWN |
| CI/CD integration | YES | UNKNOWN |
| Oracle | YES | UNKNOWN for inspectable free source |
| Migration state | Central revisions. Target ledger absent in inspected Oracle runner | UNKNOWN. No implementation source or license in inspected repository |

Evidence: P-NINE-DOC. The inspected source tree contains README.md, README_CN.md, and release_note.md.

All `P-` IDs resolve in [PRODUCT-EVIDENCE.md](PRODUCT-EVIDENCE.md#source-references).
Other IDs resolve in [EVIDENCE.md](EVIDENCE.md#source-references).
The [frontend record](UI-EVIDENCE.md) supports the shortlist classifications.
The [fork record](FORK-SEARCH.md) separates inherited platform code from independent development.

## Decision

A free OSS Oracle platform with substantial Bytebase-like structure exists: OceanBase ODC.
An exact replacement with all requested release and recovery controls was not verified.
Evaluate ODC's existing workflow first. Evaluate AccessFlow's existing schema promotion second.
Keep Archery and SQLE Community as SQL governance references.
Consider engine composition only if the existing platform evaluation fails the accepted workflow or recovery requirements.

## Bytebase API/UI POC, 04/10/2026

[Bytebase mới: 45 kết quả](BYTEBASE-ORACLE-POC-RESULTS.md) và [đối chiếu ODC](BYTEBASE-ODC-COMPARISON.md).
Kết quả: 17 PASS, 14 PARTIAL, 4 FAIL, 3 BLOCKED, 7 NOT_RUN. Runtime 3.22.1/FREE, Oracle 26ai.
Native version/replay và execution-role separation có bằng chứng tốt hơn ODC.
Procedure INVALID, SQL Review ERROR và early mockPROD vẫn là các lỗi cần xử lý.
Approval/audit bị giới hạn FREE; chưa đánh giá Enterprise hoặc controlled recovery.
Có 11 ảnh Selenium thật, API evidence và Oracle Thin hậu kiểm tại [portal](https://db-poc.apps.drgdevlab.com/).
Bằng chứng mới dùng `evidence/bytebase-poc-*.json`. Lịch sử P03/P04 vẫn FAIL, được giữ riêng.
