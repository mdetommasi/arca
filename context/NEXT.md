# Next Actions

> Lista breve e ordinata. Non trasformarla in backlog infinito.

Last updated: 2026-11-02 (template maintenance)

The research queue remains a template for `arca init`. The completed CLI
implementation and its follow-up are recorded separately below.

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

Next executable action: run `python3 arca status --full` from the repository
root to review the CLI after the source relocation. Packaging and layout
changes are complete and verified; publication was requested on 2026-11-02.
Read Git HEAD/upstream for the published revision.

Packaging builds use `.local/dist/`. The legacy build/ and egg-info directories
were moved into ignored `.local/packaging-archive.GpfTyu/`; no research artifacts
were removed. Regular/editable installs and the 21 CLI tests passed.

CLI implementation is now under `scripts/arca_cli/`, with `arca` retained as
the root launcher. README, skills, and the PDF use `python3 arca` for source
execution. Older editable installations need one reinstall to refresh their path.

CLI implementation and documentation are complete and verified. Publication
was requested on 2026-10-30; use `git log -1 --oneline` and the upstream branch
to determine the current published revision.
