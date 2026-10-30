# Data Provenance

Non trattare "il dataset" come un'entità implicita.

Per ogni dataset/versione registra in `data/registry.yaml`:
- ID stabile;
- origine;
- licenza/accesso;
- raw source;
- preprocessing;
- split protocol;
- fingerprint/hash;
- dimensioni;
- feature/target;
- known issues;
- script/commit che lo genera.

I dati pesanti possono restare fuori da Git, ma il loro **puntatore e fingerprint** devono stare nella repo.
