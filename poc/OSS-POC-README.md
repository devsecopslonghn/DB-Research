# Single-target OSS Oracle change-management POC

Implementation round: 7 October 2026. The user's new mission selects the OSS CI composition and supersedes older commercial-first next-step recommendations **for this POC only**. Historical research, expected outcomes and candidate results remain intact.

**Current runtime follow-up:** [prerequisite evidence](reports/runtime-prerequisites-20261007T095109Z/README.md) and [T1–T7 records](reports/runtime-prerequisites-20261007T095109Z/cases.json). Local dependency/installed-runner preparation is complete with unchanged implementation; execution remains gated on approved target/credential, actual actor/CI/Git and JDBC-policy inputs. No Oracle case or Jenkins configuration change occurred.

**Selected engine: Flyway Community 13.9.0, Apache-licensed Maven libraries. Selected orchestrator: the existing Jenkins 2.568.3-jdk21.** No new controller, database, portal, queue, secret manager or governance product was deployed. The runnable Python package, protected Jenkins pipeline, Flyway API entry point, SQLite admission and HTML/JSON reports are implemented. [Results](results.md) separate executed local checks from blocked Oracle/CI acceptance. Adoption is NO-GO pending runtime evidence; feasibility is undecided.

| Deliverable | Contents |
| --- | --- |
| [Workload profile](workload-profile.md) | Actual sample boundary, static corpus, grammar and remaining 19c/21c checks |
| [Engine selection](engine-selection.md) | One engine, exact pins, offline parser evidence and driver license boundary |
| [Lab topology](lab-topology.md) | Existing lab/CI observations, nonsecret route, unconfirmed principals/identity |
| [Architecture](architecture.md) | Trust boundaries, approval, admission, verification, hold and retention |
| [Test plan](test-plan.md) | Local negatives and staged T1–T7 runtime protocol |
| [Results](results.md) | Evidence-backed local results, runtime blockers and adoption decision |
| [Jenkins pipeline](ci/Jenkinsfile) | Target choice, authenticated human gates and static artifacts |
| [Inventory example](inventory/targets.example.json) | Disabled single-target configuration; never use unchanged for execution |
| [Actor/engine policy example](inventory/policy.example.json) | Empty roles, unapproved engine checksum and driver exception |

## Local verification

Run from `DB-Research`:

```sh
python3 -m unittest discover -s poc/tests -v
mvn -q -f poc/runner/java/pom.xml clean package
java -jar poc/runner/java/target/oss-oracle-runner-1.0.0.jar --version
java -cp poc/runner/java/target/oss-oracle-runner-1.0.0.jar org.example.poc.ParserProbe \
  poc/fixtures/T1_function.sql poc/fixtures/T2_invalid.sql \
  poc/fixtures/T6_partial.sql poc/fixtures/T7_lost_result.sql evaluation/workloads/release-small.sql
python3 tools/verify_research_documents.py
```

Safety tests use Python's standard library and synthetic identities/Oracle adapters. `ParserProbe` uses the real Flyway Oracle parser and cannot connect to a database. The observer needs `oracledb==3.4.0`; install a reviewed copy of this package in an operator-owned virtual environment with `python -m pip install /path/to/DB-Research/poc`. Jenkins invokes `python -I -m poc.runner`: source-workspace Python modules and `PYTHONPATH` cannot override the installed runner. The Java wrapper uses internal version/parser APIs, so upgrades require this build/parser regression.

## Before a real run

The DBA/platform owner must supply the approved writer/observer references, exact version, database/PDB identity, single schema and restricted grants. The CI owner must supply real actor IDs, protected job configuration, restricted agent and protected persistent storage. This workspace has no Git metadata; the SQL and expectation JSON must first exist at an exact commit in the approved source repository. Do not manufacture a commit for lab evidence.

Set these **operator-owned** environment references, outside the source workspace:

