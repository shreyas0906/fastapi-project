from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserOut(BaseModel):
    id: int
    email_id: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut 

    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True
    owner_id: int

class PostCreate(PostBase):
    pass

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


class ResponseModel(PostCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    
    email_id : EmailStr
    password: str

class UserResponse(BaseModel):

    id : int
    email_id : EmailStr
    created_at : datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):

    email_id : EmailStr
    password : str

class Token(BaseModel):

    access_token : str
    token_type : str

class TokenData(BaseModel):

    id: Optional[str] = None

class Vote(BaseModel):

    post_id: int
    dir: int = Field(..., le=1, ge=0)