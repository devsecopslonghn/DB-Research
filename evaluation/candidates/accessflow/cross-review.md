# Review chéo CloudDM

Ngày: 2026-10-04. Kiểm tra các nhận định chính trong `evaluation/candidates/clouddm/source-review.md` và `report.md` theo source ghim `ClouGence/open-cdm@a9f16e78b8288c9a4158ee9df4378ee16b80021e`. Source chọn lọc có SHA-256 trong `evidence/additional-platform-20261004/clouddm-source-manifest.json`. Đây là review tĩnh; runtime vẫn `NOT_RUN`.

## Nhận định được source hỗ trợ

- **License repo — SOURCE:** README và `LICENSE.txt` ghim Apache-2.0. Điều này chỉ xác nhận license source được license bao phủ, không xác nhận image, plugin, dependency hoặc Oracle JDBC driver. Báo cáo chính xác khi giữ các phần đó thành license gates riêng.
- **TCPS connection path — SOURCE:** `OracleDsFactory.java:153-217` tạo URL theo SID/service/PDB/TNS và chọn `tcps` nếu property `oracle.net.authentication_services` có `TCPS`. Đây là bằng chứng về nhánh tạo URL, không chứng minh TLS handshake, wallet/truststore hay Autonomous Oracle hoạt động.
- **Approval ticket — SOURCE:** `ChangeActionForApproval.java:144-203` gắn ticket với datasource, target path, applicant, environment và file SQL dạng attachment bị khóa; tạo approval process. Đây là bằng chứng workflow/ticket. Chưa chứng minh requester không thể tự duyệt, content-target binding bất biến hoặc không có bypass.
- **Webhook validation — SOURCE:** `DmChangeFlowWebhookController.java:129-148` kiểm commit SHA và delivery ID có định dạng/độ dài hợp lệ rồi dựng `ChangeTriggerContext` và gọi trigger. `:105-126` kiểm flow, provider và đọc webhook event. Chỉ riêng đoạn này chưa chứng minh idempotency đã lưu bền, chống race hoặc chính xác một lần ở Oracle.
- **SQL artifact — SOURCE:** `ChangeSqlServiceImpl.java:32-74` đọc nội dung review vào cache file và dùng atomic move nếu filesystem hỗ trợ. Điều này bảo vệ bước chuẩn bị file. Nó không phải checksum được xác minh, ledger tại target, distributed lock hay recovery sau partial DDL.
- **CI dedup — DOC:** GitLab guide `docs/guides/gitlab-cicd.en.md:32-34` nói dùng commit SHA bất biến qua audit/download/execution và dedup theo webhook ID/idempotency key cùng flow + commit SHA. Source controller có kiểm ID nhưng các tệp source đã giữ không chứa lớp lưu/dedup đích. Vì vậy kết luận của báo cáo là phù hợp: dedup được mô tả và có kiểm tra đầu vào, chưa chứng minh chống chạy hai lần.
- **Oracle migration parser — GAP trong source chọn lọc:** `OracleDsFactory` chỉ là adapter kết nối; bằng chứng đã lưu không bao gồm parser/executor Oracle. Kết luận đúng là chưa biết PL/SQL, slash delimiter, `ALL_ERRORS`, implicit commit và replay. Ghi “chưa có bằng chứng” thay vì khẳng định không hỗ trợ.
- **Project/promotion — DOC/SOURCE:** README và các đường dẫn đã rà nói inventory/environment/cluster và flow target. Chúng chưa chứng minh invariant application/project và promotion có thứ tự DEV→SIT→UAT→PROD. Báo cáo giữ đây là gap là hợp lý.

## Điểm cần chỉnh/giữ điều kiện

- **License gate script:** manifest có `V202605070011__dm_license_support.java`, nhưng nội dung `collectScript()` chỉ đổi cột MySQL `rdp_auth_result_info.auth_result_status` (dòng 20-29). Tên file không đủ chứng minh entitlement enforcement hoặc cổng tính năng. Báo cáo chỉ nên nói kiểm tra logic entitlement còn cần làm, không xem tệp này là license gate đã xác nhận.
- **Plugin JDBC:** Oracle implementation nằm trong plugin riêng `clouddm-plugins/.../dsc-common-oracle/OracleDsFactory.java`, không phải bằng chứng custom JDBC adapter. Cần phân biệt: đây là plugin Oracle tích hợp của sản phẩm, còn chưa rõ plugin có đóng gói trong image/release được chọn, license của plugin/dependency và điều kiện runtime download. Không gộp với adapter do khách hàng tự viết.
- **Tình trạng giá/giới hạn:** nhận định báo cáo rằng giới hạn 10 instance/5 account còn chưa xác minh là đúng. Cache cũ không phải nguồn chính; pricing response trực tiếp đã lưu không xác nhận hợp đồng hiện tại hoặc không có entitlement gate.
- **Commit SHA/ID:** tài liệu CI nói SHA và dedup, controller kiểm đầu vào. Không nâng các nhận định DOC này lên SOURCE về đảm bảo artifact bất biến hoặc exactly-once.

## Kết luận review

Source review CloudDM thận trọng và giữ đúng ranh giới DOC/SOURCE/RUNTIME. Không tìm thấy mâu thuẫn P0 cần thay đổi kết luận. Giữ license/image/plugin/driver gate; giữ Oracle parser, ledger, replay, promotion và approval security là câu hỏi POC. Bổ sung phân biệt rõ plugin Oracle tích hợp với adapter tùy chỉnh và không suy entitlement từ tên migration script license-support. Runtime tiếp tục `NOT_RUN`.
