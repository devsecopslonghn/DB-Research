# Catalog tính năng công cụ quản lý thay đổi database

Ngày kiểm: **07/10/2026**. Bối cảnh: khoảng **50 Oracle DB instance / 20 người**, hiện chạy SQL thủ công qua DBeaver; đã thử repository + Flyway CLI nhưng khó điều phối nhiều DB. Catalog gồm **24 họ công cụ, 25 hồ sơ** (Liquibase 4.33 và 5.x tách hồ sơ do khác license), bao phủ platform, SQL governance, migration/schema-as-code, rollout/CI và shared workbench.

Catalog giúp chọn công cụ để khảo sát theo công việc; **không chọn kiến trúc, không thay quyết định migration production** tại [report hiện hành](report.md). CloudDM v4.3.0 native Oracle executor vẫn NO-GO; workflow/inventory/approval của nó vẫn được ghi nhận. Bytebase/ODC POC lịch sử, expected, 45 criteria và 14 SQL workloads giữ nguyên. Không có SQL, deployment, mua dịch vụ, thay infrastructure hoặc runtime mới trong lượt này.

## Cách đọc bằng chứng và giả định

| Nhãn | Ý nghĩa | Giới hạn |
| --- | --- | --- |
| DOC | Đã đọc tài liệu chính thức, README, release note hoặc demo/video do hãng công bố | Chỉ xác nhận hãng mô tả tính năng; không khẳng định đã hoạt động trên Oracle nội bộ |
| SOURCE | Đã đối chiếu implementation/file license/tree tại pin ghi rõ | Một path được đọc không là audit toàn code/image hoặc test hành vi. SOURCE kế thừa ghi ngày/pin và link hồ sơ cũ |
| RUNTIME lịch sử | Có kết quả chạy thực tế được lưu trong repository | Chỉ áp dụng đúng build, edition, Oracle và ca đã kiểm; không chuyển PASS/FAIL sang build khác |
| NOT_RUN / chưa xác minh | Chưa có kiểm thực tế hoặc chưa có chứng cứ đủ cho claim | Không biến DOC/SOURCE, screenshots, release note hoặc demo công khai thành runtime |

Giả định làm việc: 50 **instance** là số endpoint cần quản lý, chưa biết số service/PDB/schema/connection, môi trường hay DB variant. 20 người chưa đồng nghĩa 20 named seats trong mọi license; pipeline contributor/service account có thể được tính khác. Oracle version, ngân sách, CI/Git provider, maintenance capacity và quyền DBA chưa biết; không giả định 19c/21c từ POC Oracle 26ai trước đây. “Hỗ trợ Oracle” được ghi riêng cho kết nối, review, execution và release; không suy Oracle-compatible mode thành Oracle Database thật.

**Dùng nguyên trạng** dưới đây nghĩa là sản phẩm có UI/model/workflow cho vai trò mô tả, sau cấu hình thông thường; không đồng nghĩa đạt toàn bộ acceptance hay có recovery đã kiểm. **Ghép thành phần** nghĩa là cần một engine/orchestrator/client khác và contract cho artifact, target, actor, result. Không loại tool vì thiếu target ledger: ledger giảm replay/rerun risk của engine, còn inventory/review/approval/audit có giá trị độc lập.

## Bảng tổng quan

Các claim tóm tắt dẫn đến hồ sơ có nguồn trực tiếp. “Không thấy cap” chỉ là phạm vi nguồn đã kiểm, không chứng minh scale 50/20 hay quyền vô hạn của binary.

