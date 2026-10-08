"""Unauthenticated runner network probe; records no endpoint/key/credential values."""
import argparse
import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request

from .common import summary, write_json
from .odc_client import SameOriginRedirect


def probe(base):
    result = {"runner": os.environ.get("RUNNER_NAME", "LOCAL"), "authentication": "NOT_ATTEMPTED",
              "reachable": False, "classification": "NOT_AVAILABLE", "http_status": None}
    parts = urllib.parse.urlsplit(base)
    if not base:
        result["reason"] = "ODC_DEMO_PROBE_URL repository variable is not configured"
        return result
    if parts.scheme != "https" or not parts.hostname or parts.username or parts.password or parts.query or parts.fragment:
        result.update(classification="BLOCKED", reason="Approved probe URL must be credential-free HTTPS")
        return result
    opener = urllib.request.build_opener(SameOriginRedirect())
    try:
        with opener.open(base.rstrip("/") + "/api/v2/encryption/publicKey", timeout=12) as response:
            value = json.loads(response.read(65536))
            result["http_status"] = response.status
            data = value.get("data")
            key = data.get("publicKey") if isinstance(data, dict) else data
            if value.get("successful") is True and isinstance(key, str) and key:
                result.update(reachable=True, classification="REACHABLE_UNAUTHENTICATED")
            else:
                result.update(classification="BLOCKED", reason="Expected ODC API key response is unavailable")
    except urllib.error.HTTPError as exc:
        result.update(classification="BLOCKED", http_status=exc.code, reason="ODC API access is denied from this runner")
    except (urllib.error.URLError, TimeoutError, ValueError):
        result.update(classification="BLOCKED", reason="ODC API is unreachable from this runner")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = probe(os.environ.get("ODC_DEMO_PROBE_URL", ""))
    write_json(args.output, result)
    summary(f"## ODC runner network probe\n\nResult: **{result['classification']}**. Authentication: **NOT_ATTEMPTED**. This probe does not establish approval, Oracle execution or credential readiness. Live workflows default to existing `self-hosted`, `linux`, `odc-demo` runners.\n")
    print(result["classification"])


if __name__ == "__main__":
    main()
