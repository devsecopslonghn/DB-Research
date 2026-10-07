# Benchmark spec oracle-common-v1

**Spec và SQL đã đóng băng. Chưa có benchmark hoặc xếp hạng tốc độ.**

Ngày: 2026-10-04. Task T04. Trạng thái chạy: NOT_RUN.
[Config](benchmark-config.json) và [SQL manifest](workloads/manifest.json) là artifact đầu vào.
Chỉ coordinator đổi revision khi có yêu cầu phù hợp. Mọi tool phải nhận cùng revision mới.
Không sửa workload để làm tool đạt. Ghi capability gap nếu tool không hỗ trợ.

## Điều kiện bắt đầu T05 và T09

T05 cần phạm vi deployment, namespace, schema/account và quota target được xác định.
Lượt này chưa cấp quyền thực thi T05–T10.
T09 chỉ bắt đầu sau T06–T08 và lượt user cho phép benchmark.
Mỗi workload cần hậu kiểm correctness trước đo. Lỗi P0 chặn kết luận production-ready.
Tool có P0 chưa xử lý chỉ được đo thăm dò riêng, nếu lượt sau cho phép rõ phạm vi đó.
Không đưa kết quả thăm dò vào bảng tốc độ của migration đã nghiệm thu.
Không cần chạy lại ca cũ nếu build, policy và câu hỏi không đổi.
Cần chạy lại workload chung để so sánh hiệu năng. Bằng chứng cũ không có điều kiện đo tương đương.

Phải điền toàn bộ `required_pin_fields` trong config trước đo:

| Hạng mục | Điều kiện |
| --- | --- |
| Build | Tool, edition, commit, image digest, plugin và license hợp lệ |
| Oracle | Full version, charset, NLS, service class, quota CPU/session, scheduler và database topology |
| Execution | Driver/parser version, worker count, pool min/max, timeout và retry policy |
| Host | Host/network/storage class, CPU/RAM tổng platform và các khác biệt bắt buộc |
| State | Schema ID riêng, fixture revision/hash, release ID/version và central metadata snapshot |
| Observer | Actor read-only, quyền hậu kiểm, sampling interval và đồng hồ đã đồng bộ |
| Capability | API route và UI scenario mapping trước đo, native/adapter ghi riêng |

Oracle 26ai 23.26.4.1.0 là baseline lịch sử khả dụng. Phải kiểm lại phiên bản trước lượt mới.
Oracle 19c và 21c cần các lượt riêng. Không suy rộng kết quả 26ai.
Không dùng quyền SYS/SYSTEM cho executor. Observer chỉ nhận quyền cần cho hậu kiểm schema POC.
Không tự đổi NLS hoặc cấu hình Oracle dùng chung.
Schema riêng trên một instance là target logic, không chứng minh cách ly vật lý.
Pin pool_scope và mọi idle connection. Tổng session: executor ≤8, observer ≤2, bootstrap ≤1, connection khác ≤5.
Với per-target pool, chỉ mở tối đa 8 target đang đo và mỗi pool max 1. Tổng mọi session phải ≤16.
Nếu tool không giữ được ceiling này, ghi BLOCKED thay vì âm thầm nâng quota.

## Trần tài nguyên đã chốt cho đề xuất

| Tài nguyên | Ceiling cho một tool |
| --- | --- |
| CPU toàn platform | 4 vCPU, gồm server, metadata DB, worker và proxy |
| RAM toàn platform | 8 GiB |
| Persistent storage toàn platform | 20 GiB |
| Worker | 1, giữ cố định giữa các lượt native |
| Pool target | Capacity tổng 8. Global pool min 1/max 8; nếu per-target, mỗi target min 1/max 1. |
| Session Oracle của benchmark | Tối đa 16, gồm executor, observer và bootstrap |
| Job concurrency | 1, 2, 4, 8 trên target độc lập |
| API read concurrency | 1, 2, 4, 8 |
| API/request timeout | 30 giây |
| Job wall-time timeout | 300 giây |
| UI navigation timeout | 60 giây |
| Resource sample interval | 1 giây |

Đây là ceiling đề xuất, chưa phải quota host đã kiểm. T05 phải xác nhận khả năng cấp phát.
Nếu kiến trúc cần vượt ceiling, ghi BLOCKED. Sửa spec chung theo revision trước chạy mọi tool.
Không hạ mức tài nguyên riêng để tạo số so sánh thuận lợi.
Oracle target không nằm trong ngân sách platform. Ghi quota target và session/load riêng.
Tool có nhiều process được phân bổ ngân sách bên trong cùng ceiling.
Không bỏ metadata DB hoặc proxy khỏi số CPU/RAM/storage tổng.

## SQL và fixture

