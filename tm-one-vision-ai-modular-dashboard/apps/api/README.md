# Backend API

FastAPI modular-monolith boundary for the MVP.

Required modules:
- identity and authorization
- events
- dashboard templates and publication
- metrics and aggregations
- alerts
- connector registry
- append-only audit service

All object access must be tenant/event scoped on the server side.
