# Workload profile

Observed inputs: the user's abbreviated `CREATE OR REPLACE EDITIONABLE FUNCTION ... END; /` sample description, the [existing Oracle contract](ORACLE-POC.md), and the 14-artifact [workload manifest](../evaluation/workloads/manifest.json). All existing sanitized workloads were inspected statically; none was executed in this round. The manifest remains unchanged.

## Representative function

| Observed shape | Required behavior |
| --- | --- |
| PL/SQL FUNCTION | Submit the complete definition as one statement; internal semicolons remain inside it |
| Quoted schema/object names | Preserve spelling and case; verify exact owner/name/type |
| EDITIONABLE | Preserve the keyword; verify actual edition/schema compatibility in Oracle |
| CLOB input | Preserve the signature; use a CLOB bind for an optional deterministic call |
| `/` on its own line | Treat it as the client block delimiter; do not send it as a separate Oracle SQL statement |
| Internal `;` | Do not split a PL/SQL body at each semicolon |
| No observed `@`, `@@`, `WHENEVER`, `SPOOL`, `&`, `&&` in this sample | Ordinary JDBC migration is plausible for this sample; no full-estate inference |

The attachment contains an ellipsis rather than the complete original function. [T1_function.sql](fixtures/T1_function.sql) is therefore a **derived syntax fixture**, not a sanitized copy of unseen business logic. It returns the deterministic length of a CLOB, with a null branch and an explicit observer EXECUTE grant. It introduces no business data mutation. Optional invocation is approval-bound. Replacing names to match a confirmed lab must happen in source before freezing.

## Existing sanitized corpus

`evaluation/workloads/release-small.sql` contains table creation/alteration, committed DML, a procedure, package specification **and body**, a trigger with `:NEW`/`:OLD`, and an anonymous block with slash termination. The retained corpus also has invalid compilation, partial DDL, replay, changed replay, duplicate effect, inventory fixtures, DML sizes 1,000/10,000 and statement counts 10/100/1,000. These are synthetic acceptance inputs, not the actual estate corpus.

`sqlplus-directives.sql` deliberately contains PROMPT, SET DEFINE, DEFINE, SPOOL, @, @@ and WHENEVER with an include file. Those client semantics are a separate workload and are rejected conservatively by this runner. They are not stripped or silently converted. No such directives are known to be mandatory in the user's new representative function. The admission scan is deliberately conservative, not a replacement Oracle parser; directive-looking comments/literals can cause rejection and need an explicit corpus decision.

No retained script supplies the original CLOB/EDITIONABLE function body. No evidence establishes estate use or absence of substitutions, external includes, cross-schema references, edition-sensitive dependencies, dynamic SQL, database links, invoker rights, LOB encodings, or transaction boundaries.

## Executed offline evidence and runtime gaps

Flyway 13.9.0's actual Oracle parser produces two statements for T1 (complete function plus grant), two for invalid T2, three for partial T6, two for T7 and eleven for `release-small.sql`. Parser execution never connects to Oracle and cannot prove compilation, editioning, grants, driver/TLS compatibility, effect or validity.

Oracle 19c and 21c each still need exact-RU runtime tests for CLOB/function compilation and invocation, quoted names, EDITIONABLE in the selected schema/session edition, package body and dependency diagnostics, DML commit semantics, driver authentication/TLS and observer visibility. The historical 26ai lab does not certify either estate version. Schema targeting requires the writer to own the allowlisted schema; a changed CURRENT_SCHEMA is not a privilege boundary.
