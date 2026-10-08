# Database Migration Report

## Executive Summary

Runtime gate: **BLOCKED**. Actual ODC pending approval/result observations; no execution or post-migration Oracle acceptance yet. Required live migration acceptance report: **NOT_AVAILABLE**.

Evidence source: **NOT_AVAILABLE**. Observation source: **NOT_AVAILABLE**. Scope: **NOT_AVAILABLE**.

Derived result: **WAITING_APPROVAL**. Runtime result: **NOT_AVAILABLE**. Runtime-proven complete migration: **False**.

Execution stage: **WAITING_APPROVAL**. Approval state observed: **True**. Flow instance/result identity complete: **True**. Native task IDs in log: **NOT_AVAILABLE**. Workflow node IDs remain separate.

ODC execution success alone is insufficient; every environment also needs valid objects, no compilation errors, expected rows and function result.

## Application / Release

Application: `customer-profile`\
Release: `REL-2026.10-DEMO01`\
Collected: 2026-10-08T01:54:34.970437+00:00

## Source Provenance

Repository: `devsecopslonghn/DB-Research`\
Branch: `feature/github-odc-migration-demo`\
Git commit: `848e0923f3c8e2ef854298184232352ea68ed9ce`\
GitHub actor: `LOCAL_OPERATOR`\
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

| Node | Actor | Roles | Role evidence | Native status | Timestamp |
| --- | --- | --- | --- | --- | --- |
| 2000072 | odc_poc_requester | NOT_AVAILABLE | native_operator_or_matching_project_candidate | EXECUTING | NOT_AVAILABLE |
| 2000073 | odc_poc_requester | NOT_AVAILABLE | native_operator_or_matching_project_candidate | CREATED | NOT_AVAILABLE |

Project role fallback: NOT_AVAILABLE; project ID verified: NOT_AVAILABLE.
OWNER and DBA approve in ODC. Automation has no approval or Execute operation. Native manual continuation remains an operator decision.

## Execution Timeline

| Environment | Flow created | Execution start | Flow complete | Execution actor |
| --- | --- | --- | --- | --- |
| DEV | 1791398804138 | NOT_AVAILABLE | NOT_AVAILABLE | NOT_AVAILABLE |
| SIT | 1791398804139 | NOT_AVAILABLE | NOT_AVAILABLE | NOT_AVAILABLE |
| UAT | 1791398804139 | NOT_AVAILABLE | NOT_AVAILABLE | NOT_AVAILABLE |
| MOCKPROD | 1791398804139 | NOT_AVAILABLE | NOT_AVAILABLE | NOT_AVAILABLE |

Task-node operator may identify the requester; the Execute audit is the authority for the caller. Uncollected timestamps/actors remain NOT_AVAILABLE.

## Oracle Verification

| Environment | Object | Type | Status | Errors |
| --- | --- | --- | --- | --- |
| DEV | NOT_AVAILABLE | NOT_AVAILABLE | NOT_AVAILABLE | NOT_AVAILABLE |
| SIT | NOT_AVAILABLE | NOT_AVAILABLE | NOT_AVAILABLE | NOT_AVAILABLE |
| UAT | NOT_AVAILABLE | NOT_AVAILABLE | NOT_AVAILABLE | NOT_AVAILABLE |
| MOCKPROD | NOT_AVAILABLE | NOT_AVAILABLE | NOT_AVAILABLE | NOT_AVAILABLE |

| Environment | Rows: expected / actual | Active: expected / actual | Function: expected / actual |
| --- | --- | --- | --- |
| DEV | 3 / NOT_AVAILABLE | 2 / NOT_AVAILABLE | C0001:Demo Customer One / NOT_AVAILABLE |
| SIT | 3 / NOT_AVAILABLE | 2 / NOT_AVAILABLE | C0001:Demo Customer One / NOT_AVAILABLE |
| UAT | 3 / NOT_AVAILABLE | 2 / NOT_AVAILABLE | C0001:Demo Customer One / NOT_AVAILABLE |
| MOCKPROD | 3 / NOT_AVAILABLE | 2 / NOT_AVAILABLE | C0001:Demo Customer One / NOT_AVAILABLE |

## Environment Results

| Environment | ODC Ticket/Task | Native execution | Oracle verify | Demo result |
| --- | --- | --- | --- | --- |
| DEV | 2000015 | WAIT_FOR_EXECUTION | NOT_AVAILABLE | WAITING_APPROVAL |
| SIT | 2000015 | WAIT_FOR_EXECUTION | NOT_AVAILABLE | WAITING_APPROVAL |
| UAT | 2000015 | WAIT_FOR_EXECUTION | NOT_AVAILABLE | WAITING_APPROVAL |
| MOCKPROD | 2000015 | WAIT_FOR_EXECUTION | NOT_AVAILABLE | WAITING_APPROVAL |

## Failure / Correction

Corrects: `NOT_APPLICABLE`. Depends on: `NOT_APPLICABLE`.

The failure release raises ORA-20042 in SIT before index creation. UAT/MOCKPROD wait. Review/cancel the failed batch, then approve a new correction release; preserve old SQL, hashes, approvals and failure history. Already committed DDL is not automatically rolled back.

## Audit Evidence

Native batch: `2000015`. Audit collection: LIVE_PERSONAL_AUDIT_ONLY; only explicit taskId matches retained; create events may have no taskId.
Native log evidence: NOT_AVAILABLE; flow instance: 2000015; task IDs: NOT_AVAILABLE; log batch IDs: NOT_AVAILABLE.

- `https://oceanbase.apps.drgdevlab.com/api/v2/flow/flowInstances/2000015`
- `https://oceanbase.apps.drgdevlab.com/api/v2/flow/flowInstances/2000015/tasks/result`
- `https://oceanbase.apps.drgdevlab.com/api/v2/flow/flowInstances/2000015/tasks/log?logType=ALL`
- `https://oceanbase.apps.drgdevlab.com/api/v2/audit/events`

## Artifacts

Original release artifacts are verified separately; this directory retains the envelope and pending evidence, not an execution bundle. Evidence: `evidence.json`. Reports: `migration-report.md`, `migration-report.json`.

GitHub workflow run/artifact links are available when the envelope contains a real workflow run ID. Fixtures are never runtime proof.

## Final Decision

**CONDITIONAL GO** for the recorded scope. Live approval, rollout, verification and the proven retention GitOps settings are required before claiming a working internal application pilot.

Operational effort is NOT_MEASURED unless captured by an operator. No custom execution platform, direct Oracle migration executor or automatic promotion controller is introduced.

Source: [Git commit](https://github.com/devsecopslonghn/DB-Research/commit/848e0923f3c8e2ef854298184232352ea68ed9ce).
