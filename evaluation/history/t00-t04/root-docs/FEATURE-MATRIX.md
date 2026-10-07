# Desired and optional feature matrix

## Cập nhật coverage T01–T03, 04/10/2026

[Criteria](evaluation/criteria.csv) giữ nguyên 45 expected, thêm F01–F12.
[Feature evidence](evaluation/feature-matrix.csv) tách DOC/SOURCE, runtime lịch sử và runtime mới NOT_RUN.
[Shortlist](evaluation/shortlist.md) không tính điểm tổng khi coverage khác nhau.
Các YES/PARTIAL phía dưới là feature fit của snapshot cũ, không là nghiệm thu Oracle runtime.

This register preserves twenty original candidates and adds OceanBase ODC.
The [product comparison](PRODUCT-MODEL.md) adds SQLE/DMS, frontend evidence, and separate platform scores.
This register does not control the revised platform shortlist.

The tables evaluate every SHOULD and Nice to Have item in the supplied brief.
They describe the inspected free edition or explicitly pinned source version.
YES requires source or official documentation evidence.
PARTIAL identifies a scope limit or external integration requirement.
NO identifies an absent central capability or an explicit edition boundary.
UNKNOWN identifies a feature that this review could not establish.

A positive feature entry does not establish Oracle support for that feature.
For example, Archery schema comparison primarily concerns MySQL tooling.
ODC deployment and authenticated GET endpoints received runtime inspection. Oracle 26ai API/UI results are recorded separately in ODC-ORACLE-POC-RESULTS.md.
The [ODC evaluation](ODC-EVALUATION.md) records the scope and dated runtime evidence.

An environment model means stored environment identities or selectable engine contexts.
PARTIAL engine environments require an external inventory and promotion controller.
Git integration is PARTIAL when external pipelines provide versioned files.
Generic command invocation does not establish a native GitLab or Jenkins integration.
CLI logs are PARTIAL deployment logs because they require central collection.
Backup and disaster recovery columns concern the central service.
Engine target recovery appears separately in REPORT.md and the Oracle plan.

## Organization and review

| Project | Web UI | Database inventory | Application/project organization | Environment model | Review workflow | Approval workflow | RBAC | Separation of duties |
|---|---|---|---|---|---|---|---|---|
| Bytebase Community | YES | YES | YES | YES | YES | NO | YES | PARTIAL |
| OceanBase ODC | YES | YES | YES | YES | YES | YES | YES | PARTIAL |
| AccessFlow | YES | YES | PARTIAL | YES | YES | YES | YES | YES |
| D-Band DRM | NO | PARTIAL | PARTIAL | PARTIAL | NO | NO | NO | NO |
| Open Migration | YES | YES | NO | NO | NO | NO | NO | NO |
| SchemaPilot | YES | YES | NO | NO | NO | NO | NO | NO |
| Flyway UI | YES | NO | NO | NO | NO | NO | NO | NO |
| Flyway Play | PARTIAL | NO | NO | PARTIAL | NO | NO | NO | NO |
| Liquibase Community 5.x | NO | NO | NO | PARTIAL | NO | NO | NO | NO |
| Liquibase 4.33.0 | NO | NO | NO | PARTIAL | NO | NO | NO | NO |
| Flyway Community | NO | NO | NO | PARTIAL | NO | NO | NO | NO |
| Sqitch | NO | NO | NO | PARTIAL | NO | NO | NO | NO |
| Atlas public OSS | NO | NO | NO | PARTIAL | NO | NO | NO | NO |
| Yearning | YES | YES | PARTIAL | PARTIAL | YES | YES | YES | PARTIAL |
| Archery | YES | YES | PARTIAL | PARTIAL | YES | YES | YES | PARTIAL |
| Tareya derivative | YES | YES | PARTIAL | PARTIAL | YES | YES | YES | PARTIAL |
| .NET dbdeploy | NO | NO | NO | NO | NO | NO | NO | NO |
| DbMaintain | NO | NO | NO | NO | NO | NO | NO | NO |
| dbpm | NO | NO | PARTIAL | PARTIAL | NO | NO | NO | NO |
| dbward core | UNKNOWN | YES | PARTIAL | PARTIAL | YES | YES | PARTIAL | PARTIAL |
| CloudBeaver Community | YES | YES | NO | NO | NO | NO | PARTIAL | PARTIAL |

## Source, automation, and identity

