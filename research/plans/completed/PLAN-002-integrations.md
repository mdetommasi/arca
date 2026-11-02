# PLAN-002 — Optional integrations during initialization

Status: complete · 2026-11-02

## Outcome

Install CortexDB and Feynman for Claude Code and Codex through ARCA, with
project or user scope, both during init and independently afterward.

## Decisions

- Keep plain init offline and dependency-free. Explicit `--with cortexdb
  feynman` opts in; project scope and both agents are the defaults.
- CortexDB: release binary over stdio MCP, one database shared by the two
  agents within the selected scope. No automatic recall/capture hooks.
- Feynman: skills edition, upstream workflow prompts with a host adapter;
  do not assume Pi-specific slash commands/tools exist in Claude or Codex.
- Keep downloads/state under ignored `.local/` (project) or user data storage.
  Put discoverable skills/configuration only in native agent locations.
- Pin tested upstream releases; verify binary checksums, record provenance,
  reject conflicting local edits, preserve unrelated configuration, support
  preview and repeat installation without duplicate entries.

## Work

1. [x] Inspect upstream releases, installers, prompts, and host discovery docs.
2. [x] Implement installation, status, and init integration.
3. [x] Test isolated scopes, failure paths, repeat installs, and real downloads.
4. [x] Update README, CLI/agent/memory guides, skills, PDF, and continuity.

## Sources

- https://github.com/liliang-cn/cortexdb/releases/tag/v2.142.0
- https://github.com/Companion-Inc/feynman/releases/tag/v0.5.61
- https://github.com/Companion-Inc/feynman/blob/v0.5.61/scripts/install/install-skills.sh
- https://learn.chatgpt.com/docs/extend/mcp?surface=cli
- https://learn.chatgpt.com/docs/build-skills
- https://code.claude.com/docs/en/mcp

## Validation boundary

Test downloads and runtime handshake in disposable directories; do not install
into the developer's live agent configuration as a side effect of development.
No research model calls, experiments, or scientific claims are involved.

## Results

- FACT: 46 tests passed, including both scopes/hosts, conflicts, offline
  preview, download failure, interrupted writes, relocation, cache reuse,
  init preflight, checksums, archive validation, and all 21 existing CLI tests.
- FACT: real pinned downloads installed in a temporary project on macOS ARM64;
  repeat installation changed no files. CortexDB 2.142.0 completed MCP
  initialization, exposed 115 tools, and saved/recalled a test memory across
  separate server processes using the same disposable database.
- FACT: Claude Code 2.1.292 recognized the generated project server and
  reported its normal pending-approval state. Codex config was checked against
  official documentation and TOML parsing; no interactive Codex UI was tested.
- FACT: the built wheel initialized a disposable project with both integrations,
  passed integration status, and repeated installation without changes. The four
  generated host skills passed structural validation; Feynman has one discoverable
  SKILL.md per host, with original prompts/roles stored as resources.
- FACT: README, reference docs, canonical/Claude ARCA skills, and the five-page
  illustrated guide describe installation and usage. Strict structural and
  whitespace checks passed.
- DECISION: preserve upstream prompts and role descriptions; do not copy
  nested upstream SKILL.md files that would expose Pi-only invocations through
  recursive discovery. The single feynman adapter resolves host differences.
- No live user installation, research inference, training job, commit, or push
  was performed as part of this feature task.
