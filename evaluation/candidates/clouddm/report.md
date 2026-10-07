# Đánh giá ứng viên CloudDM

**Cập nhật nghiên cứu sâu 2026-10-04:** đọc [source trace mới](../../research-round-2/clouddm/deep-source-review.md), [license/release](../../research-round-2/licensing/licensing-review.md) và [shortlist hiện tại](../../shortlist.md). Phần dưới giữ snapshot T03 đầu; kết luận mới được ghi riêng, runtime mới vẫn NOT_RUN.

Ngày rà soát: 2026-10-04. Đánh giá theo tiêu chí đóng băng trong [`criteria.csv`](../../criteria.csv). Báo cáo không thay expected hoặc gán runtime PASS. Trạng thái runtime của mọi tính năng CloudDM là **NOT_RUN**.

## Khuyến nghị

Giữ CloudDM trong shortlist nghiên cứu và chuyển sang POC giới hạn sau khi xử lý câu hỏi license và artifact. CloudDM có mức phù hợp tốt về governance và truy cập database. Sản phẩm có inventory, rule theo environment, approval workflow và Oracle JDBC connector tích hợp riêng. Source hiện tại chưa chứng minh migration Oracle đúng, replay an toàn ở target hoặc promotion theo thứ tự environment.

## Đối chiếu tiêu chí theo bằng chứng hiện có

| Phạm vi | Bằng chứng DOC/SOURCE | Đánh giá trước runtime |
| --- | --- | --- |
| Inventory và governance (F02/F03) | Tài liệu mô tả datasource, instance, environment, nhóm cluster, quyền role/function và quyền tài nguyên. Environment có rule bảo mật và ticket workflow. | **Có triển vọng về platform fit.** Mô hình project và ánh xạ target theo project như Bytebase chưa rõ. Cần kiểm tra quyền kế thừa, thời hạn, phạm vi target và hành động bị từ chối. |
| SQL review và approval (F06) | Tài liệu mô tả SQL audit và workflow. Source tạo approval ticket, target path, environment, SQL file attachment bị khóa và trạng thái `WAIT`. | **Có triển vọng về workflow.** Cần kiểm tra binding artifact/target, tách requester/approver/executor, approval bắt buộc và hành vi admin override qua ca âm tính runtime. |
| Oracle connectivity (MODEL-02/11) | Oracle plugin tạo kết nối JDBC và dựng URL SID/service/PDB/TNS. Source có nhánh tạo giao thức TCPS. | **Bằng chứng connector.** Chưa chạy kết nối, Autonomous TCPS, wallet, grants hoặc kiểm tra cross-schema. |
| Oracle migration (MODEL-05/12, SQL-01–12) | Có change workflow chung và Oracle JDBC connector. | **Khoảng trống lớn.** Bằng chứng đã rà chưa xác nhận parser Oracle PL/SQL, delimiter SQL*Plus, báo lỗi compile, stop policy ở cấp script hoặc reconciliation khi Oracle implicit commit. Không suy ra migration tương thích từ query/object support. |
| Change identity và audit (MODEL-03/04/10, F09) | Hướng dẫn GitLab mô tả input theo commit SHA và request dedup. Source kiểm tra delivery identifier và có approval record/attachment. | **Bằng chứng source một phần.** Cần exact SQL hash, record theo target, vai trò actor/thời gian, execution log và audit sau restart. Webhook dedup không phải migration ledger. |
| Replay, checksum, recovery, lock (MODEL-08/09/12, F05) | Source cache/dựng lại SQL file; tài liệu webhook mô tả dedup request. | **Khoảng trống.** Chưa có bằng chứng về target ledger, chặn checksum mismatch, replay an toàn, distributed lock, crash recovery hoặc xử lý partial DDL chưa rõ trạng thái. |
| Release/promotion (MODEL-07, F07) | Flow trỏ đến environment và database path; change workflow có thể chờ approval. | **Bằng chứng một phần.** Chưa có bằng chứng promotion DEV→SIT→UAT→PROD theo thứ tự với cùng artifact bất biến, prerequisite được enforce và resume có kiểm soát. |
| API và CI (F08) | Webhook controller có trong source; README mô tả Git Push, Web Hook và HttpCall. | **Chỉ DOC/SOURCE.** Cần xác minh runner/job identity, retry, request lặp/đồng thời, status API và quyền/license. |
| Vận hành và hiệu năng (F10/F12) | Tài liệu mô tả standalone và Console + Sidecar. | **Chưa đo.** Không build, deploy, đo tài nguyên, latency, throughput, backup/restore hoặc HA. |
| Schema lifecycle (F11) | Tài liệu mô tả quản lý database object và lấy/chuyển đổi DDL. | **Chưa xác minh drift/baseline.** Bằng chứng hiện có chưa xác nhận so sánh desired state hoặc import/reconciliation lịch sử an toàn. |

