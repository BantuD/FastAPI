from jose import JWTError, jwt
from datetime import datetime,timedelta
from . import schemas,database,models
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRETE_KEY
#ALGORITHM
#TOKEN_EXPIRATION_TIME_MINUTES

SECRETE_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
TOKEN_EXPIRATION_TIME_MINUTES = 60

def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRETE_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_token(token:str,credential_exception):
    
    try:

        payload = jwt.decode(token,SECRETE_KEY,algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credential_exception

        token_data = schemas.Token_data(id=id)

    except JWTError:
        raise credential_exception
    
    return token_data
    

def get_current_user(token:str = Depends(oauth2_scheme),db: Session=Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'Could not validate credentials',
                                          headers={"WWW-Authenticate":"Bearer"})
    token_data = verify_token(token,credentials_exception)
    user =  db.query(models.User).filter(models.User.id == token_data.id).first()

    return user
      

