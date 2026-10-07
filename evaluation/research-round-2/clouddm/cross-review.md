# Cross-review: AccessFlow và Archery source claims

Ngày rà soát: 2026-10-04. Chỉ đọc source snapshots đã pin trong `research-round-2/coordinator/source/` và review coordinator. Không sửa tiêu chí, chạy test hoặc thay runtime records.

## AccessFlow: BEGIN và PL/SQL semicolon

Nhận định source được hỗ trợ, với thuật ngữ chính xác hơn. `SchemaChangeStatementScanner.startsWithTransactionMarker` trả true cho bare `BEGIN` đầu tiên, trong khi Oracle anonymous PL/SQL block cũng bắt đầu bằng `BEGIN`. `SchemaChangeStatementGate.classify` gọi marker scanner trước parser. Vì vậy native change-set gate từ chối Oracle anonymous `BEGIN ... END;` do hình dạng đầu vào. Source comment nói chặn transaction envelope, nhưng scanner không thể phân biệt envelope đó với PL/SQL block.

Stored procedure/function/package/trigger bắt đầu bằng `CREATE`, nên không bị nhánh bare-BEGIN từ chối. Tuy nhiên scanner tìm dấu `;` ngoài literal/comment và trả true nếu còn token ngoài comment sau dấu đó. Dấu `;` nội bộ trước `END;` đáp ứng điều kiện. Gate từ chối trước SQL parser. Đây là source incompatibility cho procedural bodies có internal semicolon. Kết luận áp dụng native schema-change path đã đọc; không áp dụng tự động sang generic SQL executor.

Manifest [accessflow-release-comparison.json](../coordinator/accessflow-release-comparison.json) chỉ chứng minh các tệp được chọn tại commit `2ba5d322e7e1b4c750b5b0af85935e9ae814bd6a` byte-identical với source snapshot HEAD đã review (revision rút gọn `55c`, không gán thành release tag). Không có so sánh pin `v2.7.1`; không gán kết luận này cho tag đó. Phạm vi kết luận là tệp/path native schema-change đã review.

## Archery: package body compile check

Nhận định được ghi đúng là **inference**, chưa phải tái hiện. Query `ALL_OBJECTS` lọc `OWNER` và `OBJECT_NAME`, nhưng không lọc `OBJECT_TYPE`, không order, rồi lấy `fetchone()`. Oracle có thể có `PACKAGE` và `PACKAGE BODY` cùng owner/name với status khác nhau. Nếu fetch trả `PACKAGE VALID`, `PACKAGE BODY INVALID` có thể không được quan sát bởi nhánh hiện tại. Vì không có ORDER BY, source không cho biết hàng nào được trả trước. Vì vậy câu phù hợp là “có thể bỏ sót invalid package body”; không khẳng định sẽ bỏ sót.

Ca kiểm chứng cần tạo spec VALID/body INVALID và ghi từng hàng `ALL_OBJECTS` cùng terminal workflow result. Runtime **NOT_RUN**.

## Gợi ý sửa review chung

Giữ các kết luận là SOURCE, phân biệt native schema change khỏi generic query. Sửa mô tả BEGIN thành “scanner từ chối mọi script bắt đầu bằng bare BEGIN, gồm anonymous PL/SQL”. Giữ Archery package-body case là inference có điều kiện, không nâng thành fact/runtime failure.