```text
OSS_POC_INVENTORY=/var/lib/oracle-oss-poc/config/targets.json
OSS_POC_POLICY=/var/lib/oracle-oss-poc/config/policy.json
OSS_POC_STATE_DIR=/var/lib/oracle-oss-poc/state
OSS_POC_ENGINE_JAR=/var/lib/oracle-oss-poc/engine/oss-oracle-runner-1.0.0.jar
OSS_POC_ORACLE_DRIVER_JAR=/var/lib/oracle-oss-poc/engine/ojdbc11-21.18.0.0.jar
OSS_POC_REPORT_DIR=<protected report directory or Jenkins workspace projection>
OSS_POC_WRITER_PASSWORD=<injected by approved credential mechanism>
OSS_POC_OBSERVER_PASSWORD=<injected separately>
```

These are names and placeholder references, not secret values. No password, URL or schema is accepted as a release input. Inventory/policy and the installed runner must be writable only by trusted operators. Protect the entire agent OS: other jobs/users must not inspect its environment, processes or state. Copy the inventory example into protected configuration; `probe --target-id oracle-lab` reads identity/version using separate injected principals without changing Oracle. Compare the result with DBA records, review the complete target, then enable it.

The default Maven build excludes Oracle JDBC. Its exact `ojdbc11:21.18.0.0` POM/jar carries Oracle FUTC, not an OSS license. If the user allows the no-fee connectivity exception, use an independently supplied, reviewed driver file and set `oracle_driver.approved=true` plus its SHA-256 in protected policy. Otherwise the selected JDBC engine cannot meet a literal all-dependencies-OSS rule; execution stays blocked. Neither an OSS wrapper nor an extension's UPL license changes the driver's license.

Freeze and approve only after the operator settings are confirmed:

```sh
python -I -m poc.runner freeze --release-id "$POC_RELEASE_ID" --git-commit "$POC_COMMIT" \
  --version "$POC_VERSION" --target-id oracle-lab --actor "$POC_REQUESTER" \
  --repo "$POC_SOURCE_REPO" --sql poc/fixtures/T1_function.sql --expected poc/fixtures/T1_expected.json
python -I -m poc.runner review --release-id "$POC_RELEASE_ID"
python -I -m poc.runner approve --release-id "$POC_RELEASE_ID" --actor "$POC_REVIEWER" --binding "$POC_BINDING"
python -I -m poc.runner execute --release-id "$POC_RELEASE_ID" --actor "$POC_EXECUTOR"
```

CLI actor arguments are trusted CI assertions, not authentication. The ordinary user cannot call this CLI as the restricted service or access state/secrets. The Jenkins input gates capture actual submitter IDs; the policy checks roles and separation again. Manual trusted-operator invocation is preparation/testing, not proof of authenticated UI approval. No real human approval was obtained in this round.

The fixture schema names are proposed, not provisioned. If the approved existing schema differs, sanitize the whole SQL in Git **before freezing and reviewing**; preserve the syntax and record a new hash. No runtime placeholder rendering is enabled.

## Held outcomes

`recover-orphans` acquires the same OS execution lock before changing stranded RUNNING rows to UNKNOWN_OUTCOME. Never run it against a different state copy to infer liveness. `reconcile` performs only dictionary/effect reads and explicitly approved deterministic function calls; it records evidence without turning an unknown release into success or unlocking the target. The DBA must separately inspect engine history and sessions. `close-hold` needs a policy-authorized recovery owner, the reconciliation hash and an operator-owned JSON attestation with `sessions_clear`, `engine_history_checked`, `effects_inspected` all true. It records HOLD permanently and permits only **new** release identities. It performs no repair, retry, rollback or Oracle cleanup.

SQLite must live on a private, persistent **local POSIX filesystem** on one restricted agent. Do not put it on NFS or run several state copies. Use SQLite's online backup API and archive protected evidence with the state. After restore, disable inventory and reconcile Oracle effects/history/sessions before enabling dispatch; a stale metadata restore can otherwise lose knowledge of committed work. Backup/restore acceptance and owner assignment remain pending.

There is no environment promotion in this phase. Follow [T1–T7](test-plan.md); a failure/unknown result cannot become a usable promotion predecessor.
