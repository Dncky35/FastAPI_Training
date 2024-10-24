from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import database, models, schemas, utils

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Account)
async def create_account(account: schemas.Account_Creation, db:Session = Depends(database.get_db)):
    hashed_password = utils.hasher(account.password)
    account.password = hashed_password

    new_account = models.Account(**account.dict())
    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account