# POC tiếp theo: từ workflow demo tới lab Oracle có kiểm soát

Ngày: **07/10/2026**. Tài liệu thiết kế/handoff, **chưa dựng lab, chưa chạy app/pipeline/SQL và không có runtime mới**. Đọc [solution shortlist](solution-shortlist.md) để hiểu lựa chọn và [reference architecture](reference-architecture.md) để dùng chung contracts. Không thay [45 acceptance/expected gốc](../poc/ORACLE-POC.md), [criteria.csv](criteria.csv), [14 workload hashes](workloads/manifest.json) hoặc evidence lịch sử.

**Chọn hai POC chính:** #1 **ODC workflow + sole Flyway executor** (S2), #2 **Git/Jenkins + Flyway composition** (S6). **Optional #3:** CloudDM workflow + Flyway (S3). Bytebase Enterprise là benchmark từ docs/source và FREE runtime cũ; không tự đăng ký trial/mua license. S2/S3 native executor failures vẫn giữ; POC adapter không làm native FAIL thành PASS.

Đầu ra cần cho người quyết định: screen walkthrough có evidence labels; external executor contract go/no-go; same approved SQL/targets/actors trace được; per-target result/history và failure HOLD không replay; license/dependencies và owner burden rõ. POC không được kết thúc chỉ vì một ALTER TABLE thành công.

## 1. Phạm vi và hai tầng demo

| Tầng | Dùng gì | Chứng minh được | Chưa chứng minh |
| --- | --- | --- | --- |
| D — no-DB workflow demo | Fake inventory, SQL file/commit, approval events, dry runner và simulated result; platform UI chỉ khi lab được phép dựng | Shape of workflow, target/actor/hash policy, usability, integration contract có thể kiểm khi services thực đã dựng | Oracle execution/version/auth/locks/recovery; screenshots thiết kế không RUNTIME |
| O — isolated Oracle lab, lượt sau có quyền riêng | Actual lab Oracle/version, disposable targets/schema, engine/platform exact build và CI job | SQL/history/object state, actor denial, partial failure/uncertain reconciliation đúng cases | Production certification, 50 live instance capacity hoặc HA nếu chưa chạy riêng |

**Lượt nghiên cứu hiện tại dừng ở tài liệu.** Tầng D vẫn cần request riêng nếu phải deploy local/infrastructure services; tầng O cần explicit isolated-target/SQL/fault-injection authorization ở lượt lab. Không dùng authorization SQL ngày 04/10 làm quyền chạy lần này. Không truy cập deployments hiện hữu hoặc kết nối DB thật từ file này. Không có câu hỏi permission cần trả lời để hoàn thành research.

D demo không mở Oracle connection: runner `mode=dry-run` phải thiếu deploy credential và DB network route, output có `SIMULATED_SUCCESS/FAILURE/UNKNOWN`. Native login/approval chạy trên application lab sau này là RUNTIME của application workflow riêng, không Oracle runtime. Không mock native permission/approval API rồi ghi product capability PASS.

## 2. Inputs cần nhận và giả định có thể đảo ngược

| Input | Proposed owner | Dùng ở đâu / nếu chưa có |
| --- | --- | --- |
| Oracle major/RU/edition, charset, auth/TCPS, SID/service/PDB/schema topology | DBA | Bắt buộc tầng O; tầng D dùng logical placeholders, không chọn 19c/26ai thay user |
| Git provider/version, CI có sẵn, SSO/identity groups | DevOps/identity owner | #2 reference Jenkins; đổi GitLab Premium nếu đã có. GitLab Free approvals không mặc định enforce |
| Existing secret manager/storage hoặc lab-only replacements | DevOps | Reference OpenBao KV; nếu dùng Jenkins credential store cho lab thì ghi integration chưa tested. Không Oracle dynamic plugin mặc định |
| Managed applications/streams và 4 representative target mappings | DBA + application owner | Freeze target snapshot; synthetic estate inventory không cần real network metadata |
| Review/approval policy, privileged exception, maintenance window | DBA/owner | Baseline DEV requester trigger; SIT/UAT reviewer; PROD reviewer + DBA distinct requester. Policy được chốt trước runtime |
| Backup/recovery baseline và session/lock observer permissions | DBA | Chỉ fault/recovery stage; nếu thiếu, cases giữ NOT_RUN, không chạy fault trên ordinary target |
| Lab authorization/resource boundaries | Lab owner | Chỉ ephemeral isolated scope đã duyệt; không production/service accounts thực ngoài scope |
| Capacity/maintenance owner và budget | Team owner | Adoption decision; không ngăn contract/no-DB preparation spec |

