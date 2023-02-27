from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

#post Section
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(BaseModel):
    id:int
    title: str
    content: str
    published: bool

    class Config:  #because we're using it as pydantic model
        orm_mode = True

class UpdatePost(BaseModel):
    title:str
    content:str
    published:bool
    class Config:
        orm_model = True


#user section
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id:int
    email: EmailStr
    #password: str
    created_at:datetime

    class Config:
        orm_mode = True

class UpdateUser(BaseModel):
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token_data(BaseModel):
    id : Optional[int]

class Token(BaseModel):
    access_token: str
    token_type:str
    