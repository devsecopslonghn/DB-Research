# Coordinator review T00–T04

Ngày: 2026-10-04. Kết quả: artifact T00–T04 hoàn tất trong phạm vi source/spec.
Deployment/test/service/SQL/benchmark/target inspection: NOT_RUN.

## Task acceptance và dependency

| Task | Artifact | Acceptance của lượt này | Dependency chưa đáp ứng cho runtime |
| --- | --- | --- | --- |
| T00 | [context](../context.md), [preserved hashes](../preserved-evidence.json) | Scope/quyền/gaps/ownership đã ghi; không đọc credential | Target permission, quota host/Oracle, dedicated namespace chưa kiểm |
| T01 | [criteria](../criteria.csv) | 45 expected nguyên văn và 12 nhóm F; 57 ID duy nhất | Runtime mới của mọi ca NOT_RUN |
| T02 | [register](../candidates.csv), [search log](../search-log.md) | 36 mục product/build/fork, phân loại và keep/drop có nguồn; ba vòng tìm | Không phải 36 nền tảng độc lập hoặc toàn bộ thị trường; current HEAD của mục kế thừa chưa re-audit |
| T03 | [per-tool reports](../README.md) và worker reviews | Review sâu CloudDM/AccessFlow/Archery; kiểm đối chứng ODC/Bytebase; DOC/SOURCE/RUNTIME lịch sử tách riêng | Full image/plugin/driver/dependency license audit và runtime correctness chưa kiểm |
| T04 | [shortlist](../shortlist.md), [spec](../benchmark-spec.md), [config](../benchmark-config.json), [SQL manifest](../workloads/manifest.json) | Workload/hash/expected/reset/sampling/stop đã chốt, không chỉnh criteria cho tool | T05–T08, quota thực, build pins, API/UI mapping và quyền benchmark chưa có |

T03 kế thừa source/license hồ sơ cũ cho engine, client và fork ngoài nhóm review sâu.
Register ghi phạm vi đó. Không tuyên bố mọi dòng đã review current source đầy đủ.
Các commercial lead chỉ có DOC, không có SOURCE/RUNTIME được truy cập.

## Review song song và quyết định tổng hợp

Ba worker: discovery, CloudDM và AccessFlow/Archery. Coordinator giữ file chung.
[Worker AccessFlow/Archery review CloudDM](../candidates/accessflow/cross-review.md) xác nhận connector/approval/input checks và giữ giới hạn ledger/dedup.
[Worker CloudDM review AccessFlow/Archery](../candidates/clouddm/cross-review.md) xác nhận admission gate/central checksum và commit/INVALID paths.
Coordinator đọc các nguồn P0 được dẫn trước tổng hợp.

Các điểm được làm rõ:

- Oracle plugin tích hợp của CloudDM là native connector. Nó khác custom migration adapter hoặc wrapper do người dùng ghép.
- Webhook ID validation/dedup DOC không là target migration ledger hoặc exactly-once execution SOURCE/RUNTIME.
- AccessFlow gate chỉ từ chối SELECT/INSERT/UPDATE/DELETE. OTHER được phép, không chứng minh mọi statement chỉ đổi schema.
- AccessFlow raw query path không thay native release path cho SQL-03 hoặc benchmark release có DML.
- Archery có source named PL/SQL INVALID check. Không khẳng định thiếu compile check hoàn toàn, cũng không cấp runtime PASS.
- Archery là B theo ticket model; database operations không tự làm tool đạt full A release model.
- CloudDM pricing cache không xác nhận current cap hoặc image entitlements. File migration có tên license-support không chứng minh paid gate.
- D-Band DRM trùng DRM-cli. SQLE/dbward cũng là tái phát hiện, không đếm discovery mới.
- Bảy fork giữ source/license tại snapshot, không coi rename hoặc license badge là sản phẩm OSS Oracle mới.

Không thấy xung đột nguồn đủ để bỏ source-review conclusions sau các sửa trên.
Mọi feature runtime mới vẫn NOT_RUN. Không có benchmark sample mới.

## Review benchmark độc lập qua Antigravity

