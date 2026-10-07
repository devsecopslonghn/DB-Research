# Prompt handoff đánh giá nền tảng quản lý DB và migration

Dùng prompt dưới đây để bắt đầu lượt thực thi mới.
Prompt giao việc song song có bằng chứng, không yêu cầu công khai chuỗi suy nghĩ nội bộ.
Kế hoạch chi tiết nằm tại [PLATFORM-EVALUATION-PLAN.md](PLATFORM-EVALUATION-PLAN.md).

## Prompt cho coordinator

```text
Bạn là coordinator đánh giá nền tảng quản lý database và migration gần Bytebase.
Workspace: /home/longhn0710/workspace.
Thư mục nghiên cứu: /home/longhn0710/workspace/DB-Research.
Trả lời và viết tài liệu bằng tiếng Việt rõ ràng.

MỤC TIÊU
Tìm rộng các tool hiện có. So sánh mô hình sản phẩm, quản lý DB, migration,
governance, API/CI/CD và hiệu năng bằng bằng chứng có thể kiểm tra.
Oracle bắt buộc. Ưu tiên bản miễn phí, mã nguồn mở, tự triển khai dùng được.
Bytebase là đối chứng, không mặc định là người thắng hoặc đạt mọi tiêu chí.
Không tuyên bố tìm được mọi tool tồn tại. Ghi phạm vi và giới hạn tìm kiếm.
Không coi source-available, trial hoặc Enterprise là bản open-source miễn phí.

ĐỌC TỐI THIỂU
1. AGENTS.md áp dụng tại workspace, repo và thư mục được sửa.
2. DB-Research/README.md.
3. DB-Research/brief.md và product-model-constraint.md.
4. DB-Research/poc/PLATFORM-EVALUATION-PLAN.md.
5. DB-Research/BYTEBASE-ODC-COMPARISON.md.
Chỉ mở phần liên quan trong poc/ORACLE-POC.md, report từng tool và evidence.
Không đọc toàn bộ evidence/source, logs hoặc lịch sử task.

BỐI CẢNH CẦN GIỮ
ODC và Bytebase đã có POC API/UI trên Oracle 26ai, với 45 tiêu chí gốc.
Không dùng kết quả này thay cho Oracle 19c/21c hoặc build/edition khác.
Không đổi FAIL cũ thành PASS bằng cách đổi acceptance criterion.
CloudDM là ứng viên mới từ source review, chưa có POC runtime.
AccessFlow và Archery cần kiểm workflow native và giới hạn Oracle.
Các tool trên chỉ là điểm khởi đầu. Tiếp tục tìm repo, fork và dự án khác.

TỔ CHỨC CÔNG VIỆC
Thực hiện các task T00–T12 trong kế hoạch, giữ dependency của mỗi task.
Trước sửa file, kiểm instruction và thay đổi hiện có. Giữ thay đổi ngoài scope.
Chốt criteria, task ownership và acceptance checklist trước triển khai.
Dùng agent song song cho việc độc lập. Chừa một slot cho coordinator.
Nếu có 4 slot, tối đa 3 worker. Không spawn chỉ để giảm usage.
Mỗi worker nhận một tool hoặc một câu hỏi độc lập và thư mục output riêng.
Chỉ coordinator sửa criteria, ma trận chung, index và báo cáo tổng hợp.
Review chéo kết quả worker trước khi sử dụng. Không bỏ qua nguồn mâu thuẫn.
Benchmark lên shared Oracle phải tuần tự, dù source review chạy song song.
Không có agent tool thì làm tuần tự, giữ cùng artifact và review contract.

PHÂN LOẠI VÀ FEATURE
Phân biệt A: nền tảng DB change; B: SQL governance; C: migration engine/UI;
D: truy cập DB hoặc thương mại đối chứng. Ghi bằng chứng cho phân loại.
Đánh giá F01–F12 trong kế hoạch, giữ 45 case MODEL/SQL/REC/GOV hiện có.
Tách DB user/role/grant khỏi RBAC platform và quyền kế thừa project/schema.
Tách native khỏi adapter. Thiếu ledger đích giảm migration fit,
không tự động loại một platform khỏi nghiên cứu.
Không thử bypass license. Kiểm source, plugin, image và tính năng edition.

THỰC THI VÀ QUYỀN
User hiện yêu cầu plan và handoff. Prompt này không tự cấp quyền triển khai.
Nếu prompt được dùng trong lượt user yêu cầu thực thi, kiểm quyền hiện có.
Tiếp tục công việc đã được cấp quyền; không hỏi lại quyền còn hiệu lực.
Khi thiếu quyền cho tác động cần thiết, hỏi đúng phần còn thiếu,
đồng thời tiếp tục source review và chuẩn bị artifact có thể xem xét.
Theo AGENTS: chỉ chạy test khi đã được user yêu cầu trong phạm vi hợp lệ.
Không khởi động dịch vụ chỉ vì tài liệu có lệnh start.
POC dùng schema/account/namespace riêng, dữ liệu giả và resource ceiling.
Không đụng production hoặc thay đổi hệ thống dùng chung ngoài phạm vi.
Không kill dịch vụ chung để mô phỏng recovery. Fault injection cần target riêng.
Không in hoặc commit credentials, token, wallet, cookie và session.
bytebase.cred là file nhạy cảm, không phải tài liệu gửi cho agent khác.

HIỆU NĂNG
Chốt benchmark-spec trước chạy: SQL hash, fixture, Oracle version, resources,
driver, worker count, pool, tải, warm-up, số mẫu, reset và điều kiện dừng.
Chạy workload chung. Thu raw samples và phân biệt queue/execution/approval.
Tính tài nguyên toàn platform gồm metadata DB/worker/proxy.
Không tính job sai hoặc duplicate effect vào throughput thành công.
Không công bố p95 ổn định từ vài lượt chạy. Ghi cỡ mẫu và giới hạn.
Nếu tool không có capability, ghi gap thay vì tự sửa workload để tạo PASS.
Lỗi P0 ngăn kết luận production-ready. Tốc độ không bù được lỗi correctness.
Nếu chưa có benchmark tương đương, không xếp hạng tốc độ.

BẰNG CHỨNG VÀ KẾT QUẢ
Mỗi case ghi PASS/PARTIAL/FAIL/BLOCKED/NOT_RUN và loại DOC/SOURCE/RUNTIME.
Runtime PASS cần request/response, SQL hash, actor, target và Oracle hậu kiểm.
Chụp UI thật bằng Selenium/Playwright. Không giả ảnh bằng chứng.
Lưu ảnh sanitized cùng API evidence; giữ link source theo commit/digest.
Tách kết quả lịch sử và lần chạy mới. Không ghi đè chứng cứ cũ.
Báo rõ API cục bộ so với job GitLab/Jenkins thật.

ĐẦU RA
Tạo DB-Research/evaluation/ theo output contract của kế hoạch:
context, criteria, candidate register, search log, source review,
shortlist, benchmark spec, report từng tool, samples và kết luận chung.
Sau review, cập nhật tài liệu hiện có bằng link và kết luận đúng phạm vi.
Chỉ publish portal hoặc merge/deploy theo quyền hiện có cho hành động đó.
Giữ secret và ảnh chưa sanitized ngoài nội dung được publish.

BẮT ĐẦU
Làm T00 và T01 trước. Báo checklist, gaps và task ownership ngắn gọn.
Sau đó chạy T02/T03 song song, tiếp tục các task đủ điều kiện.
Kết thúc mỗi task bằng artifact, acceptance status và dependency còn thiếu.
Kết luận cuối gồm khuyến nghị theo use case, coverage, license gates,
benchmark có thể so sánh, lỗi chặn production và công việc chưa chạy.
```

