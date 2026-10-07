# Kết quả ODC Oracle POC qua API và UI

ODC chạy được SQL và PL/SQL trên Oracle lab. Cấu hình hiện tại chưa đủ để dùng làm migration engine CI/CD đáng tin cậy.

Ngày 04/10/2026: 12 PASS, 20 PARTIAL, 5 FAIL, 8 NOT_RUN trong 45 tiêu chí gốc. Các ca chưa chạy giữ NOT_RUN.

## Phạm vi và topology

- ODC 4.4.1-20260116 và OceanBase CE 4.3.5 làm MetaDB, do Argo CD quản lý.
- PVC ODC 5 GiB và MetaDB 10 GiB giữ nguyên UID. Pod ODC/MetaDB đã thay trong các lần sửa vận hành.
- Oracle thực tế là 26ai Enterprise Edition 23.26.4.1.0, AL32UTF8 / AL16UTF16. Chưa chứng nhận Oracle 19c/21c.
- Schema DEV/SIT/UAT/MOCKPROD có quota 50 MiB DATA. Observer chỉ CREATE SESSION và SELECT trên POC_ORDERS.
- Không cấp DBA/ANY cho schema POC. ADMIN chỉ bootstrap và đọc hậu kiểm POC.
- Schema trên cùng một database mô phỏng môi trường. Chưa chứng minh cách ly instance/mạng.

## Kết quả quan trọng

| Kiểm tra | Kết quả | Bằng chứng |
|---|---|---|
| Procedure, function, package, trigger, anonymous block, slash và Oracle literals | PASS cú pháp theo từng tiêu chí | Ticket 1000006–1000010 và Oracle hậu kiểm |
| Procedure lỗi biên dịch | FAIL | Ticket 1000011 thành công nhưng object INVALID, PLS-00201 |
| Phê duyệt mock PROD | OWNER và DBA duyệt qua UI | Ticket 1000023 và node actors |
| Tách requester khỏi executor | FAIL | Requester Execute sau duyệt trả 200 |
| Replay và checksum | FAIL tiêu chí migration | Ticket 1000024 chạy lại INSERT; SQL thay đổi vẫn được submit |
| Request API trùng | FAIL | Ticket 1000026/1000027, marker count=2 |
| Participant | QUERY cho đọc, CHANGE bị chặn, revoke lại 403 | API permissions và native Oracle denied UPDATE |
| Promotion | PARTIAL | Cùng artifact/hash và marker trên bốn schema; runner tự điều khiển thứ tự |
| UI ghi và đọc | Đã thực thi thật | UI tạo ticket 1000017, Execute, INSERT/COMMIT/SELECT REAL_UI_SELENIUM |

## API và UI đã dùng

API: RSA login → datasource/database inventory → POST flowInstances → approval → Execute → poll detail/result → Oracle postcheck.
Runner dùng tài khoản ODC riêng. CI job reference hiện là chuỗi do runner cục bộ gửi; chưa có GitLab/Jenkins runner.
CLI kiểm SHA-256 ở phía client trước approve/execute. Đây không phải checksum enforcement của ODC.

UI: Selenium W3C với Chromium container đã đăng nhập, tạo ticket, thực thi, duyệt OWNER/DBA và chạy SQL Window.
Ảnh SQL Window dùng element screenshot để không công bố danh sách schema khác trong sidebar.
Ảnh và result đều có SHA-256. Ảnh không thay thế Oracle hậu kiểm.

## Lỗi vận hành và cách xử lý

1. MetaDB bị Evicted vì diagnostic log vượt emptyDir 512 MiB. PR #34 tăng 2 GiB và dùng WARN/rotation.
2. Executor ticket dùng TCP dù console TCPS đã hoạt động. PR #35 thêm fallback TCPS chỉ cho host Autonomous đã cấu hình.
3. Khi mở nhiều console, listener trả ORA-12523. Có 17 session DEV không hoạt động trong lần quan sát.
   Đã đóng session POC và restart ODC sau khi các ticket kết thúc. UI/SQL chạy lại thành công.
   Always Free có giới hạn session theo tài liệu Oracle; đây là nguyên nhân khả nghi, chưa phải đo chứng minh chạm quota.
4. Quyền ODC được chuẩn hóa đến cuối ngày: expireTime gửi +45 giây trở thành cuối ngày phía server.
   Không kết luận lỗi expiry từ việc còn đọc được trong ngày. Revoke đã được kiểm chứng; boundary expiry chưa chạy.
5. Log task cũ trả “read log failed” sau restart; tải attachment của bốn ticket cũ cũng trả HTTP 500. Cần xuất log vào nơi lưu bền trước khi dùng production.

