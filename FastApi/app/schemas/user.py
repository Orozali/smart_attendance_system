from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    student_id: str

class Login(BaseModel):
    student_id: str
    password: str

class UserResponse(BaseModel):
    id: int

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenRefresh(BaseModel):
    refresh_token: str

class MessageResponse(BaseModel):
    message: str
    status: int

    class Config:
        from_attributes = True
