from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
import datetime
from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    admin = Column(Boolean, nullable=False, default=False)  
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    lessons = relationship("Lesson", back_populates="user")
