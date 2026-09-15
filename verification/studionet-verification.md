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
