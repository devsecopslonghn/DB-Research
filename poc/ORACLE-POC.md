# Oracle proof-of-concept plan

**ODC API/UI execution results were recorded on 2026-10-04.**
See [the result report](../ODC-ORACLE-POC-RESULTS.md). Original criteria remain unchanged.
ODC and AccessFlow remain existing platform candidates under the revised product-model rule.
Evaluate their existing workflows before implementing an engine adapter.
The original target-state acceptance criteria still apply to execution readiness.
The initial research did not receive Oracle connection details.
On 2026-10-04, ODC connected to the supplied Oracle target and completed one metadata SELECT.
The earlier metadata-only snapshot remains a separate historical connectivity check.
ODC 4.4.1 is deployed. Readiness, storage, Oracle driver presence, and selected authenticated GET routes were inspected.
The current result report identifies completed cases and remaining limits.
See [ODC onboarding and evidence limits](../ODC-EVALUATION.md).

## Existing platform acceptance first

A missing target ledger does not automatically reject the platform model.
It still prevents a claim that the platform meets reliable migration execution requirements.
A failed case must remain visible. Do not change acceptance criteria to make a candidate pass.

| ID | Existing workflow case | Acceptance criterion | Result |
|---|---|---|---|
| MODEL-01 | Project ownership | Applications/projects and their database targets have stable identities. | PASS |
| MODEL-02 | Estate inventory | Register Oracle instances, services, databases/schemas, and environments centrally. | PASS |
| MODEL-03 | Change identity | Retain a stable change/release identifier and exact SQL artifact. | PARTIAL |
| MODEL-04 | Actor records | Retain requester, approver, executor, database account, and timestamps separately. | PARTIAL |
| MODEL-05 | Review | Review the exact SQL intended for the selected Oracle targets. | PASS |
| MODEL-06 | Approval scope | Bind approval to the artifact and target set. Record any later change. | PARTIAL |
| MODEL-07 | Environment rollout | Run the same approved change through DEV, SIT, UAT, and PROD in the accepted order. | PARTIAL |
| MODEL-08 | Manual continuation | Stop between stages. Resume only through an authorized action. | PASS |
| MODEL-09 | Failed stage | Apply the accepted stop policy. Do not continue automatically after an uncertain result. | PARTIAL |
| MODEL-10 | History and logs | Display per-target status, execution records, errors, and central audit. | PARTIAL |
| MODEL-11 | Estate permissions | Prevent unauthorized project, target, approval, and execution actions. Verify inherited project access, Participant grants, expiry, and denied Oracle cross-schema access. | PARTIAL |
| MODEL-12 | Release readiness | Identify every missing release, checksum, ledger, locking, and recovery capability. | PASS |

For ODC, inspect ordered batch tickets, parent approval, child execution, and manual continuation.
Verify the documented 2–100 target task limit against the estate's release size.
For AccessFlow, inspect datasource-bound environments and the schema change-set ladder.
Verify project/estate semantics and required DML/PL/SQL against the existing script gate.

## Setup requirements

1. Use disposable DEV and SIT schemas on the required Oracle version.
2. Record the Oracle edition, patch level, character set, and driver version.
3. Pin the platform commit, migration engine version, and image digest.
4. Use separate requester, approver, executor, and observer accounts.
5. Permit only the disposable schemas in the proof-of-concept inventory.
6. Record central job IDs, release hashes, target ledger rows, and Oracle object status.
7. Place a controlled process barrier between execution and each success record.
8. Use a controlled network proxy for interruption cases.
9. Record recovery steps before running failure cases.

Do not use a generic timing delay as proof of the crash checkpoint.
Instrument the worker or engine so the commit boundary is observable.
The initial plan executed no commands. The result report records the subsequent authorized execution.

## Candidate-specific conditions

| Candidate | Required condition before verification |
|---|---|
| Existing ODC | Deployment and Oracle connectivity are available through the image-specific TCPS wrapper. Create dedicated evaluation schemas, then verify permissions, batch approval, duplicates, and uncertain-result recovery. |
| Existing AccessFlow | Verify existing schema change sets and target-bound environments before adapter design. |
| AccessFlow + Flyway | Implement a dedicated migration authoring path. Preserve approval and permission checks. |
| Archery + Flyway | Preserve reviewed SQL artifacts. Route migrations through Flyway instead of direct statement execution. |
| Jenkins + Flyway | Add a target inventory, structured result store, and approval binding to the release hash. |
| Rundeck + Flyway | Add an explicit approval record and release model. Job permission alone is insufficient. |
| Liquibase 4.33 alternative | Use the inspected Apache source. Verify the license of the actual binary and every extension. |
| Sqitch alternative | Install the licensed Oracle client separately. Verify registry integrity and deployment recovery. |

