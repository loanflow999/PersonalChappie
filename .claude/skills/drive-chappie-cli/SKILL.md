---
name: drive-chappie-cli
description: >-
  Use when you (a Claude Code / Codex session, or any terminal agent) need to
  control a running Personal Chappie instance — switch the brain provider, dispatch
  or inspect missions, read/write config, search the wiki, manage skills, browse
  outputs, etc. Teaches the `chappie` CLI: zero-config local auth, machine-readable
  output, and the safety flags. Trigger phrases: "control Chappie", "drive Chappie
  from the CLI", "switch Chappie's brain provider", "dispatch a Chappie mission".
---

# Drive Chappie from the CLI

Chappie exposes its entire WebUI action surface as a command-line tool, the same
way `gcloud` / `aws` exposes a cloud platform. You drive a **running** Chappie over
HTTP — no need to be inside the app.

## Setup (one time)

The CLI ships with the package, so after `pip install -e .` the `chappie` binary is
on PATH (aliases: `chappiectl`, `jctl`). Check it:

```bash
chappie version
```

**Auth is zero-config on the same machine as a running Chappie.** The desktop app
writes its live port + control token to a single-instance session file; the CLI
discovers it automatically, and falls back to the machine's control key. You do
not need to log in. Confirm reachability:

```bash
chappie system status        # {"reachable": true} when Chappie is running
```

For a **remote** Chappie (e.g. a VPS), tunnel it to loopback and point the CLI at it:

```bash
ssh -L 47821:127.0.0.1:47821 <host>          # then it behaves like local
# or, explicitly, per call:
chappie --url http://127.0.0.1:47821 --key "$JCTL" missions list
```

## How to use it (agent ergonomics)

- **Discover commands**: `chappie --help`, `chappie <group> --help`. Every mounted
  REST endpoint is also reachable generically via `chappie api <tag> <op> --help`.
- **Machine-readable output**: put `--json` *before* the group, e.g.
  `chappie --json missions list`. Parse that, not the human table.
- **Preview before acting**: `--dry-run` on any command prints the exact request
  (method, path, body, whether auth is attached) and sends nothing.
- **Authorize destructive actions**: reversible actions (switch provider, set
  language, enable a skill) just run. Destructive ones (any `DELETE`, `config
  set`, `missions dispatch`, `telephony outbound`) refuse unless you pass `--yes`
  (or set `CHAPPIE_CLI_ASSUME_YES=1`). This is deliberate — only add `--yes` when
  you mean it.
- **Never** pass a secret as an inline argument; `auth login` and PAT connects
  read it from a hidden prompt or stdin (`--key -`).

## Common tasks

```bash
# Switch the active brain provider (the flagship; reversible)
chappie brain switch openai
chappie brain subagent-switch openai          # switch the worker/sub-agent provider
chappie --json brain status                   # which provider is active

# Config (atomic write pipeline; `set` is destructive)
chappie --json config get brain.primary
chappie config set ui.theme dark --yes
chappie config language set en

# Missions (dispatch is destructive — spawns a worker)
chappie --json missions list --state RUNNING
chappie missions dispatch "summarize today's PRs" --yes
chappie --json missions show <id>

# Knowledge + history + outputs
chappie --json wiki recall "insurance policy"
chappie --json sessions list
chappie --json outputs list

# Skills, board, workflows, mcps, docs, … (every domain has a group)
chappie --json skills list
chappie --json board summary
chappie api --help                            # the full auto-generated surface
```

## Rules

- Read with `--json` and parse; act with explicit intent.
- `--dry-run` first when unsure what a destructive command will send.
- If `chappie system status` reports unreachable, Chappie is not running — start it
  (`chappie serve` for headless) rather than retrying blindly.
