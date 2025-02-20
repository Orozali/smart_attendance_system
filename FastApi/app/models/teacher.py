from sqlalchemy import Column, ForeignKey, Integer, String
from app.core.database import Base
from sqlalchemy.orm import relationship

class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    lessons = relationship("Lesson", back_populates="teacher", cascade="all, delete-orphan")
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)  # Ensure user_id is unique
    user = relationship("User", back_populates="teacher", uselist=False)  # uselist=False ensures one-to-one