from fastapi import APIRouter, Depends, status
from todo.models import Users
from todo.schemas import CreateUserRequest, Token
from todo.utils import hash_password, verify_password
from todo.database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone

SECRET_KEY = 'MySuperSecretTemporaryToken'
ALGORITHM = 'HS256'

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

router = APIRouter()

@router.get("/auth")
async def get_user():
    return {'user': 'authenticated'}

# TODO: check if email or username already exists
@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user: CreateUserRequest):

    hashed_pwd = hash_password(user.password)

    new_user = Users(
        email= user.email,
        username= user.username,
        first_name= user.first_name,
        last_name= user.last_name,
        hashed_password= hashed_pwd,
        is_active= user.is_active,
        role= user.role
    )

    db.add(new_user)
    db.commit()

    # pwd_verify = verify_password(user.password, hashed_pwd)
    # print(pwd_verify)

    return {"email": new_user.email, "username": new_user.username, "first_name": new_user.first_name,
                     "last_name": new_user.last_name, "role": new_user.role}


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return "Failed Authentication"
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}
