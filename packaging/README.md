# packaging/

Everything that turns the Python application into something a visitor can
download and double-click. One directory per operating system, each with a
single build script that produces exactly one release asset.

| OS      | Script                                                | Produces                                |
| ------- | ----------------------------------------------------- | --------------------------------------- |
| Windows | [`windows/build.ps1`](windows/build.ps1)              | `PersonalChappie-Setup-x64.exe`          |
| macOS   | [`macos/build.sh`](macos/build.sh)                    | `PersonalChappie-macOS-<arm64\|x64>.dmg` |
| Linux   | [`linux/build.sh`](linux/build.sh)                    | `PersonalChappie-Linux-x86_64.AppImage`  |

Each script writes into `dist/installers/`, prints the artifact path, and exits
non-zero on any failure. `.github/workflows/desktop-installers.yml` runs these
same three scripts, then publishes them plus `installers-SHA256SUMS.txt` to the
GitHub Release for the tag.

Shared pieces that are not per-OS:

- **`../chappie.spec`** - the PyInstaller build every script starts from. One
  `onedir` bundle with two executables: the windowed launcher
  (`PersonalChappie`) and the console CLI (`chappie`).
- **`pyinstaller_rthook_frozen.py`** - runtime hook that points a frozen
  install's `chappie.toml` and data directory at the per-user application
  directory, so an upgrade cannot overwrite settings and an uninstall cannot
  delete the user's memory.
- **`pyinstaller_hooks/`** - overrides for third-party PyInstaller hooks that
  are wrong for this project's dependency set.

Per-OS notes live next to each script: [`windows/`](windows),
[`macos/`](macos), [`linux/`](linux). The full maintainer walkthrough -
building, signing, releasing, and how the in-app updater consumes the result -
is [`docs/desktop-installers.md`](../docs/desktop-installers.md).
