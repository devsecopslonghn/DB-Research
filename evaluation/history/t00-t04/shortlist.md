# Shortlist T04

**Giữ bốn ứng viên để POC tiếp: ODC, CloudDM, AccessFlow và Archery theo phạm vi riêng.**
Chưa xác minh được nền tảng OSS miễn phí nào đạt toàn bộ yêu cầu migration Oracle và governance.
Đây là shortlist nghiên cứu có điều kiện. Không phải danh sách đã nghiệm thu production.
Ngày: 2026-10-04. Criteria giữ nguyên tại [criteria.csv](criteria.csv).

| Ứng viên | Nhóm và lý do giữ | License/free gate | Giới hạn Oracle và quyết định tiếp |
| --- | --- | --- | --- |
| [ODC](candidates/odc/report.md) | A. Project, estate, environment, approval và native batch model. Có API/UI Oracle 26ai lịch sử. | Apache-2.0 backend/frontend. MetaDB, Oracle driver, image và wrapper cần phạm vi license riêng. | Runtime SQL-11, REC-02/08/10, GOV-03 FAIL. Native batch chưa nghiệm thu; TCPS lịch sử có wrapper. POC sửa P0, không benchmark thành công production. |
| [CloudDM](candidates/clouddm/report.md) | A-candidate. Inventory/env/resource governance, workflow approval, CI/webhook và connector Oracle tích hợp. | Apache-2.0 source. Free limits/image/plugin/driver chưa chốt. Cache 10 instance/5 account không xác lập giới hạn hiện tại. | Chưa chứng minh project ownership tương đương Bytebase, parser PL/SQL, compile gate, target ledger, replay và promotion. Ưu tiên POC mới sau license/artifact gate. Runtime NOT_RUN. |
| [AccessFlow](candidates/accessflow/report.md) | A-partial. Native schema change set, central checksum, environment ladder, promotion và approval plan. | Apache-2.0 source; chưa thấy paid gate ở đường đã rà. Driver tải riêng và image/dependency chưa audit đủ. | Schema-change gate từ chối SELECT/INSERT/UPDATE/DELETE. OTHER được phép, không là allow-list DDL. Raw query path khác release path. PL/SQL/TCPS/target ledger chưa chứng minh. POC native trước, không thay release bằng query path. Runtime NOT_RUN. |
| [Archery](candidates/archery/report.md) | B. SQL ticket governance, inventory, approval và Oracle executor. Giữ cho nhu cầu quản trị SQL. | Apache-2.0 source; `oracledb`, Instant Client, external review tools và image có license riêng. | Source có per-statement commit và named PL/SQL INVALID check. Parser/ALL_ERRORS/release result còn cần kiểm. Không có ledger/promotion native được chứng minh. Không coi là ứng viên thay toàn bộ platform A. Runtime NOT_RUN. |

Không xếp bốn tool theo điểm tổng. Coverage runtime khác nhau.
Không suy ra source-only tool tốt hơn ODC vì chưa chạy để thấy lỗi.
ODC là đối chứng OSS đã chạy. CloudDM và AccessFlow là hai POC mới chính.
Archery chỉ POC sâu phần governance/Oracle executor nếu use case đó còn cần.

## Đối chứng tách riêng

[Bytebase 3.22.1/FREE](candidates/bytebase/report.md) giữ vai trò đối chứng mô hình và native version/replay.
FREE có 10 instance/20 user. Approval/audit cần edition phù hợp; source chỉ MIT subset.
SQL-11, strict checksum và early promotion còn FAIL. P04 SQL Review enforcement cũng FAIL ngoài 45 ca.
Mua license chưa chứng minh các lỗi correctness được sửa.
Không đưa Bytebase FREE vào nhóm OSS miễn phí đạt governance bắt buộc.

Flyway Community source, Liquibase 4.33.0 source và Sqitch là đối chứng engine.
Chúng có đường ledger Oracle trong bằng chứng source cũ, nhưng không là platform đơn lẻ.
Flyway SQLPlus đầy đủ có paid boundary; Liquibase 5.x FSL không strict OSS.
Sqitch dùng Oracle SQLPlus client với điều kiện dependency riêng.
Không đề xuất ghép engine trước khi kiểm workflow native và tính chi phí vận hành adapter.

## Ma trận knockout cho nhu cầu hoàn chỉnh

