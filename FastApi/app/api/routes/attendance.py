from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.jwt_config import get_current_user

from app.services.attendanceService import get_days

router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.get("/")
async def get_attendance_days(
    timetable_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await get_days(timetable_id, db, current_user)

