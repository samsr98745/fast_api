
from sqlalchemy import *

from psycopg import *
from sqlalchemy.orm import *

from sqlalchemy.ext.declarative import declarative_base

from app_route.routers import user
### defining our schema to create the table in db


Base = declarative_base()
class Post_tbl(Base):
    __tablename__ = "posts_orm"


    id = mapped_column(Integer, primary_key=True, nullable=True)
    title = mapped_column(String, nullable=False)
    content = mapped_column(String, nullable=False)
    published = mapped_column(Boolean, server_default='True', nullable=False)
    created_at = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id =  mapped_column(Integer, ForeignKey("posts_user.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("Post_tbl_user")   #### setup a relation to the user table 


###--------------User creation table-------------------------


class Post_tbl_user(Base):
    __tablename__ = "posts_user"


    id = mapped_column(Integer, primary_key=True, nullable=True)
    email = mapped_column(String, nullable=False, unique=True)
    password = mapped_column(String, nullable=False)
    created_at = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


####-----------------------votes---------------------------------
class Post_tbl_votes(Base):
     __tablename__ = "posts_vote"

     user_id =  mapped_column(Integer, ForeignKey("posts_user.id", ondelete="CASCADE"), primary_key=True, nullable=False)
     post_id =  mapped_column(Integer, ForeignKey("posts_orm.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    
