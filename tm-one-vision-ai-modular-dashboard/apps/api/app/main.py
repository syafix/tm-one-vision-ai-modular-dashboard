from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.db import init_db
from app.api import router
@asynccontextmanager
async def lifespan(app):
    await init_db(); yield
app=FastAPI(title="Vision AI Event Dashboard API",version="0.1.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=settings.origins,allow_credentials=False,allow_methods=["GET","POST","PUT"],allow_headers=["Authorization","Content-Type","X-Correlation-Id","X-Dev-User"])
app.include_router(router)
@app.get("/health/live")
async def live(): return {"status":"ok"}
@app.get("/health/ready")
async def ready(): return {"status":"ready","authMode":settings.auth_mode}
