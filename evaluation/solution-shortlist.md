# Từ catalog tới mô hình quản lý thay đổi Oracle có thể triển khai

Ngày nghiên cứu: **07/10/2026**. Phạm vi: khoảng **50 Oracle instance, 20 người**; nghiên cứu tài liệu/source và thiết kế demo. **Không có runtime, SQL, deployment, đăng ký dịch vụ hoặc thay đổi infrastructure mới.**

**Đề xuất bước tiếp theo:** dựng POC có điều kiện cho **ODC làm workflow + Flyway Community làm executor duy nhất**, đối chiếu với **Git + Jenkins + Flyway Community** có inventory và audit tập trung. **CloudDM workflow + Flyway** là POC thứ ba tùy chọn nếu contract thay executor rõ hơn ODC. Bytebase Enterprise giữ vai trò benchmark và phương án mua nếu báo giá phù hợp; chưa có căn cứ loại nó vì chi phí chưa biết, cũng chưa có native OSS winner đạt mọi hard requirement.

Đây là vòng chuyển kết quả nghiên cứu sang **operating model**, theo yêu cầu mới cho phép đánh giá cả A/B/C. Khác [quyết định khảo sát trước](report.md), composition nay được đề xuất để so sánh POC, **chưa được chọn triển khai** và không trở thành native platform acceptance. [Catalog](tool-feature-catalog.md), các FAIL, expected, source snapshots và runtime cũ giữ nguyên. Kiến trúc và công việc lab nằm ở [reference architecture](reference-architecture.md) và [POC plan](poc-plan.md).

## 1. Problem statement và hiện trạng

DBeaver giải quyết thao tác database của từng người. Repository + Flyway CLI giải quyết một phần version/checksum/history tại target. Team vẫn thiếu nơi nối **yêu cầu → SQL đã review → người duyệt → target/schema → thực thi → kết quả → release** trên toàn estate. Việc chọn connection, giữ credentials, chép log, đối chiếu trạng thái 50 instance và xử lý release lỗi hiện phụ thuộc người vận hành.

Mục tiêu là quản lý workflow và trách nhiệm tập trung, giữ source có thể review trong Git và dùng engine phù hợp Oracle. **Đổi Flyway sang engine khác không tự giải quyết thiếu control plane.** Một release chỉ áp dụng vào tập target của application/migration stream tương ứng, không mặc định fan-out tới cả 50 instance.

Chưa biết Oracle major/RU/edition, số service/PDB/schema, Git/CI/SSO hiện hữu, release cadence, ngân sách và maintenance capacity. `instance`, datasource/connection, PDB/service và schema là đơn vị khác nhau; 50 instance có thể tạo nhiều hơn 50 target deployment/license units. Không suy Oracle nội bộ là 26ai từ lab lịch sử.

```text
Developer/DBA → Change request → SQL + manifest trong Git → Validation
→ Review → Approval cho artifact + target set → DEV → SIT → UAT
→ Approval PROD → Controlled rollout → Verification → Audit/history/evidence
```

## 2. Đầu vào kế thừa và evidence standard

Đã đọc [root index](../README.md), [evaluation index](README.md), [round-two index](research-round-2/README.md), [catalog](tool-feature-catalog.md), [report](report.md), [shortlist cũ](shortlist.md), [kết luận gốc](../REPORT.md), các hồ sơ source/license, [45 expected](../poc/ORACLE-POC.md), [ODC results](../ODC-ORACLE-POC-RESULTS.md), [Bytebase results](../BYTEBASE-ORACLE-POC-RESULTS.md) và [so sánh runtime](../BYTEBASE-ODC-COMPARISON.md). Index benchmark ghi NOT_RUN; không có số hiệu năng để kế thừa.

| Nhãn | Điều thực sự được xác nhận |
| --- | --- |
| DOC | Tài liệu chính thức mô tả khả năng; chưa chứng minh chạy đúng trong estate |
| SOURCE | Implementation/license/file đã đọc tại commit chỉ rõ; không thay kiểm binary/runtime |
| RUNTIME lịch sử | Đúng build, edition, Oracle, cấu hình và ca đã chạy trong record cũ |
| DESIGN | Contract/kiến trúc đề xuất trong vòng này; không phải capability đã có |
| UNKNOWN / NOT_RUN | Chưa đủ evidence hoặc chưa chạy; không dùng như PASS |

| Đối chứng | Pin và kết quả kế thừa | Giới hạn ảnh hưởng quyết định |
| --- | --- | --- |
| ODC | `4.4.1-20260116`, Oracle 26ai `23.26.4.1.0`: **12 PASS / 20 PARTIAL / 5 FAIL / 8 NOT_RUN** | INVALID, replay, checksum, dedup và requester-execute FAIL; runner ngoài giữ promotion; log cũ có lỗi đọc sau restart. Bốn schema trên một instance, chưa đo 50/20 |
| Bytebase | `3.22.1/FREE`, commit `a85f6cb4195299995e8554303550d672d5093e1d`, cùng Oracle: **17 PASS / 14 PARTIAL / 4 FAIL / 3 BLOCKED / 7 NOT_RUN** | INVALID và early mockPROD FAIL; checksum detection chưa strict reject; approval/audit edition gates. P04 SQL Review enforcement FAIL ngoài 45 ca |
| CloudDM | v4.3.0 source `3aa1238a471afca2579e76e6fbf0a922d9be5579`; [artifact review](research-round-2/coordinator/clouddm-v430-artifact-review-20261007.md) | Native Oracle executor **NO-GO hiện tại**: default ticket compile off; target ledger/lock/reconciliation chưa establish. Không có RUNTIME |
| Engine và compositions | DOC/SOURCE tại [catalog](tool-feature-catalog.md), [engine evidence](../EVIDENCE.md) | Việc user từng dùng Flyway CLI không phải acceptance runtime cho stack mới |

Không rerun lỗi ODC/CloudDM trên build không đổi để kỳ vọng kết quả khác. Adapter với sole executor, binding, postcheck và policy là **delta kiến trúc cần chứng minh riêng**, không sửa status native lịch sử. Source ODC `d517c0f27971642fb0cd7565fd61ab2309875ec3` chưa map với image runtime 4.4.1.

## 3. Tiêu chí và shortlist bảy phương án

Áp dụng toàn bộ A–K: inventory, secrets, source, SQL review, approval, selection, rollout, failure/recovery, verification, audit và CI/CD. Hard gates trước adoption: Oracle/object compatibility đúng version; không plaintext password Oracle trong Git; approval binding và actor separation; sole executor; target serialization; stop khi partial/uncertain/invalid; evidence bền vững. Tổng điểm không bù được hard gate FAIL.

| ID | Solution được đánh giá | Loại | Tại sao giữ / vì sao chưa dùng ngay |
| --- | --- | --- | --- |
| S1 | Bytebase Enterprise self-host | A: integrated platform, configure/integrate | Gần desired UX nhất; commercial benchmark. 50-instance entitlement và quote cần phù hợp; edition mới chưa có runtime regression |
| S2 | ODC workflow + Flyway Community + adapter/CI | B: platform workflow + engine, compose | Inventory/approval/UI có RUNTIME lịch sử; engine ngoài có target history. Supported handoff, tắt native executor và result writeback **UNKNOWN** |
| S3 | CloudDM workflow + Flyway Community + adapter/CI | B: platform workflow + engine, compose | Inventory, approval và GitLab intake SOURCE; v4.3.0 app Apache-2.0. HttpCall không tự chứng minh supported sole-executor contract |
| S4 | AWX + Flyway Community + Git | B: automation control plane + engine, compose | UI inventory/RBAC/approval nodes/API DOC. Host inventory cần DB/schema mapping; quyền execute workflow có thể cũng approve; releases đang pause |
| S5 | Rundeck Community + Flyway Community + Git/Jenkins approvals | B: runbook composition | Node filters/job UI/ACL/API DOC. Không có evidence CE approval binding native; SQL review/approval/release records cần tích hợp |
| S6 | Git + Jenkins + Flyway Community + inventory/result publisher | C: CI-driven composition | Ít phụ thuộc executor hook của platform; Jenkins input approval và Flyway history DOC. Inventory/release summary/policy/reconciliation phải viết |
| S7 | Archery native SQL-ticket workflow | A về ticket governance, không full release platform | Oracle ticket/permissions/INVALID check SOURCE; thiếu versioned release/promotion/target ledger. Reserve, **không mở POC mặc định** |

