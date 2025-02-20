from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import traceback
import logging

from app.api.routes import users
from app.api.routes import admin
from app.api.routes import student
from app.api.routes import teacher

from app.core.database import  engine
from app.admin import register_admin

app = FastAPI(title="FastAPI PostgreSQL Example")
admin_panel = register_admin(app, engine)

app.include_router(users.router)
app.include_router(admin.router)
app.include_router(student.router)
app.include_router(teacher.router)



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
    logging.error(f"Error occurred: {str(exc)}")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "details": str(exc)}
    )
