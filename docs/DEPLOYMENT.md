# Deployment checklist

1. Publish the repository and evidence fixtures.
2. Record one immutable full commit containing all five artifacts.
3. Compute SHA-256 over the exact raw bytes of every artifact.
4. Run `python -m pytest -q` and record the contract SHA-256.
5. Deploy `contracts/ApiSunsetNoticeGate.py` as a fresh Studionet instance with a dedicated test registry controller as the constructor argument. The deployer receives no role.
6. Fetch deployed source and prove exact source parity before any writes.
7. Register the demo service using repository coordinates, immutable policy commit/digest, 90-day minimum notice and a non-deployer test controller.
8. Run and read back these live branches: eligible/consume, notice failure, migration failure, provenance failure, wrong controller, wrong authorization digest, wrong action digest and replay.
9. For every rejected transaction, compare the complete relevant pre/post state rather than relying on finality alone.
10. Add transaction hashes and authoritative readbacks to `verification/studionet-verification.md`.

Do not publish private keys or describe private test-account operations in the public repository.
