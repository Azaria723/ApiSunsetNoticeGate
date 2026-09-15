# Threat model

## Protected properties

- A requester cannot redirect validators to a different host or repository.
- Raw bytes cannot be substituted without failing Git blob and SHA-256 checks.
- Incomplete Git trees are rejected.
- Evidence instructions cannot expand the fixed model response schema.
- Negative, unavailable or unresolved outcomes cannot authorize a sunset.
- Authorization cannot cross services, revisions, endpoints, actions, callers or time windows.
- Rejected calls do not mutate consequential state.

## Adversarial cases

The test suite covers URL-like endpoints, traversal paths, invalid commits, source outage, digest mismatch, identity mismatch, truncated trees, incorrect blob SHA-1, schema smuggling, semantic negatives, stale revision, wrong controller, wrong digests and replay.

## Trust assumptions

The constructor-selected registry controller is trusted to register the correct repository and sunset controller. The deployer has no implicit privilege. Repository maintainers are authoritative for content committed in that repository. GenLayer consensus is trusted according to its protocol assumptions. A downstream gateway must independently require the exact stored authorization and action digest.

## Non-goals

This contract does not shut down infrastructure, custody funds, prove repository ownership outside registry curation, determine legal compliance, inspect runtime traffic, or guarantee that a replacement implementation behaves exactly like its documentation.
