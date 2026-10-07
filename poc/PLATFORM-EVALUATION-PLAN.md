# Kế hoạch đánh giá nền tảng quản lý DB và migration

Kế hoạch này tìm các sản phẩm gần Bytebase, đánh giá chức năng và so sánh hiệu năng trên cùng workload.
Oracle là database bắt buộc. Bản miễn phí, mã nguồn mở và tự triển khai là nhóm lựa chọn chính.
Bytebase là đối chứng về mô hình sản phẩm. Không mặc định Bytebase đạt mọi tiêu chí.

Đây là kế hoạch, chưa phải kết quả benchmark hoặc lệnh triển khai.
Các tham số benchmark và trọng số dưới đây là đề xuất ban đầu.

## Mục tiêu và điều kiện hoàn tất

1. Tạo danh mục ứng viên rộng, có nguồn, phiên bản và lý do giữ hoặc loại.
2. Phân biệt nền tảng quản lý thay đổi, cổng duyệt SQL và migration engine.
3. Xác minh phạm vi miễn phí của từng tính năng, không chỉ license ở thư mục gốc.
4. Đánh giá tool được chọn bằng API, UI thật và hậu kiểm Oracle độc lập.
5. So sánh hiệu năng bằng workload, tài nguyên và phương pháp đo đã chốt.
6. Kết luận theo từng nhu cầu. Công khai thiếu hụt và điều kiện dùng production.

Không thể chứng minh đã tìm thấy mọi tool tồn tại.
Đầu ra phải ghi phạm vi tìm kiếm, ngày tìm, truy vấn và các giới hạn truy cập.

## Tài liệu cần đọc

Đọc [index](../README.md), [brief](../brief.md) và [ràng buộc mô hình sản phẩm](../product-model-constraint.md) trước.
Dùng [45 ca Oracle](ORACLE-POC.md) làm bộ tiêu chí gốc.
Đối chiếu [ODC và Bytebase đã POC](../BYTEBASE-ODC-COMPARISON.md) trước khi tạo ca mới.
[Ứng viên bổ sung](../ADDITIONAL-PLATFORMS-20261004.md) ghi phát hiện mới về CloudDM.

Chỉ mở source hoặc bằng chứng liên quan đến câu hỏi đang xử lý.
Các kết quả cũ không thay thế việc kiểm build mới. Giữ lịch sử và ghi riêng lần chạy mới.

## Phạm vi sản phẩm

| Nhóm | Vai trò trong nghiên cứu | Ví dụ để khởi đầu |
| --- | --- | --- |
| A: Database Change Management Platform | Nhóm lựa chọn chính. Có inventory, thay đổi, review, rollout và history. | Bytebase đối chứng; ODC, CloudDM, AccessFlow cần kiểm theo build. |
| B: SQL Governance Platform | Đánh giá quản trị SQL. Ghi rõ phần release còn thiếu. | Archery, SQLE/DMS, Yearning. |
| C: Migration Engine hoặc UI | Đối chứng về thực thi và state. Không xem là nền tảng tương đương nhóm A. | Flyway, Liquibase, Sqitch, Atlas và các UI tương ứng. |
| D: Công cụ truy cập hoặc sản phẩm thương mại | Đối chứng riêng cho quản lý DB, UX hoặc chi phí. | CloudBeaver, NineData và ứng viên phát hiện thêm. |

Đây là danh sách tìm kiếm, không phải xác nhận tương thích Oracle hoặc miễn phí.
Phân loại từng sản phẩm theo bằng chứng. Không suy ra nhóm chỉ từ tên hoặc README.
Kiểm fork và dự án ít được quảng bá. Không giới hạn tìm kiếm ở danh sách trên.

Tìm ít nhất hai vòng độc lập trên repo, tài liệu chính thức và danh mục dự án.
Khi hai vòng liên tiếp không có ứng viên A mới đủ căn cứ, chuyển sang POC shortlist.
Ghi rõ lý do dừng. Dự án bị archive vẫn được ghi, nhưng phải đánh giá khả năng duy trì.

## Ma trận tính năng cần đánh giá

P0 là điều kiện bắt buộc cho phạm vi sử dụng đề xuất.
P1 là tính năng quan trọng để so sánh. P2 là tính năng bổ sung.
Mã nhóm bên dưới bổ sung cho 45 ca gốc, không sửa tiêu chí gốc.

