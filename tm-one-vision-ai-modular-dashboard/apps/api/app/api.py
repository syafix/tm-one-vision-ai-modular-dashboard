from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.security import require_roles
from app.models import Alert,DataSource,DashboardConfig
from app.schemas import EventOut,DashboardSummary,Kpi,MetricPoint,AlertOut,SourceHealth
from app import repository as repo
router=APIRouter(prefix="/api/v1")
@router.get("/events",response_model=list[EventOut])
async def events(db:AsyncSession=Depends(get_db),_=Depends(require_roles("platform_admin","product_admin","event_operator","viewer"))): return await repo.list_events(db)
@router.get("/events/{event_id}/dashboard",response_model=DashboardSummary)
async def dashboard(event_id:UUID,db:AsyncSession=Depends(get_db),_=Depends(require_roles("platform_admin","product_admin","event_operator","viewer"))):
    event=await repo.get_event(db,event_id)
    if not event: raise HTTPException(404,"Event not found")
    definitions=[("people.in","Total Visitors","persons","max"),("people.occupancy","Current Occupancy","persons","latest"),("people.flow_rate","Peak Flow","persons/min","max"),("weather.temperature","Temperature","°C","latest"),("social.trend_score","Trend Score","index","latest")]
    kpis=[]
    for key,label,unit,mode in definitions:
        if mode=="latest":
            r=await repo.latest_metric(db,event_id,key); value=float(r.value) if r else 0; quality=r.quality if r else "unavailable"
        else: value=await repo.total_metric(db,event_id,key); quality="valid" if value else "unavailable"
        kpis.append(Kpi(key=key,label=label,value=value,unit=unit,quality=quality))
    pts=await repo.series(db,event_id,"people.in")
    alerts=list((await db.scalars(select(Alert).where(Alert.event_id==event_id).order_by(Alert.observed_at.desc()).limit(10))).all())
    sources=list((await db.scalars(select(DataSource).where(DataSource.event_id==event_id))).all())
    cfg=(await db.scalars(select(DashboardConfig).where(DashboardConfig.event_id==event_id))).first()
    return DashboardSummary(event=event,kpis=kpis,visitor_series=[MetricPoint(observed_at=x.observed_at,value=float(x.value)) for x in pts],alerts=alerts,sources=[SourceHealth(id=x.id,name=x.name,connector_type=x.connector_type,status=x.status,last_success_at=x.last_success_at) for x in sources],layout=cfg.config if cfg else {"widgets":[]})
