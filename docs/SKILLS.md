# ARCA custom skills · just enough

Una skill è una procedura specializzata in `SKILL.md`, caricata quando utile. Non è memoria, non è un agente separato e non è un server MCP.

## Regola dei tre

Crea una skill se il workflow si ripete in almeno 3 task, contiene passaggi difficili da ricordare o un controllo specialistico importante, e produce output verificabile. Altrimenti resta in un piano o nel prompt.

## Cosa abbiamo incluso

Una sola skill dimostrativa: `research-evidence-audit`. Verifica se un finding/claim possiede prove e provenance corrette. Non lancia lunghi esperimenti né promuove automaticamente i claim.

- Canonica Codex: `.agents/skills/research-evidence-audit/SKILL.md`.
- Adattatore Claude Code: `.claude/skills/research-evidence-audit/SKILL.md` che punta alle stesse istruzioni canoniche, senza duplicare gli step.
- Crea ulteriori skill solo su necessità con `python3 scripts/new_skill.py slug "descrizione precisa del trigger"`.

## Anatomia

```yaml
---
name: research-evidence-audit
description: Audit a scientific finding or paper claim when asked to validate evidence, metrics, or provenance.
---
```

Contenuto breve: trigger preciso, input, passi essenziali, output, stop conditions. Dettagli estesi in `references/` solo se necessari. Preferisci 30-80 righe anziché centinaia.

## Skill ≠ AGENTS.md ≠ CortexDB

- `AGENTS.md`: principi cross-task invarianti;
- skill: workflow eseguibile just-in-time;
- CortexDB: indice/recall, può recuperare riferimenti;
- MCP: strumenti e dati operativi (permessi separati).

## Governance

Il contenuto delle skill può orientare comandi e strumenti: code review obbligatoria per nuove skill esterne, niente shell non controllata, niente segreti in file istruzioni, nessuna modifica permanente a repository o evidenze senza controlli adeguati. Non replicare le skill di Feynman o quelle native se funzionano già.

Refs: https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra ; https://learn.chatgpt.com/docs/build-skills ; https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
