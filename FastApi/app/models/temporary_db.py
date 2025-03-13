from sqlalchemy import Column, ForeignKey, Integer, String, Time
from app.core.database import Base
from sqlalchemy.orm import relationship

class TemporaryAttendance(Base):
    __tablename__ = "temporary_attendance"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_number = Column(String, nullable=True)
    entry_time = Column(Time, nullable=True)
    timetable_id = Column(Integer, ForeignKey("timetable.id"), nullable=True)

    timetable = relationship("Timetable", back_populates="temporary_attendances")
