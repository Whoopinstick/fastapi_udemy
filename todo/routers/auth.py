from fastapi import APIRouter
from todo.models import Users
from todo.schemas import CreateUserRequest
router = APIRouter()

@router.get("/auth")
async def get_user():
    return {'user': 'authenticated'}

@router.post("/auth")
async def create_user(user: CreateUserRequest):
    new_user = Users(
        email= user.email,
        username= user.username,
        first_name= user.first_name,
        last_name= user.last_name,
        hashed_password= user.password,
        is_active= user.is_active,
        role= user.role
    )
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