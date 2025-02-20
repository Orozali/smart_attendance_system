from fastapi import HTTPException
from app.models import teacher
from app.models import lessons


async def check_current_user(db, current_user):
    if current_user.role != "TEACHER":
        raise HTTPException(status_code=403, detail="Only teachers can access this")
    db_user =  db.query(teacher.Teacher).filter(teacher.Teacher.user_id == current_user.id).first()
    if not db_user:
        raise HTTPException(status_code=403, detail="Teacher with this user_id not found")
    return db_user


async def get_all_lessons_by_teacher_id(current_user, db):
    db_teacher = await check_current_user(db, current_user)
    return db_teacher.lessons


async def get_lesson_by_id(id, db, current_user):
    db_teacher = check_current_user(db, current_user)
    db_lesson = db.query(lessons.Lesson).filter(lessons.Lesson.id == id).first()
    return db_lesson.students
    