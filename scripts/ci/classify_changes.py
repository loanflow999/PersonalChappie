#!/usr/bin/env python3
"""Classify a change set into CI lanes (the orchestrator's ``detect`` job).

Reads newline-separated changed paths (repo-relative, forward slashes) from
stdin or ``--files-from``, decides which CI lanes the change can affect, and
writes ``lane=true|false`` lines to ``$GITHUB_OUTPUT`` (and stdout).

Contract — FAIL OPEN, never closed. A lane may run without need; it must
never be skipped when the change could break it:

* ``--full`` (push to main, nightly, release, manual dispatch) or an EMPTY
  change set turns every lane on. An empty set means the diff could not be
  computed, never "nothing changed".
* A change under ``.github/`` or ``scripts/ci/`` turns every lane on: it
  rewires the pipeline itself.
* ``python`` is a DENYLIST: it is off only when every path is provably
  outside what the test suite reads. Tests read docs/, the frontend source,
  install/ and assets/, so those keep it on.

Outputs beyond the lanes:

* ``full``           — every lane forced on (the caller also widens matrices).
* ``changed_count``  — number of changed paths (0 = unknown).

Usage::

    git diff --name-only BASE HEAD | python scripts/ci/classify_changes.py
    python scripts/ci/classify_changes.py --full
"""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Iterable
from pathlib import Path

# Trees the Python suite never reads (verified by grepping tests/ for each).
# Everything NOT listed keeps the python lane on — unknown means relevant.
_PY_IRRELEVANT_PREFIXES = (
    "wiki-video/",
    "homebrew-tap/",
    "scoop-bucket/",
    "board-backend/",
    "qa/",
    "skillbook/",
    "keyproxy/",
    ".github/ISSUE_TEMPLATE/",
)
_PY_IRRELEVANT_FILES = {
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/dependabot.yml",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
}

_PIPELINE_PREFIXES = (".github/workflows/", ".github/actions/", "scripts/ci/")

_FRONTEND_PREFIXES = ("chappie/ui/web/frontend/",)
_FRONTEND_FILES = {"scripts/ci/check_frontend_bundle_budget.py"}

_DEPS_FILES = {
    "pyproject.toml",
    "requirements.in",
    "requirements.txt",
    "uv.lock",
    "packaging/native-crypto.json",
    "packaging/native-crypto-uv.toml",
    "chappie/assets/browser/pyproject.toml",
    "chappie/assets/browser/requirements.in",
    "chappie/assets/browser/requirements.lock",
    "scripts/native_crypto_index.py",
    "scripts/pip_install.py",
    "scripts/build_native_crypto.py",
    "tests/contract/test_native_crypto.py",
    "tests/contract/test_native_ssh.py",
    "chappie/computers/ssh_packet_guard.py",
}

_REALTIME_PREFIXES = (
    "chappie/realtime/",
    "chappie/plugins/realtime/",
    "chappie/audio/",
    "chappie/speech/",
    "chappie/live/",
    "chappie/core/",
    "tests/contract/test_realtime",
    "tests/contract/test_gpt_live",
)
_REALTIME_FILES = {"scripts/realtime_reliability_gate.py"} | _DEPS_FILES

_CLI_PREFIXES = ("chappie/cli_ctl/", "chappie/commands/", "tests/unit/cli_ctl/")

_DRAGDROP_FILES = {
    "chappie/overlay/drop_target.py",
    "chappie/overlay/drop_bridge.py",
    "scripts/crossplatform/verify_drop_target.py",
}

_BROWSER_PREFIXES = (
    "chappie/society/browser/",
    "tests/contract/test_browser",
    "tests/unit/society/test_browser",
)
_BROWSER_FILES = {
    "chappie/ui/web/society_browser_routes.py",
    "chappie/ui/web/mcp_server_routes.py",
    "chappie/agent_chat/runner_cli.py",
    "chappie/brain/tool_gateway.py",
    "chappie/society/approvals.py",
}

# Native macOS surface: permissions, bundle, autostart, Computer-Use. The old
# standalone workflow also matched all of tests/** and chappie/ui/**, which put
# three 45-minute macOS jobs behind nearly every PR; the lane keeps the
# platform code and the exact test files that job runs.
#
# The just-in-time permission service is called from many consumers, so the
# lane also covers every directory that asks for, or acts on, a macOS
# permission: capture and speech (chappie/audio/), computer use (chappie/cu/),
# screenshots (chappie/vision/, chappie/screen_context/), dictation
# (chappie/dictation/), global shortcuts (chappie/trigger/, which includes
# chappie/trigger/backends/) and the permission port, the service and window
# control (chappie/platform/: permissions.py, permission_service.py,
# window_state.py). Packaging is covered too: the spec, packaging/macos/ and the
# single usage-string table both bundles load. The tool plugins that capture or
# type (screenshot, type_text, verify_localhost), the appshot gesture, the speech
# diagnosis, the screen-context routes, the CLI relay and the bundle-id constants
# are consumers too and are listed by file.
_MACOS_PREFIXES = (
    "install/",
    "chappie/admin/",
    "chappie/appshot/",
    "chappie/audio/",
    "chappie/autostart/",
    "chappie/cu/",
    "chappie/dictation/",
    "chappie/platform/",
    "chappie/screen_context/",
    "chappie/setup/",
    "chappie/trigger/",
    "chappie/vision/",
    "chappie/ui/desktop",
    "packaging/macos/",
    "tests/unit/platform/",
    "tests/unit/audio/",
    "tests/unit/autostart/",
    "tests/unit/cu/",
    "tests/unit/setup/",
    "tests/unit/trigger/",
    "tests/unit/ui/web/test_permissions_",
    "tests/unit/vision/",
)
_MACOS_FILES = {
    "pyproject.toml",
    "uv.lock",
    ".githooks/pre-push",
    "chappie.spec",
    "chappie/core/macos_privacy_strings.py",
    "chappie/core/branding.py",
    "chappie/core/events.py",
    "chappie/core/protocols.py",
    "chappie/cli_ctl/commands/permissions.py",
    "chappie/plugins/harness/computer_use.py",
    "chappie/plugins/tool/screen_snapshot.py",
    "chappie/plugins/tool/type_text.py",
    "chappie/plugins/tool/verify_localhost.py",
    "chappie/speech/diagnose.py",
    "chappie/speech/pipeline.py",
    "chappie/tasks/event_catalog.py",
    "chappie/ui/web/permissions_routes.py",
    "chappie/ui/web/screen_context_routes.py",
    "chappie/ui/web/settings_routes.py",
    "tests/contract/test_permission_service_contract.py",
    "tests/fakes/fake_permission_service.py",
    "tests/fakes/fake_tcc.py",
    "tests/unit/ci/test_check_frozen_macos_app.py",
    "tests/unit/ci/test_macos_desktop_permission_step.py",
    "tests/unit/ui/web/test_keybinds_input_monitoring_ask.py",
    "tests/unit/core/test_permission_events.py",
    "scripts/measure_boot.py",
    "scripts/measure_desktop_boot.py",
}

