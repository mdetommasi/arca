"""Isolated installation contracts: never touch live user configuration/network."""
from __future__ import annotations

import io
import json
import os
from pathlib import Path
import shutil
import tarfile
import tempfile
import unittest
from unittest import mock
import urllib.error

from scripts.arca_cli import core, integrations as optional
from scripts.arca_cli.cli import main


SOURCE = Path(__file__).resolve().parents[1]
BINARY = b"test MCP binary\n"


def archive(extra=None):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as handle:
        files = {f"prompts/{name}.md": f"Workflow {name}: $@\n" for name in optional.WORKFLOWS}
        files.update({f".feynman/agents/{name}.md": name for name in
                      ("researcher", "verifier", "reviewer", "writer")})
        files["LICENSE"] = "MIT test fixture"
        files["skills/literature-review/SKILL.md"] = "Original skill"
        files["src/unused.ts"] = "Must not be installed"
        for name, content in files.items():
            info = tarfile.TarInfo("feynman-test/" + name)
            data = content.encode()
            info.size = len(data)
            handle.addfile(info, io.BytesIO(data))
        if extra:
            handle.addfile(extra)
    return buffer.getvalue()


def fingerprint(path):
    return {str(p.relative_to(path)): p.read_bytes() for p in path.rglob("*") if p.is_file()}


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="arca-integrations-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / "project with spaces"
        self.home = self.base / "user home"
        self.root.mkdir()
        self.home.mkdir()
        (self.root / "framework.yaml").write_text("name: ARCA\n")
        self.enterContext(mock.patch.object(Path, "home", return_value=self.home))
        self.enterContext(mock.patch.dict(os.environ))
        os.environ.pop("CODEX_HOME", None)
        os.environ.pop("CLAUDE_CONFIG_DIR", None)
        self.enterContext(mock.patch.object(optional.platform, "system", return_value="Linux"))
        self.enterContext(mock.patch.object(optional.platform, "machine", return_value="x86_64"))
        self.enterContext(mock.patch.dict(optional.CORTEX_HASHES, {"linux-amd64": optional.digest(BINARY)}))
        self.bundle = archive()
        self.enterContext(mock.patch.object(optional, "FEYNMAN_SHA256", optional.digest(self.bundle)))
        self.fetch = self.enterContext(mock.patch.object(optional, "download", side_effect=
            lambda url, expected: self.bundle if "codeload" in url else BINARY))

    def enterContext(self, cm):
        # unittest.TestCase.enterContext was introduced after Python 3.9.
        result = cm.__enter__()
        self.addCleanup(cm.__exit__, None, None, None)
        return result

    def install(self, names=("cortexdb", "feynman"), scope="project", agents=("claude", "codex")):
        return optional.install(self.root, names, scope, agents)

    def cli(self, *args, expected=0):
        with mock.patch("sys.stdout", new_callable=io.StringIO) as output:
            code = main(["--root", str(self.root), *args, "--json"])
        self.assertEqual(code, expected, output.getvalue())
        return json.loads(output.getvalue())

    def test_preview_is_offline_and_read_only(self):
        before = fingerprint(self.base)
        result = self.cli("integrations", "install", "cortexdb", "feynman", "--dry-run")
        self.assertTrue(result["dry_run"])
        self.assertEqual(result["agents"], ["claude", "codex"])
        self.assertEqual(fingerprint(self.base), before)
        self.fetch.assert_not_called()

    def test_project_install_connects_both_hosts_to_same_database_and_is_idempotent(self):
        result = self.install()
        config = json.loads((self.root / ".mcp.json").read_text())["mcpServers"]["cortexdb"]
        self.assertEqual(config["env"]["CORTEXDB_PATH"], str(self.root / ".local/cortexdb/brain.db"))
        self.assertEqual(config["env"]["CORTEXDB_REMOTE"], "")
        toml = (self.root / ".codex/config.toml").read_text()
        self.assertIn(json.dumps(config["command"]), toml)
        self.assertIn(json.dumps(config["env"]["CORTEXDB_PATH"]), toml)
        self.assertTrue(os.access(config["command"], os.X_OK))
        for agent in (".agents", ".claude"):
            folder = self.root / agent / "skills/feynman"
            self.assertIn("ARCA host adapter", (folder / "SKILL.md").read_text())
            self.assertTrue((folder / "upstream/prompts/lit.md").is_file())
            self.assertTrue((folder / "upstream/agents/researcher.md").is_file())
            self.assertFalse((folder / "upstream/src").exists())
            self.assertFalse((folder / "upstream/skills").exists())
        self.assertTrue(optional.status(self.root)["ok"])
        self.assertEqual(fingerprint(self.home), {})
        self.assertTrue(result["changed"])
        before = fingerprint(self.base)
        self.fetch.reset_mock()
        repeated = self.install()
        self.assertEqual(repeated["changed"], [])
        self.assertEqual(fingerprint(self.base), before)
        self.fetch.assert_not_called()

    def test_user_scope_respects_host_directories_and_does_not_change_project(self):
        os.environ["CODEX_HOME"] = str(self.home / "custom codex")
        os.environ["CLAUDE_CONFIG_DIR"] = str(self.home / "custom claude")
        before = fingerprint(self.root)
        self.install(scope="user")
        self.assertEqual(fingerprint(self.root), before)
        self.assertTrue((self.home / "custom codex/config.toml").is_file())
        self.assertTrue((self.home / "custom claude/.claude.json").is_file())
        self.assertTrue((self.home / ".agents/skills/feynman/SKILL.md").is_file())
        self.assertTrue((self.home / "custom claude/skills/feynman/SKILL.md").is_file())
        self.assertTrue(optional.status(self.root, "user")["ok"])
        self.assertEqual(optional.status(self.root)["integrations"], {})

    def test_user_cli_install_works_outside_an_arca_project(self):
        with mock.patch.object(Path, "cwd", return_value=self.home), \
                mock.patch("sys.stdout", new_callable=io.StringIO) as output:
            code = main(["integrations", "install", "feynman", "--scope", "user", "--json"])
        self.assertEqual(code, 0, output.getvalue())
        self.assertEqual(json.loads(output.getvalue())["scope"], "user")

    def test_adding_second_host_preserves_first_host(self):
        self.install(agents=["claude"])
        self.assertFalse((self.root / ".codex").exists())
        before = (self.root / ".mcp.json").read_bytes()
        self.install(agents=["codex"])
        self.assertEqual((self.root / ".mcp.json").read_bytes(), before)
        self.assertEqual(optional.status(self.root)["integrations"]["cortexdb"]["agents"], ["claude", "codex"])

    def test_existing_unrelated_config_and_later_edits_are_preserved(self):
        claude = self.root / ".mcp.json"
        other = {"mcpServers": {"other": {"command": "existing"}}, "otherSetting": True}
        claude.write_text(json.dumps(other))
        codex = self.root / ".codex/config.toml"
        codex.parent.mkdir()
        prefix = '# existing comment\nmodel = "custom"\n[mcp_servers.other]\ncommand = "existing"\n'
        codex.write_text(prefix)
        result = self.install()
        backup = Path(result["backup_dir"])
        self.assertIn(str(claude), json.loads((backup / "index.json").read_text()).values())
        new = json.loads(claude.read_text())
        self.assertEqual(new["mcpServers"]["other"], other["mcpServers"]["other"])
        self.assertTrue(new["otherSetting"])
        self.assertTrue(codex.read_text().startswith(prefix))
        codex.write_text(codex.read_text().replace('model = "custom"', 'model = "changed"'))
        new["unrelatedLater"] = 1
        claude.write_text(json.dumps(new))
        self.install()
        self.assertEqual(json.loads(claude.read_text())["unrelatedLater"], 1)
        self.assertIn('model = "changed"', codex.read_text())

    def test_conflicting_server_blocks_all_installation_before_network(self):
        config = self.root / ".mcp.json"
        config.write_text('{"mcpServers": {"cortexdb": {"command": "my-server"}}}')
        before = fingerprint(self.base)
        with self.assertRaisesRegex(core.ArcaError, "already exists"):
            self.install()
        self.assertEqual(fingerprint(self.base), before)
        self.fetch.assert_not_called()

    def test_invalid_configs_are_not_replaced(self):
        config = self.root / ".mcp.json"
        for content in ("{bad", "[]", '{"mcpServers": []}'):
            with self.subTest(content=content):
                config.write_text(content)
                before = fingerprint(self.base)
                with self.assertRaises(core.ArcaError):
                    self.install()
                self.assertEqual(fingerprint(self.base), before)

    def test_codex_inline_and_quoted_existing_server_conflicts(self):
        config = self.root / ".codex/config.toml"
        config.parent.mkdir()
        for content in ('mcp_servers = {other = {command = "other"}}\n',
                        '[mcp_servers."cortexdb"]\ncommand = "other"\n',
                        '["mcp_servers"]\n"cortexdb" = { command = "other" }\n'):
            with self.subTest(content=content):
                config.write_text(content)
                before = fingerprint(self.base)
                with self.assertRaises(core.ArcaError):
                    self.install()
                self.assertEqual(fingerprint(self.base), before)

    def test_external_skill_directory_is_preserved(self):
        folder = self.root / ".claude/skills/feynman"
        folder.mkdir(parents=True)
        (folder / "SKILL.md").write_text("My existing Feynman skill")
        before = fingerprint(self.base)
        with self.assertRaisesRegex(core.ArcaError, "outside this installation"):
            self.install()
        self.assertEqual(fingerprint(self.base), before)

    def test_local_edits_are_reported_and_never_silently_replaced(self):
        self.install()
        skill = self.root / ".agents/skills/feynman/upstream/prompts/lit.md"
        skill.write_text("User changes")
        before = fingerprint(self.base)
        result = optional.status(self.root)
        self.assertFalse(result["ok"])
        with self.assertRaisesRegex(core.ArcaError, "local changes"):
            self.install()
        self.assertEqual(fingerprint(self.base), before)
        self.cli("integrations", "status", expected=1)

    def test_changed_managed_configuration_is_preserved(self):
        self.install()
        path = self.root / ".codex/config.toml"
        path.write_text(path.read_text().replace("startup_timeout_sec = 30", "startup_timeout_sec = 90"))
        before = fingerprint(self.base)
        self.assertFalse(optional.status(self.root)["ok"])
        with self.assertRaisesRegex(core.ArcaError, "local changes"):
            self.install()
        self.assertEqual(fingerprint(self.base), before)

    def test_missing_resource_is_repaired_from_verified_cache(self):
        self.install()
        path = self.root / ".agents/skills/feynman/upstream/prompts/lit.md"
        path.unlink()
        self.assertFalse(optional.status(self.root)["ok"])
        self.fetch.reset_mock()
        self.install()
        self.fetch.assert_not_called()
        self.assertTrue(optional.status(self.root)["ok"])

    def test_moved_project_refreshes_paths_without_redownload_or_losing_memory(self):
        self.install()
        db = self.root / ".local/cortexdb/brain.db"
        db.parent.mkdir(parents=True)
        db.write_bytes(b"existing database")
        previous = self.root
        self.root = self.base / "moved project"
        previous.rename(self.root)
        self.assertFalse(optional.status(self.root)["ok"])
        with self.assertRaisesRegex(core.ArcaError, "reinstall all"):
            self.install(names=["feynman"])
        self.fetch.reset_mock()
        self.install()
        self.fetch.assert_not_called()
        self.assertTrue(optional.status(self.root)["ok"])
        server = json.loads((self.root / ".mcp.json").read_text())["mcpServers"]["cortexdb"]
        self.assertTrue(server["command"].startswith(str(self.root)))
        self.assertEqual(Path(server["env"]["CORTEXDB_PATH"]).read_bytes(), b"existing database")

    def test_download_failure_has_no_partial_configuration(self):
        self.fetch.side_effect = [BINARY, core.ArcaError("Network unavailable")]
        before = fingerprint(self.base)
        with self.assertRaisesRegex(core.ArcaError, "Network unavailable"):
            self.install()
        self.assertEqual(fingerprint(self.base), before)

    def test_failed_write_rolls_back_changed_configs(self):
        (self.root / ".mcp.json").write_text('{"mcpServers":{}}\n')
        original = (self.root / ".mcp.json").read_bytes()
        real_write = optional.atomic_write

        def fail_skill(path, data, mode):
            if path == self.root / ".claude/skills/cortexdb/SKILL.md":
                raise OSError("simulated full disk")
            real_write(path, data, mode)

        with mock.patch.object(optional, "atomic_write", side_effect=fail_skill):
            with self.assertRaisesRegex(OSError, "full disk"):
                self.install()
        self.assertEqual((self.root / ".mcp.json").read_bytes(), original)
        self.assertFalse((self.root / ".codex/config.toml").exists())
        self.assertFalse((self.root / ".local/arca/integrations/manifest.json").exists())

    def test_concurrent_edit_is_detected_before_writes(self):
        path = self.root / ".mcp.json"

        def edit_during_download(url, expected):
            path.write_text('{"newSetting": 1}')
            return BINARY

        self.fetch.side_effect = edit_during_download
        with self.assertRaisesRegex(core.ArcaError, "changed during installation"):
            self.install(names=["cortexdb"])
        self.assertEqual(json.loads(path.read_text()), {"newSetting": 1})
        self.assertFalse((self.root / ".codex/config.toml").exists())

    def test_symlink_targets_are_not_followed(self):
        target = self.base / "external.json"
        target.write_text("{}")
        (self.root / ".mcp.json").symlink_to(target)
        with self.assertRaisesRegex(core.ArcaError, "symlink"):
            self.install()
        self.assertEqual(target.read_text(), "{}")

    def test_installation_lock_is_respected(self):
        state = optional.locations(self.root, "project")["state"]
        state.mkdir(parents=True)
        lock = state / "install.lock"
        lock.write_text("other process")
        with self.assertRaisesRegex(core.ArcaError, "lock exists"):
            self.install()
        self.assertEqual(lock.read_text(), "other process")
        self.fetch.assert_not_called()

    def test_unsupported_binary_platform_is_actionable_but_feynman_still_installs(self):
        with mock.patch.object(optional.platform, "machine", return_value="riscv64"):
            with self.assertRaisesRegex(core.ArcaError, "No pinned CortexDB binary"):
                self.install()
            self.install(names=["feynman"])
        self.assertFalse((self.root / ".mcp.json").exists())

    def test_init_preflights_research_notes_before_installation(self):
        for name in ("research/CHARTER.md", "context/STATE.md", "context/NEXT.md"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SOURCE / name, path)
        state = self.root / "context/STATE.md"
        state.write_text(state.read_text().replace(core.PLACEHOLDERS["state"], "Existing notes"))
        before = fingerprint(self.base)
        result = self.cli("init", "--objective", "Test objective", "--next-action", "Inspect data",
                          "--with", "cortexdb", "feynman", expected=1)
        self.assertIn("preserves existing content", result["error"])
        self.assertEqual(fingerprint(self.base), before)
        self.fetch.assert_not_called()

    def test_init_install_failure_preserves_notes_and_success_initializes(self):
        for name in ("research/CHARTER.md", "context/STATE.md", "context/NEXT.md"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SOURCE / name, path)
        args = ("init", "--objective", "Test objective", "--next-action", "Inspect data", "--with", "cortexdb")
        before = fingerprint(self.base)
        self.fetch.side_effect = core.ArcaError("Network unavailable")
        self.cli(*args, expected=1)
        self.assertEqual(fingerprint(self.base), before)
        self.fetch.side_effect = lambda url, expected: BINARY
        result = self.cli(*args)
        self.assertEqual(result["objective"], "Test objective")
        self.assertTrue(result["integrations"]["changed"])
        self.assertIn("Test objective", (self.root / "context/STATE.md").read_text())


