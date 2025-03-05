from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.schemas.lessonSchema import LessonCreate, LessonResponse
from backend.utilities.token import get_current_user
from backend.services.Google_apiService import authenticate_google_calendar , get_events_of_date
from backend.services.lessonService import create_lesson, get_possible_time_slots

router = APIRouter()

@router.post("/create", response_model=LessonResponse)
def create_lesson_endpoint(
    lesson_data: LessonCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Extract user from JWT
):
    """ Endpoint to create a lesson. """
    
    user_id = int(current_user.get("sub"))  # Extract user ID from JWT

    try:
        new_lesson = create_lesson(db, lesson_data, user_id)
        return new_lesson
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/possible_slots")
def possible_time_slots(
    lesson_data: LessonCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Extract user from JWT
):
    """ Endpoint to find possible time slots for a new lesson. """
    try : 
        service = authenticate_google_calendar()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    try:
        events = get_events_of_date(service, lesson_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    try:
        slots = get_possible_time_slots(lesson_data, events)
        return slots
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    

    




   