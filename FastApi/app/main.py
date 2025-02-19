from fastapi import FastAPI, Request
from app.core.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
import logging
from starlette.responses import JSONResponse
import traceback

from app.api.routes import users
from app.api.routes import admin

from app.core.database import Base, engine

app = FastAPI(title="FastAPI PostgreSQL Example")

Base.metadata.create_all(bind=engine)

# Define allowed origins (Frontend URL)
origins = [
    "http://localhost:5173",  # Your Next.js frontend
    "http://127.0.0.1:5173",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(users.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI with PostgreSQL"}

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logging.error(f"Error occurred: {str(exc)}")
    traceback.print_exc()  # Print full error traceback
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "details": str(exc)}
    )
