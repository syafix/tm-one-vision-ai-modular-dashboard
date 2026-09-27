# File and Module Catalogue

## Root
- `README.md`: project overview and run sequence.
- `compose.yaml`: local PostgreSQL, API, web and optional Keycloak services.
- `.env.example`: safe configuration placeholders.
- `Makefile`: common local commands.
- `SECURITY.md`: repository security policy.
- `CONTRIBUTING.md`: contribution and review rules.

## Frontend
- `apps/web/package.json`: frontend scripts and dependencies.
- `apps/web/Dockerfile`: local web container.
- `apps/web/src/App.tsx`: event dashboard screen.
- `apps/web/src/api.ts`: typed backend client.
- `apps/web/src/types.ts`: shared UI response types.
- `apps/web/src/styles.css`: responsive command-centre styling.
- `apps/web/src/widgets/registry.example.ts`: approved modular widget types.

## Backend
- `apps/api/app/main.py`: FastAPI startup, CORS and health endpoints.
- `apps/api/app/config.py`: environment validation.
- `apps/api/app/db.py`: async PostgreSQL engine/session.
- `apps/api/app/models.py`: MVP persistence models.
- `apps/api/app/schemas.py`: public API response contracts.
- `apps/api/app/security.py`: dev identity and fail-closed production OIDC hook.
- `apps/api/app/repository.py`: scoped data queries and aggregations.
- `apps/api/app/api.py`: event/dashboard endpoints.
- `apps/api/app/seed.py`: synthetic local HSN demo data.
- `apps/api/tests/test_health.py`: health test baseline.

## Connectors
- `connectors/hikcentral-openapi/`: secure HCP V3.1.1 adapter, signing, endpoints, tests and deployment notes.
- `connectors/hikvision-camera-isapi/`: direct camera-adapter boundary.
- `connectors/hikvision-access-isapi/`: access-control-adapter boundary.
- `connectors/weather/`: approved weather-provider boundary.
- `connectors/trends/`: approved trend/social-listening boundary.

## Data, deployment and security
- `database/schema.sql`: expanded database design reference.
- `packages/contracts/`: canonical metric and event configuration contracts.
- `deploy/keycloak/`: identity-broker design notes.
- `deploy/kubernetes/`: future deployment overlays.
- `security/`: release gates, threat model, SCA/SAST and SBOM evidence areas.
- `docs/technical-discovery-hikvision.md`: API discovery checklist.
