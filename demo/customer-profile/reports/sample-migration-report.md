# Database Migration Report

## Executive Summary

Evidence source: **FIXTURE**. Scope: **SAMPLE / DEMO — fixture simulation**.

Derived result: **VERIFIED**. Runtime result: **NOT_AVAILABLE**. Runtime-proven complete migration: **False**.

ODC execution success alone is insufficient; every environment also needs valid objects, no compilation errors, expected rows and function result.

## Application / Release

Application: `customer-profile`\
Release: `REL-2026.10-DEMO01`\
Collected: SAMPLE_TIMESTAMP

## Source Provenance

Repository: `devsecopslonghn/DB-Research`\
Branch: `SAMPLE / DEMO`\
Git commit: `0000000000000000000000000000000000000000`\
GitHub actor: `SAMPLE_ACTOR`\
GitHub run: `NOT_AVAILABLE`\
Manifest SHA-256: `406741b739cdec2d0c628950204319cb882ba3cd73961ce2992c374f051c1347`\
Ordered SQL SHA-256: `3ddce47b1a7675f1f02f349b21f0647437cd7693229fd560472df2a7c0338854`

## Migration Files

| File | SHA-256 | Type | Static status |
| --- | --- | --- | --- |
| 001_create_customer_table.sql | 09d5a78bf5e17b5686e56df8624870d2be0bb4c168cb658c0a7d3afe94f1d102 | TABLE | VALIDATED |
| 002_create_customer_sequence.sql | f7d0763c8ce610310b1320276aaad36083c5416ea634b4c41d9d0abebdd5f838 | SEQUENCE | VALIDATED |
| 003_create_customer_index.sql | 6f6d297e90f75d07d5c916097712f783b8b31b09b9e419ec951c2a4a0641aef6 | INDEX | VALIDATED |
| 004_create_customer_function.sql | 07c54e7d8105a171d9ecf6ad210903716e419d9dfb09066f3ca255d5b41b8da1 | FUNCTION | VALIDATED |
| 005_create_customer_view.sql | 37b0b21e054c7d9370149903b4604b4c2bbc12742b0fd624bb96cbe12cc877bc | VIEW | VALIDATED |
| 006_seed_reference_data.sql | b82e3f24b24e6ceabad4c571d564cdf294d7059af4af40fb4b3266d6b0c69991 | INSERT | VALIDATED |

## Static Validation

| File | Level | Pattern | Line |
| --- | --- | --- | --- |
| All migration files | INFO | No listed dangerous pattern | — |

Lexical analysis is not a complete Oracle parser. Dynamic SQL and dependencies require DBA review.

## Target Environments

| Environment | ODC database | Datasource | Owner schema |
| --- | --- | --- | --- |
| DEV | 1000069 | 1000001 | ODC_POC_20261004_DEV |
| SIT | 1000122 | 1000002 | ODC_POC_20261004_SIT |
| UAT | 1000184 | 1000003 | ODC_POC_20261004_UAT |
| MOCKPROD | 1000218 | 1000004 | ODC_POC_20261004_MOCKPROD |

All four owner schemas are isolated logical environments on one Oracle service; MOCKPROD is a lab schema.

## Review and Approval

| Node | Actor | Native status | Timestamp |
| --- | --- | --- | --- |
| SAMPLE_OWNER | SAMPLE_OWNER | COMPLETED | SAMPLE_TIMESTAMP |
| SAMPLE_DBA | SAMPLE_DBA | COMPLETED | SAMPLE_TIMESTAMP |

OWNER and DBA approve in ODC. Automation has no approval or Execute operation. Native manual continuation remains an operator decision.

## Execution Timeline

| Environment | Flow created | Execution start | Flow complete | Execution actor |
| --- | --- | --- | --- | --- |
| DEV | NOT_AVAILABLE | SAMPLE_TIMESTAMP | SAMPLE_TIMESTAMP | SAMPLE_OPERATOR |
| SIT | NOT_AVAILABLE | SAMPLE_TIMESTAMP | SAMPLE_TIMESTAMP | SAMPLE_OPERATOR |
| UAT | NOT_AVAILABLE | SAMPLE_TIMESTAMP | SAMPLE_TIMESTAMP | SAMPLE_OPERATOR |
| MOCKPROD | NOT_AVAILABLE | SAMPLE_TIMESTAMP | SAMPLE_TIMESTAMP | SAMPLE_OPERATOR |

Task-node operator may identify the requester; the Execute audit is the authority for the caller. Uncollected timestamps/actors remain NOT_AVAILABLE.

