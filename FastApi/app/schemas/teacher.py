from pydantic import BaseModel

class CreateTeacher(BaseModel):
    name: str
    surname: str
    email: str
    password: str