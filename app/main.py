from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import accounts, login, posts, votes

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(accounts.router)
app.include_router(login.router)
app.include_router(posts.router)
app.include_router(votes.router)

@app.get("/")
async def root():
    return {"message":"welcome to updated main page"}