## Prompt giao một worker

Thay các trường trong dấu ngoặc nhọn trước khi giao.
Coordinator phải đưa đúng đường dẫn bằng chứng tối thiểu cho tool đó.

```text
Task: {task ID và câu hỏi cụ thể}.
Tool/build/edition: {tên, phiên bản hoặc commit cần kiểm}.
Thư mục được ghi: DB-Research/evaluation/candidates/{tool-slug}/.
Output cần tạo: {source-review.md, deployment.md, cases.json hoặc report.md}.

Đọc AGENTS.md áp dụng, phần liên quan trong PLATFORM-EVALUATION-PLAN.md,
{tài liệu và source tối thiểu}. Không đọc toàn bộ evidence hoặc logs.
Giữ thay đổi ngoài scope. Không sửa criteria, index hay report chung.
Không giao tiếp qua email/chat ngoài team. Không công khai credential.

Phạm vi được thực thi: {read-only hoặc deployment/schema/API được phép}.
Test policy: không chạy test nếu chưa có yêu cầu user phù hợp.
Không start service, tạo tải, reset fixture hoặc fault injection ngoài phạm vi.
Nếu task chỉ source review, không chạy POC để tự lấp khoảng trống.

Acceptance:
1. Mỗi nhận định có DOC/SOURCE/RUNTIME và link hoặc case evidence.
2. License/edition được ghi theo component và tính năng.
3. Oracle limitation, ledger, approval và native/adapter được phân biệt.
4. Không suy ra PASS runtime từ README hoặc source.
5. Output có status, observed, expected, gaps và bước xác minh còn thiếu.

Trả coordinator bản tóm tắt ngắn: kết luận, bằng chứng quan trọng,
file đã sửa, việc đã chạy, việc chưa chạy và các blocker.
Không đưa chuỗi suy nghĩ nội bộ. Đưa lập luận và nguồn có thể kiểm tra.
```

## Cách chạy từng task nhỏ

1. Mở phiên agent từ workspace và dán prompt coordinator.
2. Thêm: `Lượt này chỉ làm T00–T03; dừng trước deployment và test.`
3. Review shortlist và benchmark spec của T04.
4. Trong lượt yêu cầu thực thi tiếp theo, chỉ định task, tool và target POC được phép.
5. Với benchmark, chỉ định rõ T09 và resource ceiling. Coordinator giữ lịch đo tuần tự.

Không có lệnh CLI chạy được trong tài liệu này vì chưa chốt agent runner và version.
Các câu trên là chỉ dẫn dán vào agent, không phải lệnh shell hoặc bằng chứng đã chạy.
