# Đánh giá ứng viên AccessFlow

**Cập nhật nghiên cứu sâu 2026-10-04:** đọc [source trace mới](../../research-round-2/coordinator/oracle-governance-source.md), [license/release](../../research-round-2/licensing/licensing-review.md) và [shortlist hiện tại](../../shortlist.md). Phần dưới giữ snapshot T03 đầu; kết luận mới được ghi riêng, runtime mới vẫn NOT_RUN.

Trạng thái: tiếp tục nghiên cứu platform fit; runtime chưa kiểm. Commit `55c209a4d9e4ba09a6c089f90e68a8b16b3f2133` khớp remote HEAD ngày 2026-10-04.

AccessFlow có các thành phần bản địa đáng chú ý cho quản lý thay đổi: schema change set, promotion record, environment ladder, approval qua request group và checksum tập trung. Đây là bằng chứng DOC/SOURCE, không phải xếp hạng tổng thể hay chấp nhận runtime. Các đặc tính này đáp ứng một phần tiêu chí native change và promotion, nhưng không tự chứng minh tất cả P0.

Cổng schema change set từ chối SELECT/INSERT/UPDATE/DELETE sau khi parser phân loại. Đây không phải allow-list chỉ cho schema DDL: mã nhận cả `OTHER`, và tài liệu nói MERGE, UPSERT, CALL cùng một số câu session có thể qua bước authoring. Các SQL query đi qua proxy là luồng governance riêng; không nên nhầm việc chặn DML của schema change set với chính sách truy cập raw SQL tổng quát. Oracle connector có driver riêng, nhưng PL/SQL body, SQLPlus, compile INVALID và tương thích Oracle 19c/21c/26ai chưa được xác minh.

Promotion có checksum SHA-256 và approval/environment ladder trong metadata trung tâm. Mã kiểm tra rung trước phải APPLIED và quyền `can_ddl`. Khi environment bắt buộc review, service yêu cầu datasource có human approval plan. Số lượng approver được lấy từ datasource plan, không lấy override trên environment. Chưa có bằng chứng ledger migration trong Oracle target hoặc replay protection ở database đích.

License gate: repository Apache-2.0; chưa thấy cổng trả phí trong luồng change-set đã rà. Oracle dùng `ojdbc11` resolve riêng; cần kiểm điều khoản driver, dependency, image phát hành và dịch vụ AI/secret tùy chọn. Không suy license image từ license repo.

Task POC kế tiếp nên ưu tiên: kết nối Oracle mục tiêu và TCPS nếu cần; kiểm DDL/DML classification, MERGE/CALL, PL/SQL units, slash delimiter và compile INVALID; xác minh chính xác artifact/checksum/target sau approval; kiểm requester-approver separation và fail-closed; chạy một release qua DEV/SIT/UAT/PROD; kiểm retry/partial failure và ledger tại target. Trước benchmark, khóa SQL hash, fixture, Oracle build, tài nguyên, driver/pool, concurrency, warm-up, số mẫu, reset và điều kiện dừng. Đo riêng queue/approval với thời gian SQL; tính cả proxy, worker và metadata DB.

Runtime: `NOT_RUN`. Không chạy test, deploy, khởi động service, SQL, credential hoặc thao tác DB. Chi tiết source và giới hạn tại [source-review.md](source-review.md). Review chéo CloudDM tại [cross-review.md](cross-review.md).
