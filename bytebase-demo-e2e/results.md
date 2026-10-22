# Kết quả thực nghiệm và giới hạn

**Hoàn thành chuỗi mới Git → Jenkins → Bytebase → Oracle → tra cứu.** PR #9 đã merge sau CI thành công, master #12 tự triển khai V1.0.0.10, và query đọc mới trên đúng bảng POC trả count 0. Bộ ảnh gồm 42 PNG thật; không dùng Plan/task cũ thay kết quả này.

| Mắt xích | ID / kết quả thực tế |
| --- | --- |
| PR chính | [#9](https://github.com/devsecopslonghn/cr7allgoals-db/pull/9), đã merge 2026-10-22T07:25:39Z |
| Source SHA đã review | `ecfb13fb31a23036d7a8ee2ad9cc0c5c37039661` |
| Merge SHA | `a8267df4c8b097b67fa4b6e88da8bf82e8146d0c` |
| PR SQL Review | [PR-9 #2](https://jenkins.apps.drgdevlab.com/job/devsecopslonghn/job/cr7allgoals-db/job/PR-9/2/), SUCCESS, 0 ERROR / 3 WARNING |
| Build triển khai | [master #12](https://jenkins.apps.drgdevlab.com/job/devsecopslonghn/job/cr7allgoals-db/job/master/12/), SUCCESS, checkout merge SHA trên |
| Release | [release_20261022-RC00](https://bytebase.apps.drgdevlab.com/projects/cr7-allgoal-kvi1/releases/release_20261022-RC00) |
| Plan | [114](https://bytebase.apps.drgdevlab.com/projects/cr7-allgoal-kvi1/plans/114) |
| Task / task run | `114` / `113`, stage `develop`, Done |
| Target | `instances/oracle-cloud-free-sge0/databases/CR7ALLGOALS_APP` |
| Project / stage | `projects/cr7-allgoal-kvi1` / `environments/develop` |
| Identity thực thi | `jenkins@service.bytebase.com` |
| Migration / object | `V1.0.0.10` / `BB_POC_E2E_20261022_A` |
| Oracle đối soát | Query mới lúc 14:28:19 GMT+7, count = 0, 243 ms |
| Ca âm | [PR #10](https://github.com/devsecopslonghn/cr7allgoals-db/pull/10), SHA `743302007818e0410d3f353c326e87960115441b`, PR-10 #2 FAILURE, chưa merge/deploy |


## Chuỗi bằng chứng và kiểm tra tính liên tục

| Liên kết | Bằng chứng |
| --- | --- |
| SQL → PR/source SHA | [09b](screenshots/09b-github-reviewed-source.png), [11 diff trước merge](screenshots/11-pr9-reviewed-sql-diff.png) |
| Source SHA → PR build → review | [13b checkout](screenshots/13b-ci-pr9-reviewed-build.png), [13c runtime](screenshots/13c-ci-pr9-runtime-review-stage.png), [14b artifact](screenshots/14b-pr9-reviewed-findings.png) |
| Review → comment/check → merge | [15b native](screenshots/15b-pr9-bytebase-native-summary.png), [15c Jenkins](screenshots/15c-pr9-jenkins-advice-comment.png), [16b check xanh](screenshots/16b-git-reviewed-head-success.png), [17 merged](screenshots/17-pr9-merged.png) |
| Merge SHA → master build → Release/Plan | [18 checkout master #12](screenshots/18-master12-merge-checkout.png), [19 console chứa link thật](screenshots/19-master12-release-plan-links.png) |
| Release SQL → task result | [21 SQL/hash](screenshots/21-bytebase-release-reviewed-sql.png), [22 rollout](screenshots/22-bytebase-new-rollout-done.png), [23 trace](screenshots/23-bytebase-task-execution-trace.png) |
| Task → trạng thái DB | [25 query mới](screenshots/25-oracle-new-object-live-query.png), [26 catalog](screenshots/26-oracle-new-table-catalog.png), [27 columns/index](screenshots/27-new-table-columns-and-key.png) |
| Tra cứu sau execution | [28 danh sách Plans](screenshots/28-find-new-plan-in-project-history.png), [29 mở lại Plan 114](screenshots/29-reopened-new-plan-history.png), [30 revision mới](screenshots/30-new-migration-revision-history.png) |

File SQL V10 ở source SHA và merge SHA cùng Git blob `7f58bbea7aff9f093f07b7526c14a099ef6bcf05`. SQL lấy từ GetSheet thật trong browser cũng trùng local từng byte: 932 bytes, SHA-256 `706ea32221e2d738a88bcb6a76db2f20c0e6e53e0a3db4295f2e4ad695446dcd`. Bản đó nằm tại [artifacts/bytebase-release-v1.0.0.10.sql](artifacts/bytebase-release-v1.0.0.10.sql). Resource Sheet dùng chính SHA-256 này làm ID.

Task đầy đủ: `projects/cr7-allgoal-kvi1/plans/114/rollout/stages/develop/tasks/114`; task run: `projects/cr7-allgoal-kvi1/plans/114/rollout/stages/develop/tasks/114/taskRuns/113`. ID lấy từ response GetRollout/ListTaskRuns thật trong browser, lưu metadata chọn lọc tại [bytebase-runtime-identifiers.json](artifacts/bytebase-runtime-identifiers.json); không xuất header auth/session.

Build master bắt đầu 07:25:57.488Z, duration 32.707 giây. Console ghi tạo Release lúc 07:26:05.107Z, Plan lúc 07:26:05.172Z, bắt đầu task stage 07:26:06.261Z và stage completed 07:26:26.553Z. Task trace chỉ ghi V1.0.0.10 với CREATE TABLE và 4 COMMENT; các file V0–5 có trong Release không đồng nghĩa đã bị thực thi lại. UI task Done khoảng 15.3 giây gồm schema sync.

## Review, cảnh báo và quyết định merge

| Vòng CI mới | SHA | Kết quả thực tế |
| --- | --- | --- |
| PR-9 #1 | `0d3ff30` | FAILURE; 1 ERROR comment cột dài >64 ký tự; 4 WARNING; comment GitHub còn lỗi 401 |
| PR-9 #2 | `ecfb13f` | SUCCESS; 0 ERROR, 3 WARNING; cả native và custom comment lên PR thành công |
| PR-10 #1 | `fe07244` | FAILURE; 2 ERROR (PK và comment dài), 3 WARNING |
| PR-10 #2 | `7433020` | FAILURE; 1 ERROR TABLE_REQUIRE_PK 601, 2 WARNING; giữ Open, không merge/deploy |

Sửa riêng SQL mới chưa áp dụng: rút ngắn comment, dùng cột ID; giữ primary key ở PR chính và cố ý không có primary key trong PR âm. Không thay rule, severity hoặc `FAIL_ON_ERROR`. Không trigger liên tục để chờ ảnh: mỗi vòng #2 đi cùng commit sửa SQL có ý nghĩa.

Ba cảnh báo còn ở PR-9 #2: (1) V0 trên master đã khác bản áp dụng từ trước, code 1; (2) naming rule muốn lowercase, code 301, còn yêu cầu POC của nhiệm vụ dùng prefix BB_POC_; (3) code 420 cho ID identity không được rule coi là default. Check hiện tại chỉ fail khi có ERROR nên warnings không chặn. Không sửa V0, checksum, lịch sử hoặc policy để làm sạch ảnh.

V0 applied SHA-256 `22eb453f50b9cb04b4a0b546791483ddadb98137d5f159bceaf3d20c985a15de`, release SHA-256 `23a609fa5b0d0d1f9a82335142da5f2df2f06d5bfc6fd07e77770123c49040ea`. Đây là lệch nguồn có sẵn cần xử lý riêng theo quy trình của chủ hệ thống; phiên demo giữ nguyên. Applied SQL đã đối chiếu với source cũ được cấp, không import/repair hay sửa migration đã áp dụng.

Ngay trước merge: head đúng SHA cuối, combined status success, mergeable true/clean, draft false, chỉ hai file mới. API xác nhận `master protected:false`, active branch rules `[]`, reviews `[]`. Đã normal merge với điều kiện exact head SHA, không bypass flag, không giả approval độc lập. Snapshot chọn lọc: [premerge-readiness.json](artifacts/premerge-readiness.json).

**CI failure, Git cưỡng chế chặn merge và người quyết định không merge là ba việc khác nhau.** Ca âm chứng minh findings, lệnh check lỗi, CI FAILURE và Git status lỗi; không chứng minh Git bắt buộc cấm merge. Không thử merge PR lỗi. [80 SQL](screenshots/80-pr10-review-only-source.png), [81 build](screenshots/81-pr10-build2-failure.png), [82b finding](screenshots/82b-pr10-missing-pk-final-finding.png), [83 comment](screenshots/83-pr10-native-review-comment.png), [84 Git status](screenshots/84-pr10-git-status-failure.png), [85 command error](screenshots/85-pr10-review-command-error.png).

## Bytebase cung cấp gì; Git/Jenkins cung cấp gì

| Thành phần | Quan sát được trong lần chạy này | Giới hạn |
| --- | --- | --- |
| GitHub | Source/diff/PR, SHA, merge commit và commit status | Không có independent review hoặc required-merge rule được chứng minh |
| Jenkins | Nhận webhook, checkout SHA, action runtime 3.22.1, điều kiện PR/master, archive review JSON, tự rollout develop, build status và link Release/Plan | PR branch build xanh riêng không thay cho PR SQL Review; console đầy đủ thuộc Jenkins |
| Bytebase SQL Review/action | Findings code/severity/file/line/target; check release trả warning/error; native PR summary được action ghi nhờ cấu hình CI | Đây là check CI, không phải approval UI hoặc rule Git bắt buộc merge |
| Jenkinsfile tích hợp comment | Bảng advice riêng có marker BYTEBASE-JENKINS-DETAILS và build URL, lấy từ review JSON rồi upsert qua GitHub API | Native comment thực tế cũng có Detailed Results; nhận xét cũ trong Jenkinsfile rằng native chỉ có counts không phản ánh đầy đủ ảnh runtime |
| Bytebase Release/Plan/Rollout | SQL/hash, target, creator CI, task result/trace/timestamp, schema sync, revision và khả năng tìm lại | Plan 114 là Release-created Plan; không trộn với approval của UI-created Plan |
| Oracle qua SQL Editor | Query đọc mới trên bảng mới count 0; metadata ba cột, default/comment và index đúng tên | Không dùng client Oracle độc lập; không thử DML/constraint hoặc tài khoản ít quyền |

Jenkinsfile hiện tại dùng credential references `bytebase-cr7-service-account` và `github-token`; các stage gọi Bytebase bằng service account, không nhận trực tiếp DB password trong đoạn pipeline đã đọc. Execution mới hiển thị `jenkins@service.bytebase.com`. Điều này chứng minh luồng CI đang gọi nền tảng bằng danh tính API; không chứng minh mọi job/agent khác không thể tiếp cận DB credential. Bytebase runtime vẫn cần DB credential khi dùng password authentication. Không mở hoặc chụp giá trị DB credential, API key hay token.

## Cấu hình hiện có và phần đã sửa tối thiểu

- Đã đọc hướng dẫn workspace/global, README, Jenkinsfile, `.bytebase/`, migration và recovery. Không tìm thấy AGENTS.md riêng trong repo lúc khảo sát.
- Jenkins job hiện có là `devsecopslonghn/cr7allgoals-db`, script path Jenkinsfile; dùng project/target/pattern đúng như bảng ID và `migrations/V*.sql`. PR chạy check với FAIL_ON_ERROR; master tạo Plan và rollout `environments/develop`. Đã đối chiếu runtime các build mới thay vì chỉ đọc source.
- Webhook hiện có ID `680094522`, active, endpoint `https://jenkins.apps.drgdevlab.com/github-webhook/`; sự kiện push/pull_request mới được nhận HTTP 200, build #12 ghi cause push master. Không tạo webhook hoặc pipeline mới.
- Blocker thật ở vòng đầu là Global Secret text `github-token` trả HTTP 401 khi ghi/đọc comment. Sau xác nhận cụ thể “Cho phép cập nhật github-token từ file đã cấp”, đã cập nhật duy nhất giá trị credential đó từ file Git local. Giữ ID/scope/description; không sửa credential Bytebase. Vòng #2 ghi được cả hai comment; lỗi 401 đã được giải quyết, không còn là blocker.
- Chỉ thêm migration/recovery mới trên hai branch và sửa chính các file chưa áp dụng đó. `source-change.patch` và `review-only-change.patch` chứa diff cuối so với base `eebabe0`, không chỉ commit đầu.
- Dựa vào target đã có V0–9 để chọn V10; PR #8 có sẵn được giữ nguyên. Không merge/sửa PR #8, sửa bảng ứng dụng, thay migration đã áp dụng, dựng hạ tầng, thêm key/user/service account, tăng quyền, bật trial, nâng cấp hệ thống hoặc triển khai Flyway.
- Không chạy DROP/TRUNCATE, repair, retry hoặc bypass gate. Không tự deploy PR #10. Oracle có sequence hệ thống phát sinh từ identity; SQL tường minh chỉ thêm bảng/constraint BB_POC_ và comments.

## Phần chưa chứng minh và giới hạn còn lại

| Mục | Trạng thái / cách trình bày đúng |
| --- | --- |
| Execution mới và đối soát | Đã chứng minh cho V10 đúng target; không còn blocker cho luồng chính |
| Trạng thái Plan trước chạy | Không chụp được vì pipeline tự rollout quá nhanh; không dựng màn hình pending hoặc thêm gate |
| Human approval Bytebase | Không có bằng chứng cho luồng Release này; Plan list Review “-”, GetPlanCheckRun của Plan 114 trả not_found. PR SQL Review vẫn có thật ở CI; không gọi đây là tính năng sản phẩm không hỗ trợ |
| Enforcement ít quyền / separation of duties | Thao tác browser Bytebase bằng tài khoản admin được cấp; deploy bằng Jenkins service account. Không thử observer hoặc reviewer độc lập, không kết luận đã chứng minh separation of duties |
| Git chặn merge | master không protected và active rules trống khi kiểm tra. Chưa có bằng chứng required check cấm merge; ca âm được chủ động giữ unmerged |
| Source link native trong Bytebase | Không thấy link Git/commit trong Release/Plan đã mở; nối qua Jenkins console và SQL hash thật, không giả native integration |
| Oracle dictionary | ALL_OBJECTS qua SQL Editor bị lỗi lớp metadata/masking “resource not found”; đã giữ ảnh lỗi 03a. Không thay masking/grants; query trực tiếp bảng POC mới vẫn thành công |
| Recovery / failure runtime | Có recovery notes, chưa thử recovery/rollback hay gây runtime failure. Transaction labels không chứng minh Oracle DDL rollback nguyên khối |
| Audit/security | Task trace/history khác Audit Log đầy đủ. Không kiểm thử việc lấy lại secret; trường mask không chứng minh không ai truy xuất được |
| Edition / quota | Current plan Community, instance usage/limit 8/10 trên UI tại lúc chụp; không bật trial. Không suy quota phổ quát hoặc đếm schema/project thành instance |
| Flyway | Chưa triển khai hoặc thực nghiệm; không có kết luận so sánh năng lực từ bộ ảnh này ngoài phần Bytebase/Git/Jenkins đã quan sát |

Bộ cũ chỉ là tư liệu riêng, không được ghép thành execution mới. Baseline master #11 / Plan 113 / release_20261007-RC00 khác hoàn toàn master #12 / Plan 114 / release_20261022-RC00 của bộ này. Ảnh phụ lục của vòng đầu vẫn là những build mới trong cùng nhiệm vụ, gắn SHA/build riêng.

## Artifacts và bảo toàn dữ liệu

- [evidence-index.csv](evidence-index.csv): từng ảnh có URL nguồn không token, timestamp UTC, kích thước, SHA-256, ID và giới hạn.
- [runtime-chain-metadata.json](artifacts/runtime-chain-metadata.json): PR/merge/build metadata chọn lọc, không có credential.
- [master12-selected-console.txt](artifacts/master12-selected-console.txt): các dòng console nguyên văn được chọn theo checkout/version/Release/Plan/rollout/result; không phải toàn bộ console.
- `artifacts/pr9-build1-sql-review.json`, `pr9-build2-sql-review.json`, `pr10-build1-sql-review.json`, `pr10-build2-sql-review.json`: JSON review gốc, không dựng lại findings.
- PNG giữ nguyên ảnh browser; không có video/TTS/subtitle, ảnh AI hoặc browser auth state trong bộ bàn giao.
