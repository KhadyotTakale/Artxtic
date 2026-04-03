"""V1 API router — includes all endpoint groups."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, generation, library, profile, subscription

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(generation.router)
router.include_router(library.router)
router.include_router(profile.router)
router.include_router(subscription.router)
