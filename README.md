# Oracle database change-management research

**GitHub/ODC migration demo:** Start at [demo/README.md](demo/README.md) for the new `customer-profile` implementation, three releases, validation, native ODC handoff and reports. [Demo evaluation](evaluation/github-odc-migration-demo.md) separates implementation, local checks, GitHub Actions and live ODC/Oracle evidence. Historical research below retains its original conclusions.

**Latest product comparison (7 October 2026): [ODC versus Bytebase for practical adoption](evaluation/odc-bytebase-practical-comparison.md).** The new research mission benchmarks Bytebase's evidenced daily workflow: ODC scores 80/100, has a moderate product gap and merits a focused adoption POC; production hardening risk remains HIGH. This documentation-only recommendation uses the practical workflow rather than the earlier custom-controller threshold. Earlier decisions and the separate CI implementation/runtime task below remain preserved; no SQL or new product test was run.

**Current implementation task (7 October 2026): [OSS-only single-target POC](poc/OSS-POC-README.md).** The user has ruled out commercial software and selected reuse of the existing CI plus one Oracle engine. The runner/tests/reports are implemented; [runtime results and blockers](poc/results.md) govern this task. The research decision records below remain historical evidence, with no result rewrites.

**Start with [the current baseline](evaluation/current-baseline.md).** It is the authoritative goal, requirements, architecture classification, candidate status and next decision, consolidated on 7 October 2026. Read it before extending research or interpreting an older shortlist.

**For the actionable decision, read [final-decision.md](evaluation/final-decision.md).** The decision-closing round recommends a gated Bytebase EE native regression when commercial terms and supported controls are viable; otherwise select the existing CI + Oracle-engine contract POC. ODC remains HOLD, and AccessFlow remains a reuse-dependent reserve without a demonstrated simplicity advantage. The document contains the decision tree, exact entry/stop gates and seven internal facts that can change the branch. It grants no runtime or purchase authorization.

The project seeks the simplest maintainable centralized Oracle workflow improving DBeaver/manual SQL and standalone Git/Flyway CLI for approximately 50 instances and 20 users, preferably free OSS and self-hosted. CI/CD is an integration requirement; Jenkins and Flyway are optional.

An integrated platform is preferred, but no OSS adoption winner is proved. Four decision options remain: ODC native (HOLD), AccessFlow deployment API + engine (RESERVE), Bytebase EE (COMMERCIAL_CHECK), and CI/Flyway (FALLBACK). No new runtime POC is currently eligible. Next establish whether suitable self-hosted EE entitlement/budget and an exact licensed build are available for the actual estate; FREE failures do not decide EE correctness.

1. [Current baseline](evaluation/current-baseline.md): problem, workflow, evidence, requirements, pain-to-capability mapping, decision model and timeline.
2. [Rejection register](evaluation/rejection-register.md): why proposals were stopped/deprioritized and what evidence would reopen them.
3. [Decision questions](evaluation/open-questions.md): public facts closed and all original questions classified as public, internal, commercial, runtime or no longer relevant.
4. [Evaluation evidence index](evaluation/README.md): detailed reports, source reviews, licensing, preserved acceptance and history.

## Historical runtime and acceptance

| Record | Exact scope | Retained results |
| --- | --- | --- |
| [ODC API/UI POC](ODC-ORACLE-POC-RESULTS.md), 4 October 2026 | ODC 4.4.1-20260116; Oracle 26ai Enterprise Edition 23.26.4.1.0; four environment schemas on one database; local TCPS wrapper | 12 PASS / 20 PARTIAL / 5 FAIL / 8 NOT_RUN |
| [Bytebase API/UI POC](BYTEBASE-ORACLE-POC-RESULTS.md), 4 October 2026 | Bytebase 3.22.1/FREE, commit a85f6cb4195299995e8554303550d672d5093e1d; same lab, not EE regression | 17 PASS / 14 PARTIAL / 4 FAIL / 3 BLOCKED / 7 NOT_RUN; extra SQL-review FAIL outside 45 totals |

[Runtime comparison](BYTEBASE-ODC-COMPARISON.md), [45-case Oracle contract](poc/ORACLE-POC.md), [criteria](evaluation/criteria.csv), [workload hashes](evaluation/workloads/manifest.json) and [engine/source evidence](EVIDENCE.md) retain their original case-level meaning. DOC, SOURCE, RUNTIME, DESIGN, UNKNOWN and NOT_RUN are separate labels. There are no new benchmarks or verified 50-instance load results.

## Earlier research generations

These are dated supporting records. Their “current,” “next,” Category A/B/C and POC A/B wording belongs to the stage in which they were written; the baseline reconciles it. Older next-step recommendations are not additional active work.

| Generation | Documents |
| --- | --- |
| Initial research and product model, 3–4 October | [Original report](REPORT.md), [brief](brief.md), [product constraint](product-model-constraint.md), [product comparison](PRODUCT-MODEL.md), [UI evidence](UI-EVIDENCE.md), [forks](FORK-SEARCH.md), [licenses](LICENSE-AUDIT.md), [Oracle coverage](ORACLE-COMPATIBILITY.md), [maturity](MATURITY.md) |
| Platform evaluation/T00–T04, 4 October | [Evaluation report](evaluation/report.md), [old shortlist](evaluation/shortlist.md), [frozen history](evaluation/history/t00-t04/README.md), [platform plan](poc/PLATFORM-EVALUATION-PLAN.md) |
| Deep source/license/artifacts, 4–7 October | [Round-two index](evaluation/research-round-2/README.md), [CloudDM artifact decision](evaluation/research-round-2/coordinator/clouddm-v430-artifact-review-20261007.md), [ODC survey](evaluation/research-round-2/coordinator/odc-source-survey-20261006.md) |
| Catalog/composition, 7 October | [Catalog](evaluation/tool-feature-catalog.md), [solution shortlist](evaluation/solution-shortlist.md), [reference architecture](evaluation/reference-architecture.md), [POC plans](evaluation/poc-plan.md) |
| Validation/gates/reassessment, 7 October | [Design validation](evaluation/poc-design-validation.md), [decision gates](evaluation/decision-gates.md), [architecture reassessment](evaluation/architecture-reassessment.md) |

The consolidation and final decision are documentation only. Historical evidence, expected results, workloads and source working files remain unchanged. Run the existing read-only document check with `python tools/verify_research_documents.py`; it checks research artifacts, not product acceptance.

## Repository checkout

The repository is hosted at [devsecopslonghn/DB-Research](https://github.com/devsecopslonghn/DB-Research). Upstream source snapshots under `evidence/source/`, `evidence/additional-source/` and `evidence/product-model/{sources,forks}/` are Git submodules pinned to the existing evidence commits. Restore them before checking source references:

```bash
git clone --recurse-submodules https://github.com/devsecopslonghn/DB-Research.git
cd DB-Research
python3 tools/verify_research_documents.py
```

For an existing checkout, run `git submodule update --init --recursive`. Keep the recorded submodule commits; `git submodule update --remote` would replace the evaluated snapshots. Local credentials, environment overrides, caches and generated runtime output are excluded by `.gitignore`. Historical reports and retained evidence keep their existing contents.
