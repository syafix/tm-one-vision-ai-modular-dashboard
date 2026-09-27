from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
    database_url:str="postgresql+asyncpg://vision_ai_app:change-local-only@localhost:5432/vision_ai"
    auth_mode:str="dev"
    dev_user_subject:str="local-developer"
    dev_user_email:str="developer@example.local"
    dev_user_roles:str="platform_admin,product_admin,event_operator"
    oidc_issuer:str=""
    oidc_audience:str="vision-ai-api"
    mfa_required:bool=True
    cors_origins:str="http://localhost:5173"
    hcp_enabled:bool=False
    @property
    def origins(self): return [x.strip() for x in self.cors_origins.split(",") if x.strip()]
settings=Settings()
