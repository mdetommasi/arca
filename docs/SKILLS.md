# ARCA custom skills · just enough

Una skill è una procedura specializzata in `SKILL.md`, caricata quando utile. Non è memoria, non è un agente separato e non è un server MCP.

## Regola dei tre

Crea una skill se il workflow si ripete in almeno 3 task, contiene passaggi difficili da ricordare o un controllo specialistico importante, e produce output verificabile. Altrimenti resta in un piano o nel prompt.

## Cosa abbiamo incluso

L'interfaccia comune è `arca`: invocala come `$arca` in Codex o `/arca` in
Claude Code e descrivi l'operazione richiesta. Usa la [CLI condivisa](CLI.md)
per inizializzare il progetto, leggerne lo stato, preparare un esperimento,
controllare la struttura o creare un checkpoint.

Scrivi l'invocazione nella chat della sessione dell'agente aperta sul progetto,
anche nell'estensione VS Code. La skill guida l'agente nell'esecuzione di
`python3 -m arca_cli`; nel terminale puoi invece usare direttamente `./arca`.
Le skill sono incluse nel repository: non serve un plugin ARCA separato.
L'installazione Python opzionale espone il comando `arca` nel terminale.

Restano disponibili i workflow mirati:

- `arca-resume`: ricostruzione in sola lettura dello stato scientifico.
- `arca-checkpoint`: aggiornamento delle note canoniche seguito dallo snapshot.
- `research-evidence-audit`: verifica di metriche, provenienza e comparabilità di un finding/claim.

Le istruzioni canoniche sono in `.agents/skills/<nome>/SKILL.md`; gli
adattatori in `.claude/skills/<nome>/SKILL.md` rimandano agli stessi file.
La CLI esegue le operazioni sui record; l'agente fornisce il contenuto
scientifico sulla base delle informazioni disponibili.

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
