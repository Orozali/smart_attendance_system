from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.jwt_config import get_current_user
from app.services.teacherService import get_all_lessons_by_teacher_id, get_lesson_by_id

router = APIRouter(prefix="/teacher", tags=['Teacher'])

@router.get("/get-lessons")
async def getLessonsByTeacherId(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return await get_all_lessons_by_teacher_id(current_user, db)

@router.get("/get-lesson/{id}")
async def getLessonById(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return await get_lesson_by_id(id, db, current_user)