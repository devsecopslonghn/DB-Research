# Nhật ký tìm kiếm T02

Ngày tìm: 2026-10-04. Phạm vi: ứng viên gần Bytebase về quản lý DB, migration Oracle, governance và performance. Criteria đã đóng băng trong `../../criteria.csv`. Đây là tìm kiếm nguồn công khai, không phải danh mục đầy đủ.

## Vòng 1 — repo và chủ đề

Truy vấn exact (web search, 2026-10-04):

- `GitHub database change management platform Oracle schema migration governance open source project`
- `GitHub Oracle database deployment platform approvals migration audit open source`
- `self hosted database management platform Oracle SQL review migration GitHub`
- `database migration release management Oracle open source alternative Bytebase`
- `site:github.com "Oracle" "database release" management CLI migration governance`
- `site:github.com/topics/database-devops Oracle release automation database change`

Kết quả đáng xem:

- `dband-drm/drm-cli`: trùng ứng viên D-Band DRM đã có trong `brief.md`, `LICENSE-AUDIT.md` và `evidence/source-references.json` (DRM-L/DRM-LOCAL/DRM-FW). Không đăng ký như discovery mới; tìm kiếm lần này chỉ xác nhận cùng project.
- `dbward-dev/dbward`: governance gateway Apache core, nhưng đã có trong `additional-candidates.md`; tái kiểm tra giới hạn Oracle, không tính là ứng viên mới.
- `ariga/atlas`, Liquibase, Flyway và các project CLI khác đã có trong nghiên cứu cũ; giữ làm migration engine/đối chứng, không đăng ký lại như platform mới.
- `oracle/oracle-database-operator` và `oracle-quickstart/expresslane` tập trung provision/lifecycle hoặc migration hạ tầng Oracle Cloud, không quản lý Oracle schema release; loại theo phạm vi chức năng.

Giới hạn: kết quả GitHub search phụ thuộc indexing/topic và mô tả README. Không suy ra tương thích Oracle hoặc license từ kết quả tìm kiếm.

## Vòng 2 — tài liệu chính thức, license và sản phẩm thương mại

Truy vấn exact (web search, 2026-10-04):

- `database release automation Oracle approvals audit platform official DBmaestro`
- `Oracle database change management platform CI CD approvals commercial official`
- `open source database governance approval platform Oracle SQL migration 2025 GitHub`
- `Oracle SQL deployment tool change control release management open source repo`
- `official Oracle Enterprise Manager Database Lifecycle Management Pack change management schema comparison licensing`
- `DataStar database change management Oracle license pricing release management official`

Kết quả:

- [DBmaestro](https://www.dbmaestro.com/faq/) công bố release automation, approvals, audit, Oracle và JDBC, nhưng là sản phẩm thương mại; không có public source/license để xác minh.
- [DataStar](https://www.datastar.software/) công bố Oracle/SQL Server, release promotion, audit và pipeline; [licensing](https://www.datastar.software/licensing) nêu subscription hàng năm theo developer seats. Cơ chế Oracle connector, edition limits và runtime chưa kiểm.
- [Oracle Enterprise Manager 13.5 licensing guide](https://docs.oracle.com/en/enterprise-manager/cloud-control/enterprise-manager-cloud-control/13.5/oemli/enterprise-database-management.html) ghi Change Management legacy và các management packs chỉ mua cùng Enterprise Edition. [13.4 guide](https://docs.oracle.com/en/enterprise-manager/cloud-control/enterprise-manager-cloud-control/13.4/oemli/enterprise-database-management.html) chỉ rõ Schema Comparison/Synchronization thuộc Database Lifecycle Management Pack.
- dbward được nhận diện lại. Source hiện tại cho thấy driver PostgreSQL/MySQL; đây không phải ứng viên Oracle.

Giới hạn: trang vendor là tuyên bố sản phẩm, chưa xác nhận độc lập. Không có quyền tải/kiểm image, binary hay private source. Tài liệu OEM nêu license gate, không xác minh entitlement của môi trường mục tiêu.

## Vòng 3 — focused search: GitLab, CNCF/catalogue, fork/dependency và SQL governance Trung Quốc

Truy vấn exact (web search, 2026-10-04):

- `site:gitlab.com Oracle database change management SQL review approval migration open source`
- `site:gitlab.com/groups database migration schema governance Oracle SQL review`
- `GitLab CI Oracle SQL deployment approval community project database release`
- `site:github.com/cncf "database migration" Oracle schema project`
- `site:github.com/awesome-selfhosted/awesome-selfhosted database management SQL Oracle migration`
- `site:github.com/topics/database-management Oracle SQL approval deployment Chinese`
- `开源 Oracle SQL 审核 平台 数据库变更 审批 SQL audit governance`
- `开源 数据库 DevOps Oracle SQL 工单 审核 平台 Github 国内`
- `开源 SQL审核 Oracle 数据库管理 平台 github 项目 审批 SQL 变更 (SQLE OR DMS OR Bytebase) -Archery -Yearning`
- `开源 Oracle SQL 审核 工单平台 GitHub 非 Archery 非 Yearning 非 SQLE`
- `Actiontech SQLE Oracle plugin forks SQL审核 数据库治理`
- `site:github.com/*/* fork Bytebase Oracle SQL audit approval governance`

Leads và quyết định:

- `tianyuso/advisorTool`: lead mới loại B, CLI rà soát SQL. Trang repository khai báo GPL-3.0 và nêu parser Oracle. [README tại SHA `19a49a72c63f741cd8a655c27dc9cbf980a8634e`](https://github.com/tianyuso/advisorTool/blob/19a49a72c63f741cd8a655c27dc9cbf980a8634e/README.md#L196) mô tả CLI dựa trên advisor của Bytebase và tuyên bố có “90+” quy tắc. [`go.mod` tại cùng SHA](https://github.com/tianyuso/advisorTool/blob/19a49a72c63f741cd8a655c27dc9cbf980a8634e/go.mod#L33) khai báo `github.com/bytebase/parser`; README lines 200–212 nêu package Oracle là `github.com/bytebase/parser/plsql`. Đây không phải platform độc lập hoặc migration runner. Chưa kiểm runtime hay độ chính xác của parser. README đề xuất dùng Bytebase cho workflow đầy đủ. Cần kiểm tra nguồn gốc dependency/code trước khi phân phối gói GPL.
- `AdminerEvo`: kết quả từ fork catalogue `u4078974/awesome-selfhosted` và kho mã nhánh upstream dẫn tới client web quản lý database trong một file. README liệt kê Oracle và Apache-2.0 OR GPL-2.0-only. Không xác nhận entry này trong catalogue nhánh upstream chính thức. Repository được archive ngày 2025-01-24; [repo nhánh upstream](https://github.com/adminerevo/adminerevo) ghi trạng thái này. Loại vì truy cập database/giao diện không chứng minh approval, đưa bản phát hành qua các môi trường hoặc target ledger. Nghiên cứu liên quan đã có các client như CloudBeaver/DBeaver.
- `actiontech/sqle`: kết quả về quản trị SQL của Trung Quốc; không phải phát hiện mới. Source đã pin và đánh giá trong `PRODUCT-MODEL.md`, `PRODUCT-EVIDENCE.md` và `LICENSE-AUDIT.md`. Kết quả tìm kiếm nêu lại Oracle support, nhưng giới hạn license/tính năng của Oracle plugin đã được ghi nhận; kết luận không đổi.
- Loại Archery/Yearning/Bytebase khỏi vòng này vì đã là seed. Kết quả về Bytebase fork `capsee123/bytebase555` không cho thấy fork được bảo trì độc lập hoặc khác nhánh upstream; không tạo ứng viên mới. `advisorTool` là wrapper/dùng lại dependency, không phải fork product.
- Truy vấn GitLab tìm thấy chức năng phê duyệt deployment ở gói Premium/Ultimate và quy trình review database nội bộ GitLab. Không tìm thấy platform governance DB Oracle. GitLab chỉ là nền CI/phê duyệt, vẫn cần ghép engine, inventory và state riêng; không đăng ký là DB platform.
- Truy vấn CNCF tìm thấy tài liệu về storage, operator và khái niệm di chuyển dữ liệu, nhưng không thấy project quản lý review/phát hành schema Oracle. Không coi Kubernetes database operator là SQL governance.
- Tìm kiếm catalogue tiếng Trung cũng cho thấy tài liệu về “SQL Quality Control Platform” của nhà cung cấp nhưng không xác định được tên sản phẩm/repository ổn định. PDF marketplace tuyên bố có quy trình phê duyệt/phát hành cho Oracle, nhưng source, chủ sở hữu, license, phiên bản sản phẩm và tình trạng hiện tại chưa rõ. Chưa đủ căn cứ đăng ký ứng viên. SQLE đã được ghi nhận ở mục trên.

Giới hạn vòng 3: chỉ mục tìm kiếm GitLab không đầy đủ; không có tìm kiếm group/project đã đăng nhập/xác thực. CNCF/awesome là danh mục, không xác nhận runtime hoặc bảo trì hiện tại. Chưa audit toàn bộ các fork của Bytebase. Tìm kiếm bằng tiếng Trung có thể bỏ sót bí danh hoặc thuật ngữ khác. Đã xem source gốc của advisorTool và AdminerEvo; nhận định SQLE dựa trên bằng chứng primary đã pin trước đó. Không chạy runtime.

## Quyết định phạm vi và điểm dừng

Sau vòng 2 và vòng focused 3, không có thêm ứng viên A OSS mới đủ căn cứ. Dừng ở đây theo quy tắc dừng hai vòng liên tiếp không tìm thấy A OSS phù hợp. Các lead B/C hoặc D mới được giữ trong danh mục với lý do giới hạn; đây không phải khẳng định đã bao phủ mọi tool tồn tại.

Không dùng runtime. Không triển khai, khởi động service, chạy test, SQL, benchmark, kiểm credential hoặc kiểm target Oracle. Không tải source snapshot về workspace; chỉ đọc có chọn lọc raw files tại SHA đã ghi trong `source-review.md`.
