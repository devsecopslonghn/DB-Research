# Review read-only T04: criteria và benchmark spec

Ngày review: 2026-10-04. Scope: đọc `evaluation/criteria.csv`, `evaluation/benchmark-spec.md`, `benchmark-config.json`, `workloads/manifest.json`. Không sửa các file đó. Không chạy test, SQL, deployment, service hoặc benchmark.

## Criteria

- CSV parse inspection ghi nhận 57 dòng: 45 tiêu chí gốc (12 MODEL, 12 SQL, 12 REC, 9 GOV) và F01–F12. ID không trùng. Tất cả 57 `new_run_status` đang `NOT_RUN`; historical results vẫn ở trường riêng. Không thấy thay đổi tiêu chí để nới điều kiện tool nào.
- 12 dòng F01–F12 có expected/evidence/origin và trỏ về kế hoạch. F03 ghi tách quyền platform/DB; F04 ghi Oracle SQL/PLSQL; F05 giữ ledger/checksum/recovery; F06–F09 giữ review, promotion và audit. F12 giữ raw samples và cách lặp.
- Đây là kiểm cấu trúc/trạng thái hiện tại, không phải diff lịch sử. Tôi không xác minh độc lập rằng từng byte của 45 expected trùng `poc/ORACLE-POC.md`; T01/context hiện tại là nguồn giữ nguyên, và không chỉnh criteria trong review này.

## Benchmark spec

- Spec có revision, trạng thái NOT_RUN, workload SQL manifest/hash, correctness hậu kiểm, raw-sample schema, dừng vì lỗi P0/resource, giới hạn tài nguyên, điều kiện pin và caveat Oracle 26ai so với 19c/21c. Spec tách queue, execution, approval wait và end-to-end; không dùng số ít để tuyên bố p95 ổn định; không chấm performance khi chưa có SLA. Đây là các guardrail phù hợp.
- Sample/round sizes được nêu rõ trong spec; workload manifest có 14 artifact cùng SHA-256 và byte count. Inspection chỉ đọc JSON/CSV/text; không tính lại hash hoặc execute workload.
- **Config gap:** `benchmark-config.json.required_pin_fields` chưa chứa toàn bộ pin đã yêu cầu trong spec. Thiếu service class, charset/NLS, CPU/session quota, scheduler/topology, parser version, timeout/retry, fixture/release IDs, metadata snapshot, observer actor/privilege/sampling/clock, API/UI mapping và capability native/adapter. Spec hiện có nêu các trường này, nhưng config chưa enforce chúng.
- **Sample-plan gap:** `minimum_samples` trong JSON chỉ biểu diễn API/UI/migration nhỏ. Nó chưa biểu diễn PERF-02 onboarding, PERF-05 concurrency wave, PERF-06 paired cases, ba đợt độc lập, hay PERF-07 NOT_RUN. Dùng spec làm nguồn định lượng hiện tại được, nhưng config không tự mang đầy đủ kế hoạch.
- **Concurrency interpretation:** spec khóa worker ở 1 và đưa concurrency thử 1/2/4/8. Cần phân biệt offered job concurrency với số executor thực sự chạy đồng thời. Nếu worker=1 làm hàng đợi tuần tự, đó là kết quả/capacity của cấu hình này; không được diễn giải thành concurrency của tool. Raw samples hiện ghi `concurrency` nhưng chưa có trường `effective_concurrency` hoặc `active_workers`.
- **Stop threshold:** mức dừng API >1%/100 request là operational guardrail, không phải SLA; spec nói đúng điều này. Cần dùng theo endpoint/concurrency cell và không gộp mẫu khác tải.
- **Precondition:** quota host/Oracle, build/image/driver, account observer, schema isolation, fixture validity và API/UI mapping chưa kiểm. Spec phân loại các việc đó là điều kiện T05/T09 chứ không tuyên bố đã hoàn tất. Giữ T09 BLOCKED/NOT_RUN cho đến khi có pin/permission/quota thực tế.

## Kết luận review

Không thấy tiêu chí bị nới hoặc benchmark đã chạy. Trước T09 nên coordinator đồng bộ `benchmark-config.json` với các required pin fields và sample plan trong spec; thêm ghi nhận effective concurrency. Đây là kiến nghị review, không sửa trong thư mục ngoài discovery. Mọi thông số host/Oracle còn là đề xuất cho tới khi T05 xác minh.
