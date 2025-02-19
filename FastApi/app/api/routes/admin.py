from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.adminService import saveTeacher, saveLesson, getAllTeachers, getTeacherById, getAllLessons
from app.schemas import teacher, lesson, user

router = APIRouter(prefix='/admin', tags=["Admin"])


@router.get("/get-all-teachers")
async def getTeachers(db: Session = Depends(get_db)):
    try:
        return await getAllTeachers(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    
@router.get("/get-teacher/{id}")
async def getById(id: int, db: Session = Depends(get_db)):
    return await getTeacherById(id, db)
    

@router.post("/add-teacher", response_model=user.MessageResponse)
async def addTeacher(request: teacher.CreateTeacher, db: Session = Depends(get_db)):
    try:
        return await saveTeacher(request, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/add-lesson", response_model=user.MessageResponse)
async def addLesson(request: lesson.CreateLesson, db: Session = Depends(get_db)):
    try:
        return await saveLesson(request, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@router.get("/get-all-lessons")
async def getLessons(db: Session = Depends(get_db)):
    return await getAllLessons(db)


@router.post("/add-lesson2teacher")
async def addLesson2Teacher():
    pass