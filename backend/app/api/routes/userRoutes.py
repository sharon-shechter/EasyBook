from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.repositories.userRepositorie import delete_user_from_db , get_user_by_email
from app.schemas.userSchema import UserCreate, UserResponse
from app.services.userService import signup_user_service,login_user_service
from app.database.database import get_db
from app.utilities.token import get_current_user
from app.schemas.userSchema import LoginRequest
 
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

@router.get("/get_user/{email}")
def get_user(email: str, db: Session = Depends(get_db) , current_user: dict = Depends(get_current_user)):
    """ get user by user_id"""
    return  get_user_by_email(db, email)

@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db) , current_user: dict = Depends(get_current_user)):
    """ delete user by user_id"""
    return  delete_user_from_db(db, user_id)

    
    
