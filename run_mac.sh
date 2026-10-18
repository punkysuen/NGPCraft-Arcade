#!/usr/bin/env bash
# Launch NgpCraft on macOS (uses project venv).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  .venv/bin/pip install -r requirements.txt
fi
# If Qt fails with "Could not find the Qt platform plugin cocoa", reinstall PyQt6:
#   .venv/bin/pip install --force-reinstall PyQt6 PyQt6-Qt6 PyQt6-sip
exec .venv/bin/python3 ngpc_shell.py "$@"
