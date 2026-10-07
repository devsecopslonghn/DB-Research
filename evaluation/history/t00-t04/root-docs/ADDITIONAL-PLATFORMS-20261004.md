# Ứng viên mã nguồn mở gần Bytebase

## Đánh giá tiếp theo T03/T04

[CloudDM review mới](evaluation/candidates/clouddm/source-review.md) kiểm connector tích hợp và các khoảng trống source.
[AccessFlow](evaluation/candidates/accessflow/source-review.md) và [Archery](evaluation/candidates/archery/source-review.md) có review current source pin và review chéo.
[Shortlist](evaluation/shortlist.md) giữ điều kiện license/image và Oracle native workflow trước POC.
Lượt T00–T04 chỉ đọc nguồn và ghi artifact. Không có runtime hoặc benchmark mới.

Ngày kiểm tra: 2026-10-04.

## Kết luận

CloudDM là ứng viên mới đáng POC tiếp. AccessFlow và Archery vẫn có giá trị trong shortlist.
Chưa có bằng chứng runtime để công nhận ba nền tảng này thay thế Bytebase trên Oracle.

Phạm vi yêu cầu: miễn phí, mã nguồn mở, tự triển khai, quản lý database tập trung và hỗ trợ Oracle.
Các tiêu chí bổ sung gồm phê duyệt, phân quyền, audit, CI/CD và quản lý trạng thái triển khai.

## So sánh

| Nền tảng | License repo | Phần gần Bytebase | Oracle và phần chưa xác minh |
| --- | --- | --- | --- |
| CloudDM | Apache-2.0 | Inventory, môi trường, RBAC, SQL audit, phiếu phê duyệt và luồng CI/CD qua Git/webhook/HTTP | Có plugin Oracle và mã tạo kết nối JDBC. Chưa POC PL/SQL, Autonomous TCPS, promotion, checksum và lịch sử tại database đích. |
| AccessFlow | Apache-2.0 | Quyền truy cập, phê duyệt, audit, deployment gate và schema change set qua các môi trường | Tài liệu công bố Oracle. Luồng schema change set từ chối SELECT/INSERT/UPDATE/DELETE. Chưa chứng minh chạy đầy đủ release Oracle có PL/SQL và DML. |
| Archery | Apache-2.0 | Quản lý instance, SQL ticket, review, thực thi và quyền truy vấn | Ma trận chính thức có Oracle. Chưa chứng minh release bất biến, promotion và lịch sử phiên bản tại database đích. |

Mức độ phù hợp trong bảng là đánh giá từ tài liệu và mã nguồn. Đây không phải kết quả POC.
CloudDM quản lý tài nguyên theo môi trường và cluster. Chưa xác nhận mô hình project tương đương Bytebase.

## Bằng chứng mới: CloudDM

Repository: <https://github.com/ClouGence/open-cdm>.

Commit đã kiểm tra: `a9f16e78b8288c9a4158ee9df4378ee16b80021e`.

1. README công bố Apache-2.0, Oracle, RBAC, phiếu phê duyệt và CI/CD.
2. Repo có backend Java, frontend và plugin Oracle. Đây là mã nền tảng, không chỉ tài liệu.
3. `OracleDsFactory.java` tạo kết nối bằng Oracle JDBC driver.
4. `DmChangeFlowWebhookController.java` cung cấp route `/cicd/webhook`.
5. `ChangeActionForApproval.java` tạo approval ticket và chuyển change sang trạng thái `WAIT`.
6. Hướng dẫn GitLab mô tả commit SHA cố định và dedup theo request ID hoặc flow cùng commit SHA.
7. Hướng dẫn triển khai có Docker, gói cài đặt và Kubernetes.

Mục 6 là hành vi được tài liệu mô tả. Chưa chạy kiểm chứng dedup.
Không suy ra dedup webhook là ledger hoặc chống chạy lại tại database đích.

Mã nguồn được lưu có chọn lọc trong [thư mục bằng chứng](evidence/additional-platform-20261004/).
[Manifest](evidence/additional-platform-20261004/clouddm-source-manifest.json) ghi URL theo commit và SHA-256 của từng tệp.
[Metadata](evidence/additional-platform-20261004/clouddm-metadata.json) ghi thông tin repository tại thời điểm truy vấn.

Repo công khai được tạo ngày 2026-05-12. Ngày tạo repo không chứng minh tuổi hoặc độ trưởng thành của sản phẩm.

## Khoảng trống về bản miễn phí

Kết quả web đã lưu trong bộ nhớ đệm của trang pricing ghi Community giới hạn 10 instance và 5 tài khoản.
Truy vấn HTTP trực tiếp ngày 2026-10-04 tới cùng URL trả trang chủ với thông báo đã mở toàn bộ mã nguồn.
Vì vậy, không dùng bảng pricing cũ để kết luận giới hạn của bản hiện tại.

[HTML nhận trực tiếp](evidence/additional-platform-20261004/clouddm-pricing.html) và
[nội dung văn bản](evidence/additional-platform-20261004/clouddm-pricing.txt) được lưu để đối chiếu.

Apache-2.0 áp dụng cho mã repo đã kiểm tra. Chưa xác minh giới hạn của image phát hành hoặc mọi dependency.

## Tiêu chí POC tiếp theo

1. Kết nối Oracle Autonomous qua TCPS bằng cấu hình tin cậy phù hợp.
2. Chạy DDL, DML, procedure, function, package và trigger qua API cùng UI.
3. Kiểm tra công cụ báo lỗi khi đối tượng PL/SQL có trạng thái `INVALID`.
4. Kiểm tra requester không tự duyệt hoặc bỏ qua approval bắt buộc.
5. Kiểm tra cùng release qua DEV, SIT, UAT và PROD.
6. Kiểm tra chạy lại, thay đổi checksum, lỗi giữa script và trạng thái sau restart.
7. Xác định lịch sử nằm ở metadata trung tâm hay database đích.
8. Kiểm tra giới hạn người dùng, instance và các chức năng cần license trong bản triển khai.

Lượt nghiên cứu này không triển khai dịch vụ, chạy test hoặc sửa database.

## Nguồn chính thức

- [CloudDM README theo commit](https://github.com/ClouGence/open-cdm/blob/a9f16e78b8288c9a4158ee9df4378ee16b80021e/README.md).
- [CloudDM license theo commit](https://github.com/ClouGence/open-cdm/blob/a9f16e78b8288c9a4158ee9df4378ee16b80021e/LICENSE.txt).
- [CloudDM GitLab CI/CD theo commit](https://github.com/ClouGence/open-cdm/blob/a9f16e78b8288c9a4158ee9df4378ee16b80021e/docs/guides/gitlab-cicd.en.md).
- [CloudDM deployment guide](https://github.com/ClouGence/open-cdm/blob/main/docs/guides/deployment.en.md).
- [CloudDM GitLab guide](https://www.cdmgr.com/docs/integrations/devops/devops_cicd_gitlab/).
- [CloudDM pricing URL có nội dung khác nhau giữa cache và HTTP trực tiếp](https://www.cdmgr.com/en/pricing/).
- [AccessFlow repository và giới hạn schema change set](https://github.com/bablsoft/accessflow).
- [Archery repository và ma trận Oracle](https://github.com/hhyo/Archery).
