# Payment creation migration guide

1. Replace `POST /v1/payments` with `POST /v2/payments`.
2. Preserve the `amount` and three-letter `currency` values.
3. Generate a new idempotency key for every migrated operation; do not copy a legacy key.
4. Send the request in a non-production environment and confirm the returned payment identifier.
5. Move production traffic only after the response and retry behavior have been verified.
