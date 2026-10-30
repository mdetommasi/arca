# ARCA — Agentic Research Context Architecture

**Versione 2.0 · UniBo research template (nome/affiliazione proposti, non ufficiali)**

ARCA è uno scheletro di repository per ML e ricerca scientifica long-running con Claude Code, Codex e agenti specializzati (es. Feynman). Protegge conoscenza sperimentale e provenance anche dopo cambio modello, compaction e pause lunghe.

## Principio

**File Git-versionati = fonte di verità. CortexDB = memoria opzionale, indice semantico e knowledge graph.**

CortexDB non sostituisce registro esperimenti, metriche, dataset fingerprint, decisioni, findings e claim del paper.

## Primo avvio (senza alcuna dipendenza)

```bash
python3 scripts/arca_check.py
python3 scripts/new_experiment.py "initial baseline"
python3 scripts/session_checkpoint.py
```

Personalizza `research/CHARTER.md`, `context/STATE.md` e `context/NEXT.md`. Apri VS Code nella root e lavora normalmente con Claude Code o Codex.

## Materiale operativo

| Cosa | Dove |
|---|---|
| Istruzioni condivise e leggere | `AGENTS.md` |
| Istruzioni Claude Code | `CLAUDE.md` |
| Stato, prossime azioni | `context/STATE.md`, `context/NEXT.md` |
| Ipotesi, risultati, decisioni | `research/` |
| Esperimenti/config/provenance | `experiments/`, `data/`, `artifacts/` |
| Claim/manoscritto | `paper/` |
| Memoria CortexDB opzionale | `memory/CORTEXDB.md` |
| Skill opzionali | `.agents/skills/`, `.claude/skills/` |
| Vademecum completo | `docs/GUIDELINES_v2.md` |
| Compatibilità aggiornata | `docs/AGENT_COMPATIBILITY.md` |

## Installazione CortexDB (solo se la vuoi)

Segui `memory/CORTEXDB.md`, che documenta installazione, isolamento progetto, permessi, privacy e diagnostica. **Nessun backend si installa o si abilita automaticamente** usando ARCA.

## Creare una skill (solo quando serve)

```bash
python3 scripts/new_skill.py "experimental-audit" "Use when validating a completed ML experiment against its recorded metrics and provenance."
```

Il generatore crea un `SKILL.md` per Codex e un delegato minimale per Claude Code. Consulta `docs/SKILLS.md`.

## Confini di sicurezza

- Evita segreti, dataset riservati e note private non autorizzate nella memoria automatica.
- Non trasferire dati su server condivisi senza autorizzazione, token e trasporto sicuro.
- Non usare memoria auto-raccolta come evidenza scientifica.
- Mantieni il sistema pienamente operativo anche con CortexDB disattivato.

## Riferimenti

- [CortexDB (repo corretto: liliang-cn/cortexdb)](https://github.com/liliang-cn/cortexdb)
- [Codex: guidance su skill e AGENTS.md, settembre 2026](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
- [Codex skill locations](https://learn.chatgpt.com/docs/build-skills)
- [Claude Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
