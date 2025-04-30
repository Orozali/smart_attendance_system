from sqlalchemy import Boolean, Column, ForeignKey, Integer, Double, Date
from app.core.database import Base
from sqlalchemy.orm import relationship

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, autoincrement=True)
    percentage = Column(Double)
    date = Column(Date)
    attended = Column(Boolean, default=False)

    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    student = relationship("Student", back_populates="attendance")

    timetable_id = Column(Integer, ForeignKey("timetable.id", ondelete="CASCADE"), nullable=False)
    timetable = relationship("Timetable")