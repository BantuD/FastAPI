from fastapi import FastAPI,Depends,HTTPException,status
import psycopg2
from typing import Optional,List
from psycopg2.extras import RealDictCursor
import time
#from passlib.context import CryptContext
from .database import engine
from sqlalchemy.orm import Session
from .database import get_db,Base
from . import models
from .routers import post,user,auth

models.Base.metadata.create_all(bind=engine) #Create the table if doesn't exist

app = FastAPI()

#pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='bantu123',
                                cursor_factory=RealDictCursor)
        print("Connection to the databse successful")
        break

    except Exception as error:
        print(f'Connection to the database is failed: {error}')
        time.sleep(2)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

