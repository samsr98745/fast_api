

from typing import Optional, List, Union
from fastapi.background import P
from pydantic import BaseModel, conint, EmailStr, ConfigDict # for defining and validating the schema
from datetime import datetime



## Input base model to validate the send reequest 

### we can also create individual model for each of the api methods and pass it 

## this is the default base model
class PostBase(BaseModel):
    #model_config = ConfigDict(from_attributes=True)
    title: str
    content: str
    published: bool = True
## we an inhiret Post base to to the requried class as below 
### PostCreate will inherit everything from PostBase to this class.
class PostCreate(PostBase):
    pass   



####Pydantic model to validate and filter out respone models so that we get only \
# ###the required fields or filter out sensitive information in the output aswell .

# class PostResponse(BaseModel):
#     title: str
#     content: str
#     published: bool
#     id: int
#     created_at: datetime

#     ## Not required in 2.0 .. if required enable . for the sqlalchemy to unpack the dicnitory for fast api 
#     ## class Config:
#     ##    orm_mode = True
    
class UserResponse(BaseModel):
    #model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    id: int
    created_at: datetime



### inherted title, content, published from the postbase class
class PostResponse(PostBase):
    #model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    owner_id: int


    owner: UserResponse   #### to fetch the deatis of the user who created this post. relationship set up in models 

class PostResponseVote(BaseModel):
    #model_config = ConfigDict(from_attributes=True)
    Post: PostResponse
    votes: int
## for the error message in get post wne id is not present 
### can use exception to by pass this 
class ErrorResponse(BaseModel):
    message: str


###----- user-----------------------------------------------------



class UserCreate(BaseModel):
    email: EmailStr
    password: str



##### moved above for the post response to use it 

# class UserResponse(BaseModel):
#     email: EmailStr
#     id: int
#     created_at: datetime

###----- login-----------------------------------------------------


class LoginUser(BaseModel):
    email: EmailStr
    password: str

####-------------------------Token ---------------------------
class Token(BaseModel):
    access_token: str
    token_type: str



class TokenData(BaseModel):
    id: Optional[int] = None



class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)