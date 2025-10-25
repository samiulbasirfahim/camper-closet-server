
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse


async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
) -> JSONResponse:

    mapped_errors = []
    for err in exc.errors():
        mapped_errors.append({
            "loc": ".".join(map(str, err.get("loc", []))),
            "msg": err.get("msg", ""),
            "type": err.get("type", "")
        })

    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation Error",
            "errors": mapped_errors
        }
    )


async def http_exception_handler(
        request: Request,
        exc: HTTPException
) -> JSONResponse:

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail,
            "errors": []
        }
    )
