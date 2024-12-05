
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from yaml import Token
from sqlalchemy.orm import Session

from . import schemas, database, models
from .config import settings  ### env variables

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')  ## 'login' is the path opertion name in auth.py 

## SECRET_KEY
##Algorithm
## Expiration time

SECRET_KEY = settings.jwt_secret_key  ### random string:  openssl rand -hex 32
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

#### creating acces token 
def create_access_token(data: dict):
    to_encode = data.copy()  ### data that has to be passed in token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

#### verifying access token created

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        payload_id = payload.get("user_id") ### user_id come from the where we have paseed in to create a token in auth.py login
        if payload_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id= payload_id)


    except JWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session =  Depends(database.get_db_session)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentials", headers={"WWW-Authenticate":"Bearer"})

    token =  verify_access_token(token, credentials_exception)
    user = db.query(models.Post_tbl_user).filter(models.Post_tbl_user.id == token.id).first()

    
    
    return user
