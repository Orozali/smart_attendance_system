from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import and_, func
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.lessons import Lesson
from app.models.user import User
from app.models.timetable import Timetable
from app.models.timetable_times import Timetable_times
from app.models.attendance import Attendance
from app.models.temporary_db import TemporaryAttendance
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sqlalchemy.orm import joinedload, selectinload

async def get_days(timetable_id: int, db: AsyncSession, current_user: User):
    if current_user.role != "TEACHER":
        raise HTTPException(status_code=403, detail="Only teachers can access this")

    db_timetable = await db.execute(
        select(Timetable)
        .where(Timetable.id == timetable_id)
    )
    db_timetable = db_timetable.scalar_one_or_none()
    if not db_timetable:
        raise HTTPException(status_code=404, detail="Timetable not found!")
    db_attendance = await db.execute(
        select(Attendance)
        .where(Attendance.timetable_id == timetable_id)
        .order_by(Attendance.date.desc())
    )
    db_attendance = db_attendance.scalars().all()
    if not db_attendance:
        return []

    unique_dates = sorted({attendance.date for attendance in db_attendance})
    return unique_dates