import base64, hashlib, hmac
from hcp_adapter.signing import sign_request

def test_signing_is_deterministic():
    result=sign_request(method="POST",path="/artemis/api/common/v1/version",
        app_key="key",app_secret="secret",body=b"{}",timestamp_ms=1700000000000,
        nonce="00000000-0000-0000-0000-000000000000",
        custom_headers={"X-Correlation-Id":"corr"})
    expected=base64.b64encode(hmac.new(b"secret",result.string_to_sign.encode(),hashlib.sha256).digest()).decode()
    assert result.headers["X-Ca-Signature"]==expected
    assert result.headers["X-Ca-Key"]=="key"
    assert "x-ca-nonce" in result.headers["X-Ca-Signature-Headers"]
    assert "/artemis/api/common/v1/version" in result.string_to_sign
