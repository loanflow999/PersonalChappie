# chappiectl — Chappie Control CLI

`chappiectl` drives a **running** Personal Chappie instance from the terminal,
the way `gcloud` drives Google Cloud. It is a thin HTTP client over the REST
API and works on Windows, macOS, and Linux.

## Install
It ships with Chappie. Activate the console script once:
```bash
pip install -e . --no-deps
chappiectl version
```

## Connect
- **Desktop (same machine):** zero config — defaults to `http://127.0.0.1:47821`
  and reads the local control key automatically.
- **Remote VPS:** `chappiectl auth login --url https://host:port --key jctl_…`
  (the key is the one from the server's Control API; on a VPS the key is the
  security boundary). Or set `CHAPPIECTL_BASE_URL` / `CHAPPIECTL_CONTROL_KEY`.

## Core commands
```bash
chappiectl system status                 # is the server reachable?
chappiectl system restart                # deterministic app restart
chappiectl tasks list --state scheduled
chappiectl tasks get <id>
chappiectl tasks create --json-body '{"title":"remind",
  "trigger":{"type":"after_delay","delay_seconds":60},
  "action":{"kind":"speak","text":"stand up"}}'
chappiectl tasks cancel <id>
```

## Every endpoint (auto-layer)
`chappiectl api <tag> <operation>` exposes **every** server endpoint, generated
live from the OpenAPI schema — new server features appear here automatically.
```bash
chappiectl api --help
chappiectl refresh        # force re-read the schema
```

## Output
Add `--json` before any command for machine-readable output:
`chappiectl --json tasks list`.

## Shell completion
`chappiectl --install-completion` (bash/zsh/fish/PowerShell).

## Known boundary
Against a remote VPS, v1 reliably drives the Bearer-gated `/api/control/*`
surface; same-origin UI routes (`/api/tasks/*`, `/api/settings/*`) are intended
for loopback — reach them remotely via an SSH tunnel until they are key-gated
server-side.
