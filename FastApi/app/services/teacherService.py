from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import func
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.lessons import Lesson
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.student_lesson import student_lesson_association


def check_current_user(current_user):
    if current_user.role != "TEACHER":
        raise HTTPException(status_code=403, detail="Only teachers can access this")
    return current_user


async def get_all_lessons_by_teacher_id(current_user, db:AsyncSession):
    db_user = check_current_user(current_user)
    db_teacher = await db.execute(
        select(Teacher)
        .options(selectinload(Teacher.lessons))
        .where(Teacher.user_id == db_user.id))
    db_teacher = db_teacher.scalar_one()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found!")
    return db_teacher.lessons


async def get_lesson_by_id(id, db: AsyncSession, current_user):
    check_current_user(current_user)
    db_lesson = await db.execute(select(Lesson).options(selectinload(Lesson.students)).where(Lesson.id == id))
    db_lesson = db_lesson.scalar_one()
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found!")
    countOfStudent = len(db_lesson.students)
    return {
        "code": db_lesson.code,
        "name": db_lesson.name,
        "countOfStudent": countOfStudent
    }
    

async def get_main(db: AsyncSession, current_user: User):
    check_current_user(current_user)
    db_teacher = await db.execute(
        select(Teacher).options(selectinload(Teacher.lessons)).where(Teacher.user_id == current_user.id)
    )

    db_teacher = db_teacher.scalar_one()
    if not db_teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found!")
    
    lesson_count = len(db_teacher.lessons)

    student_count_result = await db.execute(
        select(func.count(func.distinct(Student.id)))
        .join(student_lesson_association, student_lesson_association.c.student_id == Student.id)
        .join(Lesson, student_lesson_association.c.lesson_id == Lesson.id)
        .where(Lesson.teacher_id == db_teacher.id)
    )
    student_count = student_count_result.scalar()

    return JSONResponse(
        status_code=200,
        content={
            "teacher_name": f"{db_teacher.name} {db_teacher.surname}",
            'teacher_id': db_teacher.id,
            "lessonCount": lesson_count,
            "studentCount": student_count,
            "departmentCount": 1
        }
    )

async def get_students_of_teacher(lessonId: int, db: AsyncSession, current_user: User):
    db_user = check_current_user(current_user)
    db_teacher = await db.execute(select(Teacher).where(Teacher.user_id == db_user.id))
    db_teacher = db_teacher.scalar_one()
    if not db_teacher:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Teacher not found!")
    
    result = await db.execute(
        select(Student)
        .join(Student.lessons)
        .where(Lesson.id == lessonId, Lesson.teacher_id == db_teacher.id)
        .distinct()
    )

    students = result.scalars().unique().all()
    return students