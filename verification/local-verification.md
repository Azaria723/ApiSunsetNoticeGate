# Local verification

- Direct Mode contract tests: `19 passed`.
- Contract source SHA-256: `edced5ba35cfddd91b2ced31bde808e02a5b0a96854fbd8a0a080b1d5da7127a`.
- Contract runner and dependency are pinned to `genlayer-test 0.2.16` metadata.
- Web and LLM access use strict mocks.
- Consequential negative calls are asserted not to create authorization or mutate protected counters/state.
- Provenance tests cover Commit API identity, complete tree, blob path/mode/size/SHA-1, raw SHA-256 and service markers.
- Semantic tests cover all-positive approval, notice failure, migration failure, policy failure and malformed model output.
- Authorization tests cover caller, binding digest, action digest, revision and replay.

Studionet source parity and transaction evidence remain pending until a fresh deployment is supplied.

## Demo artifact SHA-256 values

- `deprecation-policy.md`: `9f574a3989950591f7a23e0d1934258895a11884afbcf09675ac5a75916ae850`
- `sunset-notice.md`: `982374a9eaa7a921ab8af9a7d3444cd08ca267b3095da07b8b1e091892e15536`
- `migration-guide.md`: `ca353e655cd0155f80b6c908730ff53a28541600781e7124f512c34fcb3dd177`
- `openapi-v1.txt`: `9a104dca0e2c1148124cfc640d54f181f3906bb462341faf84f813c2a2f16ad8`
- `openapi-v2.txt`: `5e42d57c37aa7e1a996ead182b40ec7ad453390ceb38a2509396ed6932eea795`
