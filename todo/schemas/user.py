from pydantic import BaseModel, Field

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str = Field(min_length=2, max_length=200)
    last_name: str = Field(min_length=2, max_length=200)
    password: str
    role: str
    is_active: bool = True


class GetUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool = True


class Token(BaseModel):
    access_token: str
    token_type: str