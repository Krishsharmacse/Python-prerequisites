from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.params import Body
from typing import Optional
from random import randrange
class post(BaseModel):
    title:str
    content:str
    published:bool=True
    rating: Optional[int]=None

app= FastAPI()
@app.get("/")
async def root():
    return {"message":"Hello World"}

my_post=[{"title":"this is tilu ai ","content":"Tilu ai is more powerful than gemini","id":1},{ "title":"Power of tilu AI","content":"Tilu Ai is much more poerful than other ai tools","id":3 }]

@app.get("/next")
def tiluAI():
    return {"content":my_post}

@app.get("/post/vibe")
def champu():
    return{"message":"HI Bro "}

@app.post("/createposts")
def post_chaha(new_post: post):
    post_dict=new_post.dict()
    post_dict['id']=randrange(0,10000)

   
    my_post.append(post_dict)
    return {"data": post_dict}