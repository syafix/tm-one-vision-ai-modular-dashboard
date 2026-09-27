from __future__ import annotations

import asyncio
import json
import random
import uuid
from typing import Any, AsyncIterator

import httpx
from .config import HCPSettings
from .endpoints import Endpoint
from .errors import HCPAPIError, HCPAuthError, HCPTransportError
from .signing import sign_request

class HCPClient:
    def __init__(self, *, base_url: str, app_key: str, app_secret: str,
                 verify: bool | str=True, timeout_seconds: float=15,
                 max_retries: int=2, max_response_bytes: int=5_242_880,
                 transport: httpx.AsyncBaseTransport | None=None):
        self._base_url=base_url.rstrip("/")
        self._app_key=app_key
        self._app_secret=app_secret
        self._max_retries=max_retries
        self._max_response_bytes=max_response_bytes
        self._client=httpx.AsyncClient(
            base_url=self._base_url, verify=verify,
            timeout=httpx.Timeout(timeout_seconds, connect=min(timeout_seconds,10)),
            follow_redirects=False, transport=transport,
            limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
        )

    @classmethod
    def from_settings(cls, s: HCPSettings):
        verify = s.ca_bundle if s.ca_bundle else s.verify_tls
        return cls(base_url=str(s.base_url), app_key=s.app_key.get_secret_value(),
                   app_secret=s.app_secret.get_secret_value(), verify=verify,
                   timeout_seconds=s.timeout_seconds, max_retries=s.max_retries,
                   max_response_bytes=s.max_response_bytes)

    async def __aenter__(self): return self
    async def __aexit__(self, *_): await self.aclose()
    async def aclose(self): await self._client.aclose()

    async def request(self, method: str, path: str, *, body: dict[str,Any] | None=None,
                      query: dict[str,object] | None=None, correlation_id: str | None=None) -> dict[str,Any]:
        payload=json.dumps(body or {}, separators=(",",":"), ensure_ascii=False).encode("utf-8")
        correlation_id=correlation_id or str(uuid.uuid4())
        signed=sign_request(method=method, path=path, app_key=self._app_key,
                            app_secret=self._app_secret, body=payload, query=query,
                            custom_headers={"X-Correlation-Id":correlation_id})
        last_error=None
        for attempt in range(self._max_retries+1):
            try:
                response=await self._client.request(method, path, params=query, content=payload, headers=signed.headers)
                if len(response.content)>self._max_response_bytes:
                    raise HCPTransportError("HCP response exceeds configured size limit")
                if response.status_code in (401,403):
                    raise HCPAuthError(f"HCP rejected credentials or permission, HTTP {response.status_code}")
                if response.status_code in (429,502,503,504) and attempt < self._max_retries:
                    retry_after=response.headers.get("Retry-After")
                    delay=float(retry_after) if retry_after and retry_after.isdigit() else (0.5*(2**attempt)+random.random()/10)
                    await asyncio.sleep(min(delay,5))
                    continue
                response.raise_for_status()
                data=response.json()
                if not isinstance(data,dict): raise HCPAPIError("Unexpected HCP response type", correlation_id=correlation_id)
                code=str(data.get("code", "0"))
                if code not in ("0","success","200"):
                    raise HCPAPIError(str(data.get("msg") or data.get("message") or "HCP API error"), code=code, correlation_id=correlation_id)
                return data
            except (httpx.TimeoutException,httpx.NetworkError) as exc:
                last_error=exc
                if attempt < self._max_retries:
                    await asyncio.sleep(min(0.5*(2**attempt)+random.random()/10,5)); continue
                break
            except httpx.HTTPStatusError as exc:
                raise HCPTransportError(f"HCP HTTP error {exc.response.status_code}") from exc
            except ValueError as exc:
                raise HCPTransportError("HCP returned non-JSON data") from exc
        raise HCPTransportError("Unable to reach HCP OpenAPI") from last_error

    async def post(self, path: str, body: dict[str,Any] | None=None):
        return await self.request("POST", path, body=body)

    async def platform_version(self): return await self.post(Endpoint.VERSION, {})
    async def acs_device_list(self, body): return await self.post(Endpoint.ACS_DEVICES, body)
    async def encode_device_list(self, body): return await self.post(Endpoint.ENCODE_DEVICES, body)
    async def camera_list(self, body): return await self.post(Endpoint.CAMERAS, body)
    async def people_total_by_time(self, body): return await self.post(Endpoint.PEOPLE_TOTAL_BY_TIME, body)
    async def passenger_flow(self, body): return await self.post(Endpoint.PASSENGER_FLOW, body)
    async def people_attributes(self, body): return await self.post(Endpoint.PEOPLE_ATTRIBUTES, body)
    async def people_realtime_count(self, body): return await self.post(Endpoint.PEOPLE_REALTIME_COUNT, body)
    async def people_heatmap(self, body): return await self.post(Endpoint.PEOPLE_HEATMAP, body)
    async def preview_urls(self, body): return await self.post(Endpoint.PREVIEW_URL_V2, body)
    async def playback_urls(self, body): return await self.post(Endpoint.PLAYBACK_URL, body)
    async def capture(self, body): return await self.post(Endpoint.CAPTURE, body)
    async def event_records(self, body): return await self.post(Endpoint.EVENT_RECORDS, body)
    async def subscribe_events(self, body): return await self.post(Endpoint.EVENT_SUBSCRIBE, body)
    async def unsubscribe_events(self, body): return await self.post(Endpoint.EVENT_UNSUBSCRIBE, body)
    async def access_events(self, body): return await self.post(Endpoint.ACS_DOOR_EVENTS, body)
    async def access_event_picture(self, body): return await self.post(Endpoint.ACS_EVENT_PICTURES, body)
    async def privilege_groups(self, body): return await self.post(Endpoint.ACS_PRIVILEGE_GROUPS, body)

    async def door_control(self, body):
        # Deliberately separate high-risk operation. Caller must enforce step-up MFA,
        # explicit permission, approval policy and audit before invoking.
        return await self.post(Endpoint.ACS_DOOR_CONTROL, body)

    async def paged(self, path: str, base_body: dict[str,Any] | None=None,
                    *, page_size: int=100, max_pages: int=1000) -> AsyncIterator[dict[str,Any]]:
        if page_size < 1 or page_size > 100: raise ValueError("page_size must be 1..100")
        body=dict(base_body or {})
        for page_no in range(1,max_pages+1):
            body.update({"pageNo":page_no,"pageSize":page_size})
            response=await self.post(path, body)
            data=response.get("data") or {}
            items=data.get("list") or []
            if not isinstance(items,list): raise HCPAPIError("Paged response list is invalid")
            for item in items:
                if isinstance(item,dict): yield item
            total=data.get("total")
            if not items or (isinstance(total,int) and page_no*page_size>=total): return
        raise HCPAPIError("Pagination safety limit exceeded")
