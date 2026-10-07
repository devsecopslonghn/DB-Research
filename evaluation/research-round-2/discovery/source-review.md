# Source review — discovery vòng hai

Ngày review: 2026-10-04. Đây là review tài liệu/source công khai có chọn lọc. Không chạy app, build, test, SQL hoặc kết nối Oracle. Runtime tất cả lead mới: `NOT_RUN`. License mô tả artifact được kiểm, không thay legal review dependency/image.

## Kết quả quyết định

Không phát hiện platform OSS miễn phí nhóm A mới đủ evidence để thay Bytebase/ODC/CloudDM/AccessFlow. Lead bổ sung chia thành client/lineage, engine/CLI, desktop độc quyền và package chưa thể audit. Không đưa nhóm này vào shortlist platform.

| Lead | Pin / nguồn | License gate | Oracle evidence | Kết luận |
| --- | --- | --- | --- | --- |
| SQLark (Dameng) | Tài liệu sản phẩm, không có source pin | Installer miễn phí theo tuyên bố; source/quyền phân phối không công khai | Tài liệu Dameng nói kết nối Oracle và schema/data migration. V3.4 ghi Oracle 11g+; hướng dẫn có Oracle→DM và resume | Desktop migration workbench hữu ích nếu đích là DM. Không có source, server, shared ledger hoặc approval evidence; D |
| DbGate | `dbgate/dbgate@c6babf5933f9e9cd81c11bcf5889bdc54e35cb81` | Community GPL-3.0. Team Premium cần license. Oracle plugin GPL-3.0; `oracledb` optional, thick mode có Instant Client dependency | Source có Oracle connector, query/object editing và schema compare/sync. Không có migration release/gate evidence | DB client, không native release workflow; D |
| DBHub | `bytebase/dbhub@4ddb26e73c5d8f1d54f5d04351c11c3caeb43cbb` | Repo MIT; review dependency/package khi phân phối. Bytebase-affiliated | Oracle DSN/connector `node-oracledb` Thin mode, SQL, readonly tool, health check/EXPLAIN. Không chứng minh schema migration | MCP component, không UI/control plane hay alternative độc lập; D |
| Hue | `cloudera/hue@afa68e4008a550dfcef42c4a9b46d523396dd94c` | Apache-2.0 source; Oracle driver/deployment deps riêng | Oracle query adapter/editor qua `cx_Oracle`; không có versioned DDL release/promotion | Hadoop/SQL query UI, không migration governance; D |
| Gudu SQLFlow | `sqlparser/sqlflow_public@067cbbe1bce1c02090d41db89f8e06715e3fa459` | `LICENSE` là Commercial License Agreement/EULA; repo docs/sample không phải OSS implementation | Docs quảng bá Oracle lineage/parser và on-prem option. Không DDL deployment | Lineage/impact product, không migration platform; D |
| d-migrate | `pt9912/d-migrate@cd2ad60b4b4ffdf3ef363a16ab5adfacf2b7c62a` | Repo MIT. `ojdbc11` theo Oracle Free Use Terms, không MIT; module comment yêu cầu kèm license khi redistribute | README nêu Oracle schema/data operations. Repo có Oracle JDBC, profiling, integration-test modules. Module comment nói Oracle adapter slice là reverse-read và write/generate theo sau; README/source cần hòa giải | CLI/MCP engine, không server/UI/RBAC/approval. C; source trace trước POC |
| DBA Bridge | `AI2Innovate/dbabridge@f96b5159aa2bf20da8584cdefe5e7b33efd338ed` | Repo khai Apache-2.0; không có implementation/dependency/artifact audit | README tuyên bố Oracle→PostgreSQL audit/conversion nhưng binary coming soon | Watch-only; chưa POC |
| DBGit (`@lovelytoonz/dbgit`) | npm `@lovelytoonz/dbgit@0.1.0`, tarball SHA-256 trong manifest; không có Git SHA | MIT license text trong archive; dependency terms cần rà | Selected npm source có Oracle introspection/DDL, target-side `DBGIT_CHANGELOG`, local UI | C schema-as-code; source-level evidence, runtime NOT_RUN; không platform A |

## Source details

### SQLark

