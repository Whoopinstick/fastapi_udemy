from email.policy import default

from fastapi import APIRouter, status, Depends, HTTPException, Path
from typing import Annotated
from todo.database import get_db
from sqlalchemy.orm import Session
from todo.oath2 import get_current_user
from todo.models import Users
from todo.schemas import GetUserRequest
from todo.utils import hash_password

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


router = APIRouter(prefix="/user", tags=["user"])

@router.get("", status_code=status.HTTP_200_OK, response_model=GetUserRequest)
async def get_current_user(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    current_user = db.query(Users).filter(Users.id == user.get('id')).first()

    return GetUserRequest(username=current_user.username, email=current_user.email,first_name=current_user.first_name,
                          last_name=current_user.last_name,role=current_user.role)

@router.put("/change_password", status_code=status.HTTP_202_ACCEPTED)
async def change_current_user_password(new_password: str, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    current_user_record = db.query(Users).filter(Users.id == user.get('id')).first()

    if not current_user_record:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Record Not Found")

    new_hashed_password = hash_password(new_password)
    current_user_record.hashed_password = new_hashed_password

    db.add(current_user_record)
    db.commit()
