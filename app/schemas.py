from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime

class Account(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True  # Instead of orm_mode = True

class Account_Creation(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Token_Data(BaseModel):
    id: Optional[str] = None

class Post(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    published: bool
    owner: Account

class Post_Creation(BaseModel):
    title: str
    content: str
    published: bool = True

class Vote(BaseModel):
    post_id :int
    dir: conint(le=1) #type: ignore

class Post_Show(BaseModel):
    Post: Post
    votes: int
