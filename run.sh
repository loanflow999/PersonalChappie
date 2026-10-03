#!/usr/bin/env sh
# Personal Chappie - POSIX launcher (macOS + Linux). Parity twin of run.bat.
#
# Usage: ./run.sh [--debug|--headless|--dev]
#   --debug     verbose logging, foreground console
#   --headless  API/WS backend only, no desktop window or voice
#   --dev       frontend served from the Vite dev server (port 5173)
#
# Runs in the foreground (Ctrl+C stops Chappie); append `&` to detach.
set -u
cd "$(dirname "$0")" || exit 1

# Activate the project venv when present (mirrors run.bat).
if [ -f ".venv/bin/activate" ]; then
    # shellcheck disable=SC1091
    . ".venv/bin/activate"
fi

# Pick the interpreter - Debian/Ubuntu ship python3 without a python alias.
if command -v python >/dev/null 2>&1; then
    PY=python
elif command -v python3 >/dev/null 2>&1; then
    PY=python3
else
    echo "error: no Python interpreter found on PATH" >&2
    exit 1
fi

# Pre-boot drift check (optional, needs PowerShell 7+). Mirrors run.bat:
# always continues on failure, never blocks boot, skipped without pwsh.
if [ -f "scripts/check-working-tree.ps1" ] && command -v pwsh >/dev/null 2>&1; then
    pwsh -NoProfile -File "scripts/check-working-tree.ps1" || true
fi

case "${1:-}" in
    --debug)
        # --debug is launcher-local: visible console + verbose logging.
        # Forwarding it to the launcher would trip argparse (see run.bat).
        CHAPPIE_DEBUG=1 exec "$PY" -m chappie.ui.web.launcher
        ;;
    --headless)
        exec "$PY" -m chappie.ui.web.launcher --headless
        ;;
    --dev)
        CHAPPIE_DEV=1 exec "$PY" -m chappie.ui.web.launcher --dev
        ;;
    *)
        exec "$PY" -m chappie.ui.web.launcher
        ;;
esac