Đã kiểm `agy models` và `/usage` trước một run có giới hạn.
Claude/GPT group còn 16% weekly quota và 100% five-hour quota lúc kiểm.
Run pin `claude-opus-5-5-medium`, từ DB-Research, chỉ review artifact tĩnh.
[Task](benchmark-review-task.txt) cấm edit, test, SQL, services, target, network và deployment.
[Result](agy-benchmark-review.json): exit code 0, JSON status SUCCESS, một turn, stderr rỗng.
Không có denied action được báo. Không đổi provider hoặc dùng credits.
Reviewer đọc text/hash/count, không thực thi workload Oracle.

| Issue | Resolution trong bản cuối |
| --- | --- |
| B1: config thiếu pin fields và native/adapter | Thêm plugin/license/Oracle/NLS/quota/topology/reset/observer/API/UI pins; execution_path và adapter hash. Không xếp hạng chung path khác nhau. |
| B2: reset fixture/central state chưa xác định | Schema owner mới mỗi trial; snapshot metadata baseline sạch, evidence export trước reset; preflight object/fixture checks và reset_id. Không reset target uncertain. |
| B3: pool scope có thể vượt 16 session | Tổng executor pool capacity 8; global max8 hoặc per-target max1, tối đa8 target. Observer2/bootstrap1/other5 giữ tổng≤16. |
| N1: replay identity chưa pin | Manifest pin cùng EVAL_REPLAY_V1/version 202610040001 cho original/changed; duplicate version riêng. |
| N2: duplicate response và delivery mode thiếu | Yêu cầu hai response cùng execution decision/job ID; sequential 0ms và concurrent barrier có send-time skew. |
| N3: SQLPlus CWD/SPOOL phụ thuộc host | Pin workload CWD và POC output path; lưu include/spool hash. |
| N4: sample plan/config và đếm success | JSON bổ sung PERF-01..07, ba đợt, timeout/sampling/stop. Fixed attempts gồm lỗi, không chạy bù. |
| N5: gộp đợt để tạo p95 | Giữ percentile API từng endpoint/load/đợt làm kết quả chính; không gộp thành p95 chính. |
| N6: approval thiếu có thể thành zero wait | Full-workflow null/BLOCKED khi thiếu mandatory approval; không ghi zero. |
| N7: release-small không phủ hết correctness | Ghi rõ workload hiệu năng không thay SQL-01..12, function/DECLARE/init/literal vẫn cần ca riêng. |
| Discovery config/concurrency review | Đồng bộ required pins/sample plan; thêm offered/effective concurrency, active_workers và target_sessions. |

Coordinator đã đọc lại spec/config/manifest sau sửa. Không chạy lại review model hoặc test.
Các issue trong JSON là lịch sử review draft; bảng resolution này mô tả artifact cuối.
SQL bytes không đổi sau review. Chỉ bổ sung metadata identity và quy tắc đo/reset.
Fixture vẫn chưa được chạy trên Oracle. T05 cần kiểm validity trước mọi đo thật.

## Completed checks và giới hạn

Đã đối chiếu 45 expected với bảng authoritative trong poc/ORACLE-POC.md. Tất cả khớp nguyên văn.
Đã kiểm CSV/JSON cấu trúc, 57 criteria ID, 60 feature rows và năm hồ sơ 45 cases.
Đã tính lại SHA-256 cho 14 SQL artifact và các tài liệu/JSON lịch sử được ghi trong manifest preservation.
Hash lịch sử không đổi. ODC/Bytebase counts và P03/P04 giữ riêng, không sửa kết quả.
Đã kiểm local Markdown links của tài liệu mới và tài liệu bị sửa.
Đã đọc diff tài liệu để giữ sửa đổi trong scope: index, link cập nhật và trạng thái source/runtime cũ.
Không có Git repository nên [diff này](document-diff.patch) được tạo từ nội dung trước/sau của các file tài liệu đã sửa.
Không có deployment, live entitlement, Oracle connection, test suite, SQL execution, browser screenshot hoặc performance verification.
Không xác minh lại live status của cluster hoặc secret. Quyền target/resource ceiling còn là dependency của T05/T09.

## Unverified acceptance items

License release image/driver/plugin, free caps thực tế, current maintenance của toàn bộ longlist và build/resource pins còn thiếu.
Oracle 19c/21c, full SQL/PLSQL/parser, negative governance, target state/recovery và real GitLab/Jenkins cần runtime mới.
Crash/fencing/restore/HA cần T10 với target/checkpoint riêng.
Benchmark p95/throughput/CPU/RAM chưa có samples. Không tính điểm hiệu năng hoặc chọn người thắng production.
