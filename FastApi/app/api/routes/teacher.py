from typing import Optional
from fastapi import APIRouter, Depends, Query
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.teacher import AttendancePayload
from app.core.database import get_db
from app.core.jwt_config import get_current_user
from app.services.teacherService import get_all_lessons_by_teacher_id, get_lesson_by_id, get_main, get_students_of_teacher, get_students_from_temp_db, save_attendance, get_lesson_today

router = APIRouter(prefix="/teacher", tags=['Teacher'])


@router.get("/main-info")
async def mainInfo(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await get_main(db, current_user)

@router.get("/get-lessons")
async def getLessonsByTeacherId(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await get_all_lessons_by_teacher_id(current_user, db)

@router.get("/get-lesson/{id}")
async def getLessonById(id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await get_lesson_by_id(id, db, current_user)

@router.get("/get-students/{lessonId}")
async def getStudentsOfTeacher(lessonId: int, db: AsyncSession = Depends(get_db),  current_user = Depends(get_current_user)):
    return await get_students_of_teacher(lessonId, db, current_user)

@router.get("/get-students-from-temporary-db/{lessonId}")
async def getStudentsFromTempDb(lessonId: int, day: Optional[date] = Query(None), db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await get_students_from_temp_db(lessonId, day, db, current_user)

@router.post("/attendance/save")
async def save_attendance_route(
    data: AttendancePayload,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await save_attendance(data.student_ids, data.timetable_id, data.manually_checked_ids, data.day, db, current_user)

@router.get("/lesson-today/{lessonId}")
async def lesson_today(
    lessonId: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await get_lesson_today(lessonId, db, current_user)
   