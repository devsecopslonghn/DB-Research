"""Write the desired-feature register from reviewed capability decisions."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
Y, P, N, U = 'YES', 'PARTIAL', 'NO', 'UNKNOWN'
PROJECTS = [
    'Bytebase Community', 'AccessFlow', 'D-Band DRM', 'Open Migration', 'SchemaPilot',
    'Flyway UI', 'Flyway Play', 'Liquibase Community 5.x', 'Liquibase 4.33.0',
    'Flyway Community', 'Sqitch', 'Atlas public OSS', 'Yearning', 'Archery',
    'Tareya derivative', '.NET dbdeploy', 'DbMaintain', 'dbpm', 'dbward core',
    'CloudBeaver Community',
]
GROUPS = [
    ('Organization and review', [
        'Web UI', 'Database inventory', 'Application/project organization', 'Environment model',
        'Review workflow', 'Approval workflow', 'RBAC', 'Separation of duties',
    ], [
        [Y,Y,Y,Y,Y,N,Y,P], [Y,Y,P,Y,Y,Y,Y,Y], [N,P,P,P,N,N,N,N],
        [Y,Y,N,N,N,N,N,N], [Y,Y,N,N,N,N,N,N], [Y,N,N,N,N,N,N,N],
        [P,N,N,P,N,N,N,N], [N,N,N,P,N,N,N,N], [N,N,N,P,N,N,N,N],
        [N,N,N,P,N,N,N,N], [N,N,N,P,N,N,N,N], [N,N,N,P,N,N,N,N],
        [Y,Y,P,P,Y,Y,Y,P], [Y,Y,P,P,Y,Y,Y,P], [Y,Y,P,P,Y,Y,Y,P],
        [N,N,N,N,N,N,N,N], [N,N,N,N,N,N,N,N], [N,N,P,P,N,N,N,N],
        [U,Y,P,P,Y,Y,P,P], [Y,Y,N,N,N,N,P,P],
    ]),
    ('Source, automation, and identity', [
        'Git integration', 'GitLab integration', 'Jenkins integration', 'CI/CD API',
        'REST API', 'SSO', 'OIDC', 'LDAP',
    ], [
        [Y,P,P,Y,Y,N,N,N], [P,Y,P,Y,Y,Y,Y,U], [P,P,P,N,N,N,N,N],
        [Y,Y,P,P,Y,N,N,N], [U,U,U,P,Y,N,N,N], [P,P,P,N,N,N,N,N],
        [P,P,P,N,N,N,N,N], [P,P,P,N,N,N,N,N], [P,P,P,N,N,N,N,N],
        [P,P,P,N,N,N,N,N], [P,P,P,N,N,N,N,N], [P,P,P,N,N,N,N,N],
        [U,U,U,P,Y,Y,Y,Y], [U,U,P,Y,Y,Y,Y,Y], [U,U,P,P,Y,U,U,U],
        [P,P,P,N,N,N,N,N], [P,P,P,N,N,N,N,N], [P,P,P,N,N,N,N,N],
        [P,U,U,Y,Y,N,N,U], [U,U,U,U,U,U,U,U],
    ]),
    ('Operations', [
        'Audit logs', 'Vault/external secrets', 'Deployment logs', 'Notifications',
        'High availability', 'Central backup/restore', 'Disaster recovery',
    ], [
        [N,N,Y,Y,U,U,U], [Y,Y,Y,Y,P,Y,Y], [N,U,P,U,N,N,N],
        [N,U,P,U,U,U,U], [N,U,P,U,U,U,U], [N,N,P,N,N,N,N],
        [N,U,P,U,N,N,N], [N,U,P,U,N,N,N], [N,U,P,U,N,N,N],
        [N,U,P,U,N,N,N], [N,U,P,U,N,N,N], [N,U,P,U,N,N,N],
        [Y,U,Y,U,U,U,U], [Y,U,Y,Y,U,U,U], [P,U,Y,U,U,U,U],
        [N,U,P,U,N,N,N], [N,U,P,U,N,N,N], [N,U,P,U,N,N,N],
        [Y,U,Y,Y,U,U,U], [U,U,P,U,U,U,U],
    ]),
    ('Optional execution and schema features', [
        'Flyway integration', 'Liquibase integration', 'SQLPlus integration',
        'Schema diff', 'Drift detection', 'SQL review/lint',
    ], [
        [N,N,N,Y,P,Y], [N,N,N,P,P,P], [P,P,Y,U,U,U],
        [N,N,N,U,U,N], [N,N,N,U,U,N], [Y,N,U,U,U,N],
        [Y,N,N,N,N,N], [N,Y,N,Y,P,U], [N,Y,N,Y,P,U],
        [Y,N,N,N,N,U], [N,N,Y,N,P,N], [N,N,N,Y,P,U],
        [N,N,N,U,U,Y], [N,N,N,P,U,P], [N,N,N,P,U,P],
        [N,N,U,N,N,N], [N,N,Y,N,N,N], [N,N,Y,U,U,U],
        [N,N,N,P,P,Y], [N,N,U,U,U,U],
    ]),
    ('Optional governance and deployment features', [
        'Policy as code', 'Release promotion', 'Environment promotion',
        'SIEM integration', 'Terraform provider', 'Kubernetes operator/Helm',
    ], [
        [P,Y,Y,N,Y,U], [Y,Y,Y,Y,Y,Y], [U,P,P,N,N,N],
        [N,N,N,N,N,U], [N,N,N,N,N,U], [N,N,N,N,N,N],
        [N,P,P,N,N,N], [P,P,P,N,U,U], [P,P,P,N,U,U],
        [N,P,P,N,U,U], [P,P,P,N,U,U], [P,P,P,N,U,U],
        [U,N,N,U,U,U], [U,N,N,U,U,U], [U,N,N,U,U,U],
        [N,N,N,N,N,N], [N,N,N,N,N,N], [U,P,P,N,N,U],
        [Y,P,P,P,U,U], [U,N,N,U,U,U],
    ]),
]
ODC_FEATURES = {
    'Organization and review': [Y,Y,Y,Y,Y,Y,Y,P],
    'Source, automation, and identity': [P,P,P,P,Y,U,U,U],
    'Operations': [Y,U,Y,U,P,U,U],
    'Optional execution and schema features': [N,N,N,P,U,Y],
    'Optional governance and deployment features': [U,P,P,U,U,U],
}
PROJECTS.insert(1, 'OceanBase ODC')
for title, columns, rows in GROUPS:
    rows.insert(1, ODC_FEATURES[title])
lines = [
    '# Desired and optional feature matrix', '',
    'This register preserves twenty original candidates and adds OceanBase ODC.',
    'The [product comparison](PRODUCT-MODEL.md) adds SQLE/DMS, frontend evidence, and separate platform scores.',
    'This register does not control the revised platform shortlist.', '',
    'The tables evaluate every SHOULD and Nice to Have item in the supplied brief.',
    'They describe the inspected free edition or explicitly pinned source version.',
    'YES requires source or official documentation evidence.',
    'PARTIAL identifies a scope limit or external integration requirement.',
    'NO identifies an absent central capability or an explicit edition boundary.',
    'UNKNOWN identifies a feature that this review could not establish.', '',
    'A positive feature entry does not establish Oracle support for that feature.',
    'For example, Archery schema comparison primarily concerns MySQL tooling.',
    'ODC deployment and authenticated GET endpoints received runtime inspection. Oracle feature acceptance remains NOT RUN.',
    'The [ODC evaluation](ODC-EVALUATION.md) records the scope and dated runtime evidence.', '',
    'An environment model means stored environment identities or selectable engine contexts.',
    'PARTIAL engine environments require an external inventory and promotion controller.',
    'Git integration is PARTIAL when external pipelines provide versioned files.',
    'Generic command invocation does not establish a native GitLab or Jenkins integration.',
    'CLI logs are PARTIAL deployment logs because they require central collection.',
    'Backup and disaster recovery columns concern the central service.',
    'Engine target recovery appears separately in REPORT.md and the Oracle plan.', '',
]
for title, columns, rows in GROUPS:
    assert len(rows) == len(PROJECTS)
    lines += ['## ' + title, '', '| Project | ' + ' | '.join(columns) + ' |',
              '|---|' + '---|' * len(columns)]
    for project, row in zip(PROJECTS, rows):
        assert len(row) == len(columns)
        lines.append('| ' + project + ' | ' + ' | '.join(row) + ' |')
    lines.append('')
lines += [
    '## Evidence and feature boundaries', '',
    '| Project group | Evidence and interpretation |', '|---|---|',
    '| Bytebase | BB-PLAN and BB-GATES establish free features and paid approval, identity, audit, and secret boundaries. Free Terraform is explicitly listed. |',
    '| OceanBase ODC | P-ODC-PROJECT, P-ODC-ENV, P-ODC-GIT-API, P-ODC-FLOW-API, P-ODC-ROLE-INHERITANCE, P-ODC-HA-DOC, and P-ODC-SCHEMA-DIFF-DOC. Git registration exists. CI writes remain unverified. HA deployment is documented, but this deployment uses single replicas. The schema comparison guide lists OceanBase tenants and MySQL, not native Oracle. Unreviewed identity, backup, notification, and infrastructure integrations remain UNKNOWN. |',
    '| AccessFlow | AF-IAC, AF-SSO, AF-VAULT, AF-AUDIT, AF-SIEM, AF-REST, AF-CI, AF-DRIFT, and AF-DISASTER. Flyway only manages its internal PostgreSQL schema. |',
    '| DRM | DRM-LOCAL, DRM-FW, DRM-LB, and DRM-SQLPLUS. Engine adapters generate scripts. They do not establish normal engine locking and validation. |',
    '| Open Migration / SchemaPilot | OM-ENG, OM-META, OM-AUTH, SP-DRIVERS, and SP-EXEC. Small server implementations have no established multi-user governance. |',
    '| Flyway UI / Play | UI-DEPS, UI-SERVLET, PLAY-SCOPE, and PLAY-DEPS. These are application components, not independent central services. |',
    '| Flyway / Liquibase / Sqitch | FW-ORA, LB4-STATE, SQ-STATE, SQ-SQLPLUS, and official engine docs. Engines provide execution, not central identity or approvals. |',
    '| Atlas | AT-DRIVERS and official compatibility. Public OSS features do not establish Oracle support. |',
    '| Yearning | YE-SCOPE and YE-IDENTITY. LDAP and OIDC routes exist. Runtime identity and duty separation remain unverified. |',
    '| Archery | AR-DOC, AR-IDENTITY, AR-LDAP, AR-API, and AR-STATE. SQL review and schema comparison have engine-specific limits. |',
    '| Tareya derivative | FORK-EXEC and inherited repository files. Independent identity and operations verification remain incomplete. |',
    '| dbdeploy / DbMaintain / dbpm | DEP-STATE, MAINT-SCOPE, PM-SCOPE, PM-LIMITS, and official DbMaintain docs. These are engine or command projects. |',
    '| dbward | WARD-REST, WARD-PLAN, WARD-RUN, and WARD-STATE. OIDC and group authorization require commercial code. No Oracle driver exists in the reviewed implementation. |',
    '| CloudBeaver | CB-SCOPE and CB-ORA. Shared SQL editing does not establish release governance. Unreviewed commercial-edition features remain UNKNOWN. |', '',
    'Original IDs resolve in [EVIDENCE.md](EVIDENCE.md#source-references). ODC IDs resolve in [PRODUCT-EVIDENCE.md](PRODUCT-EVIDENCE.md#source-references).',
    'The [main report](REPORT.md) gives hard requirements and failure reasons.',
    'The [Oracle table](ORACLE-COMPATIBILITY.md) gives individual script construct coverage.', '',
    'AccessFlow drift scans cover catalog-backed Oracle metadata.',
    'They do not establish complete package, view, index, constraint, or Oracle option comparison.',
    'AccessFlow replica and recovery documentation explains deployment procedures.',
    'It does not establish measured availability or safe concurrent Oracle migrations.', '',
    'Sqitch verification scripts can detect application-specific drift.',
    'That capability does not establish an automatic complete schema comparison.',
    'Liquibase diff and generated changelogs differ from continuous central drift monitoring.',
    'Flyway Community does not include general SQLPlus interpretation.',
    'Native SQLPlus generally preserves script syntax but requires explicit error handling.', '',
    'Jenkins and Rundeck proposals are excluded from these product feature tables.',
    'Their final capabilities depend on the implementation described in [additional-candidates.md](additional-candidates.md).', '',
]
(ROOT / 'FEATURE-MATRIX.md').write_text('\n'.join(lines))
print(f'Recorded 35 feature decisions for each of {len(PROJECTS)} source candidates.')
