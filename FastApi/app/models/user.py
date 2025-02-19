from sqlalchemy import Column, Integer, String
from app.core.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    role = Column(String)

    # One-to-One relationship with Student
    student = relationship("Student", back_populates="user", uselist=False)  # uselist=False ensures one-to-one
    
    # One-to-One relationship with Teacher
    teacher = relationship("Teacher", back_populates="user", uselist=False)
