from passlib.context import  CryptContext

pwd =  CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash(password: str): #return hashed String
    return pwd.hash(password)

def verify(plain_password,encrypted_passowrd):
    return pwd.verify(plain_password,encrypted_passowrd)



