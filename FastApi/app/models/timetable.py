from sqlalchemy import Column, Integer, ForeignKey, Time, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Timetable(Base):
    __tablename__ = "timetable"
    id = Column(Integer, primary_key=True, autoincrement=True)
    lesson_id = Column(Integer, ForeignKey("lesson.id"), nullable=False)
    day = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    lesson = relationship("Lesson", back_populates="timetables")
