# Schema concettuale per il research graph (facoltativo)

Nodi: `Project`, `Question`, `Hypothesis`, `Experiment`, `Run`, `Finding`, `Contradiction`, `Decision`, `Dataset`, `Artifact`, `Source`, `PaperClaim`.

Relazioni raccomandate:

```text
Question <-addresses- Hypothesis
Hypothesis <-tests- Experiment
Experiment -produces-> Run
Run -uses-> Dataset / Artifact / Commit
Experiment -supports|refutes-> Finding
Finding -supports|challenges-> PaperClaim
Decision -motivated_by-> Finding / Source
Contradiction -conflicts_with-> Finding / PaperClaim
```

Ogni nodo ha URI/ID canonico leggibile (`E-0042`, `H-007`), path sorgente Git, stato epistemico e timestamp. Questo schema è **una convenzione di modellazione**, non una promessa che l'importazione sia automatica o che le API di CortexDB accettino esattamente queste relazioni senza adattatore.
