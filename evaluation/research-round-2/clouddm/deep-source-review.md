# CloudDM: rà soát sâu source và governance

Ngày rà soát: 2026-10-04. Source pin: `ClouGence/open-cdm@a9f16e78b8288c9a4158ee9df4378ee16b80021e` (Git tree không truncated). Các tệp tải chọn lọc và SHA-256 nằm trong [source-manifest.json](source-manifest.json). Không build, chạy test, service, SQL, credential hoặc live DB. Mọi kết luận runtime: **NOT_RUN**.

## Kết luận

Đường CloudDM change flow đến executor tồn tại trong source: webhook nhận event, ghi receipt, tạo change; approval tạo ticket/attachment; AutoExec đóng gói QueryRequest; sidecar tải gói và chạy từng request qua session agent. Đây là SOURCE, không xác nhận flow chạy thành công hay đúng trên Oracle.

Phát hiện mới quan trọng: webhook dedup có receipt DB và insert-ignore. DDL migration xác nhận unique key theo `(owner_uid, ref_flow_id, delivery_id)` và `(owner_uid, ref_flow_id, commit_id)`. Trigger service chạy trong transaction, khóa flow bằng `SELECT ... FOR UPDATE`, rồi reserve receipt bằng `INSERT IGNORE`. Đây là dedup webhook bền vững cho delivery/commit theo flow. Đây không phải dedup SQL migration. `AutoExecJob` có tùy chọn RETRY/SKIP/FAIL và tùy chọn transaction nhóm. SKIP cho phép job báo tiếp tục sau lỗi statement; transaction không đảm bảo Oracle DDL atomic vì Oracle implicit commit. Không thấy target migration ledger, checksum theo migration ID, target lock, replay protection hoặc uncertain-commit reconcile trong đường worker đã trace.

Oracle support có hai lớp khác nhau:

- **Generic runtime executor:** worker đọc QueryRequest JSON-lines từ ZIP rồi gửi từng request qua `SessionAgent`. Oracle JDBC session thực thi query bằng `Statement.execute` hoặc callable. Ticket path split SQL trước đó qua Oracle-specific SPI theo datasource type.
- **Oracle-specific parser/splitter:** ticket execution gọi `analysisSplitStream` bằng datasource config; `QueryAnalysisServiceImpl` lấy `SqlEngineSpi` rồi engine-specific `SplitAnalysisSpi`. Oracle SPI dùng ANTLR grammar cho statement, slash delimiter, PL/SQL và q-quoted string. `sql_script` nhận slash delimiter; lexer có q-quote rule kèm TODO context-sensitive. Grammar cũng có rules cho `SET`, `PROMPT`, `WHENEVER`, `START`, `EXIT`, `SHOW ERRORS` và `TIMING`. Đây là parser support trong SOURCE, không chứng minh client semantics hoặc runtime behavior. Oracle session có compile helper đọc `ALL_ERRORS`, nhưng `QueryRequest.useCompile` mặc định false và AutoExec không bật flag ở đường đã trace.

Không kết luận CloudDM không có tính năng chỉ từ grep. Các gap bên dưới là absence of evidence trong pin/tập tệp và truy vấn đã nêu. Cần runtime POC để kết luận hành vi, entitlement và tương thích Oracle.

## Luồng đã quan sát

1. Webhook kiểm tra delivery ID và commit, tạo `ChangeTriggerContext`, gọi service trigger. `DmChangeServiceImpl` tạo receipt với owner, flow, provider, delivery, commit và trigger type; `reserve` trả 0 thì bỏ qua trigger trùng. SQL mapper dùng `INSERT IGNORE`. Migration khai báo unique keys cho delivery ID và commit ID theo owner+flow. Kết hợp với transaction và `SELECT ... FOR UPDATE` trên flow row, source xác nhận webhook dedup bền vững theo delivery/commit; race runtime chưa kiểm.
2. Change flow giữ commit ID và tạo change gắn với flow. Source có lock row trên flow ở trigger handler; đây là serialization của trigger-flow, không phải lock Oracle schema khi chạy migration.
3. Approval action dựng target path theo datasource/levels, đặt applicant, environment, approval template và ticket state; gắn SQL artifact dạng locked attachment và tạo approval process. Attachment row giữ SHA-256; confirmed blob được đọc khi split. Source chưa so hash attachment với hash gói execution.
4. AutoExec tạo job/tập task; đóng gói requests vào ZIP, tính MD5 gói và lưu attachment. Worker tải gói theo offset, kiểm size/MD5 rồi đọc QueryRequest records. MD5 ở đây bảo vệ gói khi tải, không phải checksum migration bền vững theo target.
5. Worker chạy từng QueryRequest qua `sessionAgent.submitQueries`. Tùy chọn transaction gọi `setAutoCommit(false)`, commit/rollback ở cuối job. Lỗi request có thể retry, skip hoặc fail theo cấu hình. Không thấy target ledger hoặc per-migration reconciliation trong đường này.

