from fastapi import APIRouter
from todo.models import Users
from todo.schemas import CreateUserRequest
from todo.utils import hash_password, verify_password

router = APIRouter()

@router.get("/auth")
async def get_user():
    return {'user': 'authenticated'}

@router.post("/auth")
async def create_user(user: CreateUserRequest):

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

    # pwd_verify = verify_password(user.password, hashed_pwd)
    # print(pwd_verify)
    return new_user

'''
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    '''