SQL dùng UTF-8, LF. SHA-256 tính trên byte nguyên vẹn.
Không thay schema vào SQL. Mỗi connection dùng owner schema riêng.
Nếu platform tự đổi SQL, lưu input/output hash và ghi transformation. Không gọi artifact đó bất biến.
Fixture dùng dữ liệu giả. Không dùng dữ liệu hoặc schema lịch sử Bytebase/ODC.

| Artifact | Nội dung và hậu kiểm bắt buộc |
| --- | --- |
| `fixture-inventory.sql` | 10 bảng EVAL_INV_01..10, mỗi bảng có primary key. Giữ đúng 10 bảng cho discovery. |
| `release-small.sql` | CREATE/ALTER, INSERT/UPDATE, procedure, package spec/body, trigger, block và COMMIT. AMOUNT=151, STATUS=NEW, NOTE=initial. EVAL_EVENT có đúng một hàng 150→151. Function trong package trả 151. Tất cả object VALID, không có lỗi compile. |
| `statements-10.sql` | Đúng 10 SQL statements: CREATE, 8 INSERT, COMMIT. 8 hàng. SUM(VALUE)=36. |
| `statements-100.sql` | Đúng 100 statements: CREATE, 98 INSERT, COMMIT. 98 hàng. SUM(VALUE)=4851. |
| `statements-1000.sql` | Đúng 1000 statements: CREATE, 998 INSERT, COMMIT. 998 hàng. SUM(VALUE)=498501. |
| `dml-1000.sql` | CREATE, INSERT 1000 hàng, UPDATE mỗi hàng một lần, COMMIT. SUM(VALUE)=501500. |
| `dml-10000.sql` | CREATE, INSERT 10000 hàng, UPDATE mỗi hàng một lần, COMMIT. SUM(VALUE)=50015000. |
| `replay.sql` | Migration version cố định. EVAL_REPLAY có đúng một hàng (1,1). Replay không tạo effect mới. |
| `replay-changed.sql` | Giữ migration ID/version của replay, đổi bytes. Validation phải FAIL trước execution. Không dùng version mới cho REC-08. |
| `duplicate-effect.sql` | Sau fixture replay, hai request cùng approved execution identity chỉ tăng VALUE từ 1 lên 2. |
| `invalid-compilation.sql` | Procedure dùng symbol thiếu. ALL_ERRORS có lỗi và release không báo fully successful. |
| `partial-ddl.sql` | CREATE commit theo Oracle DDL, ALTER dùng type thiếu. Bảng còn tồn tại. Central state phải báo partial/uncertain và chặn replay tự động. |
| `sqlplus-directives.sql` và `eval-include.sql` | Ca SQL-10 riêng. Không dùng để thay release-small. Directive unsupported phải fail rõ trước execution. `@` và `@@` dùng cùng include đã pin. |

Các mô tả hậu kiểm là expected, chưa phải kết quả chạy.
`release-small.sql` là workload hiệu năng, không thay SQL-01..12 cho nghiệm thu correctness.
Function độc lập, DECLARE block, package initialization có effect và literal cases vẫn cần ca gốc riêng.
Replay/changed giữ migration ID EVAL_REPLAY_V1 và version 202610040001 như manifest.
Duplicate-effect dùng EVAL_DUPLICATE_V1/version 202610040002, cùng approved execution identity.
Hai response phải liên kết cùng execution decision/job ID, ngoài việc target chỉ có một effect.
PERF-06 chạy hai delivery mode riêng: sequential delay 0 ms và concurrent cùng client barrier.
Ghi actual send-time skew, không suy ra concurrent arrival chỉ từ thời điểm bắt đầu thread.
SQLPlus chạy từ thư mục workload chứa include đã pin. SPOOL chỉ ghi trong thư mục output POC riêng.
Pin working directory/spool path, lưu spool hash và request/result. Không ghi lên thư mục dùng chung.
Observer phải kiểm ALL_OBJECTS/ALL_ERRORS, object definition, row count và giá trị.
Không chỉ kiểm terminal state UI/API.
Kiểm central history, artifact hash, actor và ledger đích bằng connection độc lập.
Nếu không có ledger đích, ghi gap. Central revision không tự đáp ứng REC-06.
Không chạy retry tự động trong harness. Retry native phải pin cấu hình và lưu từng attempt.

## Kịch bản và số mẫu

