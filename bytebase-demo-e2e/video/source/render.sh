#!/usr/bin/env bash
set -euo pipefail
SOURCE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/bytebase-video-tools"
if [[ ! -x "$TOOLS_DIR/venv/bin/python" ]]; then
  python3 -m venv "$TOOLS_DIR/venv"
fi
PIP_DISABLE_PIP_VERSION_CHECK=1 "$TOOLS_DIR/venv/bin/python" -m pip install -q -r "$SOURCE_DIR/requirements.txt"
exec "$TOOLS_DIR/venv/bin/python" "$SOURCE_DIR/render.py" "$@"
