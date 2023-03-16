from pydantic import BaseModel,EmailStr, conint
from datetime import datetime
from typing import Optional

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
    owner_id:int
    owner:UserOut
   

    class Config:  #because we're using it as pydantic model
        orm_mode = True

class PostWithVotes(BaseModel):
    Post:Post
    votes: int

    class Config:
        orm_mode = True

class UpdatePost(BaseModel):
    title:str
    content:str
    published:bool
    class Config:
        orm_model = True



#Token Section
class Token_data(BaseModel):
    id : Optional[int]

class Token(BaseModel):
    access_token: str
    token_type:str
    

#vote

class Votes(BaseModel):
    post_id: int
    dir: conint(le=1)