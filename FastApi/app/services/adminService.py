from fastapi import HTTPException
from fastapi.responses import JSONResponse
import logging

from sqlalchemy.future import select

from app.models.user import User
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.lessons import Lesson
from app.models.timetable import Timetable
from app.models.timetable_times import Timetable_times

from sqlalchemy.ext.asyncio import AsyncSession


from app.core.security import hash_password, verify_password

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def check_current_user(current_user):
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Only admins can access this")
    return current_user


async def saveTeacher(request, db: AsyncSession):
    result = await db.execute(
        select(Teacher).where(Teacher.email == request.email)
    )
    db_teacher = result.scalar_one_or_none()
    if db_teacher:
        logger.error(f"User already registered: {request.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(username = request.email, password = hash_password(request.password), role = "TEACHER")
    new_teacher = Teacher(name = request.name, surname = request.surname, email = request.email, user = new_user)
    db.add(new_user)
    db.add(new_teacher)
    await db.commit()
    await db.refresh(new_user)
    await db.refresh(new_teacher)

    response = {"message": "A new teacher successfully saved!", "status": 200}
    logger.debug(f"Teacher with the name {request.name} successfully registered!")
    return JSONResponse(status_code=200, content=response)


async def saveLesson(request, db: AsyncSession):
    new_lesson = Lesson(name = request.name, code = request.code)
    db.add(new_lesson)
    await db.commit()
    await db.refresh(new_lesson)
    response = {"message": "A new lesson successfully saved!", "status": 200}
    return JSONResponse(status_code=200, content=response)


async def getAllTeachers(db: AsyncSession):
    result = await db.execute(select(Teacher))
    return result.scalars().all()


async def getTeacherById(id, db: AsyncSession):
    result = await db.execute(
        select(Teacher).where(Teacher.id == id)
        )
    db_teacher = result.scalar_one_or_none()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher


async def getAllLessons(db:AsyncSession):
    db_lessons = await db.execute(select(Lesson))
    return db_lessons.scalars().all()


async def saveLesson2Teacher(id, request, db: AsyncSession):
    result = await db.execute(
        select(Teacher).where(Teacher.id == id))
    db_teacher = result.scalar_one_or_none()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    result_lesson = await db.execute(
        select(Lesson).where(Lesson.id.in_(request.lessonsId)))
    db_lessons = result_lesson.scalars().all()
    if not db_lessons:
        raise HTTPException(status_code=404, detail="No valid lessons found")
    
    for lesson in db_lessons:
        lesson.teacher_id = db_teacher.id
        db.add(lesson)

    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    response = {"message": "Lessons assigned successfully!", "status": 200}
    return JSONResponse(status_code=200, content=response)


async def get_lessons_of_teacher(teacher_id: int, db: AsyncSession, current_user):
    check_current_user(current_user=current_user)
    db_result = await db.execute(select(Lesson).where(Lesson.teacher_id == teacher_id))
    return db_result.scalars().all()
