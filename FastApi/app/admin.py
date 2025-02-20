from fastadmin import SqlAlchemyModelAdmin
from sqladmin import Admin, ModelView
from app.models.user import User
from app.models.teacher import Teacher
from app.models.student import Student
from app.models.timetable import Timetable
from app.models.lessons import Lesson


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.role]

class StudentAdmin(ModelView, model=Student):
    column_list = [Student.id, Student.name, Student.surname, Student.email, Student.student_id]

class TeacherAdmin(ModelView, model=Teacher):
    column_list = [Teacher.id, Teacher.name, Teacher.surname, Teacher.email]

class LessonAdmin(ModelView, model=Lesson):
    column_list = [Lesson.id, Lesson.code, Lesson.name]

class TimeTableAdmin(ModelView, model=Timetable):
    column_list = [Timetable.id, Timetable.day, Timetable.start_time, Timetable.end_time]

def register_admin(app, engine):
    admin = Admin(app, engine)
    
    # Registering the models
    admin.add_view(UserAdmin)
    admin.add_view(StudentAdmin)
    admin.add_view(TeacherAdmin)
    admin.add_view(LessonAdmin)
    admin.add_view(TimeTableAdmin)

    return admin