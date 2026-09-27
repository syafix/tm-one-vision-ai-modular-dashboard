from dataclasses import dataclass
from fastapi import Header,HTTPException,status
from app.config import settings
@dataclass(frozen=True)
class Principal:
    subject:str; email:str; roles:set[str]; mfa:bool; tenant_code:str="tm-one"

def require_roles(*required):
    async def dependency(authorization:str|None=Header(default=None),x_dev_user:str|None=Header(default=None)):
        if settings.auth_mode=="dev":
            principal=Principal(settings.dev_user_subject,settings.dev_user_email,set(settings.dev_user_roles.split(",")),True)
        else:
            # Production OIDC intentionally fails closed until JWKS validation and the approved
            # Keycloak/Entra MFA claim contract are configured.
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE,"OIDC validation is not configured")
        if settings.mfa_required and not principal.mfa: raise HTTPException(403,"MFA assurance required")
        if required and not principal.roles.intersection(required): raise HTTPException(403,"Insufficient role")
        return principal
    return dependency
