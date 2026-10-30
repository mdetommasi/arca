# Experiment System

Ogni esperimento non banale ha un ID immutabile `E-####`.

Struttura suggerita:

experiments/E-0001-short-name/
- `experiment.yaml` — piano e provenance;
- `report.md` — interpretazione umana/agentica;
- `metrics.json` — risultati machine-readable;
- `runs/` — eventuali metadata dei singoli seed/run;
- `README.md` opzionale.

Gli output pesanti non vanno necessariamente in Git: registrarli in `artifacts/manifest.jsonl`.

Regola: non riusare un ID per un nuovo esperimento. Se cambi una condizione che altera il significato del confronto, crea un nuovo ID e usa `parent_experiment`.
