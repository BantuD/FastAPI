from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from .. import database,schemas,models
from .. import utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter(prefix="/login",
                    tags=['Login'])

@router.post('/',status_code = status.HTTP_302_FOUND,response_model=schemas.Token) # no response model yet
def loginUser(user_credentials:OAuth2PasswordRequestForm=Depends(),
db: Session=Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        print('Email not found')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'User not found')

    if not utils.verify(user_credentials.password,user.password):
        print('password not found')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Invalid Password')
    
    token = oauth2.create_token(data={"user_id":user.id})
    return {"access_token":token,"token_type":"Bearer"}


   