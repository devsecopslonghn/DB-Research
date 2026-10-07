# Focused ODC runtime evidence — 7 October 2026

This folder is a new isolated evidence record. Historical ODC/Bytebase files are preserved. [Plan](../../evaluation/odc-practical-poc-plan.md) and [results](../../evaluation/odc-practical-poc-results.md) explain the scope and conditional decision.

- [Cases](cases.json): 12 bounded case records, including separate before-replacement captures. Ten PASS, one PARTIAL (automatic INVALID reporting), one FAIL (new log/result/download retrieval after approved replacement).
- [Readiness](readiness.json), [cluster baseline](cluster-before.json), [runtime review](runtime-before-replacement-review.json): exact schemas, current Oracle TCPS/version/grants/observer, legitimate roles, no active new tickets and 26 unchanged historical ticket SQL/status records.
- [A1](a1.json), [A2](a2.json): distinct role journey and permitted approved requester dispatch.
- [B1](b1.json), [B2](b2.json): one native batch and manual environment/failure boundaries; B2 deliberately cancelled before later environments.
- [C1](c1.json), [C2](c2.json): valid/invalid EDITIONABLE functions and explicit ODC DBA postchecks.
- [D before](d-before.json), [D after](d-after.json), [replacement](replacement-action.json), [cluster/files after](cluster-after.json), [audit](audit-before.json): successful/failed new-ticket metadata, SQL, results, meaningful task logs, ZIP entries and downloads with hashes before replacement. After replacement metadata/SQL/audit remain PRESERVED, logs/results/downloads MISSING; all 96 ASYNC file hashes survive.
- [E1](e1.json), [E2](e2.json), [E3](e3.json): safe duplicates, new correction ticket and description/API provenance.
- [Post-replacement review](runtime-after-replacement-review.json), [secret scan](secret-scan.json): historical tickets still unchanged, new tickets terminal, credential values absent.
- [Unapplied configuration proposal](retention-storage-proposal.yaml): separate reviewable retention hypothesis; no cluster change authorized by this file.
- [Preservation baseline](preservation-before.json), [review checks](preservation-after.json), [document verifier](document-checks.json): 54 historical files unchanged; only evaluation/README.md intentionally updated among baseline files; case fields/links/JSON and repository document checks pass.

All new change execution uses ODC's native API/task executor and existing project role identities. Oracle postchecks use ODC's console API; the existing Oracle observer performs readiness SELECTs only. No new browser capture/GUI ergonomics acceptance is claimed. The underlying 12 SQL artifacts/tickets and selected endpoint responses are retained as adjacent files. Attachments retain checksum plus decoded ZIP entries; private authentication and raw administrative responses are not published.

Disposable probes are under `/tmp/odc-practical-poc-20261007/` on the local workstation. `area_d_after.py` is the prepared read-only comparison for the same retention pair, 2000005/2000007; it never replaces a pod or executes SQL. It completed after the approved ordinary application-pod replacement. The result is retained in d-after.json. A temporary storage/stable-executor configuration experiment, including ODC-only Argo synchronization suspension and rollback, is separately pending approval.

The source-era child-list expectation and transient automatic-approval handling were corrected in the probes without replaying completed SQL. Both product task outcomes and Oracle effects are recorded separately from case acceptance.
