from pydantic import BaseModel
from datetime import time, date, datetime

# Lesson Create Schema
class LessonCreate(BaseModel):
    date: date  
    start_time: time
    end_time: time
    duration: int  
    location: str
    adress: str
    status: int  
    lesson_name: str
    class_number: int


# Lesson Response Schema
class LessonResponse(BaseModel):
    lesson_id: int  
    user_id: int
    date: date  
    start_time: time
    end_time: time
    location: str
    adress: str
    status: int
    lesson_name: str
    class_number: int
    created_at: datetime
    updated_at: datetime

class Config:
    from_attributes = True