| Mã | Workload chung | Warm-up và mẫu |
| --- | --- | --- |
| PERF-01 | API inventory list, target status, job status. UI inventory và job detail. | API: 3 warm-up rồi ít nhất 100 request mỗi endpoint/mức concurrency/đợt. UI: 3 warm-up, 10 lượt mỗi scenario/đợt. |
| PERF-02 | Onboarding 1/10/50 target logic, fixture 10 bảng mỗi target. | 1 warm-up mức 1. 5 lần mỗi mức được edition/quota cho phép. Không chia estate để lách giới hạn. |
| PERF-03 | `release-small.sql`, một target. | 3 warm-up, ít nhất 5 release độc lập/đợt. |
| PERF-04 | 10/100/1000 statements, rồi DML 1000/10000 hàng. | 3 warm-up và 5 lượt mỗi artifact/đợt. Tăng mức tuần tự. |
| PERF-05 | `release-small.sql` trên target độc lập, concurrency 1/2/4/8. | 3 warm-up mỗi mức, 5 wave mỗi mức/đợt. Mỗi wave gồm đúng số job bằng concurrency. |
| PERF-06 | Replay, checksum đổi, duplicate approved execution. | 3 warm-up và 5 paired trial mỗi case/đợt. Request reject/skip không tính throughput migration. |
| PERF-07 | Restart/recovery checkpoint riêng. | NOT_RUN đến T10 và quyền fault injection trên deployment dành riêng. Không kill dịch vụ chung. |

Chạy ba đợt độc lập, reset fixture giữa các trial ngoài cửa sổ đo.
Số lượt là số attempt cố định, kể cả lỗi. Không chạy bù để đủ năm success.
Nếu stop policy kích hoạt, ghi cell chưa đủ mẫu và giữ mọi error đã thu.
Luân phiên thứ tự tool giữa đợt bằng lịch đã lưu. Ví dụ A/B/C, B/C/A, C/A/B.
Chỉ một tool tạo tải trên shared Oracle. Coordinator giữ lịch và ghi tải nền trước/sau lượt.
Warm-up dùng schema khác có fixture cùng hash, không tạo applied state cho measured migration ID.
Không tái sử dụng release version đã applied cho PERF-03..05.
Không chạy cold-start cùng steady-state. Ghi riêng startup time nếu được đo.

Onboarding 50 target là điều kiện giữ nguyên. Edition limit khiến mức đó BLOCKED.
Pool/worker giữ nguyên khi tăng job concurrency. Ghi queue nếu capacity thấp hơn concurrency.
`concurrency` là offered job concurrency. Ghi `effective_concurrency`, active worker và target session thực tế.
Worker=1 không bảo đảm chỉ một execution đồng thời. Không suy concurrency capacity từ mức offered.
Chỉ tăng mức khi mức trước không có lỗi correctness hoặc vượt ceiling.

## Reset đã chốt

Mỗi migration trial dùng owner schema mới, cùng cấu hình/quota và schema ID đã lưu.
PERF-05 tạo số schema mới bằng offered concurrency trong một wave.
Trước trial, observer kiểm số object thuộc owner bằng 0 qua ALL_OBJECTS, không đếm object được grant từ owner khác.
PERF-02 tạo schema mới rồi áp fixture 10 bảng trước cửa sổ onboarding.
Observer kiểm đủ 10 bảng/PK và fixture hash trước đăng ký target.
PERF-06 giữ cùng schema trong một paired trial, reset trước trial kế tiếp.
Metadata trial bắt đầu từ snapshot baseline sạch đã pin, có actor/policy nhưng không có target/release benchmark đã applied.
Trước restore snapshot, xuất mọi raw evidence khỏi deployment POC. Không restore metadata lịch sử Bytebase/ODC.
Pin snapshot ID/hash và quyền restore trong T05. Nếu không tạo baseline sạch, cell đó BLOCKED.
Reset/restore/onboarding bootstrap nằm ngoài duration migration. Ghi reset_id và inspection kết quả.
Mọi reset chỉ áp dụng schema/deployment POC có ownership rõ. Không reset target uncertain để lấy thêm mẫu.
Reset benchmark không nghiệm thu GOV-06 production restore hoặc reconciliation.

## Thời gian và tài nguyên

Dùng monotonic clock cho duration. Dùng UTC timestamp cho truy vết giữa hệ thống.
Ghi `submitted`, `accepted`, `approval_ready`, `queued`, `started`, `terminal`, `observer_verified` nếu có.
Ghi nguồn timestamp. Không trộn server clock và client clock nếu chưa biết clock skew.
Đo client end-to-end từ request đầu đến terminal state, gồm polling interval cố định 250 ms.
Tách `queue_ms`, `execution_ms`, `approval_wait_ms`, `request_to_terminal_ms` và `verification_ms`.
Nếu tool thiếu timestamp đủ nghĩa, ghi null và limitation. Không suy ra execution time từ tổng wall time.

