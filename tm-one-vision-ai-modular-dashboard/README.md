# TM One Vision AI Modular Event Dashboard MVP

Runnable local MVP for reusable event dashboards. The baseline includes a React/TypeScript frontend, FastAPI backend, PostgreSQL, Keycloak identity-broker profile, mock HCP data, and the HCP OpenAPI V3.1.1 adapter.

## Local modes

### Fast start: mock identity + mock HCP
```bash
cp .env.example .env
docker compose up --build
```

Open:
- Dashboard: `http://localhost:5173`
- API docs: `http://localhost:8000/docs`
- API health: `http://localhost:8000/health/ready`

Development sign-in uses a clearly labelled mock user only when `AUTH_MODE=dev`. Never use this mode outside a local developer machine.

### Keycloak profile
```bash
docker compose --profile identity up --build
```

Keycloak is available at `http://localhost:8080`. Import/configure a realm locally, then set `AUTH_MODE=oidc`. Do not commit realm secrets or TM Entra credentials.

## Initial MVP functions
- Event list and event summary
- HSN sample event seed
- KPI cards for total visitors, occupancy, peak flow, weather and trend score
- Time-series visitor chart
- Alerts feed
- Camera/source health
- Modular widget registry and JSON event layout
- PostgreSQL persistence
- Dev mock-data generator
- HCP V3.1.1 adapter boundary
- Audit-table baseline
- OIDC/MFA policy hooks

## Mandatory HCP actions
- Rotate previously exposed Integration Partner credentials.
- Replace the linked HCP `admin` account with a dedicated least-privilege service user.
- Install a trusted TLS certificate and keep verification enabled.
- Authorise read-only APIs first.

See `docs/local-setup.md`, `docs/file-module-catalog.md`, and `docs/next-implementation-backlog.md`.
