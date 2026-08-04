"""FastAPI application setup.

Contains ONLY app factory concerns: middleware, CORS, exception handlers,
lifespan. No route logic or direct router imports besides api_router.
"""

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api import api_router
from src.config import settings
from src.exceptions import AppException


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Application lifespan — startup/shutdown hooks."""
    # Startup: eager-init the Supabase client
    from src.database import get_supabase_client

    get_supabase_client()
    yield
    # Shutdown: nothing to clean up


app = FastAPI(
    title="SARAT NARAK API",
    description="Backend API for the SARAT NARAK portfolio.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow both Nuxt origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_origin_regex=r"https://.*\.vercel\.app|http://localhost:\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Catch all domain exceptions and return a uniform JSON error."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.error_code,
            "detail": exc.detail,
        },
    )


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint for FastAPI Cloud deployment."""
    return {"status": "ok"}


# Mount all API routes
app.include_router(api_router)
