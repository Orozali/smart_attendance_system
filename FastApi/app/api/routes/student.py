from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.studentService import getAllStudents

from app.core.jwt_config import get_current_user
from app.services.studentService import choose_lesson

router = APIRouter(prefix="/student", tags=["Students"])


@router.get("/all")
async def getAll(db: Session = Depends(get_db)):
    return await getAllStudents(db)


@router.post("/choose-lesson")
async def chooseLesson(lessonsId: List[int], current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await choose_lesson(lessonsId, current_user, db)