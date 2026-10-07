"""Create the frontend and screenshot record without running any application."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'evidence/product-model/source-manifest.json').read_text())
def src(repo,path,label=None):
 item=manifest[repo]; assert (ROOT/item['directory']/path).exists(), path
 return f"[{label or path}](https://github.com/{item['repo']}/blob/{item['sha']}/{path})"
odc='oceanbase__odc-client'; af='bablsoft__accessflow'
rows_odc=[
('Projects','YES','/project','src/page/Project/Project/index.tsx'),
('Database Instances','YES. Datasources are registered connections','/datasource','src/page/Datasource/Datasource/index.tsx'),
('Databases','YES. Separate project database records','/project/:id/database','src/page/Project/Database/index.tsx'),
('Environments','YES. Security configuration','/secure/env','src/page/Secure/Env/index.tsx'),
('Changes/Releases','PARTIAL. Change tickets, no separate immutable release page established','/project/:id/task and /task','src/component/Task/MutipleAsyncTask/CreateModal/index.tsx'),
('Review/Approval','YES. Ticket process and approval configuration','/task and /secure/approval','src/component/Task/component/CommonDetailModal/TaskFlow.tsx'),
('Deployment/Rollout','YES. Batch execution modal. No independent rollout resource page established','Ticket detail and execution records','src/component/Task/MutipleAsyncTask/DetailContent/index.tsx'),
('History','YES. Ticket execution and operation records','Ticket detail','src/component/Task/component/CommonDetailModal/TaskExecuteRecord.tsx'),
('Audit','YES. Operation records','/secure/record','src/page/Secure/components/RecordPage/index.tsx'),
('Users/Roles','YES','/auth/user and /auth/role','src/page/Auth/Role/index.tsx')]
rows_af=[
('Projects','NO first-class project estate. Organization and pipeline configuration exist','/admin/organizations and /admin/deployment-pipelines','frontend/src/pages/admin/deployments/DeploymentPipelineSettingsPage.tsx'),
('Database Instances','PARTIAL. Datasources combine connection and database identity','/datasources','frontend/src/pages/datasources/DatasourceListPage.tsx'),
('Databases','PARTIAL. Per-connection schema/object view','/datasources/:id/settings','frontend/src/pages/datasources/DatasourceSettingsPage.tsx'),
('Environments','YES. Pipeline environment tab','/admin/deployment-pipelines/:id','frontend/src/components/deployments/PipelineEnvironmentsTab.tsx'),
('Changes/Releases','YES. Schema change sets. Generic deployment versions are a separate workflow','/schema-change-sets and /schema-change-sets/:id','frontend/src/pages/schemaChange/SchemaChangeSetListPage.tsx'),
('Review/Approval','YES. Request-group and SQL review queues','/request-groups/reviews and /reviews','frontend/src/pages/requestGroups/RequestGroupReviewQueuePage.tsx'),
('Deployment/Rollout','YES. Schema change-set ladder and Promote action','/schema-change-sets/:id','frontend/src/pages/schemaChange/SchemaChangeSetDetailPage.tsx'),
('History','YES. Environment, status, timestamps, and request-group link','/schema-change-sets/:id','frontend/src/pages/schemaChange/SchemaChangeSetDetailPage.tsx'),
('Audit','YES','/admin/audit-log','frontend/src/pages/admin/AuditLogPage.tsx'),
('Users/Roles','YES','/admin/users and /admin/roles','frontend/src/App.tsx')]
text='''# Frontend and screenshot evidence

**Both shortlisted platforms have an inspected frontend.**
The review used registered routes, navigation components, page components, and official images.
It did not rely on a README Web UI label.
The original frontend review used source and official images. No screenshot was captured from a research installation.
ODC is now deployed. The [ODC evaluation](ODC-EVALUATION.md) records live GET checks and the English language setting.
The screenshots below remain official examples. They do not prove Oracle execution on the deployed instance.

Research date: 2026-10-03.
The source commits are recorded in [PRODUCT-EVIDENCE.md](PRODUCT-EVIDENCE.md).
A page's existence does not prove runtime correctness or free-edition availability.

## Bytebase reference

The frontend uses React and TypeScript.
`frontend/src/app/router/routes/dashboard.tsx` registers workspace projects, instances, databases, environments, audit, users, and roles.
Project routes contain issues, plans, releases, GitOps, and plan rollout stages and tasks.
`frontend/src/components/ProjectSidebar.tsx` organizes project issues and CI/CD pages.
`CONTEXT.md` defines the corresponding backend operating model.
These resources establish the reference model. Enterprise route presence does not grant free usage.

Evidence: [P-BB-MODEL, P-BB-ROUTES, P-BB-NAV](PRODUCT-EVIDENCE.md#source-references).

## OceanBase ODC

The frontend uses React, TypeScript, Umi routes, and Ant Design.
The backend records the frontend as a Git submodule.
The inspected frontend commit matches that submodule exactly.
The standalone frontend enables Oracle batch tasks. Its embedded OceanBase Cloud Platform (OCP) mode removes the Oracle option.

Main navigation contains Team Workspace, Projects, Tickets, Data Sources, Users, Security, and Integrations.
Project tabs contain Databases, Tickets, Members, Sensitive Columns, Notifications, and Settings.
Security tabs include environments, risk rules, approval, SQL rules, and operation records.

'''
text+='Routes: '+src(odc,'config/routes.js')+'.\n\nNavigation: '+src(odc,'src/layout/SpaceContainer/Sider/index.tsx')+'.\n\n'
for title,repo,rows in [('ODC pages',odc,rows_odc),('AccessFlow pages',af,rows_af)]:
 if repo==af:
  text+='''## AccessFlow

The frontend uses React, TypeScript, React Router, and Ant Design.
Main navigation separates Workflow, Connections, Security and Access, and System.
Workflow includes SQL requests, deployments, request groups, schema change sets, and schema drift.
Pipeline settings contain environments, versions, permissions, freeze windows, and CI setup.
Datasource settings contain configuration, schema, permissions, masking, row security, diagrams, and activity.

The generic deployment workflow can approve an external application CI run.
The schema change-set workflow executes database requests and supplies the relevant database promotion evidence.
A generic deployment screenshot alone cannot prove that database workflow.

'''
  text+='Routes: '+src(af,'frontend/src/App.tsx')+'.\n\nNavigation: '+src(af,'frontend/src/components/common/Sidebar.tsx')+'.\n\n'
 text+='### '+title+'\n\n| Required page | Finding | Route or UI location | Source component |\n|---|---|---|---|\n'
 for kind,result,route,path in rows:text+=f'| {kind} | {result} | `{route}` | {src(repo,path)} |\n'
 text+='\n'
text+='''## Official screenshots

ODC screenshots come from the official documentation repository's V4.3.3 branch.
They show Projects, project database tabs, and the batch change panel.
The batch example uses OceanBase MySQL targets. It does not prove Oracle execution.
The Oracle source configuration separately enables `MULTIPLE_ASYNC` for actual Oracle connections.

![ODC Projects](evidence/product-model/screenshots/odc-projects.png)

![ODC project database tabs](evidence/product-model/screenshots/odc-project-databases.png)

![ODC batch change ticket](evidence/product-model/screenshots/odc-batch-change.png)

Sources: [P-ODC-PROJECT-DOC, P-ODC-BATCH-DOC, P-ODC-ORACLE-UI](PRODUCT-EVIDENCE.md#source-references).

AccessFlow screenshots come from its official repository at the inspected source commit.
They contain demonstration fixture data and a `v0.0.0` label.
They establish navigation and visible controls. They do not establish a production deployment.
The environment example says `Deploy-only (no database)`.
The source environment form separately supports a datasource binding.
A dedicated schema change-set screenshot was not found in the inspected image directory.
The actual change-set page and promotion-history component supply that evidence.

![AccessFlow deployment pipeline environments](evidence/product-model/screenshots/accessflow-deployment-pipeline-environments-light.webp)

![AccessFlow deployment detail](evidence/product-model/screenshots/accessflow-deployment-detail-light.webp)

![AccessFlow Oracle datasource setup](evidence/product-model/screenshots/accessflow-datasources-create-light.webp)

Source directory: '''+src(af,'website/images/docs','official repository screenshots')+'''.

## Comparative frontend checks

Archery uses Django templates and URL registration.
Its navigation includes SQL review, SQL queries, instances, databases, resource groups, and users.
No immutable release page or environment promotion page was established.
Evidence: [P-AR-NAV, P-AR-ROUTES](PRODUCT-EVIDENCE.md#source-references).

Open Migration uses Nuxt components and pages.
Its main navigation contains Dashboard, Databases, and Settings.
Its database pages display file migrations. Project, environment, review, and rollout pages were not established.
Evidence: [P-OM-NAV](PRODUCT-EVIDENCE.md#source-references).

SchemaPilot's React application switches between Scripts and History around the current connection.
That interface does not establish an estate release model.
Evidence: [P-SP-UI](PRODUCT-EVIDENCE.md#source-references).

SQLE and DMS reference a separate `dms-ui` build directory.
The public frontend location was not accessible during this review.
Frontend claims therefore remain limited. Free version-release rejection is established directly in the backend controller.
Evidence: [P-DMS-FRONTEND, P-SQLE-CE](PRODUCT-EVIDENCE.md#source-references).

## Screenshot provenance

The table records original locations and local hashes.
ODC overview and change-review images are diagrams, not UI screenshots.
The older ODC change-task image is supplemental. It does not establish the current project workflow.

| Local image | Original location | Local SHA-256 |\n|---|---|---|\n'''
urls={
'odc-projects.png':'https://obbusiness-private.oss-cn-shanghai.aliyuncs.com/doc/img/odc/433/700.database-change-management/200.project-collaborative-management/project5EN.png',
'odc-project-databases.png':'https://obbusiness-private.oss-cn-shanghai.aliyuncs.com/doc/img/odc/430/700.database-change-management/650.multiple-database-change/3EN.png',
'odc-batch-change.png':'https://obbusiness-private.oss-cn-shanghai.aliyuncs.com/doc/img/odc/430/700.database-change-management/650.multiple-database-change/6EN.png',
'odc-overview.png':'https://github.com/oceanbase/odc/assets/15030999/e8f1afaf-26da-4de2-b634-e2061ec565d5',
'odc-change-review.png':'https://github.com/oceanbase/odc/assets/15030999/ac55b51b-28e2-42e6-977a-7eeb7c3f11fa',
'odc-change-task.png':'https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6378659361/p293273.png'}
images=[]
for file in sorted((ROOT/'evidence/product-model/screenshots').iterdir()):
 if file.name.startswith('accessflow-'):
  item=manifest[af];path='website/images/docs/'+file.name.removeprefix('accessflow-');url=f"https://github.com/{item['repo']}/blob/{item['sha']}/{path}"
 else:url=urls[file.name]
 sha=hashlib.sha256(file.read_bytes()).hexdigest();images.append(dict(local_path=str(file.relative_to(ROOT)),url=url,sha256=sha))
 text+=f'| [{file.name}]({file.relative_to(ROOT)}) | [Official source]({url}) | `{sha}` |\n'
(ROOT/'UI-EVIDENCE.md').write_text(text)
(ROOT/'evidence/product-model/screenshots.json').write_text(json.dumps(images,indent=2)+'\n')
print('Created frontend record with ten required page types per shortlisted platform')
