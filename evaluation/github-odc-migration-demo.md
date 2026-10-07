# Demo migration GitHub Actions → ODC → Oracle

Đây là implementation downstream của quyết định ODC practical pilot. Entry point là [demo/README.md](../demo/README.md); ba release `customer-profile` dùng bốn schema POC đã có trên cùng một Oracle service. Không thay đổi kết luận lịch sử, 33 upstream submodule, cluster hay production.

## Phạm vi và bằng chứng hiện tại

| Phần | Trạng thái | Bằng chứng |
| --- | --- | --- |
| Manifest, policy, package, ODC client, verifier, collector, reports | IMPLEMENTED | [Scripts](../scripts/db_demo/), [demo](../demo/) |
| Validation, ordering, hashes, envelope, report, redaction, integration boundaries | LOCAL TESTED | 33 unit tests và CLI validation cho cả ba release |
| GitHub PR / Actions | NOT_RUN | Sẽ ghi run thực sau khi push nhánh feature và mở PR |
| ODC authentication / target mapping | ODC RUNTIME TESTED, read-only | [Live readiness](../evidence/github-odc-demo-20261008/local-readiness.json) |
| New ODC ticket / batch | NOT_RUN | Chưa gửi SQL migration trong thời điểm lập bản ghi này |
| New migration / Oracle verification | NOT_RUN | Không suy diễn từ historical runtime hoặc fixture |
| Reports mẫu | LOCAL TESTED, FIXTURE | [Markdown](../demo/customer-profile/reports/sample-migration-report.md), [JSON](../demo/customer-profile/reports/sample-migration-report.json) |

## Quyền và điều kiện runtime

Các target allowlist: DEV 1000069, SIT 1000122, UAT 1000184, MOCKPROD 1000218; project 1. ODC client chỉ gửi batch MANUAL, ABORT, retry 0 và đọc evidence. Client không có thao tác approve, Execute hoặc promotion. OWNER/DBA review và operator continuation diễn ra trong ODC; `EXECUTION_SUCCEEDED` phải được bổ sung bằng `USER_OBJECTS`, `USER_ERRORS`, dữ liệu và kết quả function.

Repo ban đầu chưa có Actions authentication secrets hoặc self-hosted runner. Workflow live dùng labels `self-hosted`, `linux`, `odc-demo` và protected environment `odc-demo`; không triển khai runner. Probe trên runner GitHub-hosted chỉ đọc public-key API của endpoint đã tồn tại, không gửi authentication. Kết quả sẽ được giữ trong artifact Actions.

Deployment hiện được restore về baseline và chưa có hostname/advertised identity/persistent task-log mount đã chứng minh. [Permanent GitOps recommendation](../evidence/odc-retention-experiment-20261007/permanent-gitops-recommendation.yaml) là điều kiện trước pilot. Demo không tự áp dụng patch, restart pod hoặc thay đổi Argo.

## Mô hình minh chứng

Happy, failure và correction fixture được gắn `FIXTURE`, `SAMPLE / DEMO`, `runtime_proven=false`; chúng kiểm tra contract/report, không chứng minh SQL đã chạy. FAIL giữ DEV thành công, SIT lỗi ORA-20042, UAT/MOCKPROD chờ; FIX có hash mới và tham chiếu FAIL. Native MANUAL cho phép một quyết định explicit tiếp tục sau lỗi; demo yêu cầu operator dừng/cancel FAIL, không tuyên bố một policy promotion tuyệt đối.

Operational effort chưa được đo: `NOT_MEASURED`. Không có custom execution platform, JDBC executor, automatic promotion hay Flyway ledger. ODC có thể tập trung execution/inventory/approval/history của quy trình DBeaver; Git, DBA, backup, thiết kế schema và recovery vẫn có trách nhiệm riêng.

```text
DATABASE MIGRATION DEMO RESULT
==============================
REPOSITORY = devsecopslonghn/DB-Research
APPLICATION = customer-profile
HAPPY RELEASE = REL-2026.10-DEMO01
FAILURE RELEASE = REL-2026.10-DEMO02-FAIL
CORRECTION RELEASE = REL-2026.10-DEMO02-FIX
SOURCE FLOW = Git branch → PR → GitHub Actions
VALIDATION PIPELINE = PARTIAL (local PASS; GitHub not run yet)
RELEASE ARTIFACT = PARTIAL (implemented/local-tested)
ODC INTEGRATION = PARTIAL (authenticated mapping read-only)
REVIEW / APPROVAL = BLOCKED (independent human review not performed)
NATIVE MULTI-ENV ROLLOUT = BLOCKED (new batch not created/executed)
ORACLE VERIFICATION = BLOCKED (new migration not executed)
FAILURE FLOW = PARTIAL (fixture/local tested)
CORRECTION FLOW = PARTIAL (fixture/local tested)
REPORT GENERATION = PARTIAL (local fixture tested)
TRACEABILITY = Git commit → release → migration hashes → ODC ticket/batch → approval → target → execution → Oracle verification → report
CUSTOM EXECUTION PLATFORM = NO
MANUAL DBEAVER REPLACEMENT = PARTIAL
FLYWAY REPLACEMENT = PARTIAL
DEMO DECISION = CONDITIONAL GO
WHAT IS ACTUALLY RUNTIME-PROVEN = Local ODC login and four live target identities
WHAT REMAINS DEMO/IMPLEMENTATION ONLY = New ticket, rollout, Oracle checks and GitHub workflow runtime
NEXT STEP = Run GitHub validation and create one pending reviewed ODC batch; preserve manual approval boundary
```
