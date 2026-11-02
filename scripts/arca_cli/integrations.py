"""Optional, pinned integrations for native Claude Code and Codex sessions.

No host CLI, shell installer, package manager, or model call is needed. All
downloads are staged and checked before any agent configuration is changed.
"""
from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import stat
import tarfile
import tempfile
import urllib.error
import urllib.request
import uuid

from .core import ArcaError


CORTEX_VERSION = "2.142.0"
FEYNMAN_VERSION = "0.5.61"
FEYNMAN_COMMIT = "89b0242919faf89b38dcb6ae8be92f6dbcd77203"
FEYNMAN_SHA256 = "a6c40eb85761ad6e0815ded1e7da0420a529bca1e7959910f5221db352bde855"
CORTEX_HASHES = {
    "darwin-amd64": "393506e13fd77cf1854c571e58c1d18e9d91af41f9653163f27b978427d0af27",
    "darwin-arm64": "5f5bc744f04027dfd518cf61717881ac13ae11b148e96dbe7bd49e0eb57edee7",
    "linux-amd64": "2370da21cc7ae05f4beda7f51a33e5fd164fb30f46c30a1a3e950afed20f815e",
    "linux-arm64": "9fc0563f15e32c288e86e92d52100cf8b5c1a90d87fc17c152f5be0c9d66128a",
    "windows-amd64": "eb31d2299ede094cd72bbab562adf5508ea2387308d7a488cdccf304984e3bbc",
    "windows-arm64": "bc3aee7f90889dd98bb35e9593d1e5d76d69cd5fe114d377dfc5b524fd5ffdc3",
}
WORKFLOWS = ("lit", "deepresearch", "review", "audit", "replicate", "recipe",
             "compare", "draft", "autoresearch", "summarize", "log")
