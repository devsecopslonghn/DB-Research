# Minimum engine selection

Only the previously researched engines are compared. The task-specific decision prioritizes the representative ordinary Oracle function and the already-familiar Flyway path; no product discovery or commercial-feature investigation was reopened.

| Candidate | Available evidence | Task consequence |
| --- | --- | --- |
| Flyway Community | Apache-2.0 source pin `a549f5dd1ac80fbe7bc8103dfcd2d556c606c39c`; Oracle parser/source/history references in [EVIDENCE.md](../EVIDENCE.md); source POM 13.9.0; matching OSS libraries built in this round | Selected: preserves raw versioned SQL; no changelog conversion; actual offline parser accepts the syntax fixtures |
| Liquibase 4.33.0 | Existing Apache source pin `75773ed9b45b0a5adf3c42872d2e5494da669427`; Oracle/checksum evidence retained; no installed executable or runtime build found | No demonstrated simpler available path; delimiter/split configuration and changelog would add work. 5.x licensing is not inherited from 4.x |
| SQLcl / SQL*Plus | SQLPlus command path exists; no approved distribution/version/license or integrated runtime proof; native directives present only in a synthetic historical fixture | Not selected. Reconsider only if mandatory actual corpus needs native client behavior; slash alone does not require a native client |

## Exact selected build

The wrapper uses `org.flywaydb:flyway-core:13.9.0` and `org.flywaydb:flyway-database-oracle:13.9.0`, with Java release 17 and the locally available Red Hat OpenJDK 21.0.12. These artifacts inherit Apache-2.0 from `flyway-parent:13.9.0`. It uses the OSS library coordinates rather than shipping the vendor CLI bundle with unrelated licensed components. The operator must approve the resulting engine jar SHA-256 and rebuild/retest on upgrade.

The standard Oracle JDBC dependency is `com.oracle.database.jdbc:ojdbc11:21.18.0.0`. Its POM and jar license identify **Oracle Free Use Terms and Conditions / Free Distribution, Hosting, and Use Terms and Conditions**, not an OSS license. The default POM does not bundle it. A separate hash-bound driver file is accepted only with explicit protected `oracle_driver.approved=true`; the user's connectivity-dependency decision is pending. All-dependencies-OSS therefore remains an unresolved hard boundary for Flyway/Liquibase. The Python observer uses `oracledb:3.4.0` under UPL-1.0 OR Apache-2.0.

Oracle documents 21.x JDBC compatibility with 19c/21c and supported JDKs; the current Flyway Oracle reference documents PL/SQL slash delimiters and its Oracle JDBC dependency. These are documentation claims, not this POC's runtime certification. [Oracle JDBC compatibility](https://docs.oracle.com/en/database/oracle/oracle-database/21/jjdbc/JDBC-getting-started.html), [Flyway Oracle reference](https://documentation.red-gate.com/flyway/reference/database-driver-reference/oracle-database), [driver artifact/license metadata](https://repo.maven.apache.org/maven2/com/oracle/database/jdbc/ojdbc11/21.18.0.0/ojdbc11-21.18.0.0.pom).

## Required behavior

| Concern | Implementation / evidence boundary |
| --- | --- |
| FUNCTION, procedure, package/body and `/` | Actual offline OracleParser reads the new fixtures and retained `release-small.sql`; DB compilation/execution still BLOCKED |
| Quoted identifiers and EDITIONABLE | Preserved exact SQL bytes; new function fixture parses; case/edition behavior still needs real Oracle |
| CLOB | SQL type remains untouched; approved optional invocation uses a Python CLOB bind; actual call NOT_RUN |
| Target schema | Owner writer, defaultSchema/schemas fixed to allowlist, no schema creation, identity preflight before dispatch |
| Versions | Unique increasing numeric version per canonical schema; `V<version>__<release_id>.sql`; old exact artifacts rebuilt from protected state for Flyway validation |
| Checksums | SHA-256 approval binds exact bytes and envelope. Flyway's native checksum/history remains an additional engine check, not the approval identity |
| Failure/replay | SQLite guards prevent dispatch; engine exit success still requires Oracle verification; SQL failure is conservatively PARTIAL; ambiguous result is UNKNOWN_OUTCOME |
| Native client behavior | Conservative pre-admission rejection; no paid SQLPlus emulation or script rendering |

The engine's configured operations are only `migrate` plus version readback. Clean, baseline-on-migrate, placeholders, out-of-order execution, connection retry and schema creation are disabled. Failed Flyway history may block future fresh releases; repair is a separately approved DBA operation, never automatic in this runner.

SELECTED ENGINE = Flyway Community 13.9.0
