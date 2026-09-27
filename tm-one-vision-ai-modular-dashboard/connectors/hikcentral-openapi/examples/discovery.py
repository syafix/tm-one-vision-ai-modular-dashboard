import asyncio, json
from hcp_adapter import HCPClient, HCPSettings
from hcp_adapter.endpoints import Endpoint

async def main():
    settings=HCPSettings()
    async with HCPClient.from_settings(settings) as hcp:
        results={"version":await hcp.platform_version()}
        # Enable these only after the Integration Partner is authorised for them.
        # results["cameras"]=await hcp.camera_list({"pageNo":1,"pageSize":10})
        # results["acsDevices"]=await hcp.acs_device_list({"pageNo":1,"pageSize":10})
        print(json.dumps(results,indent=2,ensure_ascii=False))

if __name__=="__main__": asyncio.run(main())
