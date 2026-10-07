# Additional candidate analysis

This document records the original five additional source candidates.
The [product-model revision](PRODUCT-MODEL.md) adds ODC and updates primary platform selection.
None of these original five candidates became a complete platform.
Five additional repositories received source review.
Jenkins and Rundeck remain proposed compositions.
They do not enter the verified platform shortlist.

## Findings

| Candidate | License | Oracle mechanism | Target state | Central service | Exact gap |
|---|---|---|---|---|---|
| .NET dbdeploy (`gigi81/dbdeploy`) | MIT | Oracle Managed Data Access | Script name, hash, user, and deployment time | NO | NO CENTRAL SERVER |
| DbMaintain | Apache-2.0 | JDBC or native SQLPlus | `DBMAINTAIN_SCRIPTS` | NO | NO CENTRAL SERVER. DEPRECATED. |
| dbpm | Apache-2.0 CLI. Required Core coverage UNKNOWN. | SQLcl or SQLPlus | Core package state. Complete ledger semantics UNKNOWN. | NO | NO CENTRAL SERVER. CORE REVIEW INCOMPLETE. |
| dbward core | Apache-2.0. Commercial identity and plan code. | PostgreSQL and MySQL drivers | `schema_migrations`, version only | YES | NO ORACLE. NO TARGET CHECKSUM VALIDATION. |
| CloudBeaver Community | Apache-2.0 core | Oracle Thin JDBC | No target migration ledger in the reviewed editor path | YES | NO TARGET MIGRATION STATE. NO RELEASE WORKFLOW. |
| Jenkins + Flyway proposal | MIT core + Apache-2.0 engine | Flyway Oracle JDBC | Flyway target history | Requires database inventory and central release records | IMPLEMENTATION AND VERIFICATION REQUIRED |
| Rundeck + Flyway proposal | Apache-2.0 core and engine | Flyway Oracle JDBC | Flyway target history | Requires approval and central release records | IMPLEMENTATION AND VERIFICATION REQUIRED |

These findings come from source inspection.
No application or Oracle execution occurred.
The permanent source links are in [EVIDENCE.md](EVIDENCE.md#source-references).

## .NET dbdeploy

The inspected repository is `gigi81/dbdeploy`.
Its Oracle connector uses Oracle Managed Data Access.
Its target table stores script name, deployment time, user name, and hash.
It provides an execution component and command interface.
It has no shared change approval service or database estate interface. [DEP-L, DEP-ORA, DEP-STATE](EVIDENCE.md#source-references)

The name also refers to an older Java project.
This research did not inspect that project's complete release source or license.
The .NET findings must not be assigned to every project named dbdeploy.

## DbMaintain

The repository has an Apache-2.0 license.
It documents JDBC execution and an optional native SQLPlus runner.
Its target script table tracks executed scripts.
The maintainer explicitly states that the project is deprecated and no longer maintained.
The project lacks a central control plane independently of that maintenance issue. [MAINT-L, MAINT-SCOPE](EVIDENCE.md#source-references)

The [official documentation](https://dbmaintain.github.io/docs/) describes script registration and Oracle procedural handling.
Source support does not establish compatibility with current Oracle versions or current Java deployments.

## dbpm

The Python command interface has an Apache-2.0 license.
It requires SQLcl or SQLPlus and an in-database Core substrate.
The reviewed command repository does not establish the complete Core license and recovery behavior.
The README distinguishes lockfile checksum verification from non-lockfile installation.
The project has no multi-user central service. [PM-L, PM-SCOPE, PM-LIMITS](EVIDENCE.md#source-references)

The changelog records version 1.5.3 on 2026-09-10.
A recent version does not prove central governance or safe Oracle DDL recovery.

## dbward

The public core includes a central server, execution agents, approval rules, and audit records.
Its database driver implementations support PostgreSQL and MySQL.
The migration runner skips versions already present in `schema_migrations`.
That target table stores only the version.
It does not store an applied script checksum. [WARD-SCOPE, WARD-STATE, WARD-RUN](EVIDENCE.md#source-references)

This corrects the initial independent draft, which missed the migration runner.
The project still fails Oracle support.
A declared dbmate-compatible file format does not establish Oracle execution.

OIDC and group authorization have commercial boundaries.
The documented Free distribution allows three database connections and twenty active users.
The license separates Apache core source from commercial plan enforcement.
A complete OSS build and its scale limits therefore need separate verification. [WARD-L, WARD-BOUNDARY, WARD-PLAN](EVIDENCE.md#source-references)

The inspected README establishes a Slack approval interface.
A general browser database inventory interface remains UNKNOWN in this review.

## CloudBeaver Community

CloudBeaver has a shared server and browser database editor.
Its public server declares an Oracle Thin JDBC driver.
The editor does not establish target migration checksums, release approval, or applied migration detection.
Oracle connectivity alone does not satisfy change management. [CB-L, CB-ORA, CB-SCOPE](EVIDENCE.md#source-references)

Commercial editions have additional identity and administration features.
Unreviewed edition-specific audit and identity features remain UNKNOWN in the comparison.

## Proposed compositions

```text
Jenkins or Rundeck central service
                |
Custom database inventory and immutable release records
                |
Approval bound to artifact, target, and environment
                |
Worker -> Flyway Community -> Oracle target history
                |
Central result records and reconciliation
```

Jenkins provides [pipeline input and submitter restrictions](https://www.jenkins.io/doc/pipeline/steps/pipeline-input-step/).
Pipeline code must bind approval to the exact release artifact.
Jenkins administrator powers and the default approval permissions require careful configuration.

Rundeck provides [job access policies](https://docs.rundeck.com/docs/learning/howto/acls/).
Those policies do not establish a complete database release approval workflow.
Job logs also require structured release records and retention controls.

Flyway provides a target ledger and normal applied-version detection.
Oracle DDL recovery remains a separate acceptance item. [FW-ORA, FW-EXEC, FW-FAIL](EVIDENCE.md#source-references)
Neither composition was implemented here.

## Other searches and fork limits

Harness Open Source core licensing does not establish Database DevOps module licensing.
The [self-managed enterprise reference](https://developer.harness.io/docs/self-managed-enterprise-edition/reference-architecture) requires licensing.
A complete, free, self-hosted OSS Database DevOps module was not established.
This report does not assert retirement or a historical module license without evidence.

The fork review used a documented sample.
The `Tareya/devops-archery` derivative received direct source review.
Its inspected Oracle workflow retains direct execution without a target migration ledger. [FORK-EXEC](EVIDENCE.md#source-references)
No inspected fork passed all requirements.
That result does not prove that no suitable fork exists.

The [search record](evidence/additional-search.md) identifies the scope and execution limits.
