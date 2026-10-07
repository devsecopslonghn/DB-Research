# Oracle implementation coverage

## Source Oracle review sâu, 04/10/2026

[Oracle/governance trace](evaluation/research-round-2/coordinator/oracle-governance-source.md) xác định AccessFlow gate, Archery package-body risk và ODC dialect warning scope.
[CloudDM execution trace](evaluation/research-round-2/clouddm/deep-source-review.md) nối CI/ticket tới datasource splitter và Oracle session. Compile validation vẫn cần runtime.
Source không chứng nhận handshake, correctness, recovery hoặc latency. Oracle 19c/21c chưa có POC mới.
Evidence Oracle 26ai, Bytebase/ODC và các FAIL lịch sử giữ nguyên. [Task spec](evaluation/research-round-2/poc-next-tasks.md) ghi ca hậu kiểm.

## Cập nhật Oracle T03, 04/10/2026

[Source reviews](evaluation/README.md) ghi giới hạn theo build và đường thực thi native.
[ODC/Bytebase comparison](BYTEBASE-ODC-COMPARISON.md) giữ kết quả runtime Oracle 26ai.
AccessFlow schema-change gate và raw query path có scope khác nhau.
Archery có named PL/SQL INVALID check trong source, chưa nghiệm thu runtime.
CloudDM có connector Oracle tích hợp. Parser/ledger/recovery chưa được chứng minh.
Oracle 19c/21c và runtime ứng viên mới vẫn chưa kiểm.

Runtime update, 2026-10-04: ODC connected to Oracle through a local TCPS wrapper and completed one metadata SELECT.
See [connection POC](ODC-CONNECTION-POC.md). The subsequent API/UI POC has [per-case results](ODC-ORACLE-POC-RESULTS.md). Earlier source statements retain their dated scope.

This table describes source support. It does not describe runtime test results.
Các ô trong bảng source không phải kết quả runtime. Kết quả Oracle 26ai nằm trong các báo cáo POC được liên kết ở trên.
ODC is deployed. Oracle plugin and driver presence received image inspection, as recorded in [ODC-EVALUATION.md](ODC-EVALUATION.md).

`YES` means an explicit implementation or documented native execution mechanism exists.
`PARTIAL` means limited parsing, configuration requirements, or a restricted execution path.
`UNKNOWN` means the review did not establish that specific construct.

| Project | SQL / DDL | DML | Procedure | Function | Package | Trigger | Anonymous block | Slash delimiter | SQLPlus scripts | Mechanism |
|---|---|---|---|---|---|---|---|---|---|---|
| AccessFlow schema change sets | YES | NO | PARTIAL | PARTIAL | PARTIAL | PARTIAL | NO for leading BEGIN | NO established support | NO | Thin JDBC, schema gate, prepared statement |
| AccessFlow ordinary query path | YES | YES | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | NO | Parser and Thin JDBC. Separate from the release workflow. |
| Bytebase | YES | YES | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | UNKNOWN | Go go-ora driver and Oracle splitter |
| Archery / sampled derivative | YES | YES | YES | YES | YES | YES | YES | PARTIAL | NO for a general script | python-oracledb and custom procedural splitting |
| DRM | YES | YES | YES | YES | YES | YES | YES | YES | PARTIAL | Native SQLPlus. Error directives and engine state need verification. |
| Open Migration | NO | NO | NO | NO | NO | NO | NO | NO | NO | No Oracle engine |
| SchemaPilot | NO | NO | NO | NO | NO | NO | NO | NO | NO | Only MySQL and PostgreSQL implementation |
| Flyway UI | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | Supplied Flyway 2.2.1 instance. No current Oracle verification. |
| Flyway Play | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | NO in default Community path | Embedded Flyway 9.16.0 plus configured Oracle driver |
| Flyway Community | YES | YES | YES | YES | YES | YES | YES | YES | NO for full SQLPlus commands | Oracle Thin JDBC and Oracle parser |
| Liquibase 4.33.0 | YES | YES | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | NO for a general script | Oracle JDBC. Use explicit procedural changeset boundaries. |
| Liquibase current Community | YES | YES | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | NO in ordinary JDBC path | JDBC. Current FSL license excludes it from strict OSS matching. |
| Sqitch | YES | YES | YES | YES | YES | YES | YES | YES | YES | SQLPlus scripts and target Oracle registry |
| Atlas public OSS | NO | NO | NO | NO | NO | NO | NO | NO | NO | Oracle driver requires Pro |
| Yearning | NO | NO | NO | NO | NO | NO | NO | NO | NO | MySQL product scope |
| .NET dbdeploy | YES | YES | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | UNKNOWN | Oracle Managed Data Access and OracleScriptParser |
| DbMaintain | YES | YES | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | YES | YES with native runner | JDBC by default. Optional native SQLPlus runner. Deprecated. |
| dbpm | YES | YES | YES | YES | YES | YES | YES | YES | PARTIAL | SQLcl or SQLPlus and required Core substrate |
| dbward | NO | NO | NO | NO | NO | NO | NO | NO | NO | PostgreSQL and MySQL execution targets |
| CloudBeaver Community | YES | YES | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | Oracle Thin JDBC driver through SQL editor |

