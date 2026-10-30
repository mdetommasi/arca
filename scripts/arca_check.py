#!/usr/bin/env python3
"""Portable ARCA smoke-check, no external dependencies, does not access CortexDB."""
from pathlib import Path
import importlib.util
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
required = ['AGENTS.md','CLAUDE.md','framework.yaml','context/STATE.md','context/NEXT.md',
            'research/CHARTER.md','experiments/REGISTRY.csv','paper/CLAIMS.md',
            'memory/CORTEXDB.md','docs/GUIDELINES_v2.md',
            '.agents/skills/research-evidence-audit/SKILL.md',
            '.claude/skills/research-evidence-audit/SKILL.md']
errors = []
for rel in required:
    if not (ROOT/rel).is_file(): errors.append('Missing: '+rel)
for cmd in ['validate_context.py']:
    r = subprocess.run([sys.executable, str(ROOT/'scripts'/cmd)], cwd=ROOT, capture_output=True, text=True)
    if r.returncode: errors.append(f'{cmd} failed: {r.stdout} {r.stderr}')
print(f'ARCA check: {"OK" if not errors else "FAIL"} | files={len(list(ROOT.rglob("*")))} | cortexdb=OPTIONAL')
for err in errors: print('ERROR:',err)
raise SystemExit(1 if errors else 0)
