# Research Task: Find an Open-Source Database Change Management Platform

## Background

We currently use or are evaluating Flyway for database migrations.

Flyway works well as a migration engine, but using Flyway alone leaves several operational and governance gaps when managing many databases and environments.

The problem is NOT simply finding another migration CLI.

We need a centralized Database Change Management / Database DevOps platform that can manage database changes across multiple applications, databases, and environments while reducing manual DBA operations.

Conceptually, we are looking for:

```text
Developers / DBA
       |
       v
Central Database Change Platform
+--------------------------------+
| Database Inventory             |
| Changes / Releases             |
| Review / Approval              |
| Execution History              |
| Audit                          |
| RBAC                           |
| Logs                           |
+---------------+----------------+
                |
                v
       Migration / Execution Engine
                |
        +-------+-------+
        |       |       |
     Flyway  Liquibase SQLPlus
        |       |       |
        +-------+-------+
                |
                v
              Oracle
                |
                v
      Migration state / history
```

Flyway/Liquibase integration is desirable but NOT mandatory.

A platform with its own reliable migration engine is acceptable.

---

# Primary Objective

Find existing projects that solve as much of this problem as possible.

The most important constraint is:

**The solution must have a genuinely usable FREE AND OPEN-SOURCE, SELF-HOSTED version.**

Do not rank commercial products, free trials, SaaS-only products, or products whose useful database-management functionality requires a commercial license as successful matches.

They may be listed separately for comparison only.

---

# Hard Requirements — MUST

A candidate should satisfy as many of these as possible, and any failure must be explicitly reported.

## 1. Free and Open Source

Verify:

- public source repository;
- exact license;
- whether the usable product is actually covered by that license;
- whether it is open-core;
- whether important functionality is Enterprise-only;
- database/user/environment limits;
- whether internal modification/forking is permitted.

Do NOT treat "source available" as equivalent to open source.

Do NOT trust marketing claims without checking the repository/license.

## 2. Self-hosted

Must be deployable on our own infrastructure.

Prefer:

- Docker;
- Docker Compose;
- Kubernetes/Helm;
- standalone server.

SaaS must not be required for normal operation.

## 3. Oracle Support

Oracle is a hard requirement.

Investigate actual implementation, not just a compatibility matrix.

Determine support for:

- Oracle SQL;
- DDL;
- DML;
- PL/SQL;
- procedures;
- functions;
- packages;
- triggers;
- anonymous PL/SQL blocks;
- SQLPlus-style scripts if applicable;
- Oracle JDBC/OCI/SQLPlus execution mechanism.

Identify known parser/execution limitations.

## 4. Reliable Migration / Change Execution

The system must execute database changes reliably.

Investigate exactly how changes are executed:

- custom JDBC executor;
- Flyway;
- Liquibase;
- SQLPlus;
- native database client;
- another migration engine.

## 5. Migration State / Idempotency

This is critical.

Determine whether the system records migration state in the TARGET DATABASE.

Examples:

Flyway:

```text
flyway_schema_history
```

Liquibase:

```text
DATABASECHANGELOG
```

Or an equivalent mechanism.

Determine:

- migration ID/version;
- checksum;
- success/failure;
- whether an already successful migration is skipped;
- checksum validation;
- behavior after partial failure;
- retry behavior;
- what happens if Oracle commits successfully but the control-plane process crashes before recording success.

A system that stores execution state ONLY in its own central metadata database must be clearly flagged.

## 6. Centralized Management

We need an actual server/control plane.

Examples:

```text
Central Server
      |
      +-- Oracle DEV
      +-- Oracle SIT
      +-- Oracle UAT
      +-- Oracle PROD
```

A CLI with local SQLite/JSON state does NOT satisfy this requirement.

Check whether there is:

- central metadata database;
- REST/gRPC API;
- daemon/backend;
- multi-user operation;
- multiple managed database instances.

## 7. Central History / Auditability

We should be able to answer:

```text
WHO
executed

WHAT
SQL/change/migration

WHERE
database/schema/environment

WHEN
timestamp

HOW
pipeline/manual/API/etc.

RESULT
success/failure
```

Check whether this information survives centrally and can be queried.

---

# Strongly Desired — SHOULD

Evaluate each candidate for:

- Web UI
- Database inventory
- Application/project organization
- DEV/SIT/UAT/STAGING/PROD environments
- Review workflow
- Approval workflow
- RBAC
- Separation of duties
- Git integration
- GitLab integration
- Jenkins integration
- CI/CD API
- REST API
- SSO
- OIDC
- LDAP
- audit logs
- Vault/external secret manager integration
- deployment logs
- notifications
- HA
- backup/restore
- disaster recovery

---

# Nice to Have

Evaluate:

- Flyway integration
- Liquibase integration
- SQLPlus integration
- schema diff
- drift detection
- SQL review/lint
- policy-as-code
- release promotion
- environment promotion
- SIEM integration
- Terraform provider
- Kubernetes operator/Helm chart

---

# Search Strategy

Do NOT search only for:

"Flyway UI"

Search the broader ecosystem using terms such as:

- open source database change management
- open source database DevOps
- database release management
- database deployment platform
- database migration control plane
- database CI/CD platform
- schema change management
- database governance platform
- database release orchestration
- Flyway dashboard
- Flyway server
- Liquibase dashboard
- Liquibase server
- database deployment manager
- database change approval
- Oracle DevOps database migration
- Oracle schema change management

Search:

