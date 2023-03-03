from fastapi import FastAPI
from .database import engine
from sqlalchemy.orm import Session
from . import models
from .routers import post,user,auth

models.Base.metadata.create_all(bind=engine) #Create the table if doesn't exist

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

