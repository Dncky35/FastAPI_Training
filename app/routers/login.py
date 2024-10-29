from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, models, utils, oauth2, schemas

router = APIRouter(
    prefix="/login",
    tags=["Authenticate"],
)

@router.post("/", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Token)
async def login(credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):

    if not credentials.password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Password should be provided")
    
    if not credentials.username:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Email should be provided")

    account = db.query(models.Account).filter(models.Account.email == credentials.username).first()

    if not account:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verifyer(credentials.password, account.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    
    access_token = oauth2.create_access_token(data = {"account_id":account.id})
    return {"access_token": access_token, "token_type":"Bearer"}