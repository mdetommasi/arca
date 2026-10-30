# ARCA v2.0 — Guidelines operative per la ricerca scientifica con coding agents

Data revisione: 22 ottobre 2026. Contesto: progetti UniBo; denominazione ARCA proposta e non istituzionalmente approvata.

## 1. Cosa risolve ARCA

Sessioni molto lunghe, compaction, cambio modello, sperimentazioni negative, modelli/checkpoint difficili da ritrovare e paper non sincronizzati. ARCA mette su disco ciò che deve essere preservato, con provenienza verificabile e un protocollo leggero per l'uso quotidiano.

## 2. Le tre regole non negoziabili

1. **Git è il sistema di record** per affermazioni scientifiche e decisioni; le metriche raw e gli artifact sono referenziati in modo verificabile.
2. **Fatto, ipotesi e interpretazione non sono sinonimi.** Confutazioni e fallimenti vanno registrati.
3. **Contesto minimo, retrieval mirato.** Nuovi modelli non traggono beneficio dal caricamento automatico di tutto.

## 3. Avvio di una nuova ricerca

Clona/copia il template, compila `research/CHARTER.md`, definisci benchmark/validazione e datasource. Scrivi una prima versione concisa di `STATE.md` e `NEXT.md`; prepara Git e l'ambiente Python. Esegui `python3 scripts/arca_check.py`.

Non è necessario installare CortexDB, skill esterne o server MCP per cominciare.

## 4. Uso giornaliero

**Sessione nuova o cambio agente.** Leggi stato/next e il task corrente, controlla `git status`; apri solo esperimenti/paper/literatura pertinenti. Se CortexDB è disponibile puoi fare recall ma devi verificare eventuali numeri prima di usarli.

**Task piccolo.** Modifica/testa/chiudi; non creare un piano burocratico.

**Task scientifico.** Collega una domanda e un'ipotesi, crea `E-####`, salva config, dataset hash, commit e baseline prima del run. Dopo: metriche leggibili da macchina, report, artifact pointer e aggiornamento dei findings.

**Fine sessione rilevante.** Aggiorna `STATE.md`, `NEXT.md` e, quando ha senso, una voce al `LAB_NOTEBOOK.md`. Fai un commit; facoltativamente lancia `python3 scripts/session_checkpoint.py`.

## 5. L'importanza dei risultati negativi

Una conclusione inconcludente o contraddittoria può costare molte GPU-hour risparmiate in futuro. Scrivi cosa hai provato, quale confronto era valido, cosa è fallito e quali ipotesi alternative restano.

## 6. Paper e report

Il manoscritto non deve ricostruire risultati dalla chat. Usa `paper/CLAIMS.md` come ponte fra `F-###` ed esperimenti `E-####`, figura/tabella e frase da pubblicare. Se i nuovi dati indeboliscono un claim, cambia prima il suo stato e la matrice, poi aggiorna il testo.

## 7. CortexDB opzionale

Leggi `memory/CORTEXDB.md`. CortexDB serve per ricordare **dove cercare**, non per certificare che un risultato sia vero. Privilegia DB locali isolati per progetto; le modalità di auto recall/capture richiedono una policy su privacy, prompt injection e qualità. Valuta 10-20 query campione contro baseline senza DB prima di abilitarlo per tutti.

## 8. Skill personalizzate senza bloat

Una skill è una procedura breve per un workflow ripetuto. Non trasformare ogni routine in una skill. Mantieni le istruzioni generali in `AGENTS.md`, quelle scientifiche specialistiche in poche `SKILL.md`, la conoscenza in findings/experiments. Genera una nuova skill con `scripts/new_skill.py` solo quando il beneficio è chiaro. Leggi `docs/SKILLS.md`.

## 9. Claude Code, Codex e Feynman

I due coding agents condividono `AGENTS.md`; Claude aggiunge un `CLAUDE.md` minimale. Feynman è un supporto a review, ipotesi, replica e critica, ma deve produrre artefatti ARCA verificabili. La review di un altro agente non deve essere scambiata per una replica sperimentale.

## 10. Handoff / compaction

Registra prima l'attuale task, evidenza aggiornata, problemi aperti, job attivi e **prossima azione esatta**. CortexDB può recuperare memoria automatica, ma non garantisce che le note siano complete o aggiornate. Gli hook hanno payload/permessi variabili e devono essere controllati; il compaction checkpoint manuale rimane affidabile e portabile.

## 11. Checklist breve

- [ ] `STATE` + `NEXT` riflettono la ricerca corrente.
- [ ] Gli esperimenti significativi hanno config, metriche, commit, dataset fingerprint, baseline e report.
- [ ] I checkpoint/modelli hanno URI e hash, non soltanto nomi vaghi.
- [ ] I risultati negativi e le contraddizioni restano visibili.
- [ ] Le figure, tabelle e frasi quantitative nel paper puntano a evidenze verificabili.
- [ ] CortexDB, se attivo, restituisce riferimenti e non sostituisce prove raw.
- [ ] Le skill presenti sono poche, specifiche, versionate e verificabili.
- [ ] Privacy, permessi e hook di terze parti sono stati controllati.

## 12. Indicatori di qualità

Valuta il framework con un test a freddo: un nuovo agente senza chat recupera correttamente risultato migliore, esperimenti falliti, confutazioni, checkpoint, protocollo e next step. Misura tempo/numero di letture, precisione dei riferimenti, claim sbagliati e qualità degli handoff. Confronta ARCA senza e con CortexDB: abilita la memoria opzionale solo se migliora i risultati misurati.

## Riferimenti tecnici verificati

- https://github.com/liliang-cn/cortexdb/blob/main/plugins/cortexdb/README.md
- https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
- https://learn.chatgpt.com/docs/build-skills
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