| Tool | Free OSS dùng được | Oracle migration đã nghiệm thu | State/recovery đáng tin cậy | Central platform | Kết quả |
| --- | --- | --- | --- | --- | --- |
| ODC | Source YES, image dependency PARTIAL | PARTIAL, Oracle 26ai lịch sử | NO cho các ca replay/checksum/dedup đã FAIL | YES | Giữ platform POC. Chưa đạt hard requirements. |
| CloudDM | Source YES, runtime/free distribution UNKNOWN | UNKNOWN, SOURCE connector | UNKNOWN | SOURCE YES, project model PARTIAL | POC có điều kiện. Chưa đạt hard requirements. |
| AccessFlow | Source YES, full distribution PARTIAL | PARTIAL SOURCE, DML gate/gap | UNKNOWN target ledger/recovery | SOURCE YES, project model PARTIAL | POC có điều kiện. Chưa đạt hard requirements. |
| Archery | Source YES, full distribution PARTIAL | PARTIAL SOURCE | UNKNOWN ledger/recovery | YES SQL governance, không full A | POC use case governance. Không đáp án migration hoàn chỉnh. |
| Bytebase FREE | PARTIAL MIT subset/edition limits | PARTIAL, Oracle 26ai lịch sử | Central replay PASS; checksum FAIL, crash chưa chạy | YES | Đối chứng. Approval/audit BLOCKED và correctness P0 FAIL. |

YES trong bảng này cần đọc cùng loại nguồn. SOURCE YES không là runtime PASS.
Target ledger chưa đủ căn cứ không tự loại platform fit. Nó vẫn chặn tuyên bố đạt yêu cầu state.
REC-05/06/07/11/12 và GOV-06/07 chưa chạy ở đối chứng lịch sử.

## Task POC tiếp theo

| Thứ tự | Task và target | Acceptance giữ nguyên | Điều kiện trước thực thi |
| --- | --- | --- | --- |
| 1 | T05 cho CloudDM và AccessFlow; ODC/Bytebase pin lại khi cần | Edition/image/driver/parser, topology, namespace/schema riêng và component license được ghi | User xác định lượt triển khai, target và quota. Không dùng credential hoặc schema lịch sử để thử tải. |
| 2 | T06 inventory/quyền cho hai POC mới | F02/F03, DB user/role/grant khác platform RBAC; positive/negative, inheritance/expiry và Oracle denial | Bootstrap/executor/requester/approver/observer riêng, least privilege, browser thật |
| 3 | T07 Oracle correctness native | SQL-01..12 và REC-01..04/08..10; script nguyên hash, ALL_OBJECTS/ALL_ERRORS và target history | Compile gate, DML release capability và trạng thái partial/uncertain phải rõ |
| 4 | T08 governance/promotion/API | Approval binding, requester separation, same artifact và enforced DEV→SIT→UAT→mockPROD | Real GitLab/Jenkins job identity khác API/CLI cục bộ; license hợp lệ |
| 5 | T07/T08 tái hiện P0 trên ODC/Bytebase build dự kiến | Không đổi FAIL cũ hoặc expected. Ghi kết quả mới riêng | Edition có license phù hợp; source/image/policy pin |
| 6 | Archery T06–T08 giới hạn governance/Oracle executor | PL/SQL splitting, INVALID diagnosis, reviewed SQL binding và partial execution | Không đổi tiêu chí để ticket workflow thành native versioned release |
| 7 | T09 benchmark chung | [benchmark-spec.md](benchmark-spec.md), chỉ throughput có hậu kiểm đúng | T06–T08 đủ điều kiện, quota/target được kiểm, lịch shared Oracle tuần tự |
| 8 | T10 controlled recovery/restore/HA | REC/GOV chưa chạy, commit/checkpoint/fencing và reconciliation | Deployment riêng, quyền fault injection cụ thể; không kill dịch vụ chung |

Mỗi lượt mới cần request/response sanitized, actor, target, SQL SHA-256, timestamps và Oracle hậu kiểm.
T09 không thay thế T10. Tốc độ không bù correctness.
Oracle 19c/21c cần target riêng và các lượt riêng nếu quyết định áp dụng cho các phiên bản đó.

## Điều kiện benchmark và phần chưa kiểm

Workload `oracle-common-v1` đã có SQL bytes/hash, warm-up, số mẫu và expected hậu kiểm.
Ceiling đề xuất: 4 vCPU/8 GiB/20 GiB toàn platform; tối đa 16 session Oracle.
Các giá trị đó chưa là quota môi trường đã kiểm. T05 phải xác nhận trước T09.
Pool, worker, image digest, driver và Oracle full version phải pin trước đo.
Tách queue/execution/approval, tính metadata DB/worker/proxy và chỉ đo shared Oracle tuần tự.
Không công bố p95 ổn định từ vài lượt UI/migration. Không có SLA thì chưa chấm điểm hiệu năng.
Lượt này không deployment, test, service, SQL, benchmark hoặc kết nối target.