## Required SQL cases

Run each case against each existing platform or implemented proposal that remains under consideration.
Keep migration files immutable after approval.

| ID | Case | Procedure | Acceptance result | Actual result |
|---|---|---|---|---|
| SQL-01 | CREATE TABLE | Deploy a table with primary key, number, varchar, and timestamp columns. | Table exists. One successful target entry and one linked central result exist. | PARTIAL |
| SQL-02 | ALTER TABLE | Add a column and a named constraint in a new migration. | Both objects exist. Version order and ledger are correct. | PARTIAL |
| SQL-03 | INSERT/UPDATE | Insert a row, update its value, and verify the final value. | The row changes once. Replay does not increase the row count or value. | PARTIAL |
| SQL-04 | Procedure | Deploy a procedure with internal semicolons and an executable body. | Procedure is VALID. Invocation changes the expected row. | PASS |
| SQL-05 | Function | Deploy a function with a numeric return value. | Function is VALID. SELECT from DUAL returns the expected value. | PASS |
| SQL-06 | Package | Deploy a specification and body with initialization code. | Both objects are VALID. Package invocation succeeds. | PASS |
| SQL-07 | Trigger | Deploy a row trigger that uses :NEW and :OLD. | Trigger is VALID. One event produces one expected effect. | PASS |
| SQL-08 | Anonymous PL/SQL | Execute BEGIN/END and DECLARE/BEGIN/END forms. | Each block executes once. Internal semicolons remain intact. | PASS |
| SQL-09 | Slash delimiter | Deploy procedural bodies with a slash on a separate line. | The parser uses the slash as a client delimiter. Oracle does not receive a bare slash statement. | PASS |
| SQL-10 | SQLPlus commands | Evaluate PROMPT, SET DEFINE, DEFINE, SPOOL, @, @@, and WHENEVER directives. | Required commands work through a supported execution path. Unsupported commands fail clearly before execution. | PARTIAL |
| SQL-11 | Invalid compilation | Deploy syntactically accepted PL/SQL with a compilation error. | The result reports invalid compilation. ALL_ERRORS identifies the error. The release is not reported as fully successful. | FAIL |
| SQL-12 | Oracle literal forms | Use q-quoted text, comment markers in strings, quoted identifiers, and nested blocks. | The parser preserves the exact body and statement boundaries. | PASS |

Flyway Community JDBC does not provide the full SQLPlus command feature.
If SQL-10 is mandatory, the design needs a separately verified native-client path.
That path must retain target tracking and error handling.
It must not silently ignore required commands.

For JDBC PL/SQL, preserve the procedural body as one database statement.
For native SQLPlus, retain its script delimiters and commands.
Do not use the same unverified statement-splitting rules for both execution mechanisms.

## Required failure and recovery cases

| ID | Case | Procedure | Acceptance result | Actual result |
|---|---|---|---|---|
| REC-01 | Intentional failure | Add a statement that references a missing table. | Execution stops according to policy. The central result contains the exact failed migration and Oracle error. | PARTIAL |
| REC-02 | Normal replay | Submit a previously successful versioned migration again. | The engine skips the migration. The platform records the replay request without changing target state. | FAIL |
| REC-03 | Retry after failure | Retry REC-01 after an approved correction and target inspection. | Recovery follows a documented decision. The platform does not repeat committed work without review. | PARTIAL |
| REC-04 | Partial DDL | Execute CREATE TABLE, then an invalid ALTER TABLE in one migration. | The created table remains visible. The platform reports partial or uncertain state. Automatic replay is blocked. | PARTIAL |
| REC-05 | Crash after target commit | Stop the process after DDL commits and before target history success is recorded. | Restart detects an uncertain result. An operator reconciles objects and history before resuming. | NOT RUN |
| REC-06 | Crash after target history | Stop the worker after the successful target ledger row and before central success recording. | Restart reads target success and repairs central state. No SQL replay occurs. | NOT RUN |
| REC-07 | Network interruption | Interrupt the connection before execution, during execution, and after commit acknowledgement. | The result distinguishes known failure from uncertain outcome. Recovery checks target history and object state. | NOT RUN |
| REC-08 | Checksum change | Change the content of a successful migration without changing its ID. | Validation fails before new SQL executes. An authorized repair cannot be silent. | FAIL |
| REC-09 | Concurrent runners | Submit two releases for the same target schema simultaneously. | Only one migration execution holds the target lock. Both central jobs have accurate results. | PARTIAL |
| REC-10 | Duplicate API request | Send the same approved execution request twice. | Stable request identity prevents duplicate work. Both API responses link to the same execution decision. | FAIL |
| REC-11 | Central restart | Restart the central service while the worker continues. | The platform reconciles the durable job and target state without duplicate execution. | NOT RUN |
| REC-12 | Stale lock | Stop a worker while it holds migration or platform locks. | Recovery distinguishes a dead worker from a slow worker. An operator can release a proven stale lock. | NOT RUN |

