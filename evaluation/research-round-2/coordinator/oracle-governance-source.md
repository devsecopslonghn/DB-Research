# Coordinator: Oracle và governance source review sâu

Ngày: 2026-10-04. Scope: source tĩnh có chọn lọc. Không runtime, test, SQL hoặc deployment.
[Manifest local source](local-source-manifest.json) và [Bytebase runtime-commit source](bytebase-source-manifest.json) ghi hash và provenance.
Các expected gốc giữ nguyên. Kết luận SOURCE không chuyển case runtime NOT_RUN thành FAIL/PASS.

## AccessFlow: native release path có giới hạn xác định được từ source

Pin: `bablsoft/accessflow@55c209a4d9e4ba09a6c089f90e68a8b16b3f2133`.

Đã đối chiếu bốn file Scanner/Gate/Promotion/Review với release `v2.7.0`, commit `2ba5d322e7e1b4c750b5b0af85935e9ae814bd6a`.
Nội dung bốn file giống từng byte. [Manifest đối chiếu](accessflow-release-comparison.json) ghi URL và SHA-256.
Kết luận gate trong các file này áp dụng cho cả hai source pin. Đây không phải xác minh image hoặc runtime release.

| Nhận định | Loại | Source và phạm vi |
| --- | --- | --- |
| BEGIN block bị gate từ chối trước parser | SOURCE | [Scanner:22–33](https://github.com/bablsoft/accessflow/blob/55c209a4d9e4ba09a6c089f90e68a8b16b3f2133/backend/src/main/java/com/bablsoft/accessflow/schemachange/internal/SchemaChangeStatementScanner.java#L22-L33) coi từ đầu BEGIN là transaction marker. [Gate:126–136](https://github.com/bablsoft/accessflow/blob/55c209a4d9e4ba09a6c089f90e68a8b16b3f2133/backend/src/main/java/com/bablsoft/accessflow/schemachange/internal/SchemaChangeStatementGate.java#L126-L136) từ chối transaction envelope. |
| Procedure/function/package/trigger thông thường có internal semicolon bị shape gate từ chối | SOURCE, suy luận trực tiếp từ điều kiện | [Scanner:35–66](https://github.com/bablsoft/accessflow/blob/55c209a4d9e4ba09a6c089f90e68a8b16b3f2133/backend/src/main/java/com/bablsoft/accessflow/schemachange/internal/SchemaChangeStatementScanner.java#L35-L66) trả true khi semicolon ngoài literal/comment còn nội dung phía sau. Internal `...; END;` thỏa điều kiện này. Scanner không theo grammar PL/SQL. Không cần giả định JSqlParser sẽ nhận body để thấy gate chạy trước. |
| SELECT/INSERT/UPDATE/DELETE bị từ chối trong change set | SOURCE | [Gate:46–47,126–152](https://github.com/bablsoft/accessflow/blob/55c209a4d9e4ba09a6c089f90e68a8b16b3f2133/backend/src/main/java/com/bablsoft/accessflow/schemachange/internal/SchemaChangeStatementGate.java#L126-L152). OTHER được nhận, không phải allow-list DDL. |
| Checksum tại promotion xác minh metadata statements trước submit | SOURCE | [Promotion:125–151](https://github.com/bablsoft/accessflow/blob/55c209a4d9e4ba09a6c089f90e68a8b16b3f2133/backend/src/main/java/com/bablsoft/accessflow/schemachange/internal/DefaultSchemaChangePromotionService.java#L125-L151). Đây là checksum trung tâm, không là Oracle target ledger hoặc strict REC-08 applied-version validation. |
| Native ladder kiểm lower APPLIED, can_ddl và review plan | SOURCE | [Promotion:248–305](https://github.com/bablsoft/accessflow/blob/55c209a4d9e4ba09a6c089f90e68a8b16b3f2133/backend/src/main/java/com/bablsoft/accessflow/schemachange/internal/DefaultSchemaChangePromotionService.java#L248-L305). Runtime binding/separation và target grant chưa kiểm. |
| Self-approval guard chạy trước reviewer override | SOURCE | [Review:117–136](https://github.com/bablsoft/accessflow/blob/55c209a4d9e4ba09a6c089f90e68a8b16b3f2133/backend/src/main/java/com/bablsoft/accessflow/requestgroups/internal/DefaultGroupReviewService.java#L117-L136) chặn submitter/on-behalf-of identity. Override reviewer logic ở :148–158 không tự bỏ bước guard này. Không tuyên bố admin không có mọi đường override khác. |
| Schema promotion dùng group stop-on-error | SOURCE | [Promotion:150–160](https://github.com/bablsoft/accessflow/blob/55c209a4d9e4ba09a6c089f90e68a8b16b3f2133/backend/src/main/java/com/bablsoft/accessflow/schemachange/internal/DefaultSchemaChangePromotionService.java#L150-L160) tạo draft với continueOnError=false. [GroupExecution:91–150](https://github.com/bablsoft/accessflow/blob/55c209a4d9e4ba09a6c089f90e68a8b16b3f2133/backend/src/main/java/com/bablsoft/accessflow/requestgroups/internal/GroupExecutionService.java#L91-L150) lưu PARTIALLY_EXECUTED nếu đã có member thành công trước lỗi. Generic continueOnError=true có semantics khác; không gán semantics đó cho native schema promotion. |
| JDBC non-select path không có compile diagnostics trong hàm đã đọc | SOURCE phạm vi hẹp | [DefaultQueryExecutor:132–170,436–442](https://github.com/bablsoft/accessflow/blob/55c209a4d9e4ba09a6c089f90e68a8b16b3f2133/backend/src/main/java/com/bablsoft/accessflow/proxy/internal/DefaultQueryExecutor.java#L436-L442) dùng executeLargeUpdate và trả affected count. Không chứng minh toàn hệ thống thiếu hook khác. |

**Quyết định:** AccessFlow vẫn đáng nghiên cứu governance và schema change đơn giản.
Không ưu tiên native Oracle migration POC với workload bắt buộc DML/PLSQL hiện tại.
`release-small.sql` không phù hợp gate này theo SOURCE. Không xóa DML/block hoặc đổi raw query path để tạo PASS.
SQL-03/04..09 và PERF-03 có source incompatibility cần ghi riêng với runtime NOT_RUN.
Đây là lý do điều phối giảm ưu tiên migration, không sửa expected hoặc ghi kết quả test giả.

Central state có `@Version`, repository lock method và scheduler ShedLock trong source liên quan.
Không kết luận không có bất kỳ lock nào. Các lock đó chưa chứng minh Oracle target fencing hoặc crash reconciliation.

## Archery: compile check có phạm vi hẹp hơn nhãn hỗ trợ PL/SQL

Pin: `hhyo/Archery@ccc7134f48d0e261f9e3ffa0d445dcec48adb790`.

Đối chiếu release `v1.14.0`, commit `bc1f10efcc465f6a63c94b97feaba5d15546712a`, phát hiện khác driver.
Release dùng `cx-Oracle==7.3.0`; HEAD được review dùng `oracledb==4.0.1`.
Không dùng lựa chọn Thin của python-oracledb để mô tả image release v1.14.0.
`sql_utils.py`, `setup.sh` và toàn hàm `execute_workflow` giống từng byte giữa hai pin.
Vì vậy nhận định về splitter, commit và package-body check trong hàm này cũng có ở source release.
[Manifest đối chiếu](archery-release-comparison.json) ghi bốn file, hash và vùng hàm release :1105–1251.
Registry revision label khớp release SHA, nhưng không thay SBOM hoặc chứng minh mọi dependency trong layer.

| Nhận định | Loại | Source và phạm vi |
| --- | --- | --- |
| Executor dùng SQL đã lưu trong review_content | SOURCE | [oracle.py:1108–1121](https://github.com/hhyo/Archery/blob/ccc7134f48d0e261f9e3ffa0d445dcec48adb790/sql/engines/oracle.py#L1108-L1121). Có cơ sở kiểm MODEL-05 artifact binding; chưa chứng minh mọi edit route invalidates approval. |
| Commit sau mỗi statement; exception dừng vòng | SOURCE | [oracle.py:1147–1152,1201–1215](https://github.com/hhyo/Archery/blob/ccc7134f48d0e261f9e3ffa0d445dcec48adb790/sql/engines/oracle.py#L1147-L1215). Partial effect tồn tại; không coi workflow là transaction nguyên script. |
| INVALID check chỉ named PLSQL object | SOURCE | [oracle.py:1156–1204](https://github.com/hhyo/Archery/blob/ccc7134f48d0e261f9e3ffa0d445dcec48adb790/sql/engines/oracle.py#L1156-L1204). Có check thực sự, không nói hoàn toàn thiếu. |
| Check có thể bỏ sót invalid package body | SOURCE inference, chưa runtime | Cùng :1163–1172 lọc OWNER/OBJECT_NAME, không lọc OBJECT_TYPE, rồi fetchone. Package spec/body có thể cùng name. Nếu hàng đầu VALID nhưng body INVALID, check không kiểm mọi hàng. Cần POC package spec VALID/body INVALID; không tuyên bố đã tái hiện. |
| Parser có logic PLSQL/custom delimiter và giới hạn regex | SOURCE | [sql_utils.py:192–270](https://github.com/hhyo/Archery/blob/ccc7134f48d0e261f9e3ffa0d445dcec48adb790/sql/utils/sql_utils.py#L192-L270). Có xử lý package body trước package, bỏ slash cuối. Regex object detection yêu cầu CREATE OR REPLACE; không chứng minh dạng CREATE-only/EDITIONABLE/quoted-name phức tạp. |
| Requester có thể execute nếu được cấp sql.sql_execute | SOURCE | [sql_review.py:13–41](https://github.com/hhyo/Archery/blob/ccc7134f48d0e261f9e3ffa0d445dcec48adb790/sql/utils/sql_review.py#L13-L41). Platform không tự cấm mọi requester execute. Role/policy cần cấu hình và negative POC. |

Oracle [ALL_OBJECTS](https://docs.oracle.com/en/database/oracle/oracle-database/12.2/refrn/ALL_OBJECTS.html) có OBJECT_TYPE và STATUS.
Oracle [package example](https://docs.oracle.com/cd/E57425_01/121/APPUG/E17931-04.pdf) minh họa PACKAGE VALID nhưng PACKAGE BODY INVALID.
Các docs cũ này dùng để giải thích dictionary semantics, không chứng nhận Archery tương thích Oracle 19c/21c/26ai.

**Quyết định:** giữ Archery cho governance POC giới hạn. Không xem source compile check là SQL-11 PASS.
Ca body INVALID phải kiểm toàn bộ object types và ALL_ERRORS, cùng terminal workflow result.

## ODC: warning khác nhau giữa Oracle và OceanBase Oracle mode

Source backend pin `d517c0f27971642fb0cd7565fd61ab2309875ec3`, không xác lập chính xác source của runtime image 4.4.1 đã chạy.
[OdcStatementCallBack:274–322](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/session/OdcStatementCallBack.java#L274-L322) chỉ đánh existWarnings khi dialect là OB_ORACLE.
Non-resultset path tạo successResult. Đoạn này không dùng ALL_ERRORS/OBJECT_TYPE để nghiệm thu compile.
Không gộp Oracle với OceanBase Oracle mode. Có warning flag cũng không tự chặn release.

[DatabaseChangeThread:221–278](https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/task/DatabaseChangeThread.java#L221-L278) retry SQL theo retryTimes/interval sau kết quả lỗi.
Retry callback không có target migration ledger/checksum gate được thấy trong đoạn này.
Tắt retry trong cấu hình POC, rồi kiểm target trước retry sau DDL partial/uncertain.
Đây là điều kiện nghiên cứu từ SOURCE, không thay REC-03 lịch sử hoặc chứng minh runtime lỗi mới.

**Quyết định:** giữ ODC platform OSS, ưu tiên pin source/image đúng build và kiểm SQL-11/REC-02/08/10/GOV-03.
Source này phù hợp với hướng điều tra false success, nhưng chưa đủ để kết luận nguyên nhân runtime đã chứng minh.

## Bytebase: trace đúng runtime commit

Pin `a85f6cb4195299995e8554303550d672d5093e1d` từ hồ sơ runtime 3.22.1/FREE.
Đã tải ba source file cụ thể qua raw GitHub, không build hoặc execute.

- SOURCE: [Oracle driver:141–218](https://github.com/bytebase/bytebase/blob/a85f6cb4195299995e8554303550d672d5093e1d/backend/plugin/db/oracle/oracle.go#L141-L218) dùng parser SplitSQL, ExecContext và transaction/autocommit modes. Đường đã đọc không hậu kiểm compilation bằng ALL_ERRORS/ALL_OBJECTS.
- SOURCE: [Migration executor:478–600](https://github.com/bytebase/bytebase/blob/a85f6cb4195299995e8554303550d672d5093e1d/backend/runner/taskrun/database_migrate_executor.go#L478-L600) đọc central revisions, skip applied version, chạy driver rồi tạo central revision. Oracle commit và central revision không là một transaction nguyên tử trong đường này.
- SOURCE: [Run tasks:778–887](https://github.com/bytebase/bytebase/blob/a85f6cb4195299995e8554303550d672d5093e1d/backend/api/v1/rollout_service.go#L778-L887) kiểm cùng environment, quyền chạy và approval theo project settings. Đoạn này không kiểm lower-stage success. Chưa trace toàn scheduler để khẳng định mọi đường thiếu invariant.
- RUNTIME lịch sử: [comparison](../../../BYTEBASE-ODC-COMPARISON.md) đã có SQL-11/REC-08/MODEL-07/GOV-04 FAIL và P04 bổ sung. Không chạy lại hoặc đổi kết quả.

**Quyết định:** giữ Bytebase làm đối chứng version/replay, không thêm FREE vào đáp án OSS governance hoàn chỉnh.
REC-05/06 phải có checkpoint giữa Oracle commit và central revision. Metadata backup riêng không tự chứng minh recovery.

## Các câu hỏi còn cần runtime

Mọi ca negative phải dùng actor/target/hash riêng và Oracle hậu kiểm độc lập.
Source trace có thể xác định capability gate, nhưng không đo handshake, enforced role, race, durability hoặc latency.
Không có dữ liệu benchmark mới. Không gán thời gian chạy hoặc điểm hiệu năng từ kiến trúc/source.
