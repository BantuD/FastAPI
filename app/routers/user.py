from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,models
from ..utils import hash
from typing import List

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

#All users
@router.get('/',status_code=status.HTTP_200_OK,response_model=List[schemas.UserOut])
def getUsers(db: Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return all_users

#Users by id
@router.get('/{id}',response_model=schemas.UserOut,status_code=status.HTTP_302_FOUND)
def getUser(id: int,db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id).first()

    if(not user_query):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user not found')

    return user_query


#Create new user
@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    # now we need to hash the password of the user

    hashed_pwd = hash(user.password)
    user.password = hashed_pwd
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#update user by id

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.UserOut)
def updae_user(id: int,post: schemas.UpdateUser,db: Session=Depends(get_db)):
    find_user = db.query(models.User).filter(models.User.id == id)

    if not find_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User not found')
    
    find_user.update(post.dict(),synchronize_session=False)
    db.commit()
    
    return find_user.first()