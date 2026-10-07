# Bytebase: source, license và đối chứng lịch sử

Ngày: 2026-10-04. Category A, đối chứng. Runtime mới: NOT_RUN.
Runtime lịch sử: 3.22.1/FREE, commit `a85f6cb4195299995e8554303550d672d5093e1d`, Oracle 26ai 23.26.4.1.0.
Đã đọc LICENSE, LICENSE.enterprise và plan.yaml theo đúng runtime commit qua raw GitHub.
[Manifest](source-manifest.json) lưu URL và SHA-256. Không build hoặc thực thi code đó.

| Nhận định | Loại | Bằng chứng và giới hạn |
| --- | --- | --- |
| Root license chỉ cấp MIT cho phần source được bao phủ | SOURCE | [LICENSE:1–25](https://github.com/bytebase/bytebase/blob/a85f6cb4195299995e8554303550d672d5093e1d/LICENSE#L1-L25). Enterprise directory và enablement code bị loại khỏi MIT grant. Dòng enablement không xác lập quyền unrestricted riêng. |
| Enterprise production cần subscription hợp lệ | SOURCE | [LICENSE.enterprise:1–26](https://github.com/bytebase/bytebase/blob/a85f6cb4195299995e8554303550d672d5093e1d/LICENSE.enterprise#L1-L26). Không bypass license hoặc suy ra fork bỏ gates. |
| FREE giới hạn 10 instance, 20 seat | SOURCE | [plan.yaml:1–44](https://github.com/bytebase/bytebase/blob/a85f6cb4195299995e8554303550d672d5093e1d/backend/enterprise/plan.yaml#L1-L44). Giới hạn runtime build cụ thể, không tự suy rộng mọi source-only build. |
| Audit có TEAM gate, approval ở Enterprise plan | SOURCE | [TEAM audit](https://github.com/bytebase/bytebase/blob/a85f6cb4195299995e8554303550d672d5093e1d/backend/enterprise/plan.yaml#L80-L94), [Enterprise features](https://github.com/bytebase/bytebase/blob/a85f6cb4195299995e8554303550d672d5093e1d/backend/enterprise/plan.yaml#L135-L150). Runtime gọi TEAM, còn marketing dùng tên Pro. |
| Trang pricing hiện tại không cấp approval/audit cho Community | DOC | [Official pricing](https://www.bytebase.com/pricing/), đọc 2026-10-04. Community 10 instance/20 user; approval ở Enterprise, audit ở Pro/Enterprise. Edition labels không thay runtime gate đã quan sát. |
| Có native version/release/revision, replay skip | RUNTIME lịch sử | MODEL-03, REC-02 trong [45 ca](../../../BYTEBASE-ORACLE-POC-RESULTS.md), [case JSON](../../../evidence/bytebase-poc-cases.json). Central revision có version/SHA/taskRun; target không có migration ledger được quan sát. |
| Checksum detection không đạt strict rejection | RUNTIME lịch sử | REC-08 FAIL: WARNING rồi DONE/skip. Expected vẫn yêu cầu validation FAIL trước SQL mới. |
| Procedure INVALID, early promotion và SQL Review enforcement còn lỗi | RUNTIME lịch sử | SQL-11 FAIL, MODEL-07/GOV-04 FAIL. P04 bổ sung FAIL ngoài 45 ca. Không ghi hai lỗi promotion thành hai feature độc lập. |
| FREE approval/audit bị chặn | RUNTIME lịch sử | MODEL-06/GOV-02 BLOCKED; audit API 403 TEAM. Không coi việc thử Enterprise sẽ tự sửa lỗi correctness. |

## Đường thực thi

UI/CLI/API → Bytebase release/plan/issue/task → Go Oracle driver → Oracle schema.
Metadata PostgreSQL trung tâm giữ revision/version/SHA/taskRun.
Không có target migration ledger được thấy qua hậu kiểm lịch sử USER_TABLES.
Central applied state giúp replay nhưng chưa chứng minh crash giữa commit và revision hoặc fencing.
[Hồ sơ runtime](../../../BYTEBASE-ORACLE-POC-RESULTS.md) mô tả TCPS và independent Thin observer.

## Phạm vi còn thiếu

Chưa audit toàn image/dependency hoặc pin image digest cho lượt benchmark mới.
Chưa POC Enterprise, Oracle 19c/21c, real GitLab/Jenkins, controlled crash/restore/HA.
Không dùng snapshot source cũ `80524fc...` thay runtime commit mà không ghi khác biệt.
Lượt này không kết nối cluster, đọc credential, test, SQL hoặc benchmark.
