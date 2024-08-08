# import src.models as models
# from fastapi import Depends
# from sqlalchemy.orm import Session
from passlib.context import CryptContext
# from .database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# def check_user_exists(db: Session = Depends(get_db)):

#     all_users_email_id = db.query(models.User).filter(models.User.email_id).all()

#     print(all_users_email_id)
