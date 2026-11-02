# Install CortexDB and Feynman

ARCA can install both integrations for Claude Code and Codex, either in one
project or for your user account. They are optional: plain `arca init` stays
offline, and ARCA's research records work without them.

## Choose the scope, then install

| Scope | Available in | CortexDB memory | Choose it when |
|---|---|---|---|
| `project` (default) | This ARCA project, on this machine | One project database shared by Claude and Codex | Research projects should keep separate memory |
| `user` | All projects for this OS user, on this machine | One shared user database | You want reusable workflows and cross-project memory |

The same scope applies to both selected integrations. To use user-wide Feynman
with project-specific memory, install them separately with different scopes.
Installing on a laptop does not install anything on an SSH server: run the
command wherever the agents execute.

**During initial setup**, type one of these in chat:

```text
Claude Code: /arca init --with cortexdb feynman --scope project
Codex:      $arca init --with cortexdb feynman --scope project
```

The agent establishes the research objective/next action and runs the CLI with
those values. Terminal equivalent (prompts for the two research values):

```bash
./arca init --with cortexdb feynman --scope project
```

For non-interactive initialization, include `--objective "..."` and
`--next-action "..."`; `--json` emits one result object. Research sections are
checked for conflicts before installation; download/configuration failures
leave those notes unchanged. Installation and research initialization are
separate stages: if a later filesystem failure prevents writing research notes,
the successfully installed integrations remain and init can be retried.

**For an existing project**, use the dedicated operation:

```bash
./arca integrations install cortexdb feynman --scope project
./arca integrations status --scope project
```

Chat accepts `/arca integrations install ...` or `$arca integrations install ...`.
This leaves the charter, STATE, and NEXT alone. With an installed `arca` command,
user-scope installation also works from outside an ARCA project.

Useful variations:

```bash
# Preview versions, download URLs, and destination paths; no writes or network.
./arca integrations install cortexdb feynman --scope user --dry-run --json

# User-wide research workflows, available to both agents.
./arca integrations install feynman --scope user

# Project memory for only Codex; omit --agents to configure both hosts.
./arca integrations install cortexdb --scope project --agents codex
```

Downloads need HTTPS access to GitHub. Installation itself needs only Python
3.9+; it does not require Go, Node, npm, or either agent's terminal executable.
The pinned CortexDB binaries cover macOS, Linux, and Windows on x86-64/ARM64.
Feynman's workflow resources are platform-independent.

## Reopen the session and use the integrations

Reopen Claude Code or Codex after installation. The host must discover the new
skills and MCP configuration. Accept its normal project/MCP trust prompt when
appropriate; ARCA does not change permission or trust settings. Organization
policies can restrict MCP loading even when installation succeeds.

| Task | Claude Code chat | Codex chat |
|---|---|---|
| Literature review | `/feynman lit calibration methods` | `$feynman lit calibration methods` |
| Investigate a topic | `/feynman deepresearch distribution shift` | `$feynman deepresearch distribution shift` |
| Review a draft | `/feynman review paper/draft.md` | `$feynman review paper/draft.md` |
| Plan a replication | `/feynman replicate <paper URL>` | `$feynman replicate <paper URL>` |
| Recall research memory | `/cortexdb recall calibration decisions` | `$cortexdb recall calibration decisions` |
| Save a verified pointer | `/cortexdb save the decision recorded in research/DECISIONS.md` | `$cortexdb save the decision recorded in research/DECISIONS.md` |

The text after the skill name is interpreted by the agent. These are chat
requests, not new `arca` terminal subcommands. Feynman also exposes `audit`,
`recipe`, `compare`, `draft`, `autoresearch`, `summarize`, and `log` through the
same skill. Experiments still require an ARCA protocol and execution budget.

### What Feynman installs

The **skills edition** installs original Feynman workflow prompts and role
descriptions, plus a small ARCA adapter named `feynman`. It uses the current
Claude/Codex session and its tools. It does not install the standalone Feynman
app, its Pi runtime, separate model login, alphaXiv commands, or custom science
database tools. If a needed capability is unavailable, the agent reports it
and uses available source-search tools where possible.

The adapter is necessary because upstream skills refer to Pi slash commands
and delegation APIs. It reads the selected upstream prompt directly and maps
tool use to the active host. If delegation is unavailable, stages run
sequentially and the review is not described as independent.

In an ARCA project, upstream `outputs/` maps to `research/feynman/`, `notes/`
to `research/feynman/notes/`, and `papers/` to `paper/drafts/`. Provenance
sidecars stay beside the outputs. `autoresearch.*` belongs inside an allocated
experiment directory. Research outputs remain separate from installation data.
The adapter preserves project instructions and the original upstream license.

### What CortexDB installs

ARCA installs the pinned `cortexdb-mcp` executable, registers a `cortexdb` stdio
MCP server in both hosts, and adds a memory skill. Both hosts receive the same
explicit `CORTEXDB_PATH`. No background daemon or global PATH change is needed:
the agent starts the server when it connects.

Project scope uses `.local/cortexdb/brain.db`; user scope uses the upstream
default `~/.cortexdb/cortexdb.db`, including an existing database there. The
database is created when the server starts. The generated configuration clears
`CORTEXDB_REMOTE` so an inherited remote address cannot redirect this local
installation. Other upstream environment settings can still be inherited.

