from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.lessons import Lesson
async def get_all_lesson(db: AsyncSession):
    lessons = await db.execute(select(Lesson).options(selectinload(Lesson.teacher)))
    return lessons.scalars().all()