| Mã | Nhóm và ưu tiên | Tính năng cần kiểm | Bằng chứng đạt |
| --- | --- | --- | --- |
| F01 | License và deployment, P0 | Public source; quyền dùng và sửa; license image/plugin/driver; free gates; giới hạn user/DB/env; Docker/K8s; dependency SaaS | Pin commit/image; bảng edition theo tính năng; kiểm thao tác bị giới hạn. |
| F02 | Inventory và ownership, P0 | Project/application; instance; database/schema; environment; owner; tags; thêm/sửa/xóa qua API/UI | ID ổn định; discovery schema; mapping tài nguyên; quyền thao tác đúng. |
| F03 | Quản lý và truy cập DB, P0/P1 | SQL editor; object browser; DDL inspection; user/role/grant; quyền project/schema; kế thừa; expiry; read-only; che dữ liệu P2 | API denied và Oracle denied thực tế; phân biệt quyền platform với quyền DB. |
| F04 | Oracle SQL và PL/SQL, P0 | DDL/DML; procedure/function/package/trigger; block; delimiter; SQLPlus directive nếu công bố; TLS/TCPS; INVALID | Object, dữ liệu, ALL_OBJECTS và ALL_ERRORS khớp kết quả UI/API. |
| F05 | Migration state, P0 | Release/version; artifact hash; target ledger; central state; replay; checksum; retry; lock; partial commit | Hậu kiểm target độc lập; không che uncertain state hoặc lặp effect. |
| F06 | Review và approval, P0 | Lint/policy; blocking rule; approval gắn artifact/target; tách requester/approver/executor; admin override | Ca âm tính bị chặn; audit lưu đủ actor; đổi nội dung buộc duyệt lại. |
| F07 | Release và promotion, P0 | DEV→SIT→UAT→mockPROD; cùng artifact; prerequisite; dừng stage; batch; rollback/forward-fix | Không lên stage cao trước điều kiện; giữ hash; policy và trạng thái chính xác. |
| F08 | API và CI/CD, P1 | Onboarding DB; change/approve/execute/status; pagination; service account; webhook; dedup; CLI; GitLab/Jenkins | Job runner thật có reference và identity. API cục bộ chỉ là bằng chứng API. |
| F09 | History và audit, P0 | WHO/WHAT/WHERE/WHEN/HOW/RESULT; per-target logs; search/export; retention; secret handling | Artifact, actor và target truy vết được sau restart hoặc rotation đã kiểm. |
| F10 | Vận hành, P1 | Kiến trúc control plane/worker/metadata DB; backup/restore; HA; SSO; secret manager; metrics; nâng cấp | Sơ đồ đúng build; restore/reconciliation có bằng chứng; phân biệt native và custom. |
| F11 | Schema lifecycle, P2 | Diff; drift; baseline; import database đã có; schema history; policy-as-code | Thay đổi ngoài tool được nhận biết; mô tả phạm vi object được so sánh. |
| F12 | Hiệu năng và UX, P1 | API/UI latency; release overhead; throughput; CPU/RAM/storage; onboarding; số thao tác | Raw samples, cấu hình, lỗi và phương pháp đo có thể lặp lại. |

Quyền quản trị Oracle user/role không đồng nghĩa với RBAC của platform.
Nếu tính năng không hỗ trợ trên Oracle, ghi riêng. Không dùng kết quả MySQL để thay thế.
Giữ so sánh khả năng quản lý DB rộng hơn migration, nhưng không mở rộng thành benchmark engine database.

## Trạng thái và cách chấm

Mỗi ca có một trạng thái: PASS, PARTIAL, FAIL, BLOCKED hoặc NOT_RUN.
Mỗi nhận định có loại bằng chứng: DOC, SOURCE hoặc RUNTIME.
PASS cho tiêu chí runtime cần kết quả chạy thật. DOC hoặc SOURCE không đủ để đổi NOT_RUN thành PASS.

BLOCKED ghi nguyên nhân như license, quyền hoặc môi trường.
Không coi việc thiếu quyền thử là bằng chứng sản phẩm thiếu tính năng.
N/A chỉ dùng khi tiêu chí tùy chọn không thuộc scope đã chốt. Nêu lý do và mẫu số.