| Project | Git integration | GitLab integration | Jenkins integration | CI/CD API | REST API | SSO | OIDC | LDAP |
|---|---|---|---|---|---|---|---|---|
| Bytebase Community | YES | PARTIAL | PARTIAL | YES | YES | NO | NO | NO |
| OceanBase ODC | PARTIAL | PARTIAL | PARTIAL | PARTIAL | YES | UNKNOWN | UNKNOWN | UNKNOWN |
| AccessFlow | PARTIAL | YES | PARTIAL | YES | YES | YES | YES | UNKNOWN |
| D-Band DRM | PARTIAL | PARTIAL | PARTIAL | NO | NO | NO | NO | NO |
| Open Migration | YES | YES | PARTIAL | PARTIAL | YES | NO | NO | NO |
| SchemaPilot | UNKNOWN | UNKNOWN | UNKNOWN | PARTIAL | YES | NO | NO | NO |
| Flyway UI | PARTIAL | PARTIAL | PARTIAL | NO | NO | NO | NO | NO |
| Flyway Play | PARTIAL | PARTIAL | PARTIAL | NO | NO | NO | NO | NO |
| Liquibase Community 5.x | PARTIAL | PARTIAL | PARTIAL | NO | NO | NO | NO | NO |
| Liquibase 4.33.0 | PARTIAL | PARTIAL | PARTIAL | NO | NO | NO | NO | NO |
| Flyway Community | PARTIAL | PARTIAL | PARTIAL | NO | NO | NO | NO | NO |
| Sqitch | PARTIAL | PARTIAL | PARTIAL | NO | NO | NO | NO | NO |
| Atlas public OSS | PARTIAL | PARTIAL | PARTIAL | NO | NO | NO | NO | NO |
| Yearning | UNKNOWN | UNKNOWN | UNKNOWN | PARTIAL | YES | YES | YES | YES |
| Archery | UNKNOWN | UNKNOWN | PARTIAL | YES | YES | YES | YES | YES |
| Tareya derivative | UNKNOWN | UNKNOWN | PARTIAL | PARTIAL | YES | UNKNOWN | UNKNOWN | UNKNOWN |
| .NET dbdeploy | PARTIAL | PARTIAL | PARTIAL | NO | NO | NO | NO | NO |
| DbMaintain | PARTIAL | PARTIAL | PARTIAL | NO | NO | NO | NO | NO |
| dbpm | PARTIAL | PARTIAL | PARTIAL | NO | NO | NO | NO | NO |
| dbward core | PARTIAL | UNKNOWN | UNKNOWN | YES | YES | NO | NO | UNKNOWN |
| CloudBeaver Community | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

## Operations

| Project | Audit logs | Vault/external secrets | Deployment logs | Notifications | High availability | Central backup/restore | Disaster recovery |
|---|---|---|---|---|---|---|---|
| Bytebase Community | NO | NO | YES | YES | UNKNOWN | UNKNOWN | UNKNOWN |
| OceanBase ODC | YES | UNKNOWN | YES | UNKNOWN | PARTIAL | UNKNOWN | UNKNOWN |
| AccessFlow | YES | YES | YES | YES | PARTIAL | YES | YES |
| D-Band DRM | NO | UNKNOWN | PARTIAL | UNKNOWN | NO | NO | NO |
| Open Migration | NO | UNKNOWN | PARTIAL | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SchemaPilot | NO | UNKNOWN | PARTIAL | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Flyway UI | NO | NO | PARTIAL | NO | NO | NO | NO |
| Flyway Play | NO | UNKNOWN | PARTIAL | UNKNOWN | NO | NO | NO |
| Liquibase Community 5.x | NO | UNKNOWN | PARTIAL | UNKNOWN | NO | NO | NO |
| Liquibase 4.33.0 | NO | UNKNOWN | PARTIAL | UNKNOWN | NO | NO | NO |
| Flyway Community | NO | UNKNOWN | PARTIAL | UNKNOWN | NO | NO | NO |
| Sqitch | NO | UNKNOWN | PARTIAL | UNKNOWN | NO | NO | NO |
| Atlas public OSS | NO | UNKNOWN | PARTIAL | UNKNOWN | NO | NO | NO |
| Yearning | YES | UNKNOWN | YES | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Archery | YES | UNKNOWN | YES | YES | UNKNOWN | UNKNOWN | UNKNOWN |
| Tareya derivative | PARTIAL | UNKNOWN | YES | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| .NET dbdeploy | NO | UNKNOWN | PARTIAL | UNKNOWN | NO | NO | NO |
| DbMaintain | NO | UNKNOWN | PARTIAL | UNKNOWN | NO | NO | NO |
| dbpm | NO | UNKNOWN | PARTIAL | UNKNOWN | NO | NO | NO |
| dbward core | YES | UNKNOWN | YES | YES | UNKNOWN | UNKNOWN | UNKNOWN |
| CloudBeaver Community | UNKNOWN | UNKNOWN | PARTIAL | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

