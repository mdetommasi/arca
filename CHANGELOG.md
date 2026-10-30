# Changelog

## Unreleased

- CLI comune `arca`: `init`, `status`, `check`, `experiment new`, `checkpoint`;
  avvio diretto dal checkout o installazione come comando Python.
- Output JSON e selezione del progetto dalla directory corrente o `--root`.
- Logica condivisa con gli script legacy; warning strutturali ora visibili,
  senza eccezioni per riferimenti a `E-0001` non registrati.
- Inizializzazione che preserva le note esistenti, provenance Git dirty/unknown
  nei nuovi esperimenti e snapshot distinti anche in rapida successione.
- Skill `arca` per Codex/Claude e adattatori Claude per i workflow canonici;
  guida CLI, esempi aggiornati e test di integrazione isolati.
- README, documentazione e guida PDF aggiornati con esempi distinti per chat
  dell'estensione, terminale e Remote SSH; troubleshooting delle skill e
  sorgente HTML versionato per rigenerare la guida illustrata.

## 2.0.0 — 2026-10-22

- Nome ARCA — Agentic Research Context Architecture.
- CortexDB adapter **opzionale** documentato (senza dipendenza forzata, senza integrazione runtime non verificata).
- Skills on-demand con una sola skill di esempio + generatore portabile per Codex/Claude Code.
- `AGENTS.md` ridotto e task-aware; niente pre-reading estensivo per ogni edit.
- Memo privacy/scope, strategia di rollout e compatibilità aggiornata coding agents.
- Preservato il modello di provenance, confutazioni, esperimenti, claim/paper della v1.
