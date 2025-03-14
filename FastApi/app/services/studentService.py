from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.lessons import Lesson
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
import logging

logging.basicConfig(level=logging.DEBUG)  # You can use DEBUG, INFO, WARNING, ERROR, CRITICAL
logger = logging.getLogger(__name__)


def check_current_user(current_user):
    if current_user.role != "STUDENT":
        raise HTTPException(status_code=403, detail="Only students can access this")
    return current_user


async def getAllStudents(db: AsyncSession):
    result = await db.execute(select(Student))
    return result.scalars().all()


from sqlalchemy.future import select
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from fastapi.responses import JSONResponse

async def choose_lesson(lessonsId, current_user, db: AsyncSession):
    db_user = check_current_user(current_user)

    db_student_result = await db.execute(
        select(Student)
        .options(selectinload(Student.lessons))
        .where(Student.user_id == db_user.id)
    )
    db_student = db_student_result.scalar_one_or_none()

    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db_lessons_result = await db.execute(select(Lesson).where(Lesson.id.in_(lessonsId)))
    db_lessons = db_lessons_result.scalars().all()

    if not db_lessons:
        raise HTTPException(status_code=404, detail="Please select at least one lesson!")

    existing_lesson_ids = {lesson.id for lesson in db_student.lessons}

    new_lessons = [lesson for lesson in db_lessons if lesson.id not in existing_lesson_ids]

    if new_lessons:
        db_student.lessons.extend(new_lessons)
        await db.commit()
        await db.refresh(db_student)

    response = {
        "message": "Lessons successfully saved!" if new_lessons else "You already have this lessons.",
        "status": 200
    }
    return JSONResponse(status_code=200, content=response)



async def get_my_lessons(db: AsyncSession, current_user: User):
    db_student = await db.execute(
        select(Student).options(
            selectinload(Student.lessons).selectinload(Lesson.teacher)
        ).where(Student.user_id == current_user.id)
    )
    db_student = db_student.scalar_one()
    if not db_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    return db_student.lessons

async def get_student_details(student_id, db: AsyncSession, bbox) -> Student:
    result = await db.execute(
        select(Student.id, Student.name, Student.surname, Student.student_id)
        .where(Student.student_id == student_id)
    )
    student = result.fetchone()

    if student:
        return {"id": student.id, "name": student.name, "surname": student.surname, "student_id": student.student_id, "bbox": bbox}
 
    return None