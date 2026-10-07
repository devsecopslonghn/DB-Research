# T02 — kiểm nguồn phát hiện mới

Kiểm có chọn lọc tại 2026-10-04. Những dẫn chứng DOC và SOURCE không phải kết quả runtime. Tất cả RUNTIME đều ở trạng thái `NOT_RUN`.

## D-Band DRM — phát hiện trùng, giữ nguyên đánh giá hiện có

Kho mã này đã được ghi nhận trong `brief.md`, `LICENSE-AUDIT.md` và `evidence/source-references.json` với các mã DRM-L/DRM-LOCAL/DRM-FW. Đây không phải phát hiện mới và đã được bỏ khỏi danh sách ứng viên của thư mục này. Kết quả tìm mới chỉ xác nhận cùng dự án. Giữ đánh giá license/source hiện có làm nguồn chính; không coi lần kiểm tra bổ sung này là ứng viên mới hoặc lặp lại kết luận cũ.

## advisorTool (`tianyuso/advisorTool`)

**Phân loại:** B, thành phần quản trị/rà soát SQL được đóng gói thành CLI/thư viện. Đây không phải platform DB loại A hoặc migration engine.

- **DOC:** README tại [SHA `19a49a72c63f741cd8a655c27dc9cbf980a8634e`](https://github.com/tianyuso/advisorTool/blob/19a49a72c63f741cd8a655c27dc9cbf980a8634e/README.md#L196) mô tả đây là CLI độc lập dựa trên engine rà soát SQL của Bytebase. Dự án tuyên bố hỗ trợ Oracle và có “90+” quy tắc. Đây là tuyên bố trong tài liệu, chưa phải kết quả runtime.
- **SOURCE:** [`go.mod` lines 33–40](https://github.com/tianyuso/advisorTool/blob/19a49a72c63f741cd8a655c27dc9cbf980a8634e/go.mod#L33) khai báo phụ thuộc `github.com/bytebase/parser`; README lines 200–212 nêu parser Oracle là `github.com/bytebase/parser/plsql`. Điều này cho thấy dự án đóng gói quy trình quanh parser và advisor nguồn upstream. Nó không chứng minh parser Oracle hoặc bộ quy tắc được phát triển độc lập.
- **LICENSE:** GitHub khai báo GPL-3.0; [`LICENSE` tại SHA đã pin, dòng 1–2](https://github.com/tianyuso/advisorTool/blob/19a49a72c63f741cd8a655c27dc9cbf980a8634e/LICENSE#L1-L2) ghi GNU GPL phiên bản 3. Chưa audit cây dependency, ghi công/nguồn gốc phần code sao chép hoặc điều chỉnh, cũng như tương thích license của toàn bộ gói. README nói dự án giữ parser/quy tắc của Bytebase, nên cần làm rõ nguồn gốc trước khi phân phối lại.
- **LIMIT:** README lines 1901–1918 tự phân biệt CLI này với UI đầy đủ, cộng tác/RBAC, quy trình phê duyệt và quản lý phiên bản DB của Bytebase. SQL review không cung cấp inventory toàn hệ thống, phê duyệt gắn với artifact/target, đưa bản phát hành qua các môi trường, migration ledger tại target hoặc recovery.
- **ORACLE:** Chỉ có tuyên bố hỗ trợ parser. Chưa kiểm bằng chứng Oracle driver/runtime hoặc phiên bản đã thử. Không chạy SQL hay kết nối.
- **Kết luận:** giữ làm lead B phụ trợ để so sánh SQL lint, không đưa vào shortlist platform. Nếu cần, có thể nghiên cứu riêng độ bao phủ quy tắc của CLI. Đây là so sánh chức năng với engine của Bytebase, không phải so sánh giữa hai platform độc lập.

## AdminerEvo

**Phân loại:** D, client truy cập/giao diện quản lý DB có tuyên bố hỗ trợ Oracle; không phải platform governance hoặc release.

- **DOC/SOURCE:** [Repository nguồn upstream tại SHA đã pin](https://github.com/adminerevo/adminerevo/tree/d11a2e87cc0da5e631d442c4b59819f92117a733) đã lưu trữ và chỉ đọc từ 2025-01-24. [README tại cùng SHA](https://github.com/adminerevo/adminerevo/blob/d11a2e87cc0da5e631d442c4b59819f92117a733/README.md) nêu Apache-2.0 OR GPL-2.0-only và liệt kê Oracle trong danh sách DB hỗ trợ. Repository có các file license riêng: [`LICENSE.Apache-2.0`, dòng 2–3](https://github.com/adminerevo/adminerevo/blob/d11a2e87cc0da5e631d442c4b59819f92117a733/LICENSE.Apache-2.0#L2-L3) và [`LICENSE.GPL-2.0-only`, dòng 1–2](https://github.com/adminerevo/adminerevo/blob/d11a2e87cc0da5e631d442c4b59819f92117a733/LICENSE.GPL-2.0-only#L1-L2). Trước khi dùng lại thành phần nào, cần xác định license áp dụng cho thành phần đó.
- **LIMIT:** Chưa thấy bằng chứng về review/phê duyệt, đưa bản phát hành qua các môi trường, ledger target, định danh bản phát hành hoặc audit trung tâm. Tuyên bố hỗ trợ Oracle chung trong README không xác minh cơ chế connector, phiên bản DB, TCPS hoặc hành vi PL/SQL.
- **Kết luận:** loại khỏi shortlist platform. Chỉ xem như tham khảo client DB đã lưu trữ; sản phẩm không đáp ứng phạm vi platform gần Bytebase đã đóng băng.

## Actiontech SQLE — trùng với nghiên cứu hiện có

`actiontech/sqle` là sản phẩm quản trị SQL của Trung Quốc xuất hiện lại trong lượt tìm tập trung. Đây không phải ứng viên mới. Giữ nguyên nhận định source/license đã pin trong `PRODUCT-MODEL.md`, `PRODUCT-EVIDENCE.md` và `LICENSE-AUDIT.md`. Đánh giá hiện có đã tách sản phẩm quản trị SQL khỏi các giới hạn project/release của Community và ghi nhận quyền phân phối Oracle plugin chưa rõ. Lần tìm lại này không làm thay đổi nhận định. Mục này không thêm tuyên bố về source hoặc runtime mới.

## DataStar

**Phân loại:** D, sản phẩm thương mại gần quản lý thay đổi và phát hành DB.

- **DOC:** [Trang sản phẩm](https://www.datastar.software/) tuyên bố hỗ trợ Oracle/SQL Server, quản lý phiên bản thành phần, promotion giữa môi trường, truy vết từ yêu cầu thay đổi đến triển khai, audit và CI/CD. Đây là thông tin từ nhà cung cấp, chưa được xác minh.
- **DOC:** [Trang license](https://www.datastar.software/licensing) nêu thuê bao hằng năm theo số tài khoản developer. Giá tùy quy mô nhóm, nền tảng DB và cách dùng CI/CD. Đây không phải platform mã nguồn mở/miễn phí.
- **DOC:** [Hướng dẫn cài đặt](https://www.datastar.software/docs/getting-started/installation) nêu cần máy chủ license và có CLI `DataStar.Tools` cho CI/CD. Cơ chế Oracle, giới hạn phiên bản sản phẩm, phiên bản Oracle, sổ migration/khôi phục và quản trị qua API chưa được kiểm.
- **SOURCE:** Chưa xác định kho mã công khai. Tài liệu nhà cung cấp không được xem là bằng chứng source.
- **Kết luận:** giữ làm đối chứng thương mại có quy trình gần phạm vi nghiên cứu. Loại khỏi OSS shortlist. Trước khi đánh giá cần xác minh license theo module/seat/database, hoạt động offline, Oracle connector/phiên bản, nơi lưu dữ liệu, audit export và phạm vi trial.

## DBmaestro

**Phân loại:** D, platform thương mại cho DevSecOps và phát hành DB.

- **DOC:** [FAQ của DBmaestro](https://www.dbmaestro.com/faq/) mô tả tự động hóa phát hành, quản lý phiên bản, thực thi bảo mật, audit tuân thủ và phê duyệt; đồng thời liệt kê Oracle cùng các DB khác. FAQ nói “any other DB via JDBC”.
- **DOC:** [Trang sản phẩm](https://www.dbmaestro.com/) mô tả quy trình, phát hiện độ lệch, chạy thử và RBAC/audit. Đây là tuyên bố của nhà cung cấp, chưa xác minh theo phiên bản sản phẩm hoặc module.
- **SOURCE:** Chưa tìm thấy source hoặc văn bản license công khai để audit. Chưa rõ Oracle dùng kết nối native hay JDBC adapter. Cần nhà cung cấp xác nhận giá, tính năng theo license, phiên bản Oracle và cách triển khai tự lưu trữ.
- **Kết luận:** giữ làm đối chứng thương mại phù hợp, nhưng không đưa vào OSS shortlist. Chỉ tiếp tục tìm hiểu mua sắm nếu phạm vi quyết định cần đối chứng thương mại.

## Oracle Enterprise Manager Cloud Control 13.5

**Phân loại:** A/D, bộ quản lý lifecycle/vận hành DB dành riêng cho Oracle; gồm change management, so sánh/đồng bộ schema, quản trị estate và quản lý hiệu năng.

- **DOC:** [Hướng dẫn license Enterprise Database Management của Oracle 13.5](https://docs.oracle.com/en/enterprise-manager/cloud-control/enterprise-manager-cloud-control/13.5/oemli/enterprise-database-management.html) liệt kê `Legacy: Change Management Pack for Oracle Database` và nêu các management pack này chỉ mua được cùng Enterprise Edition.
- **DOC:** [Hướng dẫn Oracle 13.4](https://docs.oracle.com/en/enterprise-manager/cloud-control/enterprise-manager-cloud-control/13.4/oemli/enterprise-database-management.html) gắn Schema Comparison, Schema/Data Synchronization và Change Activity Plans với Database Lifecycle Management Pack. Đây là cổng license bắt buộc.
- **DOC:** Tài liệu Oracle tách Performance/Diagnostics/Tuning thành các pack riêng. Không suy ra các chức năng này miễn phí chỉ vì Enterprise Manager hiển thị menu hoặc endpoint. Cần đối chiếu từng chức năng với phiên bản và quyền license cụ thể.
- **SOURCE:** Không áp dụng vì sản phẩm là proprietary.
- **Giới hạn so với tiêu chí:** Đây là công cụ Oracle-native nên có thể phù hợp cho quản trị estate, lifecycle và hiệu năng Oracle. Nó không phải migration tool đa nền tảng hoặc platform không phụ thuộc DB như Bytebase. Hướng dẫn 13.5 đánh dấu Change Management là legacy. Không giả định tính năng sẵn có hoặc đã được cấp license trên target.
- **Kết luận:** giữ làm tài liệu tham chiếu cho quản trị/hiệu năng Oracle, không đưa vào OSS shortlist. Trước POC cần xác minh quyền license, build OEM, plugin và phiên bản target.

## dbward — kiểm tra trùng, không đăng ký lại

**Lý do ghi nhận:** đã phân tích trong `additional-candidates.md`; lần tìm độc lập này lại tìm thấy dự án.

- **SOURCE:** Repository tại [SHA `e73370b15b2fd81fdcd9e6f8fa97004f9fd2fc69`](https://github.com/dbward-dev/dbward/tree/e73370b15b2fd81fdcd9e6f8fa97004f9fd2fc69). `Cargo.toml` lines 21–26 khai báo Apache-2.0; [`Cargo.toml` dòng 35–36](https://github.com/dbward-dev/dbward/blob/e73370b15b2fd81fdcd9e6f8fa97004f9fd2fc69/Cargo.toml#L35) bật SQLx cho PostgreSQL/MySQL, không bật Oracle. README tại cùng SHA mô tả server-agent có phê duyệt/audit, nhưng cũng nêu target DB là PostgreSQL/MySQL ở [lines 227–228](https://github.com/dbward-dev/dbward/blob/e73370b15b2fd81fdcd9e6f8fa97004f9fd2fc69/README.md#L227).
- **DOC:** Phần license/free plan của README phân biệt Apache core với OIDC/group auth thương mại và nêu giới hạn free là 3 DB/20 user; xem [lines 613–620](https://github.com/dbward-dev/dbward/blob/e73370b15b2fd81fdcd9e6f8fa97004f9fd2fc69/README.md#L613).
- **Kết luận:** không hỗ trợ Oracle; đây là thành phần governance loại B, không phải platform/migration tool Oracle. Kết quả trùng với hồ sơ cũ. Không chạy runtime.

## Bằng chứng được giữ nguyên và trạng thái chạy

Hồ sơ này không sửa file POC hoặc bằng chứng cũ của Bytebase/ODC. Không triển khai, khởi động service, chạy test, SQL, benchmark hoặc kiểm tra target. Không đọc credential. Bằng chứng runtime Bytebase/ODC hiện có vẫn là lịch sử trên Oracle 26ai, không phải kết quả runtime của ứng viên mới.
