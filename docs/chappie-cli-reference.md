# Chappie CLI — Command Reference

_Generated from the curated command tree by `scripts/ci/gen_cli_reference.py` — do not edit by hand. Every mounted REST endpoint is additionally reachable via `chappie api <tag> <op>`._

## auth

- `chappie auth login --url --key` — Verify the key against the server and persist it for future calls.
- `chappie auth logout` — Forget the saved credentials.
- `chappie auth status --url --key` — Report whether the configured (or given) target is reachable.

## board

- `chappie board achievements` — Show unlocked + locked achievements.
- `chappie board bio` — Show the AI-generated bio.
- `chappie board bio-regenerate --yes --dry-run` — Regenerate the AI bio.
- `chappie board heatmap --days` — Show the activity heatmap cells.
- `chappie board profile` — Show the profile (meta + people + review count).
- `chappie board records` — Show personal records.
- `chappie board summary --window-days` — Show personal totals + streaks over a window.

## brain

- `chappie brain deep-model <model> --persist --yes --dry-run` — Set the mission worker's deep model.
- `chappie brain list` — List configured brain providers (alias of status).
- `chappie brain status` — Show configured providers and which one is active.
- `chappie brain subagent-switch <provider> --persist --yes --dry-run` — Switch the mission-worker provider (e.g. Codex -> OpenAI).
- `chappie brain switch <provider> --persist --yes --dry-run` — Switch the ACTIVE main brain provider (e.g. `chappie brain switch openai`).
- `chappie brain test <provider> --dry-run` — Test connectivity + auth for a provider.

## clis

- `chappie clis check <name> --yes --dry-run` — Probe a CLI's binary + auth (refreshes its status).
- `chappie clis connect <name> --json-body --yes --dry-run` — Connect a CLI's auth (oauth_cli flow or api_key).
- `chappie clis disconnect <name> --yes --dry-run` — Remove a CLI's stored auth credentials.
- `chappie clis install <name> --method --yes --dry-run` — Start an install job for a CLI (output streams in the desktop view).
- `chappie clis list` — List all CLIs with status (connected, installed, version, 7-day usage).
- `chappie clis show <name>` — Show one CLI (homepage, install methods, auth mode, secrets set).
- `chappie clis usage <name>` — Show a CLI's recent usage history.
- `chappie clis usage-stats <name>` — Show a CLI's aggregated usage stats (success rate, avg duration, top commands).

## commands

- `chappie commands list` — List every registry command (id, endpoint, params, danger, UI section).
- `chappie commands show <command_id>` — Show one command's full definition (params schema, voice aliases).

## computer-use

- `chappie computer-use cancel <mission_id> --yes --dry-run` — Cancel one active run.
- `chappie computer-use cancel-all --yes --dry-run` — Cancel every active run (queued and running).
- `chappie computer-use list --limit` — List active and recent Computer-Use runs.
- `chappie computer-use show <mission_id>` — Show one run: status, goal, exit code, final output.
- `chappie computer-use start <goal> --timeout-s --yes --dry-run` — Start a desktop goal in the background; prints the mission id.

## conductor

- `chappie conductor add --def --yes --dry-run` — Add a job from a Job JSON document.
- `chappie conductor delete <job_id> --yes --dry-run` — Delete a job.
- `chappie conductor list` — List Conductor jobs + a run summary.
- `chappie conductor run <job_id> --yes --dry-run` — Manually trigger a job run.
- `chappie conductor show <job_id>` — Show one job + recent runs.
- `chappie conductor toggle <job_id> --enabled --yes --dry-run` — Enable or disable a job.

## config

- `chappie config get <path>` — Get a config value by dotted path (control-key gated).
- `chappie config language get` — Show the current reply language + the available options.
- `chappie config language set <lang> --persist --yes --dry-run` — Set the reply language (hot-reloads, no restart).
- `chappie config list` — List the mutable-settings allowlist (path, risk tier, restart needed).
- `chappie config set <path> <value> --reason --yes --dry-run` — Set a mutable config value via the atomic write pipeline (destructive: --yes).

## contacts

- `chappie contacts add --name --alias --relationship --email --phone --url --tag --organization --role --birthday --note --favorite --json-body --yes --dry-run` — Add a contact (field flags, or --json-body for the full record).
- `chappie contacts delete <slug> --yes --dry-run` — Delete a contact.
- `chappie contacts edit <slug> --name --alias --relationship --email --phone --url --tag --organization --role --birthday --note --favorite --json-body --yes --dry-run` — Edit a contact — only the given flags change (partial PATCH).
- `chappie contacts export --out` — Export all contacts as vCard 3.0 (.vcf).
- `chappie contacts import <file> --yes --dry-run` — Import contacts from a vCard file (merges, never clobbers).
- `chappie contacts list` — List contacts.
- `chappie contacts show <slug>` — Show one contact.

