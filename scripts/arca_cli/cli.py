"""User and agent entry point for ARCA's local workflows."""
from __future__ import annotations

import argparse
import json
import sys

from . import __version__, core


def common_arguments(parser):
    # Suppressed defaults allow the same options before or after a subcommand.
    parser.add_argument("--root", metavar="PATH", default=argparse.SUPPRESS,
                        help="ARCA project directory (default: discover from the current directory)")
    parser.add_argument("--json", action="store_true", default=argparse.SUPPRESS,
                        help="emit one JSON object for automation")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="arca", description="A shared local interface for ARCA research projects.",
        epilog="Start inside a copy of the ARCA template. Run 'arca COMMAND --help' for details.",
    )
    parser.add_argument("--version", action="version", version=f"ARCA CLI {__version__}")
    common_arguments(parser)
    commands = parser.add_subparsers(dest="command")
    init = commands.add_parser("init", help="set the objective and next action in an existing ARCA template")
    common_arguments(init)
    init.add_argument("--objective", help="research objective; prompts when running interactively")
    init.add_argument("--next-action", help="one executable next action; prompts when running interactively")
    status = commands.add_parser("status", help="read the objective, next action, Git state, and experiment counts")
    common_arguments(status)
    status.add_argument("--full", action="store_true", help="also print the complete STATE and NEXT records")
    check = commands.add_parser("check", help="check required files and selected references (read-only)")
    common_arguments(check)
    check.add_argument("--strict", action="store_true", help="return failure on warnings as well as errors")
    checkpoint = commands.add_parser("checkpoint", help="snapshot existing STATE/NEXT and Git metadata")
    common_arguments(checkpoint)
    experiment = commands.add_parser("experiment", help="prepare experiment records")
    common_arguments(experiment)
    actions = experiment.add_subparsers(dest="experiment_action", required=True)
    new = actions.add_parser("new", help="allocate an ID and starter files; does not launch a run")
    common_arguments(new)
    new.add_argument("title", help="experiment title")
    return parser


def init_arguments(root, args):
    existing = core.initialization_values(root)
    objective = args.objective or existing["objective"]
    next_action = args.next_action
    if next_action is None and existing["next"]:
        # Preserve only the canonical single-action form automatically.
        prefix = "1. [ ] "
        if existing["next"].startswith(prefix) and "\n" not in existing["next"]:
            next_action = existing["next"][len(prefix):]
    for label, value in (("--objective", objective), ("--next-action", next_action)):
        if not value and (getattr(args, "json", False) or not sys.stdin.isatty()):
            raise core.ArcaError(f"Provide {label} for non-interactive initialization. Run arca init --help.")
    if not objective:
        objective = input("Research objective: ").strip()
    if not next_action:
        next_action = input("Next executable action: ").strip()
    return objective, next_action


def print_result(command, result, args):
    if getattr(args, "json", False):
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    if command == "status":
        print(f"ARCA project: {result['root']}")
        print(f"Objective: {result['objective'] or '(not initialized)'}")
        print(f"Next action: {result['next_action'] or '(not recorded)'}")
        git = result["git"]
        if git["available"]:
            branch = git["branch"] or "(detached HEAD)"
            commit = (git["commit"] or "no commit")[:12]
            dirty = "modified" if git["dirty"] else "clean" if git["dirty"] is False else "unknown"
            print(f"Git: {branch} | {commit} | {dirty}")
            if git["status"]:
                print(git["status"])
        else:
            print("Git: unavailable")
        experiments = result["experiments"]
        counts = ", ".join(f"{key}={value}" for key, value in sorted(experiments["by_status"].items()))
        print(f"Experiments: {experiments['total']}" + (f" ({counts})" if counts else ""))
        print(f"Jobs: {result['job_status']}")
        for warning in result["warnings"]:
            print(f"WARNING: {warning}")
        if args.full:
            print(f"\n--- context/STATE.md ---\n{result['state']}")
            print(f"\n--- context/NEXT.md ---\n{result['next']}")
    elif command == "check":
        print_check(result)
    elif command == "init":
        print("ARCA initialization: " + ("updated " + ", ".join(result["updated"]) if result["updated"] else "already initialized"))
        print(f"Objective: {result['objective']}\nNext action: {result['next_action']}")
        print(result["note"])
    else:
        if command == "experiment":
            print(f"{result['experiment_id']} | planned")
        print(result["path"])
        print(result["note"])


def print_check(result, context_only=False):
    label = "context validation" if context_only else "ARCA check"
    state = "FAIL" if result["errors"] else "WARN" if result["warnings"] else "OK"
    print(f"{label}: {state}")
    for error in result["errors"]:
        print(f"ERROR: {error}")
    for warning in result["warnings"]:
        print(f"WARNING: {warning}")
    if not context_only:
        print("Scope: structure and selected references | CortexDB: optional, not checked")


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    try:
        root = core.find_root(getattr(args, "root", None))
        if args.command == "init":
            result = core.initialize(root, *init_arguments(root, args))
        elif args.command == "status":
            result = core.status(root)
        elif args.command == "check":
            result = core.validate(root)
        elif args.command == "checkpoint":
            result = core.checkpoint(root)
        else:
            result = core.new_experiment(root, args.title)
        print_result(args.command, result, args)
        if args.command == "check":
            return int(bool(result["errors"] or (args.strict and result["warnings"])))
        return 0
    except (core.ArcaError, OSError, UnicodeError, EOFError) as exc:
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        else:
            print(f"ARCA: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nARCA: interrupted.", file=sys.stderr)
        return 130
