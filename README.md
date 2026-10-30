<div align="center">
  <a href="docs/ARCA_Quick_Start_User_Guide.pdf">
    <img src="docs/assets/arca-workflow.svg" alt="ARCA research workflow: connect, initialize, work with evidence, checkpoint and resume" width="100%">
  </a>

  <p><strong>Research context that survives long projects, new sessions, and changing coding agents.</strong></p>

  <p>
    <a href="docs/ARCA_Quick_Start_User_Guide.pdf"><strong>Quick Start &amp; User Guide</strong></a>
    ·
    <a href="docs/CLI.md">CLI &amp; agent interface</a>
    ·
    <a href="docs/GUIDELINES_v2.md">Operating guidelines</a>
    ·
    <a href="docs/CONTEXT_ARCHITECTURE.md">Architecture</a>
  </p>
</div>

## What is ARCA?

ARCA is a repository framework for machine-learning research carried out with coding agents such as Claude Code and Codex. It keeps the scientific objective, current state, experiments, decisions, negative results, and paper claims in versioned files with traceable provenance.

You work by talking to your agent. ARCA gives it a shared structure and focused workflows; the agent handles the files and helper scripts while you approve scientific decisions, costly runs, and commits.

> **The core idea:** Git-tracked ARCA records are the source of truth. Optional memory tools such as CortexDB help you find those records; they never replace the evidence.

## Start here: your first project

Use the **chat of Claude Code or Codex** for the workflow below. The agent
uses ARCA's local CLI on your behalf.

### 1. Open the project

Copy or clone this template into your project folder. For an existing
repository, merge the ARCA scaffold while preserving your code and notes.
Open that folder in your editor and start a Claude Code or Codex session.
The session needs access to the files and a shell with Python 3.9+.
With Remote SSH, open the remote project and run the agent there.

The project skills are already included. You can follow this chat workflow
without installing a separate ARCA plugin or Python package.

### 2. Initialize once

Type **one** of these in the agent chat:

| Claude Code | Codex |
|---|---|
| `/arca init` | `$arca init` |

The agent reads the project instructions and asks for your research objective
and next action if they are missing. It then uses the CLI to fill the initial
sections of `research/CHARTER.md`, `context/STATE.md`, and `context/NEXT.md`.
It preserves sections that already contain different research notes.

Continue the conversation to define your questions, datasets, evaluation
metrics, baseline, and compute constraints. The CLI seeds the objective and
next action; the agent completes the other relevant records using facts you
provide. Review the changes with it.

### 3. Check the project, then start working

| Claude Code | Codex |
|---|---|
| `/arca check` | `$arca check` |

The agent runs the structural check and explains any issues. Once the
objective, next action, and evaluation protocol are clear, ask it to carry
out the next task. You are now in the daily workflow below.

**Already initialized?** Start with `resume` in the next section. Use `init`
for the initial setup, rather than repeating it at the start of every session.

## Daily workflow: resume → work → check → checkpoint

| When | Claude Code chat | Codex chat | What happens |
|---|---|---|---|
| Open a new session or switch agents | `/arca resume` | `$arca resume` | Reconstructs the research state, relevant evidence, and exact next action from the repository. |
| Need a quick reminder during work | `/arca status` | `$arca status` | Shows the recorded objective, next action, Git state, and experiment counts. |
| Prepare an experiment | `/arca experiment new "baseline"` | `$arca experiment new "baseline"` | Creates an `E-####` record; the agent helps complete its protocol before you approve a run. |
| Check the records | `/arca check` | `$arca check` | Checks required files and selected references; the agent explains errors and warnings. |
| End the session, take a break, or switch agents | `/arca checkpoint` | `$arca checkpoint` | The agent updates STATE/NEXT and relevant notes, then saves a checkpoint. |

Between these steps, **talk to the agent normally**: ask it to implement
code, inspect data, run an approved experiment, or investigate a result.
ARCA records the work so that it can be continued in the next session.

For example, in Claude Code:

```text
First session:
  /arca init
  [Answer the agent's questions about the project.]
  /arca check
  /arca experiment new "initial baseline"
  [Define the protocol, approve the run, and review the results.]
  /arca checkpoint

Next session, even with a different agent/model:
  /arca resume
  [Continue from the recorded next action.]
```

In Codex, use `$arca` instead of `/arca`. Small code or documentation tasks
can be handled directly; they do not need an experiment record.

### Why do some examples use sentences after `/arca`?

**`/arca` selects the skill; the text after it tells the agent what to do.**
The short forms above are the recommended way to request the operations.
For example, these two chat messages ask for the same status summary:

```text
/arca status
/arca Show the current state and next action.
```

`/arca init` requests initial setup. `/arca status` only reads the current
records. They serve different points in the workflow.

The agent interprets the text after the skill name and selects the workflow;
it is not passed verbatim to a shell. For example, `resume` uses the focused
`arca-resume` workflow, while `status` invokes the CLI's `status` command.
The standalone `arca-resume` and `arca-checkpoint` skills remain available.

