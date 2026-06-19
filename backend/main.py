"""
Bidding Radar - FastAPI Backend
領標雷達本地工具 — FastAPI 後端
"""
import os
import sys
from pathlib import Path

# Ensure backend dir is on path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import engine, Base
from backend.routers import tenders

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="領標雷達 API",
    description="政府標案與補助雷達 — 本地優先",
    version="0.1.0",
)

# CORS — allow local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(tenders.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "bidding-radar"}


@app.get("/")
def root():
    return {
        "service": "領標雷達 API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
    }
