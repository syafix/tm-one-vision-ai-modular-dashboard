# Local Setup

## Prerequisites
- Git
- Docker Desktop or Docker Engine with Compose v2
- Free local ports 5173, 8000 and 5432

## Setup
```bash
git clone <your-repository-url>
cd tm-one-vision-ai-modular-dashboard
cp .env.example .env
docker compose up --build -d
docker compose exec api python -m app.seed
```

Browse to `http://localhost:5173`. API documentation is at `http://localhost:8000/docs`.

## Useful commands
```bash
docker compose ps
docker compose logs -f api web
docker compose exec api pytest
docker compose exec api ruff check app tests
docker compose down
docker compose down -v  # deletes local database volume
```

## Local development without Docker
Backend:
```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.main:app --reload
```

Frontend:
```bash
cd apps/web
npm install
npm run dev
```

Use Docker PostgreSQL or update `DATABASE_URL` for the local database.

## Keycloak profile
```bash
docker compose --profile identity up --build
```
The committed repository intentionally does not contain a production realm export or TM Entra credentials. Configure the identity broker securely, then replace `AUTH_MODE=dev` with `AUTH_MODE=oidc`. The backend currently fails closed in OIDC mode until JWKS/token and MFA-claim validation are implemented and reviewed.

## HCP integration
Set `HCP_ENABLED=true` only after credentials are rotated, CA trust is configured, and read-only APIs are authorised. Secrets must be injected from a secrets manager rather than committed to `.env` in shared environments.
