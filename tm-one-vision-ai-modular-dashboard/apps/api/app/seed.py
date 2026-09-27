import asyncio,uuid,math,random
from datetime import datetime,timezone,timedelta
from sqlalchemy import select
from app.db import init_db,SessionLocal
from app.models import Tenant,Event,DataSource,MetricReading,Alert,DashboardConfig
async def seed():
 await init_db()
 async with SessionLocal() as db:
  tenant=(await db.scalars(select(Tenant).where(Tenant.code=="tm-one"))).first()
  if not tenant: tenant=Tenant(code="tm-one",name="TM One"); db.add(tenant); await db.flush()
  event=(await db.scalars(select(Event).where(Event.code=="hsn-2026"))).first()
  if not event:
   now=datetime.now(timezone.utc); event=Event(tenant_id=tenant.id,code="hsn-2026",name="Hari Sukan Negara 2026",venue="Event Venue",status="published",start_at=now-timedelta(hours=3),end_at=now+timedelta(hours=6)); db.add(event); await db.flush()
   source=DataSource(tenant_id=tenant.id,event_id=event.id,name="HCP People Counting",connector_type="hikcentral-openapi",status="active",last_success_at=now); db.add(source); await db.flush()
   total=0
   for i in range(36):
    t=now-timedelta(minutes=(35-i)*5); flow=max(0,18+12*math.sin(i/4)+random.randint(-3,3)); total+=int(flow)
    for name,value,unit in [("people.in",total,"persons"),("people.flow_rate",flow,"persons/min"),("people.occupancy",max(0,total-int(total*.72)),"persons"),("weather.temperature",30+(i%4)*.2,"celsius"),("social.trend_score",65+min(i,25),"index")]: db.add(MetricReading(tenant_id=tenant.id,event_id=event.id,source_id=source.id,metric_name=name,value=value,unit=unit,observed_at=t,quality="valid"))
   db.add(Alert(tenant_id=tenant.id,event_id=event.id,severity="medium",title="Crowd increasing",description="Flow increased at the main entrance",observed_at=now-timedelta(minutes=8)))
   db.add(DashboardConfig(event_id=event.id,config={"theme":"tm-hsn","widgets":["kpis","visitorTrend","alerts","sourceHealth"]},published=True))
  await db.commit(); print(event.id)
if __name__=="__main__": asyncio.run(seed())
