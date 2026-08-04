"""API router registry.

Every new domain router is imported and included here — never in main.py.
"""

from fastapi import APIRouter

from src.auth.router import router as auth_router
from src.project.router import router as project_router
from src.profile.router import router as profile_router
from src.tech_stack.router import router as tech_stack_router
from src.stats.router import router as stats_router
from src.social_media.router import router as social_media_router
from src.skill_categories.router import router as skill_categories_router
from src.qr_auth.router import router as qr_auth_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(project_router)
api_router.include_router(profile_router)
api_router.include_router(tech_stack_router)
api_router.include_router(stats_router)
api_router.include_router(social_media_router)
api_router.include_router(skill_categories_router)
api_router.include_router(qr_auth_router)
