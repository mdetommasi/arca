---
name: research-evidence-audit
description: Audit an ML finding or paper claim when asked to validate its numerical evidence, provenance, comparability, or publication readiness.
---

# Research evidence audit

Input: a `F-###` finding or `C-###` paper claim (or a precise statement and source path).

1. Locate the canonical record and linked experiment IDs.
2. Validate presence of experiment report, registered metrics/config, code commit, dataset fingerprint, and artifact pointer where applicable.
3. Cross-check exact numerical claims; compare split, seed policy, baseline, and conditions.
4. Inspect linked limitations and unresolved contradictions. Distinguish observed facts from interpretation.
5. Produce a concise table: claim, evidence path, status (verified / supported / inconclusive / invalid), discrepancy, action.
6. Do not silently modify a scientific claim or label it verified merely because a remembered summary agrees.

Stop if raw evidence is inaccessible; mark as **unverified** and list missing paths.
