from sqlalchemy.orm import Session
from backend.models.lessonModel import Lesson
from backend.schemas.lessonSchema import LessonCreate, LessonResponse
from datetime import datetime


def create_lesson(db: Session, lesson_data: LessonCreate, user_id: int):
    """Creates a new lesson in the database."""
    
    new_lesson = Lesson(
        user_id=user_id,  # Use extracted user_id
        start_time=lesson_data.start_time,
        end_time=lesson_data.end_time,
        location=lesson_data.location,
        status=lesson_data.status,
        lesson_name=lesson_data.lesson_name,
        class_number=lesson_data.class_number,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)

    return LessonResponse(
        id=new_lesson.id,
        user_id=new_lesson.user_id,
        start_time=new_lesson.start_time,
        end_time=new_lesson.end_time,
        location=new_lesson.location,
        status=new_lesson.status,
        lesson_name=new_lesson.lesson_name,
        class_number=new_lesson.class_number,
        created_at=new_lesson.created_at,
        updated_at=new_lesson.updated_at
    )