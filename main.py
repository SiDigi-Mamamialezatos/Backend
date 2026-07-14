from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.init_db import init_db
from app.api import api_router 


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Siagaku Backend",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# api_router already aggregates every resource router (users, modules,
# materials, attempts, badges, user-badges, chat-sessions, chat-messages),
# each with its own prefix/tags — so mounting it once here gives you
# /api/users, /api/modules, /api/materials, etc.
app.include_router(api_router, prefix="/api")


@app.get("/health")
def health_check():
    return {"status": "server is running okay"}