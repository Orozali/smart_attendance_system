from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.models import user
from app.models import student
from app.models import teacher
from app.models import lessons

async def check_current_user(db, current_user):
    if current_user.role != "STUDENT":
        raise HTTPException(status_code=403, detail="Only students can access this")
    db_student =  db.query(student.Student).filter(student.Student.user_id == current_user.id).first()
    if not db_student:
        raise HTTPException(status_code=403, detail="Student with this user_id not found")
    return db_student

async def getAllStudents(db):
    return db.query(student.Student).all()

async def choose_lesson(lessonsId, current_user, db):
    db_student = await check_current_user(db, current_user)
    print(db_student)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    db_lessons = db.query(lessons.Lesson).filter(lessons.Lesson.id.in_(lessonsId)).all()
    if not db_lessons:
        raise HTTPException(status_code=404, detail="No valid lessons found")
    db_student.lessons.extend(db_lessons)
    db.commit()
    response = {"message": "Lessons successfully saved!", "status": 200}
    return JSONResponse(status_code=200, content=response)
