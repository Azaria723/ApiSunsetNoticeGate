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