## costs

- `chappie costs entries --days --provider --model --role --surface --search --sort --limit --offset` — The individual model calls behind the totals.
- `chappie costs rates --days` — The rate card per model — and which models have no published rate.
- `chappie costs summary --days --provider --model --role --surface --search` — Totals plus the breakdown by provider, model, role, surface and day.

## docs

- `chappie docs list` — List documentation pages.
- `chappie docs search <query>` — Search the docs.
- `chappie docs show <slug>` — Show one doc page's body.
- `chappie docs tree` — Show the Diataxis-grouped doc tree.

## friends

- `chappie friends add --json-body --yes --dry-run` — Add a friend.
- `chappie friends delete <friend_id> --yes --dry-run` — Delete a friend and their channels.
- `chappie friends edit <friend_id> --json-body --yes --dry-run` — Edit a friend (partial).
- `chappie friends list` — List friends with their channels.
- `chappie friends message <friend_id> --text --yes --dry-run` — Send an outbound message to a friend (consequential — needs --yes).
- `chappie friends messages <friend_id>` — Show the message thread with a friend.
- `chappie friends show <friend_id>` — Show one friend (detail + channels + permission profile).

## frontier

- `chappie frontier ack --yes --dry-run` — Acknowledge (dismiss) the pending frontier proposals.
- `chappie frontier pending` — List proposed model upgrades awaiting acknowledgement.

## ide

- `chappie ide archive-terminal <name> --restore --workspace --dry-run` — Hide a coding session from the chat list, or restore it.
- `chappie ide close-terminals <names> --yes --dry-run` — Stop several coding agents and close their terminal panes.
- `chappie ide move-terminal <name> <target_workspace> --workspace --beside --side --dry-run` — Move a terminal pane into another open workspace.
- `chappie ide rename-terminal <name> <new_name> --dry-run` — Rename a running terminal pane without restarting its agent.

## local-models

- `chappie local-models assistant benchmarks --refresh --provider` — Read the benchmark data used by the assistant.
- `chappie local-models assistant diagnose --provider` — Start a guided diagnostic conversation.
- `chappie local-models assistant health --provider` — Read the selected provider's local-model health.
- `chappie local-models assistant session --provider` — Read the existing assistant session and its readiness.
- `chappie local-models assistant setup --provider` — Start the existing guided setup conversation.
- `chappie local-models assistant test --role --provider` — Run the setup test for all roles or the selected roles.
- `chappie local-models catalog recommended --provider` — The curated shortlist ranked for this machine, with its review date.
- `chappie local-models catalog search <query> --sort --capability --limit --provider` — Browse the library; offline is reported as a sentence, not a failure.
- `chappie local-models catalog tags <name> --provider` — Every tag of one library model with size, quantization, context and fit.
- `chappie local-models hf enable <state> --provider --dry-run` — Show or flip the Hugging Face browsing switch.
- `chappie local-models hf files <user> <repo> --provider` — The .gguf files of one repository with quantization, size and fit.
- `chappie local-models hf pull <user> <repo> --quant --provider --dry-run` — Start pulling hf.co/<user>/<repo>[:<quant>] through the normal pull path.
- `chappie local-models hf search <query> --sort --limit --provider` — GGUF repositories on Hugging Face.
- `chappie local-models models delete <name> --reassign --provider --yes --dry-run` — Remove a download from the server (refused while a role still uses it).
- `chappie local-models models list --provider` — Every download with its facts, what is loaded, and the disk total.
- `chappie local-models models show <name> --provider` — One download with the long facts (license, parameters, template).
- `chappie local-models models unload <name> --provider --yes --dry-run` — Free the memory a loaded model holds; the next turn pays the load again.
- `chappie local-models options clear <name> --provider --dry-run` — Drop the profile so the server's defaults apply again.
- `chappie local-models options get <name> --provider` — The profile of one model as configured (empty when none).
- `chappie local-models options set <name> <values> --provider --dry-run` — Replace the profile of a model with the given knobs (whole set).
- `chappie local-models options suggest <name> --provider` — An advisory profile for this machine, with one reason per knob.
- `chappie local-models roles list --provider` — Every role with its pick, what qualifies, and the recommendation.
- `chappie local-models roles set <role> <model> --provider --dry-run` — Assign a model to a role (written through the config writers).
- `chappie local-models server autostart <state> --provider --dry-run` — Show or flip "start the server with Chappie" (fires only while local models are in use).
- `chappie local-models server env-guide --os --provider` — Copyable per-OS commands for the server's environment variables.
- `chappie local-models server log --lines --provider` — The last lines of the server log Chappie writes when it starts the server.
- `chappie local-models server status --provider` — Runtime picture plus what is loaded and how much disk the downloads take.
- `chappie local-models server stop --provider --yes --dry-run` — Stop the server Chappie itself started (never one started elsewhere).
- `chappie local-models server test <base_url> --provider` — Probe a host before saving it: version and latency, or why it failed.
- `chappie local-models server verify --provider` — Prove the setup works: the server, one real chat answer, one real embedding.

