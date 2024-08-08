from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter 
from fastapi import status #as response_status
from ..schemas import UserResponse, UserCreate
from ..utils import get_hashed_password
from ..database import get_db
from .. import models


router = APIRouter(prefix="/users", tags=['Users'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user( user: UserCreate, db: Session = Depends(get_db)):

    hashed_password = get_hashed_password(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.model_dump())

    if new_user is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Couldn't create a user")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested user not found")
    
    return user