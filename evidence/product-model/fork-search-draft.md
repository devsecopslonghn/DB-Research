# Bytebase Forks and Alternatives Research

## Bytebase Forks
We investigated several recent forks of Bytebase listed in `evidence/api/bytebase__bytebase/forks.json` (such as `whatif-dev/db-tools-bytebase`, `camillanapoles/bytebase-Database-governance`, and `FarendraAugust/fariskha-sqlite`). 
- **Findings**: These repositories are synchronized forks rather than independent derivatives. While they contain recent commits, tracing the `HEAD` commit against the upstream `bytebase/bytebase` repository (`git merge-base`) confirmed that these commits are identical to the upstream history.
- **Conclusion on Forks**: No meaningful, independently evolved forks of Bytebase were verified in this search. (Note: This does not mean no fork exists anywhere, but none was verified among the accessible candidates).

## Alternative Platforms Search

We searched for additional platforms fitting the same product model (projects, database inventory, environments, approvals, rollout, promotion).

### 1. Archery
- **Classification**: B (SQL governance portal)
- **Details**: A widely used open-source SQL auditing platform. While it supports approvals and SQL execution, it functions more as a query and audit portal rather than a full DevOps rollout platform with project/environment promotion models akin to Bytebase.

### 2. Yearning
- **Classification**: B (SQL governance portal)
- **Details**: A Go-based SQL audit and management platform for MySQL. It provides SQL review, execution, and rollback, but focuses on auditing and query security rather than CI/CD pipeline integration and environment promotions.

### 3. Flyway / Liquibase
- **Classification**: C (Engine/UI)
- **Details**: These are standard database migration engines. While they handle schema versions and apply changes, they lack the built-in collaborative UI, instance inventory, and project-based approval workflows of a comprehensive platform out-of-the-box.

### Conclusion
**No winner**. No free, open-source, self-hosted platform with the exact Bytebase product model (complete with projects, environments, and central history) was verified during this search.

## Access Notes
- The anonymous GitHub API quota was exhausted, which limited automated large-scale querying of historical forks.
- We relied on web search, Gitee, and cloning specific candidate forks (using public pages and git) to check their commit history against the upstream repository to verify lineage.
