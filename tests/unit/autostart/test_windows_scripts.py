"""WindowsAutostart PowerShell-script assembly (pure → CI-provable anywhere).

The actual .lnk creation/read-back needs a real Windows host + WScript.Shell and
is covered by live sign-off; here we prove the script we *would* run is correct.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from chappie.autostart.protocol import LaunchSpec
from chappie.autostart.windows import (
    _icon_matches,
    build_create_script,
    build_read_script,
)


def _spec(minimized: bool = True) -> LaunchSpec:
    return LaunchSpec(
        program=r"C:\Python\pythonw.exe",
        args=("-m", "chappie.ui.web.launcher"),
        working_dir=r"C:\Users\u\Personal Chappie",
        minimized=minimized,
    )


def test_create_script_sets_target_args_workdir() -> None:
    script = build_create_script(Path(r"C:\startup\Personal Chappie.lnk"), _spec())
    assert r"$sc.TargetPath = 'C:\Python\pythonw.exe'" in script
    assert "$sc.Arguments = '-m chappie.ui.web.launcher'" in script
    assert r"$sc.WorkingDirectory = 'C:\Users\u\Personal Chappie'" in script
    assert "$sc.Save()" in script


def test_minimized_maps_to_windowstyle_7() -> None:
    assert "$sc.WindowStyle = 7" in build_create_script(Path("x.lnk"), _spec(minimized=True))


def test_non_minimized_maps_to_windowstyle_1() -> None:
    assert "$sc.WindowStyle = 1" in build_create_script(Path("x.lnk"), _spec(minimized=False))


def test_read_script_emits_four_sentinel_lines() -> None:
    script = build_read_script(Path(r"C:\startup\Personal Chappie.lnk"))
    assert script.count("Write-Output") == 4
    assert "$sc.TargetPath" in script
    assert "$sc.Arguments" in script
    assert "$sc.WorkingDirectory" in script
    assert "$sc.IconLocation" in script


def test_read_script_reads_the_icon_back() -> None:
    """The icon is the field that goes stale on its own.

    A shortcut written from one checkout keeps pointing its icon there long
    after target, arguments and working directory have moved elsewhere. Windows
    draws the taskbar button from this shortcut, so without reading the icon
    back the app shows artwork from a directory nobody uses any more, forever.
    """
    assert "$sc.IconLocation" in build_read_script(Path(r"C:\s\a.lnk"))


@pytest.mark.parametrize(
    ("actual", "expected", "matches"),
    [
        (r"C:\app\chappie.ico,0", r"C:\app\chappie.ico", True),
        (r"c:\APP\chappie.ico,0", r"C:\app\chappie.ico", True),  # Windows is case-blind
        (r"C:\old-worktree\chappie.ico,0", r"C:\app\chappie.ico", False),
        (",0", r"C:\app\chappie.ico", False),  # empty == inherit pythonw's logo
        ("", r"C:\app\chappie.ico", False),
        (r"C:\anything\chappie.ico,0", None, True),  # unresolvable → leave it alone
    ],
)
def test_icon_matches(actual: str, expected: str | None, matches: bool) -> None:
    assert _icon_matches(actual, expected) is matches


def test_create_script_embeds_icon_when_given() -> None:
    """The autostart .lnk must carry the Chappie icon so the taskbar button is
    branded from first paint — not the bare pythonw.exe Python logo."""
    ico = r"C:\Users\u\Personal Chappie\chappie\assets\icons\chappie.ico"
    script = build_create_script(Path(r"C:\startup\Personal Chappie.lnk"), _spec(), icon=ico)
    assert f"$sc.IconLocation = '{ico},0'" in script


def test_create_script_omits_icon_line_without_icon() -> None:
    """Back-compat: no icon given → no IconLocation line (never an empty ',0')."""
    script = build_create_script(Path(r"C:\startup\Personal Chappie.lnk"), _spec())
    assert "IconLocation" not in script


# --------------------------------------------------------------------------- #
# Apostrophes in paths (a login like O'Brien, a folder like "Ruben's Chappie")  #
# --------------------------------------------------------------------------- #

_APOSTROPHE_SPEC = LaunchSpec(
    program=r"C:\Users\O'Brien\.venv\Scripts\pythonw.exe",
    args=("-m", "chappie.ui.web.launcher"),
    working_dir=r"C:\Users\O'Brien\Ruben's Chappie",
)


def _quotes_balanced(script: str) -> bool:
    """Every line closes each single-quoted literal it opens."""
    return all(line.count("'") % 2 == 0 for line in script.splitlines())


def test_create_script_escapes_apostrophes_in_paths() -> None:
    # An unescaped apostrophe terminates the single-quoted PowerShell literal
    # early, so the whole script fails to parse and autostart silently never
    # installs for that user.
    script = build_create_script(
        Path(r"C:\Users\O'Brien\Startup\Personal Chappie.lnk"),
        _APOSTROPHE_SPEC,
        icon=r"C:\Users\O'Brien\chappie.ico",
    )
    assert r"$sc.TargetPath = 'C:\Users\O''Brien\.venv\Scripts\pythonw.exe'" in script
    assert r"Ruben''s Chappie" in script
    assert r"$sc.IconLocation = 'C:\Users\O''Brien\chappie.ico,0'" in script
    assert _quotes_balanced(script)


def test_read_script_escapes_apostrophes_in_the_link_path() -> None:
    script = build_read_script(Path(r"C:\Users\O'Brien\Startup\Personal Chappie.lnk"))
    assert r"O''Brien" in script
    assert _quotes_balanced(script)
