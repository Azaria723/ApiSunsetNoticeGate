SERVICE_ID: PAYMENTS-API
NOTICE_ID: POST-V1-PAYMENTS-SUNSET

# POST /v1/payments sunset notice

`POST /v1/payments` is planned for retirement after the required notice period. Clients must migrate to `POST /v2/payments`.

Known limitation: legacy idempotency keys cannot be reused. Each migrated request must use a newly generated idempotency key. No other request field loses its essential payment-creation meaning.

Migration instructions are in `/evidence/migration-guide.md` at this same immutable revision.
