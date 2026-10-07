"""Create the product comparison. No application or database execution occurs."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
caps=['Central web console','Project/application model','Database instance inventory','Environment model','Schema/database inventory','Change request','Change version/release','Review','Approval','Deployment/rollout','Multi-environment promotion','Deployment history','Audit','RBAC','Git integration','CI/CD integration','Oracle','Migration state']
profiles={
'AccessFlow': ['YES','PARTIAL. Pipelines and organizations, no first-class project estate','PARTIAL. Datasource connections, no separate instance hierarchy','YES. Ordered pipeline environments','PARTIAL. Per-datasource schema browser','YES. Requests and schema change sets','YES. Central change-set identity and frozen checksum','YES','YES','YES. Schema promotion executes database requests','YES. Lower-environment success guard','YES. Promotion history and request results','YES','YES','YES. SCM connectors and repository references','YES. Documented CI/API paths','PARTIAL. Oracle JDBC exists. Schema script gate limits scope','Central checksum and promotion state. No target ledger in reviewed execution'],
'OceanBase ODC': ['YES','YES. Projects own databases and members','YES. Registered datasources with connection properties','YES. Separate environment objects and database labels','YES. Physical and logical database records','YES. Project change tickets','PARTIAL. Ticket identity and SQL files. Immutable versioned release model not established','YES. SQL checks and risk rules','YES. Configurable workflow approval','YES. Ordered database batches and child execution records','PARTIAL. Ordered environment-labelled targets with manual or automatic batch continuation','YES. Parent and child ticket results','YES. Operation records','YES. Users, roles, and project membership','UNKNOWN. README roadmap is insufficient evidence','PARTIAL. Integration/API model. Native GitLab/Jenkins release pipeline not established','YES. Standalone Oracle plugin and multi-database capability. Embedded OCP frontend excludes Oracle','Central task/batch state. No target migration ledger in reviewed execution'],
'Archery': ['YES','PARTIAL. Resource groups, not application release projects','YES','PARTIAL. Instance classification, no ordered release environments established','YES','YES. SQL workflow tickets','NO. Immutable versioned release model not established','YES','YES','PARTIAL. Ticket execution','NO. Same approved release promotion not established','PARTIAL. Central ticket results','YES','YES','UNKNOWN','PARTIAL. API/command integration requires verification','YES','Central workflow results. No target migration ledger'],
'SQLE + DMS Community': ['YES. Separate frontend referenced by deployment build','PARTIAL. Default/project metadata. Community blocks project creation and changes','PARTIAL. Per-project connections. Global inventory endpoints are Enterprise','PARTIAL. Environment tags, no free release-stage model established','PARTIAL. DMS inventory. Oracle coverage not verified','YES','NO. Community controller rejects SQL versions','YES','YES. SQL workflow','PARTIAL. Individual workflows. Batch release is enterprise','NO. Version dependencies and batch releases are enterprise','PARTIAL. Workflow execution records','PARTIAL. Edition coverage requires further review','YES. DMS permissions','UNKNOWN','PARTIAL. Workflow APIs. Version release endpoints are enterprise','PARTIAL. Public Oracle plugin executes SQL. Plugin license coverage UNKNOWN','Central workflow records. Target ledger not established'],
'Open Migration': ['YES','NO','PARTIAL. Flat connection inventory','NO','PARTIAL. Registered databases, no estate discovery hierarchy','PARTIAL. Upload and execute files','PARTIAL. Filenames, no stored checksum','NO','NO','PARTIAL. Migration service','NO','PARTIAL. Target filenames and UI status','NO','NO','YES. GitHub and GitLab retrieval','PARTIAL. APIs, no governed release pipeline','NO','Filename target tracking for supported engines. No Oracle'],
'SchemaPilot': ['YES','NO','PARTIAL. Saved connection configuration','NO','PARTIAL. Current database connection','PARTIAL. Script editor','PARTIAL. Custom Flyway-shaped history writes','NO','NO','PARTIAL. Direct script execution','NO','PARTIAL. Script history','NO','NO','UNKNOWN','UNKNOWN','NO','Custom target history. No actual Flyway invocation or Oracle'],
'Yearning': ['YES','PARTIAL. Groups and workflow users','YES. MySQL datasource management','UNKNOWN. No release ladder established','PARTIAL. Query/schema scope','YES','NO. Versioned release artifact not established','YES','YES','PARTIAL. SQL ticket execution','NO. Immutable release promotion not established','PARTIAL. SQL ticket results','YES','YES','UNKNOWN','UNKNOWN','NO','Central SQL records. No Oracle ledger'],
'dbward core': ['UNKNOWN. Inspected source does not establish a web console','PARTIAL. Connection/team configuration','PARTIAL. Connections','PARTIAL. Connection configuration','PARTIAL. Supported-engine introspection','YES. Server approval requests','PARTIAL. Migration files and version identifiers','PARTIAL. Policies','YES. Approval path','PARTIAL. Server execution and migration component','UNKNOWN','YES. Central records','YES','PARTIAL. Paid identity and policy boundaries','UNKNOWN','UNKNOWN','NO. PostgreSQL/MySQL scope','Supported-engine version tracking. Target checksum validation not established'],
'CloudBeaver Community': ['YES','NO. SQL workspace is not an application release project','PARTIAL. Connection inventory','NO. Ordered release lifecycle not established','YES. Database object browser','NO. Governed change request not established','NO','NO. Change review not established','NO','PARTIAL. Interactive SQL execution','NO','PARTIAL. Query history','UNKNOWN. Free central accountability coverage','PARTIAL. Edition boundaries','UNKNOWN','UNKNOWN','YES. Oracle connection support','No target migration ledger or release state'],
'NineData Community repository': ['UNKNOWN. Public repository supplies documentation only','UNKNOWN','Vendor-described datasource inventory. Source absent','UNKNOWN','Vendor-described inventory. Source absent','Vendor-described SQL workflows. Source absent','UNKNOWN','Vendor-described. Source absent','Vendor-described. Source absent','Vendor-described. Source absent','UNKNOWN','UNKNOWN','Vendor-described. Source absent','UNKNOWN','UNKNOWN','UNKNOWN','UNKNOWN for inspectable free source','UNKNOWN. No implementation source or license in inspected repository']
}
refs={
'AccessFlow':'P-AF-ROUTES, P-AF-NAV, P-AF-SETS, P-AF-PROMOTE, P-AF-ENV, P-AF-INVENTORY. Execution: AF-PROM, AF-GATE, AF-GROUP.',
'OceanBase ODC':'P-ODC-PROJECT, P-ODC-ENV, P-ODC-DATABASE, P-ODC-QUEUE, P-ODC-STRATEGY, P-ODC-BATCH-EXEC, P-ODC-EXEC, P-ODC-ORACLE-UI.',
'Archery':'P-AR-NAV, P-AR-ROUTES. Execution: AR-STATE, AR-EXEC, AR-ORA.',
'SQLE + DMS Community':'P-SQLE-CE, P-SQLE-VERSION, P-DMS-PROJECT-CE, P-DMS-PROJECT-MODEL, P-DMS-INVENTORY-CE, P-DMS-ENV, P-DMS-FRONTEND, P-SQLE-ORACLE.',
'Open Migration':'P-OM-NAV. Execution: OM-ENG, OM-STATE, OM-RUN, OM-AUTH.',
'SchemaPilot':'P-SP-UI. Execution and license: SP-L, SP-EXEC, SP-DRIVERS.',
'Yearning':'YE-L, YE-SCOPE. Unestablished release capabilities remain explicit.',
'dbward core':'WARD-L, WARD-SCOPE, WARD-BOUNDARY. See additional-candidates.md for source limitations.',
'CloudBeaver Community':'CB-L, CB-ORA. See additional-candidates.md for source limitations.',
'NineData Community repository':'P-NINE-DOC. The inspected source tree contains README.md, README_CN.md, and release_note.md.'
}
profiles['OceanBase ODC'][13]='YES. Project admins, DBAs, and Developers inherit all project databases. Participants need explicit grants. Oracle GRANT remains separate'
profiles['OceanBase ODC'][14]='PARTIAL. Project repository registration API exists. Native commit-to-ticket or merge-to-deploy automation not established'
profiles['OceanBase ODC'][15]='PARTIAL. Session API can create datasources and flow tickets. CI write and Oracle execution paths remain unverified'
profiles['OceanBase ODC'][16]='YES by source. Oracle plugin and ojdbc8 driver are present in deployed 4.4.1. No external Oracle target connected. Embedded OCP frontend excludes Oracle'
refs['OceanBase ODC']+=' P-ODC-GIT-API, P-ODC-DATASOURCE-API, P-ODC-FLOW-API, P-ODC-ROLE-INHERITANCE, P-ODC-DB-PERMISSION-SERVICE. Runtime: [ODC evaluation](ODC-EVALUATION.md).'
text='''# Product model comparison

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
Deployment and authenticated GET checks succeeded. Oracle workflow acceptance remains NOT RUN.
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
'''
for name,values in profiles.items():
 assert len(values)==18
 text+='\n### '+name+'\n\n| Capability | Bytebase reference | Candidate |\n|---|---|---|\n'
 for c,v in zip(caps,values):text+=f'| {c} | '+('Central revisions. Target ledger absent in inspected Oracle runner' if c=='Migration state' else 'YES')+f' | {v} |\n'
 text+='\nEvidence: '+refs[name]+'\n'
text+='''
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
'''
(ROOT/'PRODUCT-MODEL.md').write_text(text)
print('Created ten 18-capability comparisons and independent fit scores')
