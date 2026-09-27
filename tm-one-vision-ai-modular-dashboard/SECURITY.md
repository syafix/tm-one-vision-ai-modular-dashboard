# Security Policy

- Never commit credentials, tokens, certificates or production payloads.
- Report suspected exposure immediately and rotate affected credentials.
- All interactive users, including administrators, require MFA.
- Backend/API enforcement must validate issuer, audience, signature, expiry, tenant/event scope, role and required MFA assurance.
- Remote physical-control functions require separate permissions, step-up MFA, approval and immutable audit logging.
- Production artifacts require SAST, SCA, secrets, container/IaC scan, SBOM and signature verification.
