# Hướng dẫn operator

## Trước khi bắt đầu

1. Xác nhận PR đã merge, release ID đúng và bundle được tạo từ commit đã review. Live workflow chỉ dispatch từ `refs/heads/main`; protected environment `odc-demo` cần deployment branches và reviewers do authorized operator cấu hình.
2. Kiểm tra `release-envelope.json`: commit, manifest hash, SQL hash, policy, target và thứ tự `DEV → SIT → UAT → MOCKPROD`.
3. Xác nhận đúng các schema POC cô lập trên cùng Oracle database. `MOCKPROD` chỉ là schema mô phỏng.
4. OWNER và DBA xem SQL cùng các finding; approval diễn ra trong ODC. Operator dùng account được ủy quyền. Không có thao tác tự động nào phê duyệt hoặc thực thi thay con người.

## Tạo và theo dõi change

`db-validate` kiểm tra cả ba release và đóng gói fixture reports; PR cũng chạy `db-report` fixture smoke. Đây không phải runtime. Sau khi workflow có trên `main`, dispatch `db-release` với `release_id` và operation. `prepare` tạo bundle; `create_odc_change` tạo singleton batch; `collect_status` tự tải handoff artifact mới nhất chưa hết hạn, khớp đúng release và commit, không nhận ticket input. Local CLI `odc_client collect_status` nhận ticket ID số. ODC batch dùng `MULTIPLE_ASYNC`, thứ tự bốn stage, `ABORT`, retry 0.

Trong UI ODC, kiểm tra batch, target, SQL và hash trước approval. Logical stage map tới native environment `1/dev`, `2/sit`, `1000021/POCUAT`, `1000022/POCPROD`. Sau approval, operator tiếp tục thủ công ở DEV. ODC điều phối execution; verifier gửi SELECT-only checks qua ODC. Đọc native status, verification và receipt; chỉ sau khi OWNER/DBA đồng ý mới tiếp tục stage kế tiếp. `ABORT` không tự ngăn operator bấm tiếp; trong failure scenario, hủy batch còn chờ trước correction.

## Xác minh Oracle

Verifier chạy truy vấn chỉ đọc. Với mỗi target, xác nhận object theo manifest có trạng thái hợp lệ, không có compile errors, dữ liệu `DM_CP_CUSTOMER` có 3 dòng với 2 dòng active, và `DM_CP_LABEL('C0001')` trả giá trị mong đợi. Giữ receipt gắn với release, commit, ticket và stage. Nếu có bất kỳ mismatch nào, ghi nhận thất bại; native ODC success không thay thế các kiểm tra này.

Thu thập evidence bằng `collect_evidence`, sau đó dựng báo cáo với `generate_report`. Chọn source phù hợp: `LIVE` cho receipt runtime, `FIXTURE` cho fixture checked-in, `NOT_AVAILABLE` khi không có bằng chứng. Không gọi fixture là lần chạy ODC/Oracle thật. Mẫu nằm tại `reports/sample-migration-report.md`, `.json` và `reports/fixtures/`.

Payload bytes tái tạo được từ commit; actor/run ID có thể đổi mỗi lần build. Envelope `created_at` là timestamp commit, không đo thời lượng release. Native flow `createTime` cũng không phải lúc SQL bắt đầu. Audit có thể chỉ thấy actor trong phạm vi cá nhân; event tạo flow có thể không có task ID. Chỉ ghi actor/thời điểm khi receipt/audit chứng minh được.

## Dừng và báo cáo

Dừng rollout khi ODC báo lỗi, verification thất bại, receipt thiếu hoặc artifact không khớp hash. Nếu create lỗi/timeout, kiểm tra ODC để tìm ticket trước khi thử lại; không retry create mù. Cùng release ID không đảm bảo migration replay an toàn. Ghi riêng native status, stage, verification và source evidence; chuyển sang [failure and correction](failure-and-correction.md). Không sửa bundle để che trạng thái một phần.
