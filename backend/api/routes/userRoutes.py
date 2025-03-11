from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.repositories.userRepositorie import delete_user_from_db
from backend.schemas.userSchema import UserCreate, UserResponse
from backend.services.userService import signup_user_service,login_user_service
from backend.database.database import get_db
from backend.utilities.token import get_current_user
from backend.schemas.userSchema import LoginRequest
 
router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    new_user = signup_user_service(db, user)
    return new_user

@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    access_token = login_user_service (db, user.email, user.password)
    return access_token

@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db) , current_user: dict = Depends(get_current_user)):
    """ delete user by user_id"""
    return  delete_user_from_db(db, user_id)

    
    
