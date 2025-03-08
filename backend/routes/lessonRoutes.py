from fastapi import APIRouter, Depends, HTTPException
from datetime import date
from fastapi import Body
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.schemas.lessonSchema import LessonCreate, LessonResponse
from backend.utilities.token import get_current_user
from backend.services.Google_apiService import authenticate_google_calendar , get_events_of_date 
from backend.services.lessonService import create_lesson, get_possible_time_slots , generate_full_day_slots , get_user_lessons

router = APIRouter()

@router.post("/create", response_model=LessonResponse )
def create_lesson_endpoint(
    lesson_data: LessonCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Extract user from JWT
):
    """ Endpoint to create a lesson. """
    
    user_id = int(current_user.get("sub"))  # Extract user ID from JWT

    try:
        service = authenticate_google_calendar()
        new_lesson = create_lesson(db, lesson_data, user_id , 0 , service)
        return new_lesson
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.get("/get_lessons")
def fetch_user_lessons(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)  # Extract user from JWT
):
    """
    API endpoint to fetch all lessons for a user.
    """
    user_id = int(current_user.get("sub"))  # Extract user ID from JWT
    try: 
        return get_user_lessons(db, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




    
    
@router.post("/possible_slots")
def possible_time_slots(
    request_data: dict = Body(...),  # Accept raw JSON as a dictionary
    current_user: dict = Depends(get_current_user)  # Extract user from JWT
):
    """Endpoint to find possible time slots for a new lesson."""
    
    try:
        service = authenticate_google_calendar()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    try:
        # Extract values manually
        lesson_date = date.fromisoformat(request_data.get("lesson_date"))
        lesson_type = request_data.get("lesson_type")
        lesson_address = request_data.get("lesson_address")
        lesson_duration = request_data.get("lesson_duration")


        # Validate extracted values
        if not lesson_date or not lesson_type or not lesson_duration:
            raise HTTPException(status_code=400, detail="Missing required fields in request data")

        events = get_events_of_date(service, lesson_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if not events: 
        try : 
           return generate_full_day_slots(lesson_date, lesson_duration)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:

        try:
            slots = get_possible_time_slots(
                lesson_address,
                lesson_duration,
                events
            )    
            return slots
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        
            



        
        

    




   