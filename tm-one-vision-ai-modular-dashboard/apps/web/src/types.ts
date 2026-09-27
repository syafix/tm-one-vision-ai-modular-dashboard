export type EventItem={id:string;code:string;name:string;venue?:string;timezone:string;status:string};
export type Kpi={key:string;label:string;value:number;unit:string;quality:string};
export type Point={observed_at:string;value:number};
export type Alert={id:string;severity:string;status:string;title:string;description?:string;observed_at:string};
export type Source={id:string;name:string;connector_type:string;status:string;last_success_at?:string};
export type Dashboard={event:EventItem;kpis:Kpi[];visitor_series:Point[];alerts:Alert[];sources:Source[];layout:Record<string,unknown>};