- GitHub
- GitLab
- vendor repositories
- CNCF ecosystem
- Awesome lists
- archived projects
- forks
- projects with little/no marketing presence

A project may have an unrelated name. Search source code/dependencies where useful.

Useful dependency combinations include:

```text
flyway-core + ojdbc
liquibase-core + ojdbc
oracle.jdbc + react
oracle.jdbc + spring-security
flyway + REST API
liquibase + REST API
```

---

# Projects Already Identified

Do not simply repeat previous conclusions.

Re-evaluate them against the criteria and search for additional alternatives:

- Bytebase
- AccessFlow
- D-Band DRM
- Open Migration
- SchemaPilot
- Flyway UI
- Flyway Play
- Liquibase Community
- Flyway OSS
- Sqitch
- Atlas
- Yearning
- Archery

Also investigate forks and derivative projects.

---

# Bytebase

Treat Bytebase as an important reference architecture.

Current Bytebase provides the kind of centralized control plane we are looking for.

However, investigate carefully:

- Community limits;
- database instance limits;
- open-core boundaries;
- MIT vs Enterprise licensed code;
- whether the free/open-source version is realistically usable for a large internal database estate.

Do NOT suggest bypassing license enforcement.

---

# AccessFlow

Specifically verify whether newer versions have addressed the previously identified issue:

```text
Change Set
    |
central metadata
    |
JDBC execution
    |
Oracle
```

Check whether it now has:

- target-side migration ledger;
- checksum validation against target;
- already-applied detection;
- reliable retry semantics.

Do not assume earlier findings still apply.

---

# D-Band DRM

Determine whether it now has:

- central server;
- shared metadata database;
- web UI;
- multi-user operation;

rather than only CLI + local SQLite/JSON.

---

# Evidence Requirements

Do not make important claims without evidence.

For GitHub findings provide:

- repository;
- current commit SHA or release/tag;
- file;
- relevant lines;
- permanent GitHub link pinned to commit/tag.

For documentation provide direct official documentation links.

Prefer:

1. source code;
2. license files;
3. official documentation;
4. release notes;
5. issues/discussions;
6. third-party sources only when necessary.

---

# Maturity Assessment

For each candidate report:

- first release/date if available;
- latest release;
- release frequency;
- stars;
- forks;
- contributors;
- commit activity;
- open issues;
- Docker image availability;
- documentation quality;
- security policy;
- CVE/security process;
- whether development appears maintained;
- evidence of production use if available.

Do NOT equate GitHub stars with production readiness.

---

# Required Candidate Matrix

Produce:

| Platform | OSS License | Fully Free? | Self-hosted | Oracle | Target Ledger | Central Server | Web UI | History | Audit | RBAC | Approval | GitLab | Jenkins | Maturity |

Use:

```text
YES
PARTIAL
NO
UNKNOWN
```

Do not hide uncertainty.

---

# Critical Knockout Matrix

Produce a second smaller table:

| Platform | Free OSS | Oracle | Reliable Migration State | Central Control Plane | Result |

A candidate should remain in the final shortlist only if it can realistically satisfy:

```text
FREE/OSS
    +
SELF-HOSTED
    +
ORACLE
    +
RELIABLE MIGRATION
    +
CENTRAL MANAGEMENT
```

If nothing satisfies all five, explicitly say so.

Do NOT lower the criteria just to produce a winner.

---

# Architecture Analysis

For every final candidate draw its actual execution path.

Example:

```text
Web UI
   |
Backend
   |
Flyway
   |
Oracle
   |
flyway_schema_history
```

versus:

```text
Web UI
   |
Backend metadata
   |
JDBC
   |
Oracle

No target-side ledger
```

This distinction is critical.

---

# Gap Analysis

If no existing open-source platform satisfies the requirements, determine the smallest realistic gap that would need to be implemented.

For example:

```text
Option A

AccessFlow
    +
Flyway execution adapter
```

or:

```text
Option B

Existing Flyway-based project
    +
Oracle support
    +
RBAC
```

or:

```text
Option C

Thin control plane
    |
Jenkins
    |
Flyway / SQLPlus
```

Estimate the engineering scope rather than simply saying "build your own."

---

# Final Output

Produce:

## 1. Executive Summary

What exists and whether a genuinely usable open-source solution was found.

## 2. Hard-Requirement Matrix

Evidence-based comparison.

## 3. Detailed Candidate Analysis

Architecture, license, Oracle implementation, migration semantics and limitations.

## 4. Final OSS Shortlist

Maximum 5 candidates.

Do not include commercial-only products.

## 5. Rejected Candidates

For each rejected project state the exact knockout reason.

Examples:

```text
NO ORACLE
NO CENTRAL SERVER
NO TARGET MIGRATION STATE
COMMERCIAL ONLY
COMMUNITY LIMIT TOO RESTRICTIVE
ABANDONED
```

## 6. Best PoC Candidates

Identify candidates worth installing and testing.

## 7. Required Oracle PoC

For each surviving candidate test:

- CREATE TABLE
- ALTER TABLE
- INSERT/UPDATE
- procedure
- function
- package
- trigger
- anonymous PL/SQL
- `/` delimiter
- SQLPlus commands
- intentional failure
- retry
- partial DDL
- process crash after DB commit
- network interruption

## 8. Evidence Pack

Provide source/documentation evidence for every major conclusion.

## 9. Remaining Gaps

What still prevents the OSS solution from replacing a commercial database change management platform.

Do not optimize the research for finding a winner.

Optimize it for establishing the truth.