Without an embedding provider, CortexDB uses lexical retrieval. Semantic
retrieval and remote-brain setups are separate configuration choices; see
[`memory/CORTEXDB.md`](../memory/CORTEXDB.md). ARCA's installer does not add
auto-recall/capture hooks, import transcripts, or override existing plugin hooks.
If you already use the upstream plugin, review that setup before installing a
second server. The installer detects conflicts in the target config files;
it cannot enumerate every host-managed plugin or connector.

## Where files go

| Component | Project scope | User scope (default paths) |
|---|---|---|
| Downloads, binary, manifest, backups | `.local/arca/integrations/` | `~/.local/share/arca/integrations/` |
| Codex skills | `.agents/skills/{cortexdb,feynman}/` | `~/.agents/skills/{cortexdb,feynman}/` |
| Claude skills | `.claude/skills/{cortexdb,feynman}/` | `~/.claude/skills/{cortexdb,feynman}/` |
| Codex MCP config | `.codex/config.toml` | `~/.codex/config.toml` |
| Claude MCP config | `.mcp.json` | `~/.claude.json` |
| CortexDB database | `.local/cortexdb/brain.db` | `~/.cortexdb/cortexdb.db` |

User-scope Codex configuration honors `CODEX_HOME`; Codex user skills follow
the native `~/.agents/skills` location. Claude honors `CLAUDE_CONFIG_DIR` for
skills and its `.claude.json` file. Generated MCP commands use absolute paths.
Install separately on each machine; after moving a project directory, rerun
the same install command to refresh paths before opening an agent there.

Project installation adds exact patterns to `.gitignore` for downloaded
skills, local configuration, and runtime data. Already tracked configuration
stays tracked: review its diff before committing machine-specific paths.
No new visible top-level directory is needed. Claude's `.mcp.json` is a native
host requirement. Runtime data and databases are not research artifacts.

## Repeat installs, diagnostics, and recovery

Run `arca integrations status --scope project` (or `user`) to inspect the
manifest, installed file hashes, and managed MCP entries. Exit code `1` means
files/configuration are missing or changed. This is a local integrity check,
not a connection test. `arca check` remains the separate research-structure check.
For live status use Claude's `/mcp` or `claude mcp get cortexdb`, or Codex's MCP
view. Skills missing after restart usually indicate a different project/user
scope, agent configuration directory, or managed policy.

Reinstalling the same selection is idempotent and reuses verified downloads.
Missing resources can be restored; locally edited owned files are reported
instead of overwritten. Unrelated MCP servers, settings, and TOML comments are
preserved. An existing `cortexdb` server or skill not owned by this installer
causes a conflict: keep it, or move its configuration/skill aside after review
and rerun. There is no implicit force-overwrite option.

Before writes, downloads pass pinned SHA-256 checks and all target files are
checked for conflicts. Files use atomic replacement; a caught write failure
rolls back earlier writes. An abrupt process/machine crash is not a multi-file
transaction. Existing changed files have private backups under
`backups/<id>/`, with `index.json` mapping backups to original paths. Recovery
should restore only the affected entries if other settings changed afterward.
If a crashed installer left `install.lock`, remove it only after confirming
that no installation is still running. Preview mode reports the intended
destinations; the actual install performs conflict and download verification.

For manual removal, remove the installed skill directories, the `cortexdb`
entry in Claude's `mcpServers`, and the marked ARCA block in Codex's TOML;
preserve all other settings. Then remove the installation state directory if
no host still references its binary. Keep the database unless you explicitly
intend to discard its memory. User- and project-scope installs are separate;
avoid installing the same integration at both scopes unless you have reviewed
host precedence and duplicate skill discovery.

## Design and upstream versions

The implementation lives in `scripts/arca_cli/integrations.py`. Native MCP
configuration and discoverable skill files work with CLI/editor sessions
without relying on a particular host's plugin-management CLI. A single
scope/host selection covers the two integrations, and the independent install
command avoids reinitializing a project's evolving research state.

This release pins CortexDB **2.142.0** and Feynman **0.5.61**, commit
`89b0242919faf89b38dcb6ae8be92f6dbcd77203`. CortexDB release-asset digests and
the Feynman commit archive's SHA-256 are embedded in the installer. They verify
download integrity against the reviewed bytes; they are not separate publisher
signatures. Versions are updated with ARCA after reviewing and testing upstream
changes, not silently resolved to `latest` during init. Each installed skill
contains `ARCA_PROVENANCE.json`; the scope's manifest tracks managed files.

Sources reviewed on 2026-11-02:

- [CortexDB release](https://github.com/liliang-cn/cortexdb/releases/tag/v2.142.0)
  and [upstream integration](https://github.com/liliang-cn/cortexdb/blob/v2.142.0/plugins/cortexdb/README.md).
- [Feynman release](https://github.com/Companion-Inc/feynman/releases/tag/v0.5.61),
  [skills installer](https://github.com/Companion-Inc/feynman/blob/v0.5.61/scripts/install/install-skills.sh),
  and [workflow prompts](https://github.com/Companion-Inc/feynman/tree/v0.5.61/prompts).
- [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)
  and [skill locations](https://learn.chatgpt.com/docs/build-skills).
- [Claude MCP scopes](https://code.claude.com/docs/en/mcp) and
  [configuration directories](https://code.claude.com/docs/en/claude-directory).
