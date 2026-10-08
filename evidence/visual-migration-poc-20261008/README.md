# Visual migration POC evidence · 8 October 2026

The [dashboard](../../demo/dashboard/index.html) and [formal report](../../demo/dashboard/migration-report.html) are the human-facing artifacts. This directory records their verification and the sanitized evidence snapshot used to generate them.

## Inputs

`inputs/` preserves existing records from the previous `github-odc-runtime-demo-20261008` work without modifying that uncommitted work. GitHub metadata was refreshed read-only using `gh`; the 34-test count comes from validation run `37670936711`'s real job log. `retention-conclusion.json` is the historical test from `evidence/odc-retention-experiment-20261007`, tickets `2000013/2000014`. `retention-current-state.json` is the newer configuration observation. Nothing here is a new ODC/Oracle execution.

Happy ODC batch **2000015 / APPROVING** and pending approval observations are LIVE. Its current report's runtime result is NOT_AVAILABLE. Failure/correction pending machine reports are retained alongside their separate repository fixture demos. The dashboard's data contains source filenames and full SHA-256 references.

## Verification and captures

- [visual-checks.json](visual-checks.json): offline `file://` loads, no network requests, embedded data/hash/credential checks, local links, tabs, keyboard, presentation, mobile and print.
- [local-checks.json](local-checks.json): unit tests, manifests, fixture packaging/report generation, workflow lint and document verification.
- [dashboard-overview.png](dashboard-overview.png), [full desktop page](dashboard-desktop.png).
- [environment-rollout.png](environment-rollout.png): actual waiting stages.
- [scenario-actual.png](scenario-actual.png), [scenario-expected.png](scenario-expected.png), [scenario-failure.png](scenario-failure.png), [scenario-correction.png](scenario-correction.png).
- [mobile overview](dashboard-mobile-overview.png), [full mobile page](dashboard-mobile.png).
- [report overview](migration-report-overview.png), [full report](migration-report.png), [print rendering](migration-report-print.png), [printed PDF](migration-report.pdf), [PDF layout checks](pdf-checks.json), [page 1](report-pdf-page-1.png), [page 3](report-pdf-page-3.png), [page 4](report-pdf-page-4.png), [page 6](report-pdf-page-6.png).

These screenshots are actual captures of the finished dashboard and report. No GitHub/ODC UI screenshot was fabricated. The local repository's existing runtime records were used instead of initiating another runtime experiment.
