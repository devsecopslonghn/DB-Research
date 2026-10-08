# Thất bại và correction

## Kịch bản lỗi có kiểm soát

`REL-2026.10-DEMO02-FAIL` yêu cầu `REL-2026.10-DEMO01` và tạo `DM_CP_CUSTOMER_REGION_IX`. Ở DEV, block PL/SQL đi qua và index được tạo. Ở SIT, điều kiện schema cố ý gọi `RAISE_APPLICATION_ERROR(-20042, ...)` trước lệnh `CREATE INDEX`; ODC nhận lỗi và batch `ABORT` dừng tại SIT. UAT và MOCKPROD không được tự chạy tiếp. Index đã có ở DEV vẫn còn; đây không phải rollback.

```mermaid
sequenceDiagram
  participant ODC
  participant DEV as DEV schema
  participant SIT as SIT schema
  participant Human as OWNER / DBA / operator
  participant UAT
  participant MP as MOCKPROD
  ODC->>DEV: Execute FAIL release
  DEV-->>ODC: Success; region index created
  ODC->>SIT: Execute FAIL release
  SIT-->>ODC: ORA-20042 before CREATE INDEX
  ODC-->>Human: ABORT; batch stopped at SIT
  Note over Human,MP: No automatic rollback or progression to UAT/MOCKPROD
  Human->>Human: Review native result, partial DEV state, and correction
```

## Sửa bằng release mới

`REL-2026.10-DEMO02-FIX` là release riêng, khai báo `corrects: REL-2026.10-DEMO02-FAIL` và giữ dependency vào DEMO01. SQL đã review kiểm tra `USER_INDEXES`: nếu index đã tồn tại ở DEV, giữ nguyên; nếu chưa có ở SIT/UAT/MOCKPROD, tạo index. Kiểm tra này chỉ làm cho correction xử lý trạng thái một phần đã biết; nó không phải replay ledger tổng quát và không chứng minh an toàn cho thay đổi bất kỳ.

Operator và OWNER/DBA kiểm tra receipt lỗi, trạng thái từng schema, hash của correction và kế hoạch tiếp tục. Tạo batch correction mới qua ODC, approval trong UI, sau đó operator được ủy quyền tiếp tục thủ công từng stage và xác minh sau mỗi lần chạy. Không sửa SQL của release FAIL, không giả định rollback, không tự động promote hoặc replay.

Nếu create change gặp timeout/lỗi mơ hồ, trước hết tìm ticket trong ODC; không gửi lại POST mù vì request đầu có thể đã tạo ticket. Cùng release ID không cam kết SQL replay an toàn. Dùng correction đã review với ID, hash và receipt riêng.

Native MANUAL không phải policy cấm tuyệt đối mọi continuation sau failure: operator vẫn có thể chủ động bấm tiếp. Trong demo, giữ UAT/MOCKPROD ở `WAIT_FOR_EXECUTION`, đọc lỗi SIT và cancel batch FAIL trước khi tạo batch FIX. Không diễn giải `ABORT` thành một promotion gate mạnh hơn hành vi đã được chứng minh.

Native flow `createTime` là lúc tạo flow, không phải lúc SQL thật sự bắt đầu. Audit có thể giới hạn trong phạm vi cá nhân; event tạo flow có thể không có task ID. Giữ actor và execution time là `NOT_AVAILABLE` nếu receipt không chứng minh được.

Report phải giữ cả hai release và kết quả từng stage: DEV của FAIL thành công, SIT của FAIL thất bại, các stage chưa chạy, rồi trạng thái riêng của FIX. Chỉ ghi completion sau khi receipt Oracle xác nhận object, compilation, dữ liệu và function theo manifest. Nếu không có receipt, evidence source là `FIXTURE` hoặc `NOT_AVAILABLE`, không phải `LIVE`.
