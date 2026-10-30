# ARCA — Agentic Research Context Architecture

**Versione 2.0**

ARCA è un harness di repository per ricerca scientifica in machine learning che dura nel tempo e passa di mano tra persone, modelli e sessioni. Tiene insieme obiettivo, ipotesi, esperimenti, risultati negativi, decisioni e claim del paper, con una provenienza verificabile dai file e da Git.

Un coding agent (Claude Code, Codex o un agente specializzato) legge solo il contesto utile al task corrente. Quando la chat si compatta, il modello cambia o il lavoro riprende dopo una pausa, lo stato scientifico resta nel repository.

## Cosa fa

- **Definisce il problema.** `research/CHARTER.md` fissa obiettivo, domande, ambito e criteri di successo.
- **Tiene uno stato riavviabile.** `context/STATE.md` e `context/NEXT.md` registrano dove si è arrivati e la prossima azione eseguibile.
- **Separa fatto, ipotesi e interpretazione.** Domande, ipotesi, findings, contraddizioni e decisioni restano distinti in `research/`.
- **Registra ogni esperimento.** Ogni run ha un ID, una baseline, config, fingerprint dei dati, split, seed, metriche e commit.
- **Collega il paper all'evidenza.** Un claim pubblicabile punta a un finding, a un esperimento e agli artifact.
- **Conserva i risultati negativi.** Confutazioni e fallimenti restano visibili, così il lavoro successivo parte da ciò che è già stato provato.
- **Resta usabile da solo.** CortexDB, se lo abiliti, è un indice di richiamo semantico. Registri, metriche e claim versionati restano la fonte di verità.

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
