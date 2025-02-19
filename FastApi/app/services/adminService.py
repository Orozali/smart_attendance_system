from datetime import timedelta
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from jose import JWTError
import logging

from app.models import user
from app.models import student
from app.models import teacher
from app.models import lessons

from app.core.security import hash_password, verify_password

logging.basicConfig(level=logging.DEBUG)  # You can use DEBUG, INFO, WARNING, ERROR, CRITICAL
logger = logging.getLogger(__name__)

async def saveTeacher(request, db):
    db_teacher = db.query(teacher.Teacher).filter(teacher.Teacher.email == request.email).first()
    if db_teacher:
        logger.error(f"User already registered: {request.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = user.User(username = request.email, password = hash_password(request.password), role = "TEACHER")
    new_teacher = teacher.Teacher(name = request.name, surname = request.surname, email = request.email, user = new_user)
    db.add(new_user)
    db.add(new_teacher)
    db.commit()
    db.refresh(new_user)
    db.refresh(new_teacher)

    response = {"message": "A new teacher successfully saved!", "status": 200}
    logger.debug(f"Teacher with the name {request.name} successfully registered!")
    return JSONResponse(status_code=200, content=response)


async def saveLesson(request, db):
    new_lesson = lessons.Lesson(name = request.name, code = request.code)
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    response = {"message": "A new lesson successfully saved!", "status": 200}
    return JSONResponse(status_code=200, content=response)


async def getAllTeachers(db):
    teachers = db.query(teacher.Teacher).all()
    return teachers


async def getTeacherById(id, db):
    db_teacher = db.query(teacher.Teacher).filter(teacher.Teacher.id == id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher


async def getAllLessons(db):
    db_lessons = db.query(lessons.Lesson).all()
    return db_lessons
