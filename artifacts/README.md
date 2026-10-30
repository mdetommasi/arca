# Artifact Registry

Modelli addestrati, checkpoint, embedding, dataset derivati, grandi log e figure generate sono artefatti.

Non è necessario versionare i binari in Git. È necessario versionarne la provenance.

Ogni riga di `manifest.jsonl` dovrebbe contenere:
- `artifact_id`
- `type`
- `uri_or_path`
- `sha256` o altro fingerprint
- `size_bytes`
- `experiment_id`
- `run_id`
- `git_commit`
- `dataset_ids`
- `config_hash`
- `created_at`
- `notes`

Per storage remoto puoi usare DVC, MLflow, W&B Artifacts, S3/MinIO, Hugging Face Hub o altro.
La repo deve comunque conservare un puntatore stabile e verificabile.
