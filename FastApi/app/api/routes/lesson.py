from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

from app.core.jwt_config import get_current_user
from app.services.lessonService import get_all_lesson

router = APIRouter(prefix="/lesson", tags=["Lessons"])


@router.get("/all")
async def getAll(db: AsyncSession = Depends(get_db)):
    return await get_all_lesson(db)

