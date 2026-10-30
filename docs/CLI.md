# One interface for ARCA

Use the same local operations from your terminal, Codex, or Claude Code.
The CLI runs on Python 3.9+ with no third-party runtime dependencies.

## Start here

Copy or clone the ARCA template into your project first. For an existing
repository, merge the scaffold carefully and preserve your code and notes.
`init` configures that scaffold; it does not download or merge a template.

From the project root:

```bash
./arca init
./arca status
./arca check
```

`init` asks for a research objective and one executable next action. It fills
the corresponding template sections in `research/CHARTER.md`,
`context/STATE.md`, and `context/NEXT.md`. Review questions, datasets, metrics,
and compute constraints with your agent afterward. These scientific details
still need your input.

On platforms without executable script support, use `python3 -m arca_cli`
in place of `./arca`.

### Use it through your coding agent

Open the ARCA project folder in your editor, then start a **Claude Code or
Codex session associated with that folder**. Type the invocation in that
extension's chat input. A local terminal session of either agent works too.

| Where you type | Example | What runs |
|---|---|---|
| Claude Code chat | `/arca Show the current state and next action.` | The `arca` skill asks Claude to execute the local CLI |
| Codex chat | `$arca Show the current state and next action.` | The `arca` skill asks Codex to execute the local CLI |
| Project terminal | `./arca status` | Python executes the CLI directly |

`/arca` and `$arca` are skill invocations in the agent chat. Shell commands
such as `./arca status` or `python3 -m arca_cli status` belong in a terminal;
you can also ask the agent to execute them.

For a new project, use **init → check → work → checkpoint**. In later sessions,
use **resume → work → check → checkpoint**. Use `status` for a quick reminder
during work. These short chat requests keep the sequence explicit:

| Operation | Claude Code chat | Codex chat |
|---|---|---|
| Initial setup, once | `/arca init` | `$arca init` |
| Resume an existing project | `/arca resume` | `$arca resume` |
| Read the current summary | `/arca status` | `$arca status` |
| Prepare an experiment | `/arca experiment new "baseline"` | `$arca experiment new "baseline"` |
| Check records | `/arca check` | `$arca check` |
| Close the session | `/arca checkpoint` | `$arca checkpoint` |

The text after the skill name is an instruction interpreted by the agent.
`/arca status` and `/arca Show the current state and next action.` request
the same operation. `init` initializes the project; `status` reads it.
`resume` invokes the focused `arca-resume` workflow; there is no CLI subcommand
named `resume`. A chat checkpoint includes note updates before the CLI snapshot.

Longer requests are also accepted. For example, in **Claude Code**:

```text
/arca Initialize this project using the objective we just agreed on.
/arca Show the current state and next action.
/arca Prepare an experiment to test the calibration hypothesis.
/arca Check the project structure and summarize any issues.
/arca Checkpoint this session, including the latest verification results.
```

The equivalent requests in **Codex** are:

```text
$arca Initialize this project using the objective we just agreed on.
$arca Show the current state and next action.
$arca Prepare an experiment to test the calibration hypothesis.
$arca Check the project structure and summarize any issues.
$arca Checkpoint this session, including the latest verification results.
```

The agent translates the request into the same CLI operations. For a
checkpoint it updates the canonical notes before taking the snapshot.
Existing `arca-resume` and `arca-checkpoint` skills remain available.

The project includes `.agents/skills/arca/SKILL.md` for Codex and
`.claude/skills/arca/SKILL.md` for Claude Code. ARCA is currently delivered
as repository code and skills; no separate ARCA marketplace plugin is needed.
The agent runs `python3 -m arca_cli` from the project root, so using the skill
does not require installing the `arca` console command. It does require
Python 3.9+, shell access, and the usual tool permissions for the operation.

With **VS Code Remote SSH**, open the project folder on the server and use
an agent session that can execute commands there. Python and the project files
must be available on that server. A local installation of `arca` does not
install it on the remote machine.

### Optional: install the `arca` command

For use from any directory, install into your preferred Python environment:

```bash
python3 -m pip install -e .
arca --help
```

An editable installation follows changes in this checkout. A regular
`python3 -m pip install .` also works; reinstall after updating the code.
Installation exposes the CLI; the ARCA project scaffold remains separate.

The installed command discovers the project by searching upward from the
current directory for `framework.yaml`. Select another project explicitly:

```bash
arca --root /path/to/project status
```

Without installation, run `python3 /path/to/ARCA/arca --root /path/to/project status`.
The selected project needs the ARCA scaffold, but need not contain a local
copy of the installed CLI.

Installing the Python package exposes terminal commands. Project skills
come from the repository's `.agents/skills/` and `.claude/skills/` folders.

## Commands

| Command | Result | Writes |
|---|---|---|
| `arca init` | Sets the research objective and next action | Only the corresponding empty/template sections in CHARTER, STATE, NEXT |
| `arca status` | Shows objective, next action, Git state, experiment counts | None |
| `arca status --full` | Also prints the complete STATE and NEXT records | None |
| `arca check` | Checks required files and selected experiment references | None |
| `arca experiment new "title"` | Allocates `E-####`, starter files, and a registry row | Experiment directory and registry |
| `arca checkpoint` | Snapshots existing STATE/NEXT and Git metadata | A new file under `context/session_archive/` |

Run `arca COMMAND --help` for options. Commands use the current project, even
when the CLI is installed from a different checkout. `--root PATH` and
`--json` work before or after the subcommand.

