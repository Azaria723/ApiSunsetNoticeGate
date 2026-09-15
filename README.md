# API Sunset Notice Gate

API Sunset Notice Gate is a narrow GenLayer Intelligent Contract that prevents an API endpoint from being retired until its canonical notice, migration path, replacement specification, and locked deprecation policy establish a safe sunset premise.

## Proof obligation

For one exact HTTP method and endpoint, determine whether the proposed retirement satisfies the registered notice period and whether the canonical evidence establishes an actionable, capability-preserving migration.

The contract does not operate an API gateway, prove legal compliance, or decide whether an endpoint should exist. It issues a bounded, expiring, single-use authorization that a registered sunset controller may consume.

## Why GenLayer

Dates, revisions, paths, digests, identities and authorization boundaries are deterministic. Whether a migration guide is actionable, a replacement preserves core capability, or limitations are adequately disclosed requires semantic interpretation. Validators judge only five booleans; the contract derives every verdict and reason code.

```text
canonical GitHub provenance
→ five consequential booleans
→ contract-derived verdict
→ bound one-shot authorization
```

## Canonical acquisition

The requester cannot supply a host or URL. From the owner-registered repository and submitted full commits, validators independently retrieve:

1. GitHub Commit API records;
2. recursive Git trees, requiring `truncated = false`;
3. exact blob path, mode `100644`, byte size and Git blob SHA-1;
4. raw policy, notice, migration guide and old/new specifications;
5. submitted SHA-256 commitments and embedded service identity markers.

Any incomplete or inconsistent provenance fails closed.

## Outcomes

- `SUNSET_ELIGIBLE`: all deterministic and semantic requirements passed.
- `NOTICE_INCOMPLETE`: exact endpoint identification or limitation disclosure failed.
- `MIGRATION_GAP`: the guide is not actionable or core capability is not preserved.
- `POLICY_VIOLATION`: notice duration or policy exceptions failed.
- `PROVENANCE_FAILURE`: canonical evidence could not be authenticated.
- `UNRESOLVED`: authenticated evidence could not produce a valid bounded semantic result.

Only `SUNSET_ELIGIBLE` creates an authorization. Consumption requires the registered controller, exact authorization digest, exact action digest, active time window and current service revision. Successful consumption advances the service revision, preventing reuse by stale proposals.

## Local verification

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

Current result: **19 tests passed**. The suite covers positive authorization and consumption, canonical address encoding, wrong controller, wrong binding, wrong action, replay, short notice, incomplete notice, migration failure, digest tampering, identity mismatch, source outage, truncated Git tree, blob SHA-1 mismatch, malformed model schema, invalid inputs, deactivation and state preservation.

See [architecture](docs/ARCHITECTURE.md), [threat model](docs/THREAT_MODEL.md), [deployment checklist](docs/DEPLOYMENT.md), and [local verification](verification/local-verification.md).

## Deployment status

The first Studionet deployment exposed a runtime-specific address serialization defect during registration and is superseded. The corrected source is ready for a fresh deployment; no lifecycle evidence from the superseded instance is claimed.
