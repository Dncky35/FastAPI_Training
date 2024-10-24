from fastapi import FastAPI
from .routers import accounts, login, posts, votes

app = FastAPI()

app.include_router(accounts.router)
app.include_router(login.router)
app.include_router(posts.router)
app.include_router(votes.router)

@app.get("/")
async def root():
    return {"message":"welcome to main page"}