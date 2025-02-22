from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    role: Optional[str] = "student"
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    class_name: Optional[str] = None
    lesson: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    role: str
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str]
    address: Optional[str]
    class_name: Optional[str]
    lesson: Optional[str]

    class Config:
        from_attributes = True
