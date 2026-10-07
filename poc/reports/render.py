import html
import json
from pathlib import Path

from poc.common import canonical, identifier


def write_report(store, release_id, directory):
    identifier(release_id)
    row = store.get(release_id)
    envelope = row["envelope"]
    metadata = {**envelope, **{k: row[k] for k in ("reviewed_by", "approved_by", "executor", "start_time",
                                                   "end_time", "status", "verification_status", "evidence")},
                "approval_binding_sha256": row["binding"]}
    events = [dict(e) for e in store.db.execute("SELECT * FROM events WHERE release_id=? ORDER BY sequence", (release_id,))]
    output = Path(directory) / release_id
    output.mkdir(parents=True, exist_ok=True)
    (output / "artifact.sql").write_bytes(row["sql"])
    (output / "result.json").write_text(json.dumps(metadata, indent=2) + "\n")
    (output / "events.json").write_text(json.dumps(events, indent=2) + "\n")
    escaped = html.escape
    table = "".join("<tr><th>" + escaped(k) + "</th><td><pre>" + escaped(canonical(v)) + "</pre></td></tr>"
                    for k, v in metadata.items() if k != "evidence")
    document = ('<!doctype html><html lang="en"><meta charset="utf-8">'
                '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'">'
                '<title>Oracle POC review and result</title><style>body{font:16px system-ui;max-width:1100px;margin:2em auto}'
                'pre{white-space:pre-wrap;overflow-wrap:anywhere}th{text-align:left}td,th{vertical-align:top;padding:.5em}</style>'
                '<h1>' + escaped(release_id) + '</h1><table>' + table + '</table><h2>Exact SQL</h2><pre>'
                + escaped(row["sql"].decode("utf-8")) + '</pre><h2>Evidence</h2><pre>'
                + escaped(json.dumps(row["evidence"], indent=2)) + '</pre><p><a href="artifact.sql">SQL bytes</a> · '
                '<a href="result.json">Result JSON</a> · <a href="events.json">Audit events</a></p></html>')
    (output / "index.html").write_text(document)
    return metadata
