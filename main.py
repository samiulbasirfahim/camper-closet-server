from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from core.config import settings
from core.lifespan import lifespan
from core.error_handlers import (
    validation_exception_handler,
    http_exception_handler
)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan
)


app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler  # type: ignore
)
app.add_exception_handler(
    HTTPException,
    http_exception_handler  # type: ignore
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Camper Closet Backend!",
    }
