from __future__ import annotations

import base64
import hashlib
import hmac
import time
import uuid
from dataclasses import dataclass
from urllib.parse import urlencode

@dataclass(frozen=True)
class SignedHeaders:
    headers: dict[str, str]
    string_to_sign: str

EXCLUDED_CUSTOM_HEADERS = {
    "x-ca-signature", "x-ca-signature-headers", "accept", "content-md5",
    "content-type", "date", "content-length", "server", "connection", "host",
    "transfer-encoding", "x-application-context", "content-encoding",
}

def content_md5(body: bytes) -> str:
    return base64.b64encode(hashlib.md5(body, usedforsecurity=False).digest()).decode("ascii")

def canonical_uri(path: str, query: dict[str, object] | None = None) -> str:
    if not path.startswith("/"):
        raise ValueError("API path must start with /")
    if not query:
        return path
    pairs=[]
    for key in sorted(query):
        val=query[key]
        if isinstance(val, (list, tuple)):
            for item in val: pairs.append((key, str(item)))
        elif val is None:
            pairs.append((key, ""))
        else:
            pairs.append((key, str(val)))
    return f"{path}?{urlencode(pairs)}"

def sign_request(*, method: str, path: str, app_key: str, app_secret: str,
                 body: bytes=b"", query: dict[str, object] | None=None,
                 accept: str="*/*", content_type: str="application/json",
                 timestamp_ms: int | None=None, nonce: str | None=None,
                 custom_headers: dict[str, str] | None=None) -> SignedHeaders:
    timestamp=str(timestamp_ms if timestamp_ms is not None else int(time.time()*1000))
    nonce=nonce or str(uuid.uuid4())
    base={"x-ca-key":app_key, "x-ca-timestamp":timestamp, "x-ca-nonce":nonce}
    for k,v in (custom_headers or {}).items():
        lk=k.strip().lower()
        if lk in EXCLUDED_CUSTOM_HEADERS:
            continue
        base[lk]=str(v).strip()
    signed_names=sorted(base)
    canonical_headers="".join(f"{name}:{base[name]}\n" for name in signed_names)
    md5_value=content_md5(body) if body else ""
    string_to_sign=(
        f"{method.upper()}\n{accept}\n{md5_value}\n{content_type}\n\n"
        f"{canonical_headers}{canonical_uri(path, query)}"
    )
    digest=hmac.new(app_secret.encode(), string_to_sign.encode(), hashlib.sha256).digest()
    signature=base64.b64encode(digest).decode("ascii")
    headers={
        "Accept":accept,
        "Content-Type":content_type,
        "X-Ca-Key":app_key,
        "X-Ca-Timestamp":timestamp,
        "X-Ca-Nonce":nonce,
        "X-Ca-Signature-Headers":",".join(signed_names),
        "X-Ca-Signature":signature,
    }
    if body: headers["Content-MD5"]=md5_value
    for name,value in (custom_headers or {}).items(): headers[name]=value
    return SignedHeaders(headers=headers, string_to_sign=string_to_sign)
