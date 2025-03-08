from sqlalchemy.orm import Session
from backend.models.userModel import User
from backend.schemas.userSchema import UserCreate
from backend.utilities.hash import hash_password



def create_user(db: Session, user: UserCreate):
    """Create a new user and store hashed password."""
    hashed_password = hash_password(user.password)
    db_user = User(
        admin=user.admin,
        email=user.email,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        address=user.address,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    try:
        return db.query(User).filter(User.email == email).first()
    except Exception as e:
        return (f"no user found with this email {str(e)}")

def get_user_name_by_id(db: Session, user_id: int):
    """Retrieve a user's full name by their user_id."""
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        return f"{user.first_name} {user.last_name}"
    except Exception as e:
        return (f"no user found with this id {str(e)}")