Nguồn giới hạn session: [Oracle Always Free](https://docs.oracle.com/en/cloud/paas/autonomous-database/serverless/adbsb/autonomous-always-free.html).
Nguồn expiry: `DatabasePermissionService.java`, dòng 178–179 trong source ODC đã pin của hồ sơ nghiên cứu.

## Bảng kết quả

| ID | Trạng thái | Kết quả và giới hạn |
|---|---|---|
| MODEL-01 | PASS | Project odc-oracle-poc id=1 có datasource/schema ID ổn định; bootstrap ADMIN ở project riêng id=2. |
| MODEL-02 | PASS | API đăng ký năm datasource POC. DEV/SIT/UAT/mock PROD và observer có schema, service và environment. Chỉ một Oracle instance. |
| MODEL-03 | PARTIAL | Ticket có ID và SQL. Runner lưu SHA-256/job reference. Chưa có immutable release hay checksum do ODC bắt buộc. |
| MODEL-04 | PARTIAL | Có requester, hai approver và timestamp. Service task operator có thể là creator; cần đối chiếu audit để xác định caller Execute. |
| MODEL-05 | PASS | UI hiển thị đúng CREATE POC_GOV_MANUAL và target MOCKPROD trước khi OWNER/DBA duyệt; CLI đối chiếu SHA-256. |
| MODEL-06 | PARTIAL | Ticket thủ công giữ SQL/target; PUT trực tiếp không có route cập nhật. Chưa kiểm mọi đường thay artifact hoặc target set sau duyệt. |
| MODEL-07 | PARTIAL | Bốn ticket DEV→SIT→UAT→MOCKPROD dùng cùng byte SQL và SHA-256. Thứ tự do runner điều khiển; chưa kiểm ordered batch native. |
| MODEL-08 | PASS | MANUAL dừng WAIT_FOR_EXECUTION. UI/API phải thực hiện Execute sau phê duyệt. Requester vẫn được thực thi sau duyệt. |
| MODEL-09 | PARTIAL | ABORT dừng sau lỗi bảng thiếu; dòng 1101 không được chèn. Chưa xác nhận stop policy giữa các stage của batch. |
| MODEL-10 | PARTIAL | Có ticket history/result và 97 audit record POC theo actor/action/time. Một số task log không còn đọc được sau restart ODC; chưa nghiệm thu retention. |
| MODEL-11 | PARTIAL | Outsider và Participant thiếu grant nhận 403. QUERY grant cho phép đọc; CHANGE bị chặn. Revoke lại nhận 403. Expiry được làm tròn cuối ngày nên chưa thử boundary. |
| MODEL-12 | PASS | Đã xác định thiếu target migration ledger, checksum enforcement, idempotency theo job reference và instrumentation recovery. Đây là kiểm kê gap, không phải production readiness. |
| SQL-01 | PARTIAL | Object/constraint và ticket thành công. USER_TABLES không có migration ledger; chưa có version order tại target. |
| SQL-02 | PARTIAL | Object/constraint và ticket thành công. USER_TABLES không có migration ledger; chưa có version order tại target. |
| SQL-03 | PARTIAL | INSERT/UPDATE đúng dữ liệu. Replay không được skip theo version và gặp ORA-00001; chưa đạt migration exactly-once. |
| SQL-04 | PASS | Procedure VALID; gọi procedure đổi STATUS=PAID. |
| SQL-05 | PASS | Function VALID; POC_ADD_TAX(100)=110. |
| SQL-06 | PASS | Package/spec/body VALID; initialization=42 và SET_NOTE thành công. |
| SQL-07 | PASS | Trigger VALID; UPDATE 150→200 tạo đúng một audit row. |
| SQL-08 | PASS | BEGIN và DECLARE chạy một lần, tạo đúng hai dòng 801/802. |
| SQL-09 | PASS | PL/SQL với slash riêng dòng thành công; function 10/2=5. |
| SQL-10 | PARTIAL | Ticket SQLPlus directive thất bại; marker 1001=0. Chưa kiểm từng directive riêng hoặc native SQLPlus path. |
| SQL-11 | FAIL | Ticket 1000011 EXECUTION_SUCCEEDED, successCount=1. Oracle POC_INVALID_PROC vẫn INVALID với PLS-00201 và Statement ignored. |
| SQL-12 | PASS | q-quote, comment trong literal, quoted identifier và nested block giữ đúng ba dòng. |
| REC-01 | PARTIAL | Ticket 1000012 EXECUTION_FAILED; ABORT không chèn dòng 1101. Log cũ không còn đọc được sau restart; exact error cần attachment. |
| REC-02 | FAIL | Replay SQL-03 tạo ticket 1000024 và chạy SQL lại; ORA-00001. Không có skip theo migration version. |
| REC-03 | PARTIAL | Hậu kiểm sau REC01 rồi tạo ticket sửa 1000025 chỉ chèn dòng 1101. Đây là recovery quyết định bởi operator, chưa có target-ledger reconciliation. |
| REC-04 | PARTIAL | CREATE POC_PARTIAL đã commit; ALTER thất bại và ticket báo EXECUTION_FAILED. Chưa có cơ chế target ledger khóa replay tự động. |
| REC-05 | NOT_RUN | Cần instrumentation commit checkpoint, network proxy hoặc topology/backup riêng. Không gây crash/mạng/restore trong lần POC này. |
| REC-06 | NOT_RUN | Cần instrumentation commit checkpoint, network proxy hoặc topology/backup riêng. Không gây crash/mạng/restore trong lần POC này. |
| REC-07 | NOT_RUN | Cần instrumentation commit checkpoint, network proxy hoặc topology/backup riêng. Không gây crash/mạng/restore trong lần POC này. |
| REC-08 | FAIL | Đổi SQL-01 nhưng giữ case ID vẫn tạo ticket mới 1000015. ODC không chặn checksum trước thực thi; không có migration version identity. |
| REC-09 | PARTIAL | Hai ticket cùng target được gửi Execute đồng thời và đều thành công. Chưa instrument lock owner/commit boundary để nghiệm thu serialization. |
| REC-10 | FAIL | Hai POST tạo ticket cùng artifact/job reference tạo ID 1000026/1000027 và hai marker rows. Gọi Execute lại ticket hoàn tất bị từ chối; không thay thế request-level dedup. |
| REC-11 | NOT_RUN | Cần instrumentation commit checkpoint, network proxy hoặc topology/backup riêng. Không gây crash/mạng/restore trong lần POC này. |
| REC-12 | NOT_RUN | Cần instrumentation commit checkpoint, network proxy hoặc topology/backup riêng. Không gây crash/mạng/restore trong lần POC này. |
| GOV-01 | PARTIAL | Có ticket, artifact SHA, target, actor, time và local job reference. Cần join audit và file evidence; chưa có một truy vấn release chuẩn. |
| GOV-02 | PARTIAL | Luồng phê duyệt trên ticket đã quan sát. Chưa kiểm toàn bộ thay SQL/target/environment/version và invalidation sau duyệt. |
| GOV-03 | FAIL | Rule POCPROD yêu cầu OWNER→DBA. Requester bị chặn trước duyệt nhưng POST Execute sau duyệt trả 200 và chạy thành công. |
| GOV-04 | PARTIAL | Cùng SHA-256 và marker trên bốn schema. Runner giữ thứ tự; chưa có immutable promotion enforcement ở ODC. |
| GOV-05 | NOT_RUN | Chỉ chạy API/CLI cục bộ với job reference. Chưa có runner GitLab/Jenkins và named CI service principal thực tế. |
| GOV-06 | NOT_RUN | Cần instrumentation commit checkpoint, network proxy hoặc topology/backup riêng. Không gây crash/mạng/restore trong lần POC này. |
| GOV-07 | NOT_RUN | Cần instrumentation commit checkpoint, network proxy hoặc topology/backup riêng. Không gây crash/mạng/restore trong lần POC này. |
| GOV-08 | PARTIAL | Evidence công bố dùng allowlist và so khớp secret thực tế trước publish. Chưa kiểm toàn bộ log, backing store hoặc secret-manager integration. |
| GOV-09 | PARTIAL | Audit API trả 97 record POC theo actor/action/time. Chưa nghiệm thu file export, artifact hash và retention sau rotation; task log cũ bị mất sau restart. |

## Xem lại và chạy task nhỏ

[Trang bằng chứng](https://db-poc.apps.drgdevlab.com) hiển thị ảnh, trạng thái ca và JSON đã chọn lọc.
Trong ODC, mở Projects → odc-oracle-poc và Tickets. Các object POC được giữ để xem lại.
Lệnh API/CLI và thao tác UI được mô tả tại `db-poc/poc/README.md` trong repo GitOps.

Crash checkpoint, network interruption, stale lock, restore và nhiều API replica chưa đủ instrumentation/topology.
Các lần restart sửa vận hành không được dùng làm bằng chứng PASS cho recovery.

Audit listing dùng `fuzzyUsername=POC` theo display name. Đối chiếu `taskId` còn cần kiểm detail/export riêng.

Ticket 1000028 xác nhận thêm phê duyệt qua API: OWNER→DBA, requester bị từ chối khi APPROVING, executor chạy SELECT thành công.
CLI inspect và guard từ chối SHA sai đã chạy. Runner UI readback đã chạy thành công sau khi chờ datasource khởi tạo.

Kiểm tra cuối: cả sáu datasource (kể cả oracle-cloud ban đầu) có Test Connection HTTP 200, active=true lúc 01:42 UTC.
