# Oracle database change platform research

## Đánh giá T00–T04, 04/10/2026

**Shortlist POC có điều kiện: ODC, CloudDM, AccessFlow và Archery cho SQL governance.**
Chưa ứng viên nào được chứng minh đạt toàn bộ yêu cầu migration Oracle và governance.

1. Đọc [kết luận T00–T04](evaluation/report.md) và [shortlist có lý do](evaluation/shortlist.md).
2. Kiểm [criteria](evaluation/criteria.csv), [register ứng viên](evaluation/candidates.csv) và [search log](evaluation/search-log.md).
3. Xem [feature evidence](evaluation/feature-matrix.csv), [source reports](evaluation/README.md) và [review](evaluation/reviews/coordinator-review.md).
4. Dùng [benchmark spec](evaluation/benchmark-spec.md), [config](evaluation/benchmark-config.json) và [SQL hashes](evaluation/workloads/manifest.json) cho lượt sau.

Ba worker làm song song; coordinator tổng hợp và review chéo nguồn.
Lượt này không deployment, test, service, SQL hoặc benchmark.
Bằng chứng Bytebase/ODC giữ nguyên. Oracle 19c/21c, image/dependency gates và runtime mới còn chưa kiểm.

## Nghiên cứu và POC trước T00–T04

**OceanBase ODC and AccessFlow remain in the existing open-source platform shortlist.**
ODC has Platform Fit HIGH and Migration Engine Fit LOW.
AccessFlow has Platform Fit MEDIUM and Migration Engine Fit LOW.
No complete replacement for all requested release and recovery capabilities was verified.

Research date: 2026-10-03.

1. Read [the revised research report](REPORT.md).
2. Compare [product categories and 18 capabilities](PRODUCT-MODEL.md).
3. Inspect [actual frontend pages and official screenshots](UI-EVIDENCE.md).
4. Review [Bytebase forks and historical licenses](FORK-SEARCH.md).
5. Review [supplemental source evidence](PRODUCT-EVIDENCE.md).
6. Review [original execution evidence](EVIDENCE.md).
7. Review [licenses](LICENSE-AUDIT.md), [maturity](MATURITY.md), and [Oracle coverage](ORACLE-COMPATIBILITY.md).
8. Use [the platform and Oracle verification plan](poc/ORACLE-POC.md) for a later evaluation.

The [product-model constraint](product-model-constraint.md) controls primary selection.
The original [brief](brief.md) still controls execution acceptance.
The [feature register](FEATURE-MATRIX.md) preserves the original twenty candidates and adds ODC.
The [additional candidate analysis](additional-candidates.md) remains a secondary reference.

## Kế hoạch đánh giá mở rộng

[Kế hoạch quản lý DB, migration và hiệu năng](poc/PLATFORM-EVALUATION-PLAN.md) chia tính năng F01–F12 và task T00–T12.
[Prompt handoff](poc/PLATFORM-EVALUATION-HANDOFF.md) quy định giao việc song song và cách kiểm bằng chứng.
[CloudDM và các ứng viên bổ sung](ADDITIONAL-PLATFORMS-20261004.md) là nguồn cho lượt shortlist tiếp theo.
Các tài liệu này chưa ghi nhận deployment mới hoặc kết quả benchmark.

## Phạm vi bằng chứng hiện có

Missing target migration state reduces execution readiness. It does not automatically remove a strong platform from the revised shortlist.
Archery and SQLE Community are SQL governance systems.
Flyway, Liquibase, Sqitch, and migration UIs remain secondary components.
Evaluate existing platform workflows before considering a composition.

The [search record](evidence/product-model/SEARCH.md) records requested phrases, topics, primary leads, and access limits.
The [review record](REVIEW-CHECKS.md) records verified items and remaining uncertainty.
ODC is deployed at [oceanbase.apps.drgdevlab.com](https://oceanbase.apps.drgdevlab.com).
Read [ODC architecture, Oracle integration, permissions, APIs, and licensing](ODC-EVALUATION.md).
Deployment and selected authenticated GET routes were inspected.
The 2026-10-04 connection POC executed one metadata SELECT through ODC and verified TCPS connection.
See [ODC connection setup](ODC-CONNECTION-POC.md). The 45 original criteria now have [API/UI results](ODC-ORACLE-POC-RESULTS.md).

Source snapshots retain commit identities in the original and supplemental manifests.
The product evidence, product comparison, and UI record have document generators in `tools/`.
These tools do not run candidate applications or database statements.
Antigravity's bounded fork research used pinned Gemini after Claude quota was exhausted.
Codex reviewed and extended the result.

The ODC source review used pinned Claude Opus 5.5 through Antigravity.
The [ODC review record](evidence/product-model/odc-integration-review.json) contains sanitized results and validation counts.

## ODC API/UI POC, 04/10/2026

See [results and limits](ODC-ORACLE-POC-RESULTS.md) and [preserved acceptance criteria](poc/ORACLE-POC.md).
Evidence JSON files: `evidence/oracle-poc-{api,governance,manual-approval,cases,review}.json`.
Results: 12 PASS, 20 PARTIAL, 5 FAIL, 8 NOT_RUN. Oracle 26ai ran on disposable schemas.
INVALID compilation, replay/checksum, request dedup, and requester execution separation failed their criteria.

## Bytebase API/UI POC, 04/10/2026

[Bytebase mới: 45 kết quả](BYTEBASE-ORACLE-POC-RESULTS.md) và [đối chiếu ODC](BYTEBASE-ODC-COMPARISON.md).
Kết quả: 17 PASS, 14 PARTIAL, 4 FAIL, 3 BLOCKED, 7 NOT_RUN. Runtime 3.22.1/FREE, Oracle 26ai.
Native version/replay và execution-role separation có bằng chứng tốt hơn ODC.
Procedure INVALID, SQL Review ERROR và early mockPROD vẫn là các lỗi cần xử lý.
Approval/audit bị giới hạn FREE; chưa đánh giá Enterprise hoặc controlled recovery.
Có 11 ảnh Selenium thật, API evidence và Oracle Thin hậu kiểm tại [portal](https://db-poc.apps.drgdevlab.com/).
Bằng chứng mới dùng `evidence/bytebase-poc-*.json`. Lịch sử P03/P04 vẫn FAIL, được giữ riêng.
