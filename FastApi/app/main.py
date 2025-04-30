from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse
import traceback

from app.api.routes import users
from app.api.routes import admin
from app.api.routes import student
from app.api.routes import teacher
from app.api.routes import lesson
from app.api.routes import attendance

from app.core.database import  engine
from app.admin.admin_auth import authentication_backend
from app.admin.admin import register_admin

app = FastAPI(title="FastAPI PostgreSQL Example")


admin_panel = register_admin(app, engine, authentication_backend)
app.mount("/static", StaticFiles(directory="app/admin/static"), name="static")

app.include_router(users.router)
app.include_router(admin.router)
app.include_router(student.router)
app.include_router(teacher.router)
app.include_router(lesson.router)
app.include_router(attendance.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["*"]
)

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "details": str(exc)}
    )