# Security Notes

- TLS verification is enabled by default. Use a trusted enterprise CA bundle, never `verify=False` in production.
- AppSecret must come from a secrets manager and must not be logged.
- The adapter follows the V3.1.1 AK/SK signature format with HMAC-SHA256 and Base64.
- Timestamp and nonce are signed to support anti-replay. Keep HCP and adapter clocks synchronized.
- The Integration Partner must be linked to a least-privilege HCP user and authorised only for required APIs.
- `door_control()` is a high-risk operation. Put it behind a separate application permission, step-up MFA, approval policy and immutable audit event.
- Do not persist face images, access pictures or personal data unless the use case and retention are approved.
- Do not log full API bodies for person, face, visitor or access-control endpoints.
- Pin dependencies after SCA/licence review, generate an SBOM and sign the release artifact.
