from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt  # type: ignore
from datetime import datetime, timedelta, UTC
from . import schemas, database, models, config
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    
    #PROVIDE A TIME TO EXPIRE
    expire = datetime.now(UTC) + timedelta(minutes=config.settings.access_token_expire_minutes)
    to_encode.update({"exp":expire})

    jwt_token = jwt.encode(to_encode, config.settings.secret_key, algorithm=config.settings.algorithm)

    return jwt_token

def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Not Valided Credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )

    token = verify_access_token(token, credentials_exception)
    account = db.query(models.Account).filter(models.Account.id == token.id).first()

    return account

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, config.settings.secret_key, algorithms=[config.settings.algorithm])
        id:str = payload.get("account_id")

        if id is None:
            raise credentials_exception
        else: 
            token_data = schemas.Token_Data()
            token_data.id = id
            return token_data
        
    except JWTError:
        raise credentials_exception