Giả định thiết kế: một application `core-customer`, một version stream, 4 environment tiers, serial concurrency=1, 20 role identities và 50 synthetic inventory records. Không khẳng định nội bộ đã có bất kỳ thành phần nào. 50 records chỉ kiểm import/selection/pagination; 20 lab identities chỉ role/UI smoke, không capacity throughput benchmark.

## 3. Topology, artifacts và pinning trước dựng

| POC | Thành phần cần cho demo/lab | Pin/source/evidence input | Điều không được suy |
| --- | --- | --- | --- |
| #1 ODC+FW | ODC + compatible MetaDB, Git, CI/adapter, restricted Flyway runner, secret service, result/evidence store | Historical runtime `4.4.1-20260116`; reviewed source `d517c0f27971642fb0cd7565fd61ab2309875ec3`, frontend `273fa3c4cc7d87f942ade231ce9220b98fa595e2`; [registry pins](research-round-2/licensing/registry-pins.csv), [ODC setup](../ODC-EVALUATION.md) | Source không map image 4.4.1; không có chứng cứ public tag v4.4.1/v4.5.0. Chọn actual image digest, MetaDB compatible docs, wrapper provenance trước dựng |
| #2 Jenkins+FW | Git host + Jenkins controller + restricted agent, approval/lock/auth plugins, runner/result publisher, secret/evidence storage | Reference Jenkins LTS **2.580.1**, Flyway OSS **13.9.0** theo [catalog](tool-feature-catalog.md); driver/module exact versions chọn và record khi lab dựng | Reference version không là installed artifact/digest; core MIT không license mọi plugin/module/driver |
| #3 CloudDM+FW | CloudDM standalone hoặc Console/Sidecar theo supported docs, metadata storage, CI/adapter/runner và common secret/evidence | v4.3.0 commit `3aa1238a471afca2579e76e6fbf0a922d9be5579`; [exact-artifact hashes](research-round-2/coordinator/clouddm-v430-artifact-review-20261007-hashes.json), [deploy guide](https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/docs/guides/deployment.en.md) | Native Oracle compile default off, target ledger/recovery absent from reviewed paths; adapter chưa có |
| Common secret layer | Existing manager hoặc OpenBao KV/auth reference | [OpenBao MPL license](https://github.com/openbao/openbao/blob/main/LICENSE), [JWT auth](https://openbao.org/docs/auth/jwt/) | Không claim Vault current releases OSS; không assume OpenBao Oracle rotation plugin/native Jenkins integration |
| Oracle lab | 4 isolated targets nếu có; hoặc 4 disposable schemas trên một service được label đúng | DBA cung cấp exact major/RU; observer/read-only/deployer roles riêng; no ANY/SYSDBA default | One-service/four-schema model không chứng minh four-instance isolation hay scale50 |

Versions ở bảng là nghiên cứu pin, **không auto-download/run commands**. Lab engineer kiểm actual binary/container hash, SBOM/notices và dependency/Oracle client terms, điền `versions.lock.json`; không dùng `latest`. Nếu image phải dựa trên wrapper local, ghi source commit/diff/build digest và delta, không gọi đó là upstream native TCPS.

ODC historical MetaDB OceanBase CE 4.3.5 và TCPS wrapper là topology đã quan sát, không mặc định deploy nguyên trạng; [connection POC](../ODC-CONNECTION-POC.md) ghi vận hành. #1 contract gate có thể STOP trước cần cấp writable Oracle.

## 4. Lab repository skeleton cần tạo ở lượt thực hiện

Tạo workspace **mới** cho demo, chẳng hạn `db-change-lab/`, ngoài directories evidence/source/workloads đã đóng băng của DB-Research. Các paths sau là **file cần tạo**, chưa tồn tại/implemented trong repo nghiên cứu:

```text
db-change-lab/
  README.md                          # cách dựng/dừng lab + boundaries
  versions.lock.json                 # commit/image/plugin/driver pins + notices
  inventory/targets.yaml             # non-secret target metadata + refs
  inventory/synthetic-50.yaml        # fake IDs, connection status SIMULATED
  migrations/core-customer/
    V20261001_01__customer_risk_level.sql
  verification/customer_risk_level.sql
  manifests/release-2026.10.01.yaml
  contracts/approval-envelope.schema.json
  contracts/target-result.schema.json
  ci/Jenkinsfile                     # trusted orchestration; no secret literals
  ci/gitlab-ci.reference.yml          # optional adapter/provider mapping
  adapters/odc/CONTRACT.md            # supported APIs/events, no invented endpoint
  adapters/clouddm/CONTRACT.md        # optional
  runner/dry-run.py                   # no DB imports/connections/credentials
  runner/execute-approved.py         # created only after contract/security gate
  publisher/release-summary.*         # restricted generated view + JSON
  fixtures/approval-events/           # positive/negative simulated envelopes
  runbooks/partial-or-unknown.md
  runbooks/credentials-rotation.md
  lab/                               # only authorized lab deployment manifests
  evidence/<poc-id>/<run-id>/         # new results, never overwrite old evidence
```

SQL scenario bytes chỉ lưu tại migration file; verification file quy định query expectations. Git commit → bundle digest → approval envelope → target result theo [contract](reference-architecture.md#4-common-inventory-và-artifact-contract). Migration version phải hợp lệ và phù hợp baseline stream; không dùng date như bằng chứng version đã applied. Không tự baseline existing targets.

`CONTRACT.md` phải ghi method/path/model/version lấy từ official API/source, auth/permissions, request/response fields, approval readback, how disabled native executor, idempotency, timeout/result callback và evidence links. Endpoint chưa xác minh ghi UNKNOWN; không phát minh `/execute-with-flyway` như native API.

## 5. Gate G0 — contract và preflight chung

| Task | Cách làm | Artifact | Continue / stop |
| --- | --- | --- | --- |
| G0.1 Inventory/identity | Freeze app/env/service/schema/owner/credential refs; 50 synthetic IDs và 20 non-admin identities | `inventory`, role map, target hash | Đổi service/schema sau approval phải invalidates; unknown identity giữ dry-only |
| G0.2 Artifact | Freeze exact Git commit, SQL bytes/encoding, bundle/checks, inventory/target set/policy hashes | Immutable artifact + envelope | Mutable branch fetch hoặc changed hash → reject |
| G0.3 License/artifact | Record app/engine/client/plugin license và pins; retain known image↔source gap | `versions.lock.json`, license notes | Paid features không entitled → unavailable; không auto trial |
| G0.4 Execution boundary | Verify single executor, requester không có deploy secret/trusted job edit/native writer path | Supported configuration + negative-path spec | Nếu chỉ disable UI button mà API/console vẫn write, STOP |
| G0.5 Approval authority | Identify actual reviewer/approver, capture actor và readback immutable artifact/targets | Authority/API contract | Caller boolean/string actor không trusted; self-approval không được PASS |
| G0.6 Results/durability | Design status/writeback vs result link, append-only attempt, retention/export | Result schema + UI link contract | Native SUCCESS không được thay cho external UNKNOWN/FAILED |

No-DB fixture checks dùng chung: tampered artifact, target-set edit, changed inventory route, wrong user/self-approval, duplicate request, concurrent request, lower-stage missing, expired/window gate và publish failure. Require denied dispatch before any executor call. Kết quả là `POLICY_DRY_PASS/FAIL`, không gán SQL/REC runtime PASS.

## 6. POC #1 — ODC governance + Flyway

**Câu hỏi quyết định:** có thể giữ ODC inventory/approval UX, dùng supported external executor và không để creator/native paths chạy migration không? Existing API create/approve/execute evidence không trả lời câu hỏi này.

| Step | Work package | Expected evidence | Decision |
| --- | --- | --- | --- |
| O1 | Contract spike đọc API/source đúng version; tìm supported post-approval hook hoặc approved readback + external dispatch pattern | Exact paths/models/permissions; initial status UNKNOWN trước proof | Nếu không có handoff hoặc phải replace native SQL worker sâu → STOP S2, redirect #2 |
| O2 | Configure inventory/project/env/users và read-only UI target access trong lab được phép | Login/inventory screenshots; wrong-target/outsider denial | Không gán full SoD từ role names |
| O3 | Link Git commit/artifact/target snapshot vào ticket; SQL preview phải exact bytes | Ticket ID + Git/MR + artifact hash; original attachment readback | Nếu SQL/targets có mutable path bypass approval → STOP |
| O4 | Approval→dry adapter, deny native ticket/console write cho managed stream | Authoritative actor events, no double executor, negative routes | Native creator-execute lịch sử FAIL chỉ thành resolved-composed khi architecture mới có evidence |
| O5 | Result publisher: callback supported hoặc explicit CI result link | UI phân biệt native task và external execution; commit/target/result query | Nếu require unsupported direct MetaDB update → STOP writeback; đánh UX link-only hoặc redirect |
| O6 | Sau gates/quyền tầng O, execute 4-target scenario + mapped correctness/recovery | Engine history, independent observer checks, current statuses | Full release không SUCCESS trước postchecks/audit durable |

Không dùng ODC batch Execute để chạy Flyway rồi giữ native executor tiếp tục chạy SQL. Nếu chỉ giữ ticket có SQL nhưng native scheduler autoexec vẫn reachable, đó là hard gate FAIL. Không sửa encryption/flow/native result tables trực tiếp để làm demo.

**Expected walkthrough:** Login → project/inventory → linked Git change/ticket → SQL/target preview → reviewer/DBA approval → approved target list → external CI/runner status link → result/history/evidence. Nếu native platform không có external-result screen, link CI view phải explicit; không chụp native Execution Records như external success.

ODC runtime cũ chứng minh một phần native UI/flow, **không** chứng minh O1/O4/O5 adapter. Cần một delta cụ thể (supported integration/config/code với owner) trước rerun SQL-11, REC-02/08/10, GOV-03. [Source survey](research-round-2/coordinator/odc-source-survey-20261006.md).

## 7. POC #2 — Git/Jenkins/Flyway composition

**Câu hỏi quyết định:** team có thể quản lý một release/target set và audit tập trung bằng composition nhỏ, với UX đủ tốt và ownership chấp nhận được không?

| Step | Work package | Expected evidence | Decision |
| --- | --- | --- | --- |
| C1 | Trusted deployment job/library + role restrictions; Git SQL/MR và immutable artifact | Job config/source commit; requester no Configure/Replay/secret access | Không chạy developer-supplied shell/Jenkinsfile có PROD secret |
| C2 | Generated inventory view, target ID choice và release preview | 50-record import/filter/selection, schema/owner/env visible | Không free-form JDBC/command parameters; fake records excluded tầng O |
| C3 | Reviewer input SIT/UAT; DBA input MOCKPROD capture actual actor | Actor/time/hash envelope; requester-self approval deny | Admin exception documented; job editor không regular requester |
| C4 | Dry-run deployment stages + status publisher/links | Same commit/artifact, selected-target map, simulated stop/hold | CLI wrapper không inventory/audit/selection UI → chưa đủ scope |
| C5 | Canonical per-schema mutex và durable attempt state; duplicate admission | Two jobs same target serialized; alias contention; unknown attempt persists restart | `disableConcurrentBuilds` only cùng job không đủ; no lease-based blind redispatch |
| C6 | Approved isolated Oracle scenario; `info/validate/migrate/postcheck/publish` | Exact engine history + query/output+CI identity/per-target audit | Broken verify/history/log publish → HOLD/reconcile, no auto retry |
| C7 | Recovery/export/rotation walkthrough | Fail/unknown evidence, recovery decision, preserved logs after restart | Recovery NOT_RUN nếu không instrumentation; không declare adoption GO |

Initial scope chỉ generated view + trusted jobs/runner/publisher, không new full platform UI. Nếu budget/owner muốn một UI duy nhất như Bytebase, C UX có two applications; report điểm này. GitLab Premium path chỉ substitute provider khi entitlement confirmed; giữ cùng target/result contract và negative tests.

## 8. Optional POC #3 — CloudDM workflow + Flyway

Mở sau #1 contract hoặc khi owner ưu tiên CloudDM GitLab intake; không là default native correctness rerun. Source v4.3.0 Apache/license/counter-path review đã complete, không đặt lại stale pricing 10/5 như blocker.

1. Xác minh supported flow/action **sau approval** có thể gọi sole external runner; HttpCall/webhook tồn tại không đủ. Record payload fields, actor/hash/target readback, authentication, delivery dedup, callback/polling và status contract.
2. Dùng pinned [GitLab guide](https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/docs/guides/gitlab-cicd.en.md): exact commit archive/project/branch/script-directory/target, webhook signing; GitLab version nội bộ phải compatible, không tự upgrade nó.
3. Giữ deploy secret ở runner/manager; native executor/console không có production write. Guide ghi GitLab integration tokens plaintext MetaDB: scoped token + restricted storage/backup hoặc supported alternative intake; rotation smoke riêng.
4. Làm dry approval→adapter→result link và negative tests trước Oracle. Hook/native denial/writeback fail thì STOP S3; không viết custom migration engine để vá v4.3.0.
5. Tầng O dùng cùng 45-case mapping nhưng label **COMPOSED**, không native PASS. Artifact review source/default compile finding không thay đổi.

## 9. UI capability checklist cho demo

`Native` = product UI/API có chức năng theo evidence chỉ rõ; `Integrated` = qua component khác và cần wiring; `Custom development required` = file/service/view phải viết; `Not available` = không có bước đó trong native product đã xét. Integrated/Custom cells đều **NOT_RUN cho stack mới**.

| Demo step | #1 ODC+Flyway | #2 Git/Jenkins+Flyway | #3 CloudDM+Flyway |
| --- | --- | --- | --- |
| Login | Native ODC, partial historical RUNTIME | Native Git/Jenkins, identity mapping integrated | Native DOC/SOURCE, new runtime NOT_RUN |
| View inventory | Native ODC project/datasource RUNTIME | Custom development required manifest→view; Jenkins report link | Native datasource/environment SOURCE |
| Create/select change | Native ticket + integrated Git artifact | Native MR/build + custom release envelope | Native flow/ticket SOURCE + Git intake DOC |
| SQL stored/traced in Git | Integrated/custom hash binding | Native Git + custom immutable artifact | Native exact commit intake DOC + custom engine handoff |
| Review SQL/diff/findings | Native SQL preview + integrated Git/validation | Native Git diff/comments + custom validation gate | Native audit/attachment SOURCE + integrated Git diff |
| Approve | Native approval historical RUNTIME + custom external binding | Native input plugin DOC + custom actor/hash checks | Native approval SOURCE + custom external binding |
| Select Oracle target/schema | Native project/database UI + custom approved-snapshot mapping | Custom allowlist/inventory choice, no raw DSN | Native datasource/environment + custom target snapshot |
| Execute/trigger pipeline | Custom supported adapter **UNKNOWN**; native executor disabled | Integrated engine + custom runner/trusted job | Custom supported action **UNKNOWN**; native executor disabled |
| Verification | Custom runner/observer gates | Custom runner/observer gates | Custom runner/observer gates |
| Result screen | Native ticket; external result integration UNKNOWN, otherwise explicit CI link | Native build/status + custom per-target summary | Native flow history; callback/result integration UNKNOWN |
| Audit/history | Native partial + custom durable correlated record | Native build/MR + custom durable correlated record | Native SOURCE logs/flow + custom correlation/export |
| Native external Oracle executor UI | **Not available as established capability** | Not available; composition UI above | **Not available as established capability** |

Screenshots capture actual screens trong lab sau này, ghi source/build/edition/run ID. Wireframes/fixture screenshots label DESIGN/SIMULATION. Videos/screenshots chính thức dùng DOC; không Oracle evidence.

## 10. Practical scenario và 45-case mapping

Common scenario (**file design, không chạy**):

```sql
ALTER TABLE CUSTOMER ADD RISK_LEVEL VARCHAR2(20);
```

Targets logical: `CORE_DEV`, `CORE_SIT`, `CORE_UAT`, `CORE_PROD` / `CUSTOMER_SCHEMA`; actual lab PROD tier là **MOCKPROD**. Nếu một DB chứa bốn schemas, dùng actual schema owners khác nhau và đổi manifest; không tạo cùng user `CUSTOMER_SCHEMA` bốn lần trên cùng service. Baseline `CUSTOMER` được DBA chuẩn bị trong isolated scope sau authorization, không lấy table production.

Expected trace: Git exact commit → change/ticket/MR ID → automated checks → Reviewer approval → frozen target snapshot → DEV verified → SIT verified → UAT verified → distinct DBA PROD approval → MOCKPROD verified → audit query. Add-column verification đọc metadata type/length semantics theo DBA-confirmed baseline; không claim DDL row count hoặc automatic rollback.

| Stage / IDs giữ nguyên | Điều POC mới phải chứng minh | Evidence bắt buộc / gate |
| --- | --- | --- |
| MODEL-01–12 | Inventory stable IDs, exact approved artifact, target selection, controlled continuation, failure state/UI/history/access | 50 synthetic selection và 4 real lab targets tách evidence; MODEL-12 gap inventory PASS không product acceptance |
| SQL-01/02/03 | DDL/DML version order, history, once-on-replay effect + structured target result | History before/after + independent SQL effect; scenario ALTER chỉ đủ một phần SQL-02 |
| SQL-04–09/12 | Procedure/function/package spec+body/trigger/anonymous block/slash/q-quote/nested parser | VALID objects + invocation/effect, parsed bytes/hash; exact required workload hash |
| SQL-10 | Required SQL*Plus directives qua supported/licensed path hoặc pre-execution reject | Community limitations explicit; nếu directives mandatory nhưng unavailable thì STOP scope, không silently strip |
| SQL-11 | Engine success nhưng INVALID phải thành APPLIED_INVALID/FAIL + block promotion | ALL_OBJECTS object type/owner/name + ALL_ERRORS + terminal central result; package body test riêng |
| REC-01/03/04 | Known SQL failure/partial DDL, no automatic replay, DBA-directed correction | First statement effect remains, failed statement/error known, release HOLD, recovery record |
| REC-02/08/10 | Replay skip, changed checksum pre-write reject, duplicate request stable decision | Target ledger + immutable SQL hash + attempt admission record + effects; webhook dedup riêng không đủ |
| REC-05/06/07/11/12 | Controlled commit/ledger/central/network crash, restart/stale-session reconciliation | Observable barrier/process/session identity, durable intent/history/object states; no replay after uncertain outcome |
| REC-09, GOV-07 | Cross-job/cross-dispatch concurrency and alias targets, no duplicate executor | Same canonical service/schema lock; denied/serialized jobs and accurate records; multiple-replica case NOT_RUN nếu topology thiếu |
| GOV-01/02/03/04/05 | Full actor/hash/target linkage, mutation invalidation, requester denial, promotion, actual CI identity | UI/API/console negative tests + named runner job; build reference string không actual CI runtime |
| GOV-06/08/09 | Backup/restore, no secret exposure, audit durable/export after restart/rotation | Restore verification; sanitized export; target ahead-of-backup detected. Screenshot/log success không đủ |

Dùng copy fixtures từ [workloads manifest](workloads/manifest.json) sau khi verify SHA, không sửa workload bytes trong research repo. Oracle actual versions/driver/object coverage ghi riêng. Dry negative fixture cases có IDs mới `DRY-01…`, chỉ **mapped_to** old IDs; không thay expected hoặc historical status. New runtime record per candidate có `native_or_composed`, exact pins, criterion ID, expected reference, actual/status, evidence references và limitations.

## 11. Controlled failure/recovery demonstration

Chỉ tầng O có isolated authorization/instrumentation; không dùng deployment restart tình cờ làm recovery proof. Không dùng `sleep` timing để đoán “đã commit”; worker/engine checkpoint hoặc observer signal phải thấy được boundary.

| Probe | Instrumentation / expectation | Operator action / pass boundary |
| --- | --- | --- |
| Pre-dispatch deny | Wrong hash/target/actor, expired approval hoặc unverified lower stage | Zero SQL write; state DENIED/HOLD, auditable reason |
| Partial Oracle DDL | Two-statement disposable fixture: first DDL succeeds, next intentionally invalid; stop-on-error | First object remains, result PARTIAL; no replay; DBA inspect/approve forward recovery |
| Invalid PL/SQL | Reviewed new object compile-invalid fixture | Capture owner/type/ALL_ERRORS, APPLIED_INVALID even if engine history success; promotion blocked |
| Commit before engine history | Instrumented boundary **inside actual executor path**, không mock success row | UNKNOWN_OUTCOME persists restart; inspect target effect/history; no re-dispatch until decision |
| History before central result | Barrier after observed successful history write before publisher ack | Reconcile central state from verified history/effect; no SQL replay |
| Network/timeout | Controlled lab network proxy with exact before/during/after-ack checkpoint | Distinguish known-not-started vs uncertain; worker session observed; no retry blindly |
| Stale session/lock | Worker terminated with observed session/lock; retry request while session alive | HOLD; DBA verifies stopped session before release. No auto kill ANY session or expiry-based takeover |
| Concurrent release / alias | Two different jobs map aliases to same physical schema | One holder/executor; second waits/rejects; records correct after first terminal; unresolved outcome still blocks |
| Central restart/export | Restart lab controller after persisted intent; preserve approved artifact/result/logs | Durable attempts/audit recover; callbacks cannot overwrite terminal state; new dispatch checks HOLD |
| Target restore / central backup | Approved restoration in disposable scope with before/after checkpoint | Detect divergence; stop release, reconcile. Baseline/repair never silently aligns away unknown effects |

Flyway `repair`/Liquibase `release-locks` không cleanup Oracle object/data. Recovery lựa chọn forward-fix migration mới, reviewed compensation, approved engine-history correction sau state inspection, hoặc DBA restore theo target scope. Không drop CUSTOMER/RISK_LEVEL tự động như “rollback demo”; compensating DROP có data/compatibility implications.

## 12. Evidence pack, retention và review

Mỗi run lưu mới dưới `evidence/<poc-id>/<run-id>/`; không viết vào `oracle-poc-*`, `bytebase-poc-*`, frozen cases hoặc source manifests cũ. Raw private logs restricted; published report chỉ sanitized allowlist, không token/password/wallet/key/cookie.

| Artifact | Contents |
| --- | --- |
| `run-metadata.json` | Mode DRY/APP_RUNTIME/ORACLE_RUNTIME, date, app/engine/driver/image/plugins, Oracle actual version/edition, topology, executor/principal, authorized scope |
| `release-envelope.json` | Commit/MR/change/requester, artifact/SQL/inventory/target/policy digests, authenticated approval actors/time |
| `targets-before-after.json` | Actual target/service/schema identity, baseline/version/history/object/effect state; no secrets |
| `executions.jsonl` | Append-only dispatch/attempt/lock/session/terminal/reconcile events, job/task IDs, durations/errors and state |
| `cases.json` | Criterion IDs/expected refs, native-or-composed, status PASS/PARTIAL/FAIL/BLOCKED/NOT_RUN, evidence/limits |
| `screenshots/` + manifest | Login/inventory/SQL-review/approval/target/status/audit views; build/edition/hash and simulation labels |
| `audit-export.json` | Full release query answer Who/What/When/Commit/ApprovedBy/Where/Result + evidence refs |
| `recovery-decisions.md` | Partial/unknown detection, inspected state, DBA decision/approval, exact repair/forward/restore steps, blocked targets |
| `hashes.json` | SHA-256 artifacts/screens/exports; secret scan outcome and publication allowlist |

Retention duration do owner chọn trước adoption; lab ít nhất phải giữ trọn tất cả acceptance artifacts qua restart/export/restore và review. Không suy unexpired Jenkins artifacts hoặc ODC ticket logs là permanent audit. Read role và publish role tách nhau; reviewers thử truy vấn một release và một target từ UI/report không ghép thủ công nhiều private logs. Export query không chứa plaintext secret; executed SQL/artifact restricted và traceable.

Review do DBA + DevOps kiểm kết quả actual vs expected, failure/uncertain case và contract status; không chỉ đếm PASS. Oracle 26ai cũ không thay Oracle version nội bộ. Scale50/lower-env isolation/unmeasured maintenance ghi rõ limits; chưa benchmark hiệu năng ở stage này.

## 13. Acceptance và stop/redirect rules

| Outcome | Rule |
| --- | --- |
| Contract GO (#1/#3) | Supported handoff/auth/readback, same artifact+targets, native execution deny, accountable external result/link; license/artifact scope clear |
| Contract STOP → #2 | Hook absent, deep fork needed, mutable target/SQL, unsupported MetaDB mutation, hoặc native writer vẫn bypass. Record findings; không broaden platform build |
| Dry demo complete | All intended screens/links và tamper/actor/target/promotion/duplicate negatives demonstrated, simulations labelled; Oracle cases remain NOT_RUN |
| Oracle POC complete | All relevant 45 expected evaluated with actual evidence/limits; no blind retry, no hidden INVALID/partial/unknown. NOT_RUN/blockers có explanation, không tuyên bố production GO |
| Adoption candidate | Required SQL/GOV/REC gates pass on exact edition/Oracle + maintained license/secret/audit/recovery contract + owner/budget decision. Missing hard requirement giữ NO-GO/CONDITIONAL |
| Scale/benchmark next | Chỉ sau correctness/governance; test actual multi-instance topology, 50 real endpoints/concurrency và 20-user usage separately theo frozen benchmark spec, với authorization mới |

POC #1 có thể kết thúc STOP contract vẫn là decision evidence hữu ích; để đạt intended workflow demo tiếp tục #2. Không tự thay toàn mục tiêu bằng một failed spike. Nếu C không đủ UX hoặc maintenance owner, so commercial Bytebase EE quote thay vì gọi multiple tools thành single platform.

## 14. Bước kỹ thuật đầu tiên cho DevOps/DBA ngày mai

1. DevOps chọn Git/CI lab phù hợp existing entitlement; DBA điền Oracle metadata/target/schema ownership bằng dữ liệu sanitized. Chưa cung cấp PROD secrets.
2. Tạo **lab repo riêng** với skeleton ở mục 4, scenario SQL, 50 synthetic inventory records, 20 role identities, common manifest/envelope/result schemas; freeze commit/hash.
3. Hoàn tất G0 contract #1: đường approval→external dispatch, native denial và result linkage. Nếu unsupported, ghi STOP và dùng #2; optional #3 chỉ khi bounded hook có lợi rõ.
4. Trong lượt lab được phép, dựng actual UI/controller/storage theo pinned manifests, làm walkthrough và DRY negative cases. Người xem phải chọn target, thấy SQL/commit/actor/status từ UI/report.
5. Chỉ sau contract/actor/secret gates và isolated SQL authorization, cấp deployer/observer cho tầng O, chạy 4-target scenario rồi mapped SQL/GOV/REC; fault injection có scope riêng. Export/review results before any adoption decision.

Checklist handoff đã trả lời: hai POC chính/optional thứ ba; điều phải chứng minh; exact workflow/screens; OSS/commercial boundaries; custom scope; Oracle DOC vs historical RUNTIME; failed-release protocol; future files/components/pins; first technical steps và explicit stop rules. Các unknown có nơi giải, không yêu cầu người dùng tự nghiên cứu public tool/license trước khi bắt đầu.
