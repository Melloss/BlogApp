from fastapi import Depends,Form
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated, Optional

from ..database import SessionLocal
from .jwt import get_user_data

    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
def get_user(token:str = Depends(oauth2_scheme)) -> dict:
    return get_user_data(token)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

    
    
user_dependency = Annotated[dict,Depends(get_user)]
db_dependency = Annotated[Session,Depends(get_db)]



