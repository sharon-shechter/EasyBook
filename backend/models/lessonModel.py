from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Time
from datetime import datetime
from sqlalchemy.orm import relationship
from backend.database.database import Base

class Lesson(Base):
    __tablename__ = "lessons"

    lesson_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  
    date = Column(Date, nullable=False)  
    start_time = Column(Time, nullable=False)  
    end_time = Column(Time, nullable=False)
    location = Column(String, nullable=False)  
    adress = Column(String, nullable=True)
    status = Column(Integer, default=0, nullable=False)  
    lesson_name = Column(String, nullable=False)  
    class_number = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="lessons")
