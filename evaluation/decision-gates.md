# Decision gates before implementation

Date: **07 October 2026**. Scope: approximately **50 Oracle instances / 20 human users**. This is decision closure, **not implementation**. No infrastructure, pipeline, candidate software or Oracle SQL was run; no vendor was contacted and no trial was started.

## 1. Executive conclusion

**Proceed to a bounded S6 Git + Jenkins + Flyway Community POC. Stop S2 and S3 work in this phase. Retain Bytebase Enterprise for a commercial check and exact-edition regression.** S6 can use a trusted Pipeline/shared library, Git inventory, authenticated Input steps, shared target locks, durable execution records, and generated HTML/JSON reports. A new migration portal, PostgreSQL, adapter daemon and new secret manager are not phase-1 requirements. The durable admission/recovery code remains substantial enough to need an owner and failure testing; Jenkins build history alone cannot replace it. **[DESIGN, DOC]** See sections 3, 7 and 8.

**S2 is YELLOW**, precisely for an **approval-only, externally linked result** composition. The reviewed ODC source has request/detail APIs, MANUAL wait, and an approved-task notification. Those provide a plausible bounded bridge; they do not establish a stable external-executor API, immutable approval envelope, trustworthy CI-to-human attribution, or an external completion lifecycle. A physically read-only ODC Oracle identity is the viable execution boundary. Native ODC SUCCESS is unnecessary when a linked centralized result is accepted. The remaining ODC contract adds another authority and upgrade tests while retaining most S6 execution/recovery work. **Gate A is not closed: STOP S2 for this phase**, without claiming that such a bridge is impossible. **[SOURCE, DESIGN, UNKNOWN, NOT_RUN]**

**S3 is RED at the cleaner-contract challenger gate: STOP.** CloudDM's documented `HttpCall` is an inbound workflow trigger. Its separate callback runs at native change finish and carries no approved execution envelope. It is not materially cleaner than ODC's approval notification/readback bridge. **[DOC, SOURCE]** The historical native Oracle NO-GO remains unchanged.

**S6 GREEN means research feasibility to start the stated POC, not adoption or proven Oracle correctness.** Gate C has a bounded design on documented interfaces; durable-state, identity, locking, restart and Oracle acceptance tests are all **NOT_RUN**. Failure of the tests in section 11 reverses the recommendation. Bytebase EE remains **HOLD**, since neither its actual quote nor the required EE regression exists. **[DESIGN, UNKNOWN, NOT_RUN]**

Authoritative inputs were reread: [solution shortlist](solution-shortlist.md), [reference architecture](reference-architecture.md), [POC plan](poc-plan.md), [feature catalog](tool-feature-catalog.md), [ODC source survey](research-round-2/coordinator/odc-source-survey-20261006.md), [CloudDM artifact review](research-round-2/coordinator/clouddm-v430-artifact-review-20261007.md), [ODC runtime results](../ODC-ORACLE-POC-RESULTS.md), [Bytebase runtime results](../BYTEBASE-ORACLE-POC-RESULTS.md), [collected engine evidence](../EVIDENCE.md), and the existing [POC design validation](poc-design-validation.md). This document refines the latter's minimum implementation boundary and supersedes the older shortlist's S2-first POC order. It does not change historical criteria, PASS/PARTIAL/FAIL, native verdicts or evidence files.

Evidence labels throughout: **DOC** = official documented behavior; **SOURCE** = inspected pinned implementation; **RUNTIME** = existing recorded experiment only; **DESIGN** = proposed controls, not capability evidence; **UNKNOWN** = unresolved information; **NOT_RUN** = proposed test not performed. A source path or documented step is not end-to-end runtime proof.

## 2. ODC external-executor feasibility

### Reviewed scope and support boundary

The exact reviewed source is `oceanbase/odc@d517c0f27971642fb0cd7565fd61ab2309875ec3`, matching the current public `main` observed in this review. Public release metadata and the existing image pin do **not** map this commit to the historical runtime image `4.4.1-20260116`. The source survey already records that gap. Official ODC 4.5.0 release notes describe OpenAPI/MCP work, but do not establish the exact external-executor contract below. No later-build absence is asserted. **[SOURCE, DOC, UNKNOWN]** [Source pin][odc-main], [4.5.0 release notes][odc-450], [existing pin limits](research-round-2/coordinator/odc-source-survey-20261006.md).

### 2.1 Request creation: real REST route, unclosed supported CI contract

`FlowInstanceController.createFlowInstance` exposes **`POST /api/v2/flow/flowInstances`** (root mapping plus `/`; creation returns a list). The request is `CreateFlowInstanceReq`; `taskType: ASYNC` selects `DatabaseChangeParameters`. Permission checks and server-side authentication apply; this is not an unauthenticated endpoint. **[SOURCE]** [Controller][odc-controller], [request model][odc-create], [SQL parameters][odc-parameters], [service][odc-service].

| Required input | What the inspected API actually accepts | Bridge obligation / limit |
| --- | --- | --- |
| Exact SQL | `parameters.sqlContent`, or SQL object IDs/names | Inline ordered SQL can be compared with frozen bytes. For uploaded files, read and hash actual content, not an ID/name. Preserve boundaries, encoding, delimiters and substitution parameters. **[SOURCE, DESIGN]** |
| Git commit / artifact digest / external release ID | No dedicated fields in this request DTO; `description` is available | Put reviewable identifiers and the external result URL in the description; keep the authoritative typed envelope in the trusted bundle/state store. Text metadata is not native enforcement. **[SOURCE, DESIGN]** |
| Target datasource / schema | `databaseId`; connection/database/project fields are server-populated, read-only request properties | Resolve an allowlisted target to the ODC database object; verify the actual Oracle service/PDB/schema independently before dispatch. Do not accept arbitrary client JDBC/schema values. **[SOURCE, DESIGN]** |
| Requester | Authenticated creator, not a supplied human requester field | A CI account creates a CI-owned ticket. Preserve the initiating human separately through an authenticated Git/CI intake; a description string cannot establish human identity or SoD. **[SOURCE, DESIGN]** |
| Approval-first behavior | `executionStrategy`, whose default is `AUTO` | The bridge must submit `MANUAL`, reject AUTO/TIMER for the managed stream, and confirm policy/required approval nodes. MANUAL is a wait strategy, not an executor-disable switch. **[SOURCE, DESIGN]** |

**Answer:** external creation exists in source. A documented, versioned public API/service-account authentication contract for CI automation of this specific lifecycle is **UNKNOWN**; UI REST existence does not establish that contract. The earlier lab's authenticated session/API access is **RUNTIME** for that build only, not proof of a maintainable noninteractive service identity. Gate A needs the supported build, auth method, scopes and upgrade commitment established before relying on it.

**Concrete inbound authentication [SOURCE]:** `UsernamePasswordConfigureHelper.configure` wires local form login at **`POST /api/v2/iam/login`**, with `CustomUsernamePasswordAuthenticationFilter` reading `username` and decrypting the `password` form parameter. Subsequent authenticated context supplies the ODC user; `DefaultAuthenticationFacade.currentUserId` reads that user from Spring's security context. Optional `CustomBasicAuthenticationFilter` is wired only when **`odc.web.security.basic-authentication.enabled`** is true (default false), and the implementation advises against production use. Thus session-based local login and optional Basic are implemented mechanisms, not a missing-auth claim. A supported scoped CI API token/service account for these flow routes remains unestablished, and enabling Basic is not the recommended way to close that contract. [Auth wiring][odc-auth-wiring], [login filter][odc-login-filter], [security properties][odc-security-properties], [principal facade][odc-auth-facade].

### 2.2 Approval readback and immutability

**`GET /api/v2/flow/flowInstances/{id}`** returns `FlowInstanceDetailResp`: flow identity/status, creator, timestamps, description, database/connection metadata, typed parameters, execution strategy and `nodeList`. `FlowNodeInstanceDetailResp` includes node identity/type/status, operator, candidates, comment, auto-approval indication and timestamps. `FlowApprovalInstance.internalOperate` records the authenticated operator for a non-auto approval requiring an operator. Approval/rejection routes are **`POST /{id}/approve`** and **`POST /{id}/reject`** under the same prefix. **[SOURCE]** [Controller][odc-controller], [detail model][odc-detail], [node model][odc-node], [approval instance][odc-approval].

| Readback requirement | Finding | Required bridge interpretation |
| --- | --- | --- |
| Approved state | Flow status plus required node states exist | Check **all required approval nodes**, rejection/cancellation, MANUAL pending execution and policy, not a single APPROVED event or generic completed flag. **[SOURCE, DESIGN]** |
| Authenticated approver | Persisted approval operator and time exist in the reviewed path | Validate required role and authenticated actor per node. Some response mapping uses creator as a display fallback when operator is absent; that fallback does not prove an approval. Reject missing/ambiguous actors and auto-approval when policy needs a human. **[SOURCE, DESIGN]** |
| Requester | Creator identity exists | Preserve service creator separately from authenticated initiating human; apply SoD to the latter too. Do not let the CI account disguise self-approval by its initiating user. **[SOURCE, DESIGN]** |
| Approved SQL | Typed parameters are returned | Hash frozen SQL/files plus executable options, compare with readback before authorization; fail closed on content that cannot be recovered. **[SOURCE, DESIGN]** |
| Datasource/schema | Database metadata is resolved from the referenced database | The reviewed detail mapper reads current database metadata. Freeze routing/identity alongside SQL; current datasource/credential changes are not an immutable approved target snapshot. **[SOURCE, DESIGN]** |
| Time / task identity | Flow and node IDs/times; task references exist | Record flow, task and node IDs separately; never assume notification task-entity ID equals flow-instance ID. **[SOURCE, DESIGN]** |

