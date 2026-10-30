# Coding agent compatibility · ottobre 2026

## ARCA interface in an editor session

Open the ARCA project folder in the editor and start the agent session there.
In Claude Code's chat, type `/arca Show the current state`; in Codex's chat,
type `$arca Show the current state`. These load the repository skill, which
guides the agent to run `python3 -m arca_cli` from the project root.

For direct terminal use, run `./arca status` or `python3 -m arca_cli status`.
Installing with `python3 -m pip install -e .` additionally exposes the bare
`arca` command. A separate ARCA marketplace plugin is not required.

For Remote SSH projects, the agent must execute in the remote project folder.
See [`CLI.md`](CLI.md) for setup and skill-discovery troubleshooting.

## Codex (OpenAI)

- `AGENTS.md`: repository guidance, keep lean; prefer pointers and task-specific retrieval over blanket pre-read.
- `.agents/skills/<slug>/SKILL.md`: skill repo-local, loaded on demand via metadata name + description.
- plugin support / MCP tools / hooks: feature-dependent, require version check and manual trust for untrusted hooks.
- Customizing repo instructions should adapt to newer model capabilities rather than adding redundant rules.

Refs: https://learn.chatgpt.com/docs/build-skills ; https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra ; https://developers.openai.com/plugins/build/plugins

Explicit skill selection in the CLI/IDE uses `$` or `/skills`. Codex reads
repository skills from `.agents/skills/`; if an update is not detected,
restart Codex. Verified against the official skills guide on 2026-10-30.

## Claude Code (Anthropic)

- `CLAUDE.md`: project instructions; `@AGENTS.md` keeps cross-agent contract central.
- `.claude/skills/<slug>/SKILL.md`: project skills; discovery via concise `name` and `description`, body read only on matching workflow.
- `.claude/settings.example.json`: optional hooks; verify overlap with CortexDB plugin's own hooks before activation.
- Skills may also live in user config; keep project versioned skills narrowly scoped.

Ref: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

Project skills under `.claude/skills/` can be invoked as `/skill-name` in the
Claude Code session. The VS Code extension suggests skills when typing `/`.
Current versions provide `/reload-skills` for a newly created skills directory;
reopening the session is the fallback. Verified against the official
[skills](https://code.claude.com/docs/en/skills) and
[VS Code](https://code.claude.com/docs/en/vs-code) guides on 2026-10-30;
interactive behavior has not been tested in every installed extension version.

## Feynman / other research agents

Maintain separate scientific roles (hypothesis generation, review, verification) but insist their findings be written to ARCA's canonical Markdown/registries with IDs and provenance. Avoid rewriting agent/vendor-specific capabilities into universal hard requirements.

## VS Code and portability

Use repo root paths and Python standard library helpers wherever possible. Avoid symlinks, mandatory extensions, mandatory database processes, machine-specific absolute paths in tracked files. User-local environment files and `CORTEXDB_PATH` are not committed.

## Change-management

Review upstream behavior at major agent updates: path discovery, trust model, hook payloads, plugin commands, auto memory, and tool permissions. Separate 'verified against docs' from 'tested in installed local versions'.
