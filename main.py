from contextlib import asynccontextmanager
from fastapi import FastAPI
# from app.api.v1 import auth
from app.core.config import settings
from app.db.init_db import init_db

from app.api.auth import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield 

app = FastAPI(
    title="Backend Application",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["Auth"]
)

@app.get("/health")
def health_check():
    return {"status": "server is running okay"}