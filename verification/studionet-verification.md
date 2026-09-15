# Studionet verification

> Superseded pre-release deployment. Do not submit this address as the final project contract.

## Deployment and source parity

- Contract: `0x24AeaF2815c5b12DcbaBB09992fc6eB6f3Ce7c31`
- Explorer: https://explorer-studio.genlayer.com/address/0x24AeaF2815c5b12DcbaBB09992fc6eB6f3Ce7c31
- Chain ID: `61999`
- Local contract SHA-256: `e367aeea253705d3828b1ee4d31237e909f4412fa1da796e72abe1706bf0b2e7`
- Deployed source SHA-256: `e367aeea253705d3828b1ee4d31237e909f4412fa1da796e72abe1706bf0b2e7`
- Source parity: `true`
- Initial state: `{"proposal_count": 0, "service_count": 0}`

No state-changing transaction was sent before source parity and empty deployment state were confirmed. Authority registration and lifecycle evidence remain pending until the canonical evidence repository has been published at an immutable full commit.

Registration transaction `0xbba1618abc37c67babb44a9c674ce442caeb06c85b7ccc01cc37ad4a9584c20b` exposed that GenVM supplied the `Address` parameter as an integer-like runtime value. The original helper serialized it as a decimal string rather than canonical `0x` hex. Testing stopped before any proposal was created. The helper and zero-address validation were corrected, regression coverage was added, and this deployment was superseded.

## Second superseded deployment

- Contract: `0x2d5b7e643480fe6f6Bea089116ED59B3719e9C08`
- Explorer: https://explorer-studio.genlayer.com/address/0x2d5b7e643480fe6f6Bea089116ED59B3719e9C08
- Source SHA-256 at deployment: `456cbecc28ca48548d88b1b3fe38198858872b7eac6c02b574160aeb45a2037c`
- Initial and post-registration state: zero services, zero proposals.
- Registration transaction: `0xd3d0d0c5900d2a9200dbe0d186215b129f6fab8434cbd5283d0c2ddc971150f2` ([explorer](https://explorer-studio.genlayer.com/tx/0xd3d0d0c5900d2a9200dbe0d186215b129f6fab8434cbd5283d0c2ddc971150f2)).
- Transaction status `FINALIZED` did **not** mean successful execution: leader and validators returned `exit_code 1`, `execution_result=ERROR`, and no state change.
- GenVM traceback identified `_address_text(sunset_controller)` calling `int(value)` on the hex string `0x7C87B10a3d43F3b3551414401F8b26B9F662bAB5`.

The helper now accepts and canonicalizes a validated 20-byte hex address string. A regression test exercises registration with this exact runtime representation. The 23 Direct Mode tests pass. Corrected source SHA-256: `94a53cbdd0e8ef7a049278f4975b857164462bd3ffdaef6864adeb8f1a7e728`. This second deployment is also superseded; a new deployment and successful on-chain lifecycle are still required before submission.

## Submission deployment

- Contract: `0xB6AF468338cC5C5d8bCB89A5830898b87425925a`
- Explorer: https://explorer-studio.genlayer.com/address/0xB6AF468338cC5C5d8bCB89A5830898b87425925a
- Chain ID: `61999`
- Local/deployed source SHA-256: `94a53cbbdd0e8ef7a049278f4975b857164462bd3ffdaef6864adeb8f1a7e728`
- Exact source parity: `true`
- Initial state: zero services and zero proposals.
- Registry controller was explicitly supplied to the constructor; deployment grants no implicit role.

### Successful lifecycle

- Register service: [`0x13a908b4c736f0a6d5f4f0bb496abffd06e1a06c902637bf2b326e1e1de3449d`](https://explorer-studio.genlayer.com/tx/0x13a908b4c736f0a6d5f4f0bb496abffd06e1a06c902637bf2b326e1e1de3449d)
- Propose sunset: [`0xef9c2c43a3b01787f52922d95bd410b264e1f8b0d4cc8b78d219150e9d33a896`](https://explorer-studio.genlayer.com/tx/0xef9c2c43a3b01787f52922d95bd410b264e1f8b0d4cc8b78d219150e9d33a896)
- Assess canonical evidence: [`0xcba96139cbfb3a41d7e54364f01b2d706615a8e9b03afe923e9af056ded0b75f`](https://explorer-studio.genlayer.com/tx/0xcba96139cbfb3a41d7e54364f01b2d706615a8e9b03afe923e9af056ded0b75f)
- Consume authorization: [`0x96f2f0588915b8024f40ba2cf603f30856414b051c9d317fd9a5b4fb6fe7a0d3`](https://explorer-studio.genlayer.com/tx/0x96f2f0588915b8024f40ba2cf603f30856414b051c9d317fd9a5b4fb6fe7a0d3)

Assessment readback returned `SUNSET_ELIGIBLE`, `AUTHORIZED`, and all seven diagnostic booleans `true`, including `provenance_ok` and `evaluation_complete`. Consumption changed the proposal to `CONSUMED`, set `authorization_consumed=1`, and advanced the service revision from 1 to 2.

### Adversarial authorization checks

- Wrong authorization digest: [`0x75ab67a040feaf16c7de04d1d0a7c1bac25a5c9d1c91218c187e146e05634246`](https://explorer-studio.genlayer.com/tx/0x75ab67a040feaf16c7de04d1d0a7c1bac25a5c9d1c91218c187e146e05634246) — full proposal state unchanged.
- Wrong action digest: [`0xa76836e69907c2a6d0799035e17f548b9671c9aeb9ccff35575075aaffb1f158`](https://explorer-studio.genlayer.com/tx/0xa76836e69907c2a6d0799035e17f548b9671c9aeb9ccff35575075aaffb1f158) — full proposal state unchanged.
- Replay after consumption: [`0xf7c7cc47bc0882093da6a33a106bc5ba53f9d63b7bce3a66afe2a6f94bb14361`](https://explorer-studio.genlayer.com/tx/0xf7c7cc47bc0882093da6a33a106bc5ba53f9d63b7bce3a66afe2a6f94bb14361) — full proposal state unchanged.

Canonical evidence is pinned to immutable commit `7d40a1b258b65fd6b392feefb0ced6c5d71f45d5`; the contract independently fetched the GitHub commit and complete tree, checked blob metadata and Git blob SHA-1, fetched raw bytes, recomputed every SHA-256 digest, verified service identity markers, and then performed the semantic assessment.
