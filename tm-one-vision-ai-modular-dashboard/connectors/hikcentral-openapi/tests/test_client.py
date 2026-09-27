import json, httpx, pytest
from hcp_adapter.client import HCPClient

@pytest.mark.asyncio
async def test_platform_version():
    async def handler(request):
        assert request.headers["X-Ca-Key"]=="k"
        return httpx.Response(200,json={"code":"0","msg":"success","data":{"version":"3.1.1"}})
    client=HCPClient(base_url="https://hcp.example",app_key="k",app_secret="s",
                     transport=httpx.MockTransport(handler))
    async with client:
        value=await client.platform_version()
    assert value["data"]["version"]=="3.1.1"
