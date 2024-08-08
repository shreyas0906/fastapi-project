from fastapi import APIRouter, Response, Depends, HTTPException
from fastapi import status as response_status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from .. import schemas
from .. import models
from .. import database 
from .. import utils
from .. import oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/login", status_code=response_status.HTTP_202_ACCEPTED, response_model=schemas.Token)
def login(payload:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # user = db.query(models.User).filter(models.User.email_id == payload.email_id).first()
    """
    since payload is now a OAuth2PasswordRequestForm, it contains only two fields,
    username and password. Since we are using form data now, login from postman must be using forms 
    and not payload
    """
    user = db.query(models.User).filter(models.User.email_id == payload.username).first()

    if user is None:
        raise HTTPException(status_code=response_status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # hashed_password = utils.get_hashed_password(payload.password)

    # if hashed_password != user.password:
    #     raise HTTPException(status_code=response_status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    
    if not utils.verify_password(payload.password, user.password):
        raise HTTPException(status_code=response_status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    # create and return JWT token.

    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token" : access_token, "token_type": "bearer"}