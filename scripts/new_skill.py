#!/usr/bin/env python3
"""Create a minimal portable Agent Skill for Codex and an adapter for Claude Code."""
from pathlib import Path
import re
import sys
ROOT = Path(__file__).resolve().parents[1]
if len(sys.argv) < 3:
    raise SystemExit('Usage: python3 scripts/new_skill.py kebab-case "Description with WHEN to use it"')
name = sys.argv[1]
desc = ' '.join(sys.argv[2:]).strip()
if not re.fullmatch(r'[a-z][a-z0-9]*(?:-[a-z0-9]+)*', name):
    raise SystemExit('Name must be lowercase kebab-case')
if not desc or ':' in desc or '\n' in desc or len(desc) > 220:
    raise SystemExit('Description must be nonempty, <=220 characters, single-line without colon')
p = ROOT / '.agents' / 'skills' / name / 'SKILL.md'
q = ROOT / '.claude' / 'skills' / name / 'SKILL.md'
if p.exists() or q.exists():
    raise SystemExit(f'Already exists: {name}')
p.parent.mkdir(parents=True)
q.parent.mkdir(parents=True)
p.write_text(f"""---\nname: {name}\ndescription: {desc}\n---\n\n# {name}\n\n## Input and trigger\n\n- Use only when the task matches the description.\n\n## Procedure\n\n1. Inspect the canonical ARCA files relevant to this task.\n2. Perform the narrow repeatable workflow.\n3. Validate outputs and document evidence pointers.\n\n## Output and stop conditions\n\n- Summarize result, validation, remaining uncertainty and exact output locations.\n- Stop if essential input/evidence is unavailable.\n""", encoding='utf-8')
q.write_text(f"""---\nname: {name}\ndescription: {desc}\n---\n\nRead and follow `.agents/skills/{name}/SKILL.md` as canonical instructions.\n""", encoding='utf-8')
print(p.relative_to(ROOT))
print(q.relative_to(ROOT))
