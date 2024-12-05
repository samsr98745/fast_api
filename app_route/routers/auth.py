
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. database import  get_db_session
from .. import models, schemas, utils, oauth2

router = APIRouter(tags=["Authentication"])


# @router.post("/login")
# def login(user_credentials: schemas.LoginUser, db: Session = Depends(get_db_session)):

#     user =  db.query(models.Post_tbl_user).filter(models.Post_tbl_user.email == user_credentials.email).first()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    

#     if not utils.verify_pwd(user_credentials.password, user.password):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    

#     access_token = oauth2.create_access_token(data={"user_id":user.id})
    
#     ## create token
#     ## return token

#     return{"access_token": access_token, "token_type":"bearer"}



@router.post("/login", response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session)):
##### OAuth2request from stores the username i.e email and password in the post form and we can use that 
###### to verify the authentication also we can pass that in form type in postman instead of schemas as above code
    user =  db.query(models.Post_tbl_user).filter(models.Post_tbl_user.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    

    if not utils.verify_pwd(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    ## create token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    ## return token

    return{"access_token": access_token, "token_type":"bearer"}    