## License và gate truy cập sản phẩm

Repository khai báo Apache-2.0 cho các tệp thuộc phạm vi license đó. Điều này chưa giải quyết license của release image, third-party components, plugin tùy chọn hoặc Oracle JDBC driver. Cần rà release và image cụ thể. Yêu cầu SBOM/notices và xác minh quyền phân phối driver cùng cách tải driver khi chạy.

Kết quả pricing cache cũ được cho là ghi Community giới hạn 10 instance và 5 tài khoản. Bản trả về trực tiếp đã lưu lại cho biết CloudDM đã mở mã nguồn và không nêu giới hạn số lượng. Kết quả search cache không được giữ thành nguồn chính, còn nội dung trang trực tiếp có thể chưa đầy đủ. Vì vậy, giới hạn và feature entitlement đều chưa rõ. Nếu POC cần nhiều user hoặc instance, cần xác nhận điều khoản hoặc kiểm tra license implementation của đúng release. Không tính giới hạn không được công bố là không tồn tại.

## Điều kiện và việc cần làm trong POC

1. **Gate license:** Chốt version và image digest. Rà source/release notices, SBOM, MySQL cùng dependency khác, ranh giới plugin, license/cách phân phối Oracle JDBC và mọi entitlement check. Xác nhận user, instance, approval, CI trigger, SSO hoặc Sidecar có cần license trả phí không.
2. **Gate kiến trúc:** Ghi lại topology standalone hoặc Console + Sidecar, nơi lưu metadata, quy trình backup/recovery và việc tải driver lúc chạy. Lưu version và image digest chính xác.
3. **Kết nối Oracle:** Trong môi trường cô lập, cấu hình Oracle 26ai Autonomous với trust material TCPS được phê duyệt và credential test quyền tối thiểu. Kiểm tra kết nối, reconnect và đọc metadata. Không đưa credential vào log hoặc báo cáo.
4. **Ma trận script Oracle:** Qua cả UI lẫn change/API path được hỗ trợ, chạy SQL-01–12 và ca recovery đã đóng băng. Bao gồm CREATE/ALTER/DML, procedure/function/package/trigger, anonymous block, slash delimiter, SQL*Plus directive, q-quoting, PL/SQL INVALID và compile diagnostic.
5. **Ledger/replay:** So artifact và checksum chính xác tại approval và execution. Chạy lần đầu, replay nội dung không đổi, sửa nội dung dưới cùng release identity, gây lỗi giữa script, restart sau target commit và retry sau reconciliation. Kiểm tra độc lập ledger tại target và trạng thái trung tâm.
6. **Approval/authorization:** Kiểm tra chặn self-approval, approval bắt buộc, sửa artifact hoặc target sau approval, admin override, role/resource scope, expiry, kế thừa project/environment và chặn Oracle cross-schema. Ghi riêng requester, approver, executor, database principal, target và timestamp.
7. **Promotion:** Đưa cùng artifact đã duyệt qua DEV→SIT→UAT→PROD. Kiểm tra artifact identity, prerequisite, stop/resume, cô lập lỗi và recovery. Xác định hành vi native hay orchestration tùy chỉnh.
8. **API/CI:** Kiểm tra GitLab hoặc Jenkins bằng identity riêng có quyền tối thiểu. Thu request ID, commit SHA, exact SQL hash, status reference, retry, request trùng đồng thời và hành vi authorization.

Đây là các việc POC trong tương lai. Lượt rà soát này không deploy CloudDM, chạy test, khởi động service, thực thi SQL, đọc credential hoặc kết nối database đích.