Trước khi xếp hạng, kiểm ba điều kiện riêng: free/open-source, platform fit và Oracle connectivity.
Thiếu ledger đích làm giảm migration fit. Không tự động xóa ứng viên khỏi nhóm platform.
Lỗi P0 chưa xử lý ngăn kết luận production-ready, dù tool có nhiều tính năng hoặc chạy nhanh.

| Trục so sánh | Trọng số đề xuất |
| --- | --- |
| Mô hình platform và quản lý DB | 25% |
| Oracle và độ đúng của migration | 30% |
| Governance và audit | 15% |
| API, Git và CI/CD | 10% |
| Vận hành và khả năng duy trì | 5% |
| Hiệu năng | 10% |
| UX và công sức thao tác | 5% |

Chấm các tiêu chí runtime: PASS=1, PARTIAL=0.5, FAIL=0.
BLOCKED và NOT_RUN không tạo điểm đã chứng minh; báo tỷ lệ coverage riêng.
Không xếp tool chỉ đọc source cao hơn tool đã POC chỉ vì chưa thấy lỗi.
Chỉ tổng hợp điểm giữa các ứng viên có coverage tương đương.
Hiệu năng chỉ nhận điểm khi benchmark đạt điều kiện so sánh; giữ raw metrics và lỗi bên cạnh điểm.
Chốt thang điểm hiệu năng trước chạy. Nếu chưa có SLA hợp lệ, báo metrics và để điểm tổng chưa hoàn tất.
Không đếm hai lần các ca khác nhau cùng chứng minh một tính năng.

## Phương pháp benchmark đề xuất

### Điều kiện so sánh

Pin edition, image digest, commit, Oracle version, driver, parser, worker count và cấu hình connection pool.
Mỗi tool dùng schema riêng với fixture có cùng nội dung và hash.
Dùng cùng host/network và cùng lớp tài nguyên khi phù hợp. Ghi mọi khác biệt kiến trúc bắt buộc.
Tính cả worker, metadata DB và proxy vào tài nguyên toàn nền tảng.

Oracle 26ai hiện có là baseline khả dụng, không đại diện Oracle 19c/21c.
Nếu cần quyết định cho 19c/21c, phải có lượt chạy riêng trên phiên bản đó.
Bốn schema trên một instance chỉ mô phỏng môi trường, không chứng minh cách ly vật lý.
Không tự thêm database engine khác vào benchmark bắt buộc.

Đánh giá native trước. Nếu có adapter hoặc wrapper, tạo cấu hình so sánh riêng.
Chạy các tool tuần tự trên database benchmark dùng chung. Không để agent khác tạo tải trong lượt đo.
Tách warm-up, startup và steady state. Luân phiên thứ tự tool giữa các đợt để giảm thiên lệch.

### Workload và số lần đo

| Mã | Workload đề xuất | Cách đo |
| --- | --- | --- |
| PERF-01 | API inventory/status và mở trang inventory UI | API: 3 warm-up, ít nhất 100 mẫu/lớp tải. UI: ít nhất 10 lượt, báo mẫu và khoảng dao động. |
| PERF-02 | Onboarding fixture 1/10/50 target logic | Chỉ chạy mức được edition cho phép. Ghi discovery time, số object và giới hạn. |
| PERF-03 | Release nhỏ: CREATE/ALTER, DML ít dòng, procedure/package/trigger | 3 warm-up và ít nhất 5 lần chạy trên fixture reset hoặc schema mới. |
| PERF-04 | Release nhiều statement: 10/100/1000; DML 1.000/10.000 dòng | Workload tăng dần, cùng hash, dừng khi đạt trần tài nguyên hoặc lỗi policy. |
| PERF-05 | Target độc lập, concurrency 1/2/4/8 | Đo completed jobs/minute, latency, errors và CPU/RAM. Chỉ tăng tải khi mức trước ổn định. |
| PERF-06 | Replay, duplicate request và checksum đổi | Đo thời gian ra quyết định cùng effect thực tế. Request bị chặn không tính là migration throughput. |
| PERF-07 | Restart và recovery có kiểm soát | Chỉ chạy trên deployment dành riêng. Đo thời gian phục hồi, trạng thái uncertain và thao tác cần thiết. |

