from fastapi import APIRouter,HTTPException,Path
from pydantic import BaseModel,EmailStr

from ..utils.dependencies import db_dependency,user_dependency
from ..utils.hashing import hash_password,verify_password
from ..utils.jwt import create_access_token
from ..models import User
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class UserRequest(BaseModel):
    first_name : str
    last_name : str
    email : EmailStr
    password : str
    profile_image : str

class UserUpdateRequest(BaseModel):
    first_name : str
    last_name : str
    email : EmailStr
    profile_image : str
    
class UserResponse(BaseModel):
    id: int
    first_name : str
    last_name : str
    email : EmailStr
    profile_image : str

class LoginForm(BaseModel):
    email: EmailStr
    password: str

    
     
@router.post('/register',status_code=201)
def register_user(db:db_dependency,user:UserRequest) -> UserResponse:
    new_user = User(
        first_name = user.first_name,
        last_name = user.last_name,
        email = user.email,
        hashed_password = hash_password(user.password.strip()),
        profile_image = user.profile_image,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post('/login',status_code=201,responses={
    201: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "first_name": "str",
                        "last_name": "str",
                        "email":"user@example.com",
                        "token": "*****"
                        
                    }
                }
            },
        }
})
def login_user(db:db_dependency,login_form:LoginForm) -> dict:
    logger.info("logging started")
    user = db.query(User).filter(User.email == login_form.email).first()
    if user:
        if  verify_password(login_form.password,user.hashed_password):
            return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email":user.email,
            "token":create_access_token({
                "id":user.id,
                "email":user.email,
            }
    )}
    raise HTTPException(detail="Email or Password is not correct",status_code=404)
   
    
@router.put('/user')
def update_user(db:db_dependency,user:user_dependency,updated_user: UserUpdateRequest) -> UserResponse:
    requested_user = db.query(User).filter(User.id == user.get('id')).first()
    if requested_user:
        requested_user.first_name  = updated_user.first_name
        requested_user.last_name  = updated_user.last_name
        requested_user.email = updated_user.email
        register_user.profile_image = updated_user.profile_image
        db.commit()
        db.refresh(requested_user)
        return requested_user
    raise HTTPException("User not found")

@router.get("/me")
def who_am_i(db:db_dependency,user: user_dependency) -> UserResponse:
    user = db.query(User).filter(User.id == user.get("id")).first()
    if user:
        return user
    raise HTTPException("User not found")
        
        
    