If the skill is missing from your session, see
[skill discovery troubleshooting](docs/CLI.md#when-the-skill-or-command-is-missing).

## How evidence stays connected

Every publishable quantitative claim should have a verifiable path back to the run that produced it:

```text
research question
      ↓
hypothesis  →  experiment E-####  →  finding F-###  →  paper claim
                  │                     │                 │
                  └─ config, data, metrics, artifacts, commit ─────────┘
```

ARCA keeps facts, source claims, hypotheses, interpretations, and decisions distinct. Negative and contradictory results remain visible so future sessions do not repeat failed work.

## What still needs your research judgment?

You define the research goal and approve consequential scientific decisions,
costly runs, and commits. The agent fills in the records using the evidence
available to it. A structural check does not establish that an experiment
is scientifically correct; for a finding or paper claim, invoke
`research-evidence-audit` in the appropriate agent.

Ask the agent to inspect the actual process or scheduler when monitoring a
run. The CLI's status summary reports recorded information. Optional hooks
run only when configured for your agent.

## Repository map

| Need | Canonical location |
|---|---|
| Research goal, scope, success criteria | [`research/CHARTER.md`](research/CHARTER.md) |
| Current state and next executable action | [`context/STATE.md`](context/STATE.md), [`context/NEXT.md`](context/NEXT.md) |
| Questions, hypotheses, findings, contradictions | [`research/`](research/) |
| Experiment registry, protocols, metrics, reports | [`experiments/`](experiments/) |
| Dataset fingerprints and artifact provenance | [`data/`](data/), [`artifacts/`](artifacts/) |
| Claims tied to evidence | [`paper/CLAIMS.md`](paper/CLAIMS.md) |
| Cross-agent instructions | [`AGENTS.md`](AGENTS.md) |
| Focused agent workflows | [`.agents/skills/`](.agents/skills/), [`.claude/skills/`](.claude/skills/) |
| Optional semantic memory | [`memory/CORTEXDB.md`](memory/CORTEXDB.md) |
| Complete operating guide | [`docs/GUIDELINES_v2.md`](docs/GUIDELINES_v2.md) |

The context is layered intentionally: agents read the small current state first, then retrieve only the evidence relevant to the task. See the [context architecture](docs/CONTEXT_ARCHITECTURE.md) for the full model.

## Prefer the terminal?

Use the same operations directly from the repository root:

```bash
./arca init                           # Initial setup; asks for objective and next action
./arca status                         # Read the current recorded state
./arca experiment new "initial baseline"
./arca check                          # Validate the structure
./arca checkpoint                     # Snapshot STATE/NEXT already on disk
```

In the terminal you execute the CLI directly. In chat, the skill guides the
agent through the complete workflow: for `checkpoint`, it updates the notes
before executing the snapshot command. For research resumption, use the
agent's `resume` workflow; the CLI has no `resume` subcommand.

`python3 -m arca_cli` works in place of `./arca`. Optionally install with
`python3 -m pip install -e .` to use the bare `arca` command. Existing helper
scripts and Make shortcuts remain available. See the [CLI guide](docs/CLI.md)
for all options and JSON output.

## Optional integrations

- **CortexDB** adds semantic recall and graph navigation. It is not required; follow [`memory/CORTEXDB.md`](memory/CORTEXDB.md) for isolation, permissions, privacy, and diagnostics.
- **Custom skills** package a genuinely repeated workflow. Keep them few and focused; see [`docs/SKILLS.md`](docs/SKILLS.md).
- **Feynman or other research agents** can support hypothesis generation, critique, and replication, but their output becomes evidence only after it is recorded and verified through ARCA.

## Common questions

<details>
<summary><strong>Do I need to edit every Markdown file myself?</strong></summary>

No. Start with `/arca init` in Claude Code or `$arca init` in Codex, then
answer the agent's questions. It should fill only the relevant files using
the scientific facts you provide.
</details>

<details>
<summary><strong>Does closing VS Code stop a training job?</strong></summary>

ARCA does not keep processes alive. A job continues only if it was launched through a persistent server-side process or scheduler; check the actual process or queue.
</details>

<details>
<summary><strong>Can Claude Code and Codex work on the same project?</strong></summary>

Yes. Give them separate tasks or worktrees and avoid simultaneous edits to the same files. For independent validation, let one agent review the other's result without treating that review as an experimental replication.
</details>

<details>
<summary><strong>What if the structural check passes but an experiment is wrong?</strong></summary>

That is possible. A structural check is not a scientific audit. Invoke `research-evidence-audit` and run the tests appropriate to the claim, including leakage and baseline-comparability checks.
</details>

<details>
<summary><strong>When should I checkpoint?</strong></summary>

Before ending a substantial session, switching agents or models, risking context compaction, or taking a long break—even if the current experiment is incomplete.
</details>

## Documentation

- **[Quick Start & User Guide](docs/ARCA_Quick_Start_User_Guide.pdf)** — illustrated, prompt-first walkthrough for the first setup and daily use.
- **[CLI & agent interface](docs/CLI.md)** — where to type each invocation, extension setup, terminal commands, JSON output, and troubleshooting.
- **[Operating guidelines](docs/GUIDELINES_v2.md)** — scientific discipline and the complete working protocol.
- **[Context architecture](docs/CONTEXT_ARCHITECTURE.md)** — how ARCA keeps retrieval focused.
- **[Agent compatibility](docs/AGENT_COMPATIBILITY.md)** — Codex, Claude Code, Feynman, and portability notes.
- **[Skills guide](docs/SKILLS.md)** — when and how to create focused workflows.

---

<div align="center">
  <strong>The agents do the work. You make the research decisions. The repository keeps the evidence.</strong>
</div>
