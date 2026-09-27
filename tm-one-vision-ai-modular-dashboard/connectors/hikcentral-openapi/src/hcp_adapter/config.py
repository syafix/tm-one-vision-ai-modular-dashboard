from pydantic import Field, HttpUrl, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class HCPSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="HCP_", env_file=".env", extra="ignore")

    base_url: HttpUrl
    app_key: SecretStr = Field(min_length=1)
    app_secret: SecretStr = Field(min_length=1)
    verify_tls: bool = True
    ca_bundle: str | None = None
    timeout_seconds: float = Field(default=15.0, gt=0, le=120)
    max_retries: int = Field(default=2, ge=0, le=5)
    max_response_bytes: int = Field(default=5_242_880, ge=1024, le=52_428_800)

    @model_validator(mode="after")
    def secure_transport(self):
        if str(self.base_url).lower().startswith("http://"):
            raise ValueError("HTTPS is required for HCP OpenAPI")
        return self
