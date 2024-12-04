from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import  get_db_session
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"]  ## to group the functionality in docs
)


@router.get("/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db_session)):
    get_users = db.query(models.Post_tbl_user).all()
    return get_users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_post(users: schemas.UserCreate, db: Session = Depends(get_db_session) ):

    existing_user = db.query(models.Post_tbl_user).filter(models.Post_tbl_user.email == users.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hash_pswd = utils.hash_func(users.password)

    user_data = users.model_dump()
    user_data["password"] = hash_pswd
    new_user = models.Post_tbl_user(**user_data)    ### easier way to unpack the dictionary in the pydantic model for the above commented code
    db.add(new_user) ### add it to database
    db.commit()   ### commit the changes
    db.refresh(new_user)   #### same as returning statment to ge the return values after changes
    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, response: Response, db: Session = Depends(get_db_session)):
    user = db.query(models.Post_tbl_user).filter(models.Post_tbl_user.id == id).first()
    

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} doesnot exist")
    return user