Shortlist là solution candidates, không thêm catalog rộng. S2–S6 dùng chung một engine để so sánh control/workflow. [Liquibase 4.33, Sqitch, SQLcl](#11-engine-oracle-và-cicd) là engine alternatives, không thêm ba portal giả. AccessFlow vẫn PAUSE cho DDL-only governance theo [shortlist cũ](shortlist.md); SQLE Oracle plugin license/bundle, NineData Community 10 datasource và Atlas Oracle Pro gate khiến chúng kém phù hợp cho nhánh OSS hiện tại. Harness/DBmaestro giữ tại catalog để benchmark thương mại khi có nhu cầu, không mở thêm POC trong vòng này.

## 4. Phân tích từng phương án

### S1 — Bytebase Enterprise

Inventory/project/environment, SQL editor, SQL review, plan/issue/release/rollout và audit thuộc cùng sản phẩm; SQL/Git và API có [hướng dẫn Oracle](https://www.bytebase.com/databases/oracle/schema-migration/), [Database-as-Code](https://www.bytebase.com/database-as-code/) và [example GitOps chính thức](https://github.com/bytebase/example-gitops-github-flow) (**DOC**). Jenkins/GitLab sẽ gọi API/CLI bằng service identity, đọc cùng commit/artifact; ví dụ GitHub không phải runtime Jenkins/GitLab.

Phân quyền/requester/approver/executor và SQL console cần cấu hình đồng thời: runtime FREE đã chặn rollout requester sau thu hẹp role nhưng console write từng là đường khác. Review SQL ERROR từng không chặn execution; stage order từng bị vượt. Enterprise entitlement không chứng minh các lỗi này đã sửa. Release history/revision trung tâm không tự là target-side Flyway ledger hay bằng chứng rollback Oracle DDL. Cần regression trên exact build/edition sẽ dùng.

Ít code quản trị phải tự viết nhất trong shortlist; vẫn cần onboarding, secret/SSO, policy, postcheck và audit export. Best integrated **về documented product fit**, chưa production winner. [Source plan 3.23.0](https://github.com/bytebase/bytebase/blob/c8188c635465321ff930c97200742a96ef653144/backend/enterprise/plan.yaml), [runtime report](../BYTEBASE-ORACLE-POC-RESULTS.md).

### S2 — ODC workflow + sole Flyway executor

ODC cho users login, project/connection inventory, SQL preview/ticket, comments/approval và history; một phần đã có RUNTIME lịch sử. Batch docs mô tả **2–100 database tasks cùng project**, serial/parallel và manual continuation; batch đang chạy không luôn abort được. Đây là giới hạn task, không license cap. Native batch correctness chưa RUNTIME verified. [Official batch guide](https://github.com/oceanbase/odc-doc/blob/40dc7c03522fef1968bd11b2b051bc216091e60d/en-US/700.database-change-management/650.multiple-database-change.md) (**DOC**, SOURCE kế thừa tại catalog).

**DESIGN:** Git chứa migration và manifest; CI tạo immutable artifact và ticket tham chiếu commit/hash. Adapter chỉ sau approval lấy lại SQL/targets, đối chiếu hash, chạy Flyway một lần per target, postcheck và publish result. ODC không nhận production migration credentials; UI dùng account metadata/read-only giới hạn. Native change execution và console write phải không thể chạy change đó. Nếu supported hook hoặc policy không cho thực hiện điều này, dừng S2; không dùng click Execute native rồi chạy Flyway lần nữa.

Chưa chứng minh ODC có API/hook để thay executor và cập nhật trạng thái external execution. [SQL approval integration](https://github.com/oceanbase/odc-doc/blob/40dc7c03522fef1968bd11b2b051bc216091e60d/en-US/1000.system-integration/300.sql-audit-integration.md) mô tả ODC gọi approval bên ngoài; không chứng minh chiều ngược lại hoặc external engine hook. Link tới CI result thay vì writeback là integration UX thấp hơn, phải ghi rõ. Các gap cần giữ nguyên tại [source survey](research-round-2/coordinator/odc-source-survey-20261006.md).

S2 gần Bytebase nhất trong nhánh OSS **nhờ workflow đã quan sát**, nhưng có integration/custom code đáng kể. POC đầu tiên là contract feasibility; chưa triển khai patch server chỉ để tạo một bản demo đẹp.

### S3 — CloudDM workflow + sole Flyway executor

v4.3.0 có datasource/environment, SQL audit, approval attachment và Git/HTTP actions SOURCE. [GitLab guide tại release pin](https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/docs/guides/gitlab-cicd.en.md) mô tả lấy archive theo exact commit, branch/project/script-directory/target binding, webhook signing và receipt dedup (**DOC**); GitLab 19.2.x là acceptance baseline của guide, không giả định version GitLab nội bộ.

Guide cũng nói GitLab access token, webhook secret và signing token **plaintext trong MetaDB**. Đây không phải password Oracle trong Git, nhưng phải tính vào credential burden; không quảng bá CloudDM có native Vault/encrypted-token storage chưa kiểm. **DESIGN:** runner giữ Oracle deploy secrets ngoài CloudDM; hạn chế MetaDB và dùng token read-only scoped, hoặc intake artifact do CI thực hiện bằng adapter nếu supported. Tắt native executor/write console cho stream được quản lý. HttpCall nhận/gửi HTTP không tự là transaction contract, approval binding hoặc async callback.

POC chỉ mở khi xác định được action sau approval, data truyền sang executor, auth, duplicate suppression và result receipt. Source/binary review đã đóng public license/counter-path gate; không lặp lại survey 10/5 cũ. **Native v4.3.0 NO-GO vẫn giữ**; không sửa compile flag rồi tuyên bố toàn migration/recovery đã xong. [Artifact review](research-round-2/coordinator/clouddm-v430-artifact-review-20261007.md), [current official site](https://www.cdmgr.com/en/pricing/).

### S4 — AWX + Flyway

AWX có inventories/groups, Git projects, credentials, templates, workflow graph, approval nodes và API (**DOC**). Group `core/dev` có thể map tới Oracle service/schema nhưng đó là **integration**, không native database inventory/current version. Playbook gọi cùng runner contract, `serial`/limit/batch policy và per-target result publisher. [Workflows](https://docs.ansible.com/projects/awx/en/24.6.1/userguide/workflows.html), [workflow templates](https://docs.ansible.com/projects/awx/en/24.6.1/userguide/workflow_templates.html).

Approval node cho phép người có Execute workflow, org admin hoặc Approve permission duyệt (**DOC**); không tự đảm bảo requester ≠ approver. User requester không được quyền launch executable PROD workflow; CI identity launch và approver riêng, adapter kiểm actor/requester. Extra vars/limit/project branch phải cố định để tránh đổi target/artifact sau duyệt. [RBAC](https://docs.ansible.com/projects/awx/en/24.6.1/userguide/rbac.html).

Chọn nếu đã có Ansible/AWX vận hành. [Upstream README](https://github.com/ansible/awx) hiện ghi releases pause khi refactor; latest released line 24.6.1 ngày 02/07/2024 theo catalog. K8s/operator/execution environment/upgrades tăng ownership; không thêm AWX chỉ để có một nút Approve.

### S5 — Rundeck Community + Flyway

Project/node resource model, filters, job options, job/activity UI, ACL, API và SCM job definitions là **DOC**. [Jobs](https://docs.rundeck.com/docs/manual/jobs/), [ACL](https://docs.rundeck.com/docs/administration/security/authorization.html), [SCM](https://docs.rundeck.com/docs/manual/projects/scm/git.html), [API](https://docs.rundeck.com/docs/api/). Node có thể biểu diễn target ID; schema/version registry vẫn cần adapter. SCM job definitions không phải SQL release artifact.

CE job run permission không thay multi-person approval. Dùng Git/Jenkins approval record ngoài, để một service identity launch job với frozen release ID. Người dùng chọn subset trước duyệt; job không nhận arbitrary DSN/password. Result publisher nối execution ID tới release/target/commit. Native CE approval binding chưa đủ evidence, enterprise capabilities không được tính vào CE.

Ưu điểm là portal vận hành/runbook dễ dùng cho DBA; đổi lại thêm controller bên cạnh CI và cần giữ hai lớp ACL/audit. Current release API kiểm lại cho tag **v6.2.1**, commit `e649f088e039b0fabbbb7039f730cbbcc183f82d`, ngày 09/09/2026; `6.2.1-20260909` là version string trong catalog, không phải Git tag tồn tại. [Release](https://github.com/rundeck/rundeck/releases/tag/v6.2.1), [Apache license tại commit](https://github.com/rundeck/rundeck/blob/e649f088e039b0fabbbb7039f730cbbcc183f82d/LICENSE).

### S6 — Git + Jenkins + Flyway

Git MR/PR giữ SQL/diff/comments; Jenkins build/input screens là workflow UI; Flyway chạy trên restricted agent; inventory manifest và result summary là custom integration. Đây là **CI-driven composition**, không gọi là native DB platform. [Jenkins Pipeline](https://www.jenkins.io/doc/book/pipeline/), [input step](https://www.jenkins.io/doc/pipeline/steps/pipeline-input-step/) (**DOC**).

Giữ Jenkinsfile/shared library trong repo quản trị riêng với quyền sửa hạn chế. Developer chỉ thay SQL/manifest và yêu cầu build; không được sửa trusted deployment logic hoặc dùng Replay/Configure/agent shell để lấy secrets. Hai input gate ghi Reviewer rồi DBA/Approver với `submitterParameter`; policy code kiểm người trả lời khác requester. Jenkins admin vẫn có thể trả lời input bất kể submitter: phải ghi admin exception/break-glass, không gọi là SoD tuyệt đối.

Nếu đã có GitLab Premium/Ultimate, có thể thay Jenkins bằng GitLab deployment approvals/protected environments/resource groups với cùng contract. GitLab Free có optional MR approvals nhưng **required approval enforcement** và **deployment approvals** có paid boundaries; manual job không tự là approval record. Đường không mua gói này dùng Jenkins gates và hạn chế merger thay cho mặc định GitLab Free đã đủ. [MR approvals](https://docs.gitlab.com/user/project/merge_requests/approvals/), [deployment approvals](https://docs.gitlab.com/ci/environments/deployment_approvals/) (**DOC**).

S6 là phương án đối chứng khả thi nhất khi UI engine hook của S2/S3 không đủ. Flyway vẫn giữ; operational burden chuyển từ từng DBA chạy CLI sang DevOps sở hữu inventory/policy/result/recovery code. Chưa xác nhận đội đã có Jenkins; dựng mới làm maintenance tăng.

### S7 — Archery

Ticket SQL, approval/resource groups và Oracle execution path SOURCE, gồm commit từng statement và INVALID check cho object xác định. Không suy đủ package/body/dependency coverage. [Source report](candidates/archery/source-review.md), [Oracle executor tại pin review](https://github.com/hhyo/Archery/blob/ccc7134f48d0e261f9e3ffa0d445dcec48adb790/sql/engines/oracle.py#L1125-L1205).

Developer submit ticket, reviewer đọc SQL, DBA approve/execute, DevOps giữ Django/worker/metadata/Oracle client. So với manual SQL có accountability, nhưng Git hash linkage, immutable release, multi-environment promotion và ledger/reconcile còn thiếu. Release v1.14.0 có cx_Oracle/Instant Client khác HEAD python-oracledb; SOURCE của HEAD không chứng minh binary release. Giữ reserve cho SQL-ticket use case; không biến nó thành POC migration mới khi chưa có owner.

## 5. Bytebase benchmark theo workflow

`N` = Native; `I` = Integrated qua công cụ khác; `C` = Custom development required; `—` = Not available/chưa establish trong edition/path đã xét. **N/I/C là cách cung cấp, không evidence level.** `D`, `S`, `R` tương ứng DOC, SOURCE, RUNTIME lịch sử. Các stack S2–S6 **chưa có RUNTIME end-to-end**; chữ I/C mô tả thiết kế đề xuất, không support đã chứng minh.

| Capability | Bytebase EE (benchmark) | ODC + Flyway | CloudDM + Flyway | AWX + Flyway |
| --- | --- | --- | --- | --- |
| DB inventory | N-D; FREE từng R | N-R phần project/datasource | N-S | I-D host mapping; C schema/version |
| SQL editor/change UI | N-D; FREE từng R | N-R | N-S | I Git; — SQL editor native |
| Git integration | N-D | I-D; C exact hash handoff | N-D exact commit intake; C adapter | N-D Git project; I SQL review |
| Review | N-D; old FREE enforcement FAIL | N-R preview; I Git; C fail-closed gate | N-S audit; I Git; C binding | I Git; C Oracle checks |
| Approval | N-D EE | N-R flow; C external binding | N-S; C external binding | N-D node; C actor check |
| RBAC | N-D; FREE partial R | N-R; requester execute FAIL | N-S; external path NOT_RUN | N-D; launch/approve overlap |
| Oracle | N-D; old FREE R | N-R native cũ; I-D Flyway mới | N-S connector; I-D Flyway | I-D Flyway |
| Multi-DB rollout | N-D; old stage order FAIL | N-D batch; C engine rollout | C engine rollout/selection | I-D playbook; C release semantics |
| Audit | N-D EE; FREE blocked | N-R partial; C durable correlation | N-S; C release/export correlation | N-D activity; C DB release record |
| Failure handling | N-D limited; recovery NOT_RUN | I-D history + C reconcile | I-D history + C reconcile | I-D history + C reconcile |
| API | N-S/D; FREE partial R | N-R partial; hook/writeback UNKNOWN | N-S webhook; executor hook UNKNOWN | N-D v2 |
| Self-host | N-D | N-D | N-D | N-D |
| DB-count limit | FREE/Pro 10; EE configured entitlement | No cap found in reviewed OSS; batch 100 | Old 10/5 not current; selected paths no cap | OSS no commercial target quota found |
| Free/open-source | MIT subset; EE commercial | Apache app + Apache engine | Apache app + Apache engine | Apache AWX + Apache engine |

| Capability | Bytebase EE (benchmark) | Rundeck CE + Flyway | Jenkins + Flyway | Archery native |
| --- | --- | --- | --- | --- |
| DB inventory | N-D | I node model; C schema registry | C Git manifest + generated view | N-S instances/groups |
| SQL editor/change UI | N-D | I Git; N-D job UI | I Git; N-D pipeline UI | N-S ticket UI |
| Git integration | N-D | N-D job SCM; I SQL Git | N-D pipeline/SCM | I/C commit correlation |
| Review | N-D | I Git + C policy | I Git + C policy | N-S Oracle review scope |
| Approval | N-D EE | I Jenkins; C binding | N-D input; C actor/hash binding | N-S workflow; binding unverified |
| RBAC | N-D | N-D ACL | I-D authorization plugins; C policy | N-S workflow permissions |
| Oracle | N-D | I-D engine | I-D engine | N-S; release/client boundary |
| Multi-DB rollout | N-D | I job/node dispatch; C waves | C serial/waves/promotion | — immutable release promotion |
| Audit | N-D EE | N-D execution/ACL; C correlation | N-D build; C publisher/retention | N-S ticket result; C Git linkage |
| Failure handling | N-D limited | I-D history + C reconcile | I-D history + C reconcile | N-S statement error; — target ledger |
| API | N-S/D | N-D REST; some endpoints commercial | N-D Jenkins API; CLI engine | N-S workflow routes |
| Self-host | N-D | N-D | N-D | N-D |
| DB-count limit | FREE/Pro 10; EE entitlement | OSS no count quota found | OSS no count quota found | No cap found in reviewed source |
| Free/open-source | MIT subset; EE commercial | Apache app + engine | MIT core + Apache engine | Apache app; Oracle client terms riêng |

Evidence per column: [Bytebase](#s1--bytebase-enterprise), [ODC](#s2--odc-workflow--sole-flyway-executor), [CloudDM](#s3--clouddm-workflow--sole-flyway-executor), [AWX](#s4--awx--flyway), [Rundeck](#s5--rundeck-community--flyway), [Jenkins](#s6--git--jenkins--flyway), [Archery](#s7--archery). “No cap found” không là capacity test hoặc full image/dependency entitlement audit.

## 6. Licensing và khả năng mở rộng 50 DB / 20 người

Phân biệt **Open Source** (license OSS), **Source Available** (đọc được source nhưng hạn chế quyền), **Free Tier/Community Edition** (gói phân phối, không tự là OSS), **Commercial** và **Trial** (có thời hạn). Không bỏ check artifact/client license vì root app là Apache/MIT.

| Candidate / component | License/edition, self-host | User/DB limits, Oracle | SSO/RBAC, approval, audit, API boundaries |
| --- | --- | --- | --- |
| Bytebase S1 | MIT cho subset; enterprise/enablement excluded; EE commercial, self-host | DOC pricing Community 20 users/10 instances, Pro 10 instances, EE custom; SOURCE 3.23.0 FREE 10/20, TEAM 10/unlimited seats, EE -1/-1. Oracle không mặc định EE-only; fleet license là gate | Basic IAM/Git/review/API có FREE; custom approval, external secret manager, OIDC/LDAP/custom roles/full audit EE. Pro audit 7 ngày; EE unlimited retention theo DOC. API service có permission/feature gates; không thấy quota API numeric chung |
| ODC S2 | Backend/frontend Apache-2.0; self-host | Không tìm cap seat/DB trong paths đã rà; batch 2–100 tasks/project. Oracle thật SOURCE và RUNTIME đúng build cũ | Project/RBAC/approval/audit API có evidence; SSO có cấu hình docs nhưng provider/edition/build cần preflight. Retention/export/hook chưa chứng minh; không gán native Vault |
| CloudDM S3 | v4.3.0 app Apache-2.0; self-host | Current official site không còn bảng 10/5; selected source/binary account/datasource paths không gọi cap. Không chứng minh mọi path/unlimited runtime | RBAC/SQL approval/webhook SOURCE; full SSO matrix/audit retention/export/adapter APIs UNKNOWN. Không còn căn cứ áp 10/5 cache như current license |
| AWX S4 | Apache-2.0; self-host; AAP/Controller là commercial product khác | Không seat/DB commercial quota trong OSS reviewed docs; Oracle qua engine, không native DB executor | RBAC/approval node/API DOC; auth integrations thuộc AWX docs, kiểm IDP cụ thể. Job/activity cleanup cần export trước purge; enterprise Controller features không tự thuộc AWX |
| Rundeck S5 | Apache-2.0 CE; self-host; Runbook Automation commercial riêng | Không cap 20 users/50 nodes trong CE nguồn đã kiểm; Oracle qua engine | ACL/API/job history native; approval cần ngoài. SSO/plugins và enterprise-only API phải kiểm đúng plugin/endpoint; không mua enterprise mặc định |
| Jenkins S6 | MIT core; self-host; kiểm license/security từng plugin | Core không commercial seat/DB count quota; Oracle qua engine | Input là plugin capability DOC; authorization/SSO bằng plugin. Durable audit/export/hash policy custom; admin exception. Không paid API gate core được phát hiện |
| Archery S7 | Apache-2.0 app; self-host | Không cap 50/20 tìm thấy; Oracle release dependency cx_Oracle + Instant Client | Resource/workflow permissions SOURCE; SSO, retention/export và Git release APIs chưa đủ evidence, không coi là không giới hạn verified |
| Flyway chung S2–S6 | Apache-2.0 OSS source/Community engine; self-host CLI. Redgate distribution/Teams/Enterprise có commercial terms | Core versioned migrations/history/validate Oracle DOC; no estate inventory/users. Không thấy Community DB quota tương đương Bytebase | SQL*Plus emulation/Undo/advanced features có commercial boundaries; approval/audit/SSO portal **không có** trong CLI; không gọi paid features trong baseline |
| GitLab trong compositions | CE core MIT; EE có terms riêng; self-managed Free/Premium/Ultimate khác nhau | Git/project hosting không đặt Bytebase DB cap; Oracle qua runner | Free MR review/optional approvals; required approval rules/deployment approvals/native external-secrets integration có Premium/Ultimate boundary. API existence không bỏ tier gates |
| Secret service | OpenBao MPL-2.0 OSS self-host; HashiCorp Vault current source BSL-1.1, Enterprise commercial | Chọn existing secret manager nếu có; OpenBao là reference OSS fallback. Không giả định Oracle dynamic-secret plugin miễn phí/có sẵn | JWT/AppRole/KV là interfaces DOC; Oracle rotation và Jenkins/GitLab adapter phải verify riêng. Không gọi Vault current releases là OSS |

Licensing sources: [Bytebase pricing](https://www.bytebase.com/pricing/), [plan 3.23.0](https://github.com/bytebase/bytebase/blob/c8188c635465321ff930c97200742a96ef653144/backend/enterprise/plan.yaml), [MIT boundary](https://github.com/bytebase/bytebase/blob/c8188c635465321ff930c97200742a96ef653144/LICENSE), [EE license](https://github.com/bytebase/bytebase/blob/c8188c635465321ff930c97200742a96ef653144/LICENSE.enterprise); [ODC backend license](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/LICENCE), [frontend license](https://github.com/oceanbase/odc-client/blob/273fa3c4cc7d87f942ade231ce9220b98fa595e2/LICENSE); [CloudDM exact-artifact review](research-round-2/coordinator/clouddm-v430-artifact-review-20261007.md); [AWX license](https://github.com/ansible/awx/blob/24.6.1/LICENSE.md), [credentials/auth docs](https://docs.ansible.com/projects/awx/en/24.6.1/userguide/credentials.html); [Rundeck license](https://github.com/rundeck/rundeck/blob/e649f088e039b0fabbbb7039f730cbbcc183f82d/LICENSE), [enterprise distribution](https://docs.rundeck.com/docs/enterprise/); [Jenkins license](https://github.com/jenkinsci/jenkins/blob/master/LICENSE.txt); [Archery license](https://github.com/hhyo/Archery/blob/bc1f10efcc465f6a63c94b97feaba5d15546712a/LICENSE); [Flyway OSS distribution](https://documentation.red-gate.com/flyway/reference/usage/flyway-open-source), [commercial FAQ](https://documentation.red-gate.com/flyway/learn-more-about-flyway/commercial-licensing-faq); [GitLab CE license](https://gitlab.com/gitlab-org/gitlab-foss/-/blob/master/LICENSE), [GitLab tiers](https://docs.gitlab.com/ci/environments/deployment_approvals/); [OpenBao license](https://github.com/openbao/openbao/blob/main/LICENSE), [Vault license](https://github.com/hashicorp/vault/blob/main/LICENSE).

**Bytebase conclusion:** Community và Pro không đủ 50 instance theo cả current pricing và reviewed source. EE có thể đáp ứng count nhưng cần quote đúng self-host SKU, service accounts, project/service/PDB/schema counting, Oracle, audit, SSO và external secrets. Pro $20/user/tháng không được nhân 20 để suy tổng 50-instance solution. Source enum TEAM và marketing Pro chưa map hoàn toàn; lấy exact edition contract, không tự mua/trial. Chưa có tổng chi phí phù hợp để so tiền với engineering effort.

## 7. Credential management và access model

| Hướng | Native store / evidence | Proposed deploy secret path và rotation |
| --- | --- | --- |
| Bytebase EE | External secret manager feature trong SOURCE plan, DOC pricing | Platform service identity đọc secret reference; verify provider/auth/rotation trên edition thực. Không giả định FREE có tính năng này |
| ODC | **SOURCE mới tại pin d517c0f…**: ConnectionService encrypt trước persistence; ConnectionEncryption chọn AES256SALT; organization secret dùng trong EncryptionFacadeImpl | UI chỉ giữ read-only metadata credential nếu cần; Oracle deploy secret ở external service, runner fetch khi execution. Key/store cùng failure domain không tương đương external secret manager |
| CloudDM | GitLab guide nói integration tokens plaintext MetaDB. Oracle password encryption/rotation trong actual artifact chưa audit ở vòng này | Deploy credential ngoài app; scoped intake token, MetaDB access/backup controls; token rotation/update và adapter ownership phải explicit |
| AWX | Credentials lưu encrypted theo AWX docs; external credential integrations DOC | Scope credential theo template; runner account per schema/env; verify injector/backend version và rotation |
| Rundeck CE | Key storage/ACL DOC; provider/encryption config phải kiểm | Engine runner fetch secrets hoặc key-storage provider đã kiểm; CE approval vẫn ngoài |
| Jenkins | Credentials encrypted trên controller, credential IDs/scope DOC | Lab có thể dùng folder-scoped credentials; target model dùng credential_ref. Reference OSS path runner gọi OpenBao KV qua short-lived identity; adapter chưa viết |
| Archery | Stored connection credentials; encrypt-at-rest/key-management của release chưa establish từ review này | Không rollout adoption trước kiểm store/rotation; Git chỉ giữ refs, không password |

Nguồn SOURCE ODC vừa đọc: [ConnectionService:306–333](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/connection/ConnectionService.java#L306-L333), [ConnectionEncryption:43–91](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/connection/ConnectionEncryption.java#L43-L91), [EncryptionFacadeImpl:95–110](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/encryption/EncryptionFacadeImpl.java#L95-L110). Đây là selected source read, không security audit hoặc runtime proof của image. [Jenkins credential store](https://www.jenkins.io/doc/book/using/using-credentials/), [OpenBao JWT auth](https://openbao.org/docs/auth/jwt/), [GitLab Vault integration](https://docs.gitlab.com/ci/secrets/hashicorp_vault/) (native feature có tier gate).

DESIGN chung: account deployment riêng theo service/schema/environment, không chung DBA credential; requester không đọc secret và không có direct PROD write. Database grants và network policy phải chặn đường DBeaver/manual SQL ngoài flow quản lý; nếu giữ quyền viết trực tiếp thì không có complete central audit. Break-glass qua DBA có ticket, thời hạn và audit reconciliation. Không cấp SYSDBA/ANY mặc định.

Kubernetes Secret là delivery mechanism, **base64 không phải encryption-at-rest**; không commit Secret manifest plaintext, private wallet/key, kubeconfig hoặc token. [Kubernetes Secret documentation](https://kubernetes.io/docs/concepts/configuration/secret/) (**DOC**). Env vars chỉ là cách inject tạm, không secret system of record; tránh shell trace/process/log/archived workspace leak. Oracle password rotation: DBA đổi credential theo quy trình có thể hồi phục, secret manager cập nhật version, runner dùng version mới cho dispatch sau, revoke version cũ; in-flight session và pool refresh phải kiểm. Không hứa Oracle dynamic credentials trước khi xác minh plugin/license.

## 8. Architecture A/B/C và build vs buy vs compose

| Mô hình | Centralized | Trong Git / ngoài Git | Burden chuyển về đâu |
| --- | --- | --- | --- |
| A Bytebase EE | Inventory, policy, SQL/change UI, approval, release/task, audit | SQL/manifest trong Git; runtime state trong platform; secrets native store/external provider | Vendor/platform admin vận hành và paid entitlement; DBA vẫn chịu target/recovery |
| B ODC/CloudDM + engine | Platform inventory/review/approval; adapter tổng hợp release/target result | SQL/hash/target manifest trong Git; workflow metadata + result store; secrets ngoài executor UI | Team integration sở hữu hook, model mapping, actor/hash binding, disable duplicate execution, writeback |
| B AWX/Rundeck + engine | Automation inventories/jobs/RBAC/logs | SQL và jobs/playbooks trong Git; result publisher/secret service riêng | DevOps chịu database model/approval/audit contract; DBA dùng job UI |
| C Git/Jenkins + engine | CI requests/gates/history; generated inventory/release summary và durable evidence | SQL/migrations/inventory/shared libraries trong Git; secrets ở manager; run state/log/artifact ngoài Git | DevOps chịu code, plugins, trusted runner, result/reconcile; users chuyển giữa Git và Jenkins |

| Solution | Cách dùng | Deployment complexity | Maintenance | Integration | Custom development | Operational ownership |
| --- | --- | --- | --- | --- | --- | --- |
| Bytebase EE | Configure/integrate; gần use as-is | MEDIUM | MEDIUM | LOW–MEDIUM | LOW–MEDIUM | MEDIUM |
| ODC + Flyway | Compose + adapter | HIGH | HIGH | HIGH | HIGH; VERY HIGH nếu phải fork executor | HIGH |
| CloudDM + Flyway | Compose + adapter | HIGH | HIGH | HIGH | HIGH; VERY HIGH nếu hook không supported | HIGH |
| AWX + Flyway | Compose | HIGH nếu dựng mới | HIGH (upstream pause) | MEDIUM–HIGH | HIGH DB model/recovery | HIGH |
| Rundeck + Flyway | Compose | MEDIUM | MEDIUM–HIGH | HIGH approval/correlation | HIGH | HIGH |
| Jenkins + Flyway | Compose | MEDIUM nếu có CI, HIGH nếu dựng mới | MEDIUM–HIGH | MEDIUM–HIGH | HIGH policy/result/inventory | HIGH |
| Archery native | Configure cho ticket; custom cho full release | MEDIUM | MEDIUM | HIGH cho desired release | VERY HIGH nếu xây release model | HIGH |

Các mức là judgment so khối việc còn thiếu, không số chi phí hoặc measured person-days. Không giả định license OSS làm maintenance miễn phí. Không lập platform riêng ở vòng đầu; các adapter/runner/result publisher là custom functionality hữu hạn nhưng vẫn cần owner, regression và upgrade contract. Nếu phải sửa sâu ODC/CloudDM để external executor hoạt động, chuyển sang C hoặc so quote A trước khi đầu tư fork.

## 9. Operational workflow cho team 20 người

Không tự chia 20 người thành số seat từng role; một người có thể nhiều role nhưng **cùng change PROD** phải tách requester/reviewer/approver/executor theo policy. Role mapping chi tiết nằm ở reference architecture.

| Solution | Developer | Reviewer | DBA/Approver | DevOps và burden mới |
| --- | --- | --- | --- | --- |
| Bytebase EE | Commit SQL, create change/plan linked Git | SQL diff/check findings, comment/reject | Verify inventory target, approve PROD, monitor rollout/reconcile | Onboard projects/roles/SSO/secrets, entitlement, audit export/backup; ít workflow code |
| ODC + Flyway | Commit, select ticket/change trong ODC | Git diff + ODC SQL/target preview | ODC approve; theo dõi engine result link; không Execute native | Maintain hook/mapper/state/writeback, separate read vs deploy credentials, durable logs; burden adapter lớn |
| CloudDM + Flyway | Commit, webhook tạo flow/ticket | Audit findings + Git diff | Approve exact target/artifact; monitor callback/CI link | GitLab integration token, HTTP auth, duplicate suppression, result mapping; giữ native execution off |
| AWX + Flyway | MR và request workflow qua restricted intake | Git review + immutable release summary | Approval node trên workflow do CI launch, job output | Inventory plugin/schema model, execution environment, actor restrictions, workflow vars; upgrade/refactor burden |
| Rundeck + Flyway | MR, request release/job options từ allowlist | Git review, Jenkins gate | Approve qua Jenkins; chạy/monitor authorized job | Sync node catalog/ACL + CI policy + result publisher; có hai controller |
| Jenkins + Flyway | Commit MR, create build với release/target IDs | Git diff + Jenkins Reviewer input | DBA input PROD; xem per-target summary và recovery incident | Trusted library/inventory/locks/postchecks/audit export; ownership tập trung DevOps thay DBA thao tác từng endpoint |
| Archery | Submit SQL ticket (Git reference ngoài) | Review Oracle SQL ticket | Approve/execute từng ticket, xử lý partial statement | Portal/client/backup; release/promotion/version correlation vẫn thiếu |

DEV có thể developer trigger sau validation; SIT/UAT thêm reviewer; PROD thêm DBA/approver độc lập và restricted service executor. Manual trigger, scheduler hoặc webhook đều phải kiểm lại approval/maintenance window/hash ngay trước dispatch. Scheduling không là quyền vượt gate.

## 10. Failure, recovery, verification và audit

Oracle có implicit COMMIT trước DDL hợp lệ và sau DDL thành công; script lỗi có thể để lại table/column/procedure đã tạo. COMMIT/ROLLBACK của DML không làm cả release DDL atomic. [Oracle commit semantics](https://docs.oracle.com/en/database/oracle/oracle-database/19/tdddg/committing-transactions.html) (**DOC**, dùng cho nguyên lý, không certification version nội bộ).

| Layer / công cụ | Cơ chế có evidence | Giới hạn và policy đề xuất |
| --- | --- | --- |
| Flyway engine | Version/history/checksum/validate DOC/SOURCE; schema history từng target | Không portal approval/INVALID gate/exactly-once Oracle DDL. `repair` sửa history metadata, không undo object/data; cleanup/reconcile phải trước |
| Liquibase engine | DBCL/DBCLLOCK, rollback definitions và release-locks DOC | Rollback là DDL/DML bù; formatted SQL cần explicit rollback. Release-locks chỉ gỡ mutex; không reconcile đã commit |
| Sqitch | Deploy/revert/verify scripts, registry DOC/SOURCE | Oracle deploy script có thể partial trước fail; engine không suy toàn change chưa có effect; tác giả chịu revert/verify semantics |
| Bytebase | Central revisions/task runs, replay RUNTIME partial | FREE strict checksum/INVALID/promotion failures; recovery UNKNOWN. UI rollback không mặc định Oracle DDL/data restore |
| ODC | Statement ABORT/retry config, task results RUNTIME/SOURCE | Native lacks required target identity/dedup; retryTimes=0 không tạo recovery protocol. Batch abort limitations và log retention phải kiểm |
| CloudDM | Webhook receipt dedup/source compile branch SOURCE | Receipt không migration checksum/target mutex; default compile gate off; không native crash reconciliation established |
| AWX/Rundeck/Jenkins | Workflow stop/failure/output DOC | Orchestrator timeout/cancel không chứng minh Oracle session đã dừng. Retry stage/script phải bị chặn khi outcome uncertain |
| Archery | Per-statement commit, error/INVALID check SOURCE | Oracle partial effects; version/replay/resume chưa establish |

[Flyway repair](https://documentation.red-gate.com/flyway/reference/commands/repair), [schema history](https://documentation.red-gate.com/flyway/flyway-concepts/migrations/flyway-schema-history-table), [validate](https://documentation.red-gate.com/flyway/reference/commands/validate); [Liquibase rollback](https://docs.liquibase.com/oss/reference-guide-4-33/init-update-and-rollback-commands/rollback), [DBCLLOCK](https://docs.liquibase.com/oss/user-guide-4-33/what-is-the-database-changelog-lock-table); [Sqitch deploy](https://sqitch.org/docs/manual/sqitch-deploy/). Source limitations được kế thừa tại [engine evidence](../EVIDENCE.md).

**DESIGN release state:** PLANNED → VALIDATED → REVIEWED → APPROVED → RUNNING → VERIFIED; target có NOT_STARTED, RUNNING, APPLIED_VERIFIED, FAILED_KNOWN, PARTIAL, APPLIED_INVALID, UNKNOWN_OUTCOME. APPLIED_INVALID nghĩa engine có thể đã ghi success nhưng postcheck fail; không replay cùng version để “sửa”. Một target partial/unknown/invalid làm release HOLD; các target đã verified giữ trạng thái thực, những target chưa dispatch giữ NOT_STARTED; không ghi global SUCCESS hoặc rollback fleet giả.

Recovery runbook: dừng dispatch/promotion; giữ log/attempt và xác định session; DBA so approved SQL, history, ALL_OBJECTS/ALL_ERRORS, column/data postconditions và session/lock info. Nếu worker/session còn chạy, không cấp lock mới. Nếu mất ack sau commit, ghi UNKNOWN_OUTCOME và reconcile trước mọi retry. DBA chọn forward-fix migration mới, approved repair/history correction sau kiểm effect, compensating script được review, hoặc restore theo scope backup/RTO/RPO. Killing session/releasing stale lock là thao tác DBA được duyệt, không retry hook tự làm. Target lease hết hạn không fence session Oracle cũ.

Verification mỗi target gồm artifact và executed script digest, target identity/schema, engine info/validate/history/version, timestamps/duration/error/exit status, touched-object validity và postcondition query. Baseline invalid objects được ghi để phân biệt invalid mới; package spec/body được kiểm riêng. Drift **khác checksum history**: scheduled metadata compare/snapshot là integration cần POC/object coverage/edition check, chưa native Community guarantee. DDL affected-row count có thể không meaningful; không invent row counts.

Audit cần một release summary có requester, reviewer, approver, executor/service identity, Git commit/MR, artifact/target-set/inventory hash, SQL artifact reference, execution ID, target/service/schema, attempt, start/end/duration, result/errors, verification/recovery decision và evidence URL. Native ticket/build/task/history chỉ là từng phần. S2–S6 cần result publisher và export; evidence store phân quyền read và write riêng, append-only theo attempt, backup/restore, retention được owner chọn. Artifact SQL được giữ ở khu vực restricted; public/report log chỉ allowlisted/redacted fields. CI artifact có expiry không tự là audit retention. ODC log mất sau restart lịch sử là ca regression bắt buộc.

## 11. Engine Oracle và CI/CD

**Best migration engine cho baseline: Flyway Community**, vì có version/history/validate, Oracle JDBC DOC và team đã dùng CLI; đây là lựa chọn giảm thay đổi engine, không tuyên bố mọi workload đã PASS. [Oracle driver/support](https://documentation.red-gate.com/flyway/reference/database-driver-reference/oracle-database) liệt kê driver versions 12.2/18c/19c/21c/23ai/26ai, nhưng verified versions trang hiện tại chỉ 18.4/26ai; không gọi toàn danh sách là tested. Community Java dùng module `org.flywaydb:flyway-database-oracle`; JDBC/driver/client terms riêng.

| Engine alternative | License/Oracle evidence | Khi nào đáng thay engine baseline |
| --- | --- | --- |
| Flyway Community | Apache OSS engine, Oracle DOC/SOURCE; [13.9.0 release notes](https://documentation.red-gate.com/fd/release-notes-for-flyway-engine-179732572.html) là current catalog pin | Versioned SQL phù hợp; không cần paid SQL*Plus emulation/Undo/state-based features. Verify actual OSS package/module/driver digest |
| Liquibase 4.33.0 | Apache-2.0 tại [release license](https://github.com/liquibase/liquibase/blob/v4.33.0/LICENSE.txt), Oracle JDBC DOC/SOURCE | Structured changeset/precondition/rollback authoring hữu ích; older branch maintenance/support cần xét. [4.33 Oracle](https://docs.liquibase.com/oss/integration-guide-4-33/connect-liquibase-with-oracle-database?entryId=4UUfehgRhjsmaVLoD6eckC) |
| Liquibase Community 5.0.4 | **FSL-1.1-ALv2 source available**, không OSS trước conversion; Oracle DOC | Nếu chấp nhận FSL và packaging/modules/driver owner; không coi upgrade license-neutral. [5.0 release notice](https://github.com/liquibase/liquibase/releases/tag/v5.0.0), [5.0.4 Oracle](https://docs.liquibase.com/community/integration-guide-5-0-4/connect-liquibase-with-oracle-database) |
| Sqitch 1.6.1 | MIT; Oracle SQL*Plus/DBD::Oracle DOC/SOURCE, client terms riêng | Dependency graph và explicit deploy/revert/verify cần thiết; client setup nặng hơn. [Oracle tutorial](https://sqitch.org/docs/manual/sqitchtutorial-oracle/) |
| Oracle SQLcl Project | Free download theo Oracle terms, không OSS platform; Oracle-first DOC | Nhiều PL/SQL/object export/authoring hoặc required SQLcl/native commands. [Project workflow](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/26.1/sqcug/project.html) |

Không đề xuất Atlas OSS cho Oracle (Oracle Pro-only), dbmate vì Oracle chưa established, hoặc custom SQL runner tự viết parser/history/recovery. Nếu SQL*Plus directives là hard requirement, chặn promotion cho đến khi có licensed supported execution path qua SQLcl/SQL*Plus hoặc Flyway edition phù hợp đã kiểm. Plain ALTER TABLE scenario không chứng minh SQL-04–12.

CI trigger contract chung (**DESIGN**): authenticated webhook/API/manual build nhận `release_id`, commit và requested target IDs; trusted adapter resolve inventory, verify MR/gates và immutable hashes; service executor fetch deploy secret rồi `info → validate → migrate → postcheck → info/history → publish`. Pipeline không nhận password/DSN tùy ý. Dry-run không gọi `migrate`; output simulation phải ghi SIMULATED. Jenkins/GitLab job thật đều **NOT_RUN** trong lượt này.

## 12. Decision matrix có trọng số

Giữ baseline user đề nghị, tổng **100**; đây là matrix **documented fit/readiness cho solution nghiên cứu**, không thay matrix acceptance cũ hoặc benchmark. Score 0–5: **0** không có evidence/không có khả năng; **1** gap lớn, chủ yếu custom/unresolved; **2** partial DOC/SOURCE hoặc significant integration; **3** component capability đủ theo DOC/SOURCE, chưa runtime end-to-end; **4** relevant native runtime lịch sử trong phạm vi hẹp; **5** end-to-end đúng edition/Oracle/50-target scale đã chứng minh. Không có điểm 5. Unknown hook/binding không được điểm 3 như supported integration. Maintenance điểm cao nghĩa ít burden; điểm judgment không evidence runtime.

`Weighted = Σ(weight × score / 5)`. License score 3 cho OSS reviewed terms/no cap found; score 1 cho commercial chưa biết quote/entitlement phù hợp yêu cầu ưu tiên OSS. Score license không có nghĩa Bytebase không scale. Runtime ODC chỉ tăng inventory/UX, không nâng engine-composition/recovery score. UI và inventory có weight thấp/hẹp, tránh đếm số PASS hai lần.

| Criterion | Weight | S1 BB EE | S2 ODC+FW | S3 CDM+FW | S4 AWX+FW | S5 RD+FW | S6 CI+FW | S7 Archery |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Oracle support | 15 | 3 | 3 | 3 | 3 | 3 | 3 | 2 |
| License/scalability to ~50 DB | 15 | 1 | 3 | 3 | 3 | 3 | 3 | 3 |
| Centralized inventory | 10 | 3 | 4 | 3 | 2 | 2 | 1 | 3 |
| Review/approval | 10 | 3 | 2 | 2 | 2 | 1 | 2 | 2 |
| Multi-DB rollout | 10 | 3 | 2 | 1 | 2 | 2 | 2 | 1 |
| Audit/traceability | 10 | 3 | 2 | 2 | 2 | 2 | 2 | 2 |
| Git/CI/CD | 10 | 3 | 2 | 3 | 3 | 3 | 3 | 1 |
| Failure/recovery | 8 | 2 | 2 | 2 | 2 | 2 | 2 | 1 |
| Credential management | 5 | 3 | 2 | 1 | 3 | 2 | 3 | 1 |
| UI/UX | 4 | 3 | 4 | 3 | 3 | 3 | 2 | 3 |
| Maintenance burden | 3 | 3 | 1 | 1 | 1 | 2 | 2 | 2 |
| **Weighted / 100** | **100** | **52.4** | **51.0** | **47.2** | **49.2** | **46.8** | **47.0** | **39.2** |

| Candidate | Lý do score và evidence liên quan |
| --- | --- |
| S1 | Oracle/inventory/approval/rollout/Git/audit/credentials/UX =3 từ current EE DOC/SOURCE plan; EE không thừa hưởng RUNTIME FREE. Recovery =2 vì old correctness FAIL/controlled recovery NOT_RUN. License =1 vì quote unresolved, maintenance =3 do one product/configuration với custom scope thấp nhất. [S1 evidence](#s1--bytebase-enterprise) |
| S2 | Inventory/UX =4 từ native RUNTIME project/ticket UI; Oracle =3 từ Flyway DOC, không 4 cho stack. Approval/rollout/Git/audit/secret/recovery =2 do native partial và external contract còn gap. License =3 app/engine OSS; maintenance =1 do adapter/hook/writeback. [S2 evidence](#s2--odc-workflow--sole-flyway-executor) |
| S3 | Oracle/Git/inventory/UX =3 từ DOC/SOURCE component paths; review/audit/recovery =2 và rollout =1 do engine handoff/target fanout unknown. Secret =1 vì plaintext integration tokens/external path chưa kiểm; license =3 public artifact/source finding, maintenance =1 adapter. [S3 evidence](#s3--clouddm-workflow--sole-flyway-executor) |
| S4 | Oracle/Git/credential/UI/license =3 từ component DOC/license; inventory =2 host→schema mapping; approval =2 launch/approve overlap; rollout/audit/recovery =2 cần contract. Maintenance =1 upstream pause+new controller. [S4 evidence](#s4--awx--flyway) |
| S5 | Oracle/Git/UI/license =3 component DOC; inventory/rollout/audit/recovery/secrets =2 integration; approval =1 CE lacks proved binding, outside approval service needed. Maintenance =2 thêm controller. [S5 evidence](#s5--rundeck-community--flyway) |
| S6 | Oracle/Git/credential/license =3 component DOC; inventory =1 custom; review/rollout/audit/recovery/UI =2 engine/CI screens chưa đủ DB semantics. Maintenance =2 trusted libraries/plugins/publisher. [S6 evidence](#s6--git--jenkins--flyway) |
| S7 | Inventory/UI/license =3 SOURCE/license; Oracle/review/audit =2 parser/client/partial coverage; rollout/Git/recovery/secrets =1 major unknown/gaps; maintenance =2 native ticket baseline, chưa gồm platform tự viết. [S7 evidence](#s7--archery) |

Không xếp 51.0 như certainty cao hơn 49.2: source→artifact mapping/edition evidence khác nhau và mọi stack còn gates. Nếu quote Bytebase đáp ứng 50/20 và budget, tăng riêng license score rồi so lại; không tự tăng correctness. Nếu already-owned AWX/Rundeck/Jenkins, maintenance/deployment có thể tốt hơn; ghi assumption trước re-score. Theo ưu tiên UX đã có và bài toán hiện trạng, chọn POC S2/S6 dù S4 documented-fit tổng cao hơn S6 một chút: S6 ít controller mới hơn và không cần AWX release line đang pause.

## 13. Recommendation và POC tiếp theo

| Recommendation yêu cầu | Kết luận có phạm vi |
| --- | --- |
| Best integrated platform | **Bytebase Enterprise** documented fit; không loại vì chưa biết quote, không production acceptance |
| Best OSS/self-hosted approach | **ODC governance + sole Flyway executor**, có điều kiện supported handoff/disable-native/writeback. Nếu contract thất bại, chọn CI composition thay vì fork platform mặc định |
| Best migration engine | **Flyway Community** cho versioned SQL baseline; Liquibase 4.33/Sqitch/SQLcl khi workload/object/directive cần khác |
| Best CI/CD-centric architecture | **Git + Jenkins + Flyway + reviewed target manifest + structured evidence publisher**. GitLab Premium native CI là alternative nếu đội đã có entitlement |
| Best Bytebase alternative worth POC | **S2 ODC+Flyway** gần workflow nhất nhờ UI/governance runtime; **S3 CloudDM+Flyway** là challenger SOURCE, không native executor winner |

**POC #1 — S2:** chứng minh contract ngoại vi trước: login/inventory/ticket/approval → đúng immutable artifact/target set → sole external executor → result/audit. Thất bại ở hook hoặc requester/native write suppression thì STOP S2, chưa viết platform fork. Oracle correctness probe chỉ sau delta và quyền lab mới.

**POC #2 — S6:** đối chứng ít phụ thuộc platform: Git/Jenkins screens, generated inventory/status view, reviewer/DBA gates, Flyway runner và per-target evidence. Phải chứng minh cải thiện estate operation, không chỉ bọc CLI trong Docker. Nếu không có Jenkins và team đã có GitLab Premium thì dùng cùng contract trên GitLab.

**Optional POC #3 — S3:** chỉ khi CloudDM supported flow action cho external engine rõ hơn S2 hoặc đội ưu tiên GitLab/UI. Không repeat native v4.3.0 correctness; demo new adapter architecture, plaintext integration-token handling và native-executor denial. Không dựng cả AWX/Rundeck chỉ để mở thêm catalog.

[POC plan](poc-plan.md) ghi topology, image/source pins, lab files cần tạo, screen walkthrough, contract gates, 45-case mapping, failure injection, artifacts và stop rules. Bytebase EE demo/quote có thể làm read-only commercial benchmark sau này nếu được yêu cầu; không đăng ký trial trong vòng này.

## 14. Trả lời trực tiếp bước tiếp theo hợp lý nhất

**Giữ Flyway làm engine, thử tập trung hóa control workflow trước khi đổi engine hoặc tự viết một platform lớn.** Ngày mai team có thể bắt đầu POC #1 ở contract/dry-run stage và chuẩn bị POC #2 làm đối chứng; cả hai chưa cần Oracle production credentials. Kết quả contract quyết định có nên đầu tư adapter hay chuyển sang CI composition.

| Câu hỏi vận hành | Đáp án target operating model |
| --- | --- |
| Tool(s)/architecture | Primary POC ODC+Flyway/CI adapter (B); fallback Git+Jenkins+Flyway (C); Bytebase EE benchmark (A) |
| Workflow | Git change/MR → validation → reviewer → select/freeze targets → approval → DEV/SIT/UAT → DBA PROD gate → rollout → postcheck → evidence |
| Centralized gì | Inventory catalog, actor/gates, exact release/target status, links log/history, recovery decisions; UI ODC hoặc Jenkins + generated views |
| Giữ gì trong Git | SQL/migrations, verification/recovery scripts, inventory metadata/secret refs, release manifest, trusted pipeline/adapter code; không credentials |
| Credentials ở đâu | Existing secret manager hoặc OpenBao KV reference; restricted runner fetch. ODC UI credential read-only encrypted store nếu cần; deploy secret không nằm ở UI |
| CI/CD trigger thế nào | Authenticated webhook/API/manual build với release ID + immutable commit; allowlisted target selection; Jenkins/GitLab exact job identity |
| Approvals thế nào | Preview artifact/target set trước approval, capture reviewer/DBA khác requester, bind hashes; đổi SQL/target/policy invalidates, recheck ngay dispatch |
| Audit thế nào | Structured per-target result + Git/MR/approval/task/job IDs + artifact/evidence references; durable store/export, retention được chọn và restore tested |
| Failed release thế nào | Stop wave/promotion, hold partial/invalid/unknown, DBA inspect history/object/session, approve forward-fix/repair/compensation/restore; không blind retry |
| Custom-built gì | B: external executor adapter, binding/denial/writeback. C: inventory view, trusted gate/runner, result publisher/state reconciliation. Cả hai cần target/session-aware postcheck/runbook |

## 15. Unknowns cần giải trong lab/adoption

| Unknown | Cách giải / ảnh hưởng |
| --- | --- |
| Oracle versions/topology/object mix | DBA cấp metadata sanitized; chọn lab đúng major/RU, service/PDB/schema. Không chốt engine/client certification từ 26ai cũ |
| ODC/CloudDM external executor contract | POC contract stage tìm supported post-approval hook, auth/result path; fail thì redirect C. Không đánh dấu adapter supported trước proof |
| Full artifact/dependency license và source mapping | Pin actual image/module/driver digest, notices; ODC source không map image. Selected CloudDM paths không full attestation |
| Existing CI/Git/SSO/secrets | DevOps chọn existing stack và provider; Jenkins/OpenBao là reference assumption, không khẳng định đã có |
| Scale50/users20/concurrency | Lab 50 inventory records + 20 role identities; Oracle thật 4 target isolated trước. Inventory-only smoke không chứng minh 50 live DB rollout |
| Retention/export/restore/key rotation | Owner chọn policy, POC restart/export/restore; không invent SLA hoặc unlimited native audit cho OSS |
| Approval bypass/admin/direct writes | Negative tests UI/API/console/CLI, privileged exception audit, no deploy credential outside restricted worker |
| Recovery/fencing/stale session | Controlled commit barrier + independent observer; unknown outcome requires hold. No exactly-once arbitrary Oracle DDL guarantee |
| Budget/maintenance | So quote A với code/controller burden B/C và owner capacity; chỉ qualitative effort, chưa cost/time saving |

## 16. Kiểm chứng nghiên cứu và giới hạn hoàn thành

Nguồn online quan trọng kiểm lại 07/10/2026: Bytebase pricing/plan/license; CloudDM current pricing và pinned GitLab guide; ODC pinned batch/approval docs và selected encryption source; AWX official docs/paused-release README; Rundeck release API/license/ACL/API; Jenkins input/credential docs; GitLab tiers/approvals/Vault integration; Flyway Oracle/repair docs; Liquibase 4.33 license/5.x Oracle/license notice; Oracle DDL semantics; OpenBao/Vault licenses. Links tại từng claim là primary sources; source license fetch chỉ xác nhận license, không execution implementation.

Discovery có giới hạn: không tìm thêm tool ngoài shortlist, không truy cập lab đang deployed, không liên hệ vendor, không check secrets thực. Tài liệu GitLab/Rundeck tier/security details bổ sung cho catalog; sửa nhầm tên Git tag Rundeck **trong hồ sơ mới**, giữ catalog bytes lịch sử. Không có DOC/SOURCE → RUNTIME conversion.

Definition of Done của vòng này là **tài liệu ra quyết định và bàn giao lab**, không chạy POC. Các expected và gates đủ để team khởi động sau khi có isolated lab authorization; unknown Oracle metadata/entitlement/hook đã có owner, test và stop/redirect rule. Kiểm local documentation và preservation sẽ được báo cùng kết quả công việc.

Kiểm tài liệu: `python tools/verify_research_documents.py` **PASS** (38 source snapshots, 183 source references, 11 screenshots, 45 authoritative criteria/POC IDs; không app/Oracle execution). Kiểm riêng links/anchors, bảng, fences và phép tính decision matrix; 60 URL nguồn trong ba tài liệu ban đầu trả HTTP 200, nguồn Kubernetes bổ sung được mở chính thức. So SHA-256 baseline 68.911 file chỉ có ba index cũ thay đổi; catalog/expected/workloads/evidence giữ nguyên. Repo hiện không có `.git`; review changes bằng baseline hash và unified diff, không có commit/push.