Approval có hai cửa sổ: trải nghiệm workflow đầy đủ và execution sau approval đã hoàn tất.
Giữ cùng role/policy và artifact/target. Không dùng auto-approval riêng cho một tool để tăng tốc.
Nếu không có mandatory approval hợp lệ, full-workflow window là null/BLOCKED, không ghi approval_wait_ms=0.
Native/adapter/direct_client là ba execution_path riêng. Không xếp hạng chung các path khác nhau.
Migration throughput = số job unique có terminal success và hậu kiểm đúng / thời gian đo phút.
Không tính job sai, skipped replay, request được nhận hoặc duplicate effect là success throughput.
Raw rows bị lỗi vẫn phải giữ. Không loại outlier chỉ vì thời gian cao.

Resource metrics gồm CPU, peak/steady RAM, disk growth, target connections và restart count.
Ghi từng component và tổng platform. Ghi cách lấy số đo và overhead observer/harness riêng.
Direct Oracle client là baseline đường thực thi, không phải platform thay thế.
Dùng cùng SQL bytes và fixture. Ghi driver/client khác trước khi so sánh duration.
Không gọi chênh lệch đó là platform overhead thuần khi driver hoặc tracing khác nhau.
Không suy ra tool tối ưu SQL từ wall time thấp hơn.

## Raw sample contract

T09 ghi `evaluation/benchmarks/<tool>/<run-id>/`:

1. `config.json`: toàn bộ pin fields, lịch đợt và workload manifest.
2. `samples.csv`: mỗi request/job một hàng, kể cả lỗi.
3. `resources.csv`: UTC timestamp, component, CPU, RAM, disk, connection và restart count.
4. `errors.jsonl`: request/response đã che secret, error class, uncertain state và recovery action.
5. `verification.jsonl`: actor, schema, SQL hash, row/object/error/ledger inspection và verdict.
6. `summary.json`: số mẫu, coverage, metric, exclusions có lý do và limitation.

Cột samples: `run_id,round,tool,edition,build,execution_path,adapter_commit_or_hash,workload_revision,sql_sha256,release_version,reset_id,approval_window,case_id,target_id,actor,request_id,job_id,attempt,concurrency,effective_concurrency,active_workers,target_sessions,is_warmup,submitted_utc,terminal_utc,api_ms,queue_ms,execution_ms,approval_wait_ms,request_to_terminal_ms,verification_ms,http_status,terminal_status,correctness_status,duplicate_effect,error_class`.
Không ghi password, wallet, token, cookie hoặc connection string có secret.
Ảnh UI phải là ảnh trình duyệt thật đã sanitized. Chưa có ảnh mới trong lượt này.

## Thống kê và dừng

API p50/p95 chỉ tổng hợp trong cùng endpoint, tải, đợt và cấu hình.
Báo cỡ mẫu, HTTP error rate và phương pháp quantile nearest-rank.
100 mẫu là tối thiểu thiết kế, không chứng minh p95 ổn định hoặc SLA production.
UI/migration mẫu nhỏ báo raw values, median, min/max và số lỗi. Không công bố p95 ổn định.
Kết quả chính giữ percentile từng đợt. Không gộp đợt để công bố một p95 chính.
Nếu phân tích phụ gộp raw rows, phải giữ endpoint/load/config/path và báo từng đợt bên cạnh.
Không có SLA do user xác nhận. Chưa tính điểm hiệu năng hoặc điểm tổng.
Không xếp tốc độ giữa workload hash, edition, fixture hoặc target version khác nhau.

Dừng ngay khi có false success, duplicate effect, cross-schema access hoặc leak secret.
Giữ evidence, không reset target uncertain để tiếp tục lấy mẫu.
Dừng workload sau một job timeout 300 giây. Ghi trạng thái uncertain và yêu cầu hậu kiểm.
Dừng tăng tải khi RAM/CPU/session/storage vượt ceiling, OOM/restart hoặc target có cảnh báo quản trị.
Dừng mức tải khi API error rate vượt 1% trong 100 request hoặc hai request liên tiếp timeout.
Điều kiện dừng là resource/correctness gate, không phải SLA hiệu năng.
Coordinator kiểm tải nền và health giữa wave. Không chạy fault injection để tự sửa kết luận.

## Các phần còn thiếu trước thực thi

Chưa xác minh quota host/Oracle, quyền schema, account observer hoặc dedicated namespace.
Chưa pin image/driver cho CloudDM, AccessFlow và Archery.
Chưa kiểm SQL fixture trên Oracle. Có thể phát hiện lỗi fixture khi T05 được phép.
Nếu fixture cần sửa lỗi, tăng revision chung và cập nhật mọi hash trước chạy tất cả tool.
Chưa có API endpoint mapping cuối cùng hoặc phương thức metrics cho từng build.
Chưa có approval hợp lệ trên Bytebase FREE. Không đổi criterion sang approval SKIPPED.
Chưa có crash checkpoint/fencing/restore plan. PERF-07 giữ NOT_RUN.
