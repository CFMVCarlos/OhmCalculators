from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.routes.api import router as api_router
from starlette.exceptions import HTTPException as StarletteHTTPException
import sys
from pathlib import Path
import uvicorn

# Setup path for jinja templates
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="OhmCalculators API",
    description="API for calculating voltage dividers and optimal resistor combinations",
    version="1.0.0",
)


# Global exception handlers to never expose stack traces to clients
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": exc.detail, "code": exc.status_code},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    msg = errors[0]["msg"] if errors else "Invalid request data"
    if msg.startswith("Value error, "):
        msg = msg.replace("Value error, ", "")
    return JSONResponse(
        status_code=422, content={"status": "error", "message": msg, "code": 422}
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
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
async def serve_frontend(request: Request):
    return templates.TemplateResponse(request, "index.html")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
