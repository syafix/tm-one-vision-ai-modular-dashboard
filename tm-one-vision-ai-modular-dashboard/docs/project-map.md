# Project Map

## Runtime flow
User -> WAF/API Gateway -> Web/API -> Connector -> HCP/Camera/Access Control

## Identity flow
User -> Keycloak -> TM Entra ID -> mandatory MFA -> trusted token -> API authorization

## Data flow
Vendor payload -> validation -> normalization -> canonical metric/event -> PostgreSQL -> aggregation -> dashboard widget

## Configuration flow
Marketing Editor -> draft layout/theme -> Product approval -> immutable published dashboard configuration
