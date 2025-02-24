from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
import datetime
from sqlalchemy.orm import relationship
from backend.database.database import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)  # "Zoom" or "Home"
    status = Column(Integer, default = 0, nullable=False)  
    lesson_name = Column(String, nullable=False)  
    class_number = Column(Integer, nullable=False)  # 1-12
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationship with User (optional, if needed)
    user = relationship("User", back_populates="lessons")
