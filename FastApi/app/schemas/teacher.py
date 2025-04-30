from typing import List
from pydantic import BaseModel
from datetime import date

class CreateTeacher(BaseModel):
    name: str
    surname: str
    email: str
    password: str

class AttendancePayload(BaseModel):
    student_ids: List[int]
    manually_checked_ids: List[int]
    timetable_id: int
    day: date