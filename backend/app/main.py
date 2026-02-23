from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.config import settings
from app.core.database import init_db
from app.api.api import api_router
import traceback
import sys
import os

# Build unified CORS origins from config + FRONTEND_URL env var
ALLOWED_ORIGINS = list(settings.BACKEND_CORS_ORIGINS)
_frontend_url = os.getenv("FRONTEND_URL", "")
if _frontend_url and _frontend_url not in ALLOWED_ORIGINS:
    ALLOWED_ORIGINS.append(_frontend_url)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_db()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "app": "SETU",
        "authentication": "Clerk",
        "status": "online"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


def _cors_headers(request: Request) -> dict:
    origin = request.headers.get("origin", "")
    if origin in ALLOWED_ORIGINS:
        return {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
        }
    return {}


def _log_error(request: Request, exc: Exception):
    """Log error to both console and file"""
    error_msg = f"ERROR: {request.method} {request.url}\n  Exception: {exc}\n{traceback.format_exc()}\n"
    print(error_msg, flush=True)
    sys.stderr.write(error_msg)
    sys.stderr.flush()
    # Also write to file for reliable reading
    try:
        with open("error.log", "a") as f:
            f.write(f"\n{'='*60}\n{error_msg}")
    except:
        pass


# Handle FastAPI/Starlette HTTPExceptions (401, 403, 404, 422, etc.)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    _log_error(request, exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=_cors_headers(request),
    )


# Handle all other unexpected exceptions (500s)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    _log_error(request, exc)
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"},
        headers=_cors_headers(request),
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
