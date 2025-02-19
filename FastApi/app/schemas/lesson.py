from pydantic import BaseModel

class CreateLesson(BaseModel):
    name: str
    code: str