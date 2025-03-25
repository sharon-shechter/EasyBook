from fastapi import HTTPException
from sqlalchemy.orm import Session 
from backend.models.lessonModel import Lesson
from backend.schemas.lessonSchema import LessonCreate
from backend.services.Google_apiService import add_lesson_to_calendar 


def create_lesson(db: Session, lesson_data: LessonCreate, user_id: int ,google_event_id : int , status : int , ): 
    """Creates a new lesson in the database."""
    
    try : 
        db_lesson = Lesson(
            user_id=user_id,
            google_event_id=google_event_id,
            date=lesson_data.date,
            start_time=lesson_data.start_time,
            end_time=lesson_data.end_time,
            lesson_type=lesson_data.lesson_type,
            lesson_adress=lesson_data.lesson_adress,
            status=status,
            lesson_name=lesson_data.lesson_name,
            class_number=lesson_data.class_number
        )

        db.add(db_lesson)
        db.commit()
        db.refresh(db_lesson)

        return db_lesson
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating lesson: {str(e)}")
    
def get_lessons_by_lesson_id(db: Session, lesson_id: int):
    """Fetch all lessons for a user."""
    try:
        lesson =  db.query(Lesson).filter(Lesson.lesson_id == lesson_id).first()
        if not lesson:
            raise HTTPException(status_code=404, detail="No lessons found ")
        return lesson
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching lesson: {str(e)}")
    

def delete_lesson_from_db(db: Session, lesson_id: int):
    """Delete a lesson by ID."""
    try:
        lesson = db.query(Lesson).filter(Lesson.lesson_id == lesson_id).first()
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        db.delete(lesson)
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting lesson: {str(e)}")


def get_all_user_lessons(db: Session, user_id: int):
    """
    Fetch all lessons for a specific user with user details.
    """

    lessons = (
        db.query(Lesson)
        .filter(Lesson.user_id == user_id)
        .all()
    )

    if not lessons:
        raise HTTPException(status_code=404 , detail = "No lessons found for this user")
    return lessons


