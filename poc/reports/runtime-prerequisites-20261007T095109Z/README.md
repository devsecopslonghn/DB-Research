# CI/Flyway runtime prerequisites — 7 October 2026

**NO-GO for runtime entry/adoption; T1–T7 remain BLOCKED, not executed. Oracle feasibility is undetermined.** The user authorized T1–T7 on one approved isolated Oracle target, including T7's loss instrumentation. No approved target/credential references, real actor assignments, source repository or JDBC policy answer have yet been supplied. Those inputs were requested while local preparation continued; absence of an answer was not treated as consent.

No feature, architecture, executor or verifier change was made. No ODC investigation was reopened. No Oracle connection or SQL, credential borrowing, Jenkins job/security/agent update, push or deployment occurred. Previous evidence remains unchanged.

## Completed prerequisites and local checks

| Check | Result | Evidence |
| --- | --- | --- |
| Existing Flyway engine | PASS: 13.9.0; SHA-256 `971d79cfebe8d6caa38dae3676dadbf222d40767385f436b87293a4894d1475a`, matches retained accepted local artifact | [Engine readback](engine_version.log), [checks](local-prerequisite-checks.json) |
| Existing Oracle parser | PASS on unchanged T1/T2/T6/T7 fixtures: 2/2/3/2 statements | [Parser readback](parser.log) |
| Missing Python observer dependency | Resolved in private **preparation** venv: `oracledb==3.4.0` and dependency wheels installed; exact versions/hashes retained | [Wheel pins](python-wheel-pins.json), [versions](versions.log), [dependency check](dependencies.log) |
| Unchanged runner package | Built/installed from a byte-matching private copy; isolated `python -I -m poc.runner --help` PASS | [Entry point](installed_entrypoint.log), [source match and wheel hash](local-prerequisite-checks.json) |
| Local safety checks | PASS, 30 existing tests against the isolated installed package; actual SQLite/fake Oracle adapters | [Test log](local_tests.log). This is not T1–T7 runtime evidence |
| Cached JDBC artifact | Exact 21.18.0.0 jar exists; hash recorded and Maven repository checksum matches. Execution approval remains absent | [Discovery](prerequisites-discovery.json) |

Preparation directory: `/tmp/ci-flyway-runtime-20261007.o112kqhj`; venv `venv/`. This is **not** the protected persistent Jenkins agent required for acceptance. No credential or enabled target was installed there. System Python and repository implementation files were unchanged. The first private wheel staging attempt omitted the report Python package; staging was corrected and the final build passed without a repository edit.

## Remaining runtime gates

| Required owner input / observed gate | Current evidence | Why execution waits |
| --- | --- | --- |
| DBA: approved existing isolated owner schema and separate writer/observer references | No POC credential/configuration environment variables injected; no confirmed target supplied | Historical routes and example `OSS_POC_WRITER` names do not authorize an actual target. Need current identity/version/TLS/grants and confirmation of no prior uncertain work before first write |
| Software-policy owner: Oracle FUTC JDBC connectivity exception | Cached driver is available; example policy `approved=false`; no answer to the explicit exception question | Do not silently convert an OSS-only requirement into a driver exception |
| CI owner: named requester/reviewer/executor and authorized DBA recovery owner | Existing account records were inspected as metadata only; no role assignment or authenticated per-release approval supplied | Do not fabricate identities or use CLI actor strings as authenticated approval. T7/T2 HOLD closure needs actual session/history/effect inspection and an authorized DBA decision before subsequent cases |
| CI owner: protected pipeline/job and restricted persistent agent | Jenkins Ready; global strategy `FullControlOnceLoggedInAuthorizationStrategy`; controller executors 0; two shared NORMAL SSH agents; neither has `oracle-oss-poc` label; no Kubernetes agent templates and no reference job markers in 24 inspected job configs | Source-author access to job/agent/config must be excluded or an explicit trusted-operator boundary established. Existing plugin/controller availability does not prove it. No global security settings or other jobs were changed |
| Source owner: approved Git repository/commit | Research root has no Git metadata; no source selected | A newly manufactured research commit is not approved release provenance; fixture SQL and expectations must be frozen from the supplied source |
| CI owner: credentials binding, retained artifacts and SQLite backup | No protected POC job/agent configured | Temporary preparation files cannot substitute for persistent admission and retained evidence |

The observed Jenkins strategy permits logged-in users to administer Jenkins. The team must establish the intended trusted-operator/source-author boundary for this job; changing the shared controller's global permissions is not an incidental POC edit. [Official Jenkins access-control documentation](https://www.jenkins.io/doc/book/security/access-control/).

## Oracle acceptance record

[cases.json](cases.json) records all seven cases as **BLOCKED**, including their unchanged fixture hashes, engine/driver hashes, expected outcome, missing runtime inputs and explicit no-execution flags. It does not overwrite [the original blocked attempt](../oracle-attempt-20261007/cases.json). The existing [test plan](../../test-plan.md) still governs ordering and HOLD/recovery: T1 → T3 → T4 → T5 → T7 → authorized recovery → T2 → authorized recovery → T6 last.

The next action is to supply the pending target/credential references, actor and protected CI/Git assignments, and JDBC decision. Then complete the existing runtime gates and execute that sequence on the one approved target. No additional feature or architecture work is proposed.
