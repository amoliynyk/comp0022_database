import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_pool, close_pool, is_healthy
from app.auth.users import router as auth_router
from app.routers.movies import router as movies_router
from app.routers.genres import router as genres_router
from app.routers.ratings import router as ratings_router
from app.routers.predictions import router as predictions_router
from app.routers.personality import router as personality_router
from app.routers.collections import router as collections_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_pool()
    # Create app-owned tables
    try:
        from app.auth.db import ensure_app_users_table
        ensure_app_users_table()
    except Exception as e:
        logging.warning("Could not create app tables: %s", e)
    yield
    close_pool()


app = FastAPI(
    title="COMP0022 Film Analytics API",
    description="Backend API for the Film Analytics Dashboard",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "name": "COMP0022 Film Analytics API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    db_ok = is_healthy()
    return {
        "status": "healthy" if db_ok else "degraded",
        "database": "connected" if db_ok else "unavailable",
    }


app.include_router(auth_router)
app.include_router(movies_router)
app.include_router(genres_router)
app.include_router(ratings_router)
app.include_router(predictions_router)
app.include_router(personality_router)
app.include_router(collections_router)