# Installer smoke: the raw install path a downloader runs.
_INSTALLER_PREFIXES = ("install/",)
_INSTALLER_FILES = {
    "pyproject.toml",
    "requirements.txt",
    "chappie/__main__.py",
    "chappie/setup/prefetch.py",
    "chappie/setup/model_report.py",
    "chappie/speech/wake_model_fetch.py",
    "tests/unit/install/test_install_sh_stage1.py",
    ".github/workflows/sign-installer.yml",
}

# In-app updater: status, download + verify, native handover, the restart
# helper that finishes it, and the installer scripts it hands over to. Each
# OS replaces a running app differently, so this lane runs on all three.
_UPDATER_PREFIXES = (
    "chappie/core/installer_update",
    "chappie/core/frozen",
    "chappie/ui/relauncher",
    "chappie/ui/web/update_routes",
    "packaging/",
    "tests/fakes/fake_installer_update",
    "tests/integration/test_update_",
    "tests/unit/core/test_installer_update",
    "tests/unit/install/test_installer_update",
    "tests/unit/ui/test_relauncher",
    "tests/unit/ui/web/test_launcher_update_handoff",
    "tests/unit/ui/web/test_update_routes",
    "tests/unit/web/test_update_",
)
_UPDATER_FILES = {
    "chappie/__main__.py",
    "chappie/ui/desktop_app.py",
    "chappie/ui/web/launcher.py",
    "chappie/ui/web/settings_routes.py",
    ".github/workflows/desktop-installers.yml",
} | _DEPS_FILES

LANES = (
    "python",
    "frontend",
    "deps",
    "realtime",
    "cli",
    "dragdrop",
    "browser",
    "macos_desktop",
    "installer",
    "updater",
)


def _normalize(paths: Iterable[str]) -> list[str]:
    out: list[str] = []
    for raw in paths:
        path = raw.strip().replace("\\", "/")
        if path.startswith("./"):
            path = path[2:]
        if path:
            out.append(path)
    return out


def _any(paths: list[str], prefixes: tuple[str, ...] = (), files: set[str] | None = None) -> bool:
    files = files or set()
    return any(p.startswith(prefixes) or p in files for p in paths)


def _python_relevant(path: str) -> bool:
    return not (path.startswith(_PY_IRRELEVANT_PREFIXES) or path in _PY_IRRELEVANT_FILES)


def classify(paths: Iterable[str], *, full: bool = False) -> dict[str, bool]:
    """Return ``{lane: bool}`` plus ``full`` for a change set."""
    changed = _normalize(paths)
    force = full or not changed or _any(changed, _PIPELINE_PREFIXES)
    if force:
        result = {lane: True for lane in LANES}
        result["full"] = True
        return result
    return {
        "python": any(_python_relevant(p) for p in changed),
        "frontend": _any(changed, _FRONTEND_PREFIXES, _FRONTEND_FILES),
        "deps": _any(changed, (), _DEPS_FILES),
        "realtime": _any(changed, _REALTIME_PREFIXES, _REALTIME_FILES),
        "cli": _any(changed, _CLI_PREFIXES)
        or any(p.startswith("chappie/ui/web/") and p.endswith("_routes.py") for p in changed),
        "dragdrop": _any(changed, (), _DRAGDROP_FILES),
        "browser": _any(changed, _BROWSER_PREFIXES, _BROWSER_FILES),
        "macos_desktop": _any(changed, _MACOS_PREFIXES, _MACOS_FILES),
        "installer": _any(changed, _INSTALLER_PREFIXES, _INSTALLER_FILES),
        "updater": _any(changed, _UPDATER_PREFIXES, _UPDATER_FILES),
        "full": False,
    }


def _emit(result: dict[str, bool], changed_count: int) -> list[str]:
    lines = [f"{key}={'true' if value else 'false'}" for key, value in result.items()]
    lines.append(f"changed_count={changed_count}")
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--full", action="store_true", help="Force every lane on.")
    parser.add_argument("--files-from", type=Path, help="Read paths from this file, not stdin.")
    args = parser.parse_args(argv)

    if args.full:
        paths: list[str] = []
    elif args.files_from:
        paths = args.files_from.read_text(encoding="utf-8").splitlines()
    else:
        paths = [] if sys.stdin is None or sys.stdin.isatty() else sys.stdin.read().splitlines()
    changed = _normalize(paths)
    result = classify(changed, full=args.full)
    lines = _emit(result, len(changed))

    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
