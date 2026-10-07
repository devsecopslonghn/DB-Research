"""Create the supplemental source register. This tool does not run applications."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
original = json.loads((ROOT / 'evidence/source-manifest.json').read_text())
manifest = dict(original)
for folder in ['sources', 'forks']:
    for directory in (ROOT / 'evidence/product-model' / folder).iterdir():
        if (directory / '.git').exists():
            repo = subprocess.check_output(['git', 'remote', 'get-url', 'origin'], cwd=directory, text=True).strip().removesuffix('.git').split('github.com/')[-1]
            sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=directory, text=True).strip()
            manifest[directory.name] = {'repo': repo, 'sha': sha, 'directory': str(directory.relative_to(ROOT))}
        elif (directory / 'snapshot.json').exists():
            item = json.loads((directory / 'snapshot.json').read_text())
            manifest[directory.name] = dict(item, directory=str(directory.relative_to(ROOT)))
refs = []
def add(key, repo_key, path, start=1, end=None):
    item = manifest[repo_key]
    file = ROOT / item['directory'] / path
    lines = file.read_text(errors='replace').splitlines()
    end = min(end or len(lines), len(lines))
    assert 1 <= start <= end, (key, path)
    refs.append(dict(id=key, repository=item['repo'], sha=item['sha'], path=path, start=start, end=end,
                     local_path=str(file.relative_to(ROOT)), sha256=hashlib.sha256(file.read_bytes()).hexdigest(),
                     url=f"https://github.com/{item['repo']}/blob/{item['sha']}/{path}#L{start}-L{end}"))
add('P-BB-MODEL', 'bytebase__bytebase', 'CONTEXT.md')
add('P-BB-ROUTES', 'bytebase__bytebase', 'frontend/src/app/router/routes/dashboard.tsx')
add('P-BB-NAV', 'bytebase__bytebase', 'frontend/src/components/ProjectSidebar.tsx')
add('P-BB-LICENSE', 'bytebase__bytebase', 'LICENSE', 1, 24)
for key,path in [
 ('P-AF-ROUTES','frontend/src/App.tsx'),('P-AF-NAV','frontend/src/components/common/Sidebar.tsx'),
 ('P-AF-SETS','frontend/src/pages/schemaChange/SchemaChangeSetListPage.tsx'),
 ('P-AF-PROMOTE','frontend/src/pages/schemaChange/SchemaChangeSetDetailPage.tsx'),
 ('P-AF-PIPELINE','frontend/src/pages/admin/deployments/DeploymentPipelineSettingsPage.tsx'),
 ('P-AF-ENV','frontend/src/components/deployments/PipelineEnvironmentsTab.tsx'),
 ('P-AF-INVENTORY','frontend/src/pages/datasources/DatasourceSettingsPage.tsx')]: add(key,'bablsoft__accessflow',path)
for key,path in [('P-AR-NAV','common/templates/base.html'),('P-AR-ROUTES','sql/urls.py')]:add(key,'hhyo__Archery',path)
add('P-OM-NAV','minuth__open-migration','app/components/AppSidebar.vue')
add('P-SP-UI','apegeek__schema-pilot','client/App.tsx')
odc='oceanbase__odc'; client='oceanbase__odc-client'
add('P-ODC-LICENSE',odc,'LICENCE',1,202)
add('P-ODC-DEPLOY',odc,'README.md',43,108)
add('P-ODC-ROADMAP',odc,'README.md',145,162)
base='server/odc-service/src/main/java/com/oceanbase/odc/'
for key,path in [('P-ODC-PROJECT','metadb/collaboration/ProjectEntity.java'),
 ('P-ODC-ENV','metadb/collaboration/EnvironmentEntity.java'),
 ('P-ODC-DATABASE','metadb/connection/DatabaseEntity.java'),
 ('P-ODC-BATCH-MODEL','service/flow/task/model/MultipleDatabaseChangeParameters.java'),
 ('P-ODC-BATCH-EXEC','service/flow/task/MultipleDatabaseChangeRuntimeFlowableTask.java'),
 ('P-ODC-EXEC','service/flow/task/DatabaseChangeThread.java'),
 ('P-ODC-PARAMS','service/flow/task/model/DatabaseChangeParameters.java')]: add(key,odc,base+path)
add('P-ODC-ORACLE',odc,'server/plugins/connect-plugin-oracle/src/main/java/com/oceanbase/odc/plugin/connect/oracle/OracleConnectionExtension.java',52,145)
add('P-ODC-BATCH-DOC','oceanbase__odc-doc','en-US/700.database-change-management/650.multiple-database-change.md')
add('P-ODC-PROJECT-DOC','oceanbase__odc-doc','en-US/700.database-change-management/200.project-collaborative-management.md')
controller='server/odc-server/src/main/java/com/oceanbase/odc/server/web/controller/v2/'
for key,path in [('P-ODC-DATASOURCE-API','DataSourceController.java'),
 ('P-ODC-FLOW-API','FlowInstanceController.java'),
 ('P-ODC-GIT-API','GitIntegrationController.java'),
 ('P-ODC-DB-PERMISSION-API','DatabasePermissionController.java')]:add(key,odc,controller+path)
for key,path in [('P-ODC-ROLE-INHERITANCE','service/permission/DBResourcePermissionHelper.java'),
 ('P-ODC-DB-PERMISSION-SERVICE','service/permission/database/DatabasePermissionService.java'),
 ('P-ODC-DB-PERMISSION-TYPES','service/permission/database/model/DatabasePermissionType.java')]:add(key,odc,base+path)
add('P-ODC-SWAGGER',odc,'server/odc-server/src/main/java/com/oceanbase/odc/server/config/SwaggerConfiguration.java')
add('P-ODC-DEVELOPER-GUIDE',odc,'docs/en-US/DEVELOPER_GUIDE.md')
add('P-ODC-USER-ROLES-DOC','oceanbase__odc-doc','en-US/700.database-change-management/100.user-permission-and-management/100.odc-users-and-roles.md')
add('P-ODC-HA-DOC','oceanbase__odc-doc','en-US/1100.deployment-guide/400.deploy-ha-odc-images.md',1,42)
add('P-ODC-SCHEMA-DIFF-DOC','oceanbase__odc-doc','en-US/700.database-change-management/900.structural-comparison.md',5,36)
add('P-ODC-FLOW-REQUEST',odc,base+'service/flow/model/CreateFlowInstanceReq.java')
add('P-ODC-LOCALE',client,'src/util/intl.tsx',24,40)
for key,path in [('P-ODC-CLIENT-L','LICENSE'),('P-ODC-ROUTES','config/routes.js'),
 ('P-ODC-NAV','src/layout/SpaceContainer/Sider/index.tsx'),('P-ODC-PROJECT-UI','src/page/Project/index.tsx'),
 ('P-ODC-SECURE-UI','src/page/Secure/index.tsx'),('P-ODC-PAGE-IDS','src/d.ts/_index.ts'),
 ('P-ODC-QUEUE','src/component/Task/MutipleAsyncTask/CreateModal/DatabaseQueue.tsx'),
 ('P-ODC-CHANGE-UI','src/component/Task/MutipleAsyncTask/CreateModal/index.tsx'),
 ('P-ODC-STRATEGY','src/component/Task/MutipleAsyncTask/CreateModal/MoreSetting.tsx'),
 ('P-ODC-RESULT-UI','src/component/Task/MutipleAsyncTask/DetailContent/index.tsx'),
 ('P-ODC-ORACLE-UI','src/common/datasource/oracle/index.tsx')]:add(key,client,path)
for key,repo,path in [('P-SQLE-L','actiontech__sqle','LICENSE'),('P-DMS-L','actiontech__dms','LICENSE'),
 ('P-SQLE-CE','actiontech__sqle','sqle/api/controller/v1/sql_version_ce.go'),
 ('P-SQLE-VERSION','actiontech__sqle','sqle/server/sqlversion/sql_version_ce.go'),
 ('P-SQLE-README','actiontech__sqle','README.md'),
 ('P-SQLE-ORACLE','actiontech__sqle-oracle-plugin','driver.go'),
 ('P-SQLE-ORACLE-DOC','actiontech__sqle-oracle-plugin','README.md'),
 ('P-DMS-FRONTEND','actiontech__dms','Makefile'),
 ('P-NINE-DOC','ninedata-cloud__ninedata-community','README.md')]:add(key,repo,path)
for key in ['hongweiyi__bytebase','nanzm__bytebase','WQMYH__database-govern','mydakit__dokeeper','whatif-dev-bytebase','bytebase-Database-governance','fariskha-sqlite']:
    add('P-FORK-'+key,key,'LICENSE')
    if (ROOT/manifest[key]['directory']/'LICENSE.enterprise').exists():add('P-FORK-ENT-'+key,key,'LICENSE.enterprise')
add('P-DOKEEPER-DOC','mydakit__dokeeper','README.md')
add('P-DMS-PROJECT-CE','actiontech__dms','internal/dms/biz/project_ce.go')
add('P-DMS-PROJECT-MODEL','actiontech__dms','internal/dms/biz/project.go',1,100)
add('P-DMS-INVENTORY-CE','actiontech__dms','internal/dms/service/db_service_ce.go')
add('P-DMS-ENV','actiontech__dms','internal/dms/biz/environment_tag.go',1,100)
selected_keys={r['repository'] for r in refs}
selected={k:v for k,v in manifest.items() if v['repo'] in selected_keys}
(ROOT/'evidence/product-model/source-manifest.json').write_text(json.dumps(selected,indent=2)+'\n')
(ROOT/'evidence/product-model/source-references.json').write_text(json.dumps(refs,indent=2)+'\n')
text=['# Product model source evidence','', 'Research date: 2026-10-03.',
      'This register supplements the original execution and license evidence.',
      'Each reference includes a commit, source file, line range, and local SHA-256 hash.',
      'Source review establishes implementation presence. It does not establish runtime correctness.',
      'ODC frontend commit `273fa3c4cc7d87f942ade231ce9220b98fa595e2` matches the backend client submodule.',
      'The ODC documentation branch has a separate version and commit.',
      'The deployed ODC version is 4.4.1-20260116. These source snapshots are older than the running image.',
      'The [ODC evaluation](ODC-EVALUATION.md) separates source findings from dated deployment observations.',
      'The [runtime record](evidence/product-model/odc-runtime-20261003.json) contains sanitized cluster and API observations.',
      'Dokeeper uses selected raw source files. Its full clone failed because disk space was insufficient.', '', '## Source references','',
      '| ID | Commit-pinned source | Local SHA-256 |','|---|---|---|']
for r in refs:text.append(f"| {r['id']} | [{r['repository']}: {r['path']}:{r['start']}–{r['end']}]({r['url']}) | `{r['sha256']}` |")
(ROOT/'PRODUCT-EVIDENCE.md').write_text('\n'.join(text)+'\n')
print(f'Registered {len(refs)} supplemental source references')
