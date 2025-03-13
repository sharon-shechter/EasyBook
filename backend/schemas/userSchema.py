from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime
from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    admin: Optional[bool] = False
    email: EmailStr
    password: str  
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    address: Optional[str] = None

class UserResponse(BaseModel):
    user_id: int
    admin: bool  
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str]
    address: Optional[str]
    created_at: datetime.datetime

    class Config:
        from_attributes = True