## Oracle SQL và parser

Oracle parser được nối vào CICD: `ApprovalControlServiceImpl.createExecJob` split confirmed SQL attachment bằng `QueryAnalysisService.analysisSplitStream(dsConfig, ...)`; `QueryAnalysisServiceImpl` chọn SPI theo datasource. Grammar `sql_script` chấp nhận slash delimiter; lexer nhận q-quoted string và parser có anonymous PL/SQL, procedure/package, cùng một số lệnh SQL*Plus (`SET`, `PROMPT`, `WHENEVER`, `START`, `EXIT`, `SHOW ERRORS`). Q-quote lexer có TODO về quote phụ thuộc ngữ cảnh. Grammar chỉ chứng minh khả năng parse/split, không chứng minh JDBC mô phỏng ngữ nghĩa lệnh SQL*Plus. `SPOOL`, `@@`, các dạng `SET` và chỉ thị khác cần ca kiểm tra cụ thể. Trace này áp dụng đường ticket approval; không khẳng định cùng parser xử lý mọi đường truy vấn ad-hoc.

`OraSession` là executor generic JDBC session chuyên Oracle. Nó gọi `executeStatement` qua hook; `executeStatement` dùng callable hoặc `Statement.execute`. `beforeQueryRequest` bỏ dấu `;` cuối trong một số trường hợp. `compileResultSql` truy vấn `all_errors`, nhưng chỉ ở nhánh request `isUseCompile`, và helper chọn owner/name. Điều này hỗ trợ compile diagnostics trong một execution mode. Chưa thấy AutoExec tự gắn compile mode hoặc fail job khi object `INVALID`/`ALL_ERRORS` khác rỗng.

Runner dùng Oracle-specific parse/split trước JDBC execution, nhưng generic worker không cho thấy xử lý `PROMPT`/`WHENEVER`/`START` thành hành vi client. Không thấy post-DDL `ALL_OBJECTS`/`ALL_ERRORS`, migration ledger hoặc recovery-aware auto-commit model. Phần này cần POC với SQL-08–SQL-12 và REC-01/04/05.

## Error, commit, replay, locking

`AutoExecJob` mở transaction tùy chọn cho cả job. Khi job pause/fail thì rollback JDBC transaction; khi thành công thì commit. Oracle tự commit DDL, nên rollback trong source không khôi phục được DDL đã commit ngầm. Đây là giới hạn kỳ vọng từ Oracle semantics; runtime partial state chưa kiểm.

Mỗi request có trạng thái start/finish/wait-confirm/fail/retry/skip qua service message. Khi error strategy là SKIP, worker ghi skip rồi tiếp tục vòng request kế tiếp. Vì vậy policy có thể coi job hoàn tất dù có SQL lỗi bị skip, tùy phần tổng hợp status. Xác minh trạng thái job cần runtime và kiểm message reducer.

Không thấy target-side version table/ledger hoặc compare checksum theo ID trong worker và Oracle session đã tải. Gói có MD5 cho truyền tải; webhook có receipt theo delivery; cả hai không thỏa migration replay/checksum. Map in-memory trong sidecar tránh duplicate job ID trong một process, còn server gọi `startJob` để nhận job. Chưa có bằng chứng distributed target-schema lock, stale lock, hoặc crash giữa Oracle commit và central record.

## Approval, target binding, promotion

Approval code tạo ticket với target path, datasource, environment, applicant và attachment khóa. Đây là SOURCE tích cực cho workflow review. Attachment service tính SHA-256 khi lưu và xác minh size/hash khi phục hồi blob vào cache. CICD execution đọc confirmed attachment đó rồi split và serialize request bodies. Gói AutoExec được hash MD5 cho transport, sidecar xác minh hash/size trước khi chạy. Source không so sánh SHA-256 attachment với hash gói, nhưng có đường nội dung bắt nguồn từ attachment được khóa. Cache file có sẵn được dùng mà không re-hash ở mỗi lần đọc. Ticket giữ datasource ID và levels/target được dùng để tạo job; chưa thấy target sửa trong flow confirm này. Approval action kiểm người trong allow-list. Change handler luôn thêm primary account vào approvers. Không có requester-versus-approver inequality guard trong handler đã đọc. Ghi quyền primary account thành admin authority riêng; nếu applicant là primary account thì source cho phép overlap, nhưng đây không kết luận GOV-03 thất bại với người dùng thường. Runtime identity và policy cần kiểm.

