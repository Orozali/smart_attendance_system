from fastapi import HTTPException
from fastapi.responses import JSONResponse
import logging

from app.models import user
from app.models import student
from app.models import teacher
from app.models import lessons
from app.models import timetable

from app.core.security import hash_password, verify_password

logging.basicConfig(level=logging.DEBUG)  # You can use DEBUG, INFO, WARNING, ERROR, CRITICAL
logger = logging.getLogger(__name__)


def check_current_user(current_user):
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Only admins can access this")
    return current_user


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
    return db.query(teacher.Teacher).all()


async def getTeacherById(id, db):
    db_teacher = db.query(teacher.Teacher).filter(teacher.Teacher.id == id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher


async def getAllLessons(db):
    db_lessons = db.query(lessons.Lesson).all()
    return db_lessons


async def saveLesson2Teacher(id, request, db):
    db_teacher = db.query(teacher.Teacher).filter(teacher.Teacher.id == id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    db_lessons = db.query(lessons.Lesson).filter(lessons.Lesson.id.in_(request.lessonsId)).all()
    if not db_lessons:
        raise HTTPException(status_code=404, detail="No valid lessons found")
    
    for lesson in db_lessons:
        lesson.teacher_id = db_teacher.id
        db.add(lesson)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    response = {"message": "Lessons assigned successfully!", "status": 200}
    return JSONResponse(status_code=200, content=response)


async def get_lessons_of_teacher(teacher_id, db, current_user):
    check_current_user(current_user=current_user)
    db_lessons = db.query(lessons.Lesson).filter(lessons.Lesson.teacher_id == teacher_id).all()
    return db_lessons