## Optional execution and schema features

| Project | Flyway integration | Liquibase integration | SQLPlus integration | Schema diff | Drift detection | SQL review/lint |
|---|---|---|---|---|---|---|
| Bytebase Community | NO | NO | NO | YES | PARTIAL | YES |
| OceanBase ODC | NO | NO | NO | PARTIAL | UNKNOWN | YES |
| AccessFlow | NO | NO | NO | PARTIAL | PARTIAL | PARTIAL |
| D-Band DRM | PARTIAL | PARTIAL | YES | UNKNOWN | UNKNOWN | UNKNOWN |
| Open Migration | NO | NO | NO | UNKNOWN | UNKNOWN | NO |
| SchemaPilot | NO | NO | NO | UNKNOWN | UNKNOWN | NO |
| Flyway UI | YES | NO | UNKNOWN | UNKNOWN | UNKNOWN | NO |
| Flyway Play | YES | NO | NO | NO | NO | NO |
| Liquibase Community 5.x | NO | YES | NO | YES | PARTIAL | UNKNOWN |
| Liquibase 4.33.0 | NO | YES | NO | YES | PARTIAL | UNKNOWN |
| Flyway Community | YES | NO | NO | NO | NO | UNKNOWN |
| Sqitch | NO | NO | YES | NO | PARTIAL | NO |
| Atlas public OSS | NO | NO | NO | YES | PARTIAL | UNKNOWN |
| Yearning | NO | NO | NO | UNKNOWN | UNKNOWN | YES |
| Archery | NO | NO | NO | PARTIAL | UNKNOWN | PARTIAL |
| Tareya derivative | NO | NO | NO | PARTIAL | UNKNOWN | PARTIAL |
| .NET dbdeploy | NO | NO | UNKNOWN | NO | NO | NO |
| DbMaintain | NO | NO | YES | NO | NO | NO |
| dbpm | NO | NO | YES | UNKNOWN | UNKNOWN | UNKNOWN |
| dbward core | NO | NO | NO | PARTIAL | PARTIAL | YES |
| CloudBeaver Community | NO | NO | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

## Optional governance and deployment features

| Project | Policy as code | Release promotion | Environment promotion | SIEM integration | Terraform provider | Kubernetes operator/Helm |
|---|---|---|---|---|---|---|
| Bytebase Community | PARTIAL | YES | YES | NO | YES | UNKNOWN |
| OceanBase ODC | UNKNOWN | PARTIAL | PARTIAL | UNKNOWN | UNKNOWN | UNKNOWN |
| AccessFlow | YES | YES | YES | YES | YES | YES |
| D-Band DRM | UNKNOWN | PARTIAL | PARTIAL | NO | NO | NO |
| Open Migration | NO | NO | NO | NO | NO | UNKNOWN |
| SchemaPilot | NO | NO | NO | NO | NO | UNKNOWN |
| Flyway UI | NO | NO | NO | NO | NO | NO |
| Flyway Play | NO | PARTIAL | PARTIAL | NO | NO | NO |
| Liquibase Community 5.x | PARTIAL | PARTIAL | PARTIAL | NO | UNKNOWN | UNKNOWN |
| Liquibase 4.33.0 | PARTIAL | PARTIAL | PARTIAL | NO | UNKNOWN | UNKNOWN |
| Flyway Community | NO | PARTIAL | PARTIAL | NO | UNKNOWN | UNKNOWN |
| Sqitch | PARTIAL | PARTIAL | PARTIAL | NO | UNKNOWN | UNKNOWN |
| Atlas public OSS | PARTIAL | PARTIAL | PARTIAL | NO | UNKNOWN | UNKNOWN |
| Yearning | UNKNOWN | NO | NO | UNKNOWN | UNKNOWN | UNKNOWN |
| Archery | UNKNOWN | NO | NO | UNKNOWN | UNKNOWN | UNKNOWN |
| Tareya derivative | UNKNOWN | NO | NO | UNKNOWN | UNKNOWN | UNKNOWN |
| .NET dbdeploy | NO | NO | NO | NO | NO | NO |
| DbMaintain | NO | NO | NO | NO | NO | NO |
| dbpm | UNKNOWN | PARTIAL | PARTIAL | NO | NO | UNKNOWN |
| dbward core | YES | PARTIAL | PARTIAL | PARTIAL | UNKNOWN | UNKNOWN |
| CloudBeaver Community | UNKNOWN | NO | NO | UNKNOWN | UNKNOWN | UNKNOWN |