| Tool / hồ sơ | Nhóm và việc giải quyết | Oracle và điểm phân biệt | License / self-host / miễn phí | Dùng nguyên trạng hay cần ghép |
| --- | --- | --- | --- | --- |
| [Bytebase](#tool-bytebase) | Platform inventory, SQL review, release/rollout | Có Oracle; lỗi POC lịch sử và edition gates | MIT subset + restricted enterprise/enablement; self-host; Community 10 instances/20 users | Platform có sẵn; 50 instances cần paid tier phù hợp; POC cũ chưa đạt mọi migration gate |
| [OceanBase ODC](#tool-odc) | Collaboration, project, SQL approval, multi-DB batch | Oracle thật; docs batch 2–100 target tasks | Backend/frontend Apache-2.0; self-host; full image/driver terms riêng | Native governance/batch; migration replay/INVALID gaps lịch sử |
| [CloudDM](#tool-clouddm) | Inventory, audit, approval, Git/HTTP change flows | Oracle JDBC; v4.3.0 compile gate mặc định off | Apache-2.0 app; self-host; bảng cap cũ không còn áp dụng ở nguồn hiện tại đã rà | Native workflow; sole native migration executor NO-GO; external engine là integration |
| [AccessFlow](#tool-accessflow) | Access governance, schema change set, promotion | Oracle connector; parser/DML/PL/SQL limits | Apache-2.0 source; self-host; image/driver terms chưa đầy đủ | Native governance/promotion; full Oracle release cần xử lý execution gaps |
| [Archery](#tool-archery) | SQL ticket, review/approve/execute, DBA portal | Oracle executor có INVALID check; commit từng câu | Apache-2.0; self-host; release/HEAD driver khác nhau | Native ticket portal; versioned release và promotion cần ghép |
| [SQLE + DMS](#tool-sqle) | SQL review plugin + datasource/workbench/governance | Oracle coverage phụ thuộc plugin/CE/EE | Community core + commercial features; self-host; exact component terms ở hồ sơ | Ghép hai component chính thức; migration engine/release model còn riêng |
| [NineData](#tool-ninedata) | SQL policy/approval + ordered environment release | Oracle SQL tasks; MySQL-only rollback/version features phải tách | Community free self-host 10 datasource; không chứng minh OSS implementation; Enterprise paid | Platform có sẵn; 50 datasource cần thương mại; CI blocking do cấu hình |
| [Flyway](#tool-flyway) | Versioned migrations, validate, per-target history | Oracle driver/parser; SQL*Plus features có edition boundary | Apache-2.0 OSS engine; Community free; Teams/Enterprise paid | Engine có sẵn; estate UI/approval/audit cần control plane |
| [Liquibase 4.33 / 5.x / Secure](#tool-liquibase4) | Changesets, checksum/lock, diff, policies | Oracle JDBC; DDL rollback phụ thuộc change/script | 4.33 Apache-2.0; 5.x FSL; Secure commercial; self-host engine | Engine + orchestration; không coi Secure là central approval portal đã kiểm |
| [Sqitch](#tool-sqitch) | Dependency plan, deploy/revert/verify, registry | Oracle qua SQL*Plus/DBD::Oracle | MIT; self-host CLI; client dependencies riêng | Engine; cần inventory/rollout/user workflow ngoài |
| [Atlas](#tool-atlas) | Declarative/versioned schema, planning/lint/drift | **Oracle Pro-only** | OSS/community CLI Apache-2.0; default binary/Pro terms riêng | Oracle cần commercial Pro; cloud/control-plane entitlement cần phân biệt |
| [Oracle SQLcl Project](#tool-sqlcl) | Capture/stage/release/artifact/deploy Oracle schema | Native Oracle; Liquibase integration | Download free theo Oracle terms; không OSS platform | Oracle toolchain; ghép Git/CI/target inventory/approval |
| [dbpm](#tool-dbpm) | PL/SQL package/dependency installation lifecycle | Oracle SQLcl/SQL*Plus + in-DB Core | CLI và Core source Apache-2.0 tại pins đã đọc; self-host; artifact/dependencies riêng | Package manager; ghép governance và rollout |
| [Gitora](#tool-gitora) | Git/object branching, collaboration, compilation-before-commit | Oracle/PLSQL specialist; không chứng minh fleet recovery | Proprietary self-host; trial; 300 USD/user/năm niêm yết | Native object workflow; approval/multi-target release cần kiểm/ghép |
| [OEM + Lifecycle Pack](#tool-oem) | Oracle inventory/baseline/compare/change plans | Native Oracle; script/impact cho destination | Proprietary self-host OMS/agents; schema change pack paid | Native estate/schema administration; Git/CI release contract cần adapter |
| [Rundeck](#tool-rundeck) | Job/runbook, node inventory/filter, execution API | Qua Flyway/Liquibase/SQLcl; không native migration engine | Community Apache-2.0 self-host; enterprise capabilities paid | Composition cho Oracle release; approval edition phải phân biệt |
| [AWX / Ansible](#tool-awx) | Inventory/groups, workflow, approval node, RBAC | Playbook/command/engine adapter | AWX Apache-2.0 self-host; AAP/Controller commercial | Composition; inventory host không tự là DB/schema inventory |
| [Jenkins](#tool-jenkins) | Git pipeline, input approval, agents/credentials | Engine chạy trên agent | MIT core; self-host free; plugin/ops cost riêng | Composition; target registry và DB release records tự cấu hình/phát triển |
| [Octopus Deploy](#tool-octopus) | Release snapshots, lifecycle, targets, runbooks/audit | DB engine/script bên ngoài | Proprietary cloud/self-host; free 10 users không đủ 20 | CD platform có sẵn; Oracle schema workflow cần engine; DB count khác machine count |
| [Harness Database DevOps](#tool-harness) | DB instance/schema + changelog + pipeline policies | Oracle JDBC; delegate vào private network | Commercial module; SaaS + self-host delegate; full self-managed entitlement chưa kiểm | DB-aware product; support/license/recovery cần kiểm theo package |
| [DBmaestro](#tool-dbmaestro) | Oracle source control/drift/impact/release automation | Oracle native theo vendor DOC | Commercial; on-prem integration DOC; no current public binary pin | Platform chuyên DB; version/API/self-host architecture cần xác minh |
| [CloudBeaver](#tool-cloudbeaver) | Shared connections, browser SQL editor | Oracle Thin driver source; audit panel paid | Apache-2.0 CE self-host; enterprise editions paid | Shared workbench native; release/approval engine phải ghép |
| [DbGate](#tool-dbgate) | DB client, schema diff, shared team admin | Oracle Thin/Thick connector | GPL-3.0 CE self-host; Team Premium paid | Native workbench; schema sync không tự là release workflow |
| [DBHub](#tool-dbhub) | MCP queries/metadata, multiple named sources, web workbench | Oracle Thin connector/splitter source | MIT; self-host; không thấy paid caps tại nguồn đã đọc | Component tra cứu/postcheck; không release approval platform |

## So sánh theo công việc thực tế

Đây là khả năng DOC/SOURCE ở đúng edition ghi trong hồ sơ, không bảng runtime PASS. Review người, SQL quality check và preview DDL là ba việc khác nhau; workflow approval không chứng minh Oracle execution correctness. Mỗi dòng dùng [nguồn trong hồ sơ](#chi-tiet-tool) tương ứng; “ngoài” chỉ thành phần Git/CI/engine cần ghép.

| Tool | Inventory | Chọn target | Review | Approval |
| --- | --- | --- | --- | --- |
| Bytebase | Project/instances/databases | Database/environment/plan | SQL Review + Git | Configurable flow; edition gate |
| ODC | Project/datasource/environment | Ticket hoặc batch database tasks | SQL validation/risk | Built-in/external approval |
| CloudDM | Datasource/environment | Ticket/change flow | SQL audit | Approval action/ticket |
| AccessFlow | Datasource/pipeline | Change set/environment | Statement gate/review plan | Deployment gate/promotion review |
| Archery | Instance/resource group | SQL ticket/instance | Oracle review parser | Ticket workflow + execution permission |
| SQLE+DMS | Datasource/project | Authorized workbench/ticket target | Plugin SQL audit | CE/EE-specific ticket flow |
| NineData | Datasource/environment | Task + release-node binding | Per-source policy + GitOps report | Task approver/executor |
| Flyway | Configuration, ngoài | URL/schema/config, ngoài loop | Validate/preview; PR ngoài | Ngoài |
| Liquibase | Target config, ngoài | URL/schema/context/label | Validate/diff/update-sql; Secure policy | Ngoài; không chứng minh portal Secure |
| Sqitch | Named target config | Target URI/change tag | Plan/dependency/verify scripts | Ngoài |
| Atlas | Schema/config/project | Env/URL + commercial rollout config | Diff/plan/lint, edition-specific | Git/Cloud integration, entitlement riêng |
| SQLcl Project | Project + connection | Named target connection | Stage/verify/release artifacts | Git/CI ngoài |
| dbpm | Config/schema/package registry | SQLcl/SQLPlus target | Manifest/lockfile/package verify | Ngoài |
| Gitora | Git repo + DB/object | Repo/object/database | Git diff + valid-object-before-commit | Git/CI ngoài; DB privilege là access control |
| OEM | Managed Oracle target/group | Change plan destination | Baseline diff/impact report | DBA review/privilege; hard gate chưa chứng minh |
| Rundeck | Node/resource model | Filter + job options | Git job/SQL ngoài | ACL; approval theo paid feature/plugin |
| AWX | Inventory/host/group | Inventory + limit | Git playbook/SQL ngoài | Workflow approval node |
| Jenkins | Manifest/CMDB ngoài | Pipeline param/matrix | PR + scripted checks | Input + submitter restrictions |
| Octopus | Targets/env/tenant | Env/tags/tenant/variables | Process + artifact review | Approval rules/lifecycle |
| Harness DB DevOps | DB instance/schema | DB schema/instance in step | Git + DB/pipeline checks | Pipeline approval/policy |
| DBmaestro | DB/schema connection theo DOC | Release path/target | Object diff/drift/impact DOC | Vendor workflow/policy DOC |
| CloudBeaver | Shared/private connections | Connection navigator | SQL editor, ngoài PR | Ngoài |
| DbGate | Env config hoặc premium storage | Connection/database | Schema compare/editor | Ngoài |
| DBHub | TOML sources | Named source/tool ID | SQL metadata/explain | Ngoài |

| Tool | Rollout | Kiểm kết quả | Audit | Release thất bại |
| --- | --- | --- | --- | --- |
| Bytebase | Release/plan/task | Central revision/task; INVALID gap lịch sử | Enterprise boundary | Task runs/revisions; compile/checksum/reconcile cần kiểm |
| ODC | Multi-DB serial/parallel batch | Task/output; INVALID gap lịch sử | Ticket/project/MetaDB | Dedup/replay/role gaps lịch sử; không rerun giả đã sửa |
| CloudDM | Change flow/webhook | Central results; compile off v4.3.0 | Ticket/query/flow records | Native executor NO-GO; external executor cần explicit contract |
| AccessFlow | Environment promotion ladder | Central checksum/result | Metadata audit | Parser/target replay/reconcile gaps |
| Archery | Ticket execution | Named PL/SQL INVALID check SOURCE | Execution log/ticket | Per-statement commit; partial state cần reconcile |
| SQLE+DMS | Ticket/workbench/version features theo edition | Audit/execution status | DMS/SQLE operation log theo edition | Ticket status chưa chứng minh target/recovery |
| NineData | Ordered node promotion | Task/release result; Oracle postcheck chưa kiểm | Account/AK/SQL audit DOC | Stop/pause/restart/manual backup restore; không auto rollback Oracle |
| Flyway | CI target loop/matrix | History/validate/info + postcheck ngoài | Target history + CI actor ngoài | Repair/forward fix sau target inspection; DDL có partial commit |
| Liquibase | Orchestrator nhiều target | DBCL/checksum/status + postcheck ngoài | DBCL; Secure report | Lock release khác reconcile; rollback cần script và kiểm state |
| Sqitch | Deploy theo target/plan | Registry + verify/check | Registry events | Revert intent không bảo đảm undo Oracle DDL |
| Atlas | Apply/deploy; paid rollout features | Migration/drift/lint theo edition | CLI/Cloud reports | Plan/revert/forward fix theo engine; Oracle cần Pro POC |
| SQLcl Project | Deploy artifact qua connection | Liquibase/project verify + own checks | Engine history/CI trace | Artifact/state reconciliation và DBA recovery ngoài |
| dbpm | Install/upgrade package dependency | Lockfile/Core verification scope | Package/Core state, CI ngoài | Core/install script-specific; chưa chứng minh estate resume |
| Gitora | Pull/diff/object deploy DOC | Git state, precommit validity DOC | Gitora change tracking DOC | Object Git reset khác data/DDL recovery; fleet chưa kiểm |
| OEM | Script/job theo destination | Impact report/job output | Job/change plan + admin security | Xem lỗi, sửa nguyên nhân, retry theo operator guide |
| Rundeck | Job workflow/node dispatch | Execution output/per-node | Job history/ACL | Stop/branch/retry ngoài engine; retry job không undo DDL |
| AWX | Workflow/playbook + serial/fan-out | Job events/play recap | Activity stream/job history | Failure branch; engine/runbook reconcile |
| Jenkins | Code pipeline/batches | Stage logs + scripted postcheck | Build/Git actor; full audit plugin/policy riêng | Stop/resume/retry tự thiết kế, state trong engine |
| Octopus | Release lifecycle/promotion | Task/target logs + postcheck | Mutation audit/tasks | Guided failure; schema backout phụ thuộc engine |
| Harness DB DevOps | DB-aware pipeline stage | Changeset/schema/pipeline visibility DOC | DB/pipeline audit DOC | Rollback claims phụ thuộc change scripts; Oracle cần partial-failure test |
| DBmaestro | Release automation DOC | Monitoring/drift DOC | Object/release audit DOC | Vendor backout claims; chưa SOURCE/RUNTIME |
| CloudBeaver | Editor script; release ngoài | Result/history | Query history; audit panel paid | Session/Oracle state do operator xử lý |
| DbGate | Client sync/script; release ngoài | Query/schema comparison | Premium audit | Manual/engine ngoài; không target release ledger |
| DBHub | Custom/query tools; release ngoài | Metadata/query/health | Request traces; team audit ngoài | Query retry không tương đương migration recovery |

<a id="chi-tiet-tool"></a>

## Chi tiết tool

Các SOURCE kế thừa dưới đây là review được giữ trong repository; ngày pin/review cũ khác ngày DOC recheck 07/10/2026. Những tool không có RUNTIME lịch sử nêu cụ thể đều **NOT_RUN**.

<a id="tool-bytebase"></a>

### Bytebase

**Nhóm:** nền tảng database DevOps tự triển khai, tập hợp inventory, SQL Editor, GitOps, review SQL, phê duyệt, release/rollout và audit. Trong các nền tảng ở đây, Bytebase có mô hình sản phẩm gần dạng dùng nguyên trạng nhất; độ đúng migration Oracle vẫn phải kiểm theo phiên bản.

**Tính năng**

- **Quản lý target theo project và môi trường:** [Oracle migration overview](https://www.bytebase.com/databases/oracle/schema-migration/) mô tả target, review/risk, staging và audit; release [3.23.0](https://github.com/bytebase/bytebase/releases/tag/3.23.0) thêm instance gắn theo project. (**DOC**)
- **GitOps qua pull request:** [Database-as-Code flow](https://www.bytebase.com/database-as-code/) mô tả review/phê duyệt và deploy sau merge; [ví dụ GitHub Actions chính thức](https://github.com/bytebase/example-gitops-github-flow) chạy review SQL trên pull request rồi rollout qua test/prod theo phê duyệt. (**DOC**)
- **Release/rollout có API:** [ReleaseService proto tại commit 3.23.0](https://github.com/bytebase/bytebase/blob/c8188c635465321ff930c97200742a96ef653144/proto/v1/v1/release_service.proto#L18-L65) khai báo tạo/cập nhật release qua HTTP API với quyền `bb.releases.create/update`; [RolloutService proto](https://github.com/bytebase/bytebase/blob/c8188c635465321ff930c97200742a96ef653144/proto/v1/v1/rollout_service.proto#L16-L47) khai báo tạo/liệt kê rollout theo plan, gồm API HTTP và audit field. (**SOURCE**)
- **review SQL và rollout nhiều database:** source plan 3.23.0 liệt kê pre-deployment review, batch changes, progressive environment deployment, changelog và rollout policy trong [plan.yaml](https://github.com/bytebase/bytebase/blob/c8188c635465321ff930c97200742a96ef653144/backend/enterprise/plan.yaml#L1-L160). Các tính năng được cấp theo plan; không coi đây là runtime verification. (**SOURCE**)
- **Oracle parser/schema operations:** ghi chú release [3.23.0](https://github.com/bytebase/bytebase/releases/tag/3.23.0) ghi sửa cú pháp partitioned-table constraints; các ghi chú cũ hơn nêu parser/schema sync Oracle. Đây là cải tiến cụ thể theo release, không đảm bảo tương thích toàn bộ PL/SQL/SQLPlus. (**DOC**)

**License và giới hạn 50 DB/20 người:** source pin `3.23.0`, commit `c8188c635465321ff930c97200742a96ef653144`, kiểm ngày 07/10/2026. [`plan.yaml`](https://github.com/bytebase/bytebase/blob/c8188c635465321ff930c97200742a96ef653144/backend/enterprise/plan.yaml#L1-L160) đặt FREE tối đa 10 instance/20 seat (dòng 2–4), TEAM 10 instance/không giới hạn seat (44–46), ENTERPRISE không giới hạn instance/seat (94–96); phê duyệt chỉ có Enterprise, audit hạn chế ở TEAM và đầy đủ ở Enterprise (139–140). [`LICENSE`](https://github.com/bytebase/bytebase/blob/c8188c635465321ff930c97200742a96ef653144/LICENSE#L1-L25) chỉ cấp MIT cho phần được bao phủ, loại trừ thư mục Enterprise và mã enablement; [`LICENSE.enterprise`](https://github.com/bytebase/bytebase/blob/c8188c635465321ff930c97200742a96ef653144/LICENSE.enterprise) có điều khoản riêng. Với 50 DB, cả FREE và TEAM đều thiếu instance capacity; 20 người vừa bằng giới hạn FREE. [Trang giá chính thức](https://www.bytebase.com/pricing/) hiện ghi Pro $20/user/tháng và Enterprise liên hệ bán hàng, nhưng tên SKU không ánh xạ rõ với enum plan trong source; cần quote đúng gói tự triển khai. Không thể giả định trả phí làm thay đổi lỗi runtime cũ.

**RUNTIME lịch sử và ranh giới:** build `3.22.1/FREE`, Oracle 26ai: 17 PASS, 14 PARTIAL, 4 FAIL, 3 BLOCKED, 7 NOT_RUN. Native version/revision/replay được quan sát; strict checksum, procedure INVALID, phê duyệt/audit trên FREE và một promotion path có lỗi. Chi tiết tại [`BYTEBASE-ORACLE-POC-RESULTS.md`](../BYTEBASE-ORACLE-POC-RESULTS.md) và [source review](candidates/bytebase/source-review.md). Kết quả chỉ thuộc build này, không chuyển sang 3.23.0/Enterprise.

**Giá trị và công cấu hình:** tập trung danh mục target, chọn database theo project/environment, review, rollout và task trạng thái thay việc chạy từng DB bằng DBeaver. Cần nhập 50 target, nhóm project/environment, policy, credentials/SSO và Oracle compile/post-check. Có thể dùng API/Terraform/GitOps trực tiếp; cần cấu hình repository mapping, runner, service identity và phê duyệt policy. Target-side migration ledger, crash reconciliation và Oracle compile gate cần xác minh riêng.

**Pin:** release `3.23.0` phát hành 24/09/2026; pin source/license/plan nêu trên được fetch và đọc 07/10. Runtime pin lịch sử là `3.22.1`, review ngày 04/10/2026.

<a id="tool-odc"></a>

### OceanBase ODC

**Nhóm:** trung tâm cộng tác phát triển/vận hành database. Project, ticket, phê duyệt và batch khiến ODC hữu ích cho điều phối dù ledger tại target/replay migration chưa đạt.

**Tính năng**

- **Cộng tác theo project và kiểm soát thay đổi:** [README chính thức](https://github.com/oceanbase/odc) mô tả project collaboration, phê duyệt, SQL validation, SQL window rules và risk level. (**DOC**)
- **Batch nhiều database:** [hướng dẫn batch đã ghim](https://github.com/oceanbase/odc-doc/blob/40dc7c03522fef1968bd11b2b051bc216091e60d/en-US/700.database-change-management/650.multiple-database-change.md#L1-L120) nêu serial/parallel, manual control và 2–100 target tasks; [batch parameter model](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/task/model/MultipleDatabaseChangeParameters.java#L36-L67) cùng [runtime task source](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/task/MultipleDatabaseChangeRuntimeFlowableTask.java#L1-L347) cho thấy implementation model. (**DOC/SOURCE**)
- **Tích hợp phê duyệt bên ngoài:** [tài liệu SQL approval tại commit docs đã ghim](https://github.com/oceanbase/odc-doc/blob/40dc7c03522fef1968bd11b2b051bc216091e60d/en-US/1000.system-integration/300.sql-audit-integration.md) nói ODC gọi API của hệ phê duyệt/review khi người dùng chạy SQL. (**DOC**)
- **Connector Oracle:** [OracleConnectionExtension](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/plugins/connect-plugin-oracle/src/main/java/com/oceanbase/odc/plugin/connect/oracle/OracleConnectionExtension.java#L52-L124) thực hiện phần kết nối Oracle. Phải tách Oracle Database với OceanBase Oracle mode. (**SOURCE/DOC**)

**Giấy phép và giới hạn:** backend [Apache-2.0](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/LICENCE), frontend [Apache-2.0](https://github.com/oceanbase/odc-client/blob/273fa3c4cc7d87f942ade231ce9220b98fa595e2/LICENSE); chưa xác minh license đầy đủ của MetaDB, image, JDBC và dependencies. Chưa tìm thấy cap 50 DB/20 người trong các đường source/docs đã rà, nhưng chưa kiểm entitlement hoặc tải. Xem [giới hạn dùng](https://www.oceanbase.com/docs/common-odc-1000000000876736) để phân biệt connector Oracle thật với các chế độ tương thích.

**RUNTIME lịch sử:** ODC `4.4.1-20260116`, Oracle 26ai 23.26.4.1.0: 12 PASS, 20 PARTIAL, 5 FAIL, 8 NOT_RUN. SQL-11: procedure INVALID vẫn được báo thành công; replay/checksum/dedup/tách requester FAIL; promotion qua runner ngoài PARTIAL, chưa chứng minh batch bản địa. Xem [`ODC-ORACLE-POC-RESULTS.md`](../ODC-ORACLE-POC-RESULTS.md) và [source review](candidates/odc/source-review.md). Không chạy runtime mới.

**Git/CI/API, giá trị và công cấu hình:** API và phê duyệt integration ngoài có tài liệu; README quảng bá Git repository integration. Cần cấu hình project/role/environment/risk, MetaDB backup, secret/driver/TCPS, phê duyệt và batch. Inventory, tickets, editor và batch có thể giảm thao tác từng database. Nếu migration bắt buộc ledger tại target/replay/reconciliation, cần thêm và kiểm tra tích hợp đó; không suy rằng ODC là Flyway-compatible history store.

**Pin:** source backend `d517c0f27971642fb0cd7565fd61ab2309875ec3`, frontend `273fa3c4cc7d87f942ade231ce9220b98fa595e2`, docs pin `40dc7c03522fef1968bd11b2b051bc216091e60d`; các snapshot được rà 04–06/10/2026. GitHub release ghi nhận trước đó `v4.3.4_bp2` (06/06/2025), trong khi docs hiện công bố nhánh 4.4.x; runtime lịch sử là build khác. Recheck docs 07/10/2026.

<a id="tool-clouddm"></a>

### CloudDM

**Nhóm:** bảng điều khiển quản trị database, ticket/audit SQL và webhook CI. CloudDM vẫn có giá trị ở vai trò quản trị workflow, dù Oracle executor v4.3.0 hiện **NO-GO** nếu dùng làm migration engine duy nhất.

**Tính năng**

- **Quản lý datasource và môi trường:** README [v4.3.0 đã ghim](https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/README.md) mô tả datasource, quyền, SQL audit, ticket và các lựa chọn triển khai; [hướng dẫn deploy](https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/docs/guides/deployment.en.md) có standalone và Console + Sidecar. (**DOC**)
- **Kết nối Oracle qua JDBC:** [OracleDsFactory](https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/backend/clouddm-plugins/clouddm-ds/dsc-common-oracle/src/main/java/com/clougence/clouddm/dsfamily/oracle/execute/dsfactory/OracleDsFactory.java) tạo kết nối Oracle. Kết nối được không chứng minh parser/executor migration Oracle đúng. (**SOURCE**)
- **Ticket phê duyệt gắn với thay đổi:** [action phê duyệt](https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/backend/clouddm-platform/cgdm-console/src/main/java/com/clougence/clouddm/console/web/component/cicd/action/ChangeActionForApproval.java) tạo ticket và giữ tệp SQL đính kèm; việc tách người yêu cầu/người duyệt/người chạy và ràng buộc target bất biến cần xác minh. (**SOURCE**)
- **Nhận sự kiện CI qua webhook:** [GitLab CI guide](https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/docs/guides/gitlab-cicd.en.md) và [webhook controller](https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/backend/clouddm-platform/cgdm-console/src/main/java/com/clougence/clouddm/console/web/controller/cicd/DmChangeFlowWebhookController.java) mô tả/triển khai nhận sự kiện theo commit và delivery ID. Chống lặp webhook không phải ledger migration, khóa hoặc phục hồi ở Oracle. (**DOC/SOURCE**)

**Oracle và giới hạn:** review artifact chính xác [v4.3.0 ngày 07/10](research-round-2/coordinator/clouddm-v430-artifact-review-20261007.md) xác nhận kiểm tra compile mặc định Oracle đang tắt trong đường đã rà; chưa có bằng chứng target migration ID/checksum, khóa target hoặc xử lý trạng thái commit chưa rõ. Đây là lý do NO-GO làm native executor duy nhất, không phủ nhận inventory, quyền, ticket phê duyệt, thao tác SQL và workflow tập trung. Không có RUNTIME mới.

**License, release và sức tải:** release `v4.3.0`, commit `3aa1238a471afca2579e76e6fbf0a922d9be5579`, ngày 30/09/2026; các đường source/image quan trọng được đối chiếu 07/10. Ứng dụng đã rà theo Apache-2.0; Oracle JDBC có thông báo FUTC riêng và dependency khác chưa được audit đầy đủ. Trang [giá CloudDM](https://www.cdmgr.com/en/pricing/) hiện nói đã mở mã nguồn, không còn bảng 10 instance/5 account đã thấy trong kết quả cache cũ. Review source/image chọn lọc không thấy gọi counter 5/10 trên các đường đã rà, nhưng không chứng minh mọi đường nhập liệu không giới hạn hoặc năng lực 50/20. Không chạy tải.

**Git/CI/API, giá trị và công cấu hình:** có GitLab webhook/HttpCall và REST/webhook route. Cần cấu hình kho Git/flow, định danh delivery, target/môi trường, role, secrets, Oracle driver và lưu audit. Công cụ có thể tập trung danh mục đích, ticket, phê duyệt, SQL audit và intake CI thay cho chuyển qua lại giữa DBeaver và script. Muốn chạy migration an toàn cần bổ sung executor khác hoặc thay đổi được hỗ trợ để có compile gate, trạng thái bền vững theo target, lock và reconciliation; không suy rằng Flyway mà CloudDM dùng nội bộ quản lý migration Oracle phía khách hàng.

<a id="tool-accessflow"></a>

### AccessFlow

**Nhóm:** proxy quản trị truy cập database/API, kết hợp workflow schema-change và promotion. Sản phẩm có change set/pipeline bản địa, không chỉ là giao diện review SQL.

**Tính năng**

- **Proxy SQL qua nhiều engine:** README [tại source pin](https://github.com/bablsoft/accessflow/blob/55c209a4d9e4ba09a6c089f90e68a8b16b3f2133/README.md) liệt kê Oracle cùng các SQL engine và mô tả request đi qua lớp quản trị. Đây là DOC, chưa phải kiểm tra Oracle runtime.
- **Khai báo Oracle JDBC connector:** [connector definition](https://github.com/bablsoft/accessflow/blob/55c209a4d9e4ba09a6c089f90e68a8b16b3f2133/connectors/oracle/connector.json#L1-L22) chỉ định `ojdbc11`; [backend pom](https://github.com/bablsoft/accessflow/blob/55c209a4d9e4ba09a6c089f90e68a8b16b3f2133/backend/pom.xml) nói driver phía database được phân giải riêng, không đóng gói sẵn. (**SOURCE**)
- **Cổng loại DML và change set:** [tài liệu schema-change](https://github.com/bablsoft/accessflow/blob/55c209a4d9e4ba09a6c089f90e68a8b16b3f2133/docs/20-schema-change-governance.md) mô tả thay đổi được khai báo theo change set; [statement gate](https://github.com/bablsoft/accessflow/blob/55c209a4d9e4ba09a6c089f90e68a8b16b3f2133/backend/src/main/java/com/bablsoft/accessflow/schemachange/internal/SchemaChangeStatementGate.java#L29-L152) từ chối SELECT/INSERT/UPDATE/DELETE nhưng nhận `OTHER`, nên không phải allow-list chỉ nhận DDL. (**DOC/SOURCE**)
- **Promotion theo môi trường và checksum:** [promotion service](https://github.com/bablsoft/accessflow/blob/55c209a4d9e4ba09a6c089f90e68a8b16b3f2133/backend/src/main/java/com/bablsoft/accessflow/schemachange/internal/DefaultSchemaChangePromotionService.java#L259-L321) kiểm tra trạng thái môi trường trước và review plan; [checksum](https://github.com/bablsoft/accessflow/blob/55c209a4d9e4ba09a6c089f90e68a8b16b3f2133/backend/src/main/java/com/bablsoft/accessflow/schemachange/internal/SchemaChangeChecksum.java#L9-L40) được lưu ở metadata trung tâm. Không thấy ledger migration tại Oracle target. (**DOC/SOURCE**)

**Oracle và khoảng thiếu:** docs/source công bố connector Oracle nhưng chưa chứng minh PL/SQL, slash delimiter, SQLPlus, compile INVALID, Oracle 19c/21c hoặc TCPS. Checksum và trạng thái promotion là metadata trung tâm; chống chạy lại/phục hồi tại target chưa được xác lập. Không có RUNTIME.

**License, release và người dùng:** source review pin `55c209a4d9e4ba09a6c089f90e68a8b16b3f2133`, xem [`source-review.md`](candidates/accessflow/source-review.md); release review ghi v2.7.0 tại `2ba5d322e7e1b4c750b5b0af85935e9ae814bd6a`, nhưng chỉ một số file được so sánh và chưa map đầy đủ sang image. Repo Apache-2.0; không thấy seat/instance cap công khai, nhưng chưa đo 50 DB/20 người. Image, dependencies và driver Oracle cần rà riêng.

**Git/CI/API, giá trị và công cấu hình:** trang [AccessFlow hiện tại](https://accessflow.io/) tuyên bố có GitHub Actions, GitLab CI, Azure Pipelines, Jenkins, Terraform provider và REST API; các khả năng mới nhất này là DOC, có thể sau source pin. Cần cấu hình pipeline/environment, kết nối proxy, IDP/service account, review plan, ngoại lệ parser, lịch drift và thời gian lưu audit. Có thể khảo sát nếu cần promotion DDL qua môi trường; cần tích hợp/thêm ledger tại target, replay/recovery hoặc kiểm compile Oracle nếu đây là điều kiện bắt buộc. Đây không phải composition Flyway có sẵn.

<a id="tool-archery"></a>

### Archery

**Nhóm:** cổng ticket SQL/review và portal cho tác vụ vận hành database. Có ích cho quản trị và DBA operations; chưa có release migration bất biến được chứng minh.

**Tính năng**

- **Truy vấn Oracle và một số tác vụ DBA:** README [tại commit đã rà](https://github.com/hhyo/Archery/blob/ccc7134f48d0e261f9e3ffa0d445dcec48adb790/README.md#L25-L42) công bố query, backup, data dictionary và session quản lý; không hỗ trợ quản lý account/parameter Oracle. [Oracle engine](https://github.com/hhyo/Archery/blob/ccc7134f48d0e261f9e3ffa0d445dcec48adb790/sql/engines/oracle.py#L26-L50) tạo kết nối SID/service-name. (**DOC/SOURCE**)
- **Ticket review/phê duyệt và quyền thực thi:** [workflow views](https://github.com/hhyo/Archery/blob/ccc7134f48d0e261f9e3ffa0d445dcec48adb790/sql_api/api_workflow_operations.py#L400-L526) kiểm tra review/execute permission và trạng thái workflow. (**SOURCE**)
- **Kiểm tra SQL Oracle:** [review path](https://github.com/hhyo/Archery/blob/ccc7134f48d0e261f9e3ffa0d445dcec48adb790/sql/engines/oracle.py#L736-L807) dùng sqlparse cùng delimiter tùy chỉnh. Chưa chứng minh tách PL/SQL lồng nhau hay script SQLPlus. (**SOURCE**)
- **Thực thi theo câu và phát hiện INVALID:** [executor](https://github.com/hhyo/Archery/blob/ccc7134f48d0e261f9e3ffa0d445dcec48adb790/sql/engines/oracle.py#L1125-L1205) commit từng câu, rồi kiểm tra INVALID cho object PL/SQL có tên; lỗi giữa script có thể để lại thay đổi một phần. (**SOURCE**)

**Giới hạn release và kiểm chứng:** review pin HEAD `ccc7134f48d0e261f9e3ffa0d445dcec48adb790`, license Apache-2.0; release v1.14.0 (`bc1f10efcc465f6a63c94b97feaba5d15546712a`, 07/03/2026) dùng đường Oracle dependency khác (cx-Oracle + Instant Client so với `oracledb==4.0.1` ở HEAD đã rà). Tách riêng điều khoản image/client. Chưa thấy cap 50/20 công khai hoặc thử tải. Không có RUNTIME mới.

**Nhiều target, CI/API, giá trị và công cấu hình:** resource groups/permissions và kết quả execution lưu ở metadata Archery, nhưng chưa thấy ledger tại target/checksum hay promotion có thứ tự qua stage. Có đường API/workflow cho ticket; chưa thấy promotion release qua GitOps. Có thể tập trung instance catalog, ticket SQL, review, phê duyệt, execution và một số tác vụ Oracle, giảm một phần thao tác DBeaver. Muốn có release quản trị cần ghép migration engine, ledger, artifact immutability, ordered orchestration, target reconciliation và Oracle privilege checks.

<a id="tool-sqle"></a>

### SQLE + DMS (ActionTech)

**Nhóm:** hai sản phẩm phối hợp. SQLE xử lý review/audit SQL và ticket; DMS cung cấp inventory datasource, truy cập và database workbench rộng hơn. Kết hợp này có thể giảm thao tác vận hành thủ công nhưng không tự tạo migration ledger Oracle.

**Tính năng**

- **Ticket SQL từ review đến publish:** [hướng dẫn workflow](https://actiontech.github.io/sqle-docs/docs/user-manual/project/workflow/intro/) mô tả các trạng thái, reviewer/publisher, rollback từ backup và quản lý phiên bản SQL. (**DOC**)
- **Rule review cấu hình theo loại database:** [rule template](https://actiontech.github.io/sqle-docs/docs/user-manual/project/rule-template-manager/) cho phép chọn loại DB, bộ rule, mức cảnh báo và tham số; [bảng tính năng v4](https://actiontech.github.io/sqle-docs/docs/support/compare/) ghi Oracle và review trong pipeline DevOps. (**DOC**)
- **Giám sát SQL sau triển khai:** [hướng dẫn quản lý SQL](https://actiontech.github.io/sqle-docs/docs/user-manual/project/audit_task/intro/) phân biệt ticket review trước publish với scan/collect SQL liên tục; nguồn TopSQL bao gồm Oracle. Một số quản trị SQL/insight hiệu năng là Enterprise. (**DOC**)
- **Phê duyệt qua workflow/API và công cụ cộng tác:** [hướng dẫn bắt đầu nhanh](https://actiontech.github.io/sqle-docs/docs/v2/quick-usage/) chỉ cách phân vai admin/dev/DBA, tạo ticket và review/publish; [tích hợp quy trình](https://actiontech.github.io/sqle-docs/docs/user-manual/sys-configuration/process_syn/) mô tả DingTalk/Feishu/Coding. review trong pipeline DevOps và OpenAPI được nêu trong [bảng tính năng](https://actiontech.github.io/sqle-docs/docs/support/compare/). (**DOC**)
- **DMS quản lý datasource, project và quyền ở bản CE:** source CE có [project handler](https://github.com/actiontech/dms/blob/d63b4ea798e811881107d193b25d2c33f6d8685c/internal/dms/biz/project_ce.go#L1-L57) và [inventory service](https://github.com/actiontech/dms/blob/d63b4ea798e811881107d193b25d2c33f6d8685c/internal/dms/service/db_service_ce.go#L1-L30); SQLE CE có [phiên bản SQL endpoint](https://github.com/actiontech/sqle/blob/44e88c45f9cd55edb2d826795770001e019dda81/sqle/api/controller/v1/sql_version_ce.go#L1-L57). (**SOURCE**)

**Pin và provenance kiểm 07/10/2026:** GitHub API read-only `releases/latest`, `commits/HEAD`, tag refs và raw LICENSE đã được truy vấn. SQLE release mới nhất là ref tự sinh `untagged-6b1b918ff20445087a64`, cùng trỏ về HEAD `44e88c45f9cd55edb2d826795770001e019dda81` (phát hành 30/09/2026; commit ngày 26/08). DMS không có GitHub release (API trả 404); HEAD `d63b4ea798e811881107d193b25d2c33f6d8685c` (29/09/2026). `sqle-oracle-plugin` không có release (404); HEAD `41355b4948e4e69500e5d4369a668ec0a994c272` (18/03/2022), khá cũ so với SQLE hiện hành. Vì vậy không có artifact release pin chung hay source/image mapping thống nhất cho bộ DMS+SQLE.

**License và giới hạn 50 DB/20 người:** [SQLE LICENSE tại pin](https://github.com/actiontech/sqle/blob/44e88c45f9cd55edb2d826795770001e019dda81/LICENSE) và [DMS LICENSE tại pin](https://github.com/actiontech/dms/blob/d63b4ea798e811881107d193b25d2c33f6d8685c/LICENSE) là MPL-2.0. Tại [pin Oracle plugin](https://github.com/actiontech/sqle-oracle-plugin/tree/41355b4948e4e69500e5d4369a668ec0a994c272), các request raw cho `LICENSE`, `LICENSE.txt`, `LICENSE.md` trả 404; không tìm thấy license ở root, nên MPL của core không xác lập quyền dùng/phân phối plugin Oracle. Tài liệu [project v4](https://actiontech.github.io/sqle-docs/docs/user-manual/project/intro/) nói CE chỉ có project mặc định, Enterprise tạo được nhiều project; [ticket v3](https://actiontech.github.io/sqle-docs/docs/v3/user-manual/project/workflow/create-workflow/) nói CE mỗi ticket một datasource, Enterprise hỗ trợ nhiều datasource và fanout cùng SQL. [`LICENSE-AUDIT.md`](../LICENSE-AUDIT.md) cùng code pin ghi inventory toàn cục, project changes, phiên bản SQL/dependency và batch releases có Enterprise gates. Không tìm thấy con số cap cụ thể cho 50 DB/20 seat hoặc giá bundle đầy đủ; cần hỏi đúng SKU, quyền dùng Oracle plugin và support.

**Oracle và khoảng thiếu:** Oracle Database khác với OceanBase Oracle mode. Ghi chú release 4.2606.0 nêu sửa phân loại CTE/EXPLAIN/MERGE và bổ sung khám phá view/routine, trong khi plugin Oracle riêng có pin từ 2022. Cần kiểm tra plugin đang đi cùng bản phát hành, Oracle version, file mode cho PL/SQL, compile-invalid gate, binding SQL-target và lỗi giữa chừng. review SQL không chứng minh migration đã hoàn tất đúng.

**Git/CI/API, giá trị và công cấu hình:** tài liệu có pipeline review, API, plugin; chưa chứng minh một artifact bất biến được promotion qua DEV/UAT/PROD với ledger tại target và reconciliation. DMS inventory/workbench/access kết hợp SQLE Oracle review/ticket/phê duyệt/monitoring có thể phù hợp nếu quản trị SQL là nhu cầu thật. Cần cấu hình datasource, role, environment, rule template, plugin, phê duyệt, CI credentials, DMS–SQLE handoff và thời gian lưu audit. Nếu cần release state/retry chắc chắn, ghép migration engine hoặc tự xây orchestration/ledger; đó là composition.

**Ghi chú release:** [SQLE release object](https://github.com/actiontech/sqle/releases/tag/untagged-6b1b918ff20445087a64) tóm lược mốc 4.2606.0 ở nhiều repo CE/EE; đó là DOC, không phải test. Chưa có RUNTIME cho tổ hợp.

<a id="tool-ninedata"></a>

### NineData Community / Enterprise

**Vai trò:** platform database DevOps, SQL governance, release workflow và data comparison; phù hợp khảo sát sản phẩm có sẵn. Community là bản phân phối miễn phí self-host; chưa có bằng chứng để gọi implementation là OSS.

**Năm tính năng có nguồn:**

1. **DOC:** SQL task có precheck theo policy của datasource, người approve/executor, lịch chạy và lựa chọn dừng khi gặp lỗi. Oracle được liệt kê trong SQL task và automatic backup support. [SQL tasks](https://docs.ninedata.cloud/en/sqldev/sql_task/).
2. **DOC:** release process gắn datasource vào từng environment; node có thể hạn chế sửa SQL, bỏ qua bước và chỉ cho promote thay đổi đã thành công ở baseline. [Release qua môi trường](https://docs.ninedata.cloud/en/bp/sql_dev/dev_pipeline/).
3. **DOC:** CI chạy `ninedata check` trên SQL/MyBatis XML, trả report về GitLab/Codeup. Kết quả mặc định để hiển thị; cấu hình blocking rule ở CI mới biến nó thành gate. [GitOps review](https://docs.ninedata.cloud/en/sqldev/gitops_sql_review/).
4. **DOC:** OpenAPI quản lý datasource, role, approval và workflow task; API tạo task nhận loại task và dữ liệu SQL. [OpenAPI](https://docs.ninedataglobal.com/openapi/openapi_overview/), [Create workflow](https://docs.ninedataglobal.com/openapi/workflow/createworkflow/).
5. **DOC:** Community 5.3.0 công bố audit ghi AccessKey, role con và script task phục vụ release qua môi trường cách ly. [Community release notes](https://docs.ninedata.cloud/en/release_notes/community/).

**Oracle và release lỗi:** tài liệu SQL tasks hỗ trợ Oracle thật, nhưng tùy chọn rollback tự động khi lỗi chỉ ghi **MySQL-only**. Backup tải xuống để phục hồi thủ công không là rollback mọi Oracle DDL. Chưa xác minh PL/SQL splitter, INVALID-object enforcement, target checksum/replay ledger, crash reconciliation hay Oracle version matrix cho đúng build. Release note nêu database version management cho **MySQL**; không gán tính năng đó cho Oracle. [SQL tasks](https://docs.ninedata.cloud/en/sqldev/sql_task/), [5.3.0 và lịch sử release](https://docs.ninedata.cloud/en/release_notes/community/).

**50 DB / 20 người, license và self-host:** bảng Community hiện giới hạn **10 datasource**, một default approval template mỗi approval group, Docker một máy; Enterprise mở rộng theo license và có cluster/support. Chưa có con số seat cap được kiểm. Source tree tại pin chỉ có README hai ngôn ngữ và release note, không có backend implementation hoặc LICENSE; GitHub metadata license null. Không coi “Community”, repo public hoặc miễn phí là OSS. [Edition matrix](https://docs.ninedata.cloud/community_edition/), [tree đã kiểm](https://github.com/ninedata-cloud/ninedata-community/tree/a4481123d3b490a3ad4044d03fc737a38a766e78). Đây là **SOURCE về cấu trúc artifact**, không SOURCE xác nhận tính năng.

**Giá trị và công bổ sung:** tập trung target, policy, approval và đường đi release thay cho chọn từng connection bằng DBeaver. So với Flyway CLI, bổ sung quản trị và theo dõi task; không chứng minh thay được target ledger của Flyway. Cần cấu hình environment/node restrictions, phân quyền, secret, Git/CI gate, retention và postcheck Oracle; quy mô 50 datasource cần gói thương mại. Chưa mua, liên hệ hãng hoặc chạy demo.

**Pin/ngày:** kiểm 07/10/2026; public repository HEAD `a4481123d3b490a3ad4044d03fc737a38a766e78` (08/09/2026); release note **5.3.0**, nội dung đến 02/09/2026. Không có GitHub release endpoint thành công, source→image hoặc binary digest được kiểm. DOC hiện hành có thể rộng hơn build 5.3.0; mọi runtime mới **NOT_RUN**.

<a id="tool-flyway"></a>

### Flyway Community và commercial editions

Flyway vẫn là lựa chọn hợp lý để chuẩn hóa phần **execute, record per-target, validate** vốn đã quen thuộc, nhưng cần thay hình thức chạy CLI rời rạc bằng pipeline có inventory và chiến lược rollout. Các khả năng được tài liệu xác nhận:

- **DOC — versioned migrations, thứ tự và checksum:** migrations chạy đúng một lần theo version; `flyway_schema_history` lưu checksum, success và state. [`Versioned migrations`](https://documentation.red-gate.com/flyway/flyway-concepts/migrations/versioned-migrations), [`schema history`](https://documentation.red-gate.com/flyway/flyway-concepts/migrations/flyway-schema-history-table).
- **DOC — preflight validation:** `validate` so sánh tên/type/checksum, migration thiếu/thừa và thay đổi sau khi đã deploy. [`Validate`](https://documentation.red-gate.com/flyway/reference/commands/validate).
- **DOC — Oracle:** docs driver liệt kê Oracle 12.2, 18c, 19c, 21c, 23ai, 26ai; trang nói all editions (bao gồm XE). Trang driver liệt kê các phiên bản kết nối; trang Oracle support ghi phiên bản đã kiểm **18.4 và 26ai**, không đồng nghĩa đã kiểm toàn bộ danh sách. SQL*Plus emulation thuộc Teams, cần bật `oracle.sqlplus`; không phải SQL*Plus native và có unsupported commands. [Oracle support](https://documentation.red-gate.com/flyway/reference/database-driver-reference/oracle-database), [SQL*Plus configuration](https://documentation.red-gate.com/flyway/reference/configuration/flyway-namespace/flyway-oracle-namespace/flyway-oracle-sqlplus-setting). [`Oracle driver`](https://documentation.red-gate.com/flyway/reference/database-driver-reference/oracle-database).
- **DOC — rollout fleet:** tài liệu tháng 10/2026 minh họa matrix/loop theo từng target, serial hoặc giới hạn concurrency, chain `info validate migrate`, dừng rollout khi một target lỗi, reconcile target drift và resume sau khi sửa forward. Có ví dụ GitHub Actions và liên kết cấu hình cho Jenkins/GitLab/Azure DevOps/Octopus/Harness cùng nền tảng khác. [`Fleet rollout guide`](https://documentation.red-gate.com/flyway/deploying-database-changes-using-flyway/rolling-out-updates-from-a-single-schema-to-multiple-production-databases), [`fleet tutorial`](https://documentation.red-gate.com/flyway/deploying-database-changes-using-flyway/rolling-out-updates-from-a-single-schema-to-multiple-production-databases/tutorial-fleet-rollout-with-migrations-based-deployment).
- **DOC — thêm schema-as-code:** Flyway có schema model/state-based deployment cho Oracle; Teams/Enterprise feature set mở rộng so với migration CLI Community. Cần xác nhận entitlement/giá theo user và workflow dự kiến, nhất là undo, checks, state-based deployments. [Schema model và edition](https://documentation.red-gate.com/flyway/flyway-concepts/schema-model).

**License/edition boundary:** Community miễn phí; Teams và Enterprise trả phí theo user trong chính sách thương mại Redgate được công bố. Community migration engine có thể chạy local/self-host trong CI. [`Commercial licensing FAQ`](https://documentation.red-gate.com/flyway/learn-more-about-flyway/commercial-licensing-faq), [`edition feature summary`](https://documentation.red-gate.com/flyway/reference/). Dùng `info/validate/migrate` trên từng target chỉ cho biết trạng thái target đó; việc phát hiện target nào chưa chạy cần inventory + vòng lặp target do CI/runner quản lý. Mẫu chính thức thể hiện matrix, không biến Flyway CLI thành dịch vụ user/approval tập trung.

**Oracle failure/recovery:** Redgate fleet guide mô tả Oracle trong nhóm migration transactional và nói target ở version cũ khi migration thất bại. Oracle Database docs nói DDL có implicit COMMIT trước và sau, nên DDL đã chạy không rollback như một transaction thông thường. Vì vậy không dùng tuyên bố transactional như cam kết đảo ngược Oracle DDL. Nếu script có nhiều câu lệnh hoặc PL/SQL block, phần đã commit/hoàn tất có thể còn sau lỗi; cần nhỏ hóa change, dự báo SQL, kiểm tra target, forward-fix hoặc DBA-directed recovery. Undo migration cũng là script bù, không phải rollback transaction kỳ diệu. [`Oracle DDL commit semantics`](https://docs.oracle.com/en/database/oracle/oracle-database/19/tdddg/data-definition-language-ddl-statements.html).

So với baseline, giá trị lớn là migration identity/checksum/history per DB, validate, lệnh lặp lại có exit status và mẫu rollout tự động. Phần còn phải cấu hình/tự phát triển: catalog 50 target với owner/env/maintenance windows, secret source/rotation, target groups và variant policy, approval/audit source, concurrency/rate controls, stop/resume, kết quả xác nhận SQL/object state, failed-target incident workflow, idempotent retry rules. Trong tổ hợp đã chọn Flyway để deploy, chỉ Flyway thực thi DDL của change đó.

**Schema model / phạm vi state-based (DOC):** Schema model cho Oracle có trong Teams/Enterprise. Teams hỗ trợ dùng thủ công; pipeline tự động dùng schema model cần Enterprise. CLI có thể so model với từng target và sinh script riêng để áp dụng; Redgate khuyến nghị migration-based cho CD vì script có thể review/version và luồng dữ liệu hoặc thứ tự tùy chỉnh cần tác giả kiểm soát. State-based deployment so với trạng thái trực tiếp của target và không dùng history table; cần kiểm tra baseline/drift và tuần tự hóa CI. [`Schema model`](https://documentation.red-gate.com/flyway/flyway-concepts/schema-model), [`deployment approaches`](https://documentation.red-gate.com/fd/deployment-approaches-with-flyway-167936855.html), [`fleet rollout and state-based flow`](https://documentation.red-gate.com/flyway/deploying-database-changes-using-flyway/rolling-out-updates-from-a-single-schema-to-multiple-production-databases), [`edition feature matrix`](https://documentation.red-gate.com/flyway/learn-more-about-flyway/feature-summary).

**License source và distribution trả phí:** repository source Flyway khai báo Apache-2.0. Tài liệu Redgate mô tả distribution riêng có tính năng trả phí; license repository không cấp quyền Teams/Enterprise và không có nghĩa mọi binary Redgate có cùng entitlement. Trang OSS download cung cấp CLI open-source; tài liệu license yêu cầu người tạo pipeline dùng Teams/Enterprise phải được cấp license theo user. [`Flyway source README/license`](https://github.com/flyway/flyway), [`Open Source download`](https://documentation.red-gate.com/flyway/reference/usage/flyway-open-source), [`commercial licensing`](https://documentation.red-gate.com/fd/licensing-164167730.html), [`per-user rules`](https://documentation.red-gate.com/fd/how-flyway-per-user-licensing-works-206605237.html).

**Pin release:** stable mới nhất ngày 07/10/2026 là **Flyway 13.9.0 (01/10/2026)**. Release notes ghi sửa Oracle parser; trang tải open-source chỉ tới `flyway-commandline-13.9.0`. [`13.9.0 release notes`](https://documentation.red-gate.com/fd/release-notes-for-flyway-engine-179732572.html). Source pin kế thừa `flyway/flyway@a549f5dd1ac80fbe7bc8103dfcd2d556c606c39c`, đã đọc 03/10/2026, không đại diện implementation của release hiện tại. [Repo evidence index](https://github.com/flyway/flyway/tree/a549f5dd1ac80fbe7bc8103dfcd2d556c606c39c).

<a id="tool-liquibase4"></a>

### Liquibase 4.33 Community (Apache-2.0)

- **DOC — changelog-as-code:** changesets SQL/XML/JSON/YAML, changelog có thứ tự và lệnh update; XML/JSON/YAML có change type portable, formatted SQL giữ SQL trực tiếp. [`Liquibase OSS 4.33 implementation guide`](https://docs.liquibase.com/oss/implementation-guide-4-33).
- **DOC — per-target history + lock:** `DATABASECHANGELOG` ghi thay đổi, checksum/execution metadata; `DATABASECHANGELOGLOCK` ngăn hai process Liquibase cùng update một target. Đây là khóa theo DB target, không phải khóa fleet-wide. [`DATABASECHANGELOG`](https://docs.liquibase.com/oss/user-guide-4-33/what-is-the-databasechangelog-table), [`DATABASECHANGELOGLOCK`](https://docs.liquibase.com/oss/user-guide-4-33/what-is-the-database-changelog-lock-table).
- **DOC — Oracle:** có Oracle database extension/driver, command `generate-changelog`, `diff`, `update-sql`, `update`, `rollback-sql`; test Oracle version cụ thể vẫn cần POC. [`Oracle connector 4.33`](https://docs.liquibase.com/oss/integration-guide-4-33/connect-liquibase-with-oracle-database?entryId=4UUfehgRhjsmaVLoD6eckC), [`danh sách DB hỗ trợ`](https://docs.liquibase.com/oss/integration-guide-4-33/what-databases-are-supported-by-liquibase?entryId=15zgbOmVHYcAcLHl9UkICG), [`4.33 release notes`](https://github.com/liquibase/liquibase/releases/tag/v4.33.0).
- **DOC/SOURCE — CI/API:** OSS 4.33 có hướng dẫn Maven chính thức: pin version trong `pom.xml`, cấu hình changelog/connection, chạy `mvn liquibase:updateSQL` để xem trước SQL rồi `mvn liquibase:update` để deploy. [`Liquibase OSS 4.33 Maven integration`](https://docs.liquibase.com/oss/get-started-4-33/install-liquibase-with-maven). **SOURCE** — source 4.33.0 được pin trong repo tại `liquibase/liquibase@75773ed9b45b0a5adf3c42872d2e5494da669427`; `liquibase-standard/.../Liquibase.java` khai báo facade Java `Liquibase` cùng constructors/operations, còn Javadoc nói CLI, Ant, Maven và test là wrappers quanh API. [Source class](https://github.com/liquibase/liquibase/blob/75773ed9b45b0a5adf3c42872d2e5494da669427/liquibase-standard/src/main/java/liquibase/Liquibase.java#L58-L127). Tài liệu tích hợp 4.33 liệt kê các cách dùng CLI, Java API, Maven, Spring Boot, Ant, Jenkins, GitHub Actions và Docker; trang này mô tả bề mặt tích hợp, không chứng minh tính năng Pro miễn phí. [`Liquibase 4.33 integration modes`](https://docs.liquibase.com/oss/implementation-guide-4-33). Source xác nhận Java API tồn tại; các nguồn đã đọc không cho thấy chỉ riêng việc gọi API Java cần entitlement Pro. CLI/Maven tự host được; không thành phần nào cung cấp inventory/review UI tập trung.
- **DOC — rollback boundary:** modeled changesets chỉ auto-generate rollback cho một tập change types; formatted SQL cần rollback do tác giả viết. `rollback-sql` preview trước khi thực thi; Oracle DDL implicit commit vẫn áp dụng, nên rollback là thao tác DDL mới và có thể thất bại/không phục hồi data. [`Rollback commands`](https://docs.liquibase.com/oss/reference-guide-4-33/init-update-and-rollback-commands/what-are-rollback-commands), [`rollback`](https://docs.liquibase.com/oss/reference-guide-4-33/init-update-and-rollback-commands/rollback) và [Oracle DDL semantics](https://docs.oracle.com/en/database/oracle/oracle-database/19/tdddg/data-definition-language-ddl-statements.html).

4.33 phù hợp nếu Apache-2.0 là tiêu chí license cứng hoặc muốn tận dụng hệ sinh thái lâu đời. Có thể pin engine version, driver, changelog, contexts/labels và một cấu hình trên mỗi environment/target. So với DBeaver, tạo release có thứ tự và lịch sử per DB; so với Flyway CLI, changelog structured/database-agnostic và diff/generate phong phú hơn. Phải tự ghép orchestrator/inventory, access management, reviewer approval, audit retention, rollout batching và xử lý target thất bại.

**License và pins:** Liquibase 4.33.0 source trong repository đã được pin/hash và license Apache-2.0 kiểm ở vòng trước. Source pin kế thừa `liquibase/liquibase@75773ed9b45b0a5adf3c42872d2e5494da669427` (snapshot nghiên cứu 2026-10-03; không phải release hiện tại). [Release 4.33.0](https://github.com/liquibase/liquibase/releases/tag/v4.33.0). Các tính năng ở phần này chủ yếu là DOC; lần này đọc bổ sung API Java tại pin, không tái đọc toàn source 4.33.

<a id="tool-liquibase5"></a>

### Liquibase Community 5.x và Liquibase Secure

Đây là một ranh giới license/phân phối quan trọng đã đổi từ tài liệu cũ:

**Release đã kiểm (DOC):** ngày 07/10/2026 GitHub hiển thị Community **5.0.4, phát hành 20/08/2026** là stable latest. 5.0.4 có credential redaction, opt-in lockdown cho một số tính năng thực thi code và hơn 30 fixes gồm Oracle. [`5.0.4 release`](https://github.com/liquibase/liquibase/releases/tag/v5.0.4), [`release notes`](https://docs.liquibase.com/community/release-notes/liquibase-community-5-0-4-release-notes).
**License/phân phối (DOC):** Community 5.0+ dùng Functional Source License 1.1, sau 2 năm chuyển Apache-2.0; FSL hạn chế dùng thương mại cạnh tranh với Liquibase trong thời hạn đó và không phải OSI-approved open-source. Lõi có thể tải/chạy miễn phí; package hiện module hóa, người dùng tự cài driver/extensions bằng Liquibase Package Manager. Secure có binary/repository riêng và commercial license; đừng dựa trên file Maven 5.0.0 có metadata license sai lịch sử. [`GitHub release notice`](https://github.com/liquibase/liquibase/releases/tag/v5.0.0), [`FSL`](https://fsl.software/FSL-1.1-ALv2.template.md), [`Secure distribution`](https://github.com/liquibase/liquibase/releases/tag/v5.0.0).
- **DOC — Community engine functionality:** changelog, DBCL/DBCLLOCK, update/status/snapshot/diff/rollback, CLI/Java/Maven/CI integration; 5.0 modular packaging đặt trách nhiệm driver/dependency setup lên user. Liquibase 5.0.4 notes ghi sửa lỗi Oracle. Connector guide 5.0.4 liệt kê phiên bản đã kiểm 12.2, 19c, 21c, 23ai; không đủ để kết luận mọi Oracle version/object semantics được hỗ trợ. [`Community 5.0.4 guide`](https://docs.liquibase.com/community/implementation-guide-5-0-4), [`Oracle docs`](https://docs.liquibase.com/community/integration-guide-5-0-4/connect-liquibase-with-oracle-database).
- **DOC — Secure:** thương mại tách riêng khỏi community; vendor mô tả thêm policy checks, automation, governance/change insights, flows, bundled extensions/drivers/support. Pricing hiện theo application-based tiers; số cụ thể phải lấy báo giá. [`Secure + 5.0`](https://www.liquibase.com/blog/liquibase-ignites-innovation-liquibase-secure-5-0-redefine-database-change-with-ai-velocity-and-confidence), [`pricing`](https://www.liquibase.com/pricing).
- **DOC — stale lock / recovery:** lock table là per-target và `release-locks` mở khóa nếu process chết không sạch. Điều đó chỉ gỡ mutex, không tự reconcile Oracle DDL hoặc target state. [`DBCLLOCK 5.0.3`](https://docs.liquibase.com/community/user-guide-5-0-3/what-is-the-database-changelog-lock-table).

5.x Community phù hợp nếu user chấp nhận FSL và tự quản dependency packaging; Secure đáng khảo sát khi cần governance thương mại. Lợi ích so với thao tác SQL thủ công là ordered changesets, status/history/checksum/lock và CI API. 5.x Community cũng như 4.33 đều cần control plane bên ngoài cho 50 DB/20 user; Secure có thể bù một phần nhưng phải xác minh feature/hosting/seat/application boundaries và approval workflow với vendor. Không suy từ Secure marketing ra single pane inventory hoặc automatically reconciled failure. Oracle implicit commit khiến rollback declarations không bảo đảm phục hồi.

**Pin:** current stable `v5.0.4`, release ngày 20/08/2026, Git tag source commit `2c25134` theo release page. Source pin kế thừa repo là `liquibase/liquibase@3ed5c81625671e91b4423ba4503fe68ce947d1ff`, date 2026-10-03; repo snapshot khẳng định license file nhưng không phải source pin hiện tại. [Tag v5.0.4](https://github.com/liquibase/liquibase/tree/v5.0.4). Community 5.x FSL chỉ nên chọn sau license review; bản 4.33 giữ Apache-2.0 nếu muốn tránh điều kiện FSL.

<a id="tool-sqitch"></a>

### Sqitch

- **DOC — plan-based change graph:** project giữ `sqitch.plan` với dependency order; mỗi change có deploy/revert/verify script, `add/deploy/revert/verify/check` và target config. [`Sqitch manual`](https://sqitch.org/docs/manual/sqitch/), [`tutorial`](https://sqitch.org/docs/manual/sqitchtutorial/).
- **DOC — Oracle engine:** official engine list có Oracle; cần SQL*Plus, Oracle Instant Client và Perl `DBD::Oracle`; `ORACLE_HOME`, `TNS_ADMIN`/TNS alias là vận hành bắt buộc thường làm setup agent nặng hơn Java/JDBC-only runner. Không tìm thấy Oracle version support matrix cụ thể từ Sqitch. [`Oracle tutorial/prerequisites`](https://sqitch.org/docs/manual/sqitchtutorial-oracle/), [`engine configuration`](https://sqitch.org/docs/manual/sqitch-engine/).
- **DOC — per-target registry/checks:** Oracle registry là schema riêng chứa change IDs, script hashes, deploy/revert/fail/merge events; `sqitch check` đối chiếu plan/source hashes với registry. Review source kế thừa cũng ghi chi tiết implementation tại pin cũ. [`Oracle engine`](https://github.com/sqitchers/sqitch/blob/v1.6.1/lib/App/Sqitch/Engine/oracle.sql), [`check`](https://sqitch.org/docs/manual/sqitch-check/).
- **DOC — nhiều engine/project:** engine/target được cấu hình riêng; có thể quản nhiều DB bằng config/project/target URI và gọi lặp từ shell/CI. Không có inventory daemon, release approval, dashboard, user roles hoặc fleet reconciliation tích hợp trong các nguồn đã đọc. [Target configuration](https://sqitch.org/docs/manual/sqitch-target/).
- **DOC — recovery semantics:** Sqitch thực thi deploy, verify, rồi ghi register; nếu deploy script lỗi thì giả định không có gì để revert; lỗi verify sẽ gọi revert script của change. Đây là script-level protocol, không khôi phục mọi partial DDL của Oracle. [`deploy semantics`](https://sqitch.org/docs/manual/sqitch-deploy/), Oracle DDL có implicit commit.

MIT, source available/self-host; release hiện thấy `v1.6.1` (06/01/2026; GitHub page không hiển thị year nhưng xác định lần kiểm), không tìm thấy bản mới trong danh sách release. [`Sqitch releases`](https://github.com/sqitchers/sqitch/releases), [license](https://github.com/sqitchers/sqitch/blob/v1.6.1/LICENSE.md). So với SQL thủ công, Sqitch lưu intent/dependency, verification scripts, revert plan, hash và deployment events; khác Flyway/Liquibase là author viết ba script logic, không chủ yếu đánh dấu một migration tuần tự. Tự ghép Git review, target list, secrets, approvals, serialized rollout, audit/report aggregation. `verify` là SQL do team viết; nó không tự nhận biết mọi schema drift.

Kiểm tra source hiện tại (chỉ đọc `git ls-remote`, 07/10/2026): HEAD nhánh `develop` là `b08e5c8a773ee4ab5ea4ab7cf6f7a16c55d6994e`, khớp source pin kế thừa trong repository; trang source gọi là `v1.6.2-dev`. Bản stable mới nhất vẫn là **v1.6.1**; trang GitHub release hiển thị SHA rút gọn `ce0550c`. Tag object v1.6.1 khác commit đã peel và khác HEAD develop hiện tại; dùng release tag nếu cài stable và chỉ dùng `develop@b08e5c8...` để tham khảo source hiện tại. [`v1.6.1 release`](https://github.com/sqitchers/sqitch/releases/tag/v1.6.1), [`current develop README/source`](https://github.com/sqitchers/sqitch/tree/b08e5c8a773ee4ab5ea4ab7cf6f7a16c55d6994e). EVIDENCE.md trong repository liên kết các dòng implementation thực tế về registry hash/event và SQL*Plus executor tại cùng commit; đây là phát hiện **SOURCE** từ review kế thừa, không có RUNTIME. Các feature hiện mô tả ở trên là DOC.

<a id="tool-atlas"></a>

### Atlas OSS / Atlas Pro

- **DOC — schema-as-code workflows:** workflow declarative so DB hiện tại với trạng thái mong muốn trong HCL/SQL/ORM; workflow versioned sinh và lập kế hoạch migration files. [`Atlas docs`](https://www.atlasgo.io/docs).
- **DOC — edition gate:** Atlas feature matrix ghi Oracle driver **chỉ Atlas Pro**; open OSS drivers chủ yếu PostgreSQL/MySQL/MariaDB/SQLite/TiDB/LibSQL. Migration linting, custom rules, pre-migration checks, drift detection, checkpoints, visualization, interactive migrations và deployment rollout cũng Pro. [`feature matrix`](https://www.atlasgo.io/features).
- **DOC — Oracle capabilities:** Driver Oracle của Pro liệt kê tables/columns, indexes, foreign keys, views, triggers và các object khác theo tài liệu driver. Ma trận phiên bản Oracle cụ thể chưa đủ chi tiết để đánh giá DB nội bộ; cần xác nhận với hãng trước POC. [`Oracle HCL reference`](https://www.atlasgo.io/hcl/oracle), [`hướng dẫn migration Oracle`](https://www.atlasgo.io/guides/oracle/automatic-migrations).
- **DOC — rollout/CI:** thao tác versioned/declarative dùng CLI và tích hợp GitHub Actions/CI; CI/CD cần Atlas Pro. Hướng dẫn mô tả PR review/lint/test, tạo migration artifact bất biến, Registry tùy chọn và promotion qua môi trường; phần này hỗ trợ release nhưng không chứng minh inventory người dùng/target đầy đủ. [`CI/CD setup`](https://www.atlasgo.io/versioned/setup-cicd), [`pricing`](https://www.atlasgo.io/pricing).
**Phân phối/license (DOC):** release v1.3.0 (02/08/2026) ghi binary mặc định theo Atlas MSA, community binary theo Apache-2.0; phải tách hai bản phân phối. Pro/cloud trả phí; trang giá hiện nêu Pro theo seat/usage, dự án CI/CD $59/tháng gồm 2 target database và $39 cho mỗi target bổ sung; Enterprise báo giá riêng. Xác nhận điều kiện áp dụng cho Oracle và hosting trong báo giá. [`v1.3.0 release`](https://github.com/ariga/atlas/releases/tag/v1.3.0), [`pricing`](https://www.atlasgo.io/pricing).

Atlas có thế mạnh lập kế hoạch thay đổi schema và kiểm tra rủi ro, nhưng cần Atlas Pro để kết nối Oracle. Nếu chỉ chấp nhận OSS thì Atlas không phải engine Oracle miễn phí; vẫn giữ trong danh sách thương mại đáng khảo sát về schema-as-code. Quản lý 50 target/20 người dùng cần Pro/Cloud hoặc lớp inventory/orchestration bên ngoài; phải xác nhận khả năng tự host và tổng chi phí. Khi deploy Oracle lỗi, không suy ra transaction đã tự rollback; cần kiểm tra DDL nào đã áp dụng và có kế hoạch sửa tiến tới/recovery rõ ràng.

Pin release/source: v1.3.0, commit `9a6bc60`, phát hành 02/08/2026. Repo có source pin kế thừa `ariga/atlas@1317a57674f3795de395f535a258c088d7f767bf` (snapshot 03/10/2026), khi đó CLI public chưa có Oracle driver. Kết quả **SOURCE** lịch sử này được cập nhật cho quyết định sản phẩm bởi DOC hiện tại: Oracle là tính năng Pro; không suy rằng Oracle có trong OSS. [Source pin kế thừa](https://github.com/ariga/atlas/tree/1317a57674f3795de395f535a258c088d7f767bf).

<a id="tool-sqlcl"></a>

### Oracle SQLcl Project và tích hợp Liquibase

SQLcl là CLI dành cho Oracle với hai workflow liên quan: `project` quản lý source và release artifact; extension Liquibase tích hợp để capture schema, tạo changelog và deploy. Đây là các workflow bổ trợ, không phải nền tảng quản lý tập trung riêng.

- **DOC — project/source control:** `project init` tạo khung repository; `export` capture schema/object (và APEX ở phạm vi hỗ trợ); `stage` so sánh branch hiện tại với base branch rồi tạo Liquibase changelog/changesets; `release` chuyển phần đã stage sang thư mục release có version; `gen-artifact` đóng gói zip/tgz; `deploy` triển khai artifact; `verify` chạy các phép kiểm tra đã cấu hình. [`Project command guide 26.1`](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/26.1/sqcug/project.html), [`project usage examples`](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/26.1/sqcug/project-command-usage-examples.html).
- **DOC — Liquibase capture:** `lb generate-schema` tạo XML cho từng object và controller file, có thể tạo SQL để review; cho phép lọc object, grants, synonyms, context/labels; `UPDATE` dùng changelog để deploy. [`SQLcl 26.1 Liquibase commands`](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/26.1/sqcug/liquibase.html), [`SQLcl 26.1 User Guide`](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/26.1/sqcug/oracle-sqlcl-users-guide.pdf).
- **DOC — Oracle-first scope:** export object dựa trên loại object DBMS_METADATA hỗ trợ và extension riêng của SQLcl; bao gồm Oracle procedural objects/APEX và SQLcl commands. Release notes ghi các bug/fix cho package/package body, synonym, quoted name và DDL được sinh, vì vậy migration sinh tự động vẫn cần review và verify. [`SQLcl 26.1 release notes`](https://www.oracle.com/tools/sqlcl/sqlcl-relnotes-26.1.0.html), [`26.3 changelog`](https://www.oracle.com/tools/sqlcl/sqlcl-changelog.html).
- **DOC — Git/CI:** project docs mô tả so sánh Git branch và tạo/deploy artifact; approval và quyền truy cập do Git hosting/CI cung cấp. Mỗi SQLcl client dùng connection đã cấu hình; chưa thấy inventory/service tập trung cho database. [Project/Git/artifact guide](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/26.1/sqcug/project.html).
**License (DOC):** Oracle cho tải SQLcl miễn phí theo Free Use License; CLI tự host. Hỗ trợ Oracle theo Database Support license hiện có của khách hàng. [`SQLcl download`](https://www.oracle.com/database/sqldeveloper/technologies/sqlcl/download/) (26.3.0.260.1620, 29/09/2026; Oracle Free Use License).

Quy trình này có thể cải thiện đáng kể đường đi từ phát triển đến phát hành: export source, tạo/review migration, kiểm tra, đóng gói artifact có version rồi deploy chính artifact đó. Nó giảm script DBeaver tùy hứng, nhưng UX Project được tài liệu mô tả chưa giải quyết chọn nhiều target và lưu trạng thái tập trung cho cả estate. Cần wrapper/service quản lý inventory, nhóm target, credential vault, approvals, rollout có kiểm soát, snapshot/kết quả kiểm tra và audit tổng hợp. Cần xác minh trên DB thử để Project và Liquibase độc lập không ghi hai lịch sử xung đột hoặc chạy trùng; chỉ định một executor duy nhất. Deploy lỗi cần dừng và báo trạng thái; artifact bất biến không có nghĩa target atomic. Oracle implicit commit đòi hỏi reconcile phần đã áp dụng.

Pin phiên bản: trang tải Oracle xác nhận bản mới nhất là SQLcl **26.3.0.260.1620**, phát hành 29/09/2026, theo Oracle Free Use License; User Guide 26.1 (05/2026) là tài liệu chi tiết đã dùng cho Project/Liquibase. Changelog 26.2 và 26.3 cho thấy Project/Liquibase tiếp tục được cập nhật, nên tài liệu 26.1 có thể chưa bao quát feature mới nhất. Không tải hoặc chạy binary. [`SQLcl changelog/latest 26.3`](https://www.oracle.com/tools/sqlcl/sqlcl-changelog.html), [`26.1 project guide`](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/26.1/sqcug/project.html), [`26.1 Liquibase command reference`](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/26.1/sqcug/liquibase.html), [`26.1 release notes`](https://www.oracle.com/tools/sqlcl/sqlcl-relnotes-26.1.0.html).

<a id="tool-dbpm"></a>

### dbpm (workflow package Oracle bổ sung)

Giữ dbpm trong catalog dù thiếu target ledger tập trung, vì quản lý package/dependency có ích cho release ứng dụng Oracle.

- **DOC — mô hình package/dependency:** manifest package, lockfile, giới hạn phiên bản và phân giải dependency; artifact từ GitHub Packages/registry tương thích Maven hoặc registry công khai; có lệnh plan, lock, install, upgrade, reinstall, publish. [`dbpm README`](https://github.com/512itconsulting/dbpm), [`install semantics`](https://github.com/512itconsulting/dbpm/blob/main/docs/commands/install.md).
- **DOC — thực thi trên target Oracle:** cần Python 3.11+, SQLcl hoặc SQL*Plus và cài dbpm Core trong schema target; có lockfile theo ứng dụng, runner, cấu hình target và Core. Core là lớp ghi nhận/deploy trong database, không phải server trung tâm chọn trong 50 DB. README nói cài CLI không tự chọn Oracle DB hay tạo môi trường deploy cấp hệ thống. [README tại pin đã kiểm](https://github.com/512itconsulting/dbpm/blob/ef810bd2185110c7acb44493431f76def1de4216/README.md).
- **DOC — pin release/provenance:** lockfile ghi version/package artifact; CLI có `plan`, `lock`, dry-run/approve, install/upgrade; hỗ trợ publish package và cấu hình signing key. `--approve` là cờ cho một lần gọi CLI, không phải quy trình approval đa người dùng hay phân tách nhiệm vụ. [Install command](https://github.com/512itconsulting/dbpm/blob/ef810bd2185110c7acb44493431f76def1de4216/docs/commands/install.md).
- **DOC — CI/API và giới hạn:** có thể gọi CLI từ CI và dùng thông tin xác thực để truy cập package registry; README chính thức chưa chứng minh API tập trung, portal user/role, inventory hay release coordinator cho 50 target. Cần hệ thống bên ngoài đọc manifest target, điều phối và tổng hợp kết quả, secrets, approvals. [CLI/CI interface trong README](https://github.com/512itconsulting/dbpm/blob/ef810bd2185110c7acb44493431f76def1de4216/README.md).
**License (DOC/SOURCE đã kiểm):** hai repository công khai đều khai báo Apache-2.0: CLI dbpm và Core được liên kết. README Core ghi rõ license Apache 2.0; trang upstream `dbpm.io/core` mô tả mã nguồn mở. Đây là bằng chứng công khai cho source/Core manifest, không phải ý kiến pháp lý độc lập về mọi package/artifact/dịch vụ registry. Không tìm thấy giá thương mại cho CLI/Core; cần xem riêng điều khoản dịch vụ registry. [`Core README/license`](https://github.com/512itconsulting/core), [`Core site`](https://dbpm.io/core/), [`Core LICENSE`](https://github.com/512itconsulting/core/blob/22f942db3ac1826a81502d63dbeccaf61d4e8580/LICENSE).

Kiểm tra source hiện tại (chỉ đọc `git ls-remote`, 07/10/2026): HEAD nhánh `main` của dbpm là `ef810bd2185110c7acb44493431f76def1de4216`, khớp snapshot kế thừa; Git tags công khai có `v1.5.0` (tag ref `e6b61c04cbc5e8e4c7c9f16b22a74074a551ce17`), trong khi changelog repo ghi 1.5.3 (10/09/2026) và truy vấn tag không trả `v1.5.3`. Chưa xác lập được source HEAD và artifact/release version là cùng một pin; coi HEAD là pin đọc source chưa gắn tag, không suy danh tính artifact 1.5.3 từ đó. [`main @ ef810...`](https://github.com/512itconsulting/dbpm/tree/ef810bd2185110c7acb44493431f76def1de4216), [`v1.5.0 tag`](https://github.com/512itconsulting/dbpm/tree/v1.5.0), [`repo changelog/history`](https://github.com/512itconsulting/dbpm/blob/main/CHANGELOG.md).

HEAD `main` công khai mới nhất của Core được kiểm tra chỉ đọc là **`22f942db3ac1826a81502d63dbeccaf61d4e8580`**. Repository không có GitHub Releases và truy vấn tag chỉ đọc không trả tag công khai; README Core nói dự án được phát triển/kiểm thử với Oracle 19c, đang phát triển tích cực và API có thể thay đổi. Do đó dùng commit này làm pin đọc source, không coi là artifact phát hành theo semver. [`Core @ checked HEAD`](https://github.com/512itconsulting/core/tree/22f942db3ac1826a81502d63dbeccaf61d4e8580), [`Core releases (none listed)`](https://github.com/512itconsulting/core/releases). Tài liệu công khai của repository/README/LICENSE Core giải quyết điểm chưa rõ về license: mã nguồn Apache-2.0; không tìm thấy license thương mại Core riêng trong các tài liệu công khai này. Đây là bằng chứng **DOC/SOURCE**, không phải kiểm chứng runtime/recovery của Core.

So với chạy SQL thủ công, dbpm xử lý version/dependency của PL/SQL package tái sử dụng, khóa artifact và provenance, thay vì chỉ chạy migration schema theo thứ tự. Không nên coi nó thay Flyway/Liquibase cho các release SQL tổng quát trên nhiều DB nếu chưa thử use-case đại diện. Muốn vận hành toàn estate vẫn cần inventory target toàn cục, request/review/approval, access control, rollout từng đợt, reconcile theo target, bằng chứng audit và stop/resume.

<a id="tool-gitora"></a>

### Gitora Version Control

**Vai trò:** commercial Oracle object source control và developer collaboration. Có thể dùng nguyên trạng cho Git/PL/SQL collaboration; rollout có approval trên toàn estate cần kiểm thêm hoặc ghép CI/CD.

**Năm tính năng có nguồn:**

1. **DOC:** chọn object để đưa vào Git, theo dõi thay đổi database object và liên kết Git repository với database. [Version control](https://www.gitora.com/version_control.html).
2. **DOC:** branch/merge/reset/pull cập nhật code object trong DB; tạo diff script giữa commit points và chuyển code giữa DB. [Version control](https://www.gitora.com/version_control.html), [gói Version Control](https://www.gitora.com/buy.html).
3. **DOC:** quyền ở repo/object và cộng tác cùng code trong một DB hoặc DB riêng, giúp giảm ghi đè package của đồng nghiệp. [Version control](https://www.gitora.com/version_control.html).
4. **DOC:** bản 6.4 công bố tùy chọn **Enforce Compilation**: chỉ commit object hợp lệ; bản 6.5 yêu cầu commit message tham chiếu Jira issue có thật khi cấu hình tích hợp. [Thông báo 6.4/6.5 trên blog chính thức](https://blog.gitora.com/page/2/).
5. **DOC:** Enterprise API cho commit/branch/reset; có push/pull GitHub, GitLab, Bitbucket. [API documentation](https://blog.gitora.com/gitora-api-documentation/), [gói tích hợp Git](https://www.gitora.com/buy.html).

**Oracle:** sản phẩm dành riêng Oracle/PL/SQL và object lifecycle. Không đánh đồng object source control với mọi DML/backfill/table migration. Chưa tìm được support matrix hiện hành cho từng Oracle release trong nguồn đã mở; không suy Oracle 11g/19c/21c từ ví dụ JDBC. Enforce Compilation là gate **trước commit**, không bằng chứng postdeploy validity hoặc recovery cho 50 target.

**Nhiều DB/user/release và failure:** tài liệu mô tả cùng/separate DB, diff/pull giữa DB; web Editor Home có danh sách database/user. Chưa chứng minh target-group rollout, approval tách requester/executor, release ledger từng DB hay resume sau partial DDL. Reset Git hoặc checkout branch không tự phục hồi dữ liệu đã mất. [Editor Home và role](https://blog.gitora.com/page/2/), [tính năng Version Control](https://www.gitora.com/version_control.html).

**License/self-host/giá:** proprietary subscription, trial có form và điều khoản; không phải OSS. Bảng hiện tại **300 USD/user/năm**, tối thiểu 5 users; 20 users tương ứng phép tính niêm yết **6.000 USD/năm**, chưa gồm thuế, giảm giá, phạm vi database/automation/service users hoặc module For Data. For Data là gói riêng; không cộng tính năng/gía nhầm sang Version Control. Hình thức app/API chạy bên cạnh Oracle là self-host theo hướng dẫn hãng; không tải installer hoặc chấp nhận trial terms trong lượt này. [Giá](https://www.gitora.com/buy.html), [download và điều khoản](https://www.gitora.com/download.html).

**Giá trị/công bổ sung:** đáng xem nếu khó khăn nằm ở nhiều developer cùng sửa package/procedure và code DB không khớp Git. Flyway quản lý script theo phiên bản; Gitora bổ sung luồng object và branching ở database. Cần chọn schema/object, quyền ứng dụng DB, Git remote, Jira, backup và CI approval; release rộng cần target manifest, runner, postcheck và audit correlation. Chưa có SOURCE implementation/RUNTIME.

**Pin/ngày:** trang download kiểm 07/10/2026 hiển thị **7.1.3 build 33**. Chỉ là DOC về phiên bản được cung cấp; không có source pin, binary hash hay ngày phát hành được kiểm. API doc nói 6.2+ và dùng nhãn Enterprise cũ; cần xác minh entitlement của API trong hợp đồng 7.x.

<a id="tool-oem"></a>

### Oracle Enterprise Manager + Database Lifecycle Management Pack

**Vai trò:** commercial Oracle estate administration và schema change management. Dùng nguyên trạng cho inventory/baseline/comparison/change plans khi có pack phù hợp; CI/Git release convention cần tích hợp.

**Bốn tính năng có nguồn:**

1. **DOC:** central console quản lý database targets và quyền quản trị; Job System, credentials, target groups là hạ tầng quản lý tập trung. [Base functionality](https://docs.oracle.com/en/enterprise-manager/cloud-control/enterprise-manager-cloud-control/24.1/oemli/enterprise-manager-base-functionality.html).
2. **DOC:** schema baseline/comparison/synchronization ghi và so sánh metadata giữa DB hoặc baseline. [Change Plans](https://docs.oracle.com/en/enterprise-manager/cloud-control/enterprise-manager-cloud-control/24.1/emlcm/using-change-plans.html).
3. **DOC:** Change Plan đóng gói change requests; sinh script và impact report **cho từng destination DB**, DBA kiểm và schedule execution job. [Change Plans](https://docs.oracle.com/en/enterprise-manager/cloud-control/enterprise-manager-cloud-control/24.1/emlcm/using-change-plans.html).
4. **DOC:** quyền View/Edit/Manage Change Plan, external SQL Developer client và job output/error/retry có hướng dẫn cụ thể. [Change Plans](https://docs.oracle.com/en/enterprise-manager/cloud-control/enterprise-manager-cloud-control/24.1/emlcm/using-change-plans.html).

**Oracle/nhiều DB/release:** native Oracle targets, một plan có thể đi tới nhiều destination; phù hợp DBA dùng metadata để triển khai thay đổi thay vì tự gom script. Chưa xác minh managed-target version certification: download page chuyển certification matrix sang My Oracle Support, là dữ liệu chưa truy cập. Cách Oracle đếm DB instance/PDB/schema target khác số connection và seat. [Downloads/certification](https://www.oracle.com/enterprise-manager/downloads/).

**Git/CI/API và failure:** có EM CLI/REST base framework; Git immutable artifact, CI trigger, approval binding và per-target release ID/checksum cần adapter/convention hoặc xác minh feature cụ thể. Tài liệu mô tả operator xem impact warnings/output, sửa nguyên nhân rồi Retry Script Execution; không hứa auto-revert Oracle DDL. DBA review quyền hạn khác một approval workflow bắt buộc đã chứng minh. [Base APIs](https://docs.oracle.com/en/enterprise-manager/cloud-control/enterprise-manager-cloud-control/24.1/oemli/enterprise-manager-base-functionality.html), [failure procedure](https://docs.oracle.com/en/enterprise-manager/cloud-control/enterprise-manager-cloud-control/24.1/emlcm/using-change-plans.html).

**License/self-host:** proprietary, triển khai OMS/Oracle repository/agents tại chỗ. Base functionality không đồng nghĩa miễn phí Change Management. Licensing guide 24.1 xếp schema comparison/synchronization và menu Change Management vào **Database Lifecycle Management Pack**; Change Management Pack còn mục Legacy riêng. Giá phụ thuộc Oracle license/metrics/hợp đồng, chưa có tổng cho 50 DB/20 users; chưa biết đơn vị đã có pack. [Pack licensing](https://docs.oracle.com/en/enterprise-manager/cloud-control/enterprise-manager-cloud-control/24.1/oemli/enterprise-database-management.html), [on-prem download](https://www.oracle.com/enterprise-manager/downloads/).

**Giá trị/công bổ sung:** mạnh ở inventory Oracle và thay đổi dựa metadata/impact report; đáng xem khi đã có OEM/DBA vận hành, giảm công xây một inventory khác. Cần cấu hình OMS/repository/agents, target groups, named credentials, baseline, quyền và Git/CI link. Nếu chưa có nền tảng, effort vận hành phải so với platform nhẹ hơn; không ước lượng chi phí nội bộ khi chưa biết năng lực nhóm. Chưa có SOURCE/RUNTIME.

**Pin/ngày:** kiểm 07/10/2026, downloads công khai **24ai Release 1 (24.1.0.0.0)** và docs 24.1. Đã thấy official announcement RU01 và tài liệu có các RU mới hơn; đây là pin docs/base release đã kiểm, **không tuyên bố RU01/base là patch mới nhất**. Patch/certification/entitlement chính xác còn sau MOS; không tải hay deploy.

<a id="tool-rundeck"></a>

### Rundeck Community và Runbook Automation

**Vai trò (DOC):** Rundeck điều phối automation jobs và runbooks; không có Oracle migration engine.

**Tính năng chính (DOC):**

1. Gom automation jobs vào project, chọn node qua resource model/filter, truyền options khi chạy ([Projects/Nodes](https://docs.rundeck.com/docs/manual/), [API](https://docs.rundeck.com/docs/api/)).

2. Xâu chuỗi job steps, điều kiện, notification và plugin thành workflow ([Jobs guide](https://docs.rundeck.com/docs/manual/jobs/)).

3. Phân quyền theo project/job/node/command/API bằng ACL policy ([ACL](https://docs.rundeck.com/docs/administration/security/authorization.html)).

4. Import/export job definitions với Git; SCM actions có thể điều khiển qua API ([Git SCM](https://docs.rundeck.com/docs/manual/projects/scm/git.html), [API](https://docs.rundeck.com/docs/api/)).

**Oracle và multi-target.** Không phải Oracle schema tool. Có thể tạo node đại diện DB/server, lọc node theo thuộc tính, rồi gọi script/Ansible/SQL client hoặc plugin. Node inventory cần đồng bộ từ nguồn khác hoặc tự duy trì; một DB có nhiều schema nên mô hình node không tự giải quyết state mỗi schema. Job options giúp người chạy chọn tham số/target, nhưng phải thiết kế allowlist/ACL để tránh target tùy ý. Job/execution log cho biết điều phối đã chạy và kết quả command; không chứng minh schema đúng phiên bản nếu script không tự kiểm tra.

**Release và thất bại.** Workflow có thể tuần tự hóa batch (ví dụ canary → nhóm còn lại), điều kiện nhánh và notifications; API cho trạng thái job. Lỗi command có thể dừng/đánh dấu workflow theo cấu hình. Recovery, retry idempotent, đối chiếu migration history và forward-fix là việc của script/migration engine. Git SCM quản lý job definitions, không tự biến SQL change thành migration release. Rundeck Community được ghi Apache-2.0 tại [GitHub repo](https://github.com/rundeck/rundeck); self-host được, không có quota thương mại theo 50 DB nêu ở tài liệu nguồn. Runbook Automation là sản phẩm thương mại có hỗ trợ và enterprise capabilities; license phải mua/quote, không thấy giá public: [licensing](https://docs.rundeck.com/docs/administration/license.html), [enterprise distribution](https://docs.rundeck.com/docs/enterprise/).

**Pin:** Rundeck `v6.2.1-20260909`, GitHub release hiển thị commit `e649f08`; release calendar ghi phát hành 09/09/2026 ([release](https://github.com/rundeck/rundeck/releases), [calendar](https://docs.rundeck.com/docs/history/release-calendar.html)). Đây là pin kiểm tra được, không phải phiên bản cài hoặc runtime thử nghiệm.

**Giá trị và ghép nối.** Có thể bổ sung cổng chạy tập trung, lựa chọn nhóm target, phân quyền vận hành và lịch sử runbook lên quy trình đang chạy Flyway CLI. Để thành DB release workflow cần kết hợp Flyway/Liquibase/SQLcl hoặc tool schema khác, inventory/schema registry, policy/review/approval và bước verify state. Lựa chọn nên được cố định từ inventory/ACL thay vì để người chạy nhập chuỗi kết nối tự do.

<a id="tool-awx"></a>

### AWX và Ansible Automation Platform Controller

**Vai trò (DOC):** AWX cung cấp UI/API cho Ansible automation, inventory và workflow; Automation Controller là bản thương mại của Red Hat.

**Tính năng chính (DOC):**

1. Quản lý inventories/hosts/groups, projects, credentials và templates qua UI/API ([AWX source](https://github.com/ansible/awx), [OpenAPI](https://docs.ansible.com/projects/awx/en/latest/open_api/)).

2. Xâu chuỗi job, project/inventory sync và nested workflows; nhánh success/failure/always và song song ([workflows](https://docs.ansible.com/projects/awx/en/24.6.1/userguide/workflows.html)).

3. Chèn approval node có timeout/người có quyền duyệt, rồi ghi activity/job result ([workflow templates](https://docs.ansible.com/projects/awx/en/24.6.1/userguide/workflow_templates.html), [UI/activity](https://docs.ansible.com/projects/awx/en/24.6.1/userguide/main_menu.html)).

4. Cấp quyền resource cho user/team qua RBAC ([RBAC](https://docs.ansible.com/projects/awx/en/24.6.1/userguide/rbac.html)).

**Oracle và multi-target.** AWX không có schema migration engine Oracle. Có thể dùng inventory host/group vars và `limit` để chọn danh sách Oracle endpoint hoặc runner host; Ansible execution environment chạy `sqlplus`, JDBC utility, hoặc module/collection phù hợp. Oracle client, wallet/driver, secret backend, module version và kết nối mạng đều cần cấu hình. Inventory không tự phản ánh schema versions; cần custom inventory plugin/source và playbook query/collect trạng thái (nếu được cho phép) hoặc nguồn CMDB. Workflow approval node cho phép chặn trước stage; người có quyền execute workflow hoặc org admin/approver được chỉ định có thể duyệt.

**Release và thất bại.** Workflow graph có thể chạy precheck, deploy theo nhóm, verify, rồi chỉ đi tiếp khi job thành công; nhánh lỗi cho notification/stop/diagnostic. Job output/event lưu kết quả automation. Không có migration ledger hay Oracle DDL rollback tự động: playbook cần idempotency, checkpoint, verify SQL, forward-fix và quy định xử lý DDL dở dang. API v2 quản lý workflow/inventory/job; project có thể sync Git.

**License/giá.** AWX source Apache-2.0 theo [LICENSE](https://github.com/ansible/awx/blob/devel/LICENSE.md), self-host; không tính seat/target phí từ project OSS. Release page hiện pin mới nhất được hiển thị là `24.6.1`, ngày 02/07/2024 và commit `94e5795`; README nói tạm dừng releases trong đợt refactor lớn; đây là bản phát hành gần nhất, không phải tuyên bố kết thúc dự án. Cần cân nhắc tình trạng release/upstream ([release](https://github.com/ansible/awx/releases), [repo](https://github.com/ansible/awx)). Automation Controller là sản phẩm thương mại Red Hat, license/support quote; khác AWX OSS.

**Giá trị và ghép nối.** Hữu ích nếu đội đã dùng Ansible để quản trị Oracle hosts/clients, muốn inventory, credentials, staged execution và approval UI. So với DBeaver/Flyway CLI giảm thao tác chọn/chạy từng DB, nhưng để an toàn phải tự duy trì target-to-schema inventory, migration runner, policy kiểm SQL, schema state audit và recovery. Với 20 người cần kiểm chứng quyền ở từng inventory/template; không giả định “20 user free” nếu chuyển sang Red Hat Controller.

<a id="tool-jenkins"></a>

### Jenkins

**Vai trò (DOC):** Jenkins là CI/CD engine tổng quát, dùng pipeline code và agents để điều phối công cụ bên ngoài.

**Tính năng chính (DOC):**

1. Jenkinsfile định nghĩa stages/steps trong code, lưu ở SCM để review cùng app/migration code ([Pipeline](https://www.jenkins.io/doc/book/pipeline/), [Pipeline as Code](https://www.jenkins.io/doc/book/pipeline/pipeline-as-code/)).

2. Build history lưu trạng thái/log mỗi lần chạy; multibranch xử lý branch/PR ([Pipeline](https://www.jenkins.io/doc/book/pipeline/)).

3. Input step tạm dừng stage để duyệt, giới hạn người duyệt qua `submitter` ([syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)).

4. Credentials được mã hóa và giới hạn theo folder/item; plugins thêm steps và tích hợp ([security](https://www.jenkins.io/doc/book/security/credentials/), [steps](https://www.jenkins.io/doc/pipeline/steps/)).

**Oracle và multi-target.** Không quản lý DB inventory native. Jenkins pipeline có thể đọc manifest trong Git/CMDB, map target label → connection credential, rồi chạy Flyway/Liquibase/SQLcl/SQL*Plus ở agent/container. Driver/client phải cài và agent có network path đến Oracle. Có thể fan-out theo matrix hoặc tuần tự theo target; concurrency, batch, canary và selection logic do Jenkinsfile/shared library tự thiết kế. Không để pull request không tin cậy truy cập production secrets; tài liệu cảnh báo multibranch PR và credential scope.

**Review, release, failure.** PR review của pipeline/migration diễn ra trong Git provider; input stage là approval thủ công, không phải DB-specific approver workflow hoặc risk classifier. Build log, artifact, commit và step output tạo chứng cứ thực thi; không tự phát hiện drift hoặc xác minh schema ngoài lệnh được khai báo. Pipeline có thể stop/branch/retry theo logic, nhưng Oracle DDL transaction semantics/recovery là của migration layer/runbook.

**License/giá.** Jenkins core MIT, self-host miễn phí ([repo/license](https://github.com/jenkinsci/jenkins/blob/master/LICENSE.txt)); chi phí thực nằm ở vận hành controller/agents/plugins, support tùy nhà cung cấp. Không có giới hạn sản phẩm 50 DB/20 user được xác nhận trong nguồn đã kiểm. **Stable LTS pin kiểm ngày 07/10/2026:** `2.580.1`, phát hành 30/09/2026 theo [official LTS changelog](https://www.jenkins.io/changelog-stable/); GitHub release/source cũng có tag tương ứng. `2.581` là weekly line và không còn được dùng làm pin stable đề xuất ([GitHub releases](https://github.com/jenkinsci/jenkins/releases)).

**Giá trị và ghép nối.** Tốt khi đã có Jenkins và nhóm DevOps đủ khả năng code pipeline: tái sử dụng CI, Git, secrets, agents, approvals. Đối với nhiệm vụ DB, ghép migration engine, registry/manifest 50 instance, naming/ownership, review/check policy, per-environment approver, post-run verification, evidence retention và retry/recovery. So với DBeaver là automation/repeatability; so với Flyway CLI là orchestration/governance tự xây.

<a id="tool-octopus"></a>

### Octopus Deploy

**Vai trò (DOC):** Octopus điều phối release/deployment và runbooks qua các môi trường; Oracle schema execution cần engine bên ngoài.

**Tính năng chính (DOC):**

1. Đăng ký targets theo environments; tag chọn tập target để process chạy ([target model](https://octopus.com/docs/best-practices/deployments/environments-and-deployment-targets-and-roles)).

2. Lifecycle điều khiển thứ tự promotion, điều kiện triển khai trước khi đi tiếp và retention ([lifecycles](https://octopus.com/docs/releases/lifecycles)).

3. Release snapshot promote qua environments; runbooks dùng cho tác vụ vận hành ngày 2 ([getting started](https://octopus.com/docs/getting-started), [runbooks](https://octopus.com/docs/runbooks/)).

4. Approval rules, RBAC, audit events và deployment API ([approvals](https://octopus.com/docs/approvals/octopus-approvals), [audit](https://octopus.com/docs/security/users-and-teams/auditing), [API](https://octopus.com/docs/api/deployments)).

**Oracle và multi-target.** Không phải Oracle migration engine. 50 Oracle có thể biểu diễn thành targets/server/worker hoặc tenant/resource qua script deployment; target selection theo Environment + target tag, không hard-code danh sách trong process. Nhưng DB endpoint/schema account không đồng nhất với machine deploy target; thiết kế biến/secret, network worker và cách đếm target/machine cần POC. Script gọi Flyway/Liquibase/SQLcl/JDBC. Runbook/Deployment task logs ghi output/target/status; schema result cần explicit verification step.

**Approval/recovery.** Lifecycle promotion điều khiển stage order, manual/automatic promotion; approval rules có thể áp vào project/environment deployment và runbook qua [Octopus Approvals](https://octopus.com/docs/approvals/octopus-approvals). Deployment failure có task logs/guided failure option/API; rollback application/package có cơ chế riêng, nhưng database rollback phụ thuộc script/migration engine và Oracle DDL không được coi như auto-undo. Audit ghi create/edit/delete và ai khởi tạo; tài liệu nêu không audit mọi hành vi đọc.

**License/giá.** Có thể self-host Octopus Server hoặc dùng cloud; thương mại. Trang Free hiện nêu 10 projects, 10 tenants, 10 machines, 10 users; 20 người vượt user limit. **Không đồng nhất 50 DB với 50 machines**: machine count phụ thuộc kiểu đăng ký target; nếu mỗi DB/schema được mô hình hóa thành machine target thì chạm/vượt cap, còn dùng worker/tenant/script có cách tính khác cần vendor xác nhận. Professional/Enterprise tính theo project, tenants/machines là add-on; public pricing pages đang hiển thị mức annual khác nhau, nên quote theo cấu hình thực tế ([pricing overview](https://octopus.com/pricing/overview), [free/pricing](https://octopus.com/free)). Không tìm thấy source server OSS; proprietary thương mại.

**Pin:** Trang download self-host chỉ định **Octopus Server 2026.3.15878** là latest ngày 07/10/2026, kèm installer/checksum; release history tại cùng lần kiểm cũng ghi **2026.3 build 15878** là bản khuyến nghị self-host. Đây là binary pin công khai, không có source pin vì proprietary ([downloads](https://octopus.com/downloads), [release history](https://octopus.com/downloads/previous)). Không runtime.

**Giá trị và ghép nối.** Có thể cung cấp inventory targets, release snapshots, promotion, RBAC, approval, audit/task logs cho rollout nhiều Oracle. Thành phần DB change vẫn cần Flyway/Liquibase/DBmaestro, schema baseline/drift check, Oracle-specific validation/recovery. Hợp với tổ chức đã có CD governance và chấp nhận commercial; kiểm kỹ phí 50 targets và 20 users.

<a id="tool-harness"></a>

### Harness Database DevOps

**Vai trò (DOC):** Harness Database DevOps tích hợp DB instance/schema và changelog vào pipeline Harness. [Oracle guide](https://www.harness.io/blog/oracle-database-devops-automating-schema-changes-for-oracle) ngày 29/09/2026 mô tả JDBC Thin, TCPS, Kerberos và SYS AS SYSDBA; chưa kiểm runtime/support matrix cho Oracle nội bộ.

**Tính năng chính (DOC):**

1. DB Instance step cho chọn DB instance và schema; module tích hợp Liquibase-compatible changelog và Flyway workflow ([schema sync](https://developer.harness.io/database-devops/3.0/use-db-devops/changelogs-and-schema-changes/liquibase/schema-synchronization), [product](https://www.harness.io/products/database-devops)).

2. `changelog-sync` baselines một schema bằng cách đánh changesets executed mà không chạy DDL; `diff-changelog` tạo changelog từ DB state ([sync, updated 16/07/2026](https://developer.harness.io/database-devops/3.0/use-db-devops/changelogs-and-schema-changes/liquibase/schema-synchronization), [diff, updated 02/07/2026](https://developer.harness.io/database-devops/3.0/use-db-devops/create-database-updates/diff-changelog)).

3. Pipeline policy/approval/audit và schema visibility theo environments ([product capabilities](https://www.harness.io/products/database-devops)).

4. DB instance có thể pin theo Git SHA trong pipeline, theo release note tháng 07/2026 ([release note](https://www.harness.io/blog/shipped-in-july-2026)).

5. `Tag Database Changeset` tạo post-deployment tag ngay cả khi lần chạy no-op, nhằm duy trì rollback anchor ([feature doc, updated 24/06/2026](https://developer.harness.io/database-devops/use-db-devops/deployment-pipeline-configuration/rollback-and-failure-strategies/tag-database-changeset)).

**Oracle và target.** Có hỗ trợ Oracle database qua JDBC; Harness Delegate chạy trong network riêng/VPC/Kubernetes nên control plane SaaS không cần truy cập trực tiếp DB. Model DB Instance và DB Schema chọn rõ trong step giúp giảm ambiguity giữa 50 instances và schemas. Changelogs nằm Git; baseline existing state, approval gate/risk policy, deploy theo environment stages, xem changeset status/diff và audit theo pipeline. Với 50 instance cần xem cách import/label/group/scope quyền, bulk onboarding, credential management và giới hạn concurrency/instance trong POC.

**Failure/recovery.** Product page tuyên bố rollback automation/audit/visibility; tuy vậy Oracle DDL không transactional. Harness orchestration không tự làm mọi DDL reversible: cần Liquibase rollback definition hoặc Flyway undo/forward repair, preflight, postdeploy verify và policy. Tài liệu changelog-sync nói rõ đánh dấu change đã chạy mà không thực thi DDL; baseline cần kiểm state thật trước. Release note tháng 07/2026 ghi khả năng pin DB instance theo Git SHA.

**License/giá.** Thương mại Harness Database DevOps, không phải module OSS; SaaS/control plane cùng Delegate self-hosted. Public pricing cho đúng 50 instance/20 users/DB DevOps module chưa thấy; yêu cầu quote, không suy từ free tier/giá Harness CI chung. Không có source/binary pin công khai áp dụng. **Tài liệu tính năng có dấu mốc công khai gần đây:** changelog-sync cập nhật 16/07/2026, diff-changelog cập nhật 02/07/2026, Kerberos Oracle/MSSQL cập nhật 10/08/2026; đây là dated feature docs, không phải product build version ([sync](https://developer.harness.io/database-devops/3.0/use-db-devops/changelogs-and-schema-changes/liquibase/schema-synchronization), [diff](https://developer.harness.io/database-devops/3.0/use-db-devops/create-database-updates/diff-changelog), [Kerberos](https://developer.harness.io/database-devops/3.0/use-db-devops/database-authentication-and-security/kerberos-authentication)). Public product screenshots/webinar là demo hãng, chưa runtime độc lập.

**Giá trị và ghép nối.** Trong nhóm này sản phẩm này tiến gần nhất tới “nguyên trạng” cho inventory DB/schema + Git changeset + pipeline deploy/governance/audit; còn phải dùng migration engine convention, seed inventory/credentials, define policy/approval, kiểm Oracle versions, build verify/recovery. So với DBeaver/Flyway CLI giảm việc chọn từng connection và gom execution state; ưu thế quyết định cần chứng minh bằng POC target selection, least privilege, schema state, release failure một phần và audit export.

<a id="tool-dbmaestro"></a>

### DBmaestro

**Vai trò (DOC):** DBmaestro là sản phẩm thương mại cho database source control và release automation, gồm quản lý database objects và drift.

**Tính năng chính (DOC):**

1. Source-control history/audit cho schema, procedure và metadata; check-in/check-out/object lock ([source control](https://www3.dbmaestro.com/database-source-control-made-easy)).

2. Release automation có dry-run, dependency validation/conflict checks và deployment automation theo hãng ([platform](https://www.dbmaestro.com/), [FAQ](https://www.dbmaestro.com/faq/)).

3. Drift/schema scan và visibility theo baseline/environments ([FAQ](https://www.dbmaestro.com/faq/)).

4. Governance/RBAC/approval/audit và CI integrations (Jenkins, Azure DevOps, GitLab, GitHub Actions) ([FAQ](https://www.dbmaestro.com/faq/), [platform](https://www.dbmaestro.com/)).

**Oracle và multi-target.** Vendor liệt kê Oracle native support; source control giữ object-level changes và release automation quản lý database/schema connections/environments. Giá tính theo số environment (database/schema connections) trong release pipelines theo pricing page; với 50 instance phải quote số connections thực (mỗi instance/schema có thể nhân lên), không giả định 50 license chính xác. CI orchestration tích hợp Git/CI; platform tự nhận nhiệm vụ source control/release, nhưng cần xem UI/API inventory bulk import, target naming, RBAC theo target, parallelism và cách chọn 1/nhóm DB trong demo.

**Failure/recovery.** Hãng quảng bá dry-run, impact analysis, drift/conflict prevention, audit, backout strategies và deployment monitoring. Cần xác minh Oracle DDL case thật: package invalidation/dependency, partial deployment, lock/long DDL, schema rollback/backout, repair rồi resume, log export và batch stop/continue. Không có source code public để kiểm implementation; video/web demo chỉ là DOC, không RUNTIME.

**License/giá và hosting.** Thương mại; pricing page nói tính theo số environment/database-schema connections trong release pipeline, không công khai amount ([pricing](https://www.dbmaestro.com/pricing-release-automation/)). FAQ hiện tuyên bố hỗ trợ on-premises và cloud-native databases; đây là khẳng định về database estate, chưa đủ chứng minh control-plane của DBmaestro có gói self-host/on-prem. Một bài vendor cũ nhắc cả lựa chọn on-prem/cloud nhưng không phải install/deployment guide hiện hành ([FAQ](https://www.dbmaestro.com/faq/), [vendor architecture article](https://www.dbmaestro.com/blog/database-automation/devops-automation-for-cloud-databases/)). Không thấy free tier hoặc open-source engine. **Release pin:** chưa tìm được release/build hiện hành công khai; vendor blog ghi 7.5 năm 2018, chỉ dùng làm historical public version reference, không coi current ([release announcement 7.5](https://www.dbmaestro.com/blog/database-devops/dbmaestro-flexibility-compliance/)). Cần xác minh version, support lifecycle, control-plane hosting, Oracle compatibility và licensing trong POC/quote.

**Giá trị và ghép nối.** Đây là candidate chuyên Oracle đáng khảo sát nếu cần source control ở mức database object và governance/release automation, giúp giải bài toán vượt quá migration script runner. Có thể thay nhiều thành phần tự xây, nhưng cần phân định Git artifact ownership vs platform repository, migration engine coexistence với Flyway, API/CI contract, 50-target pricing, per-user RBAC, source of truth, partial-failure recovery. Demo phải đưa SQL thật của hệ thống, không chỉ slide.

<a id="tool-cloudbeaver"></a>

### CloudBeaver Community / Enterprise

**Vai trò:** shared browser SQL workbench và connection administration. Dùng nguyên trạng cho truy cập tập trung; quản lý release phải ghép engine/workflow.

**Bốn tính năng có nguồn:**

1. **DOC:** private/shared connections thuộc project; shared connection cho nhiều user/team, quyền truy cập do admin quản lý. [Create connection](https://dbeaver.com/docs/cloudbeaver/Create-Connection/).
2. **DOC:** browser SQL editor, metadata/data editor, query history và SQL scripts là luồng làm việc chung. [SQL Editor](https://dbeaver.com/docs/cloudbeaver/SQL-Editor/), [README tại pin](https://github.com/dbeaver/cloudbeaver/blob/3b8d453bf36685e3d7aa4073244e252d25a9364d/README.md).
3. **SOURCE:** server bật driver `oracle:oracle_thin` và resource/bundle Oracle; không chỉ generic JDBC claim. [plugin.xml tại pin](https://github.com/dbeaver/cloudbeaver/blob/3b8d453bf36685e3d7aa4073244e252d25a9364d/server/bundles/io.cloudbeaver.resources.drivers.base/plugin.xml).
4. **DOC, trả phí:** audit panel từ 26.0 ghi API/auth/connection/SQL/user events và có export, chỉ Enterprise/AWS/GCP. Enterprise còn secret provider; không gán cho CE. [Audit Logging](https://dbeaver.com/docs/cloudbeaver/Audit-Logging/), [secret provider boundary](https://dbeaver.com/docs/cloudbeaver/Create-Connection/).

**Oracle/50 DB/20 người:** [Supported databases](https://github.com/dbeaver/cloudbeaver/wiki/Supported-databases) liệt kê Oracle; code driver trên được đọc. Chưa xác minh Oracle version/auth/TCPS và user concurrency; không thừa hưởng toàn bộ feature/version matrix của DBeaver Desktop sang browser. Shared connections có thể nhập nhiều endpoint, phân quyền user/team; không thấy cap 50/20 trong các nguồn đã kiểm, **không coi là load/cap test**. Không có release artifact, approval/promotion/target migration ledger đã chứng minh trong editor path.

**Git/CI/API/license:** có GraphQL/API documentation ở [DBeaver docs index](https://dbeaver.com/docs/), nhưng không là native GitOps release endpoint đã kiểm. Community source Apache-2.0 tại [LICENSE pin](https://github.com/dbeaver/cloudbeaver/blob/3b8d453bf36685e3d7aa4073244e252d25a9364d/LICENSE), self-host Docker; Oracle driver và deps có terms riêng. Enterprise thương mại; seat price/tổng 50/20 chưa kiểm đủ. SQL history khác audit compliance và migration state.

**Giá trị/công bổ sung và failure:** là đường gần nhất từ DBeaver desktop tới connection catalog và editor chung; dễ thấy ai được truy cập DB nào. Vẫn cần engine + approved artifact/target mapping + runner để bỏ thao tác SQL release thủ công. Cấu hình connection/project/team, identity, secret, retention và vận hành server. Lỗi SQL ở editor cần xử lý theo session/transaction và Oracle state; query history không là recovery ledger.

**Pin/ngày:** kiểm source 07/10/2026 tại HEAD `3b8d453bf36685e3d7aa4073244e252d25a9364d` (06/10 UTC), đọc plugin/license/README; GitHub latest-release API 404 nên dùng source pin, không bịa release. SOURCE mới giới hạn ba file này; DOC audit hiện hành chưa map vào binary. Runtime **NOT_RUN**.

<a id="tool-dbgate"></a>

### DbGate Community / Team Premium

**Vai trò:** multi-database desktop/web client, schema compare và shared team administration. Native client dùng được; migration governance cần composition.

**Bốn tính năng có nguồn:**

1. **DOC:** SQL console/history, schema compare/sync, import/export và data/model browsing. [README tại pin](https://github.com/dbgate/dbgate/blob/e12eb221652acb4ce1561e630f90c1da72db8268/README.md).
2. **SOURCE + DOC:** CE web cấu hình connection IDs/service name/readonly và quyền login bằng env; Oracle connector dùng `oracledb`, Thin mặc định, Thick gọi `initOracleClient`. [Env configuration](https://docs.dbgate.io/dbgate/customization/env-variables/index.html), [Oracle driver source](https://github.com/dbgate/dbgate/blob/e12eb221652acb4ce1561e630f90c1da72db8268/plugins/dbgate-plugin-oracle/src/backend/driver.js).
3. **DOC, trả phí:** Team Premium có admin UI users/roles/connections, quyền database/table/object đến Run script/Deny; không gán UI quản trị này cho CE. [Administration](https://www.dbgate.io/features/administration/), [permission release](https://www.dbgate.io/news/2025-08-29-6-6-2-team-premium-permissions/).
4. **DOC, trả phí:** audit login/query/import/export và SSO/OAuth2/LDAP; không có bằng chứng SQL approval trước rollout. [Administration/audit](https://www.dbgate.io/features/administration/), [Team Premium](https://www.dbgate.io/editions/team-premium/).

**Oracle/multi-target/release:** Oracle connector thật được đọc; Thick cần Instant Client và driver/client license riêng. Release 7.3.1 không tự xác nhận PL/SQL script recovery hoặc schema-sync object coverage. 50 connection có thể là cấu hình web/central admin, 20 users là login/role; không native immutable release, cross-environment approval hoặc target ledger đã chứng minh. Schema sync là thao tác client, không tự thành estate rollout.

**Git/CI/API/license:** CE/source và Oracle plugin GPL-3.0; [LICENSE](https://github.com/dbgate/dbgate/blob/e12eb221652acb4ce1561e630f90c1da72db8268/LICENSE), [plugin package](https://github.com/dbgate/dbgate/blob/e12eb221652acb4ce1561e630f90c1da72db8268/plugins/dbgate-plugin-oracle/package.json). Self-host Docker/web hoặc desktop. Team Premium hiện **15 USD/user/tháng**, tối thiểu 2 users, trial 30 ngày; 20 users phép tính niêm yết **300 USD/tháng**, chưa thuế/add-on/quote. Có API/automation nhưng chưa kiểm DB release contract; Git lưu scripts vẫn cần CI orchestration. [Team pricing/deployment](https://www.dbgate.io/editions/team-premium/).

**Giá trị/công/failure:** tập trung connection và hỗ trợ schema diff khi người dùng cần client ngoài DBeaver; premium role/audit hữu ích nếu ngân sách cho shared workbench. Cần env configuration hoặc storage DB/admin, identity/secrets, driver và external engine/workflow cho release. Không dùng schema compare/sync như lời hứa backup hay rollback Oracle DDL. SOURCE chỉ driver/package/license đã đọc; runtime **NOT_RUN**.

**Pin/ngày:** kiểm 07/10/2026; public release [v7.3.1](https://github.com/dbgate/dbgate/releases/tag/v7.3.1), 24/09/2026; source HEAD `e12eb221652acb4ce1561e630f90c1da72db8268` (06/10/2026), **khác release tag**. Feature current docs/source không phải runtime của v7.3.1.

<a id="tool-dbhub"></a>

### DBHub

**Vai trò:** MIT MCP/SQL gateway và workbench nhẹ để tra cứu nhiều DB hoặc gắn vào automation. Component, chưa là database release/governance platform độc lập.

**Bốn tính năng có nguồn:**

1. **DOC:** TOML khai báo nhiều named sources, per-source SSL/timeout/lazy connection và per-tool readonly/max_rows. [TOML configuration](https://dbhub.ai/config/toml).
2. **DOC:** `execute_sql`, `search_objects`, optional explain/health và custom parameterized SQL tools. [README pin](https://github.com/bytebase/dbhub/blob/4ddb26e73c5d8f1d54f5d04351c11c3caeb43cbb/README.md).
3. **DOC:** HTTP transport có **web Workbench**, chạy custom tools/query và xem request traces; demo mode được cung cấp. Nhận định cũ “không UI” không áp dụng cho DOC hiện tại này; chưa chứng minh team release UI. [Workbench](https://dbhub.ai/workbench/overview).
4. **SOURCE:** Oracle connector dùng node-oracledb Thin pool, SID/service DSN, metadata, PL/SQL splitter, readonly check và execution plan. [Oracle implementation](https://github.com/bytebase/dbhub/blob/4ddb26e73c5d8f1d54f5d04351c11c3caeb43cbb/src/connectors/oracle/index.ts).

**Oracle/nhiều DB/user/release:** source support thật, nhưng chưa chạy splitter/query/auth/TCPS, không xác minh supported Oracle version. Multiple sources và IDs giúp chọn target; không thấy bằng chứng org RBAC, approval, immutable release/checksum ledger hoặc 20-user identity model trong phần đã rà. Readonly parser là một guardrail, không bằng chứng mọi quyền của DB account được sandbox.

**Git/CI/API/license:** MCP STDIO/HTTP, TOML có thể version trong Git, chạy Node/Docker self-host; source MIT tại [LICENSE](https://github.com/bytebase/dbhub/blob/4ddb26e73c5d8f1d54f5d04351c11c3caeb43cbb/LICENSE). Không thấy paid feature/user/DB cap trong README đã đọc; deps/driver terms riêng. Không suy edition limit của Bytebase sang DBHub dù cùng tổ chức. CI phải tự gọi workflow và engine; MCP không là DB release REST contract.

**Giá trị/công/failure:** hữu ích cho inventory lookup và postcheck theo named Oracle target hoặc cho công cụ hỗ trợ DBA. So với DBeaver thêm headless integration; so với Flyway CLI thêm query/metadata interface, không thay engine. Cần identity/network boundary, secrets, source IDs, authorized custom queries, external approval/audit correlation và timeout. Traces/query results không tự xử lý partial DDL/replay; không dùng retry query để suy recovery. Chưa chạy public demo hoặc DBHub app.

**Pin/ngày:** API/GitHub kiểm 07/10/2026: [v1.4.0](https://github.com/bytebase/dbhub/releases/tag/v1.4.0), 28/09/2026; HEAD `4ddb26e73c5d8f1d54f5d04351c11c3caeb43cbb`, 02/10/2026. Reread connector/README/license tại đúng pin; runtime **NOT_RUN**.

## Phân biệt sản phẩm có sẵn với phương án ghép

| Hướng | Tool thực sự cung cấp | Cấu hình thông thường | Phần ghép/tự phát triển phải tính riêng |
| --- | --- | --- | --- |
| Native database workflow | Bytebase, ODC, CloudDM, AccessFlow, Archery, NineData; DBmaestro/Harness theo gói | Datasource, project/env, users/roles, policy, approval, Git/API credentials, backup/retention | Gaps Oracle/replay/recovery theo hồ sơ; không tự gán native adapter/ledger chưa tồn tại |
| Database administration/source control | OEM Change Plans; Gitora object/Git workflow | Object/schema/target groups, named credentials, role grants, Git remote, baseline | Git/CI release identity, approval/rollout toàn estate, target result correlation nếu sản phẩm không có |
| Engine + orchestrator | Flyway/Sqitch/Liquibase/SQLcl/dbpm/Atlas + AWX/Rundeck/Jenkins/Octopus | Engine project + inventory, job/template, artifact storage, secrets, approval, worker | Manifest/model DB instance-service-schema, allowlisted target selection, review/approval binding, batch policy, structured per-target result, reconciliation/runbook |
| Shared workbench + release stack | CloudBeaver/DbGate; DBHub làm integration/query component | Connection catalog, identity, access policy, driver | Dịch vụ/workflow release riêng; query history/traces không thay release audit hoặc engine history |

Đối với các tổ hợp, **không chỉ đưa Flyway CLI vào một container khác**. Một cải tiến có ích so với baseline phải cho người dùng chọn target từ inventory, biết artifact/commit nào đã duyệt, quan sát kết quả theo DB và phân biệt thành công/thất bại/chưa chạy/không rõ kết quả. Target history của engine hỗ trợ thao tác này; control plane cần tổng hợp nó và kết nối actor/approval/log. Đây là yêu cầu tích hợp đề xuất cho tình huống, không là tính năng native đã xác minh của bất kỳ tổ hợp nào.

Không ghép hai executor cùng chạy một change. Nếu khảo sát CloudDM/ODC làm workflow trước engine ngoài, phải xác định hook được hỗ trợ, vô hiệu hóa đường execution trùng, bind cùng artifact hash và target, ghi result về workflow; chưa triển khai tổ hợp này. Lợi ích UI/approval vẫn giữ được, nhưng effort và failure boundary thay đổi. [Phân tích hiện có về adapter](report.md), [CloudDM v4.3.0 review](research-round-2/coordinator/clouddm-v430-artifact-review-20261007.md).

## Nhóm đáng xem tiếp và lý do

Shortlist này là **shortlist khảo sát theo tính năng**, khác shortlist đạt migration acceptance. Chưa có bằng chứng workload 50 instance/20 user đạt yêu cầu trên bất kỳ ứng viên nào; các nhóm dưới đây không thay quyết định POC lịch sử.

1. **Workflow self-host ưu tiên OSS: ODC và CloudDM; Archery nếu nhu cầu chính là SQL ticket.** ODC có project, approval và batch 2–100 target tasks với serial/parallel/manual control được dẫn tới docs/code. CloudDM có datasource/environment/approval/change flows và webhook/API; public v4.3.0 app license đã rà. Archery có Oracle review/execution và check object INVALID trong code, nhưng commit từng câu. Khảo sát UX inventory, quyền và workflow của các sản phẩm có sẵn; ODC vẫn mang các FAIL cũ, CloudDM vẫn NO-GO sole native migration executor. Không chạy lại acceptance trên build không đổi để tạo kỳ vọng đã sửa. [ODC](#tool-odc), [CloudDM](#tool-clouddm), [Archery](#tool-archery).
2. **OSS orchestration nếu cần tự chủ hoặc đã có nền CI: AWX hoặc Rundeck + Flyway; Jenkins khi đã vận hành Jenkins.** AWX có inventory/limit/RBAC/workflow approval node; Rundeck có node filters/job options/API/SCM; Flyway có history/checksum/validate từng DB và mẫu fleet rollout chính thức. Điều này giải thích công dụng vượt CLI thủ công. Tuy nhiên đây là composition; phải thiết kế DB/schema target model, immutable artifact approval, postchecks và central per-target records. AWX đang tạm dừng releases để refactor, platform maintenance và Rundeck paid approval features là yếu tố quyết định. Chưa chọn CI provider hoặc kiến trúc thay user. [AWX](#tool-awx), [Rundeck](#tool-rundeck), [Jenkins](#tool-jenkins), [Flyway](#tool-flyway).
3. **Toolchain Oracle/schema-as-code: SQLcl Project, Sqitch, Liquibase 4.33; Gitora khi có nhiều PL/SQL developer.** SQLcl có export/stage/release/artifact/deploy; Sqitch có dependency + verify/revert intent và Oracle registry; Liquibase 4.33 giữ Apache-2.0 cùng changesets/checksum/lock. Gitora bổ sung object branching, collaboration và valid-object-before-commit, là commercial comparator khác migration CLI. Chọn nhóm này theo tỷ trọng PL/SQL/object authoring/dependencies của estate; chúng cần control plane cho 50 DB. Atlas Pro đáng so sánh declarative/lint/drift nếu chấp nhận Oracle paywall. [SQLcl](#tool-sqlcl), [Sqitch](#tool-sqitch), [Liquibase](#tool-liquibase4), [Gitora](#tool-gitora), [Atlas](#tool-atlas).
4. **Platform thương mại để đo phần có thể mua thay vì tích hợp: Bytebase Enterprise, Harness Database DevOps, DBmaestro và NineData Enterprise.** Bytebase có native release/rollout API/GitOps nhưng FREE không đủ số instance và approval/audit có edition gate. Harness có DB instance/schema concepts trong pipeline và changelog status; DBmaestro mô tả object source control/drift/impact/release automation cho Oracle. NineData có task approval, environment-node restrictions và API; Community 10 datasource không đủ fleet. So sánh một release thực tế có lỗi giữa chừng, inventory import, phân quyền 20 người, logs/export và quote đúng số instance/PDB/schema; vendor demos hiện là DOC. [Bytebase](#tool-bytebase), [Harness](#tool-harness), [DBmaestro](#tool-dbmaestro), [NineData](#tool-ninedata).
5. **SQL quality/access governance riêng: SQLE+DMS và AccessFlow.** SQLE có plugin review, DMS inventory/workbench; cần giữ CE/EE và Oracle plugin terms rõ. AccessFlow có authored-once change set, central checksum/review và environment promotion, nhưng statement gate hạn chế DML và không chứng minh PL/SQL migration. Đây là các tính năng hữu ích khi mục tiêu là quản trị truy cập/review; không phải engine winners. [SQLE+DMS](#tool-sqle), [AccessFlow](#tool-accessflow).
6. **Shared access hoặc nền OEM đã có: CloudBeaver/DbGate và OEM.** Workbench giúp gom connection/quyền/query; chỉ nên ưu tiên nếu đó là một vấn đề riêng cần giải. DBHub hữu ích làm component tra cứu/postcheck có named targets, không thay platform release. OEM đáng xem khi doanh nghiệp đã có OMS/agents/DBA và pack: Change Plans sinh script/impact cho destination thật, tiết kiệm xây lại inventory; nếu chưa có thì operating footprint/license pack có thể lớn. [CloudBeaver](#tool-cloudbeaver), [DbGate](#tool-dbgate), [DBHub](#tool-dbhub), [OEM](#tool-oem).

## Nguồn tìm kiếm, kiểm tra và giới hạn

**Dedup đầu vào:** đọc [root index](../README.md), [evaluation index](README.md), [report](report.md), [shortlist](shortlist.md), [round-two index](research-round-2/README.md), [discovery/source review](research-round-2/discovery/source-review.md), [license/release review](research-round-2/licensing/licensing-review.md) và các hồ sơ liên quan. Không tạo lại exact-artifact investigation CloudDM hoặc tiêu chí POC. Các ứng viên cũ ngoài 24 họ này vẫn còn tại [candidate register](candidates.csv), [discovery log](research-round-2/discovery/search-log.md), [additional candidates](../additional-candidates.md); catalog không xóa chúng.

**Các kênh đã dùng:** official product docs, GitHub repository/release/API/raw files, Oracle manuals/downloads, commercial pricing/edition matrices, public screenshots/demo/webinar descriptions. Public demo được dùng để tìm workflow/lead, không đăng nhập, chạy app, gửi SQL hoặc coi là RUNTIME. Không liên hệ hãng, dùng private accounts, Antigravity hay mua dịch vụ.

| Nhánh tìm kiếm / truy vấn tiêu biểu | Nguồn trực tiếp đã đối chiếu | Điều mới hoặc giới hạn được làm rõ |
| --- | --- | --- |
| `Oracle database change management approval GitOps self-hosted`; `Bytebase pricing Oracle API`; `CloudDM v4.3.0`; `OceanBase ODC multiple database change` | Bytebase docs/pricing/release/license, ODC docs/source, CloudDM exact-artifact record hiện có | Platform/workflow vẫn hữu ích khi migration engine không đạt; edition gates và source/image pin khác nhau |
| `SQLE DMS Oracle Community Enterprise license`; `AccessFlow schema change`; `Archery Oracle release` | ActionTech docs/raw LICENSE/releases, AccessFlow/Archery pinned source reviews | MPL core/plugin terms, CE/EE feature gates; Oracle driver giữa HEAD/release khác nhau |
| `Flyway Oracle fleet rollout license`; `Liquibase Community 5.0.4 FSL Secure`; `Atlas Oracle features` | Redgate Oracle/history/validate/fleet docs, Liquibase releases/FSL, Atlas feature/release matrices | Multi-target orchestration ngoài engine; FSL khác OSS; Atlas Oracle Pro-only |
| `Oracle SQLcl project release artifact`; `Sqitch Oracle registry`; `dbpm Core license` | Oracle 26.1 Project guide + SQLcl 26.3 download/release pages, Sqitch manuals/releases, dbpm/Core upstream pins và LICENSE | Object authoring/package/dependency có giá trị; Core public source Apache-2.0 đã làm rõ; không central approval portal |
| `Rundeck SCM approval API`; `AWX workflow approval inventory`; `Jenkins input LTS`; `Octopus target lifecycle approvals pricing` | Official docs/releases/license, Jenkins stable changelog, Octopus binary downloads | Node/machine/host khác DB/schema; native orchestration vs Oracle engine adapter |
| `Harness Database DevOps Oracle instance Git SHA`; `DBmaestro Oracle source control release automation` | Official product docs, dated release/blog, FAQ/pricing/demo | Commercial DB-aware workflows; self-host delegate khác control plane; proprietary build/source limits |
| `Gitora Oracle multi database API`; `OEM 24.1 schema Change Plans licensing` | Gitora feature/API/buy/download, Oracle 24.1 manuals and pack licensing | Object source control/impact plan khác script migration; free download khác free pack |
| `NineData Oracle SQL tasks GitOps Community`; `CloudBeaver audit Oracle`; `DbGate team permissions`; `DBHub workbench Oracle` | Official docs + four GitHub HEAD/release API/raw source checks | NineData 10-datasource cap, review output not default gate; paid audit/admin; DBHub web UI claim cập nhật |

**Provenance:** ngày kiểm chung 07/10/2026; mỗi hồ sơ có release/source pin và phạm vi đọc riêng. GitHub API/HEAD metadata không tự là SOURCE implementation; chỉ những file/path thực sự đọc mới được gắn SOURCE. Đọc lại CloudBeaver driver/README/LICENSE, DbGate Oracle driver/package/LICENSE, DBHub connector/README/LICENSE tại exact SHAs; NineData tree chỉ là documentation/distribution repository. Đọc bổ sung Bytebase 3.23.0 plan/license/API proto, Liquibase 4.33 Java facade và public LICENSE/README của dbpm Core; license SOURCE không là kiểm implementation/recovery Core. Nguồn implementation kế thừa dẫn tới review cũ/pinned blob; không chuyển finding của HEAD sang release binary. Release docs hiện hành của commercial SaaS không là pin binary. DBmaestro current build, Harness module build/self-managed entitlement và Oracle certification sau MOS vẫn chưa xác minh được từ public artifacts.

**Khoảng chưa xác minh công khai hoặc thực tế:** source→binary/image mapping và toàn bộ dependency/driver licenses ngoài artifact review đã có; entitlement của từng edition/module; exact Oracle object/SQL*Plus/PLSQL/version support, enforcement của approval/SQL review, concurrency và timeout, secret rotation, retention/audit export, crash/uncertain-commit recovery. Không có measured scale hoặc benchmark mới. HTTP link/release metadata check chỉ xác nhận nguồn truy cập được, không xác nhận tính năng chạy đúng.

**Dữ liệu nội bộ còn thiếu:** Oracle major/RU/edition, topology (instance/PDB/schema), target ownership/env/criticality và intentional variants, Git/CI/SSO hiện có, release frequency/approval policy, DBA privilege/backup/recovery baseline, ngân sách và người vận hành. Các phần độc lập đã nghiên cứu; những dữ liệu này dùng để chọn nhánh khảo sát, không là lý do hoãn catalog hoặc yêu cầu người dùng tự tìm thông tin công khai.

Oracle DDL có implicit COMMIT; không suy rollback/repair/retry của tool thành tự động khôi phục mọi partial release. [Oracle DDL semantics](https://docs.oracle.com/en/database/oracle/oracle-database/19/tdddg/data-definition-language-ddl-statements.html). History/checksum khác live schema drift; central job SUCCESS khác object hợp lệ hoặc 50 target cùng version. Kết quả POC lịch sử vẫn có giá trị để chọn ca cần kiểm sau khi có build/config delta và authorization, không bị thay bằng lời quảng bá.

**Kiểm tra tài liệu 07/10/2026:** [checker hiện có](../tools/verify_research_documents.py) PASS cho links/bảng, 38 source snapshots, 183 source references, 11 screenshots và 45 criteria/POC IDs. Kiểm riêng catalog: 25 hồ sơ, mỗi hồ sơ 3–5 tính năng có nguồn trực tiếp, anchors hợp lệ; 220 URL nguồn trả HTTP 200 trong lượt kiểm. So hash 104 file baseline của lượt này xác nhận chỉ ba index thay đổi, bằng chứng/expected/POC lịch sử giữ nguyên. Các kiểm tra này xác minh tài liệu và khả năng truy cập nguồn, không là RUNTIME của tool hoặc Oracle.