## marketplace

- `chappie marketplace browse` — Show everything the community marketplace offers, and what you already have.
- `chappie marketplace connect-pat <plugin_id> --token --yes --dry-run` — Connect a plugin with a personal access token.
- `chappie marketplace connect-poll <plugin_id> <flow_id>` — Poll an in-progress OAuth connect flow.
- `chappie marketplace connect-start <plugin_id> --yes --dry-run` — Begin an OAuth connect flow (prints the redirect URI + flow id).
- `chappie marketplace disconnect <plugin_id> --yes --dry-run` — Disconnect a plugin.
- `chappie marketplace install <item_id> --yes --dry-run` — Install a marketplace entry by name — skill or plugin — and report it.
- `chappie marketplace list` — List marketplace plugins + their connection status.

## mcps

- `chappie mcps check <name> --yes --dry-run` — Health-check an MCP server (lists its tools).
- `chappie mcps delete <name> --yes --dry-run` — Remove an MCP server.
- `chappie mcps disable <name> --yes --dry-run` — Disable an MCP server.
- `chappie mcps enable <name> --yes --dry-run` — Enable an MCP server.
- `chappie mcps import-claude-desktop --yes --dry-run` — Import MCP servers from the Claude Desktop config.
- `chappie mcps list` — List MCP servers + a summary.

## missions

- `chappie missions approve-tool <mission_id> <trace_id> --yes --dry-run` — Approve one paused mission tool call and resume it.
- `chappie missions cancel <mission_id> --yes --dry-run` — Cancel a running mission (kills its worker).
- `chappie missions deny-tool <mission_id> <trace_id> --reason --dry-run` — Deny one paused mission tool call without executing it.
- `chappie missions dispatch <prompt> --language --confirmed --yes --dry-run` — Dispatch a new self-healing mission — spawns a worker (destructive: --yes).
- `chappie missions kill <worker_id> --yes --dry-run` — Hard-kill a worker process by id.
- `chappie missions list --state --limit` — List missions (optionally filtered by state).
- `chappie missions rerun <mission_id> --confirmed --yes --dry-run` — Re-dispatch a terminal mission's prompt as a new linked mission.
- `chappie missions result <mission_id>` — Read a mission's signed outcome and actual deliverable contents.
- `chappie missions show <mission_id>` — Show one mission with its events + verdicts.
- `chappie missions tool-approvals <mission_id>` — List supervisor tool calls waiting for approval in a mission.

## outputs

