# Evidence của demo GitHub/ODC — 8 October 2026

Giữ riêng bằng chứng mới khỏi historical POC và retention evidence. [Evaluation](../../evaluation/github-odc-migration-demo.md) ghi các mức IMPLEMENTED, LOCAL TESTED, GITHUB ACTIONS TESTED, ODC/ORACLE RUNTIME TESTED và BLOCKED.

- [local-readiness.json](local-readiness.json): requester authentication, bốn target live và retention baseline; không cluster mutation.
- [local-checks.json](local-checks.json): initial 33 tests và checks; [final-local-checks.json](final-local-checks.json): checks sau report regression, 34 tests.
- [github-actions-implementation.json](github-actions-implementation.json): PR #1, implementation SHA, hai SUCCESS runs, jobs/steps, artifact IDs/digests/expiry.
- [github-validation-report.md](github-validation-report.md), [JSON](github-validation-report.json): validation output tải từ Actions artifact.
- [github-release-envelope.json](github-release-envelope.json), [fixture report Markdown](github-fixture-migration-report.md), [JSON](github-fixture-migration-report.json): output thực của GitHub run; report vẫn FIXTURE, không phải ODC execution proof.
- [artifact-verification.json](artifact-verification.json): downloaded bundles khớp committed hashes, outcomes của ba fixture; [payload-comparison.json](payload-comparison.json): local handoff và CI cùng payload, khác actor/run provenance.
- [runner-connectivity.json](runner-connectivity.json): hosted HTTP 200/public-key probe, authentication NOT_ATTEMPTED; [github-runtime-prerequisites.json](github-runtime-prerequisites.json): runner/secret/environment inventory không có secret values.
- [oracle-preflight.json](oracle-preflight.json): SELECT-only owner/namespace trước migration, bốn schema đúng và chưa có demo objects.
- [local-release-envelope.json](local-release-envelope.json), [odc-created.json](odc-created.json), [odc-receipt.json](odc-receipt.json): local batch 2000015 MANUAL, APPROVING; github_run_id NOT_AVAILABLE.
- [oracle-verification-pending.json](oracle-verification-pending.json), [live-evidence.json](live-evidence.json), [LIVE pending Markdown](live-migration-report.md), [JSON](live-migration-report.json): Oracle acceptance NOT_AVAILABLE, WAITING_APPROVAL, runtime_proven false.

Artifacts GitHub hết hạn sau 30 ngày; outputs chọn lọc giữ tại đây. Batch chưa approve/execute, không có Oracle migration DDL/DML. Không lưu credentials, cookies, authorization headers, kubeconfig hoặc raw environment dumps. Source đã commit giữ SQL/config; evidence giữ projections/reports được sanitize, không giữ raw sessions hay temporary runtime files.
