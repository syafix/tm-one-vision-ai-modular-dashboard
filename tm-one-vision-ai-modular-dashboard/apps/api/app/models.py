import uuid
from datetime import datetime
from sqlalchemy import String,DateTime,ForeignKey,Numeric,JSON,Boolean,Integer,func
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
class Base(DeclarativeBase): pass
class Tenant(Base):
    __tablename__="tenants"; id:Mapped[uuid.UUID]=mapped_column(primary_key=True,default=uuid.uuid4); code:Mapped[str]=mapped_column(String(64),unique=True); name:Mapped[str]=mapped_column(String(200))
class Event(Base):
    __tablename__="events"; id:Mapped[uuid.UUID]=mapped_column(primary_key=True,default=uuid.uuid4); tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id")); code:Mapped[str]=mapped_column(String(64)); name:Mapped[str]=mapped_column(String(200)); venue:Mapped[str|None]=mapped_column(String(300)); timezone:Mapped[str]=mapped_column(String(64),default="Asia/Kuala_Lumpur"); status:Mapped[str]=mapped_column(String(20),default="draft"); start_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True)); end_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
class DataSource(Base):
    __tablename__="data_sources"; id:Mapped[uuid.UUID]=mapped_column(primary_key=True,default=uuid.uuid4); tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id")); event_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("events.id")); name:Mapped[str]=mapped_column(String(200)); connector_type:Mapped[str]=mapped_column(String(100)); status:Mapped[str]=mapped_column(String(30),default="active"); last_success_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
class MetricReading(Base):
    __tablename__="metric_readings"; id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True); tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id")); event_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("events.id")); source_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("data_sources.id")); metric_name:Mapped[str]=mapped_column(String(120)); value:Mapped[float]=mapped_column(Numeric); unit:Mapped[str]=mapped_column(String(50)); observed_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),index=True); quality:Mapped[str]=mapped_column(String(20),default="valid")
class Alert(Base):
    __tablename__="alerts"; id:Mapped[uuid.UUID]=mapped_column(primary_key=True,default=uuid.uuid4); tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id")); event_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("events.id")); severity:Mapped[str]=mapped_column(String(20)); status:Mapped[str]=mapped_column(String(30),default="open"); title:Mapped[str]=mapped_column(String(200)); description:Mapped[str|None]=mapped_column(String(1000)); observed_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=func.now())
class DashboardConfig(Base):
    __tablename__="dashboard_configs"; id:Mapped[uuid.UUID]=mapped_column(primary_key=True,default=uuid.uuid4); event_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("events.id"),unique=True); version:Mapped[int]=mapped_column(Integer,default=1); config:Mapped[dict]=mapped_column(JSON); published:Mapped[bool]=mapped_column(Boolean,default=True)
