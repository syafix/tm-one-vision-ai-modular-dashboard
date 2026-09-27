# Next Implementation Backlog

## Required before pilot integration
1. Implement production OIDC/JWKS validation and approved Keycloak-to-Entra MFA assurance mapping.
2. Add Alembic migrations and PostgreSQL row-level security evaluation.
3. Add tenant/event authorization tests and audit writes for every administrative action.
4. Wire HCP resource sync and people-counting mapping to canonical metrics.
5. Add event subscription webhook receiver with signature/source validation, replay protection and dead-letter processing.
6. Replace local synthetic data with captured, sanitized, version-matched API fixtures.
7. Add Marketing event composer and controlled publish workflow.
8. Add weather and trend providers only after API/licence approval.
9. Add production WAF/API gateway, SIEM forwarding, EDR/container controls and secrets manager.
10. Complete SAST, SCA, SBOM, container scan, DAST/API VAPT and performance testing.
