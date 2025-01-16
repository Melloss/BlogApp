import jwt
from fastapi import HTTPException
from os import getenv
from datetime import datetime,timedelta,timezone

SECRECT_KEY = getenv('JWT_SECRECT_KEY')
ALGORIGHM = getenv("JWT_ALGORITHM")
EXPIRE_MINUTE = getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def create_access_token(data:dict,expire_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expires = datetime.now(timezone.utc) + (expire_delta or timedelta(minutes=float(EXPIRE_MINUTE)))
    to_encode.update({
        "exp":expires
    })
    return jwt.encode(to_encode,SECRECT_KEY,algorithm=ALGORIGHM)
    
def get_user_data(token: str) -> dict:
    try:
        decoded_data = jwt.decode(token,SECRECT_KEY,algorithms=ALGORIGHM)
        return decoded_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400,detail="Token has expired")
    except: 
        raise HTTPException(detail="Invalid Token",status_code=400)