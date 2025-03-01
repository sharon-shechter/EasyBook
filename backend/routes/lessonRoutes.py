from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.services.lessonService import LessonServices  
from backend.schemas.lessonSchema import LessonCreate, LessonResponse
from backend.utilities.token import get_current_user


router = APIRouter()

@router.post("/create", response_model=LessonResponse)
def create_lesson_endpoint(
    lesson_data: LessonCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Extract user from JWT
):
    user_id = int(current_user.get("sub"))  # Extract user ID from "sub"
   

    return LessonServices.create_lesson(db, lesson_data, user_id)  