Change flow/service có quan hệ parent/batch/children và cascade transfer. Điều đó cho thấy workflow nhiều luồng có thể được điều phối; chưa chứng minh một artifact bất biến được promote DEV→SIT→UAT→PROD theo thứ tự, với prerequisite enforced. Tên environment gắn approval ticket không phải bằng chứng promotion gate.

## License/source gate

Repository metadata/source manifest pin Apache-2.0 cho repository source. Không suy license của image, plugin, driver, Oracle JDBC hoặc dependency đóng gói. Các migration license cho thấy schema/protocol support, nhưng source được chọn chưa cho thấy validator hoặc hard counter. Cần review license service và đúng release/image để chốt entitlement gate. Không suy đoán gate từ tên migration hoặc bỏ gate bằng API khác.

## Search trace và giới hạn bằng chứng

Đã đọc coordinator instructions, criteria P0/P1, CloudDM prior source review, source manifest, metadata và toàn bộ path list từ pinned tree (`truncated=false`). Truy vấn symbol/file đã dùng gồm `AutoExecJob`, `AutoExecServiceImpl`, `AutoExecRServiceProvider`, `ExecJobRServiceProvider`, `OraSession`, `OraSqlEngineSpi`, `PlSqlLexer`, `DmChangeServiceImpl`, `DmChangeTriggerReceipt`, `ChangeActionForApproval`, `ChangeFlowWebhookPolicy`, `ErrorStrategy`, `ALL_ERRORS`, `setAutoCommit`, `commit`, `rollback`, `deliveryId`, `reserve`, `SplitScript`, `qquote`, `SQLPlus`, `slash`.

Phạm vi âm tính: thiếu kết quả cho keyword hoặc thiếu path trong tập tải không chứng minh repository/release khác không có tính năng. Không tải toàn bộ repository. Grammar/parser được tải chọn lọc sau khi trace wiring xác nhận parser được gọi. Đã truy schema migration receipt, flow row lock, split provider theo datasource, approval confirm và handler cho Change. Chưa trace hết plugin artifact packaging/registration trong image, kiểm hash cache file còn nóng, final job status aggregation và mọi chính sách external approval provider. Source cho thấy primary account được thêm vào allow-list; requester trùng primary vì vậy có thể self-approve, nhưng runtime cần kiểm route/quyền thực tế. Những điểm này ghi là GAP, không phải FAIL.

## License và giới hạn instance/account

Source migration `V202605070005__add_rdp_license.java` tạo các bảng `rdp_auth_version_field`, `rdp_auth_code_info`, `rdp_apply_code_info` và `rdp_auth_result_info`, đồng thời chèn opaque field payload theo license version. `V202605070011__dm_license_support.java` chỉ nới độ dài cột trạng thái kết quả; `V202605070018__dm_query_ds_count.java` thêm opaque payload cho version `4.6.1`. Các migration là evidence về schema/protocol support, không phải entitlement validator hoặc counter enforcement.

Tìm kiếm source đã tải theo symbol/path `License`, `RdpAuth`, `rdp_auth`, `license_version`, instance/datasource/account count và giới hạn không tìm thấy service/validator hoặc counter path. Scope là source snapshot `a9f16e78b8288c9a4158ee9df4378ee16b80021e`, các tệp migration trên, cùng paths CloudDM đã chọn trong manifest; không tải hay audit toàn tree. Vì vậy ngưỡng 10 instance/5 account chưa được chứng minh là hard counter trong pin. Cũng chưa thể kết luận gate chỉ nằm trong plugin/binary riêng. Cần xác nhận mã license service, image/plugin artifacts và phản hồi entitlement trước khi định giá hoặc loại nền tảng.

Pin source này được đối chiếu với 11 tệp chọn lọc của CloudDM `v4.3.0` tại commit `3aa1238a471afca2579e76e6fbf0a922d9be5579`; manifest coordinator ghi nhận byte-identical cho các tệp đó. Không suy rộng kết quả sang toàn repository hoặc image.

## Ca POC kế tiếp

Giữ tiêu chí hiện tại. Sau khi xác nhận đúng image/license/driver, chạy riêng Oracle POC: PL/SQL procedure/package/spec+body; slash; q-quote; directive SQL*Plus; invalid compilation/`ALL_ERRORS`; CREATE rồi ALTER lỗi; `SKIP` với lỗi ở giữa; retry sau DDL commit; replay cùng ID, replay đổi hash; crash sau commit trước record; webhook delivery lặp và hai delivery cùng commit đồng thời; approval sửa target/artifact; tự duyệt; batch environment order. Thu response, actor, target, SQL SHA, timestamp, logs, `ALL_OBJECTS`, `ALL_ERRORS`, dictionary state và side effects. Benchmark throughput chỉ sau correctness/replay/error gates đạt; dùng benchmark spec chung đã khóa, không thay workload.
