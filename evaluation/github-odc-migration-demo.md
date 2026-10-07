# Demo migration GitHub Actions → ODC → Oracle

**CONDITIONAL GO cho demo implementation có thể review.** Validation, immutable packages và report generation đã chạy thành công trên GitHub Actions. Local CLI đã tạo native ODC batch **2000015**, đang `APPROVING`; chưa có approval, migration execution hoặc post-migration Oracle verification. Đây chưa phải bằng chứng hoàn thành rollout bốn môi trường.

Entry point cho engineer mới là [demo/README.md](../demo/README.md). [PR #1](https://github.com/devsecopslonghn/DB-Research/pull/1) mở từ `feature/github-odc-migration-demo` vào `main`; chưa merge. Baseline `fd05666c44d0c4bf3cb94282b9163124db73ffa8` và 33 upstream submodule được giữ nguyên. Tất cả target là schema POC trên cùng một Oracle service; MOCKPROD không phải production. Thời điểm evidence là UTC ngày 7 October, tương ứng ngày 8 October 2026 ở Asia/Ho_Chi_Minh.

## Mức minh chứng

| Phần | Trạng thái | Bằng chứng và giới hạn |
| --- | --- | --- |
| Ba release, manifest/policy/allowlist, scripts, workflows, docs | IMPLEMENTED | [Customer-profile](../demo/customer-profile/), [scripts](../scripts/db_demo/), [workflows](../.github/workflows/) |
| Manifest, policy, ordering, hashes, envelope, redaction, report và API boundaries | LOCAL TESTED | 34 unit tests PASS; [initial checks](../evidence/github-odc-demo-20261008/local-checks.json) ghi 33 tests trước live observation, [final checks](../evidence/github-odc-demo-20261008/final-local-checks.json) thêm regression cho child chờ khi parent chưa approve |
| PR validation, packages cho cả ba release, fixture reports | GITHUB ACTIONS TESTED | Run 37668628709 SUCCESS trên implementation SHA `848e0923f3c8e2ef854298184232352ea68ed9ce`; gồm 33 tests tại SHA đó |
| Markdown/JSON fixture report workflow | GITHUB ACTIONS TESTED | Run 37668628840 SUCCESS; evidence source FIXTURE, runtime_proven false |
| Network từ GitHub-hosted runner | GITHUB ACTIONS TESTED | [Probe](../evidence/github-odc-demo-20261008/runner-connectivity.json): HTTP 200, REACHABLE_UNAUTHENTICATED, authentication NOT_ATTEMPTED |
| ODC login/inventory/create/lookup/task result/approval state | ODC RUNTIME TESTED | Local requester tạo batch 2000015 bằng CLI mới; [receipt](../evidence/github-odc-demo-20261008/odc-receipt.json) không có collection errors |
| Oracle owner và object namespace trước migration | ORACLE RUNTIME TESTED, read-only | [Preflight](../evidence/github-odc-demo-20261008/oracle-preflight.json): đúng owner, chưa có sáu object demo tại cả bốn target |
| OWNER + DBA approval và native rollout | BLOCKED | Batch APPROVING, hai approval nodes chưa COMPLETED; client không có approve/Execute |
| Object VALID, USER_ERRORS, data, function sau migration | BLOCKED | Chưa chạy migration; verifier LIVE bỏ qua target chưa EXECUTION_SUCCEEDED, [pending verification](../evidence/github-odc-demo-20261008/oracle-verification-pending.json) giữ NOT_AVAILABLE |
| Happy/failure/correction outcomes | GITHUB ACTIONS TESTED với FIXTURE; runtime BLOCKED | Happy/FIX fixture VERIFIED; FAIL fixture DEV success/SIT failure/UAT-MOCKPROD chờ; không phải product execution proof |
| Collector và LIVE pending report | LOCAL TESTED với ODC receipt thật | [Markdown](../evidence/github-odc-demo-20261008/live-migration-report.md), [JSON](../evidence/github-odc-demo-20261008/live-migration-report.json): WAITING_APPROVAL, runtime_proven false |

## GitHub PR, runs, jobs và artifacts

[Captured metadata](../evidence/github-odc-demo-20261008/github-actions-implementation.json) giữ PR number/URL/branch/head commit, run IDs/conclusions, jobs/steps và artifact IDs/digests/expiry. Hai run dưới đây kiểm tra implementation SHA `848e0923f3c8e2ef854298184232352ea68ed9ce`; các commit bổ sung evidence/report regression có checks riêng trên PR. Không gán run của SHA này cho SHA khác.

| Workflow | Run / conclusion | Job | Artifact |
| --- | --- | --- | --- |
| db-validate.yml | [37668628709](https://github.com/devsecopslonghn/DB-Research/actions/runs/37668628709), SUCCESS | [validate 112954292202](https://github.com/devsecopslonghn/DB-Research/actions/runs/37668628709/job/112954292202), SUCCESS | [db-demo-validation-37668628709 / 11502754605](https://github.com/devsecopslonghn/DB-Research/actions/runs/37668628709/artifacts/11502754605) |
| db-report.yml | [37668628840](https://github.com/devsecopslonghn/DB-Research/actions/runs/37668628840), SUCCESS | [fixture-report 112954292409](https://github.com/devsecopslonghn/DB-Research/actions/runs/37668628840/job/112954292409), SUCCESS; live-source-guard/live-report SKIPPED theo thiết kế PR | [db-demo-report-fixture-37668628840 / 11503429204](https://github.com/devsecopslonghn/DB-Research/actions/runs/37668628840/artifacts/11503429204) |

Artifacts giữ 30 ngày; metadata ghi expiry cụ thể. Outputs quan trọng đã tải xuống và giữ trong [evidence index](../evidence/github-odc-demo-20261008/README.md): validation, GitHub envelope, fixture Markdown/JSON và network probe. [Artifact verification](../evidence/github-odc-demo-20261008/artifact-verification.json) xác nhận downloaded bundles đúng hashes và committed source, ghi outcomes của cả ba fixture.

## Handoff ODC thực và provenance

Local build dùng cùng source commit với hai run Actions. [Payload comparison](../evidence/github-odc-demo-20261008/payload-comparison.json) xác nhận manifest hash, combined SQL hash, từng migration, policy và targets khớp CI. Combined SQL SHA-256 là `3ddce47b1a7675f1f02f349b21f0647437cd7693229fd560472df2a7c0338854`.

Batch 2000015 được tạo **từ local CLI**, không phải GitHub Actions. [Local envelope](../evidence/github-odc-demo-20261008/local-release-envelope.json) ghi github_actor LOCAL_OPERATOR, github_run_id NOT_AVAILABLE; [GitHub envelope](../evidence/github-odc-demo-20261008/github-release-envelope.json) giữ actor/run thực của CI. Receipt lookup kiểm tra exact SQL bytes, app/release/commit/run/hash markers và ordered target IDs trước khi thu evidence.

Native payload là MULTIPLE_ASYNC, executionStrategy MANUAL, singleton ordered groups DEV → SIT → UAT → MOCKPROD, ABORT, retry 0. Create identity được ghi ngay vào [odc-created.json](../evidence/github-odc-demo-20261008/odc-created.json), không retry POST mù. Collector đọc ticket, task results, approval nodes và personal audit API; collection_errors rỗng. Audit chỉ giữ event có explicit taskId khớp, hiện chưa có event tương quan như vậy. Reference URL không phải bằng chứng đã tải result/log/ZIP hoặc verify retention.

| Stage | ODC database | Native environment | Owner schema | Native result | Oracle acceptance |
| --- | --- | --- | --- | --- | --- |
| DEV | 1000069 | 1 / dev | ODC_POC_20261004_DEV | WAIT_FOR_EXECUTION | NOT_AVAILABLE |
| SIT | 1000122 | 2 / sit | ODC_POC_20261004_SIT | WAIT_FOR_EXECUTION | NOT_AVAILABLE |
| UAT | 1000184 | 1000021 / POCUAT | ODC_POC_20261004_UAT | WAIT_FOR_EXECUTION | NOT_AVAILABLE |
| MOCKPROD | 1000218 | 1000022 / POCPROD | ODC_POC_20261004_MOCKPROD | WAIT_FOR_EXECUTION | NOT_AVAILABLE |

Approval node operator hiện hiển thị requester trong node chưa hoàn tất; đó không phải completed approver hoặc execution actor. Report yêu cầu hai actor OWNER/DBA khác nhau, khác requester, có approval COMPLETED. Child WAIT_FOR_EXECUTION không được nâng thành demo APPROVED khi parent còn APPROVING. Native flow createTime được lưu riêng, không coi là execution start. Không có Oracle migration DDL/DML được thực thi trong nhiệm vụ này.

## Điều kiện còn thiếu và bước vận hành

**ODC LIVE INTEGRATION FROM GITHUB ACTIONS = BLOCKED**, dù local API integration đã chạy và hosted probe reachable. [Read-only prerequisites](../evidence/github-odc-demo-20261008/github-runtime-prerequisites.json) ghi không có repository secrets, self-hosted runner hoặc environment cấu hình tại thời điểm capture. Workflow live cần ODC_BASE_URL, ODC_USERNAME, ODC_PASSWORD, labels self-hosted/linux/odc-demo, protected environment odc-demo và workflow trên main. Chưa merge nên chưa dispatch workflow mới theo đường live đã thiết kế. Không triển khai runner, tạo public endpoint, chuyển credentials local vào GitHub hoặc sửa cluster.

Để hoàn tất runtime: OWNER và DBA review batch 2000015/SQL/hash, approve độc lập trong ODC UI; authorized operator thực thi DEV, collect và verify qua SELECT-only ODC path, rồi tiếp tục SIT/UAT/MOCKPROD khi stage trước VERIFIED. Không dispatch create mới cho happy release khi ticket 2000015 đã tồn tại. Local collect dùng receipt này; sau khi được phép merge/configure GitHub, cần handoff artifact đúng provenance để workflow theo dõi ticket, không tạo lại để khắc phục thiếu artifact.

Sau happy runtime mới chạy FAIL, giữ DEV đã thực thi và SIT failure cùng UAT/MOCKPROD chờ, cancel phần chưa chạy, rồi tạo FIX với hash mới và approval mới. Native MANUAL vẫn cho phép quyết định explicit tiếp tục sau lỗi; demo không tuyên bố ABORT là policy promotion tuyệt đối. Không sửa release FAIL để che thất bại, không yêu cầu rollback Oracle DDL đã commit.

Deployment ODC đã restore baseline; hostname/advertised identity/persistent task-log settings của retention experiment chưa áp dụng lâu dài. [Permanent GitOps recommendation](../evidence/odc-retention-experiment-20261007/permanent-gitops-recommendation.yaml) vẫn là điều kiện trước pilot. Demo không tự patch/restart/Argo change; không đổi historical practical pilot GO hoặc retention baseline FAIL.

## Completion audit và giới hạn

| DoD | Kết quả |
| --- | --- |
| 1–2: structure và ba release | PASS, đúng tên/manifest/SQL, FIX tham chiếu FAIL |
| 3–4: validation và local tests | PASS, 34 tests; hashes, policy, Oracle acceptance và approval boundaries được kiểm tra |
| 5–9: workflows, push, PR, validation run và capture | PASS, Actions thực SUCCESS, jobs/artifacts được lưu |
| 10: release envelope | PASS, CI/local immutable packages; downloaded hashes/source đã kiểm tra |
| 11–12: ODC client và live integration hoặc explicit blocker | PASS cho local create/collect thật; authenticated GitHub live workflow BLOCKED với dependencies cụ thể |
| 13–14: report generator và Markdown/JSON samples | PASS, checked-in SAMPLE/DEMO, CI fixture và local LIVE pending reports |
| 15–16: architecture/operator docs và evaluation phân tầng | PASS, Mermaid flow/sequence, local/GitHub commands, runner/secrets, failure/correction và provenance |
| 17: historical preservation | PASS, old evidence/conclusions giữ nguyên, 15 preserved hashes khớp, 33 gitlinks không đổi; root/index chỉ thêm demo link |

DoD đóng implementation reviewable và integration readiness; không biến blocked rollout thành runtime acceptance. Lexical scan không phải Oracle parser. Operational effort NOT_MEASURED; retention NOT_CHECKED trong report mới. Không có custom execution platform, JDBC migration executor, auto approval/Execute/promotion hoặc Flyway ledger. ODC có thể gom DBeaver execution/inventory/approval/logs; Git, DBA, backup, schema design và recovery vẫn có trách nhiệm riêng.

```text
DATABASE MIGRATION DEMO RESULT
==============================
REPOSITORY = devsecopslonghn/DB-Research
APPLICATION = customer-profile
HAPPY RELEASE = REL-2026.10-DEMO01
FAILURE RELEASE = REL-2026.10-DEMO02-FAIL
CORRECTION RELEASE = REL-2026.10-DEMO02-FIX
SOURCE FLOW = Git branch → PR → GitHub Actions
VALIDATION PIPELINE = PASS (local + actual PR workflow)
RELEASE ARTIFACT = PASS (CI/local committed payload, hashes verified)
ODC INTEGRATION = PARTIAL (local native create/collect PASS; authenticated GitHub workflow BLOCKED)
REVIEW / APPROVAL = BLOCKED (independent human approval pending)
NATIVE MULTI-ENV ROLLOUT = BLOCKED (batch 2000015 APPROVING; no migration execution)
ORACLE VERIFICATION = BLOCKED (post-migration checks unavailable; read-only preflight PASS)
FAILURE FLOW = PARTIAL (source/static/fixture tested in Actions; no live FAIL execution)
CORRECTION FLOW = PARTIAL (new immutable release/fixture tested in Actions; no live FIX execution)
REPORT GENERATION = PASS (CI FIXTURE and local LIVE pending Markdown/JSON)
TRACEABILITY = Git commit → release → migration hashes → ODC ticket/batch → approval → target → execution → Oracle verification → report; chain currently reaches pending approval, later links NOT_AVAILABLE
CUSTOM EXECUTION PLATFORM = NO
MANUAL DBEAVER REPLACEMENT = PARTIAL
FLYWAY REPLACEMENT = NO (Git version discipline exists; automatic version ledger/replay is absent)
DEMO DECISION = CONDITIONAL GO
WHAT IS ACTUALLY RUNTIME-PROVEN = GitHub validation/package/fixture reporting; hosted unauthenticated connectivity; local ODC login/inventory/native batch create/status/audit lookup; four Oracle owner/namespace SELECT preflights
WHAT REMAINS DEMO/IMPLEMENTATION ONLY = Independent completed approval, actual migration rollout, post-migration objects/errors/data/function acceptance, live FAIL/FIX, authenticated GitHub live dispatch and new-release retention
NEXT STEP = Review PR and batch 2000015; independent OWNER/DBA approval and manual stage execution/verification; configure runner/secrets/protected environment and demonstrated retention settings under separate authorization, without recreating the pending batch
```