Quy mô trên là điểm khởi đầu. Coordinator chốt fixture và trần tải sau khi kiểm quota thực tế.
Mọi tool nhận cùng revision workload. Thiếu hỗ trợ được ghi lại, không âm thầm thay SQL.
Reset nằm ngoài thời gian migration. Không reset schema có dữ liệu hoặc bằng chứng cần giữ.

### Metrics bắt buộc

- API latency p50/p95, cỡ mẫu, HTTP error rate và loại endpoint.
- Migration queue time, execution time và tổng thời gian từ request đến terminal state.
- Thời gian approval chờ người dùng tách khỏi execution time.
- Throughput của job thành công với hậu kiểm đúng, không chỉ số request được nhận.
- CPU, peak/steady RAM, restart, connection count và metadata/log growth.
- Lỗi, timeout, task báo success sai và số lần recovery thủ công.
- UX: thời gian và số bước hoàn tất cùng kịch bản, cùng vai trò và mức kinh nghiệm.

Không công bố p95 từ 5 hoặc 10 lượt migration/UI như một kết luận ổn định.
Với mẫu nhỏ, báo từng mẫu, median, min/max và phạm vi kết luận.
Nếu observer có đủ quyền và clock phù hợp, đo thời gian DB bằng tracing độc lập.
Nếu không, báo platform wall time và giới hạn phân rã. Không gán toàn bộ chênh lệch cho overhead.
CLI/client trực tiếp dùng làm đối chứng đường thực thi. Không xem nó là nền tảng thay thế.
Baseline có thể có driver khác; phải ghi rõ trước khi tính chênh lệch.

Hiệu năng database chịu ảnh hưởng plan/cache/network. Không suy ra tool tối ưu SQL chỉ từ thời gian chạy thấp hơn.
Lượt benchmark này không nhằm đo tốc độ chuyển toàn bộ dữ liệu giữa hai hệ database.

## Các task nhỏ và phụ thuộc

Tên output dưới đây là đích cần tạo trong lượt thực thi sau. Chưa có kết quả ở các đích này.

| Task | Việc cần làm | Phụ thuộc | Đầu ra và điều kiện hoàn tất |
| --- | --- | --- | --- |
| T00 | Kiểm workspace, quyền, credentials và target được phép dùng | Không | `evaluation/context.md`: scope, resource ceiling, gaps, không chứa secret. |
| T01 | Chốt feature matrix và mapping 45 ca cũ | T00 | `evaluation/criteria.csv`: ID, priority, expected, evidence, không đổi tiêu chí cũ. |
| T02 | Tìm rộng và đăng ký ứng viên | T01 | `evaluation/candidates.csv`, `evaluation/search-log.md`: category, repo, license, Oracle, keep/drop. |
| T03 | Review source, license, API và kiến trúc từng tool | T02 | `evaluation/candidates/<tool>/source-review.md`: pinned source và gaps. |
| T04 | Chọn shortlist và chốt workload | T03 | `evaluation/shortlist.md`, `evaluation/benchmark-spec.md`: lý do chọn và cách đo đóng băng. |
| T05 | Chuẩn bị deployment POC và fixture | T04; quyền thực thi phù hợp | `evaluation/candidates/<tool>/deployment.md`: namespace/schema riêng, versions và resource budget. |
| T06 | POC inventory, quản lý DB và quyền | T05 | F02/F03 có API, UI thật, positive/negative và Oracle hậu kiểm. |
| T07 | POC Oracle và migration state | T05 | SQL/REC có artifact hash, terminal state và target inspection. |
| T08 | POC approval, promotion, audit và CI/CD | T06/T07 | GOV có role enforcement; phân biệt local API với runner thật. |
| T09 | Benchmark tuần tự trên shortlist | T06–T08; đủ điều kiện đúng và đo | `evaluation/benchmarks/<tool>/`: samples CSV, metrics, config, errors. |
| T10 | Recovery, restore và HA có kiểm soát | T08; deployment và checkpoint riêng | Recovery report. Không đủ điều kiện thì BLOCKED/NOT_RUN, không suy đoán. |
| T11 | Review chéo và tổng hợp | T03, T06–T10 | Báo cáo từng tool, ma trận chung, coverage, chi phí và khuyến nghị. |
| T12 | Tích hợp tài liệu và portal bằng chứng | T11; phạm vi publish đã xác định | Cập nhật index/report, kiểm link, che secret; PR/merge/deploy theo quyền hiện có. |

