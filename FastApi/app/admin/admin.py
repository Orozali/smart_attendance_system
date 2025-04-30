from datetime import datetime, timedelta
import os

from sqlalchemy import case, delete
from app.models.timetable_times import Timetable_times
from app.models.user import User
from app.models.teacher import Teacher
from app.models.student import Student
from app.models.timetable import Timetable
from app.models.lessons import Lesson
from app.models.attendance import Attendance
from app.models.temporary_db import TemporaryAttendance
from sqlalchemy.orm import joinedload

from app.core.database import async_session_maker
from app.core.security import hash_password

from sqladmin import Admin, ModelView
from sqlalchemy.future import select

from app.admin.forms import TeacherForm
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logging.basicConfig(level=logging.DEBUG)  # You can use DEBUG, INFO, WARNING, ERROR, CRITICAL
logger = logging.getLogger(__name__)


class UserAdmin(ModelView, model=User):
    icon = "fa-solid fa-user"
    column_list = [User.id, User.username, User.role]

class StudentAdmin(ModelView, model=Student):
    icon = "fa-solid fa-graduation-cap"
    column_list = [Student.id, Student.name, Student.surname, Student.email, Student.student_id]
    column_details_list = [Student.name, Student.surname, Student.email, Student.student_id, Student.lessons]
    form_excluded_columns = [Student.user]

class TeacherAdmin(ModelView, model=Teacher):
    icon = "fa-solid fa-user-tie"
    column_list = [Teacher.id, Teacher.name, Teacher.surname, Teacher.email]
    form = TeacherForm
  
    column_details_list = [Teacher.name, Teacher.surname, Teacher.email, Teacher.lessons]

    async def on_model_change(self, data, model, is_created, request):
        async with async_session_maker() as session:
            if is_created:
                password = data.get("password")

                if password:
                    user = User(
                        username=data.get("email"),
                        password=hash_password(password),  # Hash password
                        role="TEACHER",
                    )

                    # Check if user already exists
                    result = await session.execute(select(User).where(User.username == user.username))
                    existing_user = result.scalar_one_or_none()

                    if not existing_user:
                        session.add(user)
                        await session.commit()
                        await session.refresh(user)

                    model.user = user
                    model.user_id = user.id
                    await session.commit()
            else:
                logger.debug("Teacher is editing")
                # Editing an existing Teacher
                result = await session.execute(select(User).where(User.id == model.user_id))
                user = result.scalar_one_or_none()
                logger.debug("Get user")
                if user:
                    # Update email if changed
                    logger.debug("update user")
                    new_email = data.get("email")
                    if new_email and user.username != new_email:
                        user.username = new_email

                    if "password" in data and data["password"]:
                        new_password = data["password"]
                        user.password = hash_password(new_password)  # Hash the new password if provided
                    else:
                        # Remove password from data if it's not being updated (this prevents password reset)
                        data.pop("password", None)

                    await session.commit()

        await super().on_model_change(data, model, is_created, request)

class LessonAdmin(ModelView, model=Lesson):
    icon = "fa-solid fa-book"
    column_list = [Lesson.id, Lesson.code, Lesson.name, Lesson.teacher]
    form_excluded_columns = [Lesson.timetables, Lesson.students]
    column_details_exclude_list = [Lesson.id, Lesson.teacher_id]


class TimeTableAdmin(ModelView, model=Timetable):
    icon = "fa-solid fa-calendar"
    column_list = [Timetable.id, Timetable.lesson, Timetable.day, Timetable.start_time, Timetable.end_time]
    column_details_exclude_list = [Timetable.id, Timetable.lesson_id]
    form_excluded_columns = [Timetable.timetable_times, Timetable.temporary_attendances]
    async def on_model_change(self, data, model, is_created, request):
        if is_created:
            async with async_session_maker() as session:
                times = await self.create_timetable_times(session, data)
                model.timetable_times = times
        await super().on_model_change(data, model, is_created, request)

    async def create_timetable_times(self, session: AsyncSession, timetable):
        lesson_duration = timedelta(minutes=45)
        break_duration = timedelta(minutes=10)

        current_start = datetime.combine(datetime.today(), timetable.get("start_time"))
        timetable_end = datetime.combine(datetime.today(), timetable.get("end_time"))

        times = []
        while current_start + lesson_duration <= timetable_end:
            current_end = current_start + lesson_duration

            timeslot = Timetable_times(
                start_time=current_start.time(),
                end_time=current_end.time(),
                timetable_id=timetable.get("id")
            )
            times.append(timeslot)

            logger.debug(f"Added timeslot: {timeslot.start_time} - {timeslot.end_time}")

            current_start = current_end + break_duration

        session.add_all(times)
        await session.commit()

        return times
    async def clear_and_create_timetable_times(self, session, timetable):
        """Clears existing timetable_times and recreates them."""
        await session.execute(
            delete(Timetable_times).where(Timetable_times.timetable_id == timetable.id)
        )
        await session.commit()
        await self.create_timetable_times(session, timetable)

class Timetable_timesAdmin(ModelView, model=Timetable_times):
    icon = "fa-solid fa-user-tie"
    column_list = [Timetable_times.id, Timetable_times.timetable_id, Timetable_times.start_time, Timetable_times.end_time]


class Attendance_Admin(ModelView, model=Attendance):
    column_list = [Attendance.id, Attendance.student, Attendance.percentage,Attendance.date, Attendance.timetable_id]

class TemporaryDbAdmin(ModelView, model=TemporaryAttendance):
    column_list = [TemporaryAttendance.id, TemporaryAttendance.student, TemporaryAttendance.entry_time, Attendance.timetable]

def register_admin(app, engine, authentication_backend):
    templates_path = os.path.join(os.path.dirname(__file__), 'templates')
    admin = Admin(app=app, 
                  engine=engine, 
                  authentication_backend=authentication_backend,
                  title="Smart Attendance Admin",
                  templates_dir=templates_path
                  )

    
    # Registering the models
    admin.add_view(UserAdmin)
    admin.add_view(StudentAdmin)
    admin.add_view(TeacherAdmin)
    admin.add_view(LessonAdmin)
    admin.add_view(TimeTableAdmin)
    admin.add_view(Timetable_timesAdmin)
    admin.add_view(Attendance_Admin)
    admin.add_view(TemporaryDbAdmin)

    return admin