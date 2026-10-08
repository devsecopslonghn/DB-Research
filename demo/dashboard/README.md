# Open Visual POC

Open [index.html](index.html) in a browser. No backend, database, server, npm, network access or SaaS is needed to view either HTML page.

From the repository root:

```bash
# macOS
open demo/dashboard/index.html

# Linux
xdg-open demo/dashboard/index.html
```

Windows PowerShell:

```powershell
Start-Process demo/dashboard/index.html
```

Open [migration-report.html](migration-report.html) for the formal report; choose **Print / Save PDF**. Enable background graphics for badge colors. Labels remain readable without color. [A captured PDF](../../evidence/visual-migration-poc-20261008/migration-report.pdf) is also included.

## A 2–3 minute demo

1. Start at the header: application, release, real batch and **WAITING APPROVAL**.
2. Show architecture: GitHub validates; ODC approves and executes; Oracle independently verifies.
3. Show GitHub's merged PR, passing runs, 34 historical passing tests and verified package.
4. Show incomplete approval nodes and the four waiting environment cards. The Oracle panel has **NOT RUN** checks.
5. Select **Expected Flow**, **Failure Demo**, then **Correction Demo**. Purple **FIXTURE DEMONSTRATION** labels remain visible. Explain ORA-20042 at SIT and a new correction release with new hashes and approvals.
6. Show the evidence chain, historical retention proof, before/after comparison and ODC/Flyway boundary. Finish with **GO FOR INTERNAL PILOT** and **Production Rollout: NOT APPROVED**.

**Presentation mode** provides 11 section stops. Use Next/Previous, ArrowRight/ArrowLeft or PageDown/PageUp. Escape exits. Scenario tabs also support arrow keys. Normal scrolling remains available.

## What the snapshot proves

| Area | Evidence / current result |
| --- | --- |
| Happy release | **PARTIAL LIVE**: real ODC batch `2000015`, native `APPROVING`; no completed approval or migration execution |
| Oracle acceptance | **NOT AVAILABLE**; current checks **NOT RUN**; preflight is separate |
| Failure / correction | **FIXTURE** demonstrations; no live tickets created |
| GitHub | **LIVE PASS** for implementation PR #1; `db-report` is a fixture rendering job |
| Retention | Historical **LIVE PASS** on tickets `2000013/2000014`; current configuration separately verified |

The original batch source is `848e0923…`, PR head is `44b3ee74…`, merge is `9bb1215a…`. They are intentionally separate. Authenticated Actions-to-ODC runtime handoff remains pending. Runtime evidence was read from existing sanitized records; no acceptance was expanded for this deliverable.

## Refresh after new evidence

The source of truth is [data/demo-status.json](data/demo-status.json), generated from the recorded report/envelope, ODC receipt, native approval nodes, GitHub metadata, retention proof and existing fixtures. Both HTML files embed that data, CSS and JavaScript safely so browser local-file restrictions cannot block loading. Editing JSON alone will not update the HTML pages.

Recorded inputs live in [the evidence snapshot](../../evidence/visual-migration-poc-20261008/inputs/). After a separately authorized runtime evidence collection, replace the corresponding sanitized files there (keep receipt, report and native approval snapshot consistent), then run:

```bash
python3 -m scripts.db_demo.build_dashboard
python3 -m scripts.db_demo.verify_dashboard
```

To refresh implementation PR #1 and its source/merge-specific workflow metadata from GitHub, with authenticated `gh` installed:

```bash
python3 -m scripts.db_demo.build_dashboard --refresh-github
```

This flag reads GitHub metadata and test counts; it does not connect to ODC/Oracle, approve, execute, or create a batch. It does not confuse this dashboard PR's checks with the original implementation's provenance.

You may pass `--evidence-dir evidence/<new-sanitized-snapshot>/inputs` using the same filenames/layout. Keep that directory inside the repository for portable source links. Preserve historical retention proof and fixtures; replace actual observations only with actual observations. SQL/manifest hash mismatch stops generation. Update scenario runtime notes when new failure/correction acceptance exists; the sample tabs continue to describe fixtures.

The builder and static check need Python 3.9+ and only the standard library. Existing migration checks still use the repository's bounded PyYAML requirement. Editable presentation sources are [page.template.html](assets/page.template.html), [dashboard.css](assets/dashboard.css), and [dashboard.js](assets/dashboard.js); regenerate after editing them.

## Verification

```bash
python3 -m unittest discover -s scripts/db_demo/tests -v
python3 -m scripts.db_demo.verify_dashboard
```

Optional browser checks need Playwright and Chromium in the verification environment, never to view the deliverable:

```bash
python3 -m scripts.db_demo.verify_dashboard --browser --chromium /path/to/chromium
```

This checks `file://`, blocks network requests, verifies local links, tabs, keyboard navigation, mobile width and print rendering, and captures screenshots/PDF in [evidence/visual-migration-poc-20261008](../../evidence/visual-migration-poc-20261008/README.md). The HTML files can be copied individually for the presentation; repository evidence links require keeping the checkout available. External GitHub links need connectivity only when opened.
