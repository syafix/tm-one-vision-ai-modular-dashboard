from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,ConfigDict
class EventOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:UUID; code:str; name:str; venue:str|None; timezone:str; status:str
class MetricPoint(BaseModel): observed_at:datetime; value:float
class Kpi(BaseModel): key:str; label:str; value:float; unit:str; quality:str="valid"
class SourceHealth(BaseModel): id:UUID; name:str; connector_type:str; status:str; last_success_at:datetime|None
class AlertOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:UUID; severity:str; status:str; title:str; description:str|None; observed_at:datetime
class DashboardSummary(BaseModel): event:EventOut; kpis:list[Kpi]; visitor_series:list[MetricPoint]; alerts:list[AlertOut]; sources:list[SourceHealth]; layout:dict
