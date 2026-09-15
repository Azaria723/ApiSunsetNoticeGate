# Architecture

## State model

A service is a registry-controller-curated authority record containing repository identity, policy coordinates, notice-period policy, sunset controller and monotonic revision. A proposal is append-only and captures one exact endpoint retirement plus immutable evidence coordinates and authorization constraints. The registry controller is supplied explicitly to the constructor; the deployer receives no implicit role.

```text
PENDING → AUTHORIZED → CONSUMED
        ↘ BLOCKED
```

There is no path from a negative verdict to `AUTHORIZED`. Deactivation increments the service revision and invalidates every unconsumed proposal.

## Deterministic layer

- registration and input validation;
- canonical GitHub URL construction;
- commit and complete-tree checks;
- path, mode, size, Git blob SHA-1 and SHA-256 verification;
- service identity markers;
- minimum-notice arithmetic;
- strict response schema validation;
- verdict and reason derivation;
- authorization binding, timing, revision, caller and replay checks.

## Semantic layer

Validators return exactly five booleans:

```json
{
  "notice_identifies_exact_endpoint": true,
  "migration_guide_is_actionable": true,
  "replacement_preserves_core_capability": true,
  "limitations_are_disclosed": true,
  "policy_exceptions_are_satisfied": true
}
```

Free-form explanations, excerpts and model-selected verdicts are excluded from consensus. `strict_eq` therefore covers only the consequential closed facts and deterministic provenance flags.

## Authorization boundary

The authorization digest binds service and proposal identity, controller, method, endpoint, policy/notice/old/new commits and content digests, migration digest, service revision, action digest, activation time and expiry. The separate action-digest argument must also match at consumption. Successful consumption is single-use and increments the service revision.