## Central governance and operations

| ID | Case | Acceptance result | Actual result |
|---|---|---|---|
| GOV-01 | WHO / WHAT / WHERE / WHEN / HOW / RESULT | A query returns requester, approver, executor, SQL artifact, target, times, trigger, and result. | PARTIAL |
| GOV-02 | Approval binding | Changing the artifact, target, environment, or release version invalidates the previous approval. | PARTIAL |
| GOV-03 | Separation of duties | An unauthorized requester cannot approve or execute their own production change. Document administrator powers separately. | FAIL |
| GOV-04 | Environment promotion | Higher environments receive the same immutable artifact after required lower-environment success. | PARTIAL |
| GOV-05 | CI identity | GitLab and Jenkins triggers retain a named service principal and the initiating job reference. | NOT RUN |
| GOV-06 | Backup and restore | Restored metadata, artifacts, and keys remain readable. Reconciliation detects target changes after the backup. | NOT RUN |
| GOV-07 | Multiple replicas | Concurrent API servers cannot dispatch duplicate target execution. | NOT RUN |
| GOV-08 | Secret handling | Logs and stored results contain no database passwords or secret-manager credentials. | PARTIAL |
| GOV-09 | Audit export | Audit export preserves actor, artifact hash, target, time, trigger, and result after log rotation. | PARTIAL |

## Required record for each run

1. Record the exact repository commit and binary or image digest.
2. Record the Oracle version, database service, schema, and ledger location.
3. Save the approved artifact hash and approval identities.
4. Save the central job record and redacted deployment log.
5. Save target history before and after execution.
6. Save relevant object definitions, ALL_OBJECTS status, and ALL_ERRORS output.
7. Record the observed failure checkpoint and recovery action.
8. Mark each acceptance item PASS, FAIL, or INCONCLUSIVE.

## Decision rules

Reject a proposal if an uncertain result causes automatic SQL replay.
Reject a proposal if the worker executes content different from the approved artifact.
Reject a proposal if central success hides failed history recording or invalid PL/SQL compilation.
Reject a proposal if a required capability depends on an unapproved commercial component.

An expected, detected Oracle DDL uncertainty is not an automatic engine rejection.
It requires a controlled recovery process and accurate reporting.
If automatic exactly-once execution of arbitrary Oracle DDL is mandatory, this review has no verified solution.

## Kế hoạch tiếp tục ODC POC ngày 04/10/2026

Đã có datasource `oracle-cloud`, kết nối TCPS và SELECT metadata thành công.
Người dùng cho phép tạo schema riêng để đánh giá. Bảng dưới giữ kế hoạch ban đầu. Kết quả thực tế nằm trong báo cáo liên kết.
45 ca phía trên đã có trạng thái theo hồ sơ API/UI. [Hồ sơ kết nối](../ODC-CONNECTION-POC.md) ghi bằng chứng đã có.

### Bố trí dữ liệu và tài khoản

Oracle gắn schema với user. Tạo user POC sẽ tạo namespace schema tương ứng.
Dùng prefix `ODC_POC_20261004_`. Đối chiếu `ALL_USERS` trước khi tạo để tránh trùng tên.

| Thành phần | Cấu hình dự kiến | Mục đích |
|---|---|---|
| Schema DEV | `ODC_POC_20261004_DEV`, quota 50 MiB trên DATA | SQL, PL/SQL và các ca lỗi ban đầu |
| Schema SIT | `ODC_POC_20261004_SIT`, quota 50 MiB trên DATA | Kiểm tra target thứ hai và promotion |
| Schema UAT, mock PROD | Thêm sau: suffix `UAT`, `MOCKPROD`, quota 50 MiB mỗi schema | Kiểm tra đủ bốn giai đoạn |
| Quyền schema owner | CREATE SESSION, TABLE, VIEW, SEQUENCE, PROCEDURE, TRIGGER | Tạo object trong schema của user |
| Oracle observer | CREATE SESSION và SELECT trên các bảng POC được chỉ định | Kiểm tra giới hạn đọc và truy cập chéo schema |
| ODC project | Project riêng `odc-oracle-poc` | Inventory, thành viên, quyền và ticket POC |
| ODC identities | Requester, approver, executor, observer riêng | Đối chiếu actor và separation of duties |

