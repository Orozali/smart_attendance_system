from sqlalchemy import Column, ForeignKey, Integer, String
from app.core.database import Base
from sqlalchemy.orm import relationship

class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, unique=True, index=True)

     # One-to-Many relationship (Teacher → Lessons)
    lessons = relationship("Lesson", back_populates="teacher", cascade="all, delete-orphan")

    # Foreign key to User (One-to-One relation)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)  # Ensure user_id is unique

    # One-to-One relationship with User
    user = relationship("User", back_populates="teacher", uselist=False)  # uselist=False ensures one-to-one