**Immutability is not established.** The reviewed flow controller has no generic SQL update route, but that is not proof of an immutable envelope: linked datasource/connection configuration and external file references remain dependencies. No inspected response exposes a native approval hash over the full artifact, target, inventory and trusted policy snapshot. **[SOURCE, UNKNOWN]**

**Bounded detection design:** create the frozen bundle first; show its SQL, hashes, target/service/schema and policy at approval; retain the canonical snapshot and approval-node actors; reread those fields and current routing just before durable dispatch admission. Any changed SQL/target/route/principal/policy, incomplete readback or expired/rejected request requires a new envelope and approval. Password rotation alone records the used secret version; a changed principal requires reapproval. The authority's cancellation cutoff and the race between readback/admission/cancellation must be explicit: no bridge can revoke already committed Oracle DDL. An atomic supported authorization/claim interface has **not** been established. **[DESIGN, UNKNOWN, NOT_RUN]**

### 2.3 Exact handoff: notification hint, not execution authorization

There is a concrete approved-task notification path. It is useful, but generic approval-integration documentation is not the evidence for this path: that integration makes **ODC call an external approval service**, rather than export a migration engine contract. **[DOC]** [Pinned approval integration][odc-approval-doc].

| Trace item | Exact inspected path / behavior | Meaning for external dispatch |
| --- | --- | --- |
| Approval action | `FlowInstanceController.approve` → `FlowInstanceService.approve` | Authenticated ODC approval route, not a Flyway route. **[SOURCE]** [Controller][odc-controller], [service][odc-service] |
| Event producer | `FlowInstanceService.approve`: `EventBuilder.ofApprovedTask(...)` → `broker.enqueueEvent(...)`, before `completeApprovalInstance(...)` in the transaction | Event construction/enqueue precedes completion of this approval action; delivery/commit ordering must not be assumed. Multiple-node approvals may still be incomplete. Requery authority. **[SOURCE]** [Service][odc-service] |
| Event type / labels | `TaskEvent.APPROVED`; `EventBuilder.ofApprovedTask`, `ofTask`, `resolveLabels` | Labels include approver ID, creator ID, task type/status/entity ID, connection/database/project identifiers, description, trigger time; ordinary flow mapping also resolves a flow task ID. This is not a mandatory artifact/target digest payload. **[SOURCE]** [Event enum][odc-event], [builder][odc-event-builder] |
| Outbound endpoint / body | `HttpSender.send` → HTTP request to configured `WebhookChannelConfig.webhook`; method, headers and body are templated | No fixed Flyway endpoint or immutable deployment payload. Receiver design could take only the flow ID, then authenticated readback. **[SOURCE, DESIGN]** [Sender][odc-http], [config][odc-webhook] |
| Authentication | ODC approve/readback use its authenticated server security context. Outbound webhook supports configured header templates; the config also has a `sign` field | HTTPS plus a managed static authorization header is a possible configuration. Automatic artifact-signing/HMAC verification was not demonstrated by the inspected sender. A `sign` field alone is not proof. CI readback service-account/API-key support for the selected build remains UNKNOWN. **[SOURCE, DOC, DESIGN, UNKNOWN]** [Sender][odc-http], [custom channel docs][odc-channel-doc] |
| Delivery acknowledgement | HTTP response validation accepts configured content, with HTTP success evaluated by the sender | Notification delivery acknowledgement is not a durable Flyway execution receipt or proof that all gates passed. Duplicate/lost notifications must not cause duplicate SQL. **[SOURCE, DESIGN]** |
| Plugin / task extension | `OdcRuntimeDelegateMapper` maps ASYNC task type to native `DatabaseChangeRuntimeFlowableTask` | No supported external-runner extension registration was established in these paths. Changing this switch/delegate or faking native completion would couple to internals. **[SOURCE, UNKNOWN]** [Mapper][odc-mapper] |

**Practical handoff if S2 is reopened:** a trusted Jenkins library can poll known ticket IDs and use notifications only as latency hints. This avoids operating a new webhook receiver daemon. Only authenticated readback plus the frozen envelope and durable claim authorize execution; a received message saying approved never does. Required event loss, duplicate, premature approval and cancellation tests remain **NOT_RUN**. **[DESIGN]**

### 2.4 Prevent ODC from executing the managed migration

The native route **`POST /api/v2/flow/flowInstances/{id}/tasks/execute`** calls `FlowTaskInstanceService.executeTask`. `FlowPermissionHelper.withExecutableCheck` permits the flow creator or project OWNER/DBA; successful confirmation starts the native task. `ServiceTaskPendingListener` implements MANUAL waiting. A configurable pending-execution expiry exists (`odc.task.default-wait-execution-expiration-interval-hours`, default 48 in this source); MANUAL is not a permanent external-job lifecycle. **[SOURCE]** [Controller][odc-controller], [task service][odc-task-service], [permissions][odc-permissions], [pending listener][odc-pending], [task properties][odc-properties].

Historical **RUNTIME** found MANUAL `WAIT_FOR_EXECUTION` working, and a creator's post-approval Execute accepted. That establishes the historical workflow limitation; it is not an authorization bypass finding, nor a proof that different current configuration cannot help. [ODC runtime results](../ODC-ORACLE-POC-RESULTS.md).

| Control | Can it establish Flyway as sole writer? |
| --- | --- |
| Hide Execute / remove a page | **No.** Native API and other write paths remain. **[DESIGN]** |
| Reduce ODC roles / deny SQL console | Useful, but not sufficient by itself: creator/OWNER/DBA execution behavior must be accounted for; console denial does not disable async tasks. **[SOURCE, DESIGN]** |
| Set MANUAL / constrain intake to MANUAL | Stops automatic immediate execution in this path; does not make Execute/API/native task incapable of write. **[SOURCE]** |
| Gateway deny execute route | Possible extra guard, with versioned route tests; not sufficient for alternate tasks, SQL console or direct network access. **[DESIGN]** |
| Physically read-only ODC Oracle credential | **Required viable boundary.** A dedicated observer, not the schema owner: only approved metadata/SELECT access and session access; no DML/DDL, ANY privileges, schema-owner rights, writable definer-rights routines or access to the runner's deploy secret. All ODC connections for managed targets must obey it. **[DESIGN, NOT_RUN]** |

The bridge may need ODC's application-level CHANGE permission to create/review a ticket while its actual database grants remain read-only. That pairing, SQL preview under observer grants, credential-edit restrictions and every native write path must be tested on the exact build. ODC administrators must not be able to substitute the deploy principal through an ordinary requester path. A DBA/admin override is a privileged operational exception requiring audit. No required grants were issued in this round. **[DESIGN, UNKNOWN, NOT_RUN]**

### 2.5 Result correlation without false native SUCCESS

The reviewed flow controller provides native task log/result/download routes and approval comments, but no general external-result completion, post-run comment, attachment or generic metadata-update route. Native result endpoints return native-task results; they are not evidence of a writeback API. **[SOURCE, UNKNOWN]** [Controller][odc-controller].

The least invasive correlation is **an external Jenkins/release URL in the ticket description at creation**, plus ODC flow/task IDs in Jenkins' immutable release records/report. The description is returned in flow detail. A URL's clickable rendering, retention and ticket expiry behavior need exact-build UI verification; it can still be a readable URL. Approval comments are not a general executor-writeback mechanism. **[SOURCE, DESIGN, NOT_RUN]** [Request][odc-create], [detail][odc-detail].

If this is used, the UI/report must explicitly distinguish **ODC approval/native WAIT/expiry/cancel status** from **external Flyway deployment state**. The link must resolve the particular release/envelope and attempts, including failure/HOLD, not Jenkins `lastSuccessfulBuild`. External results must survive job deletion/retention policy. Do not mark an unexecuted ODC native task SUCCESS. There is **no established native Flyway-completion writeback contract** in this review. **[DESIGN, UNKNOWN]**

### S2 verdict: YELLOW; Gate A unclosed, STOP this phase

A link-only bridge using MANUAL, readback/polling, an observer credential and owned binding/correlation code is a **bounded DESIGN possibility**, hence **YELLOW**, rather than an unsupported claim of impossibility. It is not GREEN because the exact build's supported CI auth/API, human attribution, immutable readback, revocation/claim rules and linked-result lifecycle are unproven. If native external-result SUCCESS or a replaceable internal task engine becomes a hard requirement, that variant needs an unestablished extension or deep patch and is **RED**. Do not build that fork to rescue S2. Reopen the limited bridge only with the six Gate A proofs and an owner who values its additional governance UI enough to carry its extra lifecycle. **[SOURCE, DESIGN, UNKNOWN, NOT_RUN]**

