from datetime import timedelta
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from jose import JWTError

from app.core import jwt_config

from app.models import user
from app.models import student
from app.models import teacher
from app.models import lessons

from app.core.security import verify_password, hash_password
from app.core.insightface import process_images

import logging

logging.basicConfig(level=logging.DEBUG)  # You can use DEBUG, INFO, WARNING, ERROR, CRITICAL
logger = logging.getLogger(__name__)


async def saveStudent(background_tasks, db, files, name, surname, email, password, student_id):
    logger.debug("Starting saveStudent function")
    db_user_email = db.query(student.Student).filter(student.Student.email == email).first()
    db_user_student_id = db.query(student.Student).filter(student.Student.student_id == student_id).first()
    if db_user_email:  
        logger.error(f"User already registered: {email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    elif db_user_student_id:
        logger.error(f"User already registered: {student_id}")
        raise HTTPException(status_code=400, detail="Student ID already registered")
    
    new_user = user.User(username = student_id, password=hash_password(password), role = "STUDENT")
    new_student = student.Student(name = name, surname = surname, email = email, student_id = student_id, user = new_user)
    db.add(new_user)
    db.add(new_student)
    db.commit()
    db.refresh(new_user)
    db.refresh(new_student)

    file_contents = []
    for file in files:
        contents = await file.read()  # Read the file content
        file_contents.append(contents)
     # Send response immediately
    response = {"message": "Registration is successful!", "status": 200}

    background_tasks.add_task(process_images, file_contents, student_id)
    logger.debug(f"Student {student_id} registered successfully")
    return JSONResponse(status_code=200, content=response)



async def login(db, request):
    db_user = db.query(user.User).filter(user.User.username == request.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password!")
    check = verify_password(request.password, db_user.password)
    if not check:
        raise HTTPException(status_code=400, detail="Incorrect username or password!")
    access_token = jwt_config.create_access_token(data={"sub": str(db_user.id)})
    refresh_token = jwt_config.create_refresh_token(data={"sub": str(db_user.id)})


    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


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

