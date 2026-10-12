"""Main application entry point for the OhmCalculators FastAPI service."""

from pathlib import Path
from typing import Any
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn
from src.routes.api import router as api_router

# Setup path for jinja templates
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="OhmCalculators API",
    description="API for calculating voltage dividers and optimal resistor combinations",
    version="1.0.0",
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Format HTTP exceptions as standard JSON responses.

    Parameters
    ----------
    request : Request
        Incoming HTTP request.
    exc : StarletteHTTPException
        Exception raised during request handling.

    Returns
    -------
    JSONResponse
        Standardized error response payload.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": exc.detail, "code": exc.status_code},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Format schema validation errors as client-friendly JSON.

    Parameters
    ----------
    request : Request
        Incoming HTTP request.
    exc : RequestValidationError
        Validation errors encountered by Pydantic.

    Returns
    -------
    JSONResponse
        HTTP 422 JSON response with extracted error message.
    """
    errors = exc.errors()
    msg = errors[0]["msg"] if errors else "Invalid request data"
    if msg.startswith("Value error, "):
        msg = msg.replace("Value error, ", "")
    return JSONResponse(
        status_code=422, content={"status": "error", "message": msg, "code": 422}
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all unhandled exception handler suppressing stack traces.

    Parameters
    ----------
    request : Request
        Incoming HTTP request.
    exc : Exception
        Unhandled exception instance.

    Returns
    -------
    JSONResponse
        Generic internal server error JSON response.
    """
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Internal server error.", "code": 500},
    )


# Include API router
app.include_router(api_router, prefix="/api")

# Static files and templates setup
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "static/templates"))


@app.get("/")
async def serve_frontend(request: Request) -> Any:
    """Serve the primary HTML application frontend.

    Parameters
    ----------
    request : Request
        Incoming HTTP request.

    Returns
    -------
    Any
        Rendered Jinja2 HTML template response.
    """
    return templates.TemplateResponse(request, "index.html")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
