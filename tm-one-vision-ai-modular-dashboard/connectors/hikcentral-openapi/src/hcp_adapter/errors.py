class HCPError(Exception):
    """Base adapter error."""

class HCPTransportError(HCPError):
    pass

class HCPAuthError(HCPError):
    pass

class HCPAPIError(HCPError):
    def __init__(self, message: str, *, code: str | None = None, correlation_id: str | None = None):
        super().__init__(message)
        self.code = code
        self.correlation_id = correlation_id