Tài khoản ADMIN dùng cho bootstrap. Ca thực thi dùng datasource với tài khoản POC tương ứng.
Không cấp DBA hoặc quyền ANY cho tài khoản POC. Kiểm tra grant thực tế trước các ca quyền.
Schema riêng trên một database chỉ mô phỏng môi trường. Kết quả không chứng minh cách ly instance hoặc mạng.
Quota Oracle không thay đổi hai PVC 5/10 GiB của ODC và MetaDB.

### Thứ tự và bằng chứng cần thu

| Đợt | Ca trong kế hoạch | Công việc | Bằng chứng và điều kiện đạt |
|---|---|---|---|
| 1 | Setup; MODEL-01, MODEL-02 | Ghi version Oracle, charset, driver; tạo DEV/SIT; đăng ký datasource; gắn project và environment | Inventory và ID ổn định; schema đúng; không lộ credential |
| 2 | SQL-01..03 | CREATE/ALTER TABLE, INSERT/UPDATE trên dữ liệu giả | Object, constraint và dữ liệu đúng; đối chiếu ledger và replay theo từng tiêu chí gốc |
| 3 | SQL-04..10, SQL-12 | Procedure, function, package, trigger, anonymous block, delimiter và SQLPlus directive | ALL_OBJECTS, ALL_ERRORS, giá trị trả về; chỉ rõ directive nào được hỗ trợ |
| 4 | SQL-11; MODEL-05, MODEL-09, MODEL-10; REC-01, REC-04 | Procedure INVALID, SQL Review ERROR, lỗi bảng thiếu và DDL thành công một phần | UI/API báo đúng lỗi; không che INVALID bằng trạng thái thành công; có object hậu kiểm |
| 5 | MODEL-04, MODEL-06, MODEL-11; GOV-01..03, GOV-08, GOV-09 | Approval, đổi artifact sau duyệt, actor, quyền kế thừa project, quyền schema, audit và secret | Request bị chặn thực tế; hash artifact; danh tính requester/approver/executor; log đã che dữ liệu nhạy cảm |
| 6 | MODEL-03, MODEL-07, MODEL-08, MODEL-12; GOV-04, GOV-05 | API tạo ticket, approval, trạng thái; CLI mô phỏng CI; DEV→SIT→UAT→mock PROD | Artifact giống nhau; job reference; dừng/chạy tiếp đúng quyền; ghi rõ thiếu release/ledger |
| 7 | REC-02, REC-03, REC-08..10 | Replay, retry, checksum đổi, request trùng và thực thi đồng thời | Target không chạy lặp ngoài chính sách; lock, SQL và central record khớp |
| 8 | REC-05..07, REC-11, REC-12; GOV-06, GOV-07 | Crash checkpoint, gián đoạn mạng, restart, stale lock, restore và nhiều replica | Cần instrumentation/proxy và kế hoạch phục hồi riêng trước thực thi; schema mới chưa đủ điều kiện |

Ưu tiên đợt 1–5. Hai điểm cần kiểm tra sớm là procedure INVALID và enforcement khi SQL Review có ERROR.
Đây là các điểm đã thất bại trong hồ sơ Bytebase lịch sử. Không suy ra ODC sẽ có cùng kết quả.
Đợt 6 bắt đầu bằng API/CLI giữ job reference. Chỉ gọi đó là tích hợp GitLab/Jenkins khi có runner thực tế.

Mỗi lần chạy lưu SQL artifact và SHA-256, ID ticket/task, actor, timestamp và kết quả Oracle hậu kiểm.
Ảnh Selenium chụp UI thật. Ảnh không thay thế hậu kiểm Oracle hoặc bằng chứng denied API.
Dùng dữ liệu giả. Giữ object POC để người dùng xem lại trước khi cleanup.
Đánh giá tiêu chí gốc từng ca. Nếu SQL chạy được nhưng ledger thiếu, ghi PARTIAL/FAIL tương ứng, không đổi tiêu chí.

Nguồn setup: [Oracle Autonomous: tạo user và quota](https://docs.public.content.oci.oraclecloud.com/iaas/autonomous-database-shared/doc/manage-users-create.html).
