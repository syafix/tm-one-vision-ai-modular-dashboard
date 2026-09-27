from datetime import datetime,timezone,timedelta
from uuid import UUID
from sqlalchemy import select,func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Event,MetricReading,Alert,DataSource,DashboardConfig
async def list_events(db): return list((await db.scalars(select(Event).order_by(Event.name))).all())
async def get_event(db,event_id): return await db.get(Event,event_id)
async def latest_metric(db,event_id,name):
    q=select(MetricReading).where(MetricReading.event_id==event_id,MetricReading.metric_name==name).order_by(MetricReading.observed_at.desc()).limit(1)
    return (await db.scalars(q)).first()
async def total_metric(db,event_id,name):
    q=select(func.coalesce(func.max(MetricReading.value),0)).where(MetricReading.event_id==event_id,MetricReading.metric_name==name)
    return float((await db.scalar(q)) or 0)
async def series(db,event_id,name,limit=48):
    q=select(MetricReading).where(MetricReading.event_id==event_id,MetricReading.metric_name==name).order_by(MetricReading.observed_at.desc()).limit(limit)
    return list(reversed(list((await db.scalars(q)).all())))
