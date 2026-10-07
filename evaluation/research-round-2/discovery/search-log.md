# Nhật ký mở rộng tìm kiếm T02

Ngày chốt: 2026-10-04. Phạm vi: tìm rộng công khai sản phẩm gần Bytebase về quản lý DB, migration Oracle, governance và hiệu năng. Criteria không thay đổi. Mọi kết luận về khả năng là từ tài liệu hoặc source; runtime `NOT_RUN`.

## Dedup và phương pháp

Đối chiếu 36 dòng sản phẩm/fork trong `../../candidates.csv`, `../../shortlist.md` và `../../candidates/discovery/search-log.md`. Các tên Bytebase, ODC, SQLE, Archery, AccessFlow, CloudDM, D-Band DRM, dbward, Atlas, Liquibase, Flyway, các fork Bytebase, DataStar, DBmaestro, OEM, advisorTool và AdminerEvo đã có hồ sơ được ghi lại làm seed hoặc kết quả trùng. Không đăng ký lại các mục đó.

Đã rà repository search/topic/catalogue, trang GitHub/GitLab/Gitee công khai, tài liệu sản phẩm và source tại commit cố định cho lead có triển vọng. GitHub API công khai được dùng để lấy default branch, trạng thái archive, SPDX metadata, ngày push và commit SHA trước khi giới hạn rà source. Không clone, build, chạy test hay tải image. Đã gặp rate limit GitHub API ở bước cuối; các SHA trước đó vẫn truy cập raw source thành công.

## Vòng 4 — lead cụ thể và sản phẩm Trung Quốc

Truy vấn chính:

- `GitHub SQLark database governance Oracle migration release management SQL approval`
- `GitHub SQLFlow Oracle database change management governance SQL release`
- `GitHub Hue Oracle database SQL editor query governance project Oracle support`
- `GitHub dbgate Oracle database management SQL editor Oracle support`
- `GitHub dbhub Oracle database governance migration approval project`
- `"SQLark" database platform github`; `"SQLark" SQL governance database`
- `开源 Oracle SQL 审核 平台 数据库变更 审批 SQL audit governance`
- `开源 数据库 DevOps Oracle SQL 工单 审核 平台 Github 国内`
- `达梦 SQLark 官网 Oracle 数据库 支持 SQLArk`; `SQLark V3.2 官方 达梦`

Kết quả và quyết định:

