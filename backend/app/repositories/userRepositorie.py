from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.userModel import User

def create_user(db: Session, user_data):
    """Create a new user and store hashed password."""
    try:
        db.add(user_data)
        db.commit()
        db.refresh(user_data)
        return user_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")
    
def delete_user_from_db(db: Session, user_id: int):
    """Delete a user by ID."""
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(user)
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")
    
def verigy_existing_user(db: Session, email: str):
    """Check if a user with the email already exists."""
    try:
        user = db.query(User).filter(User.email == email).first()
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

def get_user_by_email(db: Session, email: str):
    """Retrieve a user by email."""
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")
    
def get_user_by_id(db: Session, user_id: int):
    """Retrieve a user by their user_id."""
    try:
        user =  db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")
