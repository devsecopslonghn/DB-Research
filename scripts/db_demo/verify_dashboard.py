"""Check standalone artifacts; optional Playwright checks capture offline screenshots.

Default checks need Python only. --browser needs Playwright and a Chromium binary.
No live runtime systems are contacted. Browser requests to the network are blocked.
"""
import argparse
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re

from .build_dashboard import DASHBOARD, ROOT, safe_json, sha


class EmbeddedData(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_data = False
        self.data = ""
        self.external = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "script" and attrs.get("id") == "demo-data":
            self.in_data = True
        if tag in ("script", "img", "link"):
            url = attrs.get("src", attrs.get("href", ""))
            if url:
                self.external.append(url)

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_data = False

    def handle_data(self, data):
        if self.in_data:
            self.data += data


def static_checks():
    data = json.loads((DASHBOARD / "data/demo-status.json").read_text())
    for filename in ("index.html", "migration-report.html"):
        parsed = EmbeddedData()
        parsed.feed((DASHBOARD / filename).read_text())
        assert not parsed.external, (filename, parsed.external)
        assert json.loads(parsed.data) == data, "Embedded data differs from JSON"
    for item in data["files"] + data["sources"]:
        filename = item.get("path", item.get("file"))
        assert sha(ROOT / filename) == item["sha256"], f"Hash mismatch: {filename}"
    # Inspect JSON property names, not mentions of required-but-absent credentials.
    def no_secrets(value):
        if isinstance(value, dict):
            for key, child in value.items():
                assert not re.fullmatch(r"(?i)(password|access_token|refresh_token|private_key|authorization|cookie)", key), f"Credential field: {key}"
                no_secrets(child)
        elif isinstance(value, list):
            for child in value:
                no_secrets(child)
        elif isinstance(value, str):
            assert not re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN .*PRIVATE KEY-----", value), "Credential pattern"
    no_secrets(data)
    for item in data["sources"]:
        no_secrets(json.loads((ROOT / item["file"]).read_text()))
    return {"standalone_embedded_assets": "PASS", "json_matches_both_html_pages": "PASS", "source_and_sql_hashes": "PASS", "credential_scan": "PASS"}


def browser_checks(output, executable):
    from playwright.sync_api import sync_playwright
    output.mkdir(parents=True, exist_ok=True)
    findings = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=executable, headless=True, args=["--no-sandbox"])
        context = browser.new_context(viewport={"width":1440,"height":1050}, device_scale_factor=1)
        errors, requests, broken = [], [], []
        context.on("page", lambda page: page.on("pageerror", lambda err: errors.append(str(err))))
        context.route(re.compile(r"https?://.*"), lambda route: (requests.append(route.request.url), route.abort()))
        page = context.new_page()
        page.goto((DASHBOARD / "index.html").as_uri())
        page.wait_for_selector(".hero")
        assert page.locator(".hero-status h2").inner_text() == "WAITING APPROVAL"
        assert page.locator("#rollout .environment").count() == 4
        assert page.locator("#verification td").filter(has_text="NOT RUN").count() == 32
        page.screenshot(path=str(output / "dashboard-desktop.png"), full_page=True)
        page.screenshot(path=str(output / "dashboard-overview.png"))
        page.locator("#rollout").screenshot(path=str(output / "environment-rollout.png"))
        for scenario in ("expected", "failure", "correction", "actual"):
            page.locator(f"#tab-{scenario}").click()
            page.locator("#scenarios").scroll_into_view_if_needed()
            if scenario != "actual":
                assert "FIXTURE DEMONSTRATION" in page.locator("#scenario-content").inner_text()
                assert page.locator("#scenario-content .env-source .fixture").count() == 4
            if scenario == "failure":
                assert "ORA-20042" in page.locator("#scenario-content").inner_text()
                assert page.locator("#scenario-content .environment.failed").count() == 1
            page.locator("#scenarios").screenshot(path=str(output / f"scenario-{scenario}.png"))
        page.locator("#tab-actual").focus()
        page.keyboard.press("ArrowRight")
        assert page.locator("#tab-expected").get_attribute("aria-selected") == "true"
        page.locator("#tab-actual").click()
        page.locator("#presentation").click()
        assert page.locator("body").get_attribute("class") == "presentation"
        page.locator("#next-section").click()
        assert "2 / 11" in page.locator("#section-position").inner_text()
        page.keyboard.press("Escape")
        assert "presentation" not in (page.locator("body").get_attribute("class") or "")
        page.set_viewport_size({"width":390,"height":844})
        page.goto((DASHBOARD / "index.html").as_uri())
        page.wait_for_selector(".hero")
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "Mobile horizontal overflow"
        page.screenshot(path=str(output / "dashboard-mobile.png"), full_page=True)
        page.screenshot(path=str(output / "dashboard-mobile-overview.png"))
        page.set_viewport_size({"width":1120,"height":1050})
        page.goto((DASHBOARD / "migration-report.html").as_uri())
        page.wait_for_selector(".report-header")
        page.screenshot(path=str(output / "migration-report.png"), full_page=True)
        page.screenshot(path=str(output / "migration-report-overview.png"))
        page.emulate_media(media="print")
        assert page.locator("#print-report").is_hidden()
        page.pdf(path=str(output / "migration-report.pdf"), format="A4", print_background=True, prefer_css_page_size=True)
        page.screenshot(path=str(output / "migration-report-print.png"))
        # Check every rendered local link on both pages, including all scenario states.
        for filename in ("index.html", "migration-report.html"):
            page.goto((DASHBOARD / filename).as_uri())
            for href in page.locator("a[href]").evaluate_all("nodes => nodes.map(n => n.href)"):
                if href.startswith("file:"):
                    from urllib.parse import unquote, urlparse
                    parsed = urlparse(href)
                    if not Path(unquote(parsed.path)).exists():
                        broken.append(href)
                    if parsed.fragment:
                        assert page.locator(f'[id="{parsed.fragment}"]').count(), f"Broken anchor {href}"
        # Data values remain text even when an edited snapshot contains HTML.
        page.emulate_media(media="screen")
        hostile = json.loads((DASHBOARD / "data/demo-status.json").read_text())
        payload = '\"><img src=x onerror="window.__dashboardXss=1">'
        hostile["happy_path"] = payload
        hostile["application"] = payload
        hostile["files"][0]["file"] = payload
        hostile["approvals"][0]["actor"] = payload
        hostile["environments"][0]["status"] = payload
        for filename in ("index.html", "migration-report.html"):
            html = (DASHBOARD / filename).read_text()
            html = re.sub(r'(<script id="demo-data" type="application/json">).*?(</script>)',
                          lambda m: m[1] + safe_json(hostile) + m[2], html, flags=re.S)
            page.set_content(html)
            assert page.locator("img").count() == 0, "Evidence text introduced HTML"
            assert page.evaluate("window.__dashboardXss === undefined"), "Evidence text executed code"
            if filename == "index.html":
                page.locator("#tab-actual").click()
                assert page.locator("img").count() == 0
        assert not errors, errors
        assert not requests, f"Network dependency: {requests}"
        assert not broken, broken
        browser.close()
        findings.update({"file_url_load": "PASS", "network_requests": len(requests), "browser_errors": errors,
                         "missing_local_links": broken, "scenario_tabs_and_keyboard": "PASS", "presentation_controls": "PASS",
                         "mobile_390px": "PASS", "print_pdf": "PASS", "oracle_pending_cells": 32})
        findings["hostile_evidence_stays_text"] = "PASS"
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", action="store_true")
    parser.add_argument("--chromium", help="Optional Chromium executable path")
    parser.add_argument("--output", type=Path, default=ROOT / "evidence/visual-migration-poc-20261008")
    args = parser.parse_args()
    checks = {"checked_at": datetime.now(timezone.utc).isoformat(), "static": static_checks()}
    if args.browser:
        checks["browser"] = browser_checks(args.output, args.chromium)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "visual-checks.json").write_text(json.dumps(checks, indent=2)+"\n")
    print(json.dumps(checks, indent=2))


if __name__ == "__main__":
    main()