- **SQLark (达梦 SQLark 百灵连接)**: tìm được tài liệu chính thức Dameng. Tài liệu gọi đây là ứng dụng desktop phát triển/quản trị DB, hỗ trợ kết nối DM/Oracle/MySQL/PostgreSQL, quản lý object, chỉnh sửa SQL, data/schema migration có task và validation. Bài của Dameng nêu Oracle 11g trở lên ở V3.4 và hướng dẫn Oracle→DM có resume. Đây là migration workbench hữu ích nếu đích là DM; không có bằng chứng về central server, release ledger xuyên môi trường, approval binding, RBAC hoặc source/license OSS. Trang chính thức cung cấp installer “free”, nhưng không suy ra tự do phân phối/kiểm toán source. Ghi vào register nhóm D, không là ứng viên OSS A. Nguồn: [tài liệu SQLark chính thức](https://eco.dameng.com/document/dm/zh-cn/start/tool_SQLark.html), [bài Dameng về V3.4 và ma trận DB](https://eco.dameng.com/community/article/20250416172509WCFJW2BK6TIFB6A0VO), [bài Dameng về Oracle→DM resume](https://eco.dameng.com/community/question/ea7f41d42df1034006c0a81cd932259c).
- **DbGate**: source GPL-3.0, hoạt động gần đây. README có Oracle, editor, import/export và compare/synchronize schema. Oracle plugin là package riêng, dùng `oracledb` tùy chọn; code có thin mode mặc định và thick mode qua Instant Client. Tài liệu chính thức phân biệt Community FOSS với Team Premium; storage/admin UI và team role assignment thuộc Premium. Đây là DB client, không có evidence về approval/release ledger native. Ghi D/client reference; Oracle connection/schema tooling không tự thành Oracle migration governance.
- **DBHub**: source MIT và owner là Bytebase. Source có Oracle connector dựa trên `node-oracledb` Thin mode, parser DSN, SQL tool, read-only/row-limit controls, Oracle health checks/EXPLAIN opt-in. Là MCP server/headless tool, không database control plane/UI/approval/release ledger, và không phải đối thủ độc lập của Bytebase. Ghi D/component reference, không tính A.
- **Hue**: Cloudera Hue là web SQL editor/notebook. Tài liệu người dùng có mục Oracle; source Oracle adapter import `cx_Oracle` và thực thi SQL. Repo Apache-2.0. Oracle support phụ thuộc driver, không có Oracle migration workflow, ticket promotion hay ledger chứng minh được. Ghi D/query UI reference.
- **SQLFlow by Gudu**: phân biệt với project `sql-machine-learning/sqlflow` (compiler SQL/ML; README không liệt kê Oracle và không liên quan governance DB). Gudu repo `sqlparser/sqlflow_public` chứa tài liệu/sample chứ không phải implementation chính; README quảng bá Oracle lineage, SQL collection, on-prem/API. Tại pin kiểm tra, `LICENSE` là Commercial License Agreement/EULA, không phải OSS license. Có thể hữu ích cho lineage/impact analysis, nhưng không migration release platform. Ghi D/commercial component.
- **No A mới** trong các lead trên. Các tuyên bố support được ghi đúng phạm vi: SQLFlow là lineage/parser; Hue/DbGate/DBHub là kết nối, truy vấn hoặc client; SQLark là desktop migration về DM. Không suy từ Oracle connection ra Oracle migration support.

## Vòng 5 — registry, migration source và Git hosts

Truy vấn chính:

- `GitHub Oracle database migration approval change management release open source`
- `Oracle schema migration platform approval audit database release GitHub`
- `open source database schema migration tool Oracle approval workflow web UI`
- `site:github.com/topics/database-devops Oracle governance database change platform`
- `site:github.com/topics/database-management Oracle approval SQL migration`
- `site:github.com/awesome-selfhosted/awesome-selfhosted Oracle database administration migration`
- `site:github.com/awesome-foss/awesome-sysadmin database change management Oracle migration`
- `site:gitlab.com/explore/projects Oracle SQL migration approval database platform`
- `site:gitee.com Oracle database change approval release platform OSS`; `开源 Oracle 数据库 Schema 变更管理平台 审计 审批 GitHub`
- `GitHub Oracle database version control GUI open source schema deployment tool dbgit`

Kết quả và quyết định:

- GitHub topic pages cho `oracle`, `database-management`, `database-administration`, `database-version-control`, `data-governance`, `schema-migration`, `database-migrations` và `ora2pg` đưa ra nhiều client, migration engines, operators, catalog/data-governance projects. Không có A OSS Oracle workflow mới trong kết quả đã rà. El Carro và Oracle database operator quản lý provisioning/lifecycle, không quản lý schema release. `dbvc-platform` chỉ SQL Server. Các project data-governance/catalog không phải DB change control.
- Awesome-Sysadmin dẫn về Database Management; Awesome-Schema-Migration-Platform phân biệt engine/building-block với platform governance. D-migrate xuất hiện từ lead catalog/search: source MIT, nhiều Oracle schema/data operations, nhưng là CLI/MCP không phải central platform. Ghi C/engine; xem source details tại `source-review.md`.
- **d-migrate**: tại SHA `cd2ad60b4b4ffdf3ef363a16ab5adfacf2b7c62a`, README mô tả schema model, diff migration, rollback, data transfer, signed plan artifacts, Oracle support và MCP/CLI; source có Oracle JDBC module và Oracle integration test module. `ojdbc11` là Oracle Free Use Terms, không MIT; module comment nói phải mang theo license text nếu redistrib driver. Oracle adapter module comment mô tả lát cắt reverse-read và các phần write/generate theo lát tiếp theo, trong khi README nói Oracle thuộc các thao tác schema hiện hành. Đây là mâu thuẫn/độ lệch cần POC source trace trước khi phụ thuộc vào Oracle DDL. Không có central Web UI, approval/RBAC workflow hoặc shared target ledger được chứng minh. Ghi C, ứng viên engine phụ trợ đáng xem, không thay Bytebase.
- **DBGit (`junpisaanant/dbgit`)**: upstream Git URL trong metadata không mở được, nhưng npm public registry cung cấp `@lovelytoonz/dbgit@0.1.0`. Đã đọc selected files trong tarball tĩnh, không cài/chạy. Archive SHA-256 và file hashes ở source-manifest. LICENSE text là MIT; source thể hiện Oracle introspection, DDL generator/deploy, `DBGIT_CHANGELOG` per-target và UI loopback. Ghi C schema-as-code, không platform A: không central server/RBAC/approval, early version; Oracle driver/dependency terms và runtime chưa kiểm.
- **DBA Bridge**: public GitHub repo Apache-2.0 nhưng pinned tree chỉ có README/LICENSE/docs templates, không có implementation/source connector hoặc release artifact. README tự ghi binary “coming soon”, waitlist, và các feature migration/approval là kế hoạch sản phẩm. Ghi C/watch-only, chưa ứng viên thực thi.
- GitLab public topic result chủ yếu là scripts/CDC; không phát hiện platform Oracle governance. Gitee search nổi CloudDM/SQLE đã có, cùng catalogue PDF sản phẩm “SQL quality control” không có tên vendor/repo/source/license pin; không đăng ký mục mơ hồ mới.
- Các lead `OracleToGit`, `gt-checksum`, `oracdc`, Ora2Pg wrappers, migration examples, Oracle operators, Scriptella và CLI/schema tools chỉ giải quyết export, checksum, CDC, provisioning, migration hay engine; loại khỏi platform shortlist. Giữ các tên đáng theo dõi trong `source-review.md` nếu có relevance.

## Vòng 6 — lead từ điều phối và project scope rộng

Đầu mối được kiểm thêm: `bani.tools`/docs, Adiom Dsync, Liquibase Oracle demo, cùng các truy vấn SQLark, SQLFlow, DBA governance/workflow, Oracle JDBC + approval/release. Truy cập raw GitHub ở SHA công khai với các file README/LICENSE/connector/build descriptors đã chọn. Bani có Apache-2.0 source Beta, connector Oracle source/sink, nhưng UI local single-user và không release governance. Dsync có Oracle SQLBatch source-only public preview, không DDL/index; docs nêu community AGPLv3 nhưng LICENSE thiếu tại pin nên redistribution gate còn mở. Liquibase Oracle demo là sample yêu cầu Pro/Flow và Azure DevOps approval, không platform OSS. SQLark được chốt bằng trang SQLArk Dameng và bài V3.4 chính thức, bỏ link MODB không xác minh tác giả; là desktop Oracle→DM migration, không source/license OSS. SQLFlow Gudu là commercial EULA/docs, không release. DBA Bridge chưa có implementation. Các mục được đăng ký dedup trong CSV với role C/D/reference; không có A mới đủ căn cứ.

Kênh đã rà gồm GitHub repository/topic/catalog search, GitLab public project/topic discovery, Gitee public search với truy vấn Hoa ngữ, Codeberg lead/search discovery, awesome catalogs, upstream docs/source, package metadata. GitHub API bị rate-limit ở giai đoạn sau; vì vậy dùng commit pins đã thu được và raw immutable URLs. Các kênh công khai không chứng minh coverage toàn bộ private projects hay mọi forge mirror. Vòng 6 chỉ kiểm lead có hướng cụ thể và nguồn primary, không diễn giải thành exhaustiveness.

## Đánh giá điểm dừng tìm kiếm

Đã chạy ba vòng mở rộng sau log cũ: (4) lead cụ thể và tiếng Trung; (5) topics/catalogs/hosted repos và source migration/control-plane; (6) Bani/Dsync/Liquibase cùng các nhánh governance/SQLark/SQLFlow. Vòng cuối bổ sung Bani, Dsync và Liquibase sample, nhưng chỉ là engine/data movement/sample. Không có A độc lập đủ evidence tối thiểu. Vòng bổ sung sau lead đã biết không tìm ra A mới; dừng vì các kênh chính đã có log, không vì đã đủ shortlist.

Không tuyên bố tìm hết mọi dự án tồn tại. GitHub API bị rate limit sau khi lấy metadata cho các repo chính; GitLab/Gitee search index công khai và awesome catalogs không đầy đủ, không truy cập nhóm private. Codeberg chưa có lead đủ mạnh từ kết quả tìm kiếm; chưa có authenticated instance/project search. Không có bằng chứng cho rằng đã duyệt toàn bộ project/fork hoặc mirror trên các forge. Không tải binary/image; đã lấy npm DBGit tarball vào memory để liệt kê và trích các file text chọn lọc, không install hoặc execute; không liên hệ vendor. Oracle source claim khác Oracle runtime. Mọi runtime trong vòng này là `NOT_RUN`.