## 3. Jenkins/Flyway feasibility

### Minimum centralized workflow

For 20 authenticated users, one Jenkins controller and a reviewed inventory of roughly 50 **instances**, phase 1 can offer a centrally selected target-ID list, SQL/bundle preview, reviewer gate, DBA PROD gate, staged deployment, and release/target history through Jenkins plus generated reports. Actual target count may exceed instance count because services/PDBs/schemas/streams are separate deployment targets; neither 50 simultaneous sessions nor production scale is assumed. Start at concurrency **1**. **[DESIGN]**

Use a trusted deployment job/shared library pinned to reviewed code. Untrusted MR validation produces no production secret access. Users select allowlisted target IDs; trusted code resolves the approved inventory snapshot, service/schema and credential reference. Input parameters must not select executable branches, shell commands, arbitrary JDBC URLs, schemas or secret paths. Maintainers own deployment code/configuration; requester accounts do not get Configure, Replay, privileged agent access or script-console authority. **[DESIGN]** Supported shared-library and credential/build-security boundaries: **[DOC]** [Shared libraries][jenkins-library], [build security][jenkins-security], [credentials][jenkins-credentials].

The initial selection form can use built-in choices for reviewed environment/group presets and a target-ID text list validated against that snapshot. A read-only inventory report supplies the available IDs; the next preview shows the complete resolved set before approval. This is a bounded selection integration, not a claim that Jenkins natively has a DB inventory browser or multi-select grid. Require no Active Choices scripting or custom frontend in phase 1. **[DESIGN]**

Jenkins Input supplies authenticated `submitterParameter` and can restrict submitters. Administrators have an exception to the submitter restriction. Therefore the trusted library must additionally check the captured actor against the reviewed role roster and against the authenticated requester; an administrator who self-approves still fails the application SoD check. Global controller administrators remain a privileged trust boundary and require an audited exception policy, not a promise that Pipeline can constrain an administrator who can rewrite it. **[DOC, DESIGN]** [Input step][jenkins-input].

The Jenkins/Flyway evidence is **DOC + DESIGN**, not a working assembled system. Reference package versions from the catalog are Jenkins LTS **2.580.1** and Flyway **13.9.0**. Current official plugin pages reviewed here show Lockable Resources **1560.va_b_cd589f23eb_** (minimum Jenkins 2.541.3, MIT) and HTML Publisher **429** (minimum Jenkins 2.479.1). These are package references, not installed/accepted pins; capture actual distribution, compatible dependencies, licenses and digests before the POC. **[DOC, NOT_RUN]** [Catalog](tool-feature-catalog.md), [Lockable Resources][jenkins-lock], [HTML Publisher][jenkins-html], [Flyway OSS][flyway-oss].

### Function-by-function boundary

Classification: **Existing product capability**, **Configuration**, **Small integration**, **Custom service/code**, **Operational process**. Multiple entries mean a product step needs owned policy/code; they do not turn custom behavior into native capability.

