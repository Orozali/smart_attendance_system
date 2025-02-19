from sqlalchemy import Column, ForeignKey, Integer, String
from app.core.database import Base
from sqlalchemy.orm import relationship
from app.models.student_lesson import student_lesson_association


class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    student_id = Column(String, unique=True, index=True)

    # Many-to-Many relationship with Lesson
    lessons = relationship("Lesson", secondary=student_lesson_association, back_populates="students")

    # Foreign key to User (One-to-One relation)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)  # Ensure user_id is unique

    # One-to-One relationship with User
    user = relationship("User", back_populates="student", uselist=False)  # uselist=False ensures one-to-one