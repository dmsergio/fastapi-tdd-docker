from fastapi import APIRouter
from fastapi import Depends

from app.config import get_settings
from app.config import Settings


router = APIRouter()


@router.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong",
        "environment": settings.environment,
        "testing": settings.testing,
    }
