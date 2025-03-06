from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.jwt_config import get_current_user

from app.services.adminService import saveTeacher, saveLesson, getAllTeachers, getTeacherById, getAllLessons, saveLesson2Teacher, get_lessons_of_teacher
from app.schemas import teacher, lesson, user

router = APIRouter(prefix='/admin-main', tags=["Admin"])


@router.get("/get-all-teachers")
async def getTeachers(db: AsyncSession = Depends(get_db)):
    try:
        return await getAllTeachers(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@router.get("/get-teacher/{id}")
async def getById(id: int, db: AsyncSession = Depends(get_db)):
    return await getTeacherById(id, db)
    

@router.post("/add-teacher", response_model=user.MessageResponse)
async def addTeacher(request: teacher.CreateTeacher, db: AsyncSession = Depends(get_db)):
    try:
        return await saveTeacher(request, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/add-lesson", response_model=user.MessageResponse)
async def addLesson(request: lesson.CreateLesson, db: AsyncSession = Depends(get_db)):
    try:
        return await saveLesson(request, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@router.get("/get-all-lessons")
async def getLessons(db: AsyncSession = Depends(get_db)):
    return await getAllLessons(db)


@router.post("/add-lesson2teacher/{id}", response_model=user.MessageResponse)
async def addLesson2Teacher(id: int, request: lesson.AddLesson2Teacher, db: AsyncSession = Depends(get_db)):
    return await saveLesson2Teacher(id, request, db)


@router.get("/get-lessons-of-teacher/{teacher_id}")
async def getLessonsOfTeacher(teacher_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await get_lessons_of_teacher(teacher_id, db, current_user)