## Oracle Verification

| Environment | Object | Type | Status | Errors |
| --- | --- | --- | --- | --- |
| DEV | DM_CP_CUSTOMER | TABLE | VALID | 0 |
| DEV | DM_CP_CUSTOMER_SEQ | SEQUENCE | VALID | 0 |
| DEV | DM_CP_CUSTOMER_STATUS_IX | INDEX | VALID | 0 |
| DEV | DM_CP_LABEL | FUNCTION | VALID | 0 |
| DEV | DM_CP_ACTIVE_CUSTOMERS | VIEW | VALID | 0 |
| SIT | DM_CP_CUSTOMER | TABLE | VALID | 0 |
| SIT | DM_CP_CUSTOMER_SEQ | SEQUENCE | VALID | 0 |
| SIT | DM_CP_CUSTOMER_STATUS_IX | INDEX | VALID | 0 |
| SIT | DM_CP_LABEL | FUNCTION | VALID | 0 |
| SIT | DM_CP_ACTIVE_CUSTOMERS | VIEW | VALID | 0 |
| UAT | DM_CP_CUSTOMER | TABLE | VALID | 0 |
| UAT | DM_CP_CUSTOMER_SEQ | SEQUENCE | VALID | 0 |
| UAT | DM_CP_CUSTOMER_STATUS_IX | INDEX | VALID | 0 |
| UAT | DM_CP_LABEL | FUNCTION | VALID | 0 |
| UAT | DM_CP_ACTIVE_CUSTOMERS | VIEW | VALID | 0 |
| MOCKPROD | DM_CP_CUSTOMER | TABLE | VALID | 0 |
| MOCKPROD | DM_CP_CUSTOMER_SEQ | SEQUENCE | VALID | 0 |
| MOCKPROD | DM_CP_CUSTOMER_STATUS_IX | INDEX | VALID | 0 |
| MOCKPROD | DM_CP_LABEL | FUNCTION | VALID | 0 |
| MOCKPROD | DM_CP_ACTIVE_CUSTOMERS | VIEW | VALID | 0 |

| Environment | Rows: expected / actual | Active: expected / actual | Function: expected / actual |
| --- | --- | --- | --- |
| DEV | 3 / 3 | 2 / 2 | C0001:Demo Customer One / C0001:Demo Customer One |
| SIT | 3 / 3 | 2 / 2 | C0001:Demo Customer One / C0001:Demo Customer One |
| UAT | 3 / 3 | 2 / 2 | C0001:Demo Customer One / C0001:Demo Customer One |
| MOCKPROD | 3 / 3 | 2 / 2 | C0001:Demo Customer One / C0001:Demo Customer One |

## Environment Results

| Environment | ODC Ticket/Task | Native execution | Oracle verify | Demo result |
| --- | --- | --- | --- | --- |
| DEV | SAMPLE_BATCH_HAPPY | EXECUTION_SUCCEEDED | VERIFIED | VERIFIED |
| SIT | SAMPLE_BATCH_HAPPY | EXECUTION_SUCCEEDED | VERIFIED | VERIFIED |
| UAT | SAMPLE_BATCH_HAPPY | EXECUTION_SUCCEEDED | VERIFIED | VERIFIED |
| MOCKPROD | SAMPLE_BATCH_HAPPY | EXECUTION_SUCCEEDED | VERIFIED | VERIFIED |

## Failure / Correction

Corrects: `NOT_APPLICABLE`. Depends on: `NOT_APPLICABLE`.

The failure release raises ORA-20042 in SIT before index creation. UAT/MOCKPROD wait. Review/cancel the failed batch, then approve a new correction release; preserve old SQL, hashes, approvals and failure history. Already committed DDL is not automatically rolled back.

## Audit Evidence

Native batch: `SAMPLE_BATCH_HAPPY`. Audit collection: FIXTURE.

- `SAMPLE_ONLY: reviewed ODC approval/Execute audit`

## Artifacts

Release artifact: `release-envelope.json`, `release-bundle/`. Evidence: `evidence.json`. Reports: `migration-report.md`, `migration-report.json`.

GitHub workflow run/artifact links are available when the envelope contains a real workflow run ID. Fixtures are never runtime proof.

## Final Decision

**CONDITIONAL GO** for the recorded scope. Live approval, rollout, verification and the proven retention GitOps settings are required before claiming a working internal application pilot.

Operational effort is NOT_MEASURED unless captured by an operator. No custom execution platform, direct Oracle migration executor or automatic promotion controller is introduced.
