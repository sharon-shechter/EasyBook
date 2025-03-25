from fastapi import HTTPException
from datetime import date
from sqlalchemy.orm import Session
from backend.services.lessonService import get_possible_time_slots, generate_full_day_slots , create_lesson_service, delete_lesson_service
from backend.services.Google_apiService import authenticate_google_calendar , get_events_of_date
from backend.repositories.lessonRepositorie import get_all_user_lessons
from backend.schemas.lessonSchema import LessonCreate
from backend.schemas.lessonSchema import LessonResponse
from backend.services.userService import signup_user_service
from backend.schemas.userSchema import UserCreate



# Tool function for lesson creation
def create_lesson_tool(lesson_data: LessonCreate, db: Session, user_id: int):
    try:
        service = authenticate_google_calendar()
        new_lesson = create_lesson_service(db, lesson_data, user_id, 0, service)
        return new_lesson
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create lesson - {e}")


# Tool function for deleting a lesson
def delete_lesson_tool(lesson_id: int, db: Session, user_id: int):
    try:
        service = authenticate_google_calendar()
        delete_lesson_service(lesson_id, user_id, service, db)
        return {"status": "success", "message": "Lesson deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete lesson - {e}")


# Tool function for fetching all lessons
def get_lessons_tool(db: Session, user_id: int):
    try:
        lessons = get_all_user_lessons(db, user_id)
        return [LessonResponse.from_orm(lesson).dict() for lesson in lessons]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch lessons - {e}")


def possible_time_slots_tool(lesson_date: str , lesson_address: str, lesson_duration: int, user_id: int):
    """Find possible time slots for a lesson in a readable format."""
    try:
        service = authenticate_google_calendar()
        lesson_date_obj = date.fromisoformat(lesson_date)
        events = get_events_of_date(service, lesson_date_obj)
        if not events:
            slots = generate_full_day_slots(lesson_date_obj, lesson_duration)
        else:
            slots = get_possible_time_slots(lesson_address, lesson_duration, events)
        print ("slots", slots)

        formatted_slots = [
            f"From {start.strftime('%Y-%m-%d %H:%M')} to {end.strftime('%Y-%m-%d %H:%M')}"
            for start, end in slots
        ]

        return formatted_slots  

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding time slots: {str(e)}")
    
def user_signup_tool(user_data: UserCreate, db: Session):
    try:

        new_user = signup_user_service(db, user_data)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user - {e}")
    

    


        
