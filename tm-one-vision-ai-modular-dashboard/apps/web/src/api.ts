import type {Dashboard,EventItem} from "./types";
const base=import.meta.env.VITE_API_BASE_URL||"http://localhost:8000/api/v1";
async function request<T>(path:string):Promise<T>{const r=await fetch(base+path,{headers:{"X-Dev-User":"local"}});if(!r.ok)throw new Error(`API ${r.status}`);return r.json()}
export const api={events:()=>request<EventItem[]>("/events"),dashboard:(id:string)=>request<Dashboard>(`/events/${id}/dashboard`)};