[Tài liệu Dameng](https://eco.dameng.com/document/dm/zh-cn/start/tool_SQLark.html) mô tả app desktop cho phát triển/quản trị, hỗ trợ DM/Oracle/MySQL/PostgreSQL trên Windows/Linux/macOS. Tài liệu liệt kê object Oracle như schema/table/view/materialized view/function/procedure/sequence/trigger/package/link/type; có SQL editor, migration theo task và đối chiếu object/table counts. Đây là Oracle object/migration evidence, không chỉ Oracle mode của engine khác.

[Bài V3.4](https://eco.dameng.com/community/article/20250416172509WCFJW2BK6TIFB6A0VO) ghi Oracle 11g trở lên. Bài Dameng về [resume Oracle→DM](https://eco.dameng.com/community/question/ea7f41d42df1034006c0a81cd932259c) mô tả checkpoint theo primary key/ROWID. Có cơ sở giữ nếu đích migration là DM. Chưa thấy nguồn nêu Oracle→PostgreSQL hoặc Oracle→Oracle release governance. Nguồn chính thức cho biết tải installer và bản miễn phí; chưa có source/OSS license, user/team matrix, cross-environment ledger, actor separation hay approval binding. Chỉ nhóm D/reference migration. Runtime chưa kiểm.

### DbGate

Repo pin có [`LICENSE`](https://github.com/dbgate/dbgate/blob/c6babf5933f9e9cd81c11bcf5889bdc54e35cb81/LICENSE) GPL-3.0. README mô tả Oracle, SQL editor, schema compare/sync và Docker/web mode. Oracle driver tạo connection bằng optional `oracledb`; thick mode có thể cần Oracle Instant Client. Điều này chứng minh source connector/client, chưa chứng minh native Oracle migration plan, approval, target ledger hoặc recovery.

Tài liệu [Community vs Team](https://docs.dbgate.io/dbgate/customization/env-variables/index.html) gọi Community là FOSS, cấu hình từ environment variables. Team Premium cần license và storage DB/admin UI, role assignment, persisted settings. [Team Premium](https://dbgate.io/editions/team-premium/) tuyên bố roles, permissions, audit logs và central server. Đây vẫn là client/workspace. Chưa thấy artifact-bound SQL promotion/approval. Repo release page ghi v7.3.1 ngày 2026-09-24. Oracle version/auth/TCPS cần POC riêng nếu cần client, nhưng không vào shortlist migration platform.

### DBHub

Pinned [`src/connectors/oracle/index.ts`](https://github.com/bytebase/dbhub/blob/4ddb26e73c5d8f1d54f5d04351c11c3caeb43cbb/src/connectors/oracle/index.ts) có Oracle DSN, pool `node-oracledb`, metadata, PL/SQL statement splitter, health check. Config example mô tả service name/SID, thin mode, SSL, `readonly`, `max_rows`. Đây là Oracle connector/truy vấn/metadata evidence, không schema migration, approval, project inventory, release lifecycle hoặc target ledger. DBHub là repo của Bytebase và là headless MCP server. Không phải lựa chọn độc lập hoặc performance platform. Repo license khai MIT; kiểm dependency nếu redistribute.

### Hue

Hue public source pin Apache-2.0. [User guide](https://github.com/cloudera/hue/blob/afa68e4008a550dfcef42c4a9b46d523396dd94c/docs/user-guide/user-guide.md) hướng dẫn editor và có mục Oracle. [`oracle_lib.py`](https://github.com/cloudera/hue/blob/afa68e4008a550dfcef42c4a9b46d523396dd94c/desktop/libs/librdbms/src/librdbms/server/oracle_lib.py) import `cx_Oracle`, kết nối và execute statement, đọc metadata. Đây là query adapter, không Oracle migration engine. Guide có execution logs nhưng không evidence project model, version ledger, artifact-bound approvals, promotion hoặc recovery. Hue là UI/query workbench gắn Hadoop ecosystem; không vào shortlist.

### Gudu SQLFlow và project tên trùng

`sqlparser/sqlflow_public` là repo docs/sample. [README](https://github.com/sqlparser/sqlflow_public/blob/067cbbe1bce1c02090d41db89f8e06715e3fa459/README.md) nói column-level lineage cho Oracle cùng nhiều vendor, thu SQL từ Git/local/query history, API/SDK và on-prem. [`LICENSE`](https://github.com/sqlparser/sqlflow_public/blob/067cbbe1bce1c02090d41db89f8e06715e3fa459/LICENSE) là Commercial License Agreement/EULA. Public repo không đồng nghĩa OSS. Product fit là lineage/impact analysis, không thi hành schema migration hoặc promotion theo evidence đã thấy.

Tên `SQLFlow` cũng thuộc `sql-machine-learning/sqlflow`, một compiler cho SQL+ML workflow/Kubernetes. README project đó liệt kê database khác, không nêu Oracle và không làm DB governance. Không gộp hai project.

### d-migrate

[README tại pin](https://github.com/pt9912/d-migrate/blob/cd2ad60b4b4ffdf3ef363a16ab5adfacf2b7c62a/README.md) mô tả công cụ MIT CLI/MCP: neutral schema YAML, validate/compare/generate/reverse/migrate/rollback, Oracle và bốn dialect, migration plan artifact và data transfer. Source tree có `driver-oracle`, `driver-oracle-profiling`, `test/integration-oracle`. [Module Gradle](https://github.com/pt9912/d-migrate/blob/cd2ad60b4b4ffdf3ef363a16ab5adfacf2b7c62a/adapters/driven/driver-oracle/build.gradle.kts) dùng `ojdbc11`. Module comment mô tả Oracle adapter ở slice reverse-read, write/generate sau này. Đây là lệch README/source cần giải quyết bằng code path review, không bằng giả định.

README ghi production version 1.7.1 ngày 2026-09-16 và Oracle integration suite. Đây là dấu hiệu maturity source, không là runtime PASS. Không chạy test. Oracle Free Use Terms cho ojdbc11 khác project MIT và điều kiện redistribution cần giữ. Không thấy multi-user inventory, approvals, RBAC, browser UI hoặc central target ledger. Cân nhắc engine POC chỉ nếu cần so sánh migration engine; trước đó trace object DDL, partial failure/checkpoint, state/logging và license image/driver.

### DBA Bridge

Pinned repo metadata khai Apache-2.0, nhưng tree chỉ có README/LICENSE/docs templates, không implementation, connector, dependency manifest hay release. [README](https://github.com/AI2Innovate/dbabridge/blob/f96b5159aa2bf20da8584cdefe5e7b33efd338ed/README.md) nói desktop binaries “coming soon”/early access và chia feature theo phase. Oracle→PostgreSQL assessment, PL/SQL rewrite và approvals là claim của README, chưa inspectable từ source. Repo license chưa xác lập dependency coverage hoặc executable artifact. Chỉ watch-list cho đến khi code/build phát hành.

### DBGit (`@lovelytoonz/dbgit`)

GitHub URL trong npm metadata (`junpisaanant/dbgit`) không mở được, nhưng npm public registry cung cấp gói `@lovelytoonz/dbgit@0.1.0`. Đã tải archive vào bộ nhớ, ghi SHA-256 toàn archive `af488e47df91b04717f4e0ac33a08681adaa8593e5002bd2b8f353b2d7860941`, liệt kê file và chỉ lưu các file text chọn lọc. Không cài package, chạy script hoặc execute code. `source-manifest.csv` ghi hash archive và hashes file đã lưu.

Selected package source có LICENSE MIT; `package.json` khai `oracledb`; `src/db.js` mở Oracle connection; `introspect.js` đọc schema; `sqlgen.js` sinh Oracle DDL; `engine.js` lập plan/deploy và ghi nhận chú thích Oracle DDL implicit commit/partial effects; `ledger.js` ghi `DBGIT_CHANGELOG` target-side; `src/ui/server.js` bind `127.0.0.1`. Đây là evidence tốt hơn npm README đơn thuần cho một công cụ Oracle schema-as-code.

Phân loại C, không platform A: bản 0.1.0 và một lần publish theo metadata; UI loopback/local, không central server, actor separation, RBAC hoặc approvals; ledger per target không là shared release control plane. Không cài/chạy nên behavior chưa được runtime xác minh. Git history/upstream identity và dependency license vẫn cần kiểm riêng. Đề xuất chỉ đưa vào engine comparison POC nếu cần schema-diff/deploy Oracle; trước đó trace supported objects, permission model, deploy failure/reconcile, Oracle version/driver terms và nguồn phát hành chính thức. Không còn gắn `SOURCE_GATE_BLOCKED` với việc thiếu Git repository; artifact public đã cho phép review source snapshot.

## Các lead đã loại qua primary-source spot check

- `OracleToGit`: realtime DDL export/backup; không approval/release orchestrator.
- `GreatSQL/gt-checksum`: Oracle và MySQL-family schema/data/object checksum/repair; không RBAC, UI/control plane hay staged release.
- `averemee-si/oracdc`: Oracle CDC to Kafka, commercial + AGPL dual license; không schema governance.
- Ora2Pg wrappers, migration examples và generic schema tools: engine/ETL, không platform.
- Oracle database operator, Google El Carro và OCI DevOps: provisioning/lifecycle hoặc CI/CD chung, không schema release governance.
- GitHub topic `database-version-control` có `dbvc-platform` cho SQL Server, không Oracle.
- DBTool/clients: Oracle access/UI không chứng minh migration gates/ledger.

## Gaps và điều kiện tiếp theo

Không kiểm binary/image/SBOM/driver artifacts, commercial entitlement/source, private repo hay target Oracle. Oracle version ngoài các tài liệu SQLark được dẫn chưa xác minh. Không đo performance. Source claims là mô tả tại pin và selected files, không phải complete audit hoặc runtime evidence.

Đề xuất: chỉ thêm d-migrate hoặc DBGit nếu nhóm muốn so sánh engine; giữ SQLark nếu migration target là Dameng; không ưu tiên Hue/DbGate/DBHub/SQLFlow cho control-plane POC. Không sửa shortlist hoặc criteria chung trong artifact worker này.


### Bani

Bani là engine ELT/migration đa hệ, không phải governance control plane. [Tài liệu Oracle connector](https://docs.bani.tools/en/latest/connectors/oracle/) mô tả Oracle 11g–23c, Thin mode từ 12c và Thick mode cần Instant Client cho 11g. Pinned source `mugumedavid/bani@c3c386a802668ae372a6ae500cf0d039b101d7af` có Oracle source/sink connector và pyproject ghi Apache-2.0, phiên bản 1.0.2, trạng thái Beta. [Web UI guide](https://docs.bani.tools/en/latest/guides/web-ui/) nói UI single-user, connection/project local, một migration mỗi lần; không có team RBAC, approval hay central release ledger. Có thể so sánh engine data-transfer/performance nếu cần, nhưng chỉ nhóm C/composition. License source vẫn cần kiểm dependency/image nếu phân phối. Runtime NOT_RUN.

### Adiom Dsync

Pinned `adiom-data/dsync@9c0e12db57fa10bd69220482b4ce151f7620eb30`. [Support matrix](https://docs.adiom.io/getting-started/what-is-supported) đưa Oracle vào SQLBatch connector ở Public Preview, Source only và query-based; [limitations](https://docs.adiom.io/basics/limitations) nói không replicate DDL/index. Vì vậy đây là CDC/data-copy, không Oracle schema migration hoặc governance. [Public preview announcement](https://adiom.io/post/new-sql-connectors-in-public-preview) cũng nêu edition/community model; docs quảng bá single binary AGPLv3 community và enterprise thương mại, nhưng root LICENSE không có tại source pin (raw endpoint 404). Cần xác minh quyền redistribution của đúng artifact trước POC. UI monitor không chứng minh approvals/RBAC. Nhóm C/data replication, runtime NOT_RUN.

### Liquibase Oracle demo

`liquibase/liquibase-Oracle-demo@6d8b60a3ea0de556ae08800dcf7f09bf23fb0079` chỉ là sample/repository demo, không phải sản phẩm candidate. README/pipeline thể hiện Oracle 11g+ changelog deployment với Liquibase Pro license key và Liquibase Flow; approval/workflow nằm ở Azure DevOps. License của sample chưa xác minh từ artifact snapshot chọn lọc. Dùng làm ví dụ composition cần entitlement, không lấy nó làm OSS platform hoặc bằng chứng miễn phí. Runtime NOT_RUN.

### Bani/Adiom/SQLark scope guard

Sự hiện diện của Oracle connector hoặc Web UI không đủ xếp platform A. SQLark có evidence migration Oracle→Dameng trên desktop, nhưng không source/license audit. Bani có source/sink chuyển dữ liệu nhưng UI single-user. Dsync chỉ Oracle source preview cho SQLBatch và không DDL. Không lead nào trong nhóm này chứng minh Oracle schema release, central approval, actor separation và target ledger cùng lúc.

## Artifact pin và provenance

`source-manifest.csv` liệt kê raw source URL cố định theo SHA, đường dẫn snapshot local, kích thước và SHA-256. Snapshot chỉ chọn các file tối thiểu hỗ trợ claim license/Oracle/scope; nó không phải full source archive, SBOM hoặc legal opinion. Pin cho Bani, Dsync và Liquibase demo lấy từ public `git ls-remote` HEAD khi thu thập; các pin còn lại lấy từ public repository metadata/API đã truy cập trong vòng nghiên cứu. Mỗi source link trong register trỏ đúng repo hoặc tài liệu. DBGit không có Git commit pin; registry artifact đã được pin bằng version và archive SHA-256, nhưng không gắn được với Git history upstream.
