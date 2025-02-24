from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Define status values as integers
PENDING = 0
CONFIRMED = 1
COMPLETED = 2

# Lesson Creation Schema
class LessonCreate(BaseModel):
    start_time: datetime
    end_time: datetime
    location: str  # "Zoom" or "Home"
    status: Optional[int] = PENDING  # Status as an integer
    lesson_name: str
    class_number: int

# Lesson Response Schema
class LessonResponse(BaseModel):
    id: int
    user_id: int
    start_time: datetime
    end_time: datetime
    location: str
    status: int  
    lesson_name: str
    class_number: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True




