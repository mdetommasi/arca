# CortexDB integration · OPTIONAL · reviewed 2026-10-22

**Progetto corretto:** https://github.com/liliang-cn/cortexdb (MIT, Go, SQLite + FTS/graph/vector). Non confondere con altri prodotti con nome simile o dominio `cortexdb.ai`.

## Decisione architetturale

ARCA senza CortexDB = completamente funzionante. CortexDB può aiutare con recall attraverso sessioni/modelli, ricerca e grafi (e.g. H-001 -> E-0004 -> F-002 -> C-003), ma non è il database ufficiale della ricerca. `FINDINGS`, experiment reports, dati e claim Git-tracked hanno priorità.

## Opzione 1: installare il plugin ufficiale

Claude Code, nel comando slash interno:

```text
/plugin marketplace add liliang-cn/cortexdb
/plugin install cortexdb@cortexdb
```

Codex, in terminale (versione che supporta i plugin):

```bash
codex plugin marketplace add liliang-cn/cortexdb
codex plugin add cortexdb@cortexdb
```

Per Codex: apri `/hooks`, esamina e autorizza esplicitamente gli hook CortexDB di cui ti fidi. Il plugin fornisce MCP anche senza approvare gli hook. I comandi e il supporto dipendono dalla versione del coding agent; in caso di differenze usa la guida upstream.

L'installer upstream può scaricare binari precompilati al primo avvio: esamina provenienza, versioni e permessi prima di abilitarlo su ambienti istituzionali.

## Scelta A (consigliata per test): DB isolato per progetto

Dalla root della repo, prima di lanciare **entrambi** gli agenti:

```bash
mkdir -p .local/cortexdb
export CORTEXDB_PATH="$(pwd)/.local/cortexdb/brain.db"
```

`.local/` è in `.gitignore`; il DB NON è incluso nel template né sincronizzato da Git. Configura l'env anche nella sessione VS Code/terminal da cui vengono lanciati i processi. Se cambi working directory, mantieni il path assoluto.

## Scelta B: brain globale

Default upstream: `~/.cortexdb/cortexdb.db`. Offre memoria condivisa fra tutti i progetti dello stesso computer, ma aumenta il rischio di contaminazione cross-project. Con più progetti o dataset distinti, preferisci l'opzione A finché non hai testato il comportamento di scoping.

## Scelta C: brain remoto multi-macchina (fase avanzata)

CortexDB espone `cortexdb-grpc`. Le variabili documentate upstream sono `CORTEXDB_REMOTE`, `CORTEXDB_GRPC_TOKEN`, `CORTEXDB_GRPC_ADDR`. NON mettere SQLite su NFS/SMB per condividerlo. Esponi il server solo su rete privata/Tailscale/loopback; usa TLS ove appropriato e proteggi il token. Un token compromesso può dare accesso ai contenuti del brain; verifica anche la policy sui dati della ricerca applicabile al progetto.

## Workflow di recall

1. Recupera possibili riferimenti con `/recall ...` o tool MCP.
2. Per ogni finding/claim recuperato controlla file, ID, stato, commit, metriche e limiti.
3. Se l'informazione non coincide con il canonico, correggi la memoria derivata o segnala la discrepanza; non modificare l'evidenza per farla coincidere.
4. Esegui aggiornamenti semantici in modalità controllata, non un import indiscriminato di transcript.

## Quali contenuti memorizzare

Memoria utile: link a file e ID stabili, note di navigazione, problemi ricorrenti, decisioni già versionate, segnali per trovare confronti passati.

Memoria da evitare: segreti, PII, output di ricerca non verificati presentati come certi, interi dataset, dump lunghi, ricostruzioni non tracciabili da conversazioni.

## Hook e collisioni

Il plugin CortexDB può registrare `SessionStart` e `UserPromptSubmit`. ARCA non lo installa di default. Il file `.claude/settings.example.json` è solo un esempio, **non** copiarlo automaticamente se abiliti recall del plugin: verifica che gli hook non reiniettino blocchi equivalenti. Preferire un solo producer di recall per evento. Il transcript raw è un fallback, non un indice affidabile.

## Verifica e benchmark

- `cortexdb-mcp --doctor --self-test` se l'eseguibile e la versione installata lo supportano.
- Testa 10-20 domande di recupero con e senza CortexDB, incluse due confutazioni, due artifact perduti e due claim aggiornati.
- Misura precisione di provenance, falsi recall, latenza, overhead token, contaminazione tra progetti.
- Se recall introduce errori o overhead senza benefici, spegni l'integrazione: ARCA deve comunque funzionare.

## Documentazione ufficiale

- https://github.com/liliang-cn/cortexdb/blob/main/README.md
- https://github.com/liliang-cn/cortexdb/blob/main/plugins/cortexdb/README.md
- https://github.com/liliang-cn/cortexdb/blob/main/docs/GUIDE.md