### Initialize without prompts

```bash
arca init \
  --objective "Compare calibration methods on the held-out benchmark." \
  --next-action "Inspect data/registry.yaml and document the split protocol."
```

Provide both values in non-interactive sessions. Repeating initialization
with the same values makes no changes. A completed research objective and
single next action can also be reused by running `arca init` again without
flags. If a target section already contains different notes, initialization
reports the conflict before writing any target file. Edit ongoing research
notes directly or through your agent.

### Prepare an experiment

```bash
arca experiment new "temperature scaling baseline"
```

The result is a directory such as `experiments/E-0001-temperature-scaling-baseline/`
containing `experiment.yaml`, `report.md`, `metrics.json`, and `runs/`, plus
a planned entry in `experiments/REGISTRY.csv`. The record captures the current
commit and whether Git has uncommitted changes, when Git metadata is available.
Complete the protocol before launching a run. Perform experiment allocation
serially within a shared working tree.

### Check and checkpoint

```bash
arca check
# Update context/STATE.md and context/NEXT.md with your agent first.
arca checkpoint
```

The structural check reports errors and warnings. By default, errors cause a
nonzero exit; `arca check --strict` also fails on warnings. The check does
not validate scientific correctness, remote artifacts, or memory connectivity.
Warnings from reference checks are visible in both CLI and legacy output.

A checkpoint preserves the notes already on disk. The snapshot command does
not summarize the conversation or update those notes. Use the `arca` or
`arca-checkpoint` skill for the complete session handoff.

`status` reports registered experiment labels and recorded context. It does
not query a scheduler or establish whether a training process is still alive.

## Structured output for agents and scripts

```bash
arca status --json
arca check --json
arca experiment new "pilot" --json
arca checkpoint --json
```

Successful commands emit one JSON object to stdout. Operational errors also
emit a JSON object with `ok: false` and `error` when `--json` is set.
Argument syntax errors are reported by the command parser on stderr.
Initialization never prompts in JSON mode; supply missing values as flags.

`status` includes `root`, `objective`, `next_action`, `git`, `experiments`,
the canonical `state`/`next` text, `warnings`, and `job_status`.
`check` includes `ok`, `errors`, `warnings`, and the validation scope.
Experiment creation returns `experiment_id`, `path`, and the recorded status;
checkpoint creation returns the snapshot `path`.

Exit codes: `0` success; `1` operational/validation failure; `2` invalid
arguments; `130` interrupted execution. `check --strict` may return `1`
with `ok: true` when structure is valid but warnings remain.

## When the skill or command is missing

| Symptom | What to check |
|---|---|
| Codex does not show `arca` | Open the correct repository, confirm `.agents/skills/arca/SKILL.md` exists, and type `$` or use `/skills` to select it. Restart Codex if changes have not appeared. |
| Claude Code does not show `/arca` | Confirm `.claude/skills/arca/SKILL.md` exists in the project, then type `/` to browse skills. On versions that support it, `/reload-skills` loads a newly created skills directory; otherwise reopen the session. |
| The agent cannot execute commands | Use an agent session with shell access to this project and check its tool permissions. |
| `arca: command not found` in a terminal | Use `./arca` from the repository root or `python3 -m arca_cli`. To use the bare `arca` command, install it in the active Python environment. |
| `No module named arca_cli` | Run from the repository root containing `arca_cli/`, or use the installed console command with `--root`. |
| `No ARCA project found` | Change into the project containing `framework.yaml`, or pass `--root /path/to/project`. |

You can always ask the agent explicitly:

```text
From this repository root, run python3 -m arca_cli status --json
and explain the current state and next action.
```

Invocation syntax and skill discovery were checked against the official
[Codex skills guide](https://learn.chatgpt.com/docs/build-skills),
[Claude Code skills guide](https://code.claude.com/docs/en/skills), and
[Claude Code VS Code guide](https://code.claude.com/docs/en/vs-code)
on 2026-10-30. This does not imply that either extension's UI was tested
in every installed version.

## Compatibility and development

Existing helper commands continue to use the shared implementation:

| Existing command | CLI equivalent |
|---|---|
| `python3 scripts/arca_check.py` | `arca check` |
| `python3 scripts/new_experiment.py "title"` | `arca experiment new "title"` |
| `python3 scripts/session_checkpoint.py` | `arca checkpoint` |
| `python3 scripts/validate_context.py` | Context-only subset of `arca check` |

Legacy scripts target the repository containing the script, as before.
The experiment and checkpoint scripts still print just the generated path.
Keep `arca_cli/` alongside those scripts when updating an older project.

`make status`, `make check`, and `make checkpoint` use the CLI. Run the
isolated integration suite with:

```bash
python3 -m unittest discover -s tests -v
```

The illustrated guide has an editable source at
[`ARCA_Quick_Start_User_Guide.html`](ARCA_Quick_Start_User_Guide.html).
Regenerate its PDF with the optional documentation tool (not an ARCA runtime
dependency):

```bash
uvx --python "$(python3 -c 'import sys; print(sys.executable)')" \
  --from weasyprint==68.0 weasyprint \
  docs/ARCA_Quick_Start_User_Guide.html docs/ARCA_Quick_Start_User_Guide.pdf
```

WeasyPrint requires its native font libraries (including Pango) in the
selected Python environment. This is needed only to rebuild the PDF;
the checked-in PDF can be read directly.