| Function | Classification | Minimum implementation and actual evidence |
| --- | --- | --- |
| Git SQL review | Existing product capability + Configuration | Existing Git MR/PR diff/comments; protect the approved ref. Jenkins's reviewer gate binds authorization to the envelope if the Git host tier cannot enforce the needed deployment approval. **[DOC, DESIGN]** [Catalog](tool-feature-catalog.md), [Input][jenkins-input] |
| Immutable artifact | Existing product capability + Small integration + Operational process | Freeze the exact merged commit's SQL, checks, inventory, target selection and policy. Archive/export once and verify fetched bytes; Git SHA or a mutable workspace alone is insufficient. No download from a mutable branch after approval. **[DOC, DESIGN]** [Archive][jenkins-core] |
| SHA-256 binding | Existing product capability + Custom service/code | Utility SHA-256 functions exist; owned canonical encoding/key/order rules and external approval envelope bind artifact/targets/inventory/policy. Jenkins fingerprints are trace metadata, not the approval SHA-256 contract. **[DOC, DESIGN]** [Utilities][jenkins-utils], [fingerprints][jenkins-fingerprints] |
| Target inventory | Configuration + Small integration | Reviewed Git YAML is the initial source of record; include physical identity, service/PDB, schema, owner, stream/baseline, credential/observer refs and routing revision. Import existing CMDB only if available. **[DESIGN]** [Common contract](reference-architecture.md#4-common-inventory-và-artifact-contract) |
| Target selection | Configuration + Custom service/code | Parameter/Input choice from that snapshot; validate IDs, ownership/environment and canonical target-set hash. Show resolved service/schema before approval; reject raw routing overrides. No editable second inventory. **[DOC, DESIGN]** [Input][jenkins-input] |
| DEV/SIT/UAT/PROD promotion | Existing product capability + Custom service/code | Pipeline stage order plus verified-result checks and approved target list; same bundle through all stages. Previous-stage APPLIED_VERIFIED is necessary, not authority to skip the PROD gate. **[DESIGN]** |
| Reviewer approval | Existing product capability + Configuration + Small integration | Input with restricted submitter(s), captured actor/time and envelope hash persisted before dispatch. Git review alone is not the deployment permission. **[DOC, DESIGN]** [Input][jenkins-input] |
| DBA PROD approval | Existing product capability + Configuration + Small integration | Separate Input for the same envelope/PROD targets and permitted DBA roster; window/expiry rechecked. Lab uses MOCKPROD. Do not allocate a DB session/lock while waiting for human input. **[DOC, DESIGN]** [Input][jenkins-input] |
| Requester != approver | Custom service/code + Operational process | Obtain requester from authenticated human intake (Input) or validated Git event/API readback; store service initiator separately. Check both approver identities against it and their pinned role roster, including admin Input exceptions. **[DOC, DESIGN]** [Input][jenkins-input], [Remote API][jenkins-api] |
| Secret retrieval | Existing product capability + Configuration + Small integration | Integrate the existing enterprise provider or Jenkins credentials if the owner accepts that model. Resolve approved logical refs on a restricted runner; verify target/principal, record secret version reference. Masking alone is not isolation. **[DOC, DESIGN]** [Credentials][jenkins-credentials] |
| Per-schema locking | Existing product capability + Configuration + Custom service/code | Lockable Resources named key for canonical physical DB/service/PDB + schema, shared across all jobs/streams/controllers in scope; durable unresolved-attempt check is separate. Hold active lock through verification. **[DOC, DESIGN]** [Lock plugin][jenkins-lock] |
| Flyway execution | Existing product capability + Configuration + Small integration | Pinned Community CLI/Oracle module/JDBC on approved immutable SQL, one target/schema invocation; scoped deploy user. No automatic retry, clean, repair, baseline or ignored validation errors. **[DOC, DESIGN]** [Oracle][flyway-oracle], [feature tiers][flyway-features] |
| Oracle post-check | Custom service/code + Operational process | DBA/app-defined pre/postconditions; query touched-object state and expected DDL effect, preserving datatype/length semantics. Engine history/exit 0 is not the business postcondition. **[DOC, DESIGN]** [ALL_OBJECTS][oracle-objects], [ALL_ERRORS][oracle-errors] |
| INVALID detection | Custom service/code | Compare touched package/spec/body/view/trigger states and affected dependencies with preflight state; capture diagnostic rows. A successful history row with invalid objects/postcondition failure becomes APPLIED_INVALID and blocks promotion. **[DOC, DESIGN]** [Oracle dictionaries][oracle-objects] |
| Result storage | Existing product capability + Custom service/code + Operational process | Archive durable JSON/logs/checks; additionally persist pre-dispatch admission/attempt state outside workspace/build retention. Backup/export and restore reconciliation required. **[DOC, DESIGN]** [Archive][jenkins-core], [backup][jenkins-backup] |
| Release dashboard | Existing product capability + Small integration | Jenkins job/build/input UI plus escaped static HTML and JSON per release/target; generated inventory/history index if needed. Include failed/HOLD/unknown attempts and evidence links; no new portal. **[DOC, DESIGN]** [HTML Publisher][jenkins-html], [Remote API][jenkins-api] |
| Retry prevention | Custom service/code | Durable request identity and conditional admission, schema HOLD on unresolved attempt. Duplicate same request returns the existing decision; changed hash under the same ID rejects. Do not put Pipeline `retry` around migrate. **[DOC, DESIGN]** [Basic steps][jenkins-basic] |
| UNKNOWN_OUTCOME reconciliation | Custom service/code + Operational process | Read-only tool compares attempt, worker/session, Flyway history and effects. Recover a missing central result without migrate; hold partial DDL/missing history for DBA. **[DESIGN]** [DDL semantics][oracle-ddl], [existing recovery contract](reference-architecture.md#8-auditresult-storage-và-reconciliation) |
| Audit export | Existing product capability + Small integration + Operational process | Export approved bytes, identities/decisions/hashes, engine and verifier records to retained restricted storage; record backup/restore checks. Jenkins administrators can alter local files, so application append-only alone is not tamper-proof archival. **[DOC, DESIGN]** [Archive][jenkins-core], [backup][jenkins-backup] |

### Durable admission is the irreducible custom part

**DESIGN:** use one protected, persistent state location on a stable restricted runner/state host, independent of ephemeral workspace and Jenkins build deletion. A small CLI helper can maintain per-request records and sequenced events using proven exclusive creation/conditional updates, atomic replacement and acknowledged durable writes. Validate the filesystem's actual locking/fsync/restore behavior; do not assume an arbitrary shared/NFS volume provides it. Only the trusted runner can mutate records. If an existing transactional store already meets these needs, use it instead; PostgreSQL is not mandatory.

Admission key is `(release_id, target_id, migration_stream, approval_envelope_hash)`; reject a reused release/request identity with inconsistent input hashes. Attempt IDs are separate. Before any Oracle write, persist a dispatch intent and schema ownership/unresolved-attempt state. A write failure here means **no dispatch**. After execution, persist engine and verification evidence and a conditional terminal event. Duplicate callbacks cannot overwrite a failure/unknown requiring reconciliation. These are owned invariants, not features supplied by `archiveArtifacts`, `stash`, Pipeline durability or Flyway's history lock. **[DESIGN]** Jenkins distinguishes transient stash, archived artifacts and Pipeline persistence: **[DOC]** [Basic steps][jenkins-basic], [Pipeline durability][jenkins-durability].

Lockable Resources handles active job contention, including cross-job named resources. Leave persistent state saving enabled. Map every service/JDBC/target alias for the same physical database/PDB/schema to one reviewed canonical key; target ID, pipeline ID and migration stream are not lock identity. Preflight must verify actual database/container/schema/principal and baseline/history/touched-object state before any write; a mismatch holds the target rather than changing its lock/routing silently. **[DESIGN, NOT_RUN]**

The current plugin also documents remote-lock features; phase 1 deliberately chooses **one controller and one common admission/lock namespace**, and does not rely on untested remote leases. Jenkins abort/restart can release an orchestration lock while an Oracle session continues; the durable unresolved attempt must still hold the schema. Never release it and dispatch again merely because a lease expired. A metadata fencing token does not fence an already running Oracle DDL session. DBA/session evidence is required before recovery clears HOLD. **[DOC, DESIGN, NOT_RUN]** [Plugin][jenkins-lock], [Oracle commits][oracle-ddl].

**UNKNOWN_OUTCOME** after write is not retried. If history and effects prove target success but the result acknowledgement was lost, append a recovered verified result. If DDL exists without successful history, or session/worker outcome is uncertain, hold for DBA recovery. Restoring central state older than the target also freezes dispatch until reconciliation. No normal runner automatically repairs history, baselines an existing schema, restores data, kills sessions or applies compensation. **[DESIGN]** [Repair scope][flyway-repair], [common recovery contract](reference-architecture.md#7-execution-lock-và-failure-contract).

### Phase-1 UI and owned code ceiling

**DESIGN:** the dashboard begins as static, escaped HTML plus structured JSON generated from durable records, published with build/release links. Show inventory snapshot, selected targets, SQL/commit/hash, requester/reviewer/DBA, per-stage/per-target state, attempts and restricted evidence references. Configure HTML Publisher to retain each report and link the latest build even when unsuccessful; never show only the last successful deployment. Render SQL/comments as text, respect Jenkins CSP, and exclude secret values/private raw logs from general views. Archiving failed-run evidence must not depend on `onlyIfSuccessful`.

Owned code is bounded to five modules: **(1)** inventory/envelope validation; **(2)** trusted orchestration/identity/promotion policy; **(3)** durable admission/events; **(4)** Oracle verifier/read-only reconciler; **(5)** report/export generation. They use documented Pipeline/plugin steps, CLI/files and Oracle dictionary queries; no Jenkins JVM plugin, direct edits to Jenkins internal databases, Flyway fork, public application API, queue service or web portal is required. The record format is our interface and needs versioning. Adding an interactive portal, independent executor daemon or multiple deployment controllers is a scope change that reopens the buy/maintain decision. **[DESIGN]**

## 4. CloudDM challenger result

Scope is only the external-executor boundary, at public `ClouGence/open-cdm@3aa1238a471afca2579e76e6fbf0a922d9be5579` / reviewed **v4.3.0**. Artifact/license/feature-cap conclusions remain in the [existing artifact review](research-round-2/coordinator/clouddm-v430-artifact-review-20261007.md); no native test, artifact investigation or broad candidate search was repeated.

| Boundary | Concrete finding | Cleaner than S2? |
| --- | --- | --- |
| Post-approval action | `ChangeActionForApproval.doAction` creates the native approval ticket. `ChangeApprovalHandler.approvalApproved` advances approval state to WAIT_CONFIRM. Confirmation in `ApprovalControlServiceImpl` prepares an AutoExec native job. **[SOURCE]** [Approval action][cloud-approval-action], [handler][cloud-approval-handler], [control][cloud-control] | No supported Flyway dispatch/authorization action established. |
| HTTP action | Official README/FAQ call `HttpCall` a workflow **trigger**, alongside Git Push/Web Hook. `ChangeScheduleServiceImpl` registers INIT/APPROVAL/FINISH/snapshot actions; no configurable post-approval external executor action was established. **[DOC, SOURCE]** [README][cloud-readme], [FAQ][cloud-faq], [scheduler][cloud-schedule] | No; inbound trigger is not post-approval execution. |
| Callback / timing | `ChangeActionForFinish.doAction` finalizes the native change, then `doCallBack` invokes GET or POST to the configured callback URL. It is a finish callback, not an approval-completion authorization hook. **[SOURCE]** [Finish action][cloud-finish] | No; triggering Flyway here would follow native completion. |
| Payload / authentication | POST calls `CallUtils.post(callbackUrl, Collections.emptyMap())`; GET has no execution payload. The reviewed utility supplies no signed envelope or per-request authorization headers. Callback config has flow ID, enabled flag, method, URL. Config management is authenticated; that is different from authenticating outbound deployment input. **[SOURCE]** [HTTP utility][cloud-http], [config DTO][cloud-callback] | No; no release/actor/target/digest receipt contract. URL credentials/static query tokens are not an immutable authorization envelope. |
| Callback configuration endpoint | `DmChangeFlowController`: **`POST /api/entry/cicd/flow/callbackConfig`**, guarded by `@RequestAuth(DM_CICD_FLOW_MANAGE)`, invokes flow callback configuration. **[SOURCE]** [Flow controller][cloud-flow-controller], [URL prefix][cloud-url-prefix] | This configures an outbound native-finish notification, not an external completion API. |
| Exact Git commit | Pinned GitLab guide/source intake use exact commit and documented flow/commit duplicate protection. **[DOC, SOURCE]** [GitLab guide][cloud-gitlab] | Useful intake, but not the missing approval/engine contract. The same guide records plaintext GitLab integration tokens in MetaDB. |
| Immutable approval binding | No full artifact + routing + policy approval hash/readback/claim contract established in the reviewed paths. Current flow configuration remains a dependency. **[SOURCE, UNKNOWN]** [Flow service][cloud-flow-service] | No advantage over ODC; own binder still required. |
| Native executor disablement | The approval confirmation path creates and starts the native AutoExec job. No supported external-only switch was established. A dedicated read-only DB identity could physically block writes, but preview/confirmation/lifecycle under that model is NOT_RUN. **[SOURCE, DESIGN, UNKNOWN]** [Control][cloud-control] | No; at least the same credential boundary and more lifecycle work. |
| Result correlation | Reviewed change controller offers detail/approval/preview/retry/close paths; finish callback does not accept external Flyway evidence or settle an external execution. Cross-links are DESIGN; no supported native completion receipt found in these paths. **[SOURCE, UNKNOWN]** [Change controller][cloud-change-controller] | No supported cleaner result path. |

**Verdict: S3 RED at Gate B; STOP S3.** This is a rejection of the cleaner supported handoff, not proof that every possible polling/link-only adapter or future version is impossible. An unproven generic bridge would add the same owned binding/state controls as S2 and does not justify a challenger POC. Reopen only for a concrete versioned external action API that carries/references immutable approval input, physically disables native execution and correlates external results without executing the same migration twice. Marketing HTTP/callback wording or a deep engine fork does not meet Gate B. No additional CloudDM research is recommended now. **[SOURCE, DESIGN]**

## 5. Bytebase buy boundary

Bytebase EE remains the integrated commercial benchmark, with its own native executor for a selected stream. Do not run the same change through Flyway to add a second ledger. Official pricing currently places the public Community/Pro limits below this approximately 50-instance estate and makes Enterprise a custom commercial offer. The inspected 3.23.0 entitlement source is evidence of feature gates, not a quotation or assurance that a contract has unlimited instances. **[DOC, SOURCE]** [Pricing][bytebase-pricing], [3.23.0 plan at `c8188c6`][bytebase-plan].

Information needed for an actual sales/contract decision, **not sent in this round**:

| Question to settle | Concrete answer required |
| --- | --- |
| Estate / counting | Quote approximately 50 Oracle physical/logical instances and 20 human users. Define how RAC/endpoints, services, PDBs, schemas, duplicate environment registrations and disconnected/observer instances count; inventory the actual estate before buying. |
| Human / service identities | Named/concurrent seat rules, SSO provider support, reviewer/DBA custom roles, service accounts/API/CLI entitlements, service-account seat counting and audit retention of initiating human versus executor. |
| Self-host / Oracle | Exact self-host EE build and support for our actual Oracle versions/editions, connection mode, driver, TCPS/wallet and schema model; update cadence and offline/renewal behavior if relevant. |
| Approval enforcement | Exact custom approval, requester/approver separation, SQL-review blocking, stage-order and task/console permission behavior, including privileged admin exceptions and API paths. |
| Evidence | Retention duration/options, audit/event/task-log exports and formats/APIs, access controls, storage limits, backup/restore behavior and evidence access after subscription expiry. |
| Secrets | Supported enterprise provider(s), rotation/version semantics, deploy versus observer principals, external-secret entitlement and audit; verify the provider actually used by the organization. |
| Commercial terms | Annual total for the real instance/user model, minimum contract/term, implementation/support charges, renewal terms, and any environment or nonproduction exclusions. No invented dollar threshold. |
| Operations / support | Support/SLA terms and response scope; HA replicas, DR/standby/backup restoration, test installations, license-server/outage and HA/DR licensing implications. |

**[UNKNOWN]** These are requested contract facts; the pricing page and plan source do not answer all of them.

The historical FREE Bytebase 3.22.1 runtime on Oracle 26ai recorded INVALID-object success, early MOCKPROD dispatch and SQL-review ERROR execution; improved role restrictions did not resolve every correctness gate. EE behavior was not tested. Preserve those failures as exact-edition regression cases rather than assume payment resolves them. **[RUNTIME, NOT_RUN]** [Bytebase results](../BYTEBASE-ORACLE-POC-RESULTS.md).

**Qualitative buy boundary [DESIGN]:** S6 remains credible while the team can own the five bounded modules, one trusted controller, reviewed inventory and existing secret/evidence infrastructure. Prefer investigating a buy when required UI becomes an interactive migration administration portal, recovery requires a separately operated distributed execution service, multiple controllers introduce cross-domain dispatch state, ODC/Flyway/Jenkins internals must be patched, or no named owner can maintain security/recovery across upgrades. Recurring evidence export, identity/admin governance, on-call recovery and regression effort count toward maintenance burden, even when code is short. Compare the actual EE quote with that owned operating burden; do not automatically buy because a component is HIGH complexity. EE must first pass the same mandatory correctness/authorization gates. Buying a failing edition does not eliminate them.

## 6. Flyway Community Oracle compatibility

**Keep Flyway Community as baseline. No concrete mandatory workload blocker has been supplied.** Current official Oracle documentation, feature tiers and command documentation were checked; the previously collected source pin `a549f5dd1ac80fbe7bc8103dfcd2d556c606c39c` is supporting parser/history evidence, **not** proof of the future 13.9.0 binary. Freeze the actual CLI/Oracle module/JDK/JDBC stack and test the real SQL corpus before adoption. No Flyway or SQL client was executed. **[DOC, SOURCE, UNKNOWN, NOT_RUN]** [Oracle driver reference][flyway-oracle], [OSS distribution][flyway-oss], [existing engine evidence](../EVIDENCE.md).

Each row uses the requested classification. SQL*Plus emulation is licensed capability, while irreducible native-client commands are a different category; neither is inferred from ordinary PL/SQL.

For sequences and materialized views, Community OK is an **inference from documented ordinary Oracle SQL/JDBC migration support**, not a separately verified object-management feature or runtime certification of the estate. Required privileges, dependencies and effects remain workload acceptance checks. **[DOC, DESIGN, NOT_RUN]** [Oracle reference][flyway-oracle].

| Oracle requirement | Classification | Verified scope / limitation and required proof |
| --- | --- | --- |
| PL/SQL anonymous blocks | **Community OK** | Oracle parser accepts PL/SQL with the documented slash-on-separate-line block delimiter. Check the actual scripts and driver warnings. **[DOC, SOURCE]** [Oracle reference][flyway-oracle], [pinned parser][flyway-parser] |
| Package / package body | **Community OK** | Ordinary Oracle SQL migrations can create package/spec/body; parser handles these statements. Validity and diagnostics must be checked separately for both object types. **[DOC, SOURCE, DESIGN]** [Parser][flyway-parser], [ALL_OBJECTS][oracle-objects] |
| Procedures / functions | **Community OK** | Ordinary PL/SQL migrations supported; JDBC success does not guarantee VALID compilation or application semantics. **[DOC, DESIGN]** [Oracle reference][flyway-oracle] |
| Triggers | **Community OK** | Ordinary CREATE TRIGGER SQL/PLSQL; test compilation and enabled/expected behavior with suitable privileges. **[DOC, DESIGN]** [Oracle reference][flyway-oracle] |
| Sequences | **Community OK** | Ordinary Oracle SQL over JDBC; verify approved properties and grants. This is a SQL migration inference, not a sequence-management feature. **[DOC, DESIGN]** [Oracle SQL support][flyway-oracle] |
| Views | **Community OK** | Ordinary CREATE/REPLACE VIEW SQL; verify object status and expected definition/query behavior. **[DOC, DESIGN]** [Oracle reference][flyway-oracle] |
| Materialized views | **Community OK** | Ordinary Oracle DDL through SQL migration; refresh/job/tablespace/grant semantics are workload-specific and not certified by a history row. **[DOC, DESIGN, NOT_RUN]** [Oracle SQL support][flyway-oracle] |
| SQL*Plus directives that can be removed/transformed | **Requires adaptation** | Inventory `SET`, `SPOOL`, `PROMPT`, `WHENEVER`, `@/@@`, etc. Strip only nonsemantic directives or replace with reviewed runner settings/bundled files; reject unknown directives before approval. Community JDBC SQL is not a complete SQL*Plus client. **[DOC, DESIGN]** [Oracle SQL*Plus limits][flyway-oracle] |
| Flyway SQL*Plus-compatible mode | **Requires paid Flyway capability** | `oracle.sqlplus=true` is a Teams capability, default false, with documented emulation limits. Even that mode may warn/ignore unsupported commands; payment is not complete SQL*Plus equivalence. **[DOC]** [SQL*Plus setting][flyway-sqlplus] |
| SQL*Plus `&` / `&&` substitution variables | **Requires adaptation** | Convert reviewed nonsecret values to supported placeholders or pre-render a frozen approved script; bind the effective values/bytes. Do not assume `${...}` placeholders implement SQL*Plus session semantics. **[DOC, DESIGN]** [Placeholder replacement][flyway-placeholders], [Oracle reference][flyway-oracle] |
| Irreducible SQL*Plus / SQLcl client directives | **Requires SQLcl/SQL*Plus** | Commands needing genuine client behavior require that client if adaptation or licensed emulation cannot preserve semantics. No such required corpus is evidenced yet. Community currently documents script migrations; a deliberate native-client wrapper would still need pinned client, return-code/history/partial-DDL proof. Do not silently add a second migration executor. **[DOC, UNKNOWN, DESIGN]** [Feature summary][flyway-features], [Oracle reference][flyway-oracle] |
| Repeatable migrations | **Community OK** | Run when checksum changes, after pending versioned migrations; use reviewed re-runnable definitions such as CREATE OR REPLACE and verify spec/body ordering/dependencies. Avoid forced timestamp-based reruns in an uncertain attempt. **[DOC, DESIGN]** [Repeatables][flyway-repeatable] |
| Basic SQL command callbacks | **Community OK** | Community has limited SQL callback support. Keep safety postchecks in the external verifier so admission/correctness do not depend on a paid or unverified callback event. **[DOC, DESIGN]** [Callbacks][flyway-callbacks], [tiers][flyway-features] |
| Every desired callback event / API hook | **UNKNOWN** | The tier summary says callbacks are limited; accept a specific event only after verifying it in the pinned Community binary. Do not assume all events listed across tiers are available. **[DOC, UNKNOWN, NOT_RUN]** [Callback events][flyway-callback-events] |
| Checksum validation / `validate` | **Community OK** | SQL migration checksums detect engine-history/script mismatch; CRC32 is not approval SHA-256, Oracle drift detection or object validity. Fail on mismatch; no automatic repair to admit changed bytes. **[DOC, DESIGN]** [Validate][flyway-validate] |
| `repair` | **Community OK** | Repairs history metadata, including failed entries/checksum realignment; it does not undo committed user-object DDL. Only a separately approved DBA recovery decision may invoke it. **[DOC, DESIGN]** [Repair][flyway-repair] |
| `baseline` | **Community OK** | Explicitly marks an existing database baseline; it does not inspect/establish expected schema semantics. Existing-object/history reconcile is required; no automatic `baselineOnMigrate` guess. **[DOC, DESIGN]** [Baseline][flyway-baseline] |
| Multiple schemas | **Community OK** | `schemas`/default-schema configuration exists; a schema list does not fan out independent target ledgers. Use one approved target/schema per invocation/history, and lock all schemas explicitly if an approved script crosses them. **[DOC, DESIGN]** [Schemas][flyway-schemas] |
| JDBC Oracle driver compatibility for our estate | **UNKNOWN** | Oracle module/driver support is documented, including `ojdbc11`; actual Oracle release, JDK, module, driver, connection/TCPS/wallet and grants are not supplied. Oracle documentation distinguishes listed supported versions from verified versions, and the general support matrix is not identical to the Oracle page. Verify the exact stack rather than infer all older releases or every current combination. **[DOC, UNKNOWN, NOT_RUN]** [Oracle driver page][flyway-oracle], [version matrix][flyway-versions], [Oracle JDBC][oracle-jdbc] |

Community does not supply automatic rollback of Oracle DDL. Oracle DDL commits and Flyway history/recovery are separate concerns; neither a paid Undo feature nor `repair` turns a partially committed script into an atomic transaction. The existing [engine source review](../EVIDENCE.md) and [Oracle commits documentation][oracle-ddl] remain the basis for HOLD/reconciliation. **[DOC, SOURCE, DESIGN]**

**Falsifier:** a mandatory production script that cannot be adapted without changing approved semantics and needs an unavailable paid/native-client feature, or an unsupported mandatory Oracle/JDK/driver combination, reopens the engine/edition choice. Until that evidence exists, ordinary packages/triggers/views and compile checks do **not** justify switching engines. Exact workload compatibility is **NOT_RUN**.

## 7. Custom engineering comparison

Complexity is a relative engineering/risk estimate, **DESIGN**, not measured effort: **LOW** = ordinary settings/glue; **MEDIUM** = bounded versioned module; **HIGH** = identity/concurrency/recovery invariants needing failure tests; **VERY HIGH** = upstream patch/fork or distributed product lifecycle. No person-days are inferred. Owners below are proposed responsibilities and must be confirmed.

### S6: supported interfaces with owned policy/state code

| Component | Native/config/custom | Estimated complexity | Upgrade coupling | Security criticality | Owner |
| --- | --- | --- | --- | --- | --- |
| Git review / reviewed inventory | Native + configuration | LOW | Git/config format; no product internals | MEDIUM: incorrect route/ownership | App owner + DBA; DevOps format |
| Bundle / canonical envelope / target selection | Small integration + custom code | MEDIUM | Our schema/version; documented SHA/file steps | HIGH: approved bytes/routing | DevOps; DBA policy review |
| Trusted job/library / stage promotion | Native Pipeline + custom policy | MEDIUM | Documented steps/CLI; pin library/plugins | HIGH: controls write authority | DevOps; platform security |
| Human gates / SoD / roster readback | Native Input + custom identity checks | HIGH | Auth realm/IDs and documented Input semantics | HIGH: admin exception/requester attribution | Identity/security owner + DevOps |
| Secrets / restricted runner | Configuration + provider integration | MEDIUM | Provider API, credential plugin, image/JDBC | HIGH: deploy secret/code execution | DevOps + security + DBA |
| Active target locks | Native plugin + canonical-key configuration | MEDIUM | Supported lock step; pin plugin/persistence | HIGH: cross-job/schema collision | DevOps; DBA identity mapping |
| Durable admission / attempts / no replay | Custom code, no new daemon | HIGH | Owned record format + tested storage primitives | HIGH: duplicate/uncertain writes | DevOps; DBA recovery review |
| Flyway CLI invocation / history | Native engine + wrapper configuration | MEDIUM | Pinned CLI/module/driver; no Flyway fork | HIGH: credentials/DDL | DevOps package owner + DBA |
| Oracle validity / effect verifier | Custom code + defined operational checks | HIGH | Stable Oracle dictionaries; version-specific SQL | HIGH: false verification/promotion | DBA + app semantic owner |
| Read-only reconciler / DBA recovery | Custom code + operational process | HIGH | Owned state + engine info/history + Oracle reads | HIGH: deciding whether another write is safe | DBA recovery owner + DevOps |
| Durable export / backups | Native archive + integration/process | MEDIUM | Storage API/ACL/retention, restore procedures | HIGH: loss of unresolved attempts/evidence | DevOps + audit owner |
| HTML/JSON inventory/release/history view | Native publisher + report generator | MEDIUM | Supported publish step; owned report schema | MEDIUM: content injection/stale success | DevOps; DBA usability review |

The HIGH controls are mandatory; deleting their code because a plugin exists does not simplify the requirement. Supported interfaces reduce upgrade coupling, not the need to own policy/security. **[DESIGN]**

### S2: S6 execution controls plus a second workflow authority

| Component | Native/config/custom | Estimated complexity | Upgrade coupling | Security criticality | Owner |
| --- | --- | --- | --- | --- | --- |
| ODC server / MetaDB / inventory-policy config | Native product + configuration/operations | MEDIUM | Additional server, compatible MetaDB and upgrade/backup cycle | HIGH: approval authority/credential config | DevOps + DBA |
| CI ticket creation / SQL preview adapter | Custom integration to reviewed REST DTOs | MEDIUM | Internal/UI REST; supported contract UNKNOWN | HIGH: correct SQL/target/human identity | DevOps; ODC contract owner |
| Approval-node readback / human attribution | Custom code | HIGH | Response/operator/status/auth semantics per build | HIGH: false approval/SoD | DevOps + identity/security |
| Envelope freeze / mutation detection / claim cutoff | Custom code | HIGH | Owned envelope plus ODC reference/readback behavior | HIGH: time-of-check/routing mutation | DevOps + DBA policy owner |
| Notification hint / polling | Native notification + trusted-library integration | MEDIUM | Event labels/templates or poll API; no required daemon | MEDIUM: duplicate/lost hints; cannot authorize alone | DevOps |
| Prevent all ODC Oracle writes | DB-grant configuration + negative-test process | HIGH | Every datasource/native path and admin boundary | HIGH: second writer | DBA + security; DevOps credentials |
| Flyway runner / secret / locks / durable admission | Same owned S6 modules | HIGH | Same as S6; ODC does not replace them | HIGH: execution/replay | DevOps + DBA |
| Oracle verifier / reconciliation | Same owned S6 modules | HIGH | Same engine/Oracle state plus ODC lifecycle reconciliation | HIGH: partial/unknown outcome | DBA + DevOps |
| Result URL / correlation / expiry UI | Small integration + custom report/index | MEDIUM | Description/detail/expiry/retention across both systems | MEDIUM: confusing native versus external status | DevOps + DBA UX owner |
| Native completion or external task-engine fork, if demanded | Upstream internal patch/fork; **excluded** | VERY HIGH | Flowable/task mapper/status/log/permission internals | HIGH: authorization and false SUCCESS | No owner assigned; STOP that variant |

The limited S2 bridge is ownable in principle, but does not eliminate any hard execution/recovery control. Its extra costs are authority readback, service/human identity mapping, physically blocking every native writer, ticket expiry and double-system correlation. There is no demonstrated reduction in the HIGH parts relative to S6. Upstream forks receive a much larger penalty than owned code using documented Pipeline/CLI APIs. **[SOURCE, DESIGN]**

## 8. Architecture simplification

Each removal is judged against a hard requirement. All choices here are **DESIGN**, not running configuration.

| Proposed component / removal | Which hard requirement fails if simply removed? | Minimum decision |
| --- | --- | --- |
| ODC on top of Jenkins | None for S6's specified request/review/approval/results once authenticated Jenkins gates and reports exist | Remove in phase 1; additional governance UI must justify a second authority later. |
| Dedicated adapter daemon / webhook service | No requirement fails if known requests are polled/processed by the trusted deployment job | Remove. Use a shared library plus runner CLI; S2 would only need a daemon if a later latency/scale requirement proves polling insufficient. |
| PostgreSQL result service | No requirement inherently requires that database | Remove by default. Durable protected records plus export/index can suffice on one owner host; reuse an existing transactional store only if filesystem/state proof fails or queries/concurrency demand it. |
| Jenkins build metadata + end-of-run JSON as the only state | Durable pre-write admission, duplicate prevention and HOLD after abort/deletion fail | Keep build metadata for UI; **add durable pre-dispatch records** independent of workspaces and build retention. JSON format is acceptable; transient placement is not. |
| New web dashboard / migration portal | No phase-1 requirement needs an interactive portal | Remove. Publish escaped inventory/selection/release/history HTML/JSON linked from Jenkins; accept its read-only usability limit before POC. |
| New secret manager / OpenBao deployment | No need if existing enterprise provider or approved Jenkins credentials meet the actual policy | Integrate the existing owner/provider first. If neither meets policy, resolve the secret requirement explicitly before Oracle POC; do not silently invent infrastructure. |
| New object store | Durable artifact/evidence needs storage, but not a particular new product | Reuse retained storage with appropriate ACL, hashes and backups. Jenkins-only short retention is insufficient. |
| Canonical target registry / envelope binder | Allowed-target routing and approval-to-bytes binding fail | Keep; reviewed Git YAML and one versioned module suffice. No second editable catalog. |
| Shared schema lock / durable unresolved-attempt guard | Conflicting writers or replay after unknown outcome become possible | Keep both. Job-local serialization/history lock alone cannot meet the scope. |
| Oracle verifier / reconciliation | INVALID detection, promotion correctness and safe recovery fail | Keep; use CLI checks and a read-only tool, not an autonomous recovery service. |
| Multiple controllers, HA and 50-way fanout | No initial POC requirement needs them | Defer. Single controller, persistent state owner, serial target dispatch; validate restore and failure recovery first. |

**Resulting minimum shape:** existing Git + Jenkins/controller storage + one restricted runner/state host + existing secrets/evidence storage + approved Oracle targets. Owned scripts/libraries provide the five modules in section 3. There is no separate product database or application frontend by default. Centralized selection/history is still required and visible; simplification does not mean returning to developers running Flyway manually against arbitrary databases.

## 9. Remaining unknowns

| Unknown / unrun proof | Decision impact | Owner / concrete closure |
| --- | --- | --- |
| Actual Oracle versions/editions, service/PDB/physical identities, schema/stream count and baseline | Can invalidate driver assumptions, routing/lock aliases and inventory estimate | DBA: reviewed target sample/estate mapping; exact stack and corpus tests in POC #2. **[UNKNOWN, NOT_RUN]** |
| Existing Git/Jenkins, auth realm, identity roster, secret provider, retained storage and compatible plugins | Determines reusable infrastructure and authenticated human intake | DevOps + identity/audit owners: confirm existing interfaces, policies, backup/retention and exact package/digest pins before POC setup. **[UNKNOWN]** |
| Durable state atomicity, filesystem persistence, job abort/controller restart and restore behavior | S6 cannot safely dispatch if intent/attempt records are not durable | DevOps: POC #1 crash/duplicate/negative tests; Oracle-session continuation and stale metadata recovery in POC #2. **[NOT_RUN]** |
| Read-only DBA metadata visibility and application-specific postconditions | False success or overprivileged verifier | DBA + app owner: touched/dependent object baseline, expected DDL semantics, least-privilege query tests. **[UNKNOWN, NOT_RUN]** |
| Supported ODC build/API/auth plus source-to-image mapping | Gate A remains unclosed, no S2 implementation now | Reopen only with exact supported contract and owner, then negative tests; not another broad source hunt. **[UNKNOWN]** |
| ODC immutable readback/claim/revocation, service versus human creator, required-node actors and link/expiry lifecycle | Current link-only bridge remains YELLOW DESIGN | Demonstrate the six Gate A proofs on that build before allocating an S2 implementation POC. **[UNKNOWN, NOT_RUN]** |
| Concrete cleaner CloudDM contract | S3 stopped | Reopen only for a supplied supported external-action delta; no more general CloudDM review. **[UNKNOWN]** |
| Bytebase quote, instance/seat semantics, exact EE entitlement/build and regression | Buy decision cannot be made | Authorized commercial inquiry later; regression only after package/edition access is agreed. **[UNKNOWN, NOT_RUN]** |
| Owners, window, retention, recovery and privileged exceptions | Missing operations ownership blocks adoption even if POC works | DBA/DevOps/security/audit owners confirm their policies. No SLA, RTO or retention duration invented here. **[UNKNOWN]** |

The following primary references were used only for these boundaries. Pinned source conclusions are limited to the linked commit/path; mutable official documentation was checked on 07 October 2026 and must be rechecked when selecting actual packages. Historical runtime links above retain their original image/Oracle/role scope. Reference definitions below supply the URL for each inline citation.

[odc-main]: https://github.com/oceanbase/odc/tree/d517c0f27971642fb0cd7565fd61ab2309875ec3
[odc-450]: https://www.oceanbase.com/docs/common-odc-1000000006663615
[odc-controller]: https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-server/src/main/java/com/oceanbase/odc/server/web/controller/v2/FlowInstanceController.java
[odc-create]: https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/model/CreateFlowInstanceReq.java
[odc-parameters]: https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/task/model/DatabaseChangeParameters.java
[odc-service]: https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/FlowInstanceService.java
[odc-detail]: https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/model/FlowInstanceDetailResp.java
[odc-node]: https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/model/FlowNodeInstanceDetailResp.java
[odc-approval]: https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/instance/FlowApprovalInstance.java
[odc-task-service]: https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/FlowTaskInstanceService.java
[odc-permissions]: https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/FlowPermissionHelper.java
[odc-pending]: https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/listener/ServiceTaskPendingListener.java
[odc-properties]: https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/task/model/FlowTaskProperties.java
[odc-event]: https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/notification/model/TaskEvent.java
[odc-event-builder]: https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/notification/helper/EventBuilder.java
[odc-http]: https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/notification/HttpSender.java
[odc-webhook]: https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/notification/model/WebhookChannelConfig.java
[odc-mapper]: https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/flow/task/mapper/OdcRuntimeDelegateMapper.java
[odc-auth-wiring]: https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/iam/auth/UsernamePasswordConfigureHelper.java
[odc-login-filter]: https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/iam/auth/CustomUsernamePasswordAuthenticationFilter.java
[odc-security-properties]: https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/config/CommonSecurityProperties.java
[odc-auth-facade]: https://github.com/oceanbase/odc/blob/d517c0f27971642fb0cd7565fd61ab2309875ec3/server/odc-service/src/main/java/com/oceanbase/odc/service/iam/auth/DefaultAuthenticationFacade.java
[odc-approval-doc]: https://github.com/oceanbase/odc-doc/blob/40dc7c03522fef1968bd11b2b051bc216091e60d/en-US/1000.system-integration/200.approval-integration.md
[odc-channel-doc]: https://en.oceanbase.com/docs/common-odc-10000000003043326
[jenkins-input]: https://www.jenkins.io/doc/pipeline/steps/pipeline-input-step/
[jenkins-library]: https://www.jenkins.io/doc/book/pipeline/shared-libraries/
[jenkins-security]: https://www.jenkins.io/doc/book/security/securing-builds/
[jenkins-credentials]: https://www.jenkins.io/doc/book/using/using-credentials/
[jenkins-core]: https://www.jenkins.io/doc/pipeline/steps/core/
[jenkins-utils]: https://www.jenkins.io/doc/pipeline/steps/pipeline-utility-steps/
[jenkins-fingerprints]: https://www.jenkins.io/doc/book/using/fingerprints/
[jenkins-api]: https://www.jenkins.io/doc/book/using/remote-access-api/
[jenkins-basic]: https://www.jenkins.io/doc/pipeline/steps/workflow-basic-steps/
[jenkins-lock]: https://plugins.jenkins.io/lockable-resources/
[jenkins-html]: https://plugins.jenkins.io/htmlpublisher/
[jenkins-backup]: https://www.jenkins.io/doc/book/system-administration/backing-up/
[jenkins-durability]: https://www.jenkins.io/doc/book/pipeline/scaling-pipeline/
[cloud-readme]: https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/docs/README.en.md
[cloud-faq]: https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/docs/reference/faq.en.md
[cloud-gitlab]: https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/docs/guides/gitlab-cicd.en.md
[cloud-approval-action]: https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/backend/clouddm-platform/cgdm-console/src/main/java/com/clougence/clouddm/console/web/component/cicd/action/ChangeActionForApproval.java
[cloud-approval-handler]: https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/backend/clouddm-platform/cgdm-console/src/main/java/com/clougence/clouddm/console/web/component/approval/handler/ChangeApprovalHandler.java
[cloud-control]: https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/backend/clouddm-platform/cgdm-console/src/main/java/com/clougence/clouddm/console/web/service/approval/ApprovalControlServiceImpl.java
[cloud-schedule]: https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/backend/clouddm-platform/cgdm-console/src/main/java/com/clougence/clouddm/console/web/component/cicd/impl/ChangeScheduleServiceImpl.java
[cloud-finish]: https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/backend/clouddm-platform/cgdm-console/src/main/java/com/clougence/clouddm/console/web/component/cicd/action/ChangeActionForFinish.java
[cloud-http]: https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/backend/clouddm-platform/cgdm-console/src/main/java/com/clougence/clouddm/console/web/util/CallUtils.java
[cloud-callback]: https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/backend/clouddm-platform/cgdm-console/src/main/java/com/clougence/clouddm/console/web/model/fo/cicd/ChangeFlowCallbackFO.java
[cloud-flow-service]: https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/backend/clouddm-platform/cgdm-console/src/main/java/com/clougence/clouddm/console/web/service/cicd/DmChangeFlowServiceImpl.java
[cloud-change-controller]: https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/backend/clouddm-platform/cgdm-console/src/main/java/com/clougence/clouddm/console/web/controller/cicd/DmChangeController.java
[cloud-flow-controller]: https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/backend/clouddm-platform/cgdm-console/src/main/java/com/clougence/clouddm/console/web/controller/cicd/DmChangeFlowController.java
[cloud-url-prefix]: https://github.com/ClouGence/open-cdm/blob/3aa1238a471afca2579e76e6fbf0a922d9be5579/backend/clouddm-platform/cgdm-console/src/main/java/com/clougence/clouddm/console/web/constants/DmControllerUrlPrefix.java
[bytebase-pricing]: https://www.bytebase.com/pricing/
[bytebase-plan]: https://github.com/bytebase/bytebase/blob/c8188c635465321ff930c97200742a96ef653144/backend/enterprise/plan.yaml
[flyway-oracle]: https://documentation.red-gate.com/flyway/reference/database-driver-reference/oracle-database
[flyway-oss]: https://documentation.red-gate.com/flyway/reference/usage/flyway-open-source
[flyway-features]: https://documentation.red-gate.com/flyway/learn-more-about-flyway/feature-summary
[flyway-parser]: https://github.com/flyway/flyway/blob/a549f5dd1ac80fbe7bc8103dfcd2d556c606c39c/flyway-database/flyway-database-oracle/src/main/java/org/flywaydb/database/oracle/OracleParser.java
[flyway-sqlplus]: https://documentation.red-gate.com/flyway/reference/configuration/flyway-namespace/flyway-oracle-namespace/flyway-oracle-sqlplus-setting
[flyway-placeholders]: https://documentation.red-gate.com/flyway/reference/configuration/flyway-namespace/flyway-placeholder-replacement-setting
[flyway-repeatable]: https://documentation.red-gate.com/flyway/flyway-concepts/migrations/repeatable-migrations
[flyway-callbacks]: https://documentation.red-gate.com/flyway/flyway-concepts/callbacks
[flyway-callback-events]: https://documentation.red-gate.com/flyway/reference/callback-events
[flyway-validate]: https://documentation.red-gate.com/flyway/reference/commands/validate
[flyway-repair]: https://documentation.red-gate.com/flyway/reference/commands/repair
[flyway-baseline]: https://documentation.red-gate.com/flyway/reference/commands/baseline
[flyway-schemas]: https://documentation.red-gate.com/flyway/reference/configuration/environments-namespace/environment-schemas-setting
[flyway-versions]: https://documentation.red-gate.com/flyway/getting-started-with-flyway/system-requirements/supported-databases-and-versions
[oracle-objects]: https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/ALL_OBJECTS.html
[oracle-errors]: https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/ALL_ERRORS.html
[oracle-jdbc]: https://docs.oracle.com/en/database/oracle/oracle-database/19/jjdbc/JDBC-getting-started.html
[oracle-ddl]: https://docs.oracle.com/en/database/oracle/oracle-database/19/tdddg/committing-transactions.html

## 10. Final decision gates

### Gate A — ODC: unclosed, STOP S2 this phase

Proceed with a reopened **link-only** S2 only when all six proofs exist on one exact supported build:

1. **Immutable input recoverable:** approved SQL/files/options, targets/routing, inventory and policy match a frozen canonical envelope; missing content and mutation fail closed.
2. **External authorization safe:** supported authenticated readback, all required approval nodes, expiry/cancellation/admission cutoff and durable duplicate handling; no execution from notification alone.
3. **Native execution prevented:** every managed ODC connection has a physically non-writing Oracle principal; button/API/native async/console/alternate task and credential-edit negatives prove it, not merely UI hiding.
4. **Identity trustworthy:** initiating human, service creator, authenticated reviewers/DBAs, timestamps and role/SoD proof are distinct and recoverable without trusting client text.
5. **Result correlated:** stable specific release/evidence URL plus ticket/task IDs survives failure, expiry and retention; native pending status is explicitly distinguished from external results.
6. **No deep fork:** supported CI auth/API and bridge ownership confirmed; no Flowable/task/status patches required.

**Current evidence:** source supports request/detail/notification/MANUAL building blocks; the immutable, authenticated, physically blocked and lifecycle proofs remain DESIGN/UNKNOWN/NOT_RUN. Thus Gate A is not passed. **STOP S2 now**. YELLOW describes the limited technical possibility; it is not permission to implement before closing the gate. Native external SUCCESS or engine replacement via internals is an excluded RED variant.

### Gate B — CloudDM: failed, STOP S3

Proceed only with a documented versioned post-approval external action/receipt contract that is **materially cleaner than ODC**, binds the exact approval input, prevents native execution and correlates external state. Inbound HttpCall and an empty native-finish callback do not meet it. Reviewed v4.3.0 provides no such cleaner contract. **STOP S3; no further research without a concrete supported delta. [DOC, SOURCE]**

### Gate C — Jenkins: feasibility passed, POC/adoption proofs outstanding

**Proceed to the bounded POC** because the proposed controls use supported Jenkins steps/plugins, Flyway CLI and Oracle reads, no phase-1 migration portal, and the five explicitly bounded owned modules. **[DOC, DESIGN]**

Before allowing Oracle writes, POC #1 must prove exact-envelope approval/identity, fail-closed input/state admission, duplicate prevention, cross-job canonical locking/HOLD and durable results. Before adoption, POC #2 must prove actual Oracle parsing/version compatibility, INVALID/postconditions, partial DDL and unknown-outcome recovery, lower-stage promotion and backup/restore reconciliation. All are **NOT_RUN**. If durable admission or reliable human/role identity requires a product fork, if mandatory UI needs a new portal, or if the owned modules expand into a distributed platform, Gate C fails and the commercial comparison is reopened. Lack of acceptable secret/storage/operations ownership also blocks writes/adoption.

### Gate D — Bytebase: HOLD commercial decision

Retain EE until the **actual quote/counting/entitlement/support terms** in section 5 and **exact licensed edition regression** are available. No purchase or price rejection is justified by current evidence. EE adoption still requires INVALID-object rejection, SQL-review/SoD/API/console enforcement, ordered promotion, immutable artifact correlation and acceptable recovery/export. **[UNKNOWN, NOT_RUN]** Keep the historical FREE failures unchanged.

## 11. Recommended POC order

### POC #1 — S6 no-Oracle contract and centralized UX

Implement only in a future explicitly authorized implementation task. Use a representative **50-instance inventory fixture**, including multiple schemas/services and aliases, plus role fixtures for the approximately 20-user workflow. Simulation is not 50 real connected instances, certified seats, real SSO, or Oracle execution. Freeze exact target/artifact/policy bytes and show selection, SQL/hash, reviewer/DBA gates and release/history report. Use authenticated real test actors where available for Input/SoD; synthetic actors exercise policy code but cannot count as identity proof. **[DESIGN, NOT_RUN]**

Pass criteria: changed SQL/targets/route/policy or unauthorized/self-approval dispatches nothing; duplicate/replayed request returns its recorded decision; cross-job same-schema contention shares a key; failed durable write creates no dispatch; restart/abort retains unresolved HOLD; failed/unknown states appear in retained evidence/report; untrusted requester code cannot select secret/routing/executable overrides. Include staged failure simulation and malicious HTML/SQL-comment text. Simulation statuses remain `SIMULATED_*`; never write APPLIED_VERIFIED or Oracle ledger evidence. A failure of durable/identity/lock controls means **no Oracle POC** until resolved within the module ceiling. This refines, without editing, the existing [POC plan](poc-plan.md).

### POC #2 — S6 isolated Oracle correctness and recovery

Only after POC #1 and explicit isolated-target authorization. Use DEV/SIT/UAT/**MOCKPROD**, actual owner-approved version/driver/schema mapping and the existing [45-case acceptance contract](../poc/ORACLE-POC.md); existing cases/results stay historical and any new run is separate. Do not claim four-instance isolation when the lab uses four users on one service. **[DESIGN, NOT_RUN]**

Pass criteria: normal DDL and representative PL/SQL compile/effect checks; intentionally INVALID package/body/trigger blocks promotion despite history/exit success; checksum drift rejects before migration; partial DDL is HOLD without retry/repair; worker/controller interruption and lost result acknowledgement are reconciled from history/effects without re-execution; live/stale Oracle session cannot be bypassed by lock expiry; restored metadata behind the target freezes dispatch; new target/envelope or premature MOCKPROD cannot reuse prior approval. Capture every dispatched target's outcome, including in-flight work after stop-on-error. Single-target proof must precede serial multi-target deployment; measured owner-approved concurrency comes later.

Stop S6 adoption if these invariants cannot be met without a fork/distributed product. Bytebase EE becomes the next **conditional integrated regression**, after a suitable actual quote and licensed package access; it is not a parallel FREE trial or an already authorized deployment. No S2/S3 POC is scheduled merely to preserve the old shortlist order. **[DESIGN]**

| Solution | Verdict | Why | Next action |
| --- | --- | --- | --- |
| Bytebase EE | **HOLD** | Commercial/edition facts and historical-failure regressions unresolved | Obtain actual quote/entitlements, then decide whether to authorize EE regression. |
| ODC + Flyway (S2) | **YELLOW** | Limited link-only bridge possible; supported immutable authority/auth/lifecycle proofs absent, extra control plane | **STOP this phase**; reopen only with all Gate A proofs and owner value case. |
| CloudDM + Flyway (S3) | **RED** | Inbound HttpCall/empty native-finish callback is not a cleaner approved external-engine contract | **STOP**; require concrete supported contract delta to reopen. |
| Jenkins + Flyway (S6) | **GREEN — feasibility only** | Documented control interfaces and five bounded modules; no new portal needed | Run no-Oracle POC, then isolated Oracle correctness/recovery if its gates pass. |

**POC #1 = S6 no-Oracle approval/envelope/durable-state/UI proof.**

**POC #2 = S6 isolated Oracle correctness, promotion and recovery proof, conditional on POC #1.**

**STOP = S2 this phase (Gate A unclosed); S3 (Gate B failed); all upstream execution/status forks.**

**COMMERCIAL CHECK = Bytebase EE actual 50-instance/20-user self-host quote, counting/entitlements and support; exact-edition regression before any buy/adoption decision.**
