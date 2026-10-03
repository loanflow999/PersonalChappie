"""Freeze the persistent product identity values used by existing installs."""

from __future__ import annotations

import importlib
import os

import pytest

import chappie.core.branding as branding

_CURRENT_IDENTITY = {
    "PRODUCT_NAME": "Personal Chappie",
    "PRODUCT_COMPACT_NAME": "PersonalChappie",
    "PRODUCT_SLUG": "personal-chappie",
    "CONFIG_FILE_NAME": "chappie.toml",
    "KEYRING_SERVICE_NAME": "personal-chappie",
    "CONTROL_KEY_PREFIX": "jctl_",
    "SESSION_COOKIE_NAME": "chappie_session",
    "MANAGED_INSTALL_MARKER": ".chappie-managed-install",
    "DEFAULT_INSTALL_DIR_NAME": ".personal-chappie",
    "WINDOWS_USER_DATA_DIR_NAME": "Chappie",
    "FALLBACK_USER_DATA_DIR_NAME": ".chappie",
    "DESKTOP_OUTPUT_MIRROR_DIR_NAME": "Chappie-Output",
    "WINDOWS_MUTEX_NAME": r"Global\PersonalChappie_v1",
    "WINDOWS_APP_USER_MODEL_ID": "PersonalChappie.PersonalChappie",
    "WINDOWS_UNINSTALL_REGISTRY_SUBKEY": (
        r"Software\Microsoft\Windows\CurrentVersion\Uninstall\PersonalChappie"
    ),
    "WINDOWS_AUTOSTART_TASK_NAME": "Personal Chappie Autostart",
    "WINDOWS_SHORTCUT_FILE_NAME": "Personal Chappie.lnk",
    "WINDOWS_AUTOSTART_DESCRIPTION": "Personal Chappie (Autostart)",
    "WINDOWS_BRANDED_LAUNCHER_FILE_NAME": "PersonalChappie.exe",
    "WINDOWS_BRANDED_LAUNCHER_DIR_NAME": "PersonalChappie",
    "WINDOWS_BRANDED_LAUNCH_ENV_VAR": "CHAPPIE_BRANDED_LAUNCH",
    "MACOS_APP_NAME": "Personal Chappie",
    "MACOS_APP_DIR_NAME": "Personal Chappie.app",
    "MACOS_EXECUTABLE_NAME": "PersonalChappie",
    "MACOS_BUNDLE_ID": "com.personal-chappie.desktop",
    "MACOS_DMG_BUNDLE_ID": "ai.personalchappie.desktop",
    "MACOS_AUTOSTART_LABEL": "com.personal-chappie.autostart",
    "LINUX_APP_NAME": "Personal Chappie",
    "LINUX_DESKTOP_ENTRY_FILE_NAME": "personal-chappie.desktop",
    "LINUX_WM_CLASS": "personal-chappie",
    "DEFAULT_OFFICIAL_REPO_SLUG": "PersonalChappie/PersonalChappie",
    "OFFICIAL_REPO_SLUG_ENV_VAR": "CHAPPIE_OFFICIAL_REPO_SLUG",
    "OFFICIAL_REPO_SLUG": "PersonalChappie/PersonalChappie",
    "OFFICIAL_REPO_URL": "https://github.com/PersonalChappie/PersonalChappie",
    "OFFICIAL_REPO_GIT_URL": "https://github.com/PersonalChappie/PersonalChappie.git",
    "OFFICIAL_RELEASES_LATEST_API_URL": (
        "https://api.github.com/repos/PersonalChappie/PersonalChappie/releases/latest"
    ),
    "UPDATER_USER_AGENT": "PersonalChappie-Updater",
}


def test_default_exported_identity_values_are_frozen() -> None:
    previous = os.environ.pop(branding.OFFICIAL_REPO_SLUG_ENV_VAR, None)
    try:
        module = importlib.reload(branding)
        actual = {name: getattr(module, name) for name in _CURRENT_IDENTITY}
        assert actual == _CURRENT_IDENTITY
    finally:
        if previous is not None:
            os.environ[branding.OFFICIAL_REPO_SLUG_ENV_VAR] = previous
        importlib.reload(branding)


def test_official_repo_slug_override_is_exact() -> None:
    assert (
        branding.resolve_official_repo_slug(
            {"CHAPPIE_OFFICIAL_REPO_SLUG": "RenamedOrg/RenamedRepo"}
        )
        == "RenamedOrg/RenamedRepo"
    )


@pytest.mark.parametrize(
    "value",
    [
        "owner",
        "owner/repo/extra",
        "/repo",
        "owner/",
        "owner/repo evil",
        " owner/repo",
        "owner/repo ",
    ],
)
def test_official_repo_slug_override_rejects_non_exact_values(value: str) -> None:
    with pytest.raises(ValueError, match="exact owner/repository slug"):
        branding.resolve_official_repo_slug({"CHAPPIE_OFFICIAL_REPO_SLUG": value})
