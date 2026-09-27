# Endpoint Scope Included

The adapter exposes wrappers for documented V3.1.1 paths relevant to the MVP:

- Platform version
- Access-control device list
- Encoding-device list
- Camera list via configurable request body
- People statistics total, passenger flow, attributes, real-time resource-group count and heat map
- Preview/playback URLs and camera capture
- Event record search and event subscribe/unsubscribe
- Access-control event search, event pictures, privilege groups and door control

Payload schemas are intentionally passed as dictionaries because availability and request fields vary by authorised API and deployed HCP capability. Use the V3.1.1 OpenAPI Gateway online documentation as the source of truth and add Pydantic request models only after capturing approved sample payloads.
