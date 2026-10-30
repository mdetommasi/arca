"""Integration tests using disposable ARCA projects and real CLI processes."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from arca_cli import core
from arca_cli.cli import main


SOURCE = Path(__file__).resolve().parents[1]
STATE_TEMPLATE = """# Current Research State

Last updated: YYYY-MM-DD HH:MM

## Current objective

Descrivi l'obiettivo immediato e il suo legame con `research/CHARTER.md`.

## Current technical state

Preserve these unrelated technical notes.
"""
NEXT_TEMPLATE = """# Next Actions

Last updated: YYYY-MM-DD HH:MM

## Now

1. [ ] ...

## After that

1. [ ] Preserve the follow-up task.
"""


def fingerprint(root):
    return {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in root.rglob("*") if path.is_file() and "__pycache__" not in path.parts}


class CLITest(unittest.TestCase):
    def setUp(self):
        self.sandbox = tempfile.TemporaryDirectory(prefix="arca-cli-test-")
        self.addCleanup(self.sandbox.cleanup)
        self.root = Path(self.sandbox.name) / "project with spaces"
        self.root.mkdir()
        for relative in (*core.CHECK_FILES, "experiments/templates/experiment.yaml",
                         "experiments/templates/report.md", "arca"):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SOURCE / relative, destination)
        shutil.copytree(SOURCE / "arca_cli", self.root / "arca_cli", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(SOURCE / "scripts", self.root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        (self.root / "context/STATE.md").write_text(STATE_TEMPLATE, encoding="utf-8")
        (self.root / "context/NEXT.md").write_text(NEXT_TEMPLATE, encoding="utf-8")
        self.nested = self.root / "src/nested"
        self.nested.mkdir(parents=True)

    def run_cli(self, *args, cwd=None, expected=0):
        result = subprocess.run(
            [sys.executable, str(self.root / "arca"), *args], cwd=cwd or self.root,
            capture_output=True, text=True, input="", env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def init(self):
        return self.run_cli("init", "--objective", "Compare calibrated models.",
                            "--next-action", "Inspect data/registry.yaml.", "--json")

    def test_help_and_module_entrypoint(self):
        before = fingerprint(self.root)
        self.assertIn("experiment", self.run_cli("--help").stdout)
        result = subprocess.run([sys.executable, "-m", "arca_cli", "--version"], cwd=self.root,
                                capture_output=True, text=True,
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ARCA CLI", result.stdout)
        self.assertEqual(fingerprint(self.root), before)

    def test_root_discovery_and_read_only_operations(self):
        before = fingerprint(self.root)
        result = json.loads(self.run_cli("status", "--json", cwd=self.nested).stdout)
        self.assertEqual(result["root"], str(self.root.resolve()))
        self.assertIsNone(result["objective"])
        self.assertIsNone(result["next_action"])
        self.assertEqual(result["experiments"]["total"], 0)
        self.assertFalse(result["git"]["available"])
        self.assertIn("unknown", result["job_status"])
        self.assertTrue(json.loads(self.run_cli("check", "--json", cwd=self.nested).stdout)["ok"])
        self.assertEqual(fingerprint(self.root), before)

    def test_root_and_json_options_at_each_level(self):
        unrelated = Path(self.sandbox.name)
        for args in (
            ("--root", str(self.root), "--json", "status"),
            ("status", "--root", str(self.root), "--json"),
        ):
            result = json.loads(self.run_cli(*args, cwd=unrelated).stdout)
            self.assertEqual(result["root"], str(self.root.resolve()))
        result = json.loads(self.run_cli("experiment", "--root", str(self.root), "--json",
                                         "new", "pilot", cwd=unrelated).stdout)
        self.assertEqual(result["experiment_id"], "E-0001")

    def test_outside_project_and_missing_directory_fail_cleanly(self):
        result = self.run_cli("status", "--json", cwd=Path(self.sandbox.name), expected=1)
        self.assertIn("No ARCA project", json.loads(result.stdout)["error"])
        result = self.run_cli("status", "--json", "--root", str(self.root / "absent"), expected=1)
        self.assertIn("does not exist", json.loads(result.stdout)["error"])

    def test_initialization_preserves_other_sections_and_is_idempotent(self):
        result = json.loads(self.init().stdout)
        self.assertEqual(set(result["updated"]), {"research/CHARTER.md", "context/STATE.md", "context/NEXT.md"})
        self.assertIn("unrelated technical notes", (self.root / "context/STATE.md").read_text())
        self.assertIn("Preserve the follow-up task", (self.root / "context/NEXT.md").read_text())
        before = fingerprint(self.root)
        again = json.loads(self.run_cli("init", "--json").stdout)
        self.assertEqual(again["updated"], [])
        self.assertEqual(fingerprint(self.root), before)
        snapshot = json.loads(self.run_cli("status", "--json").stdout)
        self.assertEqual(snapshot["objective"], "Compare calibrated models.")
        self.assertEqual(snapshot["next_action"], "Inspect data/registry.yaml.")

    def test_initialization_conflict_has_no_partial_writes(self):
        path = self.root / "context/STATE.md"
        path.write_text(STATE_TEMPLATE.replace(core.PLACEHOLDERS["state"], "Existing research notes."))
        before = fingerprint(self.root)
        result = self.run_cli("init", "--objective", "New goal", "--next-action", "Review data",
                              "--json", expected=1)
        self.assertIn("preserves existing content", json.loads(result.stdout)["error"])
        self.assertEqual(fingerprint(self.root), before)

    def test_initialization_missing_section_has_no_partial_writes(self):
        path = self.root / "context/NEXT.md"
        path.write_text("# Custom next-action format\n")
        before = fingerprint(self.root)
        self.run_cli("init", "--objective", "New goal", "--next-action", "Review data", expected=1)
        self.assertEqual(fingerprint(self.root), before)

    def test_initialization_requires_values_without_interactive_input(self):
        before = fingerprint(self.root)
        result = self.run_cli("init", "--json", expected=1)
        self.assertIn("--objective", json.loads(result.stdout)["error"])
        self.assertEqual(fingerprint(self.root), before)

    def test_interactive_initialization(self):
        with mock.patch("sys.stdin.isatty", return_value=True), \
                mock.patch("builtins.input", side_effect=["Compare models", "Inspect the dataset"]), \
                mock.patch("sys.stdout", new_callable=io.StringIO) as output:
            code = main(["--root", str(self.root), "init"])
        self.assertEqual(code, 0, output.getvalue())
        self.assertIn("Compare models", (self.root / "research/CHARTER.md").read_text())

    def test_initialization_rejects_multiline_values(self):
        before = fingerprint(self.root)
        self.run_cli("init", "--objective", "Goal\n## forged section", "--next-action", "Review", expected=1)
        self.assertEqual(fingerprint(self.root), before)

    def test_structural_failure_and_strict_warning_exit_codes(self):
        path = self.root / "paper/CLAIMS.md"
        path.write_text("# Claim\n\nEvidence: E-0001\n")
        normal = json.loads(self.run_cli("check", "--json").stdout)
        self.assertTrue(normal["ok"])
        self.assertIn("E-0001", normal["warnings"][0])
        self.run_cli("check", "--strict", "--json", expected=1)
        (self.root / "context/NEXT.md").unlink()
        failed = json.loads(self.run_cli("check", "--json", expected=1).stdout)
        self.assertFalse(failed["ok"])
        self.assertIn("Missing: context/NEXT.md", failed["errors"])

    def test_invalid_registry_reports_actionable_error(self):
        (self.root / "experiments/REGISTRY.csv").write_text("not,a,registry\n")
        result = self.run_cli("check", "--json", expected=1)
        self.assertIn("experiment_id column", json.loads(result.stdout)["errors"][0])

    def test_experiments_share_ids_and_paths_with_legacy_script(self):
        title = 'Compare "baseline", path\\variant: α'
        result = json.loads(self.run_cli("experiment", "new", title, "--json", cwd=self.nested).stdout)
        folder = Path(result["path"])
        self.assertEqual(result["experiment_id"], "E-0001")
        self.assertEqual(json.loads((folder / "metrics.json").read_text()), {})
        self.assertIn("title: " + json.dumps(title, ensure_ascii=False), (folder / "experiment.yaml").read_text())
        self.assertIn("git_dirty: null", (folder / "experiment.yaml").read_text())
        legacy = subprocess.run([sys.executable, str(self.root / "scripts/new_experiment.py"), "legacy pilot"],
                                cwd=self.nested, capture_output=True, text=True)
        self.assertEqual(legacy.returncode, 0, legacy.stderr)
        self.assertTrue(Path(legacy.stdout.strip()).is_dir())
        self.assertIn("E-0002", legacy.stdout)
        with (self.root / "experiments/REGISTRY.csv").open(newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual([row["experiment_id"] for row in rows], ["E-0001", "E-0002"])
        self.assertEqual(rows[0]["title"], title)
        self.run_cli("check")

    def test_invalid_experiment_template_writes_nothing(self):
        (self.root / "experiments/templates/experiment.yaml").write_text("title: custom\n")
        before = fingerprint(self.root)
        self.run_cli("experiment", "new", "pilot", "--json", expected=1)
        self.assertEqual(fingerprint(self.root), before)

    def test_experiment_registry_column_order_is_preserved(self):
        path = self.root / "experiments/REGISTRY.csv"
        columns = path.read_text().strip().split(",")
        columns = list(reversed(columns)) + ["custom_annotation"]
        path.write_text(",".join(columns) + "\n")
        self.run_cli("experiment", "new", "reordered registry")
        with path.open(newline="") as handle:
            row = next(csv.DictReader(handle))
        self.assertEqual(row["experiment_id"], "E-0001")
        self.assertEqual(row["title"], "reordered registry")
        self.assertEqual(row["status"], "planned")
        self.assertEqual(row["custom_annotation"], "")
        self.run_cli("check")

    def test_unregistered_experiment_folder_prevents_id_reuse(self):
        (self.root / "experiments/E-0001-existing-pilot").mkdir()
        before = fingerprint(self.root)
        result = self.run_cli("experiment", "new", "another pilot", "--json", expected=1)
        self.assertIn("already uses E-0001", json.loads(result.stdout)["error"])
        self.assertEqual(fingerprint(self.root), before)

    def test_checkpoint_snapshots_existing_notes_with_unique_paths(self):
        before_state = (self.root / "context/STATE.md").read_bytes()
        before_next = (self.root / "context/NEXT.md").read_bytes()
        first = json.loads(self.run_cli("checkpoint", "--json").stdout)
        second = json.loads(self.run_cli("checkpoint", "--json").stdout)
        self.assertNotEqual(first["path"], second["path"])
        self.assertIn(STATE_TEMPLATE, Path(first["path"]).read_text())
        self.assertIn(NEXT_TEMPLATE, Path(first["path"]).read_text())
        self.assertEqual((self.root / "context/STATE.md").read_bytes(), before_state)
        self.assertEqual((self.root / "context/NEXT.md").read_bytes(), before_next)
        legacy = subprocess.run([sys.executable, str(self.root / "scripts/session_checkpoint.py")],
                                cwd=self.nested, capture_output=True, text=True)
        self.assertEqual(legacy.returncode, 0, legacy.stderr)
        self.assertTrue(Path(legacy.stdout.strip()).is_file())

    def test_checkpoint_failure_does_not_create_archive(self):
        (self.root / "context/NEXT.md").unlink()
        self.run_cli("checkpoint", "--json", expected=1)
        self.assertFalse((self.root / "context/session_archive").exists())

    def test_status_selects_first_unfinished_action(self):
        (self.root / "context/NEXT.md").write_text(
            "# Next\n\n## Now\n\n1. [x] Finished\n2. [ ] Inspect metrics\n3. [ ] Review findings\n"
        )
        value = json.loads(self.run_cli("status", "--json").stdout)
        self.assertEqual(value["next_action"], "Inspect metrics")
        self.assertIn(STATE_TEMPLATE, self.run_cli("status", "--full").stdout)

    @unittest.skipUnless(shutil.which("git"), "Git not installed")
    def test_real_git_status_and_provenance_without_mutation(self):
        def git(*args):
            result = subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            return result.stdout.strip()
        git("init", "-q")
        git("add", ".")
        git("-c", "user.name=ARCA test", "-c", "user.email=arca@example.invalid",
            "-c", "commit.gpgsign=false", "commit", "-qm", "fixture")
        before = fingerprint(self.root)
        status = json.loads(self.run_cli("status", "--json").stdout)
        self.assertFalse(status["git"]["dirty"])
        self.assertEqual(status["git"]["commit"], git("rev-parse", "HEAD"))
        self.assertEqual(fingerprint(self.root), before)
        (self.root / "context/STATE.md").write_text(STATE_TEMPLATE + "\nA new observation.\n")
        result = json.loads(self.run_cli("experiment", "new", "dirty pilot", "--json").stdout)
        config = (Path(result["path"]) / "experiment.yaml").read_text()
        self.assertIn("git_dirty: true", config)
        self.assertIn(git("rev-parse", "HEAD"), config)

    def test_legacy_validators(self):
        for script in ("arca_check.py", "validate_context.py"):
            result = subprocess.run([sys.executable, str(self.root / "scripts" / script)],
                                    cwd=self.nested, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
