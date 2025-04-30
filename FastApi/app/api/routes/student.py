from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

from app.core.jwt_config import get_current_user
from app.services.studentService import choose_lesson, get_my_lessons, getAllStudents

router = APIRouter(prefix="/student", tags=["Students"])


@router.get("/all")
async def getAll(db: AsyncSession = Depends(get_db)):
    return await getAllStudents(db)

@router.get("/my-lessons")
async def getLessons(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await get_my_lessons(db, current_user)


@router.post("/choose-lesson")
async def chooseLesson(lessonsId: List[int], db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await choose_lesson(lessonsId, current_user, db)
