from sqlalchemy import Column, Integer, String, DateTime
import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    role = Column(String, default="student")
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    class_name = Column(String, nullable=True)
    lesson = Column(String, nullable=True)  
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
