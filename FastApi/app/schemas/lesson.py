from typing import List
from pydantic import BaseModel

class CreateLesson(BaseModel):
    name: str
    code: str

class AddLesson2Teacher(BaseModel):
    lessonsId: List[int]