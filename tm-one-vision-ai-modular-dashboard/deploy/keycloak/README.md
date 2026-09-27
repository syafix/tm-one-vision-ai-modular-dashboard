# Keycloak Identity Broker

Target design:
- TM Entra ID remains the upstream enterprise identity provider.
- Keycloak acts as broker for the dashboard platform and future external/customer identity providers.
- MFA is mandatory and cannot be bypassed through a local login route.
- Local accounts are disabled unless explicitly approved and covered by equivalent MFA.
- Administrative access uses named accounts, MFA and privileged-access controls.
- Backend validates trusted MFA assurance in addition to normal token validation.

Realm exports and client secrets must not be committed. Store deployment configuration through approved protected CI/CD variables and secrets management.