class DownloadAndArchiveTest(unittest.TestCase):
    def test_checksum_mismatch_and_network_errors_fail_closed(self):
        with mock.patch.object(optional.urllib.request, "urlopen", return_value=io.BytesIO(b"wrong")):
            with self.assertRaisesRegex(core.ArcaError, "SHA-256 mismatch"):
                optional.download("https://example.test/asset", optional.digest(b"right"))
        with mock.patch.object(optional.urllib.request, "urlopen", side_effect=urllib.error.URLError("offline")):
            with self.assertRaisesRegex(core.ArcaError, "Download failed"):
                optional.download("https://example.test/asset", "unused")

    def test_archive_rejects_links_and_traversal(self):
        link = tarfile.TarInfo("feynman-test/prompts/evil.md")
        link.type = tarfile.SYMTYPE
        link.linkname = "/tmp/outside"
        traversal = tarfile.TarInfo("feynman-test/prompts/../../outside")
        for extra in (link, traversal):
            with self.subTest(name=extra.name):
                with self.assertRaises(core.ArcaError):
                    optional.feynman_files(archive(extra))

    def test_archive_requires_complete_workflow_bundle(self):
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode="w:gz"):
            pass
        with self.assertRaisesRegex(core.ArcaError, "missing required"):
            optional.feynman_files(buffer.getvalue())
        with self.assertRaisesRegex(core.ArcaError, "Invalid Feynman archive"):
            optional.feynman_files(b"not gzip")


if __name__ == "__main__":
    unittest.main()