Source references are in [EVIDENCE.md](EVIDENCE.md#source-references).
The primary references are AF-GATE, AF-SCAN, BB-ORA, AR-PARSER, AR-EXEC, FW-PARSER, SQ-SQLPLUS, DEP-ORA, and CB-ORA.

## Parser and execution limits

AccessFlow's schema gate treats BEGIN as a transaction envelope.
The same gate rejects semicolons followed by additional content.
That rule can reject common Oracle procedural bodies before execution.
Support in an ordinary query editor cannot be assumed to exist in the schema release path.

Archery has explicit procedural handling and compilation checks.
Its text normalization remains different from a complete native SQLPlus interpreter.
Packages, wrapped bodies, q-quoted literals, slash placement, and nested blocks still require runtime verification.

Flyway Community recognizes procedural blocks and slash delimiters.
The slash is a parsing delimiter. It is not proof of SQLPlus command support.
Flyway Teams and Redgate native features have separate license boundaries.

Liquibase procedural support depends on how the changeset divides statements.
Use explicit delimiter and statement-splitting settings for SQL bodies.
Do not assume that arbitrary SQLPlus files are valid JDBC changesets.
Version-specific slash handling needs verification against the pinned engine.

Native SQLPlus execution generally preserves Oracle script syntax.
Reliable failure reporting also needs WHENEVER SQLERROR and WHENEVER OSERROR behavior.
Target ledger locking, checksum validation, and post-commit uncertainty remain separate concerns.

## Oracle coverage from the product-model search

All Oracle execution acceptance results remain `NOT RUN`.
The following findings supplement the original execution comparison.

| Candidate | Oracle mechanism | SQL/DDL/DML | Procedural constructs | Script-client commands | State/recovery limit |
|---|---|---|---|---|---|
| OceanBase ODC | Actual Oracle Thin JDBC plugin. Distinct from OceanBase Oracle mode. Plugin and ojdbc8 driver present in deployed 4.4.1 image. | Single and multi-database task configuration exists. Execution uses JDBC. | Frontend enables PL editing and anonymous blocks. Deploy-time invalid-compilation detection not established. Packages, triggers, complex literals, and delimiters require runtime verification. | No SQLPlus interpreter established in reviewed task path. | Central parent/child results. No target version/checksum ledger found in reviewed execution path. Configured retries can repeat statements. |
| SQLE Oracle plugin | go-ora execution and transaction methods | Direct execution code exists. Full current Community packaging not verified. | Parser and compilation coverage not established. | No SQLPlus interpreter established. | Target migration state and full plugin license coverage not established. |
| Early sampled Bytebase forks | Historical driver inventory | Oracle driver not established in hongweiyi or nanzm snapshots. | UNKNOWN | UNKNOWN | A historical Apache license does not provide a missing Oracle implementation. |
| Dokeeper historical lead | Oracle source paths in inherited Bytebase tree | Implementation presence only. Free distribution suitability not established. | UNKNOWN | UNKNOWN | Copied source and enterprise license prevent an unrestricted product conclusion. |

Sources: [P-ODC-ORACLE, P-ODC-ORACLE-UI, P-ODC-EXEC, P-SQLE-ORACLE](PRODUCT-EVIDENCE.md#source-references).
The [frontend record](UI-EVIDENCE.md) explains why MySQL demonstration screenshots do not prove Oracle execution.

## ODC connection and permission acceptance

Use a native Oracle datasource with a reachable listener, SID/service, environment, and evaluation account.
The [ODC guide](ODC-EVALUATION.md) provides connection fields and JDBC URL examples.
Dòng này thuộc inspection cũ. POC Oracle 26ai sau đó đã đăng ký datasource riêng và có bằng chứng API/UI.
Oracle 19c/21c connection, schema discovery, package execution, and recovery remain unverified.

ODC project administrators, DBAs, and Developers inherit access to all project database records.
Evaluate Participant with explicit grants for access restricted to selected schema records.
ODC permission grants do not execute Oracle GRANT statements.
Verify native datasource privileges and denied cross-schema access in the Oracle acceptance plan.
Sources: [P-ODC-ROLE-INHERITANCE, P-ODC-DB-PERMISSION-SERVICE](PRODUCT-EVIDENCE.md#source-references).