Giới hạn POC sâu ban đầu ở 3–4 nền tảng, ngoài đối chứng đã có.
Ứng viên mới hoặc tool bị loại vẫn có hồ sơ lý do. Không deploy toàn bộ longlist.
Chạy lại Bytebase/ODC khi cần benchmark chung hoặc xác minh build/policy khác.
Không chạy lại toàn bộ ca đã có nếu điều kiện không đổi và không có câu hỏi mới.

## Cách phối hợp song song

Coordinator giữ criteria, shortlist, workload, credentials mapping và kết luận chung.
Worker chỉ ghi thư mục tool được giao. Reviewer kiểm nguồn và hậu kiểm trước khi tổng hợp.
Dùng tối đa 3 worker khi môi trường chỉ có 4 slot tính cả coordinator.

| Giai đoạn | Việc có thể song song | Việc phải điều phối tuần tự |
| --- | --- | --- |
| Tìm và đọc source | Agent theo từng tool hoặc nhóm ứng viên; review license độc lập | Chốt tiêu chí chung và danh mục tránh trùng. |
| POC chức năng | Deployment/schema/account riêng, không vượt resource budget | Đổi cấu hình chung, grants bootstrap và thao tác shared target. |
| Benchmark | Phân tích samples hoặc review kết quả đã chạy | Tải lên cùng instance/network; fixture reset; fault injection. |
| Tổng hợp | Review chéo report từng tool | Một coordinator ghi ma trận/index/report chung. |

Mỗi worker gửi: kết luận, bằng chứng, gaps, file đã đổi và phạm vi chưa chạy.
Không yêu cầu agent công khai chuỗi suy nghĩ nội bộ. Yêu cầu nhận định, nguồn và lập luận có thể kiểm tra.
Nếu không có multi-agent tool, thực hiện từng worker tuần tự và giữ nguyên artifact contract.

## Quy tắc bằng chứng và tác động ngoài

Mỗi case record gồm tool/build/edition, ID, actor, target, SQL hash, timestamps, expected và observed.
Lưu request/response đã che secret, Oracle hậu kiểm, ảnh UI và link source theo commit.
Case ID hoặc link evidence phải xuất hiện trong nhận định so sánh tương ứng.

Ảnh UI dùng Selenium/Playwright với trình duyệt thật, có thể chạy container.
Ảnh chính thức dùng làm tham khảo phải ghi nguồn. Không dùng ảnh giả để chứng minh thao tác đã thực hiện.
Không đưa credential, wallet, token, session cookie hoặc dữ liệu thật vào Git hay portal.
Không đọc và in toàn bộ `bytebase.cred` trong report hoặc prompt.

Ở lượt lập kế hoạch này không chạy test, deployment, migration hoặc benchmark.
Lượt thực thi kiểm quyền đã có trước mỗi tác động ngoài; không hỏi lại quyền vẫn hợp lệ.
Chỉ dùng schema và deployment POC đã được xác định. Không thao tác production.
Fault injection không làm gián đoạn dịch vụ dùng chung; cần target và quyền cụ thể.
Giữ bằng chứng cho người dùng xem lại. Cleanup chỉ áp dụng tài nguyên POC có ownership rõ và quyền phù hợp.

## Đầu ra quyết định

1. Danh mục rộng và bảng loại theo lý do, không tuyên bố bao phủ mọi tool.
2. Shortlist nền tảng miễn phí dùng được, tách nhóm thương mại và engine.
3. Báo cáo mỗi tool: kiến trúc, feature coverage, license gates, Oracle, runtime evidence và gaps.
4. Bảng benchmark có raw samples và điều kiện tương đương.
5. Khuyến nghị riêng cho quản lý DB, migration Oracle và governance miễn phí.
6. Ghi chi phí hạ tầng, license cần thiết và công sức adapter, không chỉ giá license repo.
7. Danh sách lỗi chặn production và các ca chưa chạy.

Không cần chọn một người thắng nếu không tool nào đạt P0.
Đề xuất thành phần ghép chỉ sau khi đã kiểm workflow native, và phải ghi chi phí vận hành bổ sung.