## Evidence and feature boundaries

| Project group | Evidence and interpretation |
|---|---|
| Bytebase | BB-PLAN and BB-GATES establish free features and paid approval, identity, audit, and secret boundaries. Free Terraform is explicitly listed. |
| OceanBase ODC | P-ODC-PROJECT, P-ODC-ENV, P-ODC-GIT-API, P-ODC-FLOW-API, P-ODC-ROLE-INHERITANCE, P-ODC-HA-DOC, and P-ODC-SCHEMA-DIFF-DOC. Git registration exists. CI writes remain unverified. HA deployment is documented, but this deployment uses single replicas. The schema comparison guide lists OceanBase tenants and MySQL, not native Oracle. Unreviewed identity, backup, notification, and infrastructure integrations remain UNKNOWN. |
| AccessFlow | AF-IAC, AF-SSO, AF-VAULT, AF-AUDIT, AF-SIEM, AF-REST, AF-CI, AF-DRIFT, and AF-DISASTER. Flyway only manages its internal PostgreSQL schema. |
| DRM | DRM-LOCAL, DRM-FW, DRM-LB, and DRM-SQLPLUS. Engine adapters generate scripts. They do not establish normal engine locking and validation. |
| Open Migration / SchemaPilot | OM-ENG, OM-META, OM-AUTH, SP-DRIVERS, and SP-EXEC. Small server implementations have no established multi-user governance. |
| Flyway UI / Play | UI-DEPS, UI-SERVLET, PLAY-SCOPE, and PLAY-DEPS. These are application components, not independent central services. |
| Flyway / Liquibase / Sqitch | FW-ORA, LB4-STATE, SQ-STATE, SQ-SQLPLUS, and official engine docs. Engines provide execution, not central identity or approvals. |
| Atlas | AT-DRIVERS and official compatibility. Public OSS features do not establish Oracle support. |
| Yearning | YE-SCOPE and YE-IDENTITY. LDAP and OIDC routes exist. Runtime identity and duty separation remain unverified. |
| Archery | AR-DOC, AR-IDENTITY, AR-LDAP, AR-API, and AR-STATE. SQL review and schema comparison have engine-specific limits. |
| Tareya derivative | FORK-EXEC and inherited repository files. Independent identity and operations verification remain incomplete. |
| dbdeploy / DbMaintain / dbpm | DEP-STATE, MAINT-SCOPE, PM-SCOPE, PM-LIMITS, and official DbMaintain docs. These are engine or command projects. |
| dbward | WARD-REST, WARD-PLAN, WARD-RUN, and WARD-STATE. OIDC and group authorization require commercial code. No Oracle driver exists in the reviewed implementation. |
| CloudBeaver | CB-SCOPE and CB-ORA. Shared SQL editing does not establish release governance. Unreviewed commercial-edition features remain UNKNOWN. |

Original IDs resolve in [EVIDENCE.md](EVIDENCE.md#source-references). ODC IDs resolve in [PRODUCT-EVIDENCE.md](PRODUCT-EVIDENCE.md#source-references).
The [main report](REPORT.md) gives hard requirements and failure reasons.
The [Oracle table](ORACLE-COMPATIBILITY.md) gives individual script construct coverage.

AccessFlow drift scans cover catalog-backed Oracle metadata.
They do not establish complete package, view, index, constraint, or Oracle option comparison.
AccessFlow replica and recovery documentation explains deployment procedures.
It does not establish measured availability or safe concurrent Oracle migrations.

Sqitch verification scripts can detect application-specific drift.
That capability does not establish an automatic complete schema comparison.
Liquibase diff and generated changelogs differ from continuous central drift monitoring.
Flyway Community does not include general SQLPlus interpretation.
Native SQLPlus generally preserves script syntax but requires explicit error handling.

Jenkins and Rundeck proposals are excluded from these product feature tables.
Their final capabilities depend on the implementation described in [additional-candidates.md](additional-candidates.md).
