from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.services.lessonService import create_lesson  
from backend.schemas.lessonSchema import LessonCreate, LessonResponse
from backend.utilities.token import get_current_user
from fastapi import HTTPException


router = APIRouter()

@router.post("/create", response_model=LessonResponse)
def create_lesson_endpoint(
    lesson_data: LessonCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Extract user from JWT
):
    print(current_user)
    user_id = int(current_user.get("sub"))  # Extract user ID from "sub"

    return create_lesson(db, lesson_data, user_id)  