BEGIN = "# BEGIN ARCA cortexdb (managed)"
END = "# END ARCA cortexdb (managed)"
FEYNMAN_SKILL = """---
name: feynman
description: Use Feynman's research workflows for literature reviews, deep research, paper review, replication planning, training recipes, comparison, and drafting inside the current coding agent.
---

# Feynman research workflows · ARCA host adapter

Invoke as `/feynman lit <topic>` in Claude Code or `$feynman lit <topic>`
in Codex. The first argument selects a workflow; the rest is the research
request. If no workflow is specified, infer the closest one from that request.

Read only the selected `upstream/prompts/<workflow>.md`, relative to this
SKILL.md. Supported workflows: lit, deepresearch, review, audit, replicate,
recipe, compare, draft, autoresearch, summarize, log. Replace `$@` in the
prompt with the user's request. These are instruction files, not native
slash commands: do not invoke `/lit` or a `feynman` executable.

## Host adaptation

The upstream prompts target Feynman's Pi runtime. Apply these adaptations:
- Use the current host's available search, browsing, file, and shell tools.
  Pi-specific tools such as `feynman_science_database_search`, `subagent`,
  `runs.all`, and `feynman alpha` are not installed by this skills edition.
  Use available primary-source search instead; report unavailable capabilities.
- If delegation is available and authorized, read the relevant role from
  `upstream/agents/{researcher,verifier,reviewer,writer}.md` and translate it
  to the host's delegation API. Otherwise perform stages sequentially and
  disclose that review was not independent. Never run Pi workflow JavaScript.
- Preserve the active repository's instructions, scientific protocol, and
  user constraints. Installation does not authorize experiments or paid jobs.
  For replication/autoresearch, establish the environment and run budget first.
  In ARCA, allocate an experiment before a measured run and keep upstream
  `autoresearch.*` files inside that experiment directory.
- In ARCA projects, map upstream `outputs/` to `research/feynman/`,
  `notes/` to `research/feynman/notes/`, and `papers/` to `paper/drafts/`.
  Keep provenance sidecars and intermediate files under those same mappings.
  Link accepted findings to ARCA records; external claims are not measured facts.
  In other repositories, use their output conventions or the upstream paths.

Original prompts and role descriptions are preserved under `upstream/` with
their license. This adapter supplies workflow instructions, not the standalone
Feynman terminal app, its model login, custom tools, or telemetry runtime.
"""
CORTEX_SKILL = """---
name: cortexdb
description: Recall or save research memory through the configured CortexDB MCP server, verifying recalled evidence against canonical project records.
---

# CortexDB memory

Use the `cortexdb` MCP server configured by ARCA. For recall, discover and use
`knowledge_memory_recall`, `memory_search`, or `knowledge_search` as appropriate.
For an explicit save request, use `memory_save` or `knowledge_save` with source
paths and epistemic status. Use the actual tool schemas exposed by the server.
If tools are absent, report the connection problem and ask the user to reopen
the agent session and inspect MCP status; do not pretend a local file is MCP.

Git-backed ARCA records remain canonical. Verify consequential recalled claims
against their source files. Follow `memory/MEMORY_POLICY.md` when present.
Never bulk-import transcripts or enable capture hooks as part of a recall/save.
The configured database is shared by Claude and Codex within the chosen scope.
User scope shares memory across projects: include project identity in records
and verify that recalled evidence belongs to the current project.
"""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def download(url, expected):
    request = urllib.request.Request(url, headers={"User-Agent": "ARCA-integrations/1"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read(200 * 1024 * 1024 + 1)
    except (urllib.error.URLError, TimeoutError) as exc:
        raise ArcaError(f"Download failed for {url}: {exc}. Rerun the installation to retry.") from exc
    if len(data) > 200 * 1024 * 1024:
        raise ArcaError(f"Download exceeds the 200 MiB limit: {url}")
    if digest(data) != expected:
        raise ArcaError(f"SHA-256 mismatch for {url}; nothing has been installed.")
    return data


def locations(root, scope):
    home = Path.home().resolve()
    base = root if scope == "project" else home
    state = (root / ".local/arca/integrations" if scope == "project"
             else home / ".local/share/arca/integrations")
    codex_dir = (root / ".codex" if scope == "project" else
                 Path(os.environ.get("CODEX_HOME", str(home / ".codex"))).expanduser().resolve())
    claude_dir = (root / ".claude" if scope == "project" else
                  Path(os.environ.get("CLAUDE_CONFIG_DIR", str(home / ".claude"))).expanduser().resolve())
    # Claude's custom config directory contains .claude.json; otherwise it is in HOME.
    claude_config = (root / ".mcp.json" if scope == "project" else
                     claude_dir / ".claude.json" if os.environ.get("CLAUDE_CONFIG_DIR")
                     else home / ".claude.json")
    return {"state": state, "codex_config": codex_dir / "config.toml",
            "claude_config": claude_config,
            "codex_skills": base / ".agents/skills", "claude_skills": claude_dir / "skills",
            "database": (root / ".local/cortexdb/brain.db" if scope == "project"
                         else home / ".cortexdb/cortexdb.db")}


def plan(root, names, scope="project", agents=("claude", "codex")):
    if scope not in ("project", "user") or not names or set(names) - {"cortexdb", "feynman"}:
        raise ArcaError("Choose cortexdb and/or feynman and scope project or user.")
    if not agents or set(agents) - {"claude", "codex"}:
        raise ArcaError("Choose claude and/or codex.")
    if scope == "project" and not (root / "framework.yaml").is_file():
        raise ArcaError("Project installation requires an ARCA scaffold (framework.yaml).")
    paths = locations(root, scope)
    items = []
    for name in sorted(set(names)):
        item = {"name": name, "version": CORTEX_VERSION if name == "cortexdb" else FEYNMAN_VERSION,
                "skills": [str(paths[f"{agent}_skills"] / name) for agent in sorted(set(agents))]}
        if name == "cortexdb":
            system = platform.system().lower()
            arch = {"x86_64": "amd64", "amd64": "amd64", "aarch64": "arm64",
                    "arm64": "arm64"}.get(platform.machine().lower())
            target = f"{system}-{arch}"
            if target not in CORTEX_HASHES:
                raise ArcaError(f"No pinned CortexDB binary for {system}/{platform.machine()}.")
            filename = f"cortexdb-mcp-{target}" + (".exe" if system == "windows" else "")
            item.update(url=f"https://github.com/liliang-cn/cortexdb/releases/download/v{CORTEX_VERSION}/{filename}",
                        sha256=CORTEX_HASHES[target], binary=str(paths["state"] / "bin" / filename),
                        database=str(paths["database"]),
                        configs=[str(paths[f"{agent}_config"]) for agent in sorted(set(agents))],
                        edition="stdio MCP and memory skill; no hooks")
        else:
            item.update(url=f"https://codeload.github.com/Companion-Inc/feynman/tar.gz/{FEYNMAN_COMMIT}",
                        sha256=FEYNMAN_SHA256, commit=FEYNMAN_COMMIT,
                        edition="research workflows (skills edition)")
        items.append(item)
    return {"ok": True, "scope": scope, "agents": sorted(set(agents)), "integrations": items,
            "manifest": str(paths["state"] / "manifest.json"), "dry_run": True,
            "note": "Preview only: no downloads, writes, or live connection checks."}


def read_json(path):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise ArcaError(f"Invalid JSON in {path}; preserve and repair it before retrying.") from exc
    if not isinstance(value, dict):
        raise ArcaError(f"Expected a JSON object in {path}.")
    return value


def load_manifest(path):
    if not path.exists():
        return {"schema": 1, "files": {}, "configs": {}, "integrations": {}}
    value = read_json(path)
    if value.get("schema") != 1 or any(not isinstance(value.get(k), dict)
                                      for k in ("files", "configs", "integrations")):
        raise ArcaError(f"Unsupported or invalid installation manifest: {path}")
    return value


def feynman_files(archive):
    """Read only workflow resources, without extracting archive paths to disk."""
    files = {"SKILL.md": FEYNMAN_SKILL.encode()}
    total = 0
    try:
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as source:
            for member in source:
                parts = PurePosixPath(member.name).parts
                if len(parts) < 2:
                    continue
                relative = PurePosixPath(*parts[1:])
                selected = (relative.as_posix() == "LICENSE" or
                            relative.parts[0] == "prompts" or
                            relative.parts[:2] == (".feynman", "agents"))
                if not selected:
                    continue
                if ".." in parts or "\\" in member.name or member.name.startswith("/"):
                    raise ArcaError("Unsafe path in Feynman archive.")
                if member.isdir():
                    continue
                if not member.isfile():
                    raise ArcaError("Feynman resources must be regular files, not links.")
                total += member.size
                if total > 10 * 1024 * 1024:
                    raise ArcaError("Feynman workflow resources exceed 10 MiB.")
                target = relative.as_posix().replace(".feynman/agents/", "agents/", 1)
                key = "upstream/" + target
                if key in files:
                    raise ArcaError(f"Duplicate resource in Feynman archive: {target}")
                files[key] = source.extractfile(member).read()
    except (tarfile.TarError, EOFError) as exc:
        raise ArcaError(f"Invalid Feynman archive: {exc}") from exc
    required = [f"upstream/prompts/{name}.md" for name in WORKFLOWS]
    required += [f"upstream/agents/{name}.md" for name in ("researcher", "verifier", "reviewer", "writer")]
    required += ["upstream/LICENSE"]
    if any(name not in files for name in required):
        raise ArcaError("Feynman archive is missing required workflows, roles, or license.")
    return files


def managed_block(text):
    if BEGIN not in text and END not in text:
        return ""
    pattern = re.escape(BEGIN) + r"\n.*?\n" + re.escape(END) + r"\n?"
    matches = list(re.finditer(pattern, text, re.DOTALL))
    if len(matches) != 1 or text.count(BEGIN) != 1 or text.count(END) != 1:
        raise ArcaError("Malformed ARCA block in Codex configuration; preserve and repair it first.")
    return matches[0].group()


def codex_config(original, server, owned):
    text = original.decode("utf-8")
    block = managed_block(text)
    if block and digest(block.encode()) != owned.get("sha256"):
        raise ArcaError("Codex's ARCA CortexDB block has local changes or is not owned by this installation.")
    remaining = text.replace(block, "", 1) if block else text
    # Conservative also for quoted/dotted keys, inline tables, and Python 3.9/3.10.
    if re.search(r"cortexdb", remaining, re.IGNORECASE):
        raise ArcaError("Codex already mentions CortexDB outside ARCA's managed block; review that configuration first.")
    if re.search(r"(?m)^\s*[\"']?mcp_servers[\"']?\s*=", remaining):
        raise ArcaError("Codex uses an inline mcp_servers table; convert it to [mcp_servers.NAME] tables first.")
    new = (f"{BEGIN}\n[mcp_servers.cortexdb]\ncommand = {json.dumps(server['command'], ensure_ascii=False)}\n"
           f"args = []\nstartup_timeout_sec = 30\n[mcp_servers.cortexdb.env]\n"
           + "".join(f"{key} = {json.dumps(value, ensure_ascii=False)}\n" for key, value in server["env"].items())
           + END + "\n")
    updated = text.replace(block, new, 1) if block else text + ("\n" if text else "") + new
    try:
        import tomllib
    except ImportError:
        pass  # New tables use a fixed TOML grammar; existing content is preserved.
    else:
        try:
            tomllib.loads(updated)
        except tomllib.TOMLDecodeError as exc:
            raise ArcaError(f"Invalid Codex TOML configuration: {exc}") from exc
    return updated.encode(), {"kind": "toml", "sha256": digest(new.encode())}


def claude_config(original, server, owned):
    try:
        config = json.loads(original) if original else {}
    except (ValueError, UnicodeError) as exc:
        raise ArcaError("Invalid Claude JSON configuration; preserve and repair it first.") from exc
    if not isinstance(config, dict) or not isinstance(config.get("mcpServers", {}), dict):
        raise ArcaError("Claude configuration and mcpServers must be JSON objects.")
    servers = config.setdefault("mcpServers", {})
    if "cortexdb" in servers and digest(json_bytes(servers["cortexdb"])) != owned.get("sha256"):
        raise ArcaError("Claude's cortexdb server already exists or has local changes; review it first.")
    servers["cortexdb"] = server
    return json_bytes(config), {"kind": "json", "sha256": digest(json_bytes(server))}


def ensure_regular(path):
    for candidate in (path, *path.parents):
        if candidate.is_symlink():
            raise ArcaError(f"Refusing to replace or write through a symlink: {candidate}")
    if path.exists() and not path.is_file():
        raise ArcaError(f"Expected a regular file: {path}")


def atomic_write(path, data, mode):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".arca-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def install_lock(state):
    ensure_regular(state / "install.lock")
    state.mkdir(parents=True, exist_ok=True)
    lock = state / "install.lock"
    try:
        handle = lock.open("x")
    except FileExistsError as exc:
        raise ArcaError(f"Installation lock exists: {lock}. If no installer is running, remove the stale lock and retry.") from exc
    try:
        with handle:
            handle.write(str(os.getpid()))
        yield
    finally:
        lock.unlink(missing_ok=True)


def install(root, names, scope="project", agents=("claude", "codex"), dry_run=False):
    result = plan(root, names, scope, agents)
    if dry_run:
        return result
    paths = locations(root, scope)
    with install_lock(paths["state"]):
        return _install(root, result, paths)


def _install(root, result, paths):
    manifest_path = Path(result["manifest"])
    ensure_regular(manifest_path)
    manifest = load_manifest(manifest_path)
    previous_root = manifest.get("root")
    if result["scope"] == "project" and previous_root and previous_root != str(root):
        required_names = set(manifest["integrations"])
        required_agents = {agent for item in manifest["integrations"].values() for agent in item["agents"]}
        if (required_names - {item["name"] for item in result["integrations"]}
                or required_agents - set(result["agents"])):
            raise ArcaError("Project moved: reinstall all previously installed integrations and hosts together to refresh paths.")
        for group in ("files", "configs"):
            try:
                manifest[group] = {str(root / Path(path).relative_to(previous_root)): value
                                   for path, value in manifest[group].items()}
            except ValueError as exc:
                raise ArcaError("Installation manifest has paths outside its previous project root.") from exc
    pending, originals, modes = {}, {}, {}

    def prepare(path, data, mode=0o644, owned_file=False):
        ensure_regular(path)
        old = path.read_bytes() if path.exists() else None
        if owned_file and old is not None and old != data and digest(old) != manifest["files"].get(str(path)):
            raise ArcaError(f"Existing file is not owned by ARCA or has local changes: {path}")
        originals[path] = old
        modes[path] = stat.S_IMODE(path.stat().st_mode) if old is not None else mode
        if old != data or (mode == 0o755 and os.name != "nt" and not modes[path] & 0o111):
            pending[path] = (data, mode if mode == 0o755 else modes[path])
        if owned_file:
            manifest["files"][str(path)] = digest(data)

    # Preflight host configurations before downloads. Only our named server is merged.
    for item in result["integrations"]:
        if item["name"] != "cortexdb":
            continue
        server = {"type": "stdio", "command": item["binary"], "args": [],
                  "env": {"CORTEXDB_PATH": item["database"], "CORTEXDB_REMOTE": ""}}
        for agent in result["agents"]:
            path = paths[f"{agent}_config"]
            ensure_regular(path)
            original = path.read_bytes() if path.exists() else b""
            owned = manifest["configs"].get(str(path), {})
            content, record = (claude_config if agent == "claude" else codex_config)(original, server, owned)
            prepare(path, content, mode=0o600)
            manifest["configs"][str(path)] = record

    for item in result["integrations"]:
        name = item["name"]
        if name == "cortexdb":
            binary = Path(item["binary"])
            ensure_regular(binary)
            existing = binary.read_bytes() if binary.exists() else b""
            data = existing if digest(existing) == item["sha256"] else download(item["url"], item["sha256"])
            prepare(binary, data, mode=0o755, owned_file=True)
            resources = {"SKILL.md": CORTEX_SKILL.encode()}
        else:
            cache = paths["state"] / f"feynman-{FEYNMAN_COMMIT}.tar.gz"
            ensure_regular(cache)
            existing = cache.read_bytes() if cache.exists() else b""
            data = existing if digest(existing) == item["sha256"] else download(item["url"], item["sha256"])
            resources = feynman_files(data)
            prepare(cache, data, owned_file=True)
        resources["ARCA_PROVENANCE.json"] = json_bytes({k: item[k] for k in
            ("name", "version", "url", "sha256", "edition", "commit") if k in item})
        for directory in item["skills"]:
            folder = Path(directory)
            # Do not adopt an unrelated skill, even if it contains extra unowned files.
            if folder.exists() and not any(str(p).startswith(str(folder) + os.sep) for p in manifest["files"]):
                raise ArcaError(f"Skill directory already exists outside this installation: {folder}")
            for relative, content in resources.items():
                prepare(folder / relative, content, owned_file=True)
        prior_agents = manifest["integrations"].get(name, {}).get("agents", [])
        manifest["integrations"][name] = {"version": item["version"], "edition": item["edition"],
            "agents": sorted(set(prior_agents + result["agents"])), "url": item["url"], "sha256": item["sha256"]}

    if result["scope"] == "project":
        path = root / ".gitignore"
        ensure_regular(path)
        original = path.read_text(encoding="utf-8") if path.exists() else ""
        patterns = ["/.local/"]
        for item in result["integrations"]:
            patterns += ["/" + Path(p).relative_to(root).as_posix() + "/" for p in item["skills"]]
            patterns += ["/" + Path(p).relative_to(root).as_posix() for p in item.get("configs", [])]
        missing = [p for p in dict.fromkeys(patterns) if p not in original.splitlines()]
        if missing:
            prepare(path, (original.rstrip("\n") + "\n\n# ARCA optional integrations (machine-local)\n"
                           + "\n".join(missing) + "\n").encode())

    manifest.update(scope=result["scope"])
    if result["scope"] == "project":
        manifest["root"] = str(root)
    # Repeating an unchanged install is a true no-op, including its manifest.
    old_manifest = load_manifest(manifest_path)
    if manifest != old_manifest or pending:
        manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    prepare(manifest_path, json_bytes(manifest), mode=0o600)
    # Detect edits made by an agent or editor while downloads were in flight.
    for path, original in originals.items():
        ensure_regular(path)
        if (path.read_bytes() if path.exists() else None) != original:
            raise ArcaError(f"File changed during installation; retry after reviewing it: {path}")
    backup_dir = paths["state"] / "backups" / uuid.uuid4().hex
    backups = {digest(str(path).encode()) + ".bak": str(path)
               for path in pending if originals[path] is not None}
    if backups:
        atomic_write(backup_dir / "index.json", json_bytes(backups), 0o600)
    changed = []
    try:
        for path, (content, mode) in pending.items():
            if originals[path] is not None:
                atomic_write(backup_dir / (digest(str(path).encode()) + ".bak"), originals[path], 0o600)
            atomic_write(path, content, mode)
            changed.append(path)
    except (OSError, KeyboardInterrupt):
        for path in reversed(changed):
            if originals[path] is None:
                path.unlink(missing_ok=True)
            else:
                atomic_write(path, originals[path], modes[path])
        raise
    result.update(dry_run=False, changed=[str(p) for p in changed],
                  backup_dir=str(backup_dir) if backup_dir.exists() else None,
                  note="Installed locally. Reopen Claude Code/Codex to discover skills and MCP. "
                       "Host trust/permission prompts still apply; no hooks or model jobs were started.")
    return result


def status(root, scope="project"):
    path = locations(root, scope)["state"] / "manifest.json"
    manifest = load_manifest(path)
    issues = []
    if scope == "project" and manifest.get("root", str(root)) != str(root):
        issues.append("Project moved: reinstall all installed integrations and hosts to refresh absolute paths.")
    for name, expected in manifest["files"].items():
        file = Path(name)
        if not file.is_file() or digest(file.read_bytes()) != expected:
            issues.append(f"Missing or changed installed file: {name}")
        elif file.parent.name == "bin" and os.name != "nt" and not os.access(file, os.X_OK):
            issues.append(f"Installed binary is not executable: {name}")
    for name, record in manifest["configs"].items():
        file = Path(name)
        try:
            if record["kind"] == "json":
                content = json_bytes(read_json(file).get("mcpServers", {}).get("cortexdb"))
            else:
                content = managed_block(file.read_text(encoding="utf-8")).encode()
            if digest(content) != record["sha256"]:
                issues.append(f"Missing or changed CortexDB configuration: {name}")
        except (OSError, ArcaError, UnicodeError, AttributeError) as exc:
            issues.append(f"Cannot inspect {name}: {exc}")
    return {"ok": not issues, "scope": scope, "manifest": str(path),
            "integrations": manifest["integrations"], "issues": issues,
            "note": "Local files/configuration only; agent loading and MCP connectivity are not checked."}
