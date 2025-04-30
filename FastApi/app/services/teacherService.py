from datetime import date, datetime
from typing import List
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import and_, func
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.lessons import Lesson
from app.models.user import User
from app.models.timetable import Timetable
from app.models.timetable_times import Timetable_times
from app.models.attendance import Attendance
from app.models.temporary_db import TemporaryAttendance
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from app.models.student_lesson import student_lesson_association


def check_current_user(current_user):
    if current_user.role != "TEACHER":
        raise HTTPException(status_code=403, detail="Only teachers can access this")
    return current_user


async def get_all_lessons_by_teacher_id(current_user, db:AsyncSession):
    db_user = check_current_user(current_user)
    db_teacher = await db.execute(
        select(Teacher)
        .options(selectinload(Teacher.lessons))
        .where(Teacher.user_id == db_user.id))
    db_teacher = db_teacher.scalar_one()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found!")
    return db_teacher.lessons


async def get_lesson_by_id(id, db: AsyncSession, current_user):
    check_current_user(current_user)
    db_lesson = await db.execute(select(Lesson).options(selectinload(Lesson.students)).where(Lesson.id == id))
    db_lesson = db_lesson.scalar_one()
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found!")
    countOfStudent = len(db_lesson.students)
    return {
        "id": db_lesson.id,
        "code": db_lesson.code,
        "name": db_lesson.name,
        "countOfStudent": countOfStudent
    }
    

async def get_main(db: AsyncSession, current_user: User):
    check_current_user(current_user)
    db_teacher = await db.execute(
        select(Teacher).options(selectinload(Teacher.lessons)).where(Teacher.user_id == current_user.id)
    )

    db_teacher = db_teacher.scalar_one()
    if not db_teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found!")
    
    lesson_count = len(db_teacher.lessons)

    student_count_result = await db.execute(
        select(func.count(func.distinct(Student.id)))
        .join(student_lesson_association, student_lesson_association.c.student_id == Student.id)
        .join(Lesson, student_lesson_association.c.lesson_id == Lesson.id)
        .where(Lesson.teacher_id == db_teacher.id)
    )
    student_count = student_count_result.scalar()

    return JSONResponse(
        status_code=200,
        content={
            "teacher_name": f"{db_teacher.name} {db_teacher.surname}",
            'teacher_id': db_teacher.id,
            "lessonCount": lesson_count,
            "studentCount": student_count,
            "departmentCount": 1
        }
    )


async def get_students_of_teacher(lessonId: int, db: AsyncSession, current_user: User):
    db_user = check_current_user(current_user)
    db_teacher = await db.execute(select(Teacher).where(Teacher.user_id == db_user.id))
    db_teacher = db_teacher.scalar_one()
    if not db_teacher:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Teacher not found!")
    
    result = await db.execute(
        select(Student)
        .join(Student.lessons)
        .where(Lesson.id == lessonId, Lesson.teacher_id == db_teacher.id)
        .distinct()
    )

    students = result.scalars().unique().all()
    return students


async def get_students_from_temp_db(lessonId, day: date, db: AsyncSession, current_user):
    db_user = check_current_user(current_user)

    db_teacher = await db.execute(select(Teacher).where(Teacher.user_id == db_user.id))
    db_teacher = db_teacher.scalar_one()
    if not db_teacher:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Teacher not found!")

    filters = [Lesson.id == lessonId]
    if day:
        day_name = day.strftime("%A").upper()
        filters.append(Timetable.day == day_name)


    query = (
        select(Timetable)
        .join(Lesson)
        .filter(and_(*filters))
        .options(joinedload(Timetable.lesson).joinedload(Lesson.students).joinedload(Student.attendance))
    )
    result = await db.execute(query)
    timetables = result.unique().scalars().all()

    if not timetables:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No timetable found!")

    timetable = timetables[0]
    timetable_id = timetable.id
    all_students = timetable.lesson.students

    # Always get temporary attendance data for image + entry_time
    temporary_attendances = await students_in_temp_db(db, timetable_id)
    student_attendance_data = {
        temp_attendance.student.id: {
            "image": temp_attendance.image,
            "entry_time": temp_attendance.entry_time
        }
        for temp_attendance in temporary_attendances
    }

    if day:
        # Use real attendance table for "attended"
        attendance_query = select(Attendance).where(
            and_(
                Attendance.timetable_id == timetable_id,
                Attendance.date == day,
                Attendance.attended != True
            )
        )
        attendance_result = await db.execute(attendance_query)
        attendance_records = attendance_result.scalars().all()
        # attended_student_ids = {att.student_id for att in attendance_records}
        unattended_student_ids = {att.student_id for att in attendance_records}
        attended_student_ids = {student.id for student in all_students if student.id not in unattended_student_ids}

    else:
        # Use temporary DB for "attended"
        attended_student_ids = set(student_attendance_data.keys())

    student_list = [
        {
            "id": student.id,
            "student_id": student.student_id,
            "name": student.name,
            "surname": student.surname,
            "attended": student.id in attended_student_ids,
            "timetable_id": timetable_id,
            "attendance_percentage": sum(
                att.percentage for att in student.attendance if att.timetable_id == timetable_id
            ),
            "image": student_attendance_data.get(student.id, {}).get("image"),
            "entry_time": (
                student_attendance_data.get(student.id, {}).get("entry_time").strftime("%H:%M")
                if student_attendance_data.get(student.id, {}).get("entry_time")
                else None
            )
        }
        for student in all_students
    ]

    return student_list


async def students_in_temp_db(db: AsyncSession, timetable_id):
    query = (
        select(TemporaryAttendance)
        .filter(TemporaryAttendance.timetable_id == timetable_id)
        .options(joinedload(TemporaryAttendance.student))
    )

    result = await db.execute(query)
    return result.scalars().all()


async def save_attendance(studentsID: List[int], timetable_id: int, manually_checked_ids: List[int], day: date, db: AsyncSession, current_user):
    check_current_user(current_user)
    today = date.today()
    if day and day < today:
        for student_id in manually_checked_ids:
            result = await db.execute(select(Student).where(Student.id == student_id))
            student = result.scalar_one_or_none()
            if not student:
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Student with id {student_id} not found")

            result = await db.execute(
                select(Attendance).where(
                    Attendance.student_id == student_id,
                    Attendance.timetable_id == timetable_id,
                    Attendance.date == day
                )
            )
            attendance = result.scalar_one_or_none()

            if attendance:
                attendance.percentage = max(0, attendance.percentage - 6.25)
                attendance.attended = True
                db.add(attendance)
        await db.commit()
    for student_id in studentsID:   
        result = await db.execute(select(Student).where(Student.id == student_id))
        student = result.scalar_one_or_none()
        if not student:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Student with id {student_id} not found")

        result = await db.execute(
            select(Attendance).where(
                Attendance.student_id == student_id,
                Attendance.timetable_id == timetable_id,
                Attendance.date == day
            )
        )
        attendance = result.scalar_one_or_none()

        if not attendance:
            result = await db.execute(select(Timetable).where(Timetable.id == timetable_id))
            timetable = result.scalar_one_or_none()
            if not timetable:
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Timetable with id {timetable_id} not found")

            new_attendance = Attendance(
                student_id=student.id,
                timetable_id=timetable.id,
                percentage=6.25,
                date=day
            )
            db.add(new_attendance)

    await db.commit()

    return {"message": "Attenance successfully saved!", "status": 200}
