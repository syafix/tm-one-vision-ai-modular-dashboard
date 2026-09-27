# HCP OpenAPI Adapter V3.1.1

> Security notice: rotate the currently exposed Integration Partner credentials before testing. Do not use the built-in admin account as the linked user. See `docs/deployment-instance.md`.

A secure Python adapter for HikCentral Professional OpenAPI V3.1.1 using AK/SK request signing.

## What is included
- HMAC-SHA256 + Base64 request signing
- `X-Ca-Key`, `X-Ca-Signature`, `X-Ca-Signature-Headers`, `X-Ca-Timestamp`, `X-Ca-Nonce`
- TLS verification on by default
- Timeouts, retry for transient failures, response-size guard and structured errors
- Generic signed request method
- Endpoint wrappers for platform version, resources, people analytics, video, event and access-control APIs
- Safe pagination helper
- Canonical metric mapping hooks for the event dashboard
- Unit tests for deterministic signing and response handling

## Important
The exact APIs exposed depend on the HCP deployment, licences, linked devices and APIs authorised for the Integration Partner. Check the actual OpenAPI Gateway list before enabling a wrapper.

Never commit AppSecret. Load AppKey/AppSecret from the enterprise secrets manager at runtime.

## Quick start
```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
pytest
```

```python
import asyncio
from hcp_adapter import HCPClient, HCPSettings

async def main():
    settings = HCPSettings()
    async with HCPClient.from_settings(settings) as hcp:
        print(await hcp.platform_version())
        cameras = await hcp.camera_list({"pageNo": 1, "pageSize": 100})
        print(cameras)

asyncio.run(main())
```

## Deployment checks
1. Enable Open Platform/OpenAPI Gateway.
2. Create a dedicated Integration Partner linked to a least-privilege HCP user.
3. Authorise only required APIs.
4. Install a trusted service certificate and configure `HCP_CA_BUNDLE` when using a private CA.
5. Verify HCP/server time synchronisation because timestamp and nonce are part of anti-replay controls.
6. Run the discovery script without exposing secrets in logs.
