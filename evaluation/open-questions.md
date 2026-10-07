# Decision questions: public closure and remaining inputs

Updated **7 October 2026** in the decision-closing round. Original question IDs are preserved; every question below now has an explicit disposition. [Final decision](final-decision.md) supplies the branch recommendation. The [baseline](current-baseline.md) owns requirements/status/next decision. Owners below are roles to identify, not assigned personnel. Close questions with dated sanitized evidence or explicit owner decisions; keep prior uncertainty in history.

Approximately 50 instances/20 users and DBeaver/manual execution are user-reported. Internal versions/providers/policies require owner input; public product facts are closed separately below. The Oracle 26ai lab and catalog releases do not answer them. This register authorizes no live inventory, credential access, SQL, vendor contact or trial.


## Dispositions and closed public facts

`RESOLVED_PUBLICLY` means current DOC/SOURCE answers the scoped question, including absence of an established supported capability. It does not mean runtime PASS. `INTERNAL_INPUT_REQUIRED` requires estate records or policy; `COMMERCIAL_INPUT_REQUIRED` requires actual quote/contract/private access; `RUNTIME_REQUIRED` requires a separately authorized exact-build test. `NO_LONGER_RELEVANT` means unnecessary for the current branch choice, with later adoption work explicitly deferred.

| Public question | Disposition | Answer / evidence |
| --- | --- | --- |
| ODC current release/source and bounded safety delta | RESOLVED_PUBLICLY | Vendor docs list V4.5.0/V4.4.3; public HEAD remains the reviewed d517c0f pin and GitHub latest release is v4.3.4_bp2. No qualifying supported closure within two additions is established. **ODC remains HOLD**. [Delta review](decision-closing/odc-public-delta.md). |
| AccessFlow supported handoff/current release | RESOLVED_PUBLICLY | Current main is c8bb247; latest release v2.7.0 is older. Submit/gate/confirm/outcome endpoints are supported. [Contract review](decision-closing/accessflow-public-contract.md). |
| AccessFlow artifact/target binding and exclusive claim | RESOLVED_PUBLICLY | Optional references/metadata do not bind bytes/targets. Run-tuple idempotency/optimistic status locking do not supply Oracle release admission; repeated EXECUTED confirmation can succeed. [Contract review](decision-closing/accessflow-public-contract.md). |
| AccessFlow identities/approval/per-target state/promotion | RESOLVED_PUBLICLY | API-key owner, human attribution and self-approval controls exist; outcomes are caller-reported. No per-target PARTIAL/UNKNOWN or Oracle verified-promotion contract. [Contract review](decision-closing/accessflow-public-contract.md). |
| AccessFlow smaller than existing CI | RESOLVED_PUBLICLY | No demonstrated reduction of five safety responsibilities. Existing operated components can change marginal operations burden; a short runner does not eliminate correctness ownership. [Final comparison](final-decision.md#5-accessflow-final-research-status). |
| Bytebase plan boundaries/limits | RESOLVED_PUBLICLY | Community 20 users/10 instances; Pro custom users/10 instances; Enterprise custom contracted counts, approval and external secrets. Audit unavailable/7-day/unlimited advertised; HA add-on. [Pricing](https://www.bytebase.com/pricing/), [public review](decision-closing/bytebase-public.md). |
| Bytebase self-host/Oracle/API/rollout | RESOLVED_PUBLICLY | Public supported architecture, connector, service accounts and release/plan/rollout interfaces are documented. Post-execution verifier/promotion acceptance is separate. [Public review](decision-closing/bytebase-public.md). |
| Bytebase published counting terminology | RESOLVED_PUBLICLY | Users/database instances are published units; instance/database/schema terms are documented. Exact RAC/PDB/alias/service-account billing belongs to C2. [Public review](decision-closing/bytebase-public.md). |
| Bytebase release and post-FREE Oracle changes | RESOLVED_PUBLICLY | 3.23.0 is c8188c635465321ff930c97200742a96ef653144. Public Oracle additions do not establish fixes for historical INVALID/checksum/promotion failures. [Public review](decision-closing/bytebase-public.md). |
| Bytebase external-secret providers/auth | RESOLVED_PUBLICLY | Pinned 3.23.0 source supports Vault KV v2 token/AppRole, AWS Secrets Manager, GCP Secret Manager and Azure Key Vault with SDK credential chains. Actual estate provider/access/rotation is internal/runtime, not a public-product unknown. [Provider evidence](decision-closing/bytebase-public.md#external-secret-managers-source-bytebase-3230). |
| Bytebase source/Enterprise license boundary | RESOLVED_PUBLICLY | MIT subset has explicit commercial exclusions; Enterprise production use needs applicable subscription/agreement rights. Development/testing license allowance does not authorize feature activation or trial here. [License evidence](decision-closing/bytebase-public.md#license-and-production-entitlement-boundary-source). |
| Bytebase native verifier/advancement contract | RESOLVED_PUBLICLY | No first-class post-execution verifier contract established in inspected public interfaces. Inline failing PL/SQL is a plausible task-level path; propagation and UI/API predecessor enforcement are RUNTIME_REQUIRED. [Public/source findings](decision-closing/bytebase-public.md). |

## Estate

| ID / unknown | Disposition | Why it matters | How to obtain it | Decision affected |
| --- | --- | --- | --- | --- |
| E1 Oracle versions, RU, edition, charset | INTERNAL_INPUT_REQUIRED | Exact parser/driver/object/licensing compatibility; 26ai lab cannot certify estate | DBA supplies existing CMDB/support inventory or separately authorized read-only export | MUST M1; exact native/engine POC matrix |
| E2 RAC and HA/DR topology | INTERNAL_INPUT_REQUIRED | Instances/services can share a DB; aliases must not evade locks/counting | DBA maps existing cluster/database/standby records and failover model | Canonical lock/target count, recovery and entitlement |
| E3 Services, routes, SID/TCPS and aliases | INTERNAL_INPUT_REQUIRED | Routing changes approved target; auth/session limits differ | DBA/network owner supplies sanitized service-to-DB/PDB catalog and TLS/wallet requirements, no secrets | Binding, driver/build compatibility, session budget |
| E4 PDB count/container relationships | INTERNAL_INPUT_REQUIRED | Logical targets, restore scope and rights exceed instance count | Map existing CDB/PDB records to services/environments | Inventory/license count, isolation/restore |
| E5 Schema count, owners and grants | INTERNAL_INPUT_REQUIRED | Targets/credentials multiply per service; owner is not read-only observer | DBA/application owners supply existing ownership/grant records through approved process | Target model, least privilege, script and lock scope |
| E6 Applications, deployment streams, variants and release subsets | INTERNAL_INPUT_REQUIRED | Fifty instances are not universal fanout; streams can share schemas | Owners map repos/releases to schemas/current baselines; sample 2–3 releases | Inventory ownership, version admission, rollout |

## Identity

| ID / unknown | Disposition | Why it matters | How to obtain it | Decision affected |
| --- | --- | --- | --- | --- |
| I1 SSO/protocol/groups/stable principal IDs | INTERNAL_INPUT_REQUIRED | Human lifecycle/attribution and edition gates differ from fixtures | Identity owner provides actual provider/group and integration requirements | Edition, authenticated approval POC |
| I2 Roles and independent reviewer/approver/executor/admin policy | INTERNAL_INPUT_REQUIRED | Role names/quorum do not prove separation; API/console can bypass rollout | DBA/security/release owner documents actions/distinct actors by environment and privileged exceptions | MUST M5; native/composed authorization negatives |
| I3 Service accounts and initiating-human attribution | INTERNAL_INPUT_REQUIRED | Service creator must not conceal requester; seats/API scopes differ | DevOps inventories approved identities and attribution; product/contract defines scopes/counting | EE quote, AccessFlow contract, trusted CI |

## Infrastructure

| ID / unknown | Disposition | Why it matters | How to obtain it | Decision affected |
| --- | --- | --- | --- | --- |
| F1 Existing Jenkins/plugins/agents/owners | INTERNAL_INPUT_REQUIRED | Reuse reduces setup; new controller adds maintenance, not governance proof | DevOps supplies existing service/plugin inventory and operators | Practical S6 fallback; Jenkins not assumed |
| F2 Git/GitLab version and edition | INTERNAL_INPUT_REQUIRED | Free manual jobs/optional reviews do not prove deployment approval | DevOps supplies actual Git/CI entitlement and protected-environment controls | GitLab substitution, artifact/review integration |
| F3 Secret manager/credential store/rotation | INTERNAL_INPUT_REQUIRED | Need protected references and scoped access without assuming new services | Secrets owner identifies approved store/provider, nonsecret references and rotation owner | MUST M4; native EE provider versus runner |
| F4 Storage/retention/backup/restore/RPO/RTO | INTERNAL_INPUT_REQUIRED | Build archives expire; admission/audit must survive restart/restore | Platform owner supplies existing metadata/file/object storage and approved retention/restore policy | Extra services, native simplicity, MUST M9/M10 |
| F5 Existing Oracle tooling/entitlements | NO_LONGER_RELEVANT | OEM pack, SQLcl/SQLPlus or object tools may solve bounded needs already | Do not reopen reserve discovery; revisit only a concrete existing entitlement or mandatory-client requirement that changes the selected branch | Reuse/commercial reserve, mandatory client path |
| F6 Network/resources/session limits | INTERNAL_INPUT_REQUIRED | Connectivity/session budgets and metadata services affect lab/operations | Platform/network/DBA supply existing monitored limits and approved isolated-lab scope | POC entry, serial dispatch, later live scale |

## Process

| ID / unknown | Disposition | Why it matters | How to obtain it | Decision affected |
| --- | --- | --- | --- | --- |
| P1 Change frequency and DB releases/month | NO_LONGER_RELEVANT | Volume/complexity determines daily value | Defer measurement to the selected POC/adoption; not required to choose this branch. No savings are claimed | Operating-model value, maintain/buy comparison |
| P2 Current review/approval process and binding | INTERNAL_INPUT_REQUIRED | Manual policy details unknown; mandatory actors and mutation policy need definition | Capture ordinary release request/review/approval/selection/execution handoffs | MUST M5/M8; mandatory gate versus configurable SHOULD |
| P3 PROD windows, stop/cancel/resume policy | INTERNAL_INPUT_REQUIRED | Approval can expire during HOLD; running Oracle work cannot be presumed undone | DBA/release owner states windows, fresh PROD approval, cutoff/resume rules | Native promotion/batch and recovery policy |
| P4 Emergency changes and privileged access | INTERNAL_INPUT_REQUIRED | Routine bypass defeats admission; emergencies need traceability | Owners specify exception actors, evidence and retrospective reconciliation | RBAC/console and audit/recovery |
| P5 Current effort, failure/retry/lock investigation and audit retrieval | NO_LONGER_RELEVANT | No measured savings or cost comparison | Defer measurement to the selected POC/adoption; not required to choose this branch. No savings are claimed | Simplicity/value; no invented savings |
| P6 Maintenance and recovery owners/capacity | INTERNAL_INPUT_REQUIRED | Critical custom modules, upgrades and Oracle HOLD need people | Team names platform/DevOps/DBA/application responsibilities and available capacity | Adoption, code ceiling, buy comparison |

## Commercial

| ID / unknown | Disposition | Why it matters | How to obtain it | Decision affected |
| --- | --- | --- | --- | --- |
| C1 Budget and paid-software acceptance | INTERNAL_INPUT_REQUIRED | Preferably OSS does not authorize purchase; strict OSS branch stays separate | Owner states comparison/budget/contract constraints or OSS-only | Whether EE branch is available |
| C2 Bytebase EE quote/existing entitlement | COMMERCIAL_INPUT_REQUIRED | Plan/pricing is not a contract; physical/logical targets and service seats differ | Licensing/procurement provides terms, or obtains quote in separately authorized contact task: counting, self-host, approval/audit/secrets/support/renewal | Commercial C0 gate; no unlimited EE assumption |
| C3 Exact privately entitled build/image/driver/access | COMMERCIAL_INPUT_REQUIRED | Public latest version is resolved; legitimate licensed artifact access is private | Supported artifact record identifies version/digest/driver, relevant build/policy delta and legitimate access; no trial here | Future exact-build EE regression entry/scope |
| C4 Other paid entitlement/support | NO_LONGER_RELEVANT | Existing Oracle/NineData/Harness/etc. rights change reuse economics | Do not reopen reserve discovery; revisit only a concrete existing entitlement or mandatory-client requirement that changes the selected branch | Whether a specific reserve merits reopening |

## Technical

| ID / unknown | Disposition | Why it matters | How to obtain it | Decision affected |
| --- | --- | --- | --- | --- |
| T1 Mandatory SQLPlus/SQLcl features | INTERNAL_INPUT_REQUIRED | JDBC Community is not full SQLPlus; stripping commands can change semantics | Static sanitized script inventory of PROMPT/SET/SPOOL/@/@@/WHENEVER and required client behavior | Product/engine/edition compatibility and client path |
| T2 Substitution variables and runtime options | INTERNAL_INPUT_REQUIRED | &/&& differ from engine placeholders; effective bytes/options need approval | Static corpus review plus nonsecret rendering policy | Binding, adaptation and engine choice |
| T3 Cross-schema migrations/grants/dependencies | INTERNAL_INPUT_REQUIRED | Local locks/principals may not protect every touched object | Owners identify touched schemas/types/dependencies/approved grants from records/scripts | Admission lock scope, privilege and validity |
| T4 DML + DDL atomicity expectations | INTERNAL_INPUT_REQUIRED | Implicit DDL commits prevent general whole-script rollback; statement DML commits can violate needs | Owners state transaction boundaries and approved forward-fix/compensation for representative releases | Hard executor compatibility; no arbitrary DDL exactly-once promise |
| T5 Current supported ODC safety delta | RESOLVED_PUBLICLY | No qualifying supported native closure established; later binary internals are not inferred | Public recheck closed this branch; see decision-closing/odc-public-delta.md. Do not continue historical image mapping or unchanged surveys | ODC remains HOLD; no new ODC POC |
| T6 Native/external state and recovery guarantees | RUNTIME_REQUIRED | Revision, API EXECUTED, engine history and Oracle effects can disagree | Future authorized focused contract/regression with real actors and observable commit/session/result checkpoints, separate run records | EE native adequacy, AccessFlow reserve, CI HOLD |
| T7 ODC logs/attachment durability root cause | RUNTIME_REQUIRED | Restart/read/HTTP 500 failures unresolved; persistence settings only hypothesis | Existing sanitized config/log review when available, then authorized changed-setup restart/restore/download regression | MUST M9; whether bounded persistence/export suffices |

## Smallest team decision dataset

Use only the **seven grouped facts** in [final-decision.md, section 14](final-decision.md#14-minimal-internal-decision-dataset): commercial allowance; sanitized Oracle target map; mandatory corpus; actors/identities; already operated infrastructure; accountable owners; isolated POC access/grants. Each states why it changes the decision and who can answer it. Individual IDs above preserve provenance; they are not 32 questions to send the team.

Runtime dependencies T6/T7 are acceptance work after selection, not reasons to prolong public research. Historical source/image correspondence is no longer a current ODC research task without a supported safety delta. No public unknown is transferred to the internal team. No purchase, runtime PASS or canonical candidate-status change follows from this closure.
