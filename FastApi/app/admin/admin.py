import os
from app.models.user import User
from app.models.teacher import Teacher
from app.models.student import Student
from app.models.timetable import Timetable
from app.models.lessons import Lesson

from app.core.database import async_session_maker
from app.core.security import hash_password

from sqladmin import Admin, ModelView
from sqlalchemy.future import select

from app.admin.forms import TeacherForm
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

    return admin