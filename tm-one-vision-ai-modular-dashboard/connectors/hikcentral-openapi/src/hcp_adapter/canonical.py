from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import uuid

def metric(*, event_id: str, source_id: str, metric_name: str, value: float,
           unit: str, observed_at: str | None=None, attributes: dict[str,Any] | None=None):
    return {
        "eventId": event_id,
        "sourceId": source_id,
        "metricName": metric_name,
        "value": value,
        "unit": unit,
        "observedAt": observed_at or datetime.now(timezone.utc).isoformat(),
        "quality": "valid",
        "correlationId": str(uuid.uuid4()),
        "attributes": attributes or {},
    }

def map_people_counts(record: dict[str,Any], *, event_id: str, source_id: str,
                      in_field: str, out_field: str, observed_at_field: str | None=None):
    observed=record.get(observed_at_field) if observed_at_field else None
    return [
        metric(event_id=event_id, source_id=source_id, metric_name="people.in",
               value=float(record[in_field]), unit="persons", observed_at=observed),
        metric(event_id=event_id, source_id=source_id, metric_name="people.out",
               value=float(record[out_field]), unit="persons", observed_at=observed),
    ]
