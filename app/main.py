from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.api import api_router
from fastapi.openapi.utils import get_openapi
from app.db.init_db import init_db
from app.utils.openapi_utils import custom_openapi

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    init_db()
    yield

app = FastAPI(
    title="Cap Table Management API",
    description="API for managing company capitalization tables",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.openapi = custom_openapi(app)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Cap Table Management API is running"}