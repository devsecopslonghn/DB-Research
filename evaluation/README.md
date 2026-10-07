# Evaluation evidence index

**GitHub/ODC migration demo:** [Demo landing page](../demo/README.md) and [implementation/runtime evaluation](github-odc-migration-demo.md) record the downstream `customer-profile` migration pipeline. New evidence is kept separately from the original research, acceptance and retention records.

**Final ODC practical-adoption decision:** **GO for the governed internal pilot with the demonstrated retention settings.** Read the [final retention experiment and executive decision](odc-retention-experiment.md), [updated practical results](odc-practical-poc-results.md), [new retention evidence](../evidence/odc-retention-experiment-20261007/) and [minimal GitOps recommendation](../evidence/odc-retention-experiment-20261007/permanent-gitops-recommendation.yaml). Fresh successful/failed tickets preserve result/log/ZIP/metadata/audit after ordinary replacement without retired-pod routing. Exact baseline configuration and Argo reconciliation are restored; ODC/MetaDB are healthy and historical evidence remains unchanged. Apply the demonstrated GitOps settings before pilot operation. The [earlier practical baseline](../evidence/odc-practical-poc-20261007/) remains FAIL for retention; no A/B/C/E or Bytebase rerun occurred. Updated practical parity is **86/100, moderate gap**; Flyway automatic migration-version/replay semantics and production estate hardening remain distinct.

**Latest product comparison, 7 October 2026:** Read [ODC versus Bytebase for practical adoption](odc-bytebase-practical-comparison.md) for the new research mission. It uses the evidenced Bytebase product rather than a custom safety contract, scores ODC 80/100 (moderate gap), rates production hardening risk HIGH, and recommends a focused workflow POC with five bounded adoption items. DOC/SOURCE/RUNTIME/UNKNOWN remain separate. Earlier mission conclusions and the separate CI runtime task below are preserved; no SQL, new product test or historical verdict edit occurred.

**Current runtime task, 7 October 2026:** Use the existing CI/Flyway reference only. [Runtime prerequisites and acceptance evidence](../poc/reports/runtime-prerequisites-20261007T095109Z/README.md), [current T1–T7 BLOCKED records](../poc/reports/runtime-prerequisites-20261007T095109Z/cases.json), and [POC results](../poc/results.md) record completed local preparation and the remaining target/identity/CI/Git/JDBC inputs. No features, architecture changes or ODC reopening; no Oracle case executed yet.

**Current comparison, 7 October 2026:** Read [ODC versus the implemented CI reference](odc-vs-ci-reference.md) first, supported by [recovered current lab state](odc-current-lab-state.md) and [sanitized read-only capture](odc-current-lab-evidence-20261007.json). This independent round gives neither historical ODC HOLD nor implemented CI a default preference. ODC wins routine UX; the CI reference wins the specified simplicity/architecture threshold, with Oracle/Jenkins acceptance still blocked. At least four ODC additions remain and admission/recovery needs an independent authority; renewed ODC runtime is not justified. No SQL/tests or cluster changes were made and historical results remain unchanged.

**Implemented benchmark:** [OSS POC](../poc/OSS-POC-README.md), [workload](../poc/workload-profile.md), [engine](../poc/engine-selection.md), [topology](../poc/lab-topology.md), [architecture](../poc/architecture.md), [test plan](../poc/test-plan.md), [results](../poc/results.md). Its five owned responsibilities and retained local checks are the comparison benchmark, not adoption acceptance.

**Requirement and decision provenance:** [current-baseline.md](current-baseline.md) defines the consolidated requirements and earlier candidate statuses; [rejection-register.md](rejection-register.md) records prior stopped proposals; [open-questions.md](open-questions.md) records unresolved inputs. The explicit new ODC/CI comparison above is the outcome authority for this round; baseline status labels did not decide it. [final-decision.md](final-decision.md) retains the earlier commercial/OSS decision tree and gates, including the conditional Bytebase EE branch. Historical records are preserved.

## Decision provenance

| Stage | Supporting record and historical scope |
| --- | --- |
| Native evaluation | [Report](report.md), [shortlist](shortlist.md), [round-two index](research-round-2/README.md): native findings and scoped candidate decisions |
| Tool roles/fit | [Catalog](tool-feature-catalog.md): existing capabilities, license/edition/pin evidence; not adoption acceptance |
| Composition proposals | [Solutions](solution-shortlist.md), [architectures](reference-architecture.md), [POC plan](poc-plan.md): old S2/S3/S6 designs before handoff validation |
| Handoff/fallback validation | [Validation](poc-design-validation.md), [gates](decision-gates.md): MANUAL versus external completion; S2/S3 stopped, former S6-first priority |
| Integrated simplicity | [Reassessment](architecture-reassessment.md): owned correctness/recovery burden; conditional EE regression, ODC HOLD, AccessFlow API reserve, S6 fallback |
| Goal-aligned operating decision | [Final assessment](goal-aligned-final-assessment.md): actual UI journeys, Oracle/license/custom-code/operations comparison, three conditional options and a small OSS POC entry/design; canonical statuses unchanged |
| Decision-closing round | [Final decision](final-decision.md): preferred commercial branch, selected OSS fallback, current public closure, hard POC entry/stop gates and smallest internal dataset; baseline remains factual authority |
| Implemented OSS benchmark | [POC results](../poc/results.md), [architecture](../poc/architecture.md): one-target implementation and 30 local tests; Oracle/Jenkins runtime blocked, promotion not implemented |
| Recovered ODC/CI reassessment | [Comparison](odc-vs-ci-reference.md), [current state](odc-current-lab-state.md), [capture](odc-current-lab-evidence-20261007.json): actual preserved lab, responsibility/UX/operations/failure comparison; CI reference selected conditionally, ODC runtime not justified |
| Practical Bytebase product benchmark | [Practical comparison](odc-bytebase-practical-comparison.md): daily feature/UX/ownership matrix, historical failure severity, 80/100 ODC parity, HIGH hardening risk and focused adoption POC recommendation under the new mission; no new runtime or verdict edits |

