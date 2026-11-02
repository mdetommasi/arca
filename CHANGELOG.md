# Changelog

## Unreleased

- Installazione opzionale CortexDB/Feynman da `init --with` o dal nuovo
  `integrations install`, con scope progetto/utente e supporto Claude/Codex.
  CortexDB via MCP locale; Feynman come workflow upstream con adattatore skill.
  Versioni fissate, SHA-256, anteprima offline, stato locale, backup,
  protezione delle configurazioni esistenti e ripristino su errori di scrittura.
- Implementazione CLI raccolta in `scripts/arca_cli/` insieme agli strumenti
  del repository; launcher `./arca` e comando installato `arca` invariati.
  Avvio dal sorgente con `python3 arca` o `python3 -m scripts.arca_cli`.
- Packaging CLI con Hatchling e output locale in `.local/dist/`; installazioni
  normali/editable senza residui `build/` o `*.egg-info/` nella root.
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
