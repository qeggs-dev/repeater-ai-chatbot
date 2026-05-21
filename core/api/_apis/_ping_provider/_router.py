from fastapi import APIRouter

ping_provider_router = APIRouter(prefix="/ping_provider", tags=["ping_provider"])