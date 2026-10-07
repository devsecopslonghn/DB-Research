# Rà soát chéo: AccessFlow và Archery

Ngày rà soát: 2026-10-04. Đối chiếu report với source snapshot cục bộ ghi trong `evidence/source-manifest.json`. Không chạy test, build, service, SQL, deploy, dùng credential hoặc kết nối runtime.

## AccessFlow

**Chấp nhận — change governance native.** Phân biệt giữa schema change set/promotion native và công cụ migration database thông thường phù hợp source đã pin. `docs/20-schema-change-governance.md` mô tả change-set và promotion record. `DefaultSchemaChangePromotionService.java` tạo promotion metadata và liên kết request group (dòng 126–171). Deployment ladder kiểm tra các environment phía dưới đã có promotion `APPLIED` (dòng 258–279). Đây là bằng chứng governance P0 đáng kể, nhưng không chứng minh Oracle execution chạy đúng.

**Chấp nhận — statement gate không phải allow-list.** `SchemaChangeStatementGate.java` khai báo SELECT, INSERT, UPDATE và DELETE là nhóm statement bị chặn (dòng 29–47), rồi phân loại và xử lý statement đã parse (dòng 74–103, từ 126 trở đi). Report giữ đúng rủi ro rằng loại OTHER hoặc parser fallback có thể được nhận. Cần giữ kèm giới hạn parser và ví dụ trong tài liệu schema-change.

**Chấp nhận — checksum là metadata trung tâm, không phải target ledger.** `SchemaChangeChecksum.java` định nghĩa SHA-256 trên statement đã chuẩn hóa theo thứ tự (dòng 10 trở đi). `DefaultSchemaChangePromotionService.java` kiểm tra checksum change-set và lưu checksum trong promotion metadata (dòng 126–171). Điều này hỗ trợ identity artifact trong trạng thái platform. Thiết kế được rà chưa chứng minh Oracle history ở target hoặc replay an toàn. Report giữ đúng phân biệt này.

**Chấp nhận — ràng buộc approval plan.** `DefaultSchemaChangePromotionService.java` kiểm tra environment yêu cầu review có datasource human-review plan có thể enforce hay không (dòng 291–304). Đây là bằng chứng cho tình huống fail-closed đã mô tả. Source này chưa chứng minh requester/approver tách biệt hoặc hành vi runtime đầy đủ của external approval provider.

**Chấp nhận — gate license.** `LICENSE.md` khai báo Apache License 2.0. Oracle connector khai báo `ojdbc11`; `backend/pom.xml` và `connectors/README.md` mô tả cách phân giải driver và không đóng gói driver. Vì vậy license repository không giải quyết license Oracle driver tải riêng, image composition hoặc dependency gián tiếp. Report nêu đúng ranh giới này.

**Chưa rõ — phạm vi Oracle.** Oracle connector/catalog được tài liệu hỗ trợ, nhưng source được rà chưa chứng minh Autonomous TCPS, wallet setup hoặc tương thích với các Oracle version mục tiêu. Giới hạn PL/SQL parser được giữ đúng như gate POC. Không tính relational parser hoặc JDBC support là nghiệm thu SQL-01–12.

## Archery

**Chấp nhận — Oracle connection và client dependency.** `sql/engines/oracle.py` tại commit đã pin dùng `oracledb` và tạo DSN bằng SID/service name (dòng 19, 26–50). `requirements.txt:19` pin `oracledb`; `src/docker/setup.sh:26–34` tải Oracle Instant Client 19.21. Report xác định đúng việc rà license client/image riêng và không khẳng định TCPS hoặc wallet đã chạy thành công.

**Chấp nhận — commit từng statement và trạng thái partial.** `sql/engines/oracle.py` lặp qua các statement đã tách rồi gọi `conn.commit()` sau mỗi `cursor.execute()` thành công (dòng 1132–1152). Điều này hỗ trợ rủi ro partial release và liên quan trực tiếp REC-04/REC-05. Nó không chứng minh cách lưu trạng thái lỗi chính xác hoặc recovery.

**Chấp nhận — kiểm tra INVALID có giới hạn.** Oracle executor truy vấn `ALL_OBJECTS` cho named PL/SQL object và đánh dấu `INVALID` (dòng 1153–1187). Đây là bằng chứng source cho một dạng kiểm tra compile status. Nó không đọc `ALL_ERRORS`, không bao phủ anonymous block và không chứng minh stop behavior cấp release. Report mô tả đúng giới hạn.

**Chấp nhận — platform approval khác Oracle authorization.** `sql_api/api_workflow_operations.py` và `sql/utils/sql_review.py` kiểm soát workflow bằng Django permission và resource group. Oracle engine kết nối riêng bằng database credential đã cấu hình (`sql/engines/oracle.py:35–50`). Report yêu cầu xác minh độc lập quyền cross-schema và Oracle grants là đúng.

**Chấp nhận — phạm vi Apache-2 và dependency gate.** `LICENSE:1–5` chứa Apache License 2.0. Source pin Oracle Python client và script setup tải Instant Client; hai chi tiết này không xác nhận license của toàn image/dependency. Report giữ việc rà license ở trạng thái mở.

**Chưa rõ — parser.** `sql/utils/sql_utils.py` dùng `sqlparse.split` và có logic viết lại delimiter tùy chỉnh (dòng 123–145, 188–231). Oracle execution tiêu thụ danh sách statement đó. Đây là bằng chứng cụ thể về parser. Slash delimiter, SQL*Plus directive, package body, q-quoted string và các trường hợp PL/SQL khác vẫn cần runtime. Không nên mô tả parser là chỉ dùng generic splitter; có custom PLSQL handling, nhưng độ chính xác chưa được xác minh.

**Chưa rõ — ledger và promotion.** Report nói chưa thấy native target ledger hoặc environment promotion ladder trong workflow/engine path đã rà. Đây là cách diễn đạt phù hợp, có giới hạn phạm vi. Không mở rộng thành khẳng định tính năng không tồn tại ở mọi nơi trong Archery hoặc extension.

## Nội dung cần coordinator giữ chính xác

Không phát hiện claim P0 hoặc license nào cần sửa về mặt trọng yếu theo source snapshot đã pin. Giữ các cách diễn đạt sau trong phần tổng hợp:

- AccessFlow có checksum theo thứ tự và promotion state **ở metadata trung tâm**; target-side Oracle ledger/replay chưa được chứng minh.
- Schema-change gate AccessFlow chặn bốn nhóm DML đã parse, nhưng **không phải schema-only allow-list**.
- Archery commit statement thành công từng bước và có thể đánh dấu named PL/SQL object là INVALID. Điều này chưa chứng minh migration PL/SQL hoàn chỉnh hoặc diagnostic đầy đủ.
- Với cả hai nền tảng, dùng cụm **chưa có bằng chứng trong các path đã rà** khi nói về ledger hoặc promotion còn thiếu. Rà license release image, plugin, driver và dependency là các gate riêng.
- Source finding vẫn là DOC/SOURCE. Trạng thái runtime mọi tính năng vẫn **NOT_RUN**.
