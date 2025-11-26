from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.templating import Jinja2Templates
from todo.models import Users
from todo.schemas import CreateUserRequest, Token
from todo.utils import hash_password, verify_password
from todo.database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from todo.oath2 import create_access_token


db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="templates")


def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

router = APIRouter(prefix="/auth", tags=["auth"])





### Pages ###
@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

### Endpoints ###
@router.get("")
async def get_user():
    return {'user': 'authenticated'}

# TODO: check if email or username already exists
@router.post("", status_code=status.HTTP_201_CREATED)
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}