- `chappie outputs files <slug>` — List the artifacts a mission produced.
- `chappie outputs graph <slug>` — Print a session's mission-map page (self-contained HTML node graph).
- `chappie outputs list` — List output sessions (a mission's deliverable folders).
- `chappie outputs open-with <slug> <path> --opener --yes --dry-run` — Open an artifact with a chosen editor (desktop only).
- `chappie outputs openers` — List installed editors/apps that can open an artifact.
- `chappie outputs plan <slug>` — Show a session's plan + steps.
- `chappie outputs preferred-opener <opener> --yes --dry-run` — Get or set the default artifact opener.

## permissions

- `chappie permissions open-settings <permission_id> --yes --dry-run` — Open the matching macOS privacy pane through LaunchServices.
- `chappie permissions request <permission_id> --yes --dry-run` — Ask macOS for one permission through the same service the app uses.
- `chappie permissions reset <permission_id> --bundle-id --yes --dry-run` — Forget what macOS recorded for Personal Chappie, so it asks again on next use (macOS only).
- `chappie permissions status --include-automation` — Show each macOS privacy permission and what is waiting on one. Never prompts.

## refresh

- `chappie refresh` — Clear the cached API schema (next call re-fetches it).

## sessions

- `chappie sessions command <session_id> <command> --arguments --request-id --yes --dry-run` — Run an explicit command in a Chappie or agent chat.
- `chappie sessions control <session_id>` — Read a chat's current work mode and persistent goal.
- `chappie sessions delete <session_id> --yes --dry-run` — Delete a text conversation thread.
- `chappie sessions latest-turn --session-id` — Show the latest persisted user transcript and its complete turn.
- `chappie sessions list --days --limit` — List text + voice sessions, newest first.
- `chappie sessions resume <kind> <session_id> --yes --dry-run` — Seed the brain from a past conversation to continue it in text.
- `chappie sessions show <kind> <session_id>` — Show one conversation with its messages.
- `chappie sessions speak <kind> <session_id> --yes --dry-run` — Start a voice session seeded from a past conversation (503 on headless).

## skills

- `chappie skills catalog-install <name> --source-url --title --raw-url --yes --dry-run` — Install a skill from the catalog (lands as a draft).
- `chappie skills catalog-search <query>` — Search the installable skill catalog.
- `chappie skills commit --draft --yes --dry-run` — Commit a generated draft to disk (still state=draft until enabled).
- `chappie skills create <intent> --name --trigger --schedule --language --yes --dry-run` — Author AND write a new skill in one step (the voice path's `create-skill`).
- `chappie skills disable <name> --yes --dry-run` — Deactivate a skill.
- `chappie skills draft <intent> --name-hint --category --trigger --schedule --language --yes --dry-run` — Generate a skill draft from an intent WITHOUT writing it (review, then `commit`).
- `chappie skills enable <name> --yes --dry-run` — Activate a skill.
- `chappie skills import <source> --yes --dry-run` — Install a skill from a local folder or a SKILL.md link.
- `chappie skills list` — List all discovered skills.
- `chappie skills reload --yes --dry-run` — Re-scan the skills directory.
- `chappie skills show <name>` — Show one skill's detail.

## socials

- `chappie socials add --json-body --yes --dry-run` — Add a social link.
- `chappie socials delete <social_id> --yes --dry-run` — Delete a social link.
- `chappie socials edit <social_id> --json-body --yes --dry-run` — Edit a social link (partial).
- `chappie socials list` — List social links.

## system

- `chappie system audio-devices --output --input` — List audio devices, or pick where the voice plays / which mic listens.
- `chappie system restart --force --yes --dry-run` — Refuse a CLI restart; use the desktop UI's explicit Restart action.
- `chappie system status` — Report server reachability + version (GET /api/control/auth/probe).

## tasks

- `chappie tasks cancel <task_id> --yes --dry-run` — Soft-cancel a scheduled/running task.
- `chappie tasks create --json-body --yes --dry-run` — Create + schedule a task from a TaskSpec JSON document.
- `chappie tasks delete <task_id> --yes --dry-run` — Hard-delete a task (terminal states only, server-enforced).
- `chappie tasks get <task_id>` — Show one task with its step timeline.
- `chappie tasks list --state --limit` — List tasks (optionally filtered by state).

## telephony

- `chappie telephony config` — Show the telephony config.
- `chappie telephony outbound <to> --message --yes --dry-run` — Place a real outbound call (destructive: costs money; needs --yes).
- `chappie telephony status` — Report telephony availability/status.

## version

- `chappie version` — Print the chappiectl version.

## wiki

- `chappie wiki backfill --days --max-sessions --preview --yes --dry-run` — Backfill recent Realtime sessions through evidence-safe Wiki capture.
- `chappie wiki health` — Show wiki subsystem health: bootstrap, last write, chain failures, backlog (spec A5).
- `chappie wiki ingest <text> --source --dry-run` — Store a fact through the guarded Wiki curator.
- `chappie wiki page <slug>` — Read a wiki page by vault path / slug.
- `chappie wiki recall <query>` — Full-text search the wiki.
- `chappie wiki reindex --preview` — Rebuild the wiki search index from the active vault.
- `chappie wiki tree` — Show the vault folder tree + stats.
- `chappie wiki vaults` — List the user's registered Obsidian vaults (connect picker, spec A6).

## workflows

- `chappie workflows create --def --yes --dry-run` — Create a workflow from a WorkflowDef JSON document.
- `chappie workflows delete <workflow_id> --yes --dry-run` — Delete a workflow.
- `chappie workflows list` — List workflows + a run summary.
- `chappie workflows run <workflow_id> --yes --dry-run` — Trigger a workflow run.
- `chappie workflows run-history --workflow-id` — List workflow runs (optionally for one workflow).
- `chappie workflows show <workflow_id>` — Show one workflow + recent runs.

