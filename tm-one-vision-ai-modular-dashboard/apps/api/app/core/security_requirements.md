# API Security Requirements

- Validate OIDC issuer, audience, signature and expiry.
- Enforce required MFA assurance using the approved IdP/broker claim contract.
- Reject missing or untrusted MFA assurance.
- Authorize every object by tenant and event scope.
- Use parameterized database access only.
- Apply body, pagination, timeout and rate limits.
- Return generic errors with correlation IDs.
- Exclude tokens, secrets, personal images and biometric data from logs.
