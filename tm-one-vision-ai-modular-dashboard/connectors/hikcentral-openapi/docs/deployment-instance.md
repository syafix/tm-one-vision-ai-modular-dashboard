# Current HCP Instance Configuration

## Observed instance
- HCP version: 3.1.1.20260724
- Current host: 175.140.166.217
- Integration Partner: TM-One-Vision-AI-Dashboard
- Current Domain ID selection: WAN (ID: 1)

## Mandatory remediation before use
1. Rotate the Integration Partner Key and Secret because credentials were visibly exposed in a screenshot.
2. Do not link the integration partner to the built-in `admin` user. Create a dedicated, named least-privilege HCP user such as `svc_vai_dashboard`.
3. Authorize only required API groups for discovery, camera resources, people analytics, event service and required access-control read operations.
4. Do not authorize remote door-control APIs until step-up MFA, separate permission, approval and immutable audit controls exist.
5. Replace the untrusted/self-signed browser certificate with a certificate trusted by the adapter host. Prefer a DNS name in the certificate SAN instead of direct IP access.
6. Keep TLS verification enabled. Import the issuing CA chain into `/etc/ssl/certs/hcp-openapi-ca.pem` or the host trust store.
7. Store the rotated Key/Secret only in the approved secrets manager and inject them at runtime.
8. Confirm HCP and adapter hosts use synchronized NTP time.

## Least-privilege role baseline
Read-only permissions initially:
- Common/platform version
- Resource query for camera and access-control device inventory
- Required people-counting/analytics query APIs
- Event record search and event subscription where needed
- Preview URL or capture only if approved

Excluded initially:
- Person creation/modification
- Card/biometric enrollment
- Permission assignment
- Remote door open/control
- Platform administration

## Initial connectivity command
After injecting rotated credentials into the runtime environment:

```bash
python examples/discovery.py
```

Do not place credentials in shell history, source code, screenshots, tickets or application logs.
