# Policy di memoria

**Ordine di autorità:** raw scientific artifacts > versioned metrics/configs/provenance > curated Git findings/decisions/claims > conversation transcript > automatic memory retrieval. La verità su «cosa è accaduto» deve essere verificabile da esperimenti e commit, non dai soli riassunti.

## Memory write gate

Promuovi in memoria recuperabile solo annotazioni con:

- scope: project id (non solo basename ambiguo);
- source: path + entity id + git commit or timestamp;
- epistemic status: fact / hypothesis / decision / interpretation / unverified;
- superseded-by (se aggiornato);
- breve riepilogo, senza interi transcript.

L'integrazione CortexDB può non esporre tutti questi campi nel formato desiderato: se non sono supportati, rappresentali nel contenuto della nota e mantieni comunque il record canonico su disco.

La raccolta automatica è assistiva. Non importare senza controllo email, credenziali, note personali, dataset riservati, materiale proprietario o contenuti di terzi.

## Backup

- Git conserva evidenze versionate, **non** il DB CortexDB.
- Backup del brain opzionale secondo policy istituzionali, con controllo accessi/retention.
- Verificare procedura di export Markdown upstream prima di dipendere dal backend.
