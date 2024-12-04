

from fastapi import FastAPI
from . import models
from .database import  engine
from . routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware



## sqlalchemy 
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

##### cors 
origins = ["*"]   #### ["www.youtube.com", "www.google.com"]  set the websites that allow all the api to be accesed

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  ### will only allow specific requests
    allow_headers=["*"],
)


@app.get("/")
def get_hello():
    return {"message":"hello world"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
    


#settings