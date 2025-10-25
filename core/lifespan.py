from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.db import initialize_models


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    initialize_models()
    yield
    print("Shutting down...")
