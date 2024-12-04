from email import message
from turtle import mode, pos

from fastapi.background import P
from app_route import oauth2
from .. import models, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from .. database import  get_db_session
from typing import List, Optional, Union
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostResponseVote])
#@router.get("/")
def get_posts(db: Session = Depends(get_db_session), current_user: int = Depends(oauth2.get_current_user), limit: int = 5, skip: int =0, search : Optional[str] = ""):
    #get_pst = db.query(models.Post_tbl).filter(models.Post_tbl.title.contains(search)).limit(limit).offset(skip).all()

    #result_query =  db.query(models.Post_tbl, func.count(models.Post_tbl_votes.post_id).label("votes")).join(models.Post_tbl_votes,models.Post_tbl.id == models.Post_tbl_votes.post_id, isouter=True ).group_by(models.Post_tbl.id)
    result_query = (select(models.Post_tbl,func.count(models.Post_tbl_votes.post_id).label("votes")).join(models.Post_tbl_votes,models.Post_tbl.id == models.Post_tbl_votes.post_id,isouter=True).where(models.Post_tbl.title.contains(search))
                    .group_by(models.Post_tbl.id)).limit(limit).offset(skip)
    posts = db.execute(result_query).all()

    pst_out = [
        {
            "Post": Post,
            "votes": vote
        }
        for Post, vote in posts
    ]

    return pst_out
    # # Return serialized response
    #return posts

    #get_pst = db.query(models.Post_tbl).filter(models.Post_tbl.owner_id == current_user.id).all()  ####to get posts only from the individual user loged in 
    #return result 




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db_session), current_user: int = Depends(oauth2.get_current_user) ):
    # new_post = models.Post_tbl(title = post.title, content=post.content,  published=post.published
    # print(current_user.id)


    new_post = models.Post_tbl(owner_id=current_user.id, **post.model_dump())    ### easier way to unpack the dictionary in the pydantic model for the above commented code
    db.add(new_post) ### add it to database
    db.commit()   ### commit the changes
    db.refresh(new_post)   #### same as returning statment to ge the return values after changes
    return new_post


@router.get("/{id}", response_model=schemas.PostResponseVote)
def get_posts(id: int, response: Response, db: Session = Depends(get_db_session), current_user: int = Depends(oauth2.get_current_user)):
    #test_post = db.query(models.Post_tbl).filter(models.Post_tbl.id == id).first()
    test_post_query = (select(models.Post_tbl,func.count(models.Post_tbl_votes.post_id).label("votes")).join(models.Post_tbl_votes,models.Post_tbl.id == models.Post_tbl_votes.post_id,isouter=True)).where(models.Post_tbl.id == id).group_by(models.Post_tbl.id)
    test_post =  db.execute(test_post_query).first()
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    # ##### to check if the user owner of the post before retreving logic 
    # if test_post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised to perform requested action")
    post_out = {
        "Post": test_post[0],
        "votes": test_post[1]
    }

    return post_out

    

#  ### shorter way to raise the http exception      
# # @app.get("/posts/{id}")
# # def get_posts(id: int):
# #     cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
# #     test_post =  cursor.fetchone()   
# #     if not test_post:
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")
# #     return{"post_details": test_post}



@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int,  db: Session = Depends(get_db_session), current_user: int = Depends(oauth2.get_current_user)):

    dele_post = db.query(models.Post_tbl).filter(models.Post_tbl.id == id)
    
    if dele_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesnot exist")
    

    if dele_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised to perform requested action")
    
    dele_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)




@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db_session), current_user: int = Depends(oauth2.get_current_user)):
    
    pst =  db.query(models.Post_tbl).filter(models.Post_tbl.id == id)
    upd_pst = pst.first()
    if upd_pst == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesnot exist")
    

    if upd_pst.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised to perform requested action")
    pst.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return pst.first()