The baseline reconciles evidence and chronology. Old Category A/B/C and POC A/B labels are not its three architecture classes. Older GO/GREEN describes design feasibility, not passed Oracle tests or execution permission.

## Source, license and candidate records

| Subject | Targeted references |
| --- | --- |
| ODC | [Source](candidates/odc/source-review.md), [report](candidates/odc/report.md), [survey](research-round-2/coordinator/odc-source-survey-20261006.md), [historical cases](candidates/odc/cases.json) |
| ODC previous public delta | [Earlier release/source/configuration/API review](decision-closing/odc-public-delta.md): historical HOLD conclusion preserved; [new lab/reference comparison](odc-vs-ci-reference.md) independently assesses current ownership and reuse |
| Bytebase | [Source/license](candidates/bytebase/source-review.md), [report](candidates/bytebase/report.md), [runtime-commit manifest](candidates/bytebase/source-manifest.json), [historical cases](candidates/bytebase/cases.json) |
| Bytebase final public facts | [Edition/counting/architecture/Oracle/API/secrets/source changes](decision-closing/bytebase-public.md): publicly resolvable facts closed, quote and exact-build acceptance separated |
| AccessFlow | [Source](candidates/accessflow/source-review.md), [report](candidates/accessflow/report.md), [native trace](research-round-2/coordinator/oracle-governance-source.md), [external API](architecture-reassessment.md#supported-external-deployment-api-composed-reserve), [new cases NOT_RUN](candidates/accessflow/cases.json) |
| AccessFlow final public contract | [Supported API and runner responsibility review](decision-closing/accessflow-public-contract.md): repeated confirmation, unbound artifacts/targets and reported outcomes; no demonstrated CI simplicity win |
| CloudDM | [Source](candidates/clouddm/source-review.md), [report](candidates/clouddm/report.md), [v4.3.0 artifact review](research-round-2/coordinator/clouddm-v430-artifact-review-20261007.md), [new cases NOT_RUN](candidates/clouddm/cases.json) |
| Archery | [Source](candidates/archery/source-review.md), [report](candidates/archery/report.md), [release/Oracle trace](research-round-2/coordinator/oracle-governance-source.md), [new cases NOT_RUN](candidates/archery/cases.json) |
| Licensing/distribution | [License/release](research-round-2/licensing/licensing-review.md), [registry](research-round-2/licensing/registry-review.md), [components](research-round-2/licensing/license-components.csv), [root audit](../LICENSE-AUDIT.md) |
| Discovery history | [Candidate register](candidates.csv), [search log](search-log.md), [round-two discovery](research-round-2/discovery/source-review.md); no broad discovery scheduled |

## Immutable acceptance and review history

[ODC results](../ODC-ORACLE-POC-RESULTS.md), [Bytebase results](../BYTEBASE-ORACLE-POC-RESULTS.md) and [comparison](../BYTEBASE-ODC-COMPARISON.md) record exact historical builds/editions on the Oracle 26ai one-database lab. They do not establish current-version, EE or actual-estate acceptance.

[45-case contract](../poc/ORACLE-POC.md), [criteria](criteria.csv), [feature evidence](feature-matrix.csv), [workload manifest](workloads/manifest.json), [benchmark spec](benchmark-spec.md) and [config](benchmark-config.json) remain original references. [Benchmarks](benchmarks/README.md) has no raw samples; new runtime/recovery/scale work remains NOT_RUN.

[T00–T04 history](history/t00-t04/README.md), [preserved hashes](preserved-evidence.json), [freeze manifest](freeze-manifest.json), [acceptance record](acceptance-status.json), [coordinator review](reviews/coordinator-review.md) and [round-two review](research-round-2/coordinator-review.md) preserve earlier decisions/checks. Dated check JSON and diffs describe their own runs; do not overwrite them with consolidation checks.

Run from repository root: `python tools/verify_research_documents.py`. This read-only verifier checks links/tables, snapshots, source hashes, screenshots and authoritative criterion IDs/statuses; it does not execute candidate software or Oracle SQL. The comparison above records the newly requested reassessment without altering historical acceptance or authorizing runtime work.
