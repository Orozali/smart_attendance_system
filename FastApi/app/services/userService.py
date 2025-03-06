import base64
from datetime import timedelta
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from jose import JWTError
from app.core import jwt_config

from app.models.user import User
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.lessons import Lesson

from app.core.security import verify_password, hash_password
from app.core.insightface import process_images

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


import logging

logging.basicConfig(level=logging.DEBUG)  # You can use DEBUG, INFO, WARNING, ERROR, CRITICAL
logger = logging.getLogger(__name__)


async def saveStudent(background_tasks, db: AsyncSession, files, name, surname, email, password, student_id):
    logger.debug("Starting saveStudent function")
    db_user_email_result = await db.execute(select(Student).where(Student.email == email))
    db_user_email = db_user_email_result.scalar_one_or_none()
    db_user_student_id_result = await db.execute(select(Student).where(Student.student_id == student_id))
    db_user_student_id = db_user_student_id_result.scalar_one_or_none()
    if db_user_email:  
        logger.error(f"User already registered: {email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    elif db_user_student_id:
        logger.error(f"User already registered: {student_id}")
        raise HTTPException(status_code=400, detail="Student ID already registered")
    
    new_user = User(username = student_id, password=hash_password(password), role = "STUDENT")
    new_student = Student(name = name, surname = surname, email = email, student_id = student_id, user = new_user)
    db.add(new_user)
    db.add(new_student)
    await db.commit()
    await db.refresh(new_user)
    await db.refresh(new_student)

    file_contents = []
    for file in files:
        contents = await file.read()  # Read the file content
        file_contents.append(contents)
     # Send response immediately
    response = {"message": "Registration is successful!", "status": 200}

    background_tasks.add_task(process_images, file_contents, student_id)
    logger.debug(f"Student {student_id} registered successfully")
    return JSONResponse(status_code=200, content=response)



async def login(db: AsyncSession, request):
    db_result = await db.execute(select(User).where(User.username == request.username))
    db_user = db_result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password!")
    check = verify_password(request.password, db_user.password)
    if not check:
        raise HTTPException(status_code=400, detail="Incorrect username or password!")
    access_token = jwt_config.create_access_token(data={"sub": str(db_user.id)})
    refresh_token = jwt_config.create_refresh_token(data={"sub": str(db_user.id)})
    role = db_user.role

    return {"access_token": access_token, "refresh_token": refresh_token, "role": role}


async def refreshToken(refresh_token):
    try:
        payload = jwt_config.jwt.decode(refresh_token.refresh_token, jwt_config.SECRET_KEY, algorithms=[jwt_config.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        
        access_token_expires = timedelta(minutes=jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = jwt_config.create_access_token(data={"sub": str(user_id)}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")



async def profile(db: AsyncSession, current_user: User):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    image_data = None
    if current_user.role == "STUDENT":
        result = await db.execute(
            select(Student).where(Student.user_id == current_user.id))
        student = result.scalars().first()
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
        
        if student.image:
            image_data = "data:image/png;base64," + student.image
        else:
            image_data = None
        return {
            "id": student.id,
            "name": student.name,
            "surname": student.surname,
            "email": student.email,
            "student_id": student.student_id,
            "image": image_data
        }

    elif current_user.role == "TEACHER":
        result = await db.execute(
            select(Teacher).where(Teacher.user_id == current_user.id))
        teacher = result.scalars().first()
        if not teacher:
            return {"error": "Teacher profile not found"}
        if teacher.image:
            image_data = "data:image/png;base64," + teacher.image
        else:
            image_data = None
        return {
            "id": teacher.id,
            "name": teacher.name,
            "surname": teacher.surname,
            "email": teacher.email,
            "image": image_data
        }

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")



async def save_avatar(file, db: AsyncSession, current_user: User):
    file_bytes = await file.read()  # Read file as bytes
    encoded_image = base64.b64encode(file_bytes).decode('utf-8')

    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if current_user.role == "STUDENT":
        db_student = await db.execute(
            select(Student).where(Student.user_id == current_user.id)
        )
        db_student = db_student.scalar_one()
        if not db_student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        db_student.image = encoded_image
        await db.commit()
        await db.refresh(db_student)

    elif current_user.role == "TEACHER":
        db_teacher = await db.execute(
            select(Teacher).where(Teacher.user_id == current_user.id)
        )
        db_teacher = db_teacher.scalar_one()
        if not db_teacher:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
        db_teacher.image = encoded_image
        await db.commit()
        await db.refresh(db_teacher)

    return {"message": "Image successfully saved!", "status": 200}