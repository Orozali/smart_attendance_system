from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse
import traceback

from app.api.routes import users
from app.api.routes import admin
from app.api.routes import student
from app.api.routes import teacher
from app.api.routes import lesson

from app.core.database import  engine
from app.admin.admin_auth import authentication_backend
from app.admin.admin import register_admin

from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuth2 as OAuth2Model


app = FastAPI(title="FastAPI PostgreSQL Example")

admin_panel = register_admin(app, engine, authentication_backend)
app.mount("/static", StaticFiles(directory="app/admin/static"), name="static")

app.include_router(users.router)
app.include_router(admin.router)
app.include_router(student.router)
app.include_router(teacher.router)
app.include_router(lesson.router)


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "details": str(exc)}
    )
