from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.userSchema import UserCreate, UserResponse
from backend.services.userService import get_user_by_email, create_user
from backend.database.database import get_db
from backend.models.userModel import User
from backend.utilities.hash import verify_password
from backend.utilities.token import create_access_token
from backend.schemas.userSchema import LoginRequest
 
router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = create_user(db, user)
    return new_user

@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": str(db_user.id)})
    
    return {"access_token": access_token, "token_type": "bearer"}