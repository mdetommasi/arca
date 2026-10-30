# Coding agent compatibility · ottobre 2026

## Codex (OpenAI)

- `AGENTS.md`: repository guidance, keep lean; prefer pointers and task-specific retrieval over blanket pre-read.
- `.agents/skills/<slug>/SKILL.md`: skill repo-local, loaded on demand via metadata name + description.
- plugin support / MCP tools / hooks: feature-dependent, require version check and manual trust for untrusted hooks.
- Customizing repo instructions should adapt to newer model capabilities rather than adding redundant rules.

Refs: https://learn.chatgpt.com/docs/build-skills ; https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra ; https://developers.openai.com/plugins/build/plugins

## Claude Code (Anthropic)

- `CLAUDE.md`: project instructions; `@AGENTS.md` keeps cross-agent contract central.
- `.claude/skills/<slug>/SKILL.md`: project skills; discovery via concise `name` and `description`, body read only on matching workflow.
- `.claude/settings.example.json`: optional hooks; verify overlap with CortexDB plugin's own hooks before activation.
- Skills may also live in user config; keep project versioned skills narrowly scoped.

Ref: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

## Feynman / other research agents

Maintain separate scientific roles (hypothesis generation, review, verification) but insist their findings be written to ARCA's canonical Markdown/registries with IDs and provenance. Avoid rewriting agent/vendor-specific capabilities into universal hard requirements.

## VS Code and portability

Use repo root paths and Python standard library helpers wherever possible. Avoid symlinks, mandatory extensions, mandatory database processes, machine-specific absolute paths in tracked files. User-local environment files and `CORTEXDB_PATH` are not committed.

## Change-management

Review upstream behavior at major agent updates: path discovery, trust model, hook payloads, plugin commands, auto memory, and tool permissions. Separate 'verified against docs' from 'tested in installed local versions'.
