from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.userModel import User
from app.repositories.userRepositorie import get_user_by_email, create_user, get_user_by_id , verigy_existing_user
from app.utilities.hash import hash_password, verify_password
from app.utilities.token import create_access_token
from app.schemas.userSchema import UserCreate

def signup_user_service(db: Session, user: UserCreate):
    """Handles user signup with email validation and password hashing."""
    existing_user =verigy_existing_user(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    db_user = create_user(db, User(
        admin=user.admin,
        email=user.email,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        address=user.address,
    ))

    return db_user

def login_user_service(db: Session, email: str, password: str):
    """Authenticates a user and returns a JWT token."""
    db_user = get_user_by_email(db, email)
    if not db_user or not verify_password(password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": str(db_user.user_id)})
    return {"access_token": access_token, "token_type": "bearer"}


def get_user_full_name(db: Session, user_id: int):
    """Retrieve a user's full name."""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return f"{user.first_name} {user.last_name}"

