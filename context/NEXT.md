# Next Actions

> Lista breve e ordinata. Non trasformarla in backlog infinito.

Last updated: 2026-11-02 (template maintenance)

The research queue remains a template for `arca init`. Framework maintenance
is recorded separately below.

## Now

1. [ ] ...

## After that

1. [ ] ...

## Waiting / external

- [ ] ...

## Do not do yet

- ... perché ...

## Stop condition

La prossima unità di lavoro è conclusa quando:
- ...

## Template maintenance

Next executable action: run `python3 arca integrations install cortexdb feynman --scope project --dry-run`
from the repository root to review the installation paths without changing
the template or live agent configuration.

Optional integration implementation is complete and verified; publication was
requested on 2026-11-02. Use Git HEAD/upstream for the revision. Details and decisions:
`docs/INTEGRATIONS.md`, `research/plans/completed/PLAN-002-integrations.md`.
46 tests, installed-wheel setup, real CortexDB MCP save/recall, and generated
skill validation passed in disposable directories. Live user profiles remain
unchanged. Codex's interactive UI and Feynman model workflows were not run.

CLI code remains in `scripts/arca_cli/`; generated packages use `.local/dist/`.
Scientific objective/next-action placeholders above remain available for a new
research project to initialize.
