from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status, BackgroundTasks
from app.schemas import user as schemas
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.userService import login, saveStudent, refreshToken, profile, save_avatar
from app.core.jwt_config import get_current_user

router = APIRouter(prefix="/auth", tags=["Users"])

@router.post("/register", response_model=schemas.UserResponse)
async def upload_embeddings(background_tasks: BackgroundTasks,
                            name: str = Form(...),
                            surname: str = Form(...),
                            email: str = Form(...),
                            password: str = Form(...),
                            student_id: str = Form(...),
                            files: list[UploadFile] = File(...),
                            db: AsyncSession = Depends(get_db)):
    try:
        return await saveStudent(background_tasks,db, files, name, surname, email, password, student_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
   
@router.post("/login", response_model=schemas.LoginResponse)
async def get_user(request: schemas.Login, db: AsyncSession = Depends(get_db)):
    try:
        return await login(db, request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/refresh-token", response_model=schemas.Token)
async def refresh_access_token(refresh_token: schemas.TokenRefresh):
    return await refreshToken(refresh_token)


@router.get("/profile")
async def get_profile(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await profile(db, current_user)


@router.post("/add-avatar")
async def saveAvatar(file: UploadFile = File(...), db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await save_avatar(file, db, current_user)
