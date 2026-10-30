# Experiment Configurations

Le configurazioni devono essere versionabili, diffabili e sufficienti a ricostruire un run.

Buone pratiche:
- evitare parametri critici nascosti nel codice;
- salvare una config risolta per ogni run importante;
- registrare hash/config path in `experiment.yaml`;
- non modificare retroattivamente la config di un esperimento concluso senza